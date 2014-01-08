#!/bin/bash

# ------------------------------------------------------------
# CentralReport Unix/Linux bash functions for tests
# Alpha version. Don't use in production environment!
# ------------------------------------------------------------
# https://github.com/CentralReport
# ------------------------------------------------------------

#
# Gets all script arguments
#
# PARAMETERS: None
# RETURN: None
#
function get_arguments(){

    # Default values. These vars are global.
    ARG_A=false
    ARG_P=false
    ARG_S=false
    ARG_V=false
    ARG_WRONG=false

    echo " "
    OPTIONS_COUNT=0

    # http://wiki.bash-hackers.org/howto/getopts_tutorial
    while getopts ":apsv" opt; do
        OPTIONS_COUNT=$((OPTIONS_COUNT+1))

        case $opt in
            a) ARG_A=true; logInfo "All tests will be performed"; ;;
            p) ARG_P=true; logInfo "Python unit tests will be performed"; ;;
            s) ARG_S=true; logInfo "System tests will be performed"; ;;
            v) ARG_V=true; logInfo "Vagrant tests will be performand"; ;;
            \?) ARG_WRONG=true ;;
        esac
    done

    # Default value if no option is given
    if [ "${OPTIONS_COUNT}" -eq 0 ]; then
        ARG_A=true
        printBox yellow "All tests will be performed, including Vagrant.| \
                         Performing tests on virtual machines with Vagrant may take several minutes.| \
                         You can use the -h argument to view all available tests. || \
                         Tests will start in 10 seconds. Press CTRL+C to cancel."
        sleep 10;
    fi

    if [ ${ARG_A} == true ]; then
        ARG_P=true
        ARG_S=true
        ARG_V=true
    fi

    echo " "
}

#
# Erases the current log file
#
# PARAMETERS: None
# RETURN: None
#
function init_log_file(){

    echo " " > ${ERROR_FILE}

}

#
# Show script usage
#
# PARAMETERS: None
# RETURN: None
#
function show_usage(){
    echo "Usage: "
    echo "  -a Runs all tests, including Vagrant"
    echo "  -p Executes Python unit tests"
    echo "  -s Executes global system tests"
    echo "  -v Executes all tests using Vagrant"
}
