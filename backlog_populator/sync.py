import logging
import os
import django.db
from django.forms.models import model_to_dict
import django.core.exceptions

os.environ['DJANGO_SETTINGS_MODULE'] = 'db.settings'

django.setup()

from backlog.models import Study, Run, RunAssembly
from backlog_populator import mgnify_handler as emg_handler

logging.basicConfig(level=logging.DEBUG)


def save_or_update_studies(studies, database):
    for i, study in enumerate(studies):
        d = model_to_dict(study)
        del d['id']
        studies[i], _ = Study.objects.using(database).update_or_create(primary_accession=d['primary_accession'],
                                                                       secondary_accession=d['secondary_accession'],
                                                                       defaults=d)
    return studies


def sync_studies(ena_api, database, cutoff_date):
    logging.info('Syncing studies')
    ena_studies = ena_api.get_updated_studies(cutoff_date)
    logging.info('Found {} new studies'.format(str(len(ena_studies))))
    studies = {}
    for study, data in ena_studies.items():
        try:
            studies[study] = emg_handler.create_study_obj(data)
        except Exception as e:
            logging.error(e)
            logging.error('Could not insert {}'.format(study))
            continue
    logging.info('Storing studies...')
    studies = {study.secondary_accession: study for study in save_or_update_studies(list(studies.values()), database)}
    logging.info('Finished storing studies')
    return studies


def save_or_update_runs(runs, database):
    for i, run in enumerate(runs):
        d = model_to_dict(run)
        # Remove un-necessary information, fix issue where study is replaced with row id
        del d['id']
        d['study'] = run.study
        runs[i], _ = Run.objects.using(database).update_or_create(primary_accession=d['primary_accession'],
                                                                  defaults=d)
    return runs


def sync_runs(ena_api, database, cutoff_date, studies):
    logging.info('Syncing runs')
    ena_runs = ena_api.get_updated_runs(cutoff_date)
    logging.info('Found {} new runs'.format(str(len(ena_runs))))
    runs = {}
    for run, data in ena_runs.items():
        try:
            runs[run] = emg_handler.create_run_obj(ena_api, database, studies, data)
        except (django.core.exceptions.ValidationError, ValueError, KeyError) as e:
            logging.error(e)
            logging.error('Could not insert {}'.format(run))
            continue
    logging.info('Storing runs...')
    runs = {run.primary_accession: run for run in save_or_update_runs(list(runs.values()), database)}
    logging.info('Finished storing runs')
    return runs


def sync_assemblies(ena_api, database, cutoff_date, studies, runs):
    logging.info('Syncing assemblies')
    ena_assemblies = ena_api.get_updated_assemblies(cutoff_date)
    logging.info('Found {} new assemblies'.format(str(len(ena_assemblies))))
    assemblies = {}
    insertable_assemblies = []
    for assembly, data in ena_assemblies.items():
        try:
            assembly_obj = emg_handler.create_assembly(ena_api, database, studies, data)
            assembly_obj.save(using=database)
            assemblies[assembly] = assembly_obj
            insertable_assemblies.append(assembly)
        except Exception as e:
            logging.error(e)
            continue
    logging.info('Finished storing assemblies')
    link_assemblies_to_runs(ena_api, database, studies, runs, ena_assemblies, assemblies)
    return assemblies


def link_assemblies_to_runs(ena_api, database, studies, runs, ena_assemblies, assemblies):
    run_assemblies = []
    for assembly_accession, assembly in assemblies.items():
        assembly_accession = assembly.primary_accession
        run_accession = ena_assemblies[assembly_accession]['analysis_alias']
        if run_accession[0:3] in ('SRR', 'DRR', 'ERR'):
            if run_accession not in runs:
                try:
                    runs[run_accession] = emg_handler.fetch_run(ena_api, database, studies, run_accession)
                except ValueError as e:
                    logging.error(e)
                    logging.warning(
                        'Could not find a run for assembly {} with alias {}'.format(assembly_accession,
                                                                                    run_accession))
            run_assemblies.append(RunAssembly(assembly=assembly, run=runs[run_accession]))

    try:
        RunAssembly.objects.using(database).bulk_create(run_assemblies)
    except django.db.utils.IntegrityError:
        for run_assembly in run_assemblies:
            run_assembly.save()
    logging.info('Finished linking assemblies to runs in EMG.')
