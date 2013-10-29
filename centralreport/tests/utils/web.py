# -*- coding: utf-8 -*-

"""
    CentralReport - Tests for cr.utils.web module
        Please see: http://docs.python.org/2/library/unittest.html

    https://github.com/CentralReport
"""

import unittest
import cr.utils.web

class CrCheckPortTest(unittest.TestCase):
    """
        Tests for check_port function
    """

    def test_success(self):
        self.assertEqual(True, cr.utils.web.check_port('centralreport.net', 80))

    def test_fail(self):
        self.assertEqual(False, cr.utils.web.check_port('centralreport.net', 50, 2))


def suite():
    """
        Gather all the tests from this module in a test suite.
    """
    test_suite = unittest.TestSuite()
    test_suite.addTest(unittest.makeSuite(CrCheckPortTest))
    return test_suite
