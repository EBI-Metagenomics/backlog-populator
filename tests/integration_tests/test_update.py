from unittest import TestCase, mock
from datetime import datetime
import sys
import json

import pytest
from dateutil.relativedelta import relativedelta
from backlog_populator import update
import os

from ..utils import ena_creds_path, write_creds_file, db_name, clear_database, Study, Run, Assembly, \
    ena_api_handler_options, mocked_requests_get, num_fixture_studies, num_fixture_runs, num_fixture_assemblies
from backlog_populator import ena_api_handler


class TestSync(TestCase):
    @classmethod
    def setUpClass(cls):
        write_creds_file()

    def setUp(self):
        clear_database()

    @mock.patch('swagger_client.ApiClient.request', new=mocked_requests_get)
    def test_main(self):
        cutoff = (datetime.now().date() - relativedelta(days=1)).strftime('%Y-%m-%d')
        update.main(['-c', cutoff, '--database', 'default'])
        ena_handler = ena_api_handler.EnaApiHandler(ena_creds_path, ena_api_handler_options)
        studies = ena_handler.get_updated_studies(cutoff)
        runs = ena_handler.get_updated_runs(cutoff)
        assemblies = ena_handler.get_updated_assemblies(cutoff)

        db_studies = Study.objects.using(db_name).all()
        db_runs = Run.objects.using(db_name).all()
        db_assemblies = Assembly.objects.using(db_name).all()

        self.assertEqual(len(studies), num_fixture_studies)
        self.assertEqual(len(db_studies), num_fixture_studies)
        self.assertEqual(len(runs), num_fixture_runs)
        self.assertEqual(len(db_runs), num_fixture_runs)
        self.assertEqual(len(assemblies), num_fixture_assemblies)
        self.assertEqual(len(db_assemblies), num_fixture_assemblies)

    @mock.patch('swagger_client.ApiClient.request', new=mocked_requests_get)
    def test_main_should_write_cutoff_json(self):
        cutoff = (datetime.now().date() - relativedelta(days=1)).strftime('%Y-%m-%d')
        update.main(['-c', cutoff, '--database', 'default'])
        self.assertTrue(os.path.exists(update.cutoff_file))
        with open(update.cutoff_file, 'r') as f:
            self.assertEqual(json.load(f)['cutoff-date'], datetime.today().strftime('%Y-%m-%d'))

    @mock.patch('swagger_client.ApiClient.request', new=mocked_requests_get)
    def test_main_should_read_cutoff_json(self):
        cutoff = (datetime.now().date() - relativedelta(days=1)).strftime('%Y-%m-%d')
        with open(update.cutoff_file, 'w') as f:
            json.dump({'cutoff-date': cutoff}, f)
        self.assertTrue(os.path.exists(update.cutoff_file))
        update.main(['--database', 'default'])
        with open(update.cutoff_file, 'r') as f:
            self.assertEqual(json.load(f)['cutoff-date'], datetime.today().strftime('%Y-%m-%d'))

        ena_handler = ena_api_handler.EnaApiHandler(ena_creds_path, ena_api_handler_options)
        studies = ena_handler.get_updated_studies(cutoff)
        runs = ena_handler.get_updated_runs(cutoff)
        assemblies = ena_handler.get_updated_assemblies(cutoff)

        db_studies = Study.objects.using(db_name).all()
        db_runs = Run.objects.using(db_name).all()
        db_assemblies = Assembly.objects.using(db_name).all()

        self.assertEqual(len(studies), num_fixture_studies)
        self.assertEqual(len(db_studies), num_fixture_studies)
        self.assertEqual(len(runs), num_fixture_runs)
        self.assertEqual(len(db_runs), num_fixture_runs)
        self.assertEqual(len(assemblies), num_fixture_assemblies)
        self.assertEqual(len(db_assemblies), num_fixture_assemblies)

    def tearDown(self):
        clear_database()

    @classmethod
    def tearDownClass(cls):
        if os.path.exists(ena_creds_path):
            os.remove(ena_creds_path)


def test_main_python_vers():
    with pytest.raises(SyntaxError, message='Did not detect execution with Python 2.x.x'):
        with mock.patch.object(sys, 'version_info') as v_info:
            v_info.major = 2
            cutoff = (datetime.now().date() - relativedelta(days=1)).strftime('%Y-%m-%d')
            update.main(['-c', cutoff, '--database', 'default'])
