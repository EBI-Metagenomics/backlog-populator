import argparse
from enum import Enum
from datetime import datetime
import os
import logging
import sys
import json
from ena_portal_api import ena_handler
from mgnify_backlog import mgnify_handler

import backlog_populator.sync as sync


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
    parser.add_argument('--db', choices=['default', 'dev', 'prod'], default='default')
    parser.add_argument('-r', '--refresh', action="store_true", help='If set update all data')
    parser.add_argument('-e', '--ena-credentials', help='Path to ena credentials yml file')
    parser.add_argument("-c",
                        "--cutoffdate",
                        help="The Start Date - format YYYY-MM-DD",
                        type=valid_date)
    parser.add_argument('-v', '--verbose', action='store_true', help='Set logging level to DEBUG')
    args = parser.parse_args(raw_args)
    return args


cutoff_file = os.path.join(os.path.dirname(__file__), 'cutoff.json')


def load_cutoff_date():
    if os.path.exists(cutoff_file):
        with open(cutoff_file, 'r') as f:
            return json.load(f)['cutoff-date']


def save_cutoff_date(date):
    with open(cutoff_file, 'w+') as f:
        json.dump({'cutoff-date': date}, f)


def main(raw_args=sys.argv[1:]):
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
    ena = ena_handler.EnaApiHandler()
    mgnify = mgnify_handler.MgnifyHandler(args.db)
    studies_created, studies_updated, study_errors = sync.sync_studies(ena, mgnify, cutoff)
    runs_created, runs_updated, run_errors = sync.sync_runs(ena, mgnify, cutoff)
    assem_created, assem_updated, assem_errors = sync.sync_assemblies(ena, mgnify, cutoff)

    logging.info('Created {} studies'.format(studies_created))
    logging.info('Updated {} studies'.format(studies_updated))
    logging.info('Created {} runs'.format(runs_created))
    logging.info('Updated {} runs'.format(runs_updated))
    logging.info('Created {} assemblies'.format(assem_created))
    logging.info('Updated {} assemblies'.format(assem_updated))

    errors = study_errors + run_errors + assem_errors
    if len(errors) > 10:
        logging.warning('More than 10 update errors occured, see error.log for details')
        with open('error.log', 'w') as f:
            f.writelines([a + ': ' + b for a, b in errors])
    else:
        if 0 < len(errors) <= 10:
            for accession, error in errors:
                logging.error(accession, error)
        else:
            save_cutoff_date(datetime.today().strftime('%Y-%m-%d'))


if __name__ == '__main__':
    main()
