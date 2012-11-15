__author__ = 'che'

import logging

def configLog():
    logging.basicConfig(
        filename='/var/log/centralreport.log',
        format='%(levelname)s - %(asctime)s : %(message)s',
        level=logging.DEBUG,
        datefmt='%m/%d/%Y %I:%M:%S %p'
    )


def writeDebug(text):
    logging.debug(text)


def writeInfo(text):
    logging.info(text)


def writeError(text):
    logging.error(text)


def writeCritical(text):
    logging.critical(text)


def writeFatal(text):
    logging.fatal(text)
