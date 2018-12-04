from unittest import TestCase, mock
from unittest.mock import patch
from datetime import datetime
import sys
import os
import json
import pytest
from dateutil.relativedelta import relativedelta
from backlog_populator import update

from ..utils import clear_database, Study, Run, Assembly, mocked_ena_study_query, mocked_ena_read_run_query, \
    mocked_ena_assemblies_query

from ena_portal_api import ena_handler


class TestSync(TestCase):
    def setUp(self):
        clear_database()

    @patch.object(ena_handler.EnaApiHandler, 'get_updated_studies', mocked_ena_study_query)
    @patch.object(ena_handler.EnaApiHandler, 'get_updated_runs', mocked_ena_read_run_query)
    @patch.object(ena_handler.EnaApiHandler, 'get_updated_assemblies', mocked_ena_assemblies_query)
    def test_main(self):
        cutoff = (datetime.now().date() - relativedelta(days=1)).strftime('%Y-%m-%d')
        update.main(['-c', cutoff, '--db', 'default'])
        db_studies = Study.objects.all()
        db_runs = Run.objects.all()
        db_assemblies = Assembly.objects.all()
        self.assertEqual(len(db_studies), 11)
        self.assertEqual(len(db_runs), 11)
        self.assertEqual(len(db_assemblies), 5)

    @patch.object(ena_handler.EnaApiHandler, 'get_updated_studies', mocked_ena_study_query)
    @patch.object(ena_handler.EnaApiHandler, 'get_updated_runs', mocked_ena_read_run_query)
    @patch.object(ena_handler.EnaApiHandler, 'get_updated_assemblies', mocked_ena_assemblies_query)
    def test_main_should_write_cutoff_json(self):
        cutoff = (datetime.now().date() - relativedelta(days=1)).strftime('%Y-%m-%d')
        update.main(['-c', cutoff, '--db', 'default'])
        self.assertTrue(os.path.exists(update.cutoff_file))
        with open(update.cutoff_file, 'r') as f:
            self.assertEqual(json.load(f)['cutoff-date'], datetime.today().strftime('%Y-%m-%d'))

    @patch.object(ena_handler.EnaApiHandler, 'get_updated_studies', mocked_ena_study_query)
    @patch.object(ena_handler.EnaApiHandler, 'get_updated_runs', mocked_ena_read_run_query)
    @patch.object(ena_handler.EnaApiHandler, 'get_updated_assemblies', mocked_ena_assemblies_query)
    def test_main_should_read_cutoff_json(self):
        cutoff = (datetime.now().date() - relativedelta(days=1)).strftime('%Y-%m-%d')
        with open(update.cutoff_file, 'w') as f:
            json.dump({'cutoff-date': cutoff}, f)
        self.assertTrue(os.path.exists(update.cutoff_file))

        update.main(['--db', 'default'])

        with open(update.cutoff_file, 'r') as f:
            self.assertEqual(json.load(f)['cutoff-date'], datetime.today().strftime('%Y-%m-%d'))

        db_studies = Study.objects.all()
        db_runs = Run.objects.all()
        db_assemblies = Assembly.objects.all()
        self.assertEqual(len(db_studies), 11)
        self.assertEqual(len(db_runs), 11)
        self.assertEqual(len(db_assemblies), 5)

    def tearDown(self):
        pass
        # clear_database()


def test_main_python_vers():
    with pytest.raises(SyntaxError, message='Did not detect execution with Python 2.x.x'):
        with mock.patch.object(sys, 'version_info') as v_info:
            v_info.major = 2
            cutoff = (datetime.now().date() - relativedelta(days=1)).strftime('%Y-%m-%d')
            update.main(['-c', cutoff, '--db', 'default'])
