import yaml
from dateutil import relativedelta
import json

from mgnify_backlog.mgnify_handler import *

db_name = 'default'
date_format = '%Y-%m-%d'
sync_time = relativedelta.relativedelta(weeks=4)

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
    AssemblyJob.objects.all().delete()
    AssemblyJobStatus.objects.all().delete()

    AnnotationJob.objects.all().delete()

    RunAssembly.objects.all().delete()
    RunAssemblyJob.objects.all().delete()
    Run.objects.all().delete()
    Assembly.objects.all().delete()
    Study.objects.all().delete()

    UserRequest.objects.all().delete()
    User.objects.all().delete()

    Pipeline.objects.all().delete()
    Assembler.objects.all().delete()


def fetch_mock_response(filename):
    filepath = os.path.join(os.path.dirname(__file__), 'mock_ena_responses', filename)
    with open(filepath) as f:
        return json.load(f)


class MockResponse:
    def __init__(self, data, status_code):
        self.data = data
        self.status_code = status_code

    def json(self):
        return self.data


def mocked_ena_study_query(*kwargs):
    return fetch_mock_response('studies.json')


def mocked_ena_read_run_query(*kwargs):
    return fetch_mock_response('runs.json')


def mocked_ena_read_assemblies_query(*kwargs):
    return fetch_mock_response('assemblies.json')


def mocked_ena_read_single_study(*kwargs):
    return fetch_mock_response('single_studies.json')


def mocked_ena_invalid_study_response(*kwargs):
    return fetch_mock_response('./invalid_responses/invalid_studies.json')


def mocked_ena_invalid_runs_response(*kwargs):
    return fetch_mock_response('./invalid_responses/runs_missing_counts.json')


def mocked_ena_assemblies_query(*kwargs):
    return fetch_mock_response('assemblies.json')


def mocked_ena_assembles_multiple_in_same_study_query(*kwargs):
    return fetch_mock_response('assemblies_same_study.json')
