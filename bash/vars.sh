#!/bin/bash

# ------------------------------------------------------------
# CentralReport Unix/Linux - bash vars
# Alpha version. Don't use in production environment!
# ------------------------------------------------------------
# https://github.com/miniche/CentralReport/
# ------------------------------------------------------------

# This file contains all variables used by bash scripts

# Folders
CR_BIN_FILE=/usr/local/bin/centralreport

CR_LIB_DIR_RELATIVE=/usr/local/lib/
CR_LIB_DIR=/usr/local/lib/centralreport/

CR_CONFIG_DIR=/etc/centralreport/

CONFIG_ASSISTANT=/usr/local/bin/centralreport/config.py

PID_FILE=/var/run/centralreport/centralreport.pid

# OS
CURRENT_OS=
OS_MAC="MacOS"
OS_DEBIAN="Debian"

# Mac OS startup plist
STARTUP_PLIST=/Library/LaunchDaemons/com.centralreport.plist
STARTUP_PLIST_INSTALL=utils/init/mac/com.centralreport.plist

# Debian startup script
STARTUP_DEBIAN=/etc/init.d/centralreport
STARTUP_DEBIAN_INSTALL=utils/init/debian/centralreport

# Libraries directories
SETUPTOOLS_TAR=thirdparties/setuptools.tar.gz

SETUPTOOLS_DIR=thirdparties/setuptools-0.6c11
