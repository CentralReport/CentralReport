#!/bin/bash

# CentralReport Unix/Linux Indev version.
# By careful! Don't use in production environment!

function getOS(){
    # Getting actual OS (Linux distrib or Unix OS)
    if [ $(uname -s) == "Darwin" ]; then
        CURRENT_OS=${OS_MAC}
    elif [ -f "/etc/debian_version" ] || [ -f "/etc/lsb-release" ]; then
        CURRENT_OS=${OS_DEBIAN}
    fi
}

function getPythonIsInstalled {

    python -V

    if [ $? -ne 0 ]; then
        return 1
    else
        return 0
    fi

}

function displayMessage() {
  echo "$*"
}

function displaytTitle() {
  displayMessage "------------------------------------------------------------------------------"
  displayMessage "$*"
  displayMessage "------------------------------------------------------------------------------"
}

function displayError() {
  displayMessage "$*" >&2
}

# First parameter: ERROR CODE
# Second parameter: MESSAGE
function displayErrorAndExit() {
  local exitcode=$1
  shift
displayerror "$*"
  exit $exitcode
}

# First parameter: MESSAGE
# Others parameters: COMMAND (! not |)
function displayAndExec() {
  local message=$1
  echo -n "[...] $message"
  shift
echo ">>> $*" >> /dev/null 2>&1
  sh -c "$*" >> /dev/null 2>&1
  local ret=$?
  if [ $ret -ne 0 ]; then
echo -e "\r\e[0;31m [ERR]\e[0m $message"
  else
echo -e "\r\e[0;32m [OK ]\e[0m $message"
  fi
return $ret
}
