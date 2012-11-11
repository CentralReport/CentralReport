#!/usr/bin/env python

#
# CentralReport - Indev version
#

import sys,time,random,socket
from cr.tools import Config
from centralreport import CentralReport

if __name__ == "__main__":

    print('\n-------------------------------------------------- ')
    print('         CentralReport config editor                 ')
    print('--------------------------------------------------   ')
    print('\nYou can also edit manually the config file, located at /etc/cr/centralreport.cfg')

    print("Stopping CentralReport...")
    time.sleep(1)

    daemon = CentralReport(Config.pid_file)
    centralReportRunningBefore = True
    try:
        daemon.stop()
    except:
        print("CentralReport isn't running")
        centralReportRunningBefore = False

    # Getting the actual config
    config = Config()

    # Enable or disable internal web server
    print("\n\n-- Internal web server options --")
    print("CentralReport have a small internal web server to display checks datas, with a simple web browser.")
    print("With this web server, you can monitor this host without account on centralreport.net")

    validEnableWebServer = False
    while (validEnableWebServer != True):
        resultEnableWebServer = raw_input("Do you want to enable the internal web server? [yes/no] ")
        if(resultEnableWebServer == "yes"):
            validEnableWebServer = True
            Config.config_webserver_enable = True

        elif(resultEnableWebServer == "no"):
            validEnableWebServer = True
            Config.config_webserver_enable = False

        else:
            print("We don't understand your answer. Please use 'yes' or 'no'")


    # If the webserver is enabled, we can ask the default port for it.
    if(Config.config_webserver_enable == True):
        print("\nDefault port is 8080. You can choose a custom port if you want.")

        validPort = False
        while(validPort != True):
            resultPort = raw_input("Use this port : ")
            resultPortInt = 0

            try:
                resultPortInt = int(resultPort)

                port = random.randint(33000, 60000)
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                try:
                    s.connect(("127.0.0.1", int(resultPort)))
                except socket.error, e:
                    validPort = True
                else:
                    s.close
                    print("Port "+ resultPort +" is already used on this host. Please define a free port.")
                    validPort = False

            except ValueError:
                validPort = False
                print("You must enter a valid number!")


        Config.config_webserver_port = resultPortInt


    print("\n\nThanks! Writing the new config file...")
    config.writeConfigFile()

    # We're looking if CentralReport ran before.
    if(centralReportRunningBefore == True):
        print("\nRestarting CentralReport...")
        daemon.start()

    print("\n\n-- End of config script")

    sys.exit(0)