#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
    CentralReport - Config script
        First config assistant, used during installation.

    https://github.com/miniche/CentralReport/
"""

import socket
import sys
import time
from centralreport import CentralReport
from cr.tools import Config

if __name__ == '__main__':

    if 1 == len(sys.argv):

        print '\n'
        print '-------------------------------------------------- '
        print '         CentralReport config editor                 '
        print '--------------------------------------------------   '
        print '\n'
        print 'You can also edit manually the config file, located at /etc/centralreport.cfg'

        print 'Stopping CentralReport...'
        time.sleep(1)

        daemon = CentralReport(Config.CR_PID_FILE)
        if not daemon.status():
            print 'CentralReport is not running'
            centralReportRunningBefore = False
        else:

            centralReportRunningBefore = True
            try:
                daemon.stop()
            except:
                print 'Error stopping CentralReport daemon...'

        config = Config()  # Getting the actual config

        # Enable or disable internal web server

        print '\n\n'
        print '-- Internal web server options --'
        print 'CentralReport has a small internal web server to display checks datas, with a simple web browser.'
        print 'With this web server, you can monitor this host without account on centralreport.net'

        validEnableWebServer = False
        while (not validEnableWebServer):
            resultEnableWebServer = raw_input('Do you want to enable the internal web server? [y/n] ')
            if('y' == resultEnableWebServer.lower()[:1]):
                validEnableWebServer = True
                Config.setConfigValue('Webserver', 'enable', True)
            elif 'n' == resultEnableWebServer.lower()[:1]:

                validEnableWebServer = True
                Config.config_webserver_enable = False
                Config.setConfigValue('Webserver', 'enable', False)
            else:

                print 'We do not understand your answer. Please use "yes" or "no"'

        # If the webserver is enabled, we can ask the default port for it.

        if bool(Config.getConfigValue('Webserver', 'enable')):
            print '\n'
            print 'Default port is 8080. You can choose a custom port if you want.'

            validPort = False
            while not validPort:
                resultPort = raw_input('Use this port: ')
                resultPortInt = 0

                try:
                    resultPortInt = int(resultPort)

                    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    try:
                        s.connect(('127.0.0.1', int(resultPort)))
                    except socket.error, e:
                        validPort = True
                    else:
                        s.close
                        print('Port ' + resultPort + ' is already used on this host. Please define a free port.')
                        validPort = False
                except ValueError:

                    validPort = False
                    print 'You must enter a valid number!'

            Config.setConfigValue('Webserver', 'port', resultPortInt)

        print '\n\n'
        print 'Thanks! Writing the new config file...'
        config.writeConfigFile()

        # Checking if CentralReport was previously running.

        if centralReportRunningBefore:
            print '\n'
            print 'Restarting CentralReport...'
            daemon.start()

        print '\n\n'
        print '--------------------------------------------------'
        print '             End of config script'
        print '--------------------------------------------------'

        sys.exit(0)
    elif 'update' == sys.argv[1]:

        print 'Not implemented yet.'
