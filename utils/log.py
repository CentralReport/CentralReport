# CentralReport - Indev version
# Project by Charles-Emmanuel CAMUS - Avril 2012

import syslog

class CRLog:

    @staticmethod
    def writeLog(text):
        syslog.openlog("CentralReport")
        syslog.syslog(syslog.LOG_ALERT, text)