# -*- coding: utf-8 -*-

"""
    CentralReport - Tests for cr.utils.text module
        Please see: http://docs.python.org/2/library/unittest.html

    https://github.com/CentralReport
"""

import unittest
from cr.utils import text as cr_text


class SpecialCharactersTest(unittest.TestCase):
    """
        Tests for the remove_specials_characters functions
    """

    def test_removed_characters(self):
        self.assertEqual(cr_text.remove_specials_characters('\n\r\ltest'), 'test')

    def test_uncleaned_characters(self):
        self.assertEquals(cr_text.remove_specials_characters('\ttest'), '\ttest')


class NumberSeparatorsTest(unittest.TestCase):
    """
        Tests for the add_number_separators functions
    """

    def test_small_number(self):
        self.assertEqual(cr_text.add_number_separators(123), '123')

    def test_big_number(self):
        self.assertEqual(cr_text.add_number_separators(123456789), '123 456 789')

    def test_float(self):
        self.assertEqual(cr_text.add_number_separators(123456789.123), '123 456 789.123')

    def test_custom_seperator(self):
        self.assertEqual(cr_text.add_number_separators(123456, '-'), '123-456')


class TextToBoolTest(unittest.TestCase):
    """
        Tests for the convert_text_to_bool functions
    """

    def test_true(self):
        self.assertEqual(cr_text.convert_text_to_bool('true'), True)

    def test_t(self):
        self.assertEqual(cr_text.convert_text_to_bool('t'), True)

    def test_false(self):
        self.assertEqual(cr_text.convert_text_to_bool('false'), False)

    def test_wrong_value(self):
        self.assertNotEqual(cr_text.convert_text_to_bool('hello'), True)


class SecondsToPhraseTest(unittest.TestCase):
    """
        Tests for the convert_seconds_to_phrase_time functions
    """

    def test_one_second(self):
        self.assertEqual(cr_text.convert_seconds_to_phrase_time(1), '1 second')

    def test_two_second(self):
        self.assertEqual(cr_text.convert_seconds_to_phrase_time(2), '2 seconds')

    def test_more_than_one_minute(self):
        self.assertEqual(cr_text.convert_seconds_to_phrase_time(61), '1 minute 1 second')

    def test_more_than_one_hour(self):
        self.assertEqual(cr_text.convert_seconds_to_phrase_time(3725), '1 hour 2 minutes 5 seconds')

    def test_one_day(self):
        self.assertEqual(cr_text.convert_seconds_to_phrase_time(86400), '1 day')

    def test_one_year(self):
        self.assertEqual(cr_text.convert_seconds_to_phrase_time(31536000), '1 year')

    def test_complex_time(self):
        self.assertEqual(cr_text.convert_seconds_to_phrase_time(31649051), '1 year 1 day 7 hours 24 minutes 11 seconds')


class ConvertByteTest(unittest.TestCase):
    """
        Tests for the convert_byte functions
    """

    def test_one_byte(self):
        self.assertEqual(cr_text.convert_byte(1), '1.0 B')

    def test_more_than_one_kilobyte(self):
        self.assertEqual(cr_text.convert_byte(1500), '1.46 KB')

    def test_more_than_one_megabyte(self):
        self.assertEqual(cr_text.convert_byte(8765434), '8.36 MB')

    def test_one_gigabyte(self):
        self.assertEqual(cr_text.convert_byte(1073741824), '1.0 GB')

    def test_one_terabyte(self):
        self.assertEqual(cr_text.convert_byte(1099511627776), '1.0 TB')

def suite():
    """
        Gather all the tests from this module in a test suite.
    """
    test_suite = unittest.TestSuite()
    test_suite.addTest(unittest.makeSuite(SpecialCharactersTest))
    test_suite.addTest(unittest.makeSuite(NumberSeparatorsTest))
    test_suite.addTest(unittest.makeSuite(TextToBoolTest))
    test_suite.addTest(unittest.makeSuite(SecondsToPhraseTest))
    test_suite.addTest(unittest.makeSuite(ConvertByteTest))
    return test_suite
