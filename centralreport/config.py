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
            central_report_running_before = False
        else:
            central_report_running_before = True

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

        valid_enable_webserver = False
        while not valid_enable_webserver:
            result_enable_webserver = raw_input('Do you want to enable the internal web server? [Y/n] ')

            # Default value, if empty
            if len(result_enable_webserver) == 0:
                result_enable_webserver = "y"

            # Config setters
            if 'y' == result_enable_webserver.lower()[:1]:
                valid_enable_webserver = True
                Config.set_config_value('Webserver', 'enable', True)

            elif 'n' == result_enable_webserver.lower()[:1]:
                valid_enable_webserver = True
                Config.config_webserver_enable = False
                Config.set_config_value('Webserver', 'enable', False)

            else:
                print 'We do not understand your answer. Please use "yes" or "no"'

        # If the webserver is enabled, we can ask the default port for it.
        if bool(Config.get_config_value('Webserver', 'enable')):
            print '\n'
            print 'Default port is 8080. You can choose a custom port if you want.'

            valid_port = False
            result_port_int = 0

            while not valid_port:
                result_port = raw_input('Web server port: [8080] ')

                # Default value
                if len(result_port) == 0:
                    result_port = 8080

                try:
                    result_port_int = int(result_port)
                    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

                    try:
                        s.connect(('127.0.0.1', int(result_port)))
                    except socket.error, e:
                        valid_port = True
                    else:
                        s.close()
                        print 'Port %s is already used on this host. Please define a free port.' % result_port
                        valid_port = False

                except ValueError:
                    valid_port = False
                    print 'You must enter a valid number!'

            Config.set_config_value('Webserver', 'port', result_port_int)

        print '\n'
        print 'Thanks! Writing the new config file...'
        config.write_config_file()

        # Checking if CentralReport was previously running.
        if central_report_running_before:
            print '\n'
            print 'Restarting CentralReport...'
            daemon.start()

        sys.exit(0)

    elif 'update' == sys.argv[1]:
        print 'Not implemented yet.'
