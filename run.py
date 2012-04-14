#!/usr/bin/env python

# CentralReport - Indev version
# Project by Charles-Emmanuel CAMUS - Avril 2012

import sys, time
from daemon import Daemon

__author__ = "che"

class MyDaemon(Daemon):
    def run(self):
        while True:
            time.sleep(1)

if __name__ == "__main__":
    daemon = MyDaemon('/tmp/daemon-centralreport.pid')
    if len(sys.argv) == 2:
        if 'start' == sys.argv[1]:
            daemon.start()
        elif 'stop' == sys.argv[1]:
            daemon.stop()
        elif 'restart' == sys.argv[1]:
            daemon.restart()
        else:
            print "Unknown command"
            sys.exit(2)
        sys.exit(0)
    else:
        print "usage: %s start|stop|restart" % sys.argv[0]
        sys.exit(2)