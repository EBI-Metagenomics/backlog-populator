from unittest import TestCase
import argparse
import os

from src import update
from ..utils import ena_creds_path, write_creds_file, clear_database


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
            self.assertEqual(db, args.database)

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
        self.assertEqual(str_date, args.cutoffdate)

    def tearDown(self):
        clear_database()

    @classmethod
    def tearDownClass(cls):
        if os.path.exists(ena_creds_path):
            os.remove(ena_creds_path)
