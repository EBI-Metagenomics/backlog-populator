import logging
import django.db
import django.core.exceptions

from mgnify_util.accession_parsers import is_run_accession

logging.basicConfig(level=logging.DEBUG)


def sync_studies(ena_api, mgnify, cutoff_date):
    logging.info('Syncing studies')
    ena_studies = ena_api.get_updated_studies(cutoff_date)
    logging.info('Found {} new studies'.format(str(len(ena_studies))))
    errors = []
    for study_data in ena_studies:
        try:
            mgnify.create_study_obj(study_data)
        except django.db.utils.IntegrityError:
            mgnify.update_study_obj(study_data)
        except Exception as e:
            logging.debug(e)
            logging.debug('Could not insert {}'.format(study_data))
            errors.append((study_data['secondary_study_accession'], e))
            continue
    return errors


def sync_runs(ena_api, mgnify, cutoff_date):
    logging.info('Syncing runs')
    ena_runs = ena_api.get_updated_runs(cutoff_date)
    logging.info('Found {} new runs'.format(str(len(ena_runs))))
    study_cache = {}
    errors = []
    for run_data in ena_runs:
        study_prim_accession = run_data['study_accession']
        if study_prim_accession in study_cache:
            study = study_cache[study_prim_accession]
        else:
            try:
                study = mgnify.get_or_save_study(ena_api, study_prim_accession)
            except ValueError as e:
                logging.debug(e)
                errors.append((study_prim_accession, e))
                continue
            study_cache[study_prim_accession] = study
        try:
            mgnify.create_run_obj(study, run_data)
        except django.db.utils.IntegrityError:
            mgnify.update_run_obj(run_data)
        except (django.core.exceptions.ValidationError, ValueError, KeyError) as e:
            logging.debug(e)
            logging.debug('Could not insert {}'.format(run_data))
            errors.append((run_data['run_accession'], e))
            continue

    return errors


def sync_assemblies(ena_api, mgnify, cutoff_date):
    logging.info('Syncing assemblies')
    ena_assemblies = ena_api.get_updated_assemblies(cutoff_date)
    logging.info('Found {} new assemblies'.format(str(len(ena_assemblies))))
    study_cache = {}
    errors = []
    for assembly_data in ena_assemblies:
        study_prim_accession = assembly_data['study_accession']
        if study_prim_accession in study_cache:
            study = study_cache[study_prim_accession]
        else:
            try:
                study = mgnify.get_or_save_study(ena_api, study_prim_accession)
            except ValueError as e:
                errors.append((study_prim_accession, e))
                continue
            study_cache[study_prim_accession] = study
        if is_run_accession(assembly_data['assembly_name']):
            run_obj = mgnify.get_or_save_run(ena_api, assembly_data['assembly_name'])
            assembly_data['related_runs'] = [run_obj]
        try:
            mgnify.create_assembly_obj(study, assembly_data)
        except django.db.utils.IntegrityError:
            mgnify.update_assembly_obj(assembly_data)
        except Exception as e:
            logging.debug(e)
            logging.debug('Could not insert assembly {}'.format(assembly_data))
            errors.append((assembly_data['accession'], e))
    return errors
