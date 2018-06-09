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
    filepath = os.path.join(os.path.dirname(__file__), 'mock_responses', filename)
    with open(filepath, 'r') as f:
        return f.read().replace('\n', '')


# This method will be used by the mock to replace requests.get
def mocked_requests_get(*args, **kwargs):
    class MockResponse:
        def __init__(self, json_data, status_code):
            self.data = json.dumps(json_data)
            self.status_code = status_code

        def json(self):
            return self.data

    api_call_result = kwargs['query_params'][0][1]
    response = MockResponse(None, 404)
    if api_call_result == 'study':
        response = MockResponse({"data": fetch_mock_response('studies.txt')}, 200)
    elif api_call_result == 'read_run':
        response = MockResponse({"data": fetch_mock_response('runs.txt')}, 200)
    elif api_call_result == 'analysis':
        response = MockResponse({"data": fetch_mock_response('assemblies.txt')}, 200)
    return response
