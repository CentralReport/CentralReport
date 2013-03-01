#!/bin/bash

# ------------------------------------------------------------
# CentralReport Unix/Linux - Debian functions
# Alpha version. Don't use in production environment!
# ------------------------------------------------------------
# https://github.com/miniche/CentralReport/
# ------------------------------------------------------------

# This file contains all functions to manage CR install/unistall on a Debian/Ubuntu distribution.

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

    logFile "Removing CentralReport bin files..."

    if [ -d ${INSTALL_DIR} ]; then
        displayAndExec "Removing existing install directory..." rm -rfv $INSTALL_DIR
        RETURN_CODE="$?"

        if [ ${RETURN_CODE} -ne "0" ]; then
            logError "Error deleting CentralReport bin directory at ${INSTALL_DIR} (Error code: ${RETURN_CODE})"
            return ${RETURN_CODE}
        else
            logFile "CentralReport bin files removed"
            return 0
        fi
    else
        logInfo "CentralReport bin directory doesn't exist!"
        return 0
    fi
}

function debian_remove_config {

    logFile "Removing CentralReport config file..."

    if [ -f ${CONFIG_FILE} ]; then
        displayAndExec "Removing existing config file..." rm -fv $CONFIG_FILE
        RETURN_CODE="$?"

        if [ ${RETURN_CODE} -ne "0" ]; then
            logError "Error deleting CentralReport config file at ${CONFIG_FILE} (Error code: ${RETURN_CODE})"
            return ${RETURN_CODE}
        else
            logFile "CentralReport config file deleted"
            return 0
        fi
    else
        logInfo "CentralReport config file not found!"
        return 0
    fi
}

function debian_remove_startup_script {

    logFile "Removing startup script..."

    if [ -f ${STARTUP_DEBIAN} ]; then
        displayAndExec "Removing existing startup script..." rm -rfv $STARTUP_DEBIAN
        RETURN_CODE="$?"

        if [ ${RETURN_CODE} -ne "0" ]; then
            logError "Error deleting startup script at ${STARTUP_DEBIAN} (Error code: ${RETURN_CODE})"
            return 1
        else

            displayAndExec "Removing startup service..." update-rc.d -f centralreport.sh remove
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
    # Copy CentralReport files in the right directory.
    mkdir ${INSTALL_DIR}

    if [ $? -ne "0" ]; then
          logError "Error creating CentralReport dir at ${INSTALL_DIR} (Error code: $?)"
          return 1
    else
        displayAndExec "Copying CentralReport in the good directory..." cp -R -f -v centralreport ${PARENT_DIR}
        RETURN_CODE="$?"

        if [ ${RETURN_CODE} -ne "0" ]; then
            logError "Error copying CentralReport bin files in ${PARENT_DIR} (Error code: ${RETURN_CODE})"
            return ${RETURN_CODE}
        else
            return 0
        fi
    fi
}

function debian_cp_startup_plist {
    # Copy startup plist for launchd in the right directory.

    displayAndExec "Copying startup script in the good directory..." cp -f -v ${STARTUP_DEBIAN_INSTALL} ${STARTUP_DEBIAN}
    RETURN_CODE="$?"

    if [ ${RETURN_CODE} -ne "0" ]; then
      logError "Error copying startup script at ${STARTUP_PLIST} (Error code: ${RETURN_CODE})"
      return ${RETURN_CODE}
    else
        chmod 755 ${STARTUP_DEBIAN}

        displayAndExec "Registering startup script" update-rc.d centralreport.sh defaults
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
# Install procedure
# --

function debian_install {

    # Install only can perform if current user has administrative privileges
    if [[ $EUID -ne 0 ]]; then
        echo " "
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

    debian_cp_startup_plist
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
