import os
import yaml
from datetime import datetime
from dateutil import relativedelta
import django.db
import json

os.environ['DJANGO_SETTINGS_MODULE'] = 'db.settings'

django.setup()

from backlog.models import Study, Run, Assembly, RunAssembly

db_name = 'default'
date_format = '%Y-%m-%d'
sync_time = relativedelta.relativedelta(weeks=1)

ena_api_handler_options = {
    'limit': 10
}

ena_creds_path = os.path.realpath(os.path.join(os.path.dirname(__file__), os.pardir, 'ena_creds_test.yml'))

mock_fixtures_path = os.path.join(os.path.dirname(__file__), 'mock_ena_responses')
with open(os.path.join(mock_fixtures_path, 'studies.json')) as f:
    num_fixture_studies = len(json.load(f))

with open(os.path.join(mock_fixtures_path, 'runs.json')) as f:
    num_fixture_runs = len(json.load(f))

with open(os.path.join(mock_fixtures_path, 'assemblies.json')) as f:
    num_fixture_assemblies = len(json.load(f))


def write_creds_file():
    data = {
        'USERNAME': os.environ['ENA_USERNAME'],
        'PASSWORD': os.environ['ENA_PASSWORD']
    }
    with open(ena_creds_path, 'w') as f:
        yaml.dump(data, f)


def str_to_date(string):
    return datetime.strptime(string, date_format).date()


def date_to_str(date):
    return date.strftime(date_format)


def clear_database():
    RunAssembly.objects.using(db_name).all().delete()
    Assembly.objects.using(db_name).all().delete()
    Run.objects.using(db_name).all().delete()
    Study.objects.using(db_name).all().delete()


def fetch_mock_response(filename):
    filepath = os.path.join(os.path.dirname(__file__), 'mock_ena_responses', filename)
    with open(filepath, 'r') as f:
        return f.read()


class MockResponse:
    def __init__(self, data, status_code):
        self.data = data
        self.status_code = status_code

    def json(self):
        return self.data


# This method will be used by the mock to replace requests.get
def mocked_requests_get(*args, **kwargs):
    api_call_result = kwargs['query_params'][0][1]
    response = MockResponse(None, 404)
    if api_call_result == 'study':
        query_filter = kwargs['query_params'][1][1]
        if "secondary_study_accession" in query_filter:
            study_fixture = query_filter.replace('secondary_study_accession=', '') + '.json'
            response = MockResponse(fetch_mock_response(os.path.join('single_studies', study_fixture)), 200)
        else:
            response = MockResponse(fetch_mock_response('studies.json'), 200)
    elif api_call_result == 'read_run':
        response = MockResponse(fetch_mock_response('runs.json'), 200)
    elif api_call_result == 'analysis':
        response = MockResponse(fetch_mock_response('assemblies.json'), 200)
    return response


# Run includes 1 lacking read / base count
def mock_invalid_run_get_request(*args, **kwargs):
    api_call_result = kwargs['query_params'][0][1]
    response = MockResponse(None, 404)
    if api_call_result == 'study':
        study_fixture = kwargs['query_params'][1][1].replace('secondary_study_accession=', '') + '.json'
        response = MockResponse(fetch_mock_response(os.path.join('single_studies', study_fixture)), 200)
    elif api_call_result == 'read_run':
        response = MockResponse(fetch_mock_response(os.path.join('invalid_responses', 'runs_missing_counts.json')), 200)
    return response
