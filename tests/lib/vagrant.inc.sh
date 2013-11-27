#!/bin/bash

# ------------------------------------------------------------
# CentralReport Unix/Linux bash functions for tests
# Alpha version. Don't use in production environment!
# ------------------------------------------------------------
# https://github.com/CentralReport
# ------------------------------------------------------------

#
# Performs tests on a chosen virtual machine
#
# PARAMETERS:
#      $1 = The name of the virtual machine
# RETURN:
#      0 = Tests performed without error
#      1 = Error initializing the virtual machine
#      2 = Error during the tests
#
function vagrant_test_vm(){

    if [ "$1" == "" ]; then
        return 1
    fi

    vagrant up $1
    vagrant ssh $1 --command "/vagrant/tests/run_tests.sh -p -s;" 1>>"${ERROR_FILE}" 2>>"${ERROR_FILE}"

    local RETURN_CODE="$?"

    vagrant destroy $1 --force

    if [ ${RETURN_CODE} -ne 0 ]; then
        printLightBox red " Error during executing the Python unit tests on $1"
        return 2
    fi

    printLightBox yellow " All tests done successfully on $1!"
    return 0
}

#
# Performs tests on all available virtual machines
#
# PARAMETERS: None
# RETURN:
#      0 = Tests performed without error
#      1 = Error during the tests
#
function vagrant_perform_tests(){

    VAGRANT_VM=$(vagrant status)

    VAGRANT_ERROR=false
    LINE_NUMBER=3
    VALID_LINE=true

    while [ "${VALID_LINE}" == true ]; do
        CURRENT_LINE=$(echo "${VAGRANT_VM}" | awk 'NR=='"${LINE_NUMBER}"'')
        if [ "${CURRENT_LINE}" == "" ]; then
            VALID_LINE=false
            break
        fi

        vagrant_test_vm $(echo "${CURRENT_LINE}" | awk '{ print $1 }')
        if [ "$?" -ne 0 ]; then
            VAGRANT_ERROR=true
        fi

        LINE_NUMBER=$((LINE_NUMBER+1))
    done

    if [ "${VAGRANT_ERROR}" == true ]; then
        printLightBox red " Error testing the project on Vagrant boxes!"
        return 1
    fi

    printLightBox yellow " All Vagrant boxes are tested successfully!"
    return 0
}
