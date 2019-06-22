import argparse
import os
import sys
import json
import traceback

import django
import logging
from datetime import datetime
import django.db
import django.core.exceptions

from ena_portal_api import ena_handler
from mgnify_backlog import mgnify_handler

from biome_classifier import load_classifier

ena_creds = os.environ.get('ENA_CREDS_FILE')
cutoff_file = os.environ.get('BACKLOG_SYNC_CUTOFF_FILE', os.path.join(os.path.dirname(__file__), 'cutoff.json'))
DEFAULT_STUDY_FIELDS = 'study_accession,secondary_study_accession,study_description,study_name,study_title,' \
                       'tax_id,scientific_name,center_name,last_updated,first_public'


def valid_date(s):
    try:
        datetime.strptime(s, "%Y-%m-%d")
        return s
    except ValueError:
        msg = "Not a valid date: '{0}'.".format(s)
        raise argparse.ArgumentTypeError(msg)


def parse_args(raw_args):
    parser = argparse.ArgumentParser(description='Tool to update backlog schema from the ENA API')
    parser.add_argument('--db', choices=['default', 'dev', 'prod'], default='default')
    parser.add_argument("-c",
                        "--cutoffdate",
                        help="The Start Date - format YYYY-MM-DD",
                        type=valid_date)
    parser.add_argument('-v', '--verbose', action='store_true', help='Set logging level to DEBUG')
    args = parser.parse_args(raw_args)
    return args


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


class Updater:
    def __init__(self, args):
        self.db = args.db
        self.ena_api = ena_handler.EnaApiHandler()
        self.mgnify = mgnify_handler.MgnifyHandler(args.db)
        self.cutoff = args.cutoffdate or load_cutoff_date() or '1970-01-01'
        self.num_studies = get_studies(args.db).count()
        self.num_runs = get_runs(args.db).count()
        self.num_assemblies = get_assemblies(args.db).count()

        self.biome_classifier = load_classifier.get_model()

    def sync_all(self):
        study_errors = self.sync_studies()
        run_errors = self.sync_runs()
        assem_errors = self.sync_mgnify_assemblies()

        self.display_update_stats()

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
                # Only increment by 6 months if max results were returned
                new_cutoff = datetime.today()
                save_cutoff_date(new_cutoff.strftime('%Y-%m-%d'))

    def sync_studies(self):
        logging.info('Syncing studies')
        ena_studies = self.ena_api.get_updated_studies(self.cutoff, fields=DEFAULT_STUDY_FIELDS)
        logging.info('Found {} new studies'.format(str(len(ena_studies))))
        errors = []
        for study_data in ena_studies:
            try:
                self.mgnify.create_study_obj(study_data)
            except django.db.utils.IntegrityError:
                self.mgnify.update_study_obj(study_data)
            except Exception as e:
                print(traceback.format_exc())
                logging.debug('Could not insert {}'.format(study_data))
                errors.append((study_data['secondary_study_accession'], e))
                continue
        return errors

    def sync_runs(self):
        logging.info('Syncing runs')
        ena_runs = self.ena_api.get_updated_runs(self.cutoff)
        logging.info('Found {} new runs'.format(str(len(ena_runs))))
        study_cache = {}
        errors = []
        for run_data in ena_runs:

            study_prim_accession = run_data['study_accession']
            study_sec_accession = run_data['secondary_study_accession']
            try:
                if run_data['base_count'] == '':
                    run_data['base_count'] = None
                if run_data['read_count'] == '':
                    run_data['read_count'] = None
                if study_prim_accession in study_cache:
                    study = study_cache[study_prim_accession]
                else:
                    tqdm.write('Fetching extra study {} {}'.format(study_prim_accession, study_sec_accession))
                    study = self.mgnify.get_or_save_study(self.ena_api, study_prim_accession, study_sec_accession)
                study_cache[study_prim_accession] = study

                inp = ' '.join([study.title,
                                study.description,
                                study.scientific_name,
                                run_data['library_name'],
                                run_data['sample_alias'],
                                run_data['sample_title'],
                                run_data['sample_description'],
                                ])
                best_lineage_match, prob = self.biome_classifier.pred_input(inp)[0]
                if prob > 0.95:
                    run_data['inferred_lineage'] = best_lineage_match
                self.mgnify.create_run_obj(study, run_data)
            except django.db.utils.IntegrityError:
                self.mgnify.update_run_obj(run_data)
            except (django.core.exceptions.ValidationError, ValueError, KeyError) as e:
                logging.error(e)
                logging.error('Could not insert {}'.format(run_data))
                errors.append((run_data['run_accession'], e))
        return errors

    def sync_mgnify_assemblies(self):
        logging.info('Syncing TPA assemblies')
        ena_assemblies = self.ena_api.get_updated_tpa_assemblies(self.cutoff)
        logging.info('Found {} new assemblies'.format(str(len(ena_assemblies))))
        study_cache = {}
        errors = []
        for assembly_data in ena_assemblies:
            study_prim_accession = assembly_data['study_accession']
            if study_prim_accession in study_cache:
                study = study_cache[study_prim_accession]
            else:
                try:
                    study = self.mgnify.get_or_save_study(self.ena_api, study_prim_accession)
                except ValueError as e:
                    errors.append((study_prim_accession, e))
                    continue
                study_cache[study_prim_accession] = study
            try:
                is_public = datetime.strptime(assembly_data['first_public'], "%Y-%m-%d") < datetime.now()
            except ValueError:
                is_public = False

            inp = ' '.join([study.title,
                            study.description,
                            study.scientific_name,
                            assembly_data['sample_alias'],
                            assembly_data['sample_title'],
                            assembly_data['sample_description'],
                            ])

            best_lineage_match, prob = self.biome_classifier.pred_input(inp)[0]
            if prob > 0.95:
                assembly_data['inferred_lineage'] = best_lineage_match
            try:
                self.mgnify.create_assembly_obj(self.ena_api, study, assembly_data, is_public)
            except django.db.utils.IntegrityError:
                self.mgnify.update_assembly_obj(assembly_data)
            except Exception as e:
                logging.error(e)
                logging.error('Could not insert assembly {}'.format(assembly_data))
                errors.append((assembly_data['analysis_accession'], e))
        return errors

    def display_update_stats(self):
        new_studies = get_studies(self.db)
        new_runs = get_runs(self.db)
        new_assemblies = get_assemblies(self.db)

        created_studies = new_studies.count() - self.num_studies
        created_runs = new_runs.count() - self.num_runs
        created_assemblies = new_assemblies.count() - self.num_assemblies

        updated_studies = new_studies.filter(
            ena_last_update=datetime.today().strftime('%Y-%m-%d')).count() - created_studies
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

    log_level = logging.DEBUG if args.verbose else logging.INFO

    logfile = os.path.join('~', 'backlog-populator', 'backlog.log')
    os.makedirs(os.path.dirname(logfile), exist_ok=True)
    logging.basicConfig(level=log_level)
    updater = Updater(args)
    updater.sync_all()


if __name__ == '__main__':
    main()
