from unittest import TestCase
import argparse
from datetime import datetime
from dateutil.relativedelta import relativedelta
from src import update

from ..utils import clear_database


class TestSync(TestCase):
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

    def test_main(self):
        cutoff = (datetime.now().date() - relativedelta(days=1)).strftime('%Y-%m-%d')
        update.main(['-c', cutoff, '--database', 'default'])

    def tearDown(self):
        clear_database()
