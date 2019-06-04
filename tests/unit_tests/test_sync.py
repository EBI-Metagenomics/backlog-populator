import os
from datetime import datetime

import pytest
from unittest.mock import patch

from tests.utils import ena_creds_path, write_creds_file, date_to_str, clear_database, Study, Run, Assembly, RunAssembly, \
    sync_time, mocked_ena_study_query, mocked_ena_read_run_query, mocked_ena_invalid_study_response, \
    mocked_ena_invalid_runs_response, mocked_ena_assemblies_query, mocked_ena_assembles_multiple_in_same_study_query

from src.update import Updater, parse_args

from ena_portal_api import ena_handler


class TestUpdater:
    future_date = datetime.now() + sync_time
    past_date = datetime.now() - sync_time
    updater = None

    @classmethod
    def setup_class(cls):
        write_creds_file()

    def setup_method(self):
        clear_database()

    def teardown_method(self):
        clear_database()

    @classmethod
    def teardown_class(cls):
        if os.path.exists(ena_creds_path):
            os.remove(ena_creds_path)

    # def test_sync_studies_future_date_should_insert_nothing(self):
    #     updater = Updater(parse_args(['-c', date_to_str(self.future_date)]))
    #     updater.sync_studies()
    #     assert len(Study.objects.all()) == 0
    #
    # def test_sync_runs_future_date_should_insert_nothing(self):
    #     updater = Updater(parse_args(['-c', date_to_str(self.future_date)]))
    #     updater.sync_runs()
    #     assert len(Run.objects.all()) == 0
    #
    # def test_sync_analyses_future_date_should_insert_nothing(self):
    #     updater = Updater(parse_args(['-c', date_to_str(self.future_date)]))
    #     updater.sync_mgnify_assemblies()
    #     assert len(Assembly.objects.all()) == 0
    #
    # def test_sync_studies_past_date_should_insert_correct_number_of_studies(self):
    #     updater = Updater(parse_args(['-c', date_to_str(self.past_date)]))
    #     updater.ena_api.get_updated_studies = mocked_ena_study_query
    #     updater.sync_studies()
    #     assert len(Study.objects.all()) == len(mocked_ena_study_query())
    #
    # def test_sync_studies_should_not_create_duplicates(self):
    #     updater = Updater(parse_args(['-c', date_to_str(self.past_date)]))
    #     updater.ena_api.get_updated_studies = mocked_ena_study_query
    #     updater.sync_studies()
    #     updater.sync_studies()
    #     assert len(Study.objects.all()) == len(mocked_ena_study_query())
    #
    # def test_sync_runs_past_date_should_insert_correct_number_of_runs(self):
    #     updater = Updater(parse_args(['-c', date_to_str(self.past_date)]))
    #     updater.ena_api.get_updated_runs = mocked_ena_read_run_query
    #     updater.sync_runs()
    #     assert len(Run.objects.all()) == len(mocked_ena_read_run_query())
    #     assert len(Study.objects.all()) == len(set([run['study_accession'] for run in mocked_ena_read_run_query()]))

    def test_sync_runs_past_date_should_not_create_duplicate(self):
        updater = Updater(parse_args(['-c', date_to_str(self.past_date)]))
        updater.ena_api.get_updated_runs = mocked_ena_read_run_query
        updater.sync_runs()
        updater.sync_runs()
        assert len(Run.objects.all()) == len(mocked_ena_read_run_query())
        assert len(Study.objects.all()) == len(set([run['study_accession'] for run in mocked_ena_read_run_query()]))

    def test_sync_studies_handle_illegal_api_response(self):
        updater = Updater(parse_args(['-c', date_to_str(self.past_date)]))
        updater.ena_api.get_updated_studies = mocked_ena_invalid_study_response
        updater.sync_studies()
        assert len(Study.objects.all()) == 1

    # Second run in mocked request will be missing base_count, this should be caught by the script
    def test_sync_runs_handle_illegal_api_response(self):
        updater = Updater(parse_args(['-c', date_to_str(self.past_date)]))
        updater.ena_api.get_updated_runs = mocked_ena_invalid_runs_response
        updater.sync_runs()
        assert len(Run.objects.all()) == 1

    def test_sync_mgnify_assemblies_past_date_should_insert_correct_number_of_assemblies(self):
        updater = Updater(parse_args(['-c', date_to_str(self.past_date)]))
        updater.ena_api.get_updated_tpa_assemblies = mocked_ena_assemblies_query
        updater.sync_mgnify_assemblies()
        assert len(Assembly.objects.all()) == len(mocked_ena_assemblies_query())
        # Should create link between assembly and run
        assert len(RunAssembly.objects.all()) == 5

    def test_sync_mgnify_assemblies_past_date_should_not_create_duplicates(self):
        updater = Updater(parse_args(['-c', date_to_str(self.past_date)]))
        updater.ena_api.get_updated_tpa_assemblies = mocked_ena_assemblies_query
        updater.sync_mgnify_assemblies()
        updater.sync_mgnify_assemblies()
        assert len(Assembly.objects.all()) == len(mocked_ena_assemblies_query())
        # Should create link between assembly and run
        assert len(RunAssembly.objects.all()) == 5

    def test_sync_mgnify_assemblies_past_date_should_hit_study_cache(self):
        updater = Updater(parse_args(['-c', date_to_str(self.past_date)]))
        updater.ena_api.get_updated_tpa_assemblies = mocked_ena_assembles_multiple_in_same_study_query
        updater.sync_mgnify_assemblies()
        assert len(Assembly.objects.all()) == len(mocked_ena_assembles_multiple_in_same_study_query())
        # Should create link between assembly and run
        assert len(RunAssembly.objects.all()) == 2
        # One study of assemblies, 1 study of raw data
        assert len(Study.objects.all()) == 2
