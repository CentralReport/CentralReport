# -*- coding: utf-8 -*-

"""
    CentralReport - Text module
        Contains useful functions to working with strings

    https://github.com/miniche/CentralReport/
"""

import math


def remove_specials_characters(text):
    """
        Removes specials characters in string (\n, \r and \l).
    """

    text = str.replace(text, '\n', '')
    text = str.replace(text, '\r', '')
    text = str.replace(text, '\l', '')

    return text


def add_number_separators(number, separator=' '):
    """
        Adds a separator every 3 digits in the number.
    """

    if not isinstance(number, str):
        number = str(number)

    # Remove decimal part
    str_number = number.split('.')

    if len(str_number[0]) <= 3:
        str_number[0] = str_number[0]
    else:
        str_number[0] = add_number_separators(str_number[0][:-3]) + separator + str_number[0][-3:]

    # Verify if the var "number" have a decimal part.
    if len(str_number) > 1:
        return "%s.%s" % (str_number[0], str_number[1])

    return str_number[0]


def convert_text_to_bool(text):
    """
        Converts a text to a boolean.
    """

    true_values = ['True', 'true', 't', 'T', '1']

    if text in true_values:
        return True

    return False


def convert_seconds_to_phrase_time(seconds):
    """
        Converts seconds to a phrase time (ex: 65 = 1 minute 5 seconds).
    """

    ONE_DAY = 60 * 60 * 24
    ONE_HOUR = 60 * 60
    ONE_MINUTE = 60
    ONE_YEAR = 60 * 60 * 24 * 365

    remaining_seconds = seconds
    result_string = ''

    if remaining_seconds > ONE_YEAR:
        years = remaining_seconds / ONE_YEAR
        years = math.floor(years)

        remaining_seconds -= years * ONE_YEAR

        result_string += '1 year ' if 1 == years else str(int(years)) + ' years '

    if ONE_DAY < remaining_seconds:
        days = remaining_seconds / ONE_DAY
        days = math.floor(days)

        remaining_seconds -= days * ONE_DAY
        result_string += '1 day ' if 1 == days else str(int(days)) + ' days '

    if ONE_HOUR < remaining_seconds:
        hours = remaining_seconds / ONE_HOUR
        hours = math.floor(hours)

        remaining_seconds -= hours * ONE_HOUR
        result_string += '1 hour ' if 1 == hours else str(int(hours)) + ' hours '

    if ONE_MINUTE < remaining_seconds:
        minutes = remaining_seconds / ONE_MINUTE
        minutes = math.floor(minutes)

        remaining_seconds -= minutes * ONE_MINUTE
        result_string += '1 minute ' if 1 == minutes else str(int(minutes)) + ' minutes '

    result_string += '1 second ' if 1 == remaining_seconds else str(int(remaining_seconds)) + ' seconds '

    return str(result_string)


def convert_byte(byte_to_convert):
    """
        Converts byte to most biggest unit.
    """

    TBYTE = 1024 * 1024 * 1024 * 1024
    GBYTE = 1024 * 1024 * 1024
    MBYTE = 1024 * 1024
    KBYTE = 1024

    if byte_to_convert / TBYTE >= 1:
        return str(round(byte_to_convert / TBYTE, 2)) + " TB"
    elif byte_to_convert / GBYTE >= 1:
        return str(round(byte_to_convert / GBYTE, 2)) + " GB"
    elif byte_to_convert / MBYTE >= 1:
        return str(round(byte_to_convert / MBYTE, 2)) + " MB"
    elif byte_to_convert / KBYTE >= 1:
        return str(round(byte_to_convert / KBYTE, 2)) + " KB"
    else:
        return str(round(byte_to_convert, 0)) + " B"
