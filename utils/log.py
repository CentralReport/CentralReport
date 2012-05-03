# CentralReport - Indev version
# Project by Charles-Emmanuel CAMUS - Avril 2012

import logging

class CRLog:

    @staticmethod
    def configLog():
        logging.basicConfig(filename='/var/log/centralreport.log',format='%(levelname)s - %(asctime)s : %(message)s',level=logging.DEBUG, datefmt='%m/%d/%Y %I:%M:%S %p')

    @staticmethod
    def writeDebug(text):
        logging.debug(text)

    @staticmethod
    def writeInfo(text):
        logging.info(text)


    @staticmethod
    def writeError(text):
        logging.error(text)

    @staticmethod
    def writeCritical(text):
        logging.critical(text)

    @staticmethod
    def writeFatal(text):
        logging.fatal(text)