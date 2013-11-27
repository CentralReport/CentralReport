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

    python ../centralreport/tests.py

    if [ "$?" -ne 0 ]; then
        printLightBox red " Error during executing the Python unit tests!"
        return 1
    fi

    printLightBox yellow " All Python unit tests are OK"
    return 0
}
