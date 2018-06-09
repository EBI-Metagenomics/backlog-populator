import logging

from src import ena_api_handler
from src.emg_backlog_handler import Run, Study, Assembly, RunAssembly

from src import emg_backlog_handler as emg_handler

logging.basicConfig(level=logging.DEBUG)


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
            continue
    Study.objects.using(database).bulk_create(studies.values())
    return ena_studies


def sync_runs(ena_api, database, cutoff_date, studies):
    logging.info('Syncing runs')
    ena_runs = ena_api.get_updated_runs(cutoff_date)
    logging.info('Found {} new runs'.format(str(len(ena_runs))))
    runs = {}
    for run, data in ena_runs.items():
        try:
            runs[run] = emg_handler.create_run_obj(ena_api, database, studies, data)
        except Exception as e:
            logging.error(e)
            continue
    Run.objects.using(database).bulk_create(runs.values())
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
            assembly_obj.save()
            assemblies[assembly] = assembly_obj
            insertable_assemblies.append(assembly)
        except Exception as e:
            logging.error(e)
    link_assemblies_to_runs(ena_api, database, studies, runs, ena_assemblies, assemblies)
    return assemblies


def link_assemblies_to_runs(ena_api, database, studies, runs, ena_assemblies, assemblies):
    run_assemblies = []
    for assembly_accession, assembly in assemblies.items():
        assembly_accession = assembly.primary_accession
        run_accession = ena_assemblies[assembly_accession]['analysis_alias']
        if run_accession not in runs:
            try:
                runs[run_accession] = emg_handler.fetch_run(ena_api, database, studies, run_accession)
                run_assemblies.append(RunAssembly(assembly=assembly, run=runs[run_accession]))
            except ValueError as e:
                logging.error(e)
                logging.warning(
                    'Could not find a run for assembly {} with alias {}'.format(assembly_accession,
                                                                                run_accession))
    RunAssembly.objects.using(database).bulk_create(run_assemblies)
    logging.info('Finished linking assemblies to runs in EMG.')


if __name__ == '__main__':
    ena_handler = ena_api_handler.EnaApiHandler('/Users/mdb/work/backlog-populator/travis/ena_creds.yml')
    sync_assemblies(ena_handler, 'default', '2018-06-05', {}, {})
