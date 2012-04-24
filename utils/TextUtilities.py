# CentralReport - Indev version
# Project by Charles-Emmanuel CAMUS - Avril 2012


class TextUtilities:

    @staticmethod
    def removeSpecialsCharacters(text):
        """
        Remove Specials characters in string
        """


        text = str.replace(text,"\n","")
        text = str.replace(text,"\r","")
        text = str.replace(text,"\l","")

        return text
