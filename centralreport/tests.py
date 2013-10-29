#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
    CentralReport - Python unittest suite
        Please see: http://docs.python.org/2/library/unittest.html

    https://github.com/CentralReport
"""

import unittest

import tests.utils.date
import tests.utils.text
import tests.utils.web


def suite():
    """
        Defines all suites to run
    """

    cr_test_suite = unittest.TestSuite()
    cr_test_suite.addTests(tests.utils.date.suite())
    cr_test_suite.addTests(tests.utils.text.suite())
    cr_test_suite.addTest(tests.utils.web.suite())
    return cr_test_suite

if __name__ == '__main__':
    unittest.main(defaultTest='suite')
