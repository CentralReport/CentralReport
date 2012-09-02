#!/usr/bin/env python

# CentralReport - Indev version
# Project by Charles-Emmanuel CAMUS - Avril 2012

import sys, time
from daemon import Daemon
import centralreport

__author__ = "che"

class MyDaemon(Daemon):
    def run(self):
        centralreport.CentralReport()
        while True:
            time.sleep(1)

    def stop(self):
        Daemon.stop(self)



if __name__ == "__main__":
    daemon = MyDaemon('/tmp/daemon-centralreport.pid')
    if len(sys.argv) == 2:
        if 'start' == sys.argv[1]:
            print("CentralReport -- Start")
            daemon.start()
        elif 'stop' == sys.argv[1]:
            daemon.stop()
            print("CentralReport -- Stopped")
        elif 'restart' == sys.argv[1]:
            print ("CentralReport -- Restarting...")
            daemon.restart()
            print ("CentralReport -- Started")
        else:
            print "Unknown command"
            sys.exit(2)
        sys.exit(0)
    else:
        print "usage: %s start|stop|restart" % sys.argv[0]
        sys.exit(2)