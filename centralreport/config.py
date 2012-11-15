#!/usr/bin/env python

#
# CentralReport - Indev version
#

import sys
import time
import random
import socket
from cr.tools import Config
from centralreport import CentralReport

if __name__ == '__main__':

    print('\n')
    print('-------------------------------------------------- ')
    print('         CentralReport config editor                 ')
    print('--------------------------------------------------   ')
    print('\n')
    print('You can also edit manually the config file, located at /etc/cr/centralreport.cfg')

    print('Stopping CentralReport...')
    time.sleep(1)

    daemon = CentralReport(Config.pid_file)
    centralReportRunningBefore = True
    try:
        daemon.stop()
    except:
        print('CentralReport is not running')
        centralReportRunningBefore = False

    # Getting the actual config
    config = Config()

    # Enable or disable internal web server
    print('\n\n')
    print('-- Internal web server options --')
    print('CentralReport have a small internal web server to display checks datas, with a simple web browser.')
    print('With this web server, you can monitor this host without account on centralreport.net')

    validEnableWebServer = False
    while (not validEnableWebServer):
        resultEnableWebServer = raw_input('Do you want to enable the internal web server? [yes/no] ')
        if('yes' == resultEnableWebServer.lower()):
            validEnableWebServer = True
            Config.config_webserver_enable = True

        elif('no' == resultEnableWebServer.lower()):
            validEnableWebServer = True
            Config.config_webserver_enable = False

        else:
            print('We do not understand your answer. Please use "yes" or "no"')

    # If the webserver is enabled, we can ask the default port for it.
    if Config.config_webserver_enable:
        print('\n')
        print('Default port is 8080. You can choose a custom port if you want.')

        validPort = False
        while(not validPort):
            resultPort = raw_input('Use this port : ')
            resultPortInt = 0

            try:
                resultPortInt = int(resultPort)

                port = random.randint(33000, 60000)
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
                print('You must enter a valid number!')

        Config.config_webserver_port = resultPortInt

    print('\n\n')
    print('Thanks! Writing the new config file...')
    config.writeConfigFile()

    # We're looking if CentralReport ran before.
    if(centralReportRunningBefore):
        print('\n')
        print('Restarting CentralReport...')
        daemon.start()

    print('\n\n')
    print('--------------------------------------------------')
    print('             End of config script')
    print('--------------------------------------------------')

    sys.exit(0)
