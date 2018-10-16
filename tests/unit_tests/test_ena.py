from unittest import TestCase
import pytest
import yaml
from datetime import datetime
import os
from backlog_populator import ena_api_handler
from ..utils import ena_creds_path, write_creds_file, sync_time, ena_api_handler_options


def test_invalid_credentials_path():
    with pytest.raises(FileNotFoundError, message='Expecting FileNotFoundError'):
        ena_api_handler.EnaApiHandler('invalid/path')


def test_invalid_credentials_empty_file():
    tmp_file = os.path.join('tests', 'tmp.yml')
    with open(tmp_file, 'w') as f:
        f.write('invalid_yaml')
    with pytest.raises(TypeError, message='Expect yaml error'):
        ena_api_handler.EnaApiHandler(tmp_file)
    if os.path.exists(tmp_file):
        os.remove(tmp_file)


def test_invalid_credentials_empty_field():
    with pytest.raises(AssertionError, message='Expecting AssertionError'):
        tmp_file = os.path.join('tests', 'tmp.yml')
        with open(tmp_file, 'w') as f:
            yaml.dump({"USERNAME": '', "PASSWORD": 'secret'}, f, allow_unicode=True)
        with pytest.raises(TypeError, message='Expect yaml error'):
            ena_api_handler.EnaApiHandler(tmp_file)
    if os.path.exists(tmp_file):
        os.remove(tmp_file)


class TestEnaAPIHandlerResponses(TestCase):
    expected_study_fields = {'study_accession', 'secondary_study_accession', 'study_description', 'study_name',
                             'study_title', 'center_name', 'broker_name', 'last_updated',
                             'first_public'}

    expected_run_fields = {'base_count', 'read_count', 'instrument_platform', 'instrument_model', 'library_layout',
                           'library_source', 'secondary_study_accession', 'library_strategy', 'sample_accession',
                           'last_updated', 'first_public', 'fastq_ftp', 'scientific_name', 'tax_id', 'study_title',
                           'sample_title', 'run_accession', 'environment_biome', 'environment_feature',
                           'environment_material'}

    ena_handler = None

    @classmethod
    def setUpClass(cls):
        write_creds_file()

    def setUp(self):
        self.ena_handler = ena_api_handler.EnaApiHandler(ena_creds_path, ena_api_handler_options)

    def test_fetch_single_study_has_correct_fields(self):
        study = self.ena_handler.get_study('ERP001736')
        self.assertEqual(study.keys(), self.expected_study_fields)

    def test_fetch_single_study_with_invalid_accession(self):
        with pytest.raises(ValueError, message='Expect ValueError'):
            self.ena_handler.get_study('invalid_accession')

    def test_fetch_multiple_studies_with_correct_fields(self):
        date = datetime.now() - sync_time
        studies = self.ena_handler.get_updated_studies(date.strftime("%Y-%m-%d"))
        for study in studies.values():
            self.assertEqual(study.keys(), self.expected_study_fields)

    def test_fetches_studies_from_date(self):
        date = datetime.now() - sync_time
        studies = self.ena_handler.get_updated_studies(date.strftime("%Y-%m-%d"))
        for study in studies.values():
            self.assertLessEqual(date.date(), datetime.strptime(study['last_updated'], "%Y-%m-%d").date())

    def test_fetch_multiple_runs_with_correct_fields(self):
        date = datetime.now() - sync_time
        runs = self.ena_handler.get_updated_runs(date.strftime("%Y-%m-%d"))
        for run in runs.values():
            self.assertEqual(run.keys(), self.expected_run_fields)

    def test_fetch_single_run_has_correct_fields(self):
        study = self.ena_handler.get_run('SRR7186375')
        self.assertEqual(study.keys(), self.expected_run_fields)

    def test_fetch_single_run_with_invalid_accession(self):
        with pytest.raises(ValueError, message='Expect ValueError'):
            self.ena_handler.get_run('invalid_accession')

    def test_fetch_multiple_analyses_with_correct_fields(self):
        date = datetime.now() - sync_time
        expected_analysis_fields = {'analysis_accession', 'analysis_alias', 'first_public', 'last_updated',
                                    'secondary_study_accession'}
        analyses = self.ena_handler.get_updated_assemblies(date.strftime("%Y-%m-%d"))
        for analysis in analyses.values():
            self.assertEqual(analysis.keys(), expected_analysis_fields)

    def test_fetch_study_no_update(self):
        date = datetime.now() + sync_time
        studies = self.ena_handler.get_updated_studies(date.strftime("%Y-%m-%d"))
        self.assertEqual(studies, {})

    def test_fetch_runs_no_update(self):
        date = datetime.now() + sync_time
        runs = self.ena_handler.get_updated_runs(date.strftime("%Y-%m-%d"))
        self.assertEqual(runs, {})

    def test_fetch_analyses_no_update(self):
        date = datetime.now() + sync_time
        analyses = self.ena_handler.get_updated_assemblies(date.strftime("%Y-%m-%d"))
        self.assertEqual(analyses, {})

    @classmethod
    def tearDownClass(cls):
        if os.path.exists(ena_creds_path):
            os.remove(ena_creds_path)
