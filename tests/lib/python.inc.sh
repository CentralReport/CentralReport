#!/bin/bash

# ------------------------------------------------------------
# CentralReport Unix/Linux bash functions for tests
# Alpha version. Don't use in production environment!
# ------------------------------------------------------------
# https://github.com/CentralReport
# ------------------------------------------------------------

#
# Performs the Python unit tests
#
# PARAMETERS: None
# RETURN:
#      0 = Tests performed without error
#      1 = Error during tests
#
function python_perform_unit_tests(){

    python ../centralreport/tests.py 2>&1 | tee -a "${ERROR_FILE}"

    if [ "$?" -ne 0 ]; then
        local ERROR_MESSAGE="Error during executing the Python unit tests!"

        logFile "${ERROR_MESSAGE}"
        printLightBox red "${ERROR_MESSAGE}"
        return 1
    fi

    local OK_MESSAGE="All Python unit tests are OK"

    logFile "${OK_MESSAGE}"
    printLightBox yellow "${OK_MESSAGE}"
    return 0
}
