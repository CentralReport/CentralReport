#!/bin/bash

# ------------------------------------------------------------
# CentralReport Unix/Linux - Debian functions
# Alpha version. Don't use in production environment!
# ------------------------------------------------------------
# https://github.com/miniche/CentralReport/
# ------------------------------------------------------------

# This file contains all functions to manage CR install/unistall on a Debian/Ubuntu distribution.

source vars.sh

# --
# CentralReport daemon functions
# --
function debian_start_cr {

    printTitle "Starting CentralReport..."

    if [ -f ${PID_FILE} ]; then
        logInfo "CentralReport is already running!"
        return 0

    else
        python ${INSTALL_DIR}/centralreport.py start
        RETURN_CODE="$?"

        if [ ${RETURN_CODE} -ne "0" ]; then
            logError "Error starting CentralReport (Error code: ${RETURN_CODE})!"
            return ${RETURN_CODE}
        else
            # Waiting three seconds before all CR threads really started.
            sleep 3

            logInfo "CentralReport started!"
            return 0
        fi
    fi
}

function debian_stop_cr {

    printTitle "Stopping CentralReport..."

    if [ ! -f ${PID_FILE} ]; then
        logInfo "CentralReport is already stopped!"
        return 0
    else
        python ${INSTALL_DIR}/centralreport.py stop
        RETURN_CODE="$?"

        if [ ${RETURN_CODE} -ne "0" ] && [ ${RETURN_CODE} -ne "143" ]; then
            logError "Error stopping CentralReport (Error code: ${RETURN_CODE})"
            return ${RETURN_CODE}
        else
            logInfo "CentralReport stopped"
            return 0
        fi
    fi
}

# --
# CentralReport config assistant
# --
function debian_config_assistant {

    logFile "Launching CentralReport configuration wizard..."

    printBox blue "Launching CentralReport configuration wizard..."

    python ${CONFIG_ASSISTANT} < /dev/tty

    return 0
}

# --
# Uninstall functions
# --
function debian_remove_bin {

    logFile "Removing CentralReport binary file..."

    if [ -f ${CR_BIN_FILE} ]; then
        displayAndExec "Removing existing binary file..." rm -f ${CR_BIN_FILE}
        RETURN_CODE="$?"

        if [ ${RETURN_CODE} -ne "0" ]; then
            logError "Error deleting CentralReport binary file at ${CR_BIN_FILE} (Error code: ${RETURN_CODE})"
            return ${RETURN_CODE}
        else
            logFile "CentralReport binary file removed"
            return 0
        fi
    else
        logInfo "CentralReport binary file doesn't exist!"
        return 0
    fi
}

function debian_remove_lib {

    logFile "Removing CentralReport lib files..."

    if [ -d ${CR_LIB_DIR} ]; then
        displayAndExec "Removing existing CentralReport libraries..." rm -rf ${CR_LIB_DIR}
        RETURN_CODE="$?"

        if [ ${RETURN_CODE} -ne "0" ]; then
            logError "Error deleting CentralReport lib directory at ${CR_LIB_DIR} (Error code: ${RETURN_CODE})"
            return ${RETURN_CODE}
        else
            logFile "CentralReport lib files removed"
            return 0
        fi
    else
        logInfo "CentralReport lib directory doesn't exist!"
        return 0
    fi
}

function debian_remove_config {

    logFile "Removing CentralReport config dir..."

    if [ -d ${CR_CONFIG_DIR} ]; then
        displayAndExec "Removing existing config dir..." rm -rf ${CR_CONFIG_DIR}
        RETURN_CODE="$?"

        if [ ${RETURN_CODE} -ne "0" ]; then
            logError "Error deleting CentralReport config dir at ${CR_CONFIG_DIR} (Error code: ${RETURN_CODE})"
            return ${RETURN_CODE}
        else
            logFile "CentralReport config dir deleted"
            return 0
        fi
    else
        logInfo "CentralReport config dir not found!"
        return 0
    fi
}

function debian_remove_startup_script {

    logFile "Removing startup script..."

    if [ -f ${STARTUP_DEBIAN} ]; then
        displayAndExec "Removing existing startup script..." rm -rf ${STARTUP_DEBIAN}
        RETURN_CODE="$?"

        if [ ${RETURN_CODE} -ne "0" ]; then
            logError "Error deleting startup script at ${STARTUP_DEBIAN} (Error code: ${RETURN_CODE})"
            return 1
        else

            displayAndExec "Removing startup service..." update-rc.d -f centralreport remove
            RETURN_CODE="$?"

            if [ ${RETURN_CODE} -ne "0" ]; then
                logError "Error removing startup script with update-rc.d (Error code: ${RETURN_CODE})"
                return ${RETURN_CODE}
            else
                logFile "Startup script deleted"
                return 0
            fi
            return 0
        fi
    else
        logInfo "Startup plist file not found!"
        return 0
    fi
}

