import argparse
from enum import Enum
from datetime import datetime
import os
import logging
import sys

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
                        required=True,
                        type=valid_date)
    parser.add_argument('-v', '--verbose', action='store_true', help='Set logging level to DEBUG')
    args = parser.parse_args(raw_args)
    args.database = str(args.database)
    return args


def main(raw_args):
    if sys.version_info.major < 3:
        raise SyntaxError("Must be using Python 3")
    args = parse_args(raw_args)
    log_level = logging.DEBUG if args.verbose else logging.INFO
    logging.basicConfig(filename=os.path.join('~', 'backlog-populator', 'backlog.log'), level=log_level)

    # Setup ENA API module
    ena_handler = ena_api_handler.EnaApiHandler(ena_creds)

    studies = sync.sync_studies(ena_handler, args.database, args.cutoffdate)
    logging.info('Updated {} studies'.format(len(studies)))
    runs = sync.sync_runs(ena_handler, args.database, args.cutoffdate, studies)
    logging.info('Updated {} runs'.format(len(runs)))
    assemblies = sync.sync_assemblies(ena_handler, args.database, args.cutoffdate, studies, runs)
    logging.info('Updated {} assemblies'.format(len(assemblies)))

if __name__ == '__main__':
    main(sys.argv[1:])
