#
# CentralReport - Indev version
#

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

