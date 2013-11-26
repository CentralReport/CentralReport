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
    ARG_V=false
    ARG_WRONG=false

    echo " "

    # http://wiki.bash-hackers.org/howto/getopts_tutorial
    while getopts ":apv" opt; do
        case $opt in
            a) ARG_A=true; echo "All tests will be performed"; ;;
            p) ARG_P=true; echo "Python unit tests will be performed"; ;;
            v) ARG_V=true; echo "Vagrant tests will be performand"; ;;
            \?) ARG_WRONG=true ;;
        esac
    done

    echo " "
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
    echo "  -v Executes all tests using Vagrant"
}
