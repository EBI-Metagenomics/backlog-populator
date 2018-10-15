from unittest import TestCase, mock
import os
from datetime import datetime

from ..utils import ena_creds_path, write_creds_file, db_name, date_to_str, clear_database, Study, Run, Assembly, \
    sync_time, ena_api_handler_options, mocked_requests_get, mock_invalid_run_get_request, num_fixture_studies, \
    num_fixture_runs, num_fixture_assemblies, mock_invalid_study_get_request

from src import sync, ena_api_handler


class TestSync(TestCase):
    future_date = datetime.now() + sync_time
    past_date = datetime.now() - sync_time
    ena_handler = None

    @classmethod
    def setUpClass(cls):
        write_creds_file()

    def setUp(self):
        clear_database()
        self.ena_handler = ena_api_handler.EnaApiHandler(ena_creds_path, ena_api_handler_options)

    def test_sync_studies_future_date_should_insert_nothing(self):
        sync.sync_studies(self.ena_handler, db_name, date_to_str(self.future_date))
        self.assertEqual(len(Study.objects.using(db_name).all()), 0)

    def test_sync_runs_future_date_should_insert_nothing(self):
        sync.sync_runs(self.ena_handler, db_name, date_to_str(self.future_date), {})
        self.assertEqual(len(Run.objects.using(db_name).all()), 0)

    def test_sync_analyses_future_date_should_insert_nothing(self):
        sync.sync_assemblies(self.ena_handler, db_name, date_to_str(self.future_date), {}, {})
        self.assertEqual(len(Assembly.objects.using(db_name).all()), 0)

    @mock.patch('swagger_client.ApiClient.request', side_effect=mocked_requests_get)
    def test_sync_studies_past_date_should_insert_correct_number_of_studies(self, mock_get):
        studies = sync.sync_studies(self.ena_handler, db_name, date_to_str(self.past_date))
        self.assertEqual(len(Study.objects.using(db_name).all()), num_fixture_studies)
        self.assertEqual(len(studies), num_fixture_studies)

    @mock.patch('swagger_client.ApiClient.request', side_effect=mocked_requests_get)
    def test_sync_runs_past_date_should_insert_correct_number_of_runs(self, mock_get):
        runs = sync.sync_runs(self.ena_handler, db_name, date_to_str(self.past_date), {})
        self.assertEqual(len(Run.objects.using(db_name).all()), num_fixture_runs)
        self.assertEqual(len(runs), num_fixture_runs)

    # First study in mocked request will be missing primary_study_accession, this should be caught by the script
    @mock.patch('swagger_client.ApiClient.request', new=mock_invalid_study_get_request)
    def test_sync_studies_handle_illegal_api_response(self):
        studies = sync.sync_studies(self.ena_handler, db_name, date_to_str(self.past_date))
        self.assertEqual(len(studies), 1)
        self.assertEqual(len(Study.objects.using(db_name).all()), 1)

    # Second run in mocked request will be missing base_count, this should be caught by the script
    @mock.patch('swagger_client.ApiClient.request', new=mock_invalid_run_get_request)
    def test_sync_runs_handle_illegal_api_response(self):
        runs = sync.sync_runs(self.ena_handler, db_name, date_to_str(self.past_date), {})
        self.assertEqual(len(runs), 1)
        self.assertEqual(len(Run.objects.using(db_name).all()), 1)

    @mock.patch('swagger_client.ApiClient.request', side_effect=mocked_requests_get)
    def test_sync_assemblies_past_date_should_insert_correct_number_of_assemblies(self, mock_get):
        assemblies = sync.sync_assemblies(self.ena_handler, db_name, date_to_str(self.past_date), {}, {})
        self.assertEqual(len(Assembly.objects.using(db_name).all()), num_fixture_assemblies)
        self.assertEqual(len(assemblies), num_fixture_assemblies)

    def tearDown(self):
        clear_database()

    @classmethod
    def tearDownClass(cls):
        if os.path.exists(ena_creds_path):
            os.remove(ena_creds_path)
