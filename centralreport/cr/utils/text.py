#
# CentralReport - Indev version
#

def removeSpecialsCharacters(text):
    """
    Remove Specials characters in string
    """

    text = str.replace(text,"\n","")
    text = str.replace(text,"\r","")
    text = str.replace(text,"\l","")

    return text
