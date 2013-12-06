#!/bin/bash

# ------------------------------------------------------------
# CentralReport Unix/Linux bash functions for System tests
# Alpha version. Don't use in production environment!
# ------------------------------------------------------------
# https://github.com/CentralReport
# ------------------------------------------------------------

#
# Performs all tests related to the installer
#
# PARAMETERS: None
# RETURN:
#      0 = Tests performed without error
#      1 = Error during the tests
#
function system_test_installer(){

    logInfo "Testing the bash installer..."

    cd ../
    ./install.sh -k -s 1>/dev/null | tee -a "${ERROR_FILE}"
    cd tests/

    if [ "$?" -ne 0 ]; then
        printLightBox red " Error validating the bash installer!"
        return 2
    fi

    printLightBox green " The installer has return the success code"
    return 0

}

#
# Performs all tests related to the uninstaller
#
# PARAMETERS: None
# RETURN:
#      0 = Tests performed without error
#      1 = Error during the tests
#
function system_test_uninstaller(){

    logInfo "Testing the bash uninstaller..."

    cd ../
    ./uninstall.sh -k -s 1>/dev/null | tee -a "${ERROR_FILE}"
    cd tests/

    if [ "$?" -ne 0 ]; then
        printLightBox red " Error validating the bash uninstaller!"
        return 2
    fi

    printLightBox green " The uninstaller has return the success code"
    return 0

}

#
# Checks whether CentralReport is running
#
# PARAMETERS: None
# RETURN:
#      0 = CentralReport is running
#      1 = Error during the tests
#
function system_test_status(){

    logInfo "Testing whether CentralReport is running..."

    CR_PID=$(/usr/local/bin/centralreport pid)

    if [ "$?" -ne 0 ]; then
        printLightBox red " Error executing 'centralreport pid' command!"
        return 1
    fi

    if [ "${CR_PID}" -eq 0 ]; then
        printLightBox red " CentralReport is not running!"
        return 1
    fi

    printLightBox green "CentralReport is running with PID ${CR_PID}"
    return 0

}


#
# Executes all system tests
#
# PARAMETERS: None
# RETURN:
#      0 = Tests performed without error
#      1 = Error during the tests
#
function system_test_suite(){

    local ERROR=false

    echo " "
    printTitle "Starting system tests..."

    system_test_installer
    if [ "$?" -ne 0 ]; then
        ERROR=true
    fi

    system_test_status
    if [ "$?" -ne 0 ]; then
        ERROR=true
    fi

    system_test_uninstaller
    if [ "$?" -ne 0 ]; then
        ERROR=true
    fi

    if "${ERROR}" == true ]; then
        return 1
    fi

    return 0
}
