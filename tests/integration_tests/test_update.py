from datetime import datetime
from unittest import mock
from unittest.mock import patch
import sys
import os
import json
import pytest
from dateutil.relativedelta import relativedelta
from backlog_populator import update

from ..utils import clear_database, Study, Run, Assembly, mocked_ena_study_query, mocked_ena_read_run_query, \
    mocked_ena_assemblies_query

from ena_portal_api import ena_handler


class TestSync:
    @classmethod
    def setup_method(cls):
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
        assert len(db_studies) == 5
        assert len(db_runs) == 10
        assert len(db_assemblies) == 5

    @patch.object(ena_handler.EnaApiHandler, 'get_updated_studies', mocked_ena_study_query)
    @patch.object(ena_handler.EnaApiHandler, 'get_updated_runs', mocked_ena_read_run_query)
    @patch.object(ena_handler.EnaApiHandler, 'get_updated_assemblies', mocked_ena_assemblies_query)
    def test_main_should_write_cutoff_json(self, tmpdir):
        cutoff_file = os.path.join(str(tmpdir), 'cutoff.json')
        update.cutoff_file = cutoff_file

        cutoff = (datetime.now().date() - relativedelta(days=1)).strftime('%Y-%m-%d')
        update.main(['-c', cutoff, '--db', 'default'])
        assert os.path.exists(update.cutoff_file)
        with open(update.cutoff_file, 'r') as f:
            assert json.load(f)['cutoff-date'] == datetime.today().strftime('%Y-%m-%d')

    @patch.object(ena_handler.EnaApiHandler, 'get_updated_studies', mocked_ena_study_query)
    @patch.object(ena_handler.EnaApiHandler, 'get_updated_runs', mocked_ena_read_run_query)
    @patch.object(ena_handler.EnaApiHandler, 'get_updated_assemblies', mocked_ena_assemblies_query)
    def test_main_should_read_cutoff_json(self, tmpdir):
        cutoff_file = os.path.join(str(tmpdir), 'cutoff.json')
        update.cutoff_file = cutoff_file

        cutoff = (datetime.now().date() - relativedelta(days=1)).strftime('%Y-%m-%d')
        with open(update.cutoff_file, 'w') as f:
            json.dump({'cutoff-date': cutoff}, f)
        assert os.path.exists(update.cutoff_file)

        update.main(['--db', 'default'])

        with open(update.cutoff_file, 'r') as f:
            assert json.load(f)['cutoff-date'] == datetime.today().strftime('%Y-%m-%d')

        db_studies = Study.objects.all()
        db_runs = Run.objects.all()
        db_assemblies = Assembly.objects.all()

        assert len(db_studies) == 5
        assert len(db_runs) == 10
        assert len(db_assemblies) == 5

    @classmethod
    def taredown_method(cls):
        # pass
        clear_database()


def test_main_python_vers():
    with pytest.raises(SyntaxError):
        with mock.patch.object(sys, 'version_info') as v_info:
            v_info.major = 2
            cutoff = (datetime.now().date() - relativedelta(days=1)).strftime('%Y-%m-%d')
            update.main(['-c', cutoff, '--db', 'default'])
