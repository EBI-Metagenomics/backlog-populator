from datetime import datetime
import os
import logging

import django.db

os.environ['DJANGO_SETTINGS_MODULE'] = 'db.settings'

django.setup()

from backlog.models import Study, Run, Assembly, RunAssembly


def sanitise_string(text):
    return ''.join([i if ord(i) < 128 else ' ' for i in text])


def get_date(data, field):
    try:
        date = datetime.strptime(data[field], "%Y-%m-%d").date()
    except ValueError:
        date = datetime.now().date()
    return date


def save_study(database, data):
    # TODO Missing fields: first created, pubmed, webin
    # TODO First created / last updated are auto-set by django model
    logging.info('Saving study {}'.format(data['secondary_study_accession']))

    # try:
    s = Study(primary_accession=data['study_accession'],
              secondary_accession=data['secondary_study_accession'],
              title=sanitise_string(data['study_title']),
              public=get_date(data, 'first_public') <= datetime.now().date(),
              ena_last_update=get_date(data, 'last_updated'),
              )
    s.save(using=database)
    # except django.db.IntegrityError:
    #     logging.warning('Django IntegrityError occured when retrieving {}', data['study_accession'])
    #     s = Study.objects.using(database).get(primary_accession=data['study_accession'])
    return s


def save_run(ena_api, database, studies, data):
    logging.info('Saving run {} to study {}'.format(data['run_accession'], data['secondary_study_accession']))

    study_acc = data['secondary_study_accession']
    if study_acc not in studies:
        studies[study_acc] = fetch_study(ena_api, database, study_acc)
    r = Run(study=studies[study_acc],
            primary_accession=data['run_accession'],
            base_count=data['base_count'],
            read_count=data['read_count'],
            instrument_platform=sanitise_string(data['instrument_platform']),
            instrument_model=sanitise_string(data['instrument_model']),
            library_strategy=sanitise_string(data['library_strategy']),
            library_layout=sanitise_string(data['library_layout']),
            ena_last_update=get_date(data, 'last_updated'),
            biome_validated=False
            )
    r.save(using=database)
    return r


def save_assembly(ena_api, database, studies, runs, data):
    logging.info('Saving analysis {}'.format(data['analysis_accession']))

    study_acc = data['secondary_study_accession']
    run_accession = data['analysis_alias']
    if study_acc not in studies:
        studies[study_acc] = fetch_study(ena_api, database, study_acc)
    a = Assembly(study=studies[study_acc],
                 primary_accession=data['analysis_accession'],
                 ena_last_update=get_date(data, 'last_updated'),
                 )
    a.save()

    if run_accession not in runs:
        try:
            runs[run_accession] = fetch_run(ena_api, database, studies, run_accession)
        except ValueError as e:
            logging.warning('Could not find a run for assembly {} with alias {}'.format(data['analysis_accession'],
                                                                                        run_accession))
        else:
            ra = RunAssembly(assembly=a, run=runs[run_accession])
            ra.save()
    return a


def fetch_study(ena_api, database, secondary_study_accession):
    backlog_study = Study.objects.using(database).filter(secondary_accession=secondary_study_accession)
    if len(backlog_study) == 0:
        study = save_study(database, ena_api.get_study(secondary_study_accession))
    else:
        study = backlog_study[0]
    return study


def fetch_run(ena_api, database, studies, run_accession):
    backlog_run = Run.objects.using(database).filter(primary_accession=run_accession)
    if len(backlog_run) == 0:
        run_data = ena_api.get_run(run_accession)
        run = save_run(ena_api, database, studies, run_data)
    else:
        run = backlog_run[0]
    return run
