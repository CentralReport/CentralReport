#!/bin/bash

# CentralReport Unix/Linux Indev version.
# By careful! Don't use in production environment!

# Folders
PARENT_DIR=/usr/local/bin/
INSTALL_DIR=/usr/local/bin/centralreport

CONFIG_FILE=/etc/centralreport.cfg
CONFIG_ASSISTANT=/usr/local/bin/centralreport/config.py

PID_FILE=/var/run/centralreport.pid

# OS
CURRENT_OS=
OS_MAC="MacOS"
OS_DEBIAN="Debian"

# Mac OS startup plist
STARTUP_PLIST=/Library/LaunchDaemons/com.centralreport.plist
STARTUP_PLIST_INSTALL=utils/launchers/mac/com.centralreport.plist

# Debian startup script
STARTUP_DEBIAN=/etc/init.d/centralreport.sh
STARTUP_DEBIAN_INSTALL=utils/launchers/debian/centralreport.sh

# Temp install directories.
CHERRYPY_TAR=thirdparties/CherryPy.tar.gz
JINJA_TAR=thirdparties/Jinja2.tar.gz
SETUPTOOLS_TAR=thirdparties/setuptools.tar.gz
SETPROCTITLE_TAR=thirdparties/setproctitle.tar.gz

CHERRYPY_DIR=thirdparties/CherryPy-3.2.2
JINJA_DIR=thirdparties/Jinja2-2.6
SETUPTOOLS_DIR=thirdparties/setuptools-0.6c11
SETPROCTITLE_DIR=thirdparties/setproctitle-1.1.6
