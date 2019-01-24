import argparse
from datetime import datetime
import os
import logging
import sys
import json
from ena_portal_api import ena_handler
from mgnify_backlog import mgnify_handler

import backlog_populator.sync as sync


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


cutoff_file = os.environ.get('BACKLOG_SYNC_CUTOFF_FILE', os.path.join(os.path.dirname(__file__), 'cutoff.json'))


def load_cutoff_date():
    if os.path.exists(cutoff_file):
        with open(cutoff_file, 'r') as f:
            return json.load(f)['cutoff-date']


def save_cutoff_date(date):
    with open(cutoff_file, 'w+') as f:
        json.dump({'cutoff-date': date}, f)


def get_studies(db):
    return mgnify_handler.Study.objects.using(db).all()


def get_runs(db):
    return mgnify_handler.Run.objects.using(db).all()


def get_assemblies(db):
    return mgnify_handler.Assembly.objects.using(db).all()


def display_update_stats(db, num_studies, num_runs, num_assemblies):
    new_studies = get_studies(db)
    new_runs = get_runs(db)
    new_assemblies = get_assemblies(db)

    created_studies = new_studies.count() - num_studies
    created_runs = new_runs.count() - num_runs
    created_assemblies = new_assemblies.count() - num_assemblies

    updated_studies = new_studies.filter(ena_last_update=datetime.today().strftime('%Y-%m-%d')).count() - created_studies
    updated_runs = new_runs.filter(ena_last_update=datetime.today().strftime('%Y-%m-%d')).count() - created_runs
    updated_assemblies = new_assemblies.filter(
        ena_last_update=datetime.today().strftime('%Y-%m-%d')).count() - created_assemblies

    logging.info('Created {} studies'.format(created_studies))
    logging.info('Updated {} studies'.format(max(0, updated_studies)))
    logging.info('Created {} runs'.format(created_runs))
    logging.info('Updated {} runs'.format(max(0, updated_runs)))
    logging.info('Created {} assemblies'.format(created_assemblies))
    logging.info('Updated {} assemblies'.format(max(0, updated_assemblies)))


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

    num_studies = get_studies(args.db).count()
    num_runs = get_runs(args.db).count()
    num_assemblies = get_assemblies(args.db).count()

    study_errors = sync.sync_studies(ena, mgnify, cutoff)
    run_errors = sync.sync_runs(ena, mgnify, cutoff)
    assem_errors = sync.sync_assemblies(ena, mgnify, cutoff)

    display_update_stats(args.db, num_studies, num_runs, num_assemblies)

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
            logging.error(cutoff_file)
            save_cutoff_date(datetime.today().strftime('%Y-%m-%d'))


if __name__ == '__main__':
    main()
