#!/bin/bash

# ------------------------------------------------------------
# CentralReport Unix/Linux bash dependencies builder
# Alpha version. Don't use in production environment!
# ------------------------------------------------------------
# https://github.com/CentralReport
# ------------------------------------------------------------

source bash/log.inc.sh

PATH_EGGS=centralreport/libs/
PATH_WEB_STATIC=centralreport/cr/static/

#
# Main logic
#
# PARAMETERS: None
# RETURN:
#   0: No error, build finished successfully
#   1: One or more error happend
#
function main(){

    is_error=false

    printBox blue "-- CentralReport - Dependencies builder --"

    if [ ${PWD##*/} != "CentralReport" ]; then
        echo "ERROR - You must be in the root directory of the project to execute this script."
        return 1
    fi

    get_arguments $*

    if [ ${ARG_WRONG} == true ]; then
        printBox red "ERROR! Unknown argument| \
                      Use: build.sh| \
                      -a Build all dependencies (needs NodeJS)| \
                      -p Build Python eggs| \
                      -w Build web front dependencies (needs NodeJS)"
        return 1
    fi

    if [ "${ARG_EGGS}" == true ]; then

        printBox blue "Building Python libraries..."

        build_eggs
        if [ "$?" -ne 0 ]; then
            is_error=true
        fi
    fi

    if [ "${is_error}" == false ] && [ "${ARG_WEB}" == true ]; then

        printBox blue "Building front assets..."

        build_web
        if [ "$?" -ne 0 ]; then
            is_error=true
        fi
    fi

    if [ "${is_error}" == true ]; then
        printBox red "ERROR building dependencies. Please read previous logs."
        return 1
    fi

    printBox green "All dependencies built successfully!"
    return 0
}

#
# Gets all script arguments
#
# PARAMETERS: None
# RETURN: None
#
function get_arguments() {

    ARG_ALL=false
    ARG_EGGS=false
    ARG_WEB=false
    ARG_WRONG=false

    while getopts ":apw" opt; do
        case $opt in
            a) ARG_ALL=true ;;
            p) ARG_EGGS=true ;;
            w) ARG_WEB=true ;;
            \?) ARG_WRONG=true ;;
            :) ARG_WRONG=true ;;
        esac
    done

    if [ "${ARG_ALL}" == true ]; then
        ARG_EGGS=true
        ARG_WEB=true
    fi
}

#
# Builds Python dependencies using Buildout and eggs
#
# PARAMETERS: None
# RETURN:
#   0: Build finished successfully
#   1: Error initializing Buildout
#   2: Error building eggs using Buildout
#
function build_eggs(){

    if [ -d ${PATH_EGGS} ]; then
        printLightBox yellow "Deleting old eggs..."
        rm -Rf ${PATH_EGGS}
    fi

    printLightBox yellow "Creating new egg directory..."
    mkdir ${PATH_EGGS}

    cd utils/libs/eggs/

    printLightBox yellow "Initializing Buildout..."
    python bootstrap.py
    if [ "$?" -ne "0" ]; then
        logError "Error initializing Buildout!"
        cd ../

        return 1
    fi

    printLightBox yellow "Starting Buildout to retrieve eggs..."
    python bin/buildout
    if [ "$?" -ne "0" ]; then
        logError "Error building eggs using Buildout!"
        cd ../

        return 2
    fi

    cd ../../../

    printBox green "Python eggs built successfully!"
    return 0
}

#
# Builds web dependencies (using Node and Grunt JS)
#
# PARAMETERS: None
# RETURN:
#   0: Build finished successfully
#   1: Error building npm modules
#   2: Error building assets using grunt
#
function build_web(){

    if [ -d ${PATH_WEB_STATIC} ]; then
        printLightBox yellow "Deleting old static directory..."
        rm -Rf ${PATH_WEB_STATIC}
    fi

    cd utils/libs/web/

    printLightBox yellow "Getting NodeJS dependancies..."
    npm install
    if [ "$?" -ne "0" ]; then
        logError "Error loading npm modules!"
        cd ../

        return 1
    fi

    printLightBox yellow "Building assets with Grunt..."
    ./node_modules/.bin/grunt prod
    if [ "$?" -ne "0" ]; then
        logError "Error building front assets using grunt!"
        cd ../

        return 2
    fi

    cd ../../../

    printBox green "Web assets built successfully!"
    return 0
}

main $*
exit "$?"
