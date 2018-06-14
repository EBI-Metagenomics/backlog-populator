from datetime import datetime
import os
import logging

import django.db

os.environ['DJANGO_SETTINGS_MODULE'] = 'db.settings'

django.setup()

from backlog.models import Study, Run, Assembly


def sanitise_string(text):
    return ''.join([i if ord(i) < 128 else ' ' for i in text])


def get_date(data, field):
    try:
        date = datetime.strptime(data[field], "%Y-%m-%d").date()
    except (ValueError, KeyError):
        date = datetime.now().date()
    return date


def create_study_obj(data):
    # TODO Missing fields: first created, pubmed, webin
    # TODO First created / last updated are auto-set by django model
    logging.info('Saving study {}'.format(data['secondary_study_accession']))
    s = Study(primary_accession=data['study_accession'],
              secondary_accession=data['secondary_study_accession'],
              title=sanitise_string(data['study_title']),
              public=get_date(data, 'first_public') <= datetime.now().date(),
              ena_last_update=get_date(data, 'last_updated'),
              )
    return s


def create_run_obj(ena_api, database, studies, data):
    logging.info('Saving run {} to study {}'.format(data['run_accession'], data['secondary_study_accession']))

    study_acc = data['secondary_study_accession']
    if study_acc not in studies or studies[study_acc].id is None:
        logging.info('Study {} not found in cache, fetching...'.format(study_acc))
        studies[study_acc] = fetch_study(ena_api, database, study_acc)

    r = Run(study=studies[study_acc],
            primary_accession=data['run_accession'],
            base_count=data['base_count'],
            read_count=data['read_count'],
            instrument_platform=sanitise_string(data['instrument_platform']),
            instrument_model=sanitise_string(data['instrument_model']),
            library_strategy=sanitise_string(data['library_strategy']),
            library_layout=sanitise_string(data['library_layout']),
            library_source=sanitise_string(data['library_source']),
            ena_last_update=get_date(data, 'last_updated'),
            biome_validated=False
            )
    r.clean_fields()
    return r


def create_assembly(ena_api, database, studies, data):
    logging.info('Saving analysis {}'.format(data['analysis_accession']))

    study_acc = data['secondary_study_accession']
    if study_acc not in studies or studies[study_acc].id is None:
        logging.info('Study {} not found in cache, fetching...'.format(study_acc))
        studies[study_acc] = fetch_study(ena_api, database, study_acc)
    a = Assembly(study=studies[study_acc],
                 primary_accession=data['analysis_accession'],
                 ena_last_update=get_date(data, 'last_updated'),
                 )
    return a


def fetch_study(ena_api, database, secondary_study_accession):
    backlog_study = Study.objects.using(database).filter(secondary_accession=secondary_study_accession)
    if len(backlog_study) == 0:
        study = create_study_obj(ena_api.get_study(secondary_study_accession))
        study.save()
    else:
        study = backlog_study[0]
    return study


def fetch_run(ena_api, database, studies, run_accession):
    backlog_run = Run.objects.using(database).filter(primary_accession=run_accession)
    if len(backlog_run) == 0:
        run_data = ena_api.get_run(run_accession)
        run = create_run_obj(ena_api, database, studies, run_data)
        run.save()
    else:
        run = backlog_run[0]
    return run
