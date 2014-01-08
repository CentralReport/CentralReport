# -*- coding: utf-8 -*-

"""
    CentralReport - Tests for cr.utils.date module
        Please see: http://docs.python.org/2/library/unittest.html

    https://github.com/CentralReport
"""

import datetime
import unittest

from cr.utils import date as cr_date


class CrTimestampTest(unittest.TestCase):
    """
        Tests for datetime_to_timestamp function
    """

    def test_datetime_to_timestamp(self):
        date_to_convert = datetime.datetime(2012, 10, 10, 10, 10, 10)
        self.assertEqual(cr_date.datetime_to_timestamp(date_to_convert), 1349863810L)

    def test_wrong_timestamp(self):
        date_to_convert = datetime.datetime(2012, 10, 10, 10, 10, 10)
        self.assertNotEquals(cr_date.datetime_to_timestamp(date_to_convert), 1349856611L)


def suite():
    """
        Gather all the tests from this module in a test suite.
    """
    test_suite = unittest.TestSuite()
    test_suite.addTest(unittest.makeSuite(CrTimestampTest))
    return test_suite
