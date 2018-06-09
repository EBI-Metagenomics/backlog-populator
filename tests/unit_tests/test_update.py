from unittest import TestCase, mock
import argparse
from datetime import datetime
from dateutil.relativedelta import relativedelta
from src import update
import os
from swagger_client import ApiClient

from ..utils import ena_creds_path, write_creds_file, db_name, clear_database, Study, Run, Assembly, \
    ena_api_handler_options, mocked_requests_get
from src import ena_api_handler

class TestSync(TestCase):
    @classmethod
    def setUpClass(cls):
        write_creds_file()

    def setUp(self):
        clear_database()

    def test_argparse_should_not_accept_valid_db_names(self):
        try:
            update.parse_args(['-d', 'illegal_db', '-c', '2018-01-01'])
        except SystemExit as e:
            self.assertIsInstance(e.__context__, argparse.ArgumentError)
        else:
            raise ValueError('Illegal DB name error not raised')

    def test_argparse_should_accept_valid_db_names(self):
        dbs = ['default', 'dev', 'prod']
        for db in dbs:
            args = update.parse_args(['-d', db, '-c', '2018-01-01'])
            self.assertEquals(db, args.database)

    def test_argparse_should_raise_error_if_invalid_date(self):
        invalid_date = 'invalid_date'
        try:
            update.parse_args(['-c', invalid_date])
        except SystemExit as e:
            self.assertIsInstance(e.__context__, argparse.ArgumentError)
        else:
            raise ValueError('Illegal date format error not raised')

    def test_argparse_should_accept_valid_date(self):
        str_date = '2018-01-01'
        args = update.parse_args(['-c', str_date])
        self.assertEquals(str_date, args.cutoffdate)

    @mock.patch('swagger_client.ApiClient.request', side_effect=mocked_requests_get)
    def test_main(self, mock_get):
        cutoff = (datetime.now().date() - relativedelta(days=1)).strftime('%Y-%m-%d')
        update.main(['-c', cutoff, '--database', 'default'])
        ena_handler = ena_api_handler.EnaApiHandler(ena_creds_path, ena_api_handler_options)
        studies = ena_handler.get_updated_studies(cutoff)
        runs = ena_handler.get_updated_runs(cutoff)
        assemblies = ena_handler.get_updated_assemblies(cutoff)

        db_studies = Study.objects.using(db_name).all()
        db_runs = Run.objects.using(db_name).all()
        db_assemblies = Assembly.objects.using(db_name).all()

        self.assertEqual(len(studies), len(db_studies))
        self.assertEqual(len(runs), len(db_runs))
        self.assertEqual(len(assemblies), len(db_assemblies))

    def tearDown(self):
        clear_database()

    @classmethod
    def tearDownClass(cls):
        if os.path.exists(ena_creds_path):
            os.remove(ena_creds_path)
