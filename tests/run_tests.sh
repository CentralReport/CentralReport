#!/bin/bash

# ------------------------------------------------------------
# CentralReport Unix/Linux bash functions for tests
# Alpha version. Don't use in production environment!
# ------------------------------------------------------------
# https://github.com/CentralReport
# ------------------------------------------------------------

# Importing scripts...
cd "$(dirname "$0")"
source ../bash/log.inc.sh
source lib/functions.inc.sh
source lib/python.inc.sh
source lib/vagrant.inc.sh

TEST_ERRORS=false
ERROR_FILE="/tmp/centralreport_tests.log"
ERROR_METHOD="TESTS"

clear
logFile "-------------- Starting CentralReport tests  --------------"

printBox blue  "---------------------------- CentralReport tests ------------------------------| \
                | \
                This script will perform the selected tests (Unit or Vagrant). | \
                All tests may take a few minutes. You can abort them with CTRL+C."

get_arguments $*

if [ ${ARG_WRONG} == true ]; then
    show_usage
    exit 1
fi

if [ ${ARG_A} == true ]; then
    ARG_P=true
    ARG_V=true
fi

if [ ${ARG_P} == true ]; then
    echo " "
    printTitle "Performing Python unit tests..."
    python_perform_unit_tests

    if [ "$?" -ne 0 ]; then
        TEST_ERRORS=true
    fi
fi

if [ ${ARG_V} == true ]; then
    echo " "
    printTitle "Starting tests on multiple environments using Vagrant..."
    vagrant_perform_tests 2>&1 | tee -a "${ERROR_FILE}"

    if [ "$?" -ne 0 ]; then
        TEST_ERRORS=true
    fi
fi

if [ ${TEST_ERRORS} == true ]; then
    printBox red "Tests failed! | \
                  Please read previous log for more details."
    exit 1
fi

echo " "
printBox blue "All tests done successfully!"
exit 0