# --
# Install functions
# --
function debian_cp_bin {
    # Copy CentralReport binary file in the right directory.
    # In some cases, /usr/local and /usr/local/bin doesn't exist. We will creating them in this case.
    if [ ! -d "/usr/local" ]; then
        mkdir /usr/local
    fi
    if [ ! -d "/usr/local/bin" ]; then
        mkdir /usr/local/bin
    fi

    displayAndExec "Installing CentralReport binary file in the good directory..." cp -f centralreport ${CR_BIN_FILE}
    RETURN_CODE="$?"

    if [ ${RETURN_CODE} -ne "0" ]; then
        logError "Error copying CentralReport binary file in ${CR_BIN_FILE} (Error code: ${RETURN_CODE})"
        return ${RETURN_CODE}
    else
        chmod +x ${CR_BIN_FILE}
        RETURN_CODE="$?"

        if [ ${RETURN_CODE} -ne "0" ]; then
            logError "Error applying chmod on ${CR_BIN_FILE} (Error code: ${RETURN_CODE})"
            return ${RETURN_CODE}
        else
            return 0
        fi
    fi
}

function debian_cp_lib {
    # Copy CentralReport libraries in the right directory.
    # In some cases, /usr/local and /usr/local/bin doesn't exist. We will creating them in this case.
    if [ ! -d "/usr/local" ]; then
        mkdir /usr/local
    fi
    if [ ! -d "/usr/local/lib" ]; then
        mkdir /usr/local/lib
    fi

    sudo mkdir ${CR_LIB_DIR}
    RETURN_CODE="$?"

    if [ ${RETURN_CODE} -ne "0" ]; then
          displayError "Error creating CentralReport lib dir at ${CR_LIB_DIR} (Error code: ${RETURN_CODE})"
          return ${RETURN_CODE}
    else
        displayAndExec "Copying CentralReport libraries in the good directory..." cp -f -R centralreport ${CR_LIB_DIR_RELATIVE}
        RETURN_CODE="$?"

        if [ ${RETURN_CODE} -ne "0" ]; then
            logError "Error copying CentralReport libraries in ${CR_LIB_DIR_RELATIVE} (Error code: ${RETURN_CODE})"
            return ${RETURN_CODE}
        else
            return 0
        fi
    fi

}

function debian_cp_startup_script {
    # Copy startup plist for launchd in the right directory.

    displayAndExec "Copying startup script in the good directory..." cp -f -v ${STARTUP_DEBIAN_INSTALL} ${STARTUP_DEBIAN}
    RETURN_CODE="$?"

    if [ ${RETURN_CODE} -ne "0" ]; then
      logError "Error copying startup script at ${STARTUP_PLIST} (Error code: ${RETURN_CODE})"
      return ${RETURN_CODE}
    else
        chmod 755 ${STARTUP_DEBIAN}

        displayAndExec "Registering startup script" update-rc.d centralreport defaults
        RETURN_CODE="$?"

        if [ ${RETURN_CODE} -ne "0" ]; then
          logError "Error registering startup script with update-rc.d (Error code: ${RETURN_CODE})"
          return ${RETURN_CODE}
        else
            return 0
        fi
    fi
}


# --
# Related to CentralReport user
# --

function debian_user_verify {
    # Checks if the CentralReport user already exist, or not
    # Returns 0 if the CR user doesn't exist

    RETURN_USER=""
    cat /etc/passwd | grep 'centralreport' >> ${RETURN_USER}
    if [ ${RETURN_USER} == "" ]; then
        return 0
    else
        return 1
    fi
}

function debian_user_new {
    # Adds the CentralReport user for security purposes

    useradd --system --home /usr/local/bin/centralreport/ --shell /bin/sh --user-group --comment "CentralReport Daemon" centralreport
    RETURN_CODE="$?"

    if [ ${RETURN_CODE} -ne 0 ]; then
        logConsole " "
        logError "Error creating the CentralReport user (Error code: ${RETURN_CODE}"
        exit 1
    fi

    exit 0
}

function debian_user_del {
    # Deletes the CentralReport user

    userdel centralreport
    RETURN_CODE="$?"

    if [ ${RETURN_CODE} -ne 0 ]; then
        logConsole " "
        logError "Error deleting the CentralReport user (Error code: ${RETURN_CODE}"
        exit 1
    fi

    exit 0
}

