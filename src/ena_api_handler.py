import yaml
import logging

from ena_swagger_client import swagger_client

study_fetch_fields = 'study_accession,secondary_study_accession,study_description,study_name,study_title,center_name,' \
                     'broker_name,last_updated,first_public'

run_fetch_fields = 'base_count,read_count,instrument_platform,instrument_model,library_layout,library_source,' \
                   'secondary_study_accession,library_strategy,sample_accession,last_updated,first_public,fastq_ftp,' \
                   'scientific_name,tax_id,study_title,sample_title,run_accession,environment_biome,' \
                   'environment_feature,environment_material'


def load_ena_credentials(path):
    try:
        with open(path, 'r') as f:
            creds = yaml.load(f)
            assert len(creds['USERNAME']) > 0
            assert len(creds['PASSWORD']) > 0
            return creds
    except FileNotFoundError:
        logging.error('Ena credentials file not found at: ./' + path)
        raise
    except (yaml.YAMLError, TypeError, AssertionError) as e:
        e.message = 'Could not load ENA credentials, check yaml config file'
        raise e


class EnaApiHandler:
    def __init__(self, ena_credentials_path, extra_options=None):
        try:
            ena_creds = load_ena_credentials(ena_credentials_path)
        except:
            raise
        self.configuration = swagger_client.Configuration()
        self.configuration.username = ena_creds['USERNAME']
        self.configuration.password = ena_creds['PASSWORD']
        self.api = swagger_client.PortalAPIApi(swagger_client.ApiClient(self.configuration))
        self.default_options = {
            'data_portal': 'metagenome',
            'format': 'tsv'
        }
        if extra_options:
            self.default_options.update(extra_options)

    def get_updated_studies(self, cutoff_date):
        raw_results = self.api.search_using_get('study',
                                                query='last_updated>=' + cutoff_date,
                                                fields=study_fetch_fields,
                                                **self.default_options)
        if len(raw_results) == 0:
            return {}
        raw_headers, *rows = raw_results.split('\n')
        headers = raw_headers.split('\t')
        data = {}
        logging.info('Found {} studies to update'.format(len(rows)))
        for row in list(filter(lambda x: len(x) > 0, rows)):
            row_data = row.split('\t')
            entry = {header: value for header, value in zip(headers, row_data)}
            data[entry['secondary_study_accession']] = entry
        return data

    def get_study(self, secondary_study_accession):
        raw_results = self.api.search_using_get('study',
                                                query='secondary_study_accession=' + secondary_study_accession,
                                                fields=study_fetch_fields,
                                                **self.default_options)
        if len(raw_results) == 0:
            raise ValueError('Study {} does not exist in ENA'.format(secondary_study_accession))
        raw_headers, *rows = raw_results.split('\n')
        headers = raw_headers.split('\t')
        row_data = rows[0].split('\t')
        data = {header: value for header, value in zip(headers, row_data)}
        return data

    def get_updated_runs(self, cutoff_date):
        raw_results = self.api.search_using_get('read_run',
                                                query='last_updated>=' + cutoff_date,
                                                fields=run_fetch_fields,
                                                **self.default_options)
        if len(raw_results) == 0:
            return {}
        raw_headers, *rows = raw_results.split('\n')
        headers = raw_headers.split('\t')
        data = {}
        logging.info('Found {} runs to update'.format(len(rows)))

        for row in list(filter(lambda x: len(x) > 0, rows)):
            row_data = row.split('\t')
            run_data = {header: value for header, value in zip(headers, row_data)}
            run_accession = run_data['run_accession']
            data[run_accession] = run_data
        return data

    def get_run(self, run_accession):
        raw_results = self.api.search_using_get('read_run',
                                                query='run_accession=' + run_accession,
                                                fields=run_fetch_fields,
                                                **self.default_options)
        if len(raw_results) == 0:
            raise ValueError('Run {} does not exist in ENA'.format(run_accession))
        raw_headers, *rows = raw_results.split('\n')
        headers = raw_headers.split('\t')
        row_data = rows[0].split('\t')
        data = {header: value for header, value in zip(headers, row_data)}
        return data

    def get_updated_assemblies(self, cutoff_date):
        raw_results = self.api.search_using_get('analysis',
                                                query='analysis_type=SEQUENCE_ASSEMBLY'
                                                      ' AND last_updated>=' + cutoff_date,
                                                fields='analysis_accession,analysis_alias,'
                                                       'first_public,last_updated,secondary_study_accession',
                                                **self.default_options)
        if len(raw_results) == 0:
            return {}
        raw_headers, *rows = raw_results.split('\n')
        headers = raw_headers.split('\t')
        data = {}
        logging.info('Found {} assemblies to update'.format(len(rows)))
        for row in list(filter(lambda x: len(x) > 0, rows)):
            row_data = row.split('\t')
            entry = {header: value for header, value in zip(headers, row_data)}
            data[entry['analysis_accession']] = entry
        return data