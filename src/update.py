import argparse
from enum import Enum
from datetime import datetime
import os
import logging
import sys
import json
from src import ena_api_handler, sync


class Database(Enum):
    prod = 'prod'
    dev = 'dev'
    default = 'default'

    def __str__(self):
        return self.value


def valid_date(s):
    try:
        datetime.strptime(s, "%Y-%m-%d")
        return s
    except ValueError:
        msg = "Not a valid date: '{0}'.".format(s)
        raise argparse.ArgumentTypeError(msg)


ena_creds = os.path.realpath(os.path.join(os.path.dirname(__file__), os.pardir, 'ena_creds.yml'))


def parse_args(raw_args):
    parser = argparse.ArgumentParser(description='Tool to update backlog schema from the ENA API')
    parser.add_argument('-d', '--database', type=Database, choices=list(Database), default=Database.dev,
                        help='Target database to update')
    parser.add_argument('-r', '--refresh', action="store_true", help='If set update all data')
    parser.add_argument("-c",
                        "--cutoffdate",
                        help="The Start Date - format YYYY-MM-DD",
                        type=valid_date)
    parser.add_argument('-v', '--verbose', action='store_true', help='Set logging level to DEBUG')
    args = parser.parse_args(raw_args)
    args.database = str(args.database)
    return args


cutoff_file = os.path.join(os.path.dirname(__file__), 'cutoff.json')


def load_cutoff_date():
    if os.path.exists(cutoff_file):
        with open(cutoff_file, 'r') as f:
            return json.load(f)['cutoff-date']


def save_cutoff_date(date):
    with open(cutoff_file, 'w+') as f:
        json.dump({'cutoff-date': date}, f)


def main(raw_args):
    if sys.version_info.major < 3:
        raise SyntaxError("Must be using Python 3")
    args = parse_args(raw_args)
    log_level = logging.DEBUG if args.verbose else logging.info
    logging.basicConfig(filename=os.path.join('~', 'backlog-populator', 'backlog.log'), level=log_level)

    if not args.cutoffdate:
        cutoff = load_cutoff_date() or '1970-01-01'
    else:
        cutoff = args.cutoffdate
    # Setup ENA API module
    ena_handler = ena_api_handler.EnaApiHandler(ena_creds)

    studies = sync.sync_studies(ena_handler, args.database, cutoff)
    logging.info('Updated {} studies'.format(len(studies)))
    runs = sync.sync_runs(ena_handler, args.database, cutoff, studies)
    logging.info('Updated {} runs'.format(len(runs)))
    assemblies = sync.sync_assemblies(ena_handler, args.database, cutoff, studies, runs)
    logging.info('Updated {} assemblies'.format(len(assemblies)))

    save_cutoff_date(datetime.today().strftime('%Y-%m-%d'))


if __name__ == '__main__':
    main(sys.argv[1:])