# --
# Install procedure
# --

function debian_install {

    # Install only can perform if current user has administrative privileges
    if [[ $EUID -ne 0 ]]; then
        logConsole " "
        logError "Installation can only be performed if the current user has administrative privileges!"
        exit 1
    fi

    # Uninstall previsous installation, if exist.
    debian_stop_cr
    RETURN_CODE="$?"
    if [ ${RETURN_CODE} -ne 0 ]; then
        return ${RETURN_CODE}
    fi

    # Delete CR bin files
    debian_remove_bin
    RETURN_CODE="$?"
    if [ ${RETURN_CODE} -ne 0 ]; then
        return ${RETURN_CODE}
    fi

    # Delete startup plist file
    debian_remove_startup_script
    RETURN_CODE="$?"
    if [ ${RETURN_CODE} -ne 0 ]; then
        return ${RETURN_CODE}
    fi

    printTitle "Starting installation..."

    debian_cp_bin
    RETURN_CODE="$?"
    if [ ${RETURN_CODE} -ne 0 ]; then
        return ${RETURN_CODE}
    fi

    debian_cp_startup_script
    RETURN_CODE="$?"
    if [ ${RETURN_CODE} -ne 0 ]; then
        return ${RETURN_CODE}
    fi

    printTitle "Installing third-party softwares..."
    logInfo " (Please consult http://github.com/miniche/CentralReport for licenses) "


    # Setuptools (easy_install included)
    printTitle "Installing Setuptools..."
    displayAndExec "Untaring Setuptools..." tar -xzvf ${SETUPTOOLS_TAR} -C thirdparties/
    RETURN_CODE="$?"
    if [ ${RETURN_CODE} -ne 0 ]; then
        return ${RETURN_CODE}
    fi

    cd ${SETUPTOOLS_DIR};
    displayAndExec "Installing Setuptools..." python setup.py install
    RETURN_CODE="$?"
    cd ../../;
    if [ ${RETURN_CODE} -ne 0 ]; then
        return ${RETURN_CODE}
    fi

    displayAndExec "Deleting installation files..." rm -Rf ${SETUPTOOLS_DIR}
    RETURN_CODE="$?"
    if [ ${RETURN_CODE} -ne 0 ]; then
        return ${RETURN_CODE}
    fi


    # Using easy_install (included in setuptools), we're installing required libraries...
    printTitle "Installing required libraries..."

    # CherryPy (webserver)
    displayAndExec "Installing CherryPy..." easy_install CherryPy
    RETURN_CODE="$?"
    if [ ${RETURN_CODE} -ne 0 ]; then
        return ${RETURN_CODE}
    fi

    # Jinja2 (Templates for CherryPy)
    displayAndExec "Installing Jinja 2..." easy_install Jinja2
    RETURN_CODE="$?"
    if [ ${RETURN_CODE} -ne 0 ]; then
        return ${RETURN_CODE}
    fi

    # Routes (route dispatcher for CherryPy)
    displayAndExec "Installing Routes..." easy_install routes
    RETURN_CODE="$?"
    if [ ${RETURN_CODE} -ne 0 ]; then
        return ${RETURN_CODE}
    fi

    # Cleaning screen
    clear

    # CR config assistant
    debian_config_assistant

    debian_start_cr
    RETURN_CODE="$?"
    if [ ${RETURN_CODE} -ne 0 ]; then
        return ${RETURN_CODE}
    fi

    return 0
}

# --
# Uninstall procedure
# --

function debian_uninstall {

    # Uninstall only can perform if current user is root (or have administrative privileges)
    if [[ $EUID -ne 0 ]]; then
        echo " "
        logError "You must be root to uninstall CentralReport!"
        exit 1
    fi

    # Check if CentralReport is already running, and stop it.
    debian_stop_cr
    RETURN_CODE="$?"
    if [ ${RETURN_CODE} -ne 0 ]; then
        return ${RETURN_CODE}
    fi

    # Delete CR bin files
    debian_remove_bin
    RETURN_CODE="$?"
    if [ ${RETURN_CODE} -ne 0 ]; then
        return ${RETURN_CODE}
    fi

    # Delete CR config file
    debian_remove_config
    RETURN_CODE="$?"
    if [ ${RETURN_CODE} -ne 0 ]; then
        return ${RETURN_CODE}
    fi

    # Delete startup plist file
    debian_remove_startup_script
    RETURN_CODE="$?"
    if [ ${RETURN_CODE} -ne 0 ]; then
        return ${RETURN_CODE}
    fi

    return 0
}
