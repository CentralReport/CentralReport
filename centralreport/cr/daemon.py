# -*- coding: utf-8 -*-

"""
    CentralReport - Daemon generic class
        Please see: http://www.jejik.com/articles/2007/02/a_simple_unix_linux_daemon_in_python/

    https://github.com/CentralReport
"""

import atexit
import os
import sys


class Daemon:
    """
        A generic daemon class.

        Usage: subclass the Daemon class and override the run() method
    """

    def __init__(self, pidfile, stdin=os.devnull, stdout=os.devnull, stderr='/tmp/centralreport_error.log'):

        self.stdin = stdin
        self.stdout = stdout
        self.stderr = stderr
        self.pidfile = pidfile

    def daemonize(self):
        """
            do the UNIX double-fork magic, see Stevens' "Advanced
            Programming in the UNIX Environment" for details (ISBN 0201563177)
            http://www.erlenstar.demon.co.uk/unix/faq_2.html#SEC16
        """

        try:
            pid = os.fork()
            if pid > 0:
                # exit first parent

                sys.exit(0)
        except OSError, e:
            sys.stderr.write('fork #1 failed: %d (%s)\n' % (e.errno, e.strerror))
            sys.exit(1)

        # decouple from parent environment

        os.chdir('/')
        os.setsid()
        os.umask(0)

        # do second fork

        try:
            pid = os.fork()
            if pid > 0:
                # exit from second parent

                sys.exit(0)
        except OSError, e:
            sys.stderr.write('fork #2 failed: %d (%s)\n' % (e.errno, e.strerror))
            sys.exit(1)

        # redirect standard file descriptors

        sys.stdout.flush()
        sys.stderr.flush()
        si = file(self.stdin, 'r')
        so = file(self.stdout, 'a+')
        se = file(self.stderr, 'a+', 0)
        os.dup2(si.fileno(), sys.stdin.fileno())
        os.dup2(so.fileno(), sys.stdout.fileno())
        os.dup2(se.fileno(), sys.stderr.fileno())

        # write pidfile

        atexit.register(self.delete_pid)
        pid = str(os.getpid())
        file(self.pidfile, 'w+').write('%s\n' % pid)

    def delete_pid(self):
        os.remove(self.pidfile)

    def start(self):
        """
            Start the daemon
        """

        # Check for a pidfile to see if the daemon already runs

        try:
            pf = file(self.pidfile, 'r')
            pid = int(pf.read().strip())
            pf.close()
        except IOError:
            pid = None

        if pid:
            message = 'pidfile %s already exist. Daemon already running?\n'
            sys.stderr.write(message % self.pidfile)
            sys.exit(1)

        # Start the daemon

        self.daemonize()
        self.run()

    def run(self):
        """
            You should override this method when you subclass Daemon. It will be called after the process has been
            daemonized by start() or restart().
        """
