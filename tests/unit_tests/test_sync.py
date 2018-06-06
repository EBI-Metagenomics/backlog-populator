from unittest import TestCase
import os
from datetime import datetime

from ..utils import ena_creds_path, write_creds_file, db_name, date_to_str, clear_database, Study, Run, Assembly, \
    sync_time, ena_api_handler_options

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
        self.assertEquals(len(Study.objects.using(db_name).all()), 0)

    def test_sync_runs_future_date_should_insert_nothing(self):
        sync.sync_runs(self.ena_handler, db_name, date_to_str(self.future_date), {})
        self.assertEquals(len(Run.objects.using(db_name).all()), 0)

    def test_sync_analyses_future_date_should_insert_nothing(self):
        sync.sync_assemblies(self.ena_handler, db_name, date_to_str(self.future_date), {}, {})
        self.assertEquals(len(Assembly.objects.using(db_name).all()), 0)

    def test_sync_studies_past_date_should_insert_correct_number_of_studies(self):
        studies = sync.sync_studies(self.ena_handler, db_name, date_to_str(self.past_date))
        self.assertEquals(len(Study.objects.using(db_name).all()), len(studies))

    def test_sync_runs_past_date_should_insert_correct_number_of_runs(self):
        runs = sync.sync_runs(self.ena_handler, db_name, date_to_str(self.past_date), {})
        self.assertEquals(len(Run.objects.using(db_name).all()), len(runs))

    def test_sync_analyses_past_date_should_insert_correct_number_of_assembliess(self):
        assemblies = sync.sync_assemblies(self.ena_handler, db_name, date_to_str(self.past_date), {}, {})
        self.assertEquals(len(Assembly.objects.using(db_name).all()), len(assemblies))

    def tearDown(self):
        clear_database()

    @classmethod
    def tearDownClass(cls):
        if os.path.exists(ena_creds_path):
            os.remove(ena_creds_path)
