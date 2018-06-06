import logging
from src import emg_backlog_handler as emg_handler

logging.basicConfig(level=logging.DEBUG)


def sync_studies(ena_api, database, cutoff_date):
    logging.info('Syncing studies')
    ena_studies = None
    try:
        ena_studies = ena_api.get_updated_studies(cutoff_date)
        logging.info('Found {} new studies'.format(str(len(ena_studies))))
        for study, data in ena_studies.items():
            ena_studies[study] = emg_handler.save_study(database, data)
    except Exception as e:
        logging.error(e)
    return ena_studies


def sync_runs(ena_api, database, cutoff_date, studies):
    logging.info('Syncing runs')
    ena_runs = None
    try:
        ena_runs = ena_api.get_updated_runs(cutoff_date)
        logging.info('Found {} new runs'.format(str(len(ena_runs))))
        for run, data in ena_runs.items():
            ena_runs[run] = emg_handler.save_run(ena_api, database, studies, data)
    except Exception as e:
        logging.error(e)
    return ena_runs


def sync_assemblies(ena_api, database, cutoff_date, studies, runs):
    logging.info('Syncing assemblies')
    ena_assemblies = None
    try:
        ena_assemblies = ena_api.get_updated_assemblies(cutoff_date)
        logging.info('Found {} new assemblies'.format(str(len(ena_assemblies))))
        for assembly_accession, data in ena_assemblies.items():
            try:
                ena_assemblies[assembly_accession] = emg_handler.save_assembly(ena_api, database, studies, runs, data)
            except Exception as e:
                logging.error(e)
                logging.error('Could not store assembly {}'.format(assembly_accession))
    except Exception as e:
        logging.error(e)
    return ena_assemblies
