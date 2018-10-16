import os
from datetime import datetime
from backlog_populator import ena_api_handler
from copy import deepcopy
from unittest import TestCase, mock

from backlog_populator import mgnify_handler, sync

from ..utils import ena_creds_path, write_creds_file, db_name, str_to_date, clear_database, ena_api_handler_options, \
    Study, Run, Assembly, RunAssembly, num_fixture_runs, mocked_requests_get


class TestBacklogHandler(TestCase):
    study_data = {
        'study_accession': 'PRJEB1787',
        'secondary_study_accession': 'ERP001736',
        'study_title': 'Shotgun Sequencing of Tara Oceans DNA samples '
                       'corresponding to size fractions for  prokaryotes.',
        'first_public': '2017-01-01',
        'last_updated': '2018-01-01',
    }

    run_data = {
        'secondary_study_accession': 'ERP001736',
        'run_accession': 'ERR599097',
        'instrument_platform': 'ILLUMINA',
        'instrument_model': 'Illumina HiSeq 2000',
        'read_count': 167058316,
        'base_count': 32976603710,
        'library_layout': 'PAIRED',
        'library_strategy': 'WGS',
        'last_updated': '2014-09-12',
        'library_source': 'METAGENOMIC'
    }

    run2_data = {
        'secondary_study_accession': 'ERP001736',
        'run_accession': 'ERR599098',
        'instrument_platform': 'ILLUMINA',
        'instrument_model': 'Illumina HiSeq 2000',
        'read_count': 29188354,
        'base_count': 5795959196,
        'library_layout': 'PAIRED',
        'library_strategy': 'WGS',
        'last_updated': '2014-09-12',
        'library_source': 'METAGENOMIC'
    }

    assembly_data = {
        'analysis_accession': 'ERZ477576',
        'secondary_study_accession': 'ERP001736',
        'analysis_alias': 'ERR599097',
        'first_public': '2018-01-16',
        'last_updated': '2018-01-16',
    }

    assembly2_data = {
        'analysis_accession': 'ERZ477577',
        'secondary_study_accession': 'ERP001736',
        'analysis_alias': 'ERR599097',
        'first_public': '2018-01-16',
        'last_updated': '2018-01-16',
    }

    assembly_data_no_run = {
        'analysis_accession': 'ERZ477577',
        'secondary_study_accession': 'ERP001736',
        'analysis_alias': 'unknown',
        'first_public': '2018-01-16',
        'last_updated': '2018-01-16',
    }

    ena_handler = None

    @classmethod
    def setUpClass(cls):
        write_creds_file()

    def setUp(self):
        self.ena_handler = ena_api_handler.EnaApiHandler(ena_creds_path, ena_api_handler_options)
        clear_database()

    def assert_study_in_db(self, study_data):
        study_data['public'] = True
        study_data['primary_accession'] = study_data['study_accession']
        study_data['secondary_accession'] = study_data['secondary_study_accession']
        study = Study.objects.using(db_name).get(primary_accession=study_data['study_accession'])
        self.assertEqual(study.primary_accession, study_data['study_accession'])
        self.assertEqual(study.secondary_accession, study_data['secondary_study_accession'])
        self.assertEqual(study.title, study_data['study_title'])
        self.assertTrue(study.public)
        self.assertEqual(study.last_updated.date(), datetime.now().date())

    def assert_run_in_db(self, run_data):
        run = Run.objects.using(db_name).get(primary_accession=run_data['run_accession'])
        self.assertEqual(run.study.secondary_accession, run_data['secondary_study_accession'])
        self.assertEqual(run.primary_accession, run_data['run_accession'])
        self.assertEqual(run.instrument_platform, run_data['instrument_platform'])
        self.assertEqual(run.instrument_model, run_data['instrument_model'])
        self.assertEqual(run.read_count, run_data['read_count'])
        self.assertEqual(run.base_count, run_data['base_count'])
        self.assertEqual(run.library_layout, run_data['library_layout'])
        self.assertEqual(run.library_strategy, run_data['library_strategy'])
        self.assertEqual(run.ena_last_update, str_to_date(run_data['last_updated']))
        self.assertEqual(run.last_updated.date(), datetime.now().date())

    def assert_assembly_in_db(self, assembly_data, is_associated_to_run=True):
        assembly = Assembly.objects.using(db_name).get(primary_accession=assembly_data['analysis_accession'])
        self.assertEqual(assembly.primary_accession, assembly_data['analysis_accession'])
        self.assertEqual(assembly.study.secondary_accession, assembly_data['secondary_study_accession'])

        if is_associated_to_run:
            related_runs = assembly.runassembly_set.select_related()
            self.assertEqual(related_runs[0].run.primary_accession, assembly_data['analysis_alias'])
            self.assertEqual(assembly.ena_last_update, str_to_date(assembly_data['last_updated']))
        else:
            self.assertEqual(0, len(RunAssembly.objects.using(db_name).all()))

    def test_insert_study(self):
        mgnify_handler.create_study_obj(self.study_data).save()
        self.assert_study_in_db(self.study_data)

    def test_insert_run_without_cached_study(self):
        mgnify_handler.create_run_obj(self.ena_handler, db_name, {}, self.run_data).save()
        self.assert_study_in_db(self.study_data)
        self.assert_run_in_db(self.run_data)

    def test_insert_run_with_cached_study(self):
        mgnify_handler.create_run_obj(self.ena_handler, db_name, {}, self.run_data).save()
        mgnify_handler.create_run_obj(self.ena_handler, db_name, {}, self.run2_data).save()
        self.assert_study_in_db(self.study_data)
        self.assert_run_in_db(self.run_data)
        self.assert_run_in_db(self.run2_data)

    def test_insert_study_with_invalid_dates_sets_defaults_dates(self):
        study_invalid_dates = deepcopy(self.study_data)
        study_invalid_dates['first_public'] = 'invalid_date'
        study_invalid_dates['last_updated'] = 'invalid_date'
        mgnify_handler.create_study_obj(study_invalid_dates).save()
        study_invalid_dates['first_public'] = datetime.now().date()
        study_invalid_dates['last_updated'] = datetime.now().date()
        self.assert_study_in_db(study_invalid_dates)

    def test_insert_assembly_without_cached_run(self):
        mgnify_handler.create_assembly(self.ena_handler, db_name, {}, self.assembly_data).save()
        self.assert_assembly_in_db(self.assembly_data, False)
        self.assertEqual(1, len(Study.objects.using(db_name).all()))

    def test_insert_assembly_with_cached_run(self):
        mgnify_handler.create_assembly(self.ena_handler, db_name, {}, self.assembly_data).save()
        mgnify_handler.create_assembly(self.ena_handler, db_name, {}, self.assembly2_data).save()
        self.assert_study_in_db(self.study_data)
        self.assert_assembly_in_db(self.assembly_data, False)
        self.assert_assembly_in_db(self.assembly2_data, False)
        self.assertEqual(1, len(Study.objects.using(db_name).all()))

    def test_insert_assembly_without_run(self):
        mgnify_handler.create_assembly(self.ena_handler, db_name, {}, self.assembly_data_no_run).save()
        self.assert_assembly_in_db(self.assembly_data_no_run, False)
        self.assertEqual(1, len(Study.objects.using(db_name).all()))

    @mock.patch('swagger_client.ApiClient.request', side_effect=mocked_requests_get)
    def test_fetch_existing_run_from_mgnify(self, mock_name):
        run_accession = 'SRR6670121'
        sync.sync_runs(self.ena_handler, db_name, '2018-01-01', {})
        self.assertEqual(num_fixture_runs, len(Run.objects.using(db_name).all()))
        run = mgnify_handler.fetch_run(self.ena_handler, db_name, {}, run_accession)
        self.assertEqual(run.primary_accession, run_accession)

    @mock.patch('swagger_client.ApiClient.request', side_effect=mocked_requests_get)
    def test_fetch_new_run_from_mgnify(self, mock_name):
        self.assertEqual(0, len(Run.objects.using(db_name).all()))
        run_accession = 'SRR6670121'
        run = mgnify_handler.fetch_run(self.ena_handler, db_name, {}, run_accession)
        self.assertEqual(1, len(Run.objects.using(db_name).all()))
        self.assertEqual(run.primary_accession, run_accession)

    def tearDown(self):
        clear_database()

    @classmethod
    def tearDownClass(cls):
        if os.path.exists(ena_creds_path):
            os.remove(ena_creds_path)
