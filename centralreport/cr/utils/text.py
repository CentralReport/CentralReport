#
# CentralReport - Indev version
#

import math

def removeSpecialsCharacters(text):
    """ Remove Specials characters in string (\n, \r and \l) """

    text = str.replace(text,"\n","")
    text = str.replace(text,"\r","")
    text = str.replace(text,"\l","")

    return text


def numberSeparators(number, separator=' '):
    """ Add a separator every 3 digit in the number  """

    # It's a string ?
    if not isinstance(number,str):
        number = str(number)

    # Remove decimal part
    str_number = number.split('.')

    if len(str_number[0]) <= 3:
        str_number[0] = str_number[0]
    else:
        str_number[0] = numberSeparators(str_number[0][:-3]) + separator + str_number[0][-3:]

    # Verify if the var "number" have a decimal part.
    if len(str_number) > 1:
        return str_number[0] +'.'+ str_number[1]
    else:
        return str_number[0]



def textToBool(text):
    true_values = ['True','true','t','T','1']

    if text in true_values:
        return True
    else:
        return False



def secondsToPhraseTime(seconds):
    """
        WIP (miniche)
    """

    ONE_YEAR = 60*60*24*365
    ONE_DAY = 60*60*24
    ONE_HOUR = 60*60
    ONE_MINUTE = 60

    remaining_seconds = seconds
    result_string = ''

    if remaining_seconds > ONE_YEAR:
        years = remaining_seconds/ONE_YEAR
        years = math.floor(years)

        remaining_seconds = remaining_seconds - years * ONE_YEAR

        if 1 == years:
            result_string += '1 year '
        else:
            result_string += str(int(years)) +' years '


    if remaining_seconds > ONE_DAY:
        days = remaining_seconds/ONE_DAY
        days = math.floor(days)

        remaining_seconds = remaining_seconds - days * ONE_DAY

        if 1 == days:
            result_string += '1 day '
        else:
            result_string += str(int(days)) +' days '


    if remaining_seconds > ONE_HOUR:
        hours = remaining_seconds/ONE_HOUR
        hours = math.floor(hours)

        remaining_seconds = remaining_seconds - hours * ONE_HOUR

        if 1 == hours:
            result_string += '1 hour '
        else:
            result_string += str(int(hours)) +' hours '

    if remaining_seconds > ONE_MINUTE:
        minutes = remaining_seconds/ONE_MINUTE
        minutes = math.floor(minutes)

        remaining_seconds = remaining_seconds - minutes * ONE_MINUTE

        if 1 == minutes:
            result_string += '1 minute '
        else:
            result_string += str(int(minutes)) +' minutes '


    if remaining_seconds == 1:
        result_string += ' 1 second'
    elif remaining_seconds > 1:
        result_string += str(int(remaining_seconds)) +' seconds'


    return str(result_string)
