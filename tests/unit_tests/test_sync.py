import os
from datetime import datetime

from unittest.mock import patch

from ..utils import ena_creds_path, write_creds_file, date_to_str, clear_database, Study, Run, Assembly, RunAssembly, \
    sync_time, mocked_ena_study_query, mocked_ena_read_run_query, mocked_ena_invalid_study_response, \
    mocked_ena_invalid_runs_response, mocked_ena_assemblies_query, mocked_ena_assembles_multiple_in_same_study_query

from backlog_populator import sync

from mgnify_backlog import mgnify_handler
from ena_portal_api import ena_handler


class TestSync:
    future_date = datetime.now() + sync_time
    past_date = datetime.now() - sync_time
    ena = None
    mgnify = None

    @classmethod
    def setup_class(cls):
        write_creds_file()

    def setup_method(self):
        clear_database()
        self.ena = ena_handler.EnaApiHandler()
        self.mgnify = mgnify_handler.MgnifyHandler('default')

    def teardown_method(self):
        clear_database()

    @classmethod
    def teardown_class(cls):
        if os.path.exists(ena_creds_path):
            os.remove(ena_creds_path)

    def test_sync_studies_future_date_should_insert_nothing(self):
        sync.sync_studies(self.ena, self.mgnify, date_to_str(self.future_date))
        assert len(Study.objects.all()) == 0

    def test_sync_runs_future_date_should_insert_nothing(self):
        sync.sync_runs(self.ena, self.mgnify, date_to_str(self.future_date))
        assert len(Run.objects.all()) == 0

    def test_sync_analyses_future_date_should_insert_nothing(self):
        sync.sync_assemblies(self.ena, self.mgnify, date_to_str(self.future_date))
        assert len(Assembly.objects.all()) == 0

    @patch.object(ena_handler.EnaApiHandler, 'get_updated_studies', mocked_ena_study_query)
    def test_sync_studies_past_date_should_insert_correct_number_of_studies(self):
        sync.sync_studies(self.ena, self.mgnify, date_to_str(self.past_date))
        assert len(Study.objects.all()) == len(mocked_ena_study_query())

    @patch.object(ena_handler.EnaApiHandler, 'get_updated_studies', mocked_ena_study_query)
    def test_sync_studies_should_not_create_duplicates(self):
        sync.sync_studies(self.ena, self.mgnify, date_to_str(self.past_date))
        sync.sync_studies(self.ena, self.mgnify, date_to_str(self.past_date))
        assert len(Study.objects.all()) == len(mocked_ena_study_query())

    @patch.object(ena_handler.EnaApiHandler, 'get_updated_runs', mocked_ena_read_run_query)
    def test_sync_runs_past_date_should_insert_correct_number_of_runs(self):
        sync.sync_runs(self.ena, self.mgnify, date_to_str(self.past_date))
        assert len(Run.objects.all()) == len(mocked_ena_read_run_query())
        assert len(Study.objects.all()) == len(set([run['study_accession'] for run in mocked_ena_read_run_query()]))

    @patch.object(ena_handler.EnaApiHandler, 'get_updated_runs', mocked_ena_read_run_query)
    def test_sync_runs_past_date_should_not_create_duplicate(self):
        sync.sync_runs(self.ena, self.mgnify, date_to_str(self.past_date))
        sync.sync_runs(self.ena, self.mgnify, date_to_str(self.past_date))
        assert len(Run.objects.all()) == len(mocked_ena_read_run_query())
        assert len(Study.objects.all()) == len(set([run['study_accession'] for run in mocked_ena_read_run_query()]))

    # First study in mocked request will be missing primary_study_accession, this should be caught by the script
    @patch.object(ena_handler.EnaApiHandler, 'get_updated_studies', mocked_ena_invalid_study_response)
    def test_sync_studies_handle_illegal_api_response(self):
        sync.sync_studies(self.ena, self.mgnify, date_to_str(self.past_date))
        assert len(Study.objects.all()) == 1

    # Second run in mocked request will be missing base_count, this should be caught by the script
    @patch.object(ena_handler.EnaApiHandler, 'get_updated_runs', mocked_ena_invalid_runs_response)
    def test_sync_runs_handle_illegal_api_response(self):
        sync.sync_runs(self.ena, self.mgnify, date_to_str(self.past_date))
        assert len(Run.objects.all()) == 1

    @patch.object(ena_handler.EnaApiHandler, 'get_updated_assemblies', mocked_ena_assemblies_query)
    def test_sync_assemblies_past_date_should_insert_correct_number_of_assemblies(self):
        sync.sync_assemblies(self.ena, self.mgnify, date_to_str(self.past_date))
        assert len(Assembly.objects.all()) == len(mocked_ena_assemblies_query())
        # Should create link between assembly and run
        assert len(RunAssembly.objects.all()) == 1

    @patch.object(ena_handler.EnaApiHandler, 'get_updated_assemblies', mocked_ena_assemblies_query)
    def test_sync_assemblies_past_date_should_not_create_duplicates(self):
        sync.sync_assemblies(self.ena, self.mgnify, date_to_str(self.past_date))
        sync.sync_assemblies(self.ena, self.mgnify, date_to_str(self.past_date))
        assert len(Assembly.objects.all()) == len(mocked_ena_assemblies_query())
        # Should create link between assembly and run
        assert len(RunAssembly.objects.all()) == 1

    @patch.object(ena_handler.EnaApiHandler, 'get_updated_assemblies',
                  mocked_ena_assembles_multiple_in_same_study_query)
    def test_sync_assemblies_past_date_should_hit_study_cache(self):
        sync.sync_assemblies(self.ena, self.mgnify, date_to_str(self.past_date))
        assert len(Assembly.objects.all()) == len(mocked_ena_assembles_multiple_in_same_study_query())
        # Should create link between assembly and run
        assert len(RunAssembly.objects.all()) == 2
        # One study of assemblies, 1 study of raw data
        assert len(Study.objects.all()) == 2
