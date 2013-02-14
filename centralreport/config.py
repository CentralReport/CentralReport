#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
    CentralReport - Config script
        First config assistant, used during installation.
        This assistant asks some questions to the administrator to then write values in the config file.

        Important: Every console outputs must contain at most 80 characters.
        It's the default width of major consoles.

    https://github.com/miniche/CentralReport/
"""

import socket
import sys
import time
from centralreport import CentralReport
from cr.tools import Config

if __name__ == '__main__':

    if 1 == len(sys.argv):

        print ' '
        print '--------------------------------------------------------------------------------'
        print '                         CentralReport config editor                            '
        print '--------------------------------------------------------------------------------'
        print ' '
        print 'You can also edit manually the config file, located at /etc/centralreport.cfg'

        daemon = CentralReport(Config.CR_PID_FILE)
        if not daemon.status():
            centralReportRunningBefore = False
        else:
            centralReportRunningBefore = True

            try:
                print 'Stopping CentralReport...'
                daemon.stop()
                time.sleep(1)
            except:
                print 'Error stopping CentralReport daemon...'

        config = Config()  # Getting the actual config

        # Enable or disable internal web server
        print '\n'
        print '-- Internal web server options --'
        print 'CentralReport has a small internal web server to display checks data,'
        print 'with a simple web browser. This web server allows you to check your data'
        print 'locally, without being registered on our online platform'
        print '(http://centralreport.net)'

        validEnableWebServer = False
        while (not validEnableWebServer):
            resultEnableWebServer = raw_input('Do you want to enable the internal web server? [Y/n] ')

            # Default value, if empty
            if len(resultEnableWebServer) == 0:
                resultEnableWebServer = "y"

            # Config setters
            if ('y' == resultEnableWebServer.lower()[:1]):
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
                resultPort = raw_input('Web server port: [8080] ')
                resultPortInt = 0

                # Default value
                if len(resultPort) == 0:
                    resultPort = 8080

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

        print '\n'
        print 'Thanks! Writing the new config file...'
        config.writeConfigFile()

        # Checking if CentralReport was previously running.
        if centralReportRunningBefore:
            print '\n'
            print 'Restarting CentralReport...'
            daemon.start()

        sys.exit(0)

    elif 'update' == sys.argv[1]:
        print 'Not implemented yet.'
