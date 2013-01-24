#!/bin/bash

# ------------------------------------------------------------
# CentralReport Unix/Linux - bash vars
# Alpha version. Don't use in production environment!
# ------------------------------------------------------------
# https://github.com/miniche/CentralReport/
# ------------------------------------------------------------

# This file contains all variables used by bash scripts

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

# Libraries directories
SETUPTOOLS_TAR=thirdparties/setuptools.tar.gz

SETUPTOOLS_DIR=thirdparties/setuptools-0.6c11
