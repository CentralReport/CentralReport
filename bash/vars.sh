#!/bin/bash

# CentralReport Unix/Linux Indev version.
# By careful! Don't use in production environment!

# Vars
PARENT_DIR=/usr/local/bin/
INSTALL_DIR=/usr/local/bin/centralreport

CONFIG_FILE=/etc/cr/centralreport.cfg

PID_FILE=/tmp/daemon-centralreport.pid

# OS
CURRENT_OS=
OS_MAC="MacOS"
OS_DEBIAN="Debian"

# Mac OS startup plist
STARTUP_PLIST=/Library/LaunchDaemons/com.centralreport.plist
STARTUP_PLIST_INSTALL=lunchers/com.centralreport.plist

# Debian startup script
STARTUP_DEBIAN=/etc/init.d/centralreport_debian.sh
STARTUP_DEBIAN_INSTALL=lunchers/centralreport_debian.sh

# Temp install directories.
CHERRYPY_TAR=thirdparties/CherryPy.tar.gz
MAKO_TAR=thirdparties/Mako.tar.gz

CHERRYPY_DIR=thirdparties/CherryPy-3.2.2
MAKO_DIR=thirdparties/Mako-0.7.2
