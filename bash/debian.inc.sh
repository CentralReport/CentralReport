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

#
# Starts the CentralReport daemon
#
# PARAMETERS: None
# RETURN:
#   0 = Success
#   The error code otherwise
#
function debian_start_cr {

    printTitle "Starting CentralReport..."

    if [ -f ${CR_PID_FILE} ]; then
        logInfo "CentralReport is already running!"
        return 0

    else
        centralreport start
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

#
# Stops the CentralReport daemon
#
# PARAMETERS: None
# RETURN:
#   0 = Success
#   The error code otherwise
#
function debian_stop_cr {

    printTitle "Stopping CentralReport..."

    if [ ! -f ${CR_PID_FILE} ]; then
        logInfo "CentralReport is already stopped!"
        return 0
    else
        centralreport stop
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

#
# Launchs the CentralReport configuration wizard
#
# PARAMETERS: None
# RETURN:
#   0 in all case
#
function debian_launch_config_assistant {

    logFile "Launching CentralReport configuration wizard..."

    printBox blue "Launching CentralReport configuration wizard..."

    python ${CONFIG_ASSISTANT} < /dev/tty

    return 0
}

# --
# Uninstall functions
# --

#
# Removes the binary file
#
# PARAMETERS: None
# RETURN:
#   0 = Success
#   The error code otherwise
#
function debian_remove_bin {

    logFile "Removing CentralReport binary file..."

    if [ -f ${CR_BIN_FILE} ]; then
        rm -f ${CR_BIN_FILE}
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

#
# Removes the CentralReport library
#
# PARAMETERS: None
# RETURN:
#   0 = Success
#   The error code otherwise
#
function debian_remove_lib {

    logFile "Removing CentralReport library..."

    if [ -d ${CR_LIB_DIR} ]; then
        rm -rf ${CR_LIB_DIR}
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

#
# Removes the startup script
#
# PARAMETERS: None
# RETURN:
#   0 = Success
#   The error code otherwise
#
function debian_remove_startup_script {

    logFile "Removing startup script..."

    if [ -f ${STARTUP_DEBIAN} ]; then
        rm -rf ${STARTUP_DEBIAN}
        RETURN_CODE="$?"

        if [ ${RETURN_CODE} -ne "0" ]; then
            logError "Error deleting startup script at ${STARTUP_DEBIAN} (Error code: ${RETURN_CODE})"
            return 1
        else

            update-rc.d -f centralreport remove
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

#
# Removes the confguration directory
#
# PARAMETERS: None
# RETURN:
#   0 = Success
#   The error code otherwise
#
function debian_remove_config_directory {

    logFile "Removing CentralReport config dir..."

    if [ -d ${CR_CONFIG_DIR} ]; then
        rm -rf ${CR_CONFIG_DIR}
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

#
# Removes the directory which store the PID.
#
# PARAMETERS: None
# RETURN:
#   0 = Success
#   The error code otherwise
#
function debian_remove_pid_directory {

    logFile "Removing PID directory..."

    if [ -d ${CR_PID_DIR} ]; then
        rm -R -f ${CR_PID_DIR}
        RETURN_CODE="$?"

        if [ $? -ne "0" ]; then
            logError "Error deleting pid directory at ${CR_PID_DIR} (Error code: ${RETURN_CODE})"
            return ${RETURN_CODE}
        else
            logFile "PID directory deleted"
        fi
    else
        logInfo "PID directory already deleted!"
    fi

    return 0
}

#
# Removes the directory which store log files
#
# PARAMETERS: None
# RETURN:
#   0 = Success
#   The error code otherwise
#
function debian_remove_log_directory {

    logFile "Removing log directory..."

    if [ -d ${CR_LOG_DIR} ]; then
        rm -R -f ${CR_LOG_DIR}
        RETURN_CODE="$?"

        if [ $? -ne "0" ]; then
            logError "Error deleting log directory at ${CR_LOG_DIR} (Error code: ${RETURN_CODE})"
            return ${RETURN_CODE}
        else
            logFile "Log directory deleted"
        fi
    else
        logInfo "Log directory already deleted!"
    fi

    return 0
}

# --
# Install functions
# --

#
# Copies the binary script is the good directory
#
# PARAMETERS: None
# RETURN:
#   0 = Success
#   The error code otherwise
#
function debian_copy_bin {

    # In some cases, /usr/local and /usr/local/bin doesn't exist. We will creating them in this case.
    if [ ! -d "/usr/local" ]; then
        mkdir /usr/local
    fi
    if [ ! -d "/usr/local/bin" ]; then
        mkdir /usr/local/bin
    fi

    cp -f utils/bin/centralreport ${CR_BIN_FILE}
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

#
# Copies the CentralReport library
#
# PARAMETERS: None
# RETURN:
#   0 = Success
#   The error code otherwise
#
function debian_copy_lib {
    # Copy CentralReport libraries in the right directory.
    # In some cases, /usr/local and /usr/local/bin doesn't exist. We will creating them in this case.
    if [ ! -d "/usr/local" ]; then
        mkdir /usr/local
    fi
    if [ ! -d "/usr/local/lib" ]; then
        mkdir /usr/local/lib
    fi

    mkdir ${CR_LIB_DIR}
    RETURN_CODE="$?"

    if [ ${RETURN_CODE} -ne "0" ]; then
          logError "Error creating CentralReport lib dir at ${CR_LIB_DIR} (Error code: ${RETURN_CODE})"
          return ${RETURN_CODE}
    fi

    cp -f -R centralreport ${CR_LIB_DIR_RELATIVE}
    RETURN_CODE="$?"

    if [ ${RETURN_CODE} -ne "0" ]; then
        logError "Error copying CentralReport libraries in ${CR_LIB_DIR_RELATIVE} (Error code: ${RETURN_CODE})"
        return ${RETURN_CODE}
    fi

    chmod +x ${CR_LIB_DAEMON}
    RETURN_CODE="$?"

    if [ ${RETURN_CODE} -ne "0" ]; then
        logError "Error applying chmod on ${CR_LIB_DAEMON} (Error code: ${RETURN_CODE})"
        return ${RETURN_CODE}
    fi

    return 0

}

#
# Copies the CentralReport init.d script
#
# PARAMETERS: None
# RETURN:
#   0 = Success
#   The error code otherwise
#
function debian_copy_startup_script {

    cp -f -v ${STARTUP_DEBIAN_INSTALL} ${STARTUP_DEBIAN}
    RETURN_CODE="$?"

    if [ ${RETURN_CODE} -ne "0" ]; then
        logError "Error copying startup script at ${STARTUP_PLIST} (Error code: ${RETURN_CODE})"
        return ${RETURN_CODE}
    else
        chmod 755 ${STARTUP_DEBIAN}

        update-rc.d centralreport defaults
        RETURN_CODE="$?"

        if [ ${RETURN_CODE} -ne "0" ]; then
            logError "Error registering startup script with update-rc.d (Error code: ${RETURN_CODE})"
            return ${RETURN_CODE}
        else
            return 0
        fi
    fi
}

#
# Creates the directory which will store configuration files.
# Important: CentralReport user and group must have already been created!
#
# PARAMETERS: None
# RETURN:
#   0 = Success
#   The error code otherwise
#
function debian_create_config_directory {

    if [ -d ${CR_CONFIG_DIR} ]; then
        logFile "Config directory already exist!"
    else
        mkdir ${CR_CONFIG_DIR}
        RETURN_CODE="$?"

        if [ ${RETURN_CODE} -ne "0" ]; then
            logError "Error creating the config directory at ${CR_CONFIG_DIR} (Error code: ${RETURN_CODE})"
            return ${RETURN_CODE}
        fi
    fi

    chown -R centralreport:centralreport ${CR_CONFIG_DIR}
    RETURN_CODE="$?"

    if [ ${RETURN_CODE} -ne "0" ]; then
        logError "Error updating owner of ${CR_CONFIG_DIR} (Error code: ${RETURN_CODE})"
        return ${RETURN_CODE}
    fi

    return 0
}

#
# Creates the directory which will store the logs
# Important: CentralReport user and group must have already been created!
#
# PARAMETERS: None
# RETURN:
#   0 = Success
#   The error code otherwise
#
function debian_create_log_directory {

    if [ -d ${CR_LOG_DIR} ]; then
        logFile "Log directory already exist!"
    else
        mkdir ${CR_LOG_DIR}
        RETURN_CODE="$?"

        if [ ${RETURN_CODE} -ne "0" ]; then
            logError "Error creating the log directory at ${CR_LOG_DIR} (Error code: ${RETURN_CODE})"
            return ${RETURN_CODE}
        fi
    fi

    chown -R centralreport:centralreport ${CR_LOG_DIR}
    RETURN_CODE="$?"

    if [ ${RETURN_CODE} -ne "0" ]; then
        logError "Error updating owner of ${CR_LOG_DIR} (Error code: ${RETURN_CODE})"
        return ${RETURN_CODE}
    fi

    return 0
}

#
# Creates the directory which will store the PID directory
# Important: CentralReport user and group must have already been created!
#
# PARAMETERS: None
# RETURN:
#   0 = Success
#   The error code otherwise
#
function  debian_create_pid_directory {

    if [ -d ${CR_PID_DIR} ]; then
        logFile "PID directory already exist!"
    else
        mkdir ${CR_PID_DIR}
        RETURN_CODE="$?"

        if [ ${RETURN_CODE} -ne "0" ]; then
            logError "Error creating the PID directory at ${CR_PID_DIR} (Error code: ${RETURN_CODE})"
            return ${RETURN_CODE}
        fi
    fi

    chown -R centralreport:centralreport ${CR_PID_DIR}
    RETURN_CODE="$?"

    if [ ${RETURN_CODE} -ne "0" ]; then
        logError "Error updating owner of ${CR_PID_DIR} (Error code: ${RETURN_CODE})"
        return ${RETURN_CODE}
    fi

    return 0
}

# --
# Related to CentralReport user
# --

#
# Verifies if the CentralReport user is already available on this host.
#
# PARAMETERS: None
# RETURN:
#   0 = CentralReport user doesn't exist
#   1 = CentralReport user already exist
#
function debian_verify_user {

    CR_USER_FOUND=$(cat /etc/passwd | grep 'centralreport')
    if [ -z ${CR_USER_FOUND} ]; then
        return 0
    else
        return 1
    fi
}

#
# Adds the CentralReport user to his host.
# This function verifies if CR already exist or not.
#
# PARAMETERS: None
# RETURN:
#   0 = CentralReport user now available
#   The error code otherwise
#
function debian_create_user {

    debian_verify_user
    RETURN_CODE="$?"
    if [ ${RETURN_CODE} -ne 0 ]; then
        logFile "CentralReport user already exist. Skipping this step."
    else
        useradd --system --home /usr/local/lib/centralreport/ --shell /bin/bash --user-group --comment "CentralReport Daemon" centralreport
        RETURN_CODE="$?"

        if [ ${RETURN_CODE} -ne 0 ]; then
            logConsole " "
            logError "Error creating the CentralReport user (Error code: ${RETURN_CODE})"
            return ${RETURN_CODE}
        fi
    fi

    return 0
}

#
# Deletes the CentralReport user from this host.
# This function verifies if CR already exist or not.
#
# PARAMETERS: None
# RETURN:
#   0 = CentralReport user deleted
#   The error code otherwise
#
function debian_remove_user {

    debian_verify_user
    RETURN_CODE="$?"
    if [ ${RETURN_CODE} -eq 0 ]; then
        logFile "CentralReport user already deleted. Skipping this step."
    else
        userdel centralreport
        RETURN_CODE="$?"

        if [ ${RETURN_CODE} -ne 0 ]; then
            logConsole " "
            logError "Error deleting the CentralReport user (Error code: ${RETURN_CODE})"
            return ${RETURN_CODE}
        fi
    fi

    return 0
}

# --
# Install/Uninstall procedure
# --

#
# Launchs the CentralReport installer for Debian
#
# PARAMETERS: None
# RETURN:
#   0 = CentralReport has been installed
#   The error code otherwise
#
function debian_install {

    # Install only can perform if current user has administrative privileges
    if [[ $EUID -ne 0 ]]; then
        logConsole " "
        logError "Installation can only be performed if the current user has administrative privileges!"
        return 1
    fi

    # Uninstall previsous installation, if exist.
    displayAndExec "Stopping CentralReport..." debian_stop_cr
    RETURN_CODE="$?"
    if [ ${RETURN_CODE} -ne 0 ]; then
        return ${RETURN_CODE}
    fi

    # Delete startup plist file
    displayAndExec "Removing CentralReport init.d script..." debian_remove_startup_script
    RETURN_CODE="$?"
    if [ ${RETURN_CODE} -ne 0 ]; then
        return ${RETURN_CODE}
    fi

    # Delete CR bin files
    displayAndExec "Removing CentralReport binary script..." debian_remove_bin
    RETURN_CODE="$?"
    if [ ${RETURN_CODE} -ne 0 ]; then
        return ${RETURN_CODE}
    fi

    # Delete CR lib files
    displayAndExec "Removing CentralReport library..." debian_remove_lib
    RETURN_CODE="$?"
    if [ ${RETURN_CODE} -ne 0 ]; then
        return ${RETURN_CODE}
    fi

    printTitle "Starting installation..."

    displayAndExec "Creating CentralReport user..." debian_create_user
    RETURN_CODE="$?"
    if [ ${RETURN_CODE} -ne 0 ]; then
        return ${RETURN_CODE}
    fi

    displayAndExec "Copying CentralReport binary script..." debian_copy_bin
    RETURN_CODE="$?"
    if [ ${RETURN_CODE} -ne 0 ]; then
        return ${RETURN_CODE}
    fi

    displayAndExec "Copying CentralReport library..." debian_copy_lib
    RETURN_CODE="$?"
    if [ ${RETURN_CODE} -ne 0 ]; then
        return ${RETURN_CODE}
    fi

    displayAndExec "Creating configuration directory..." debian_create_config_directory
    RETURN_CODE="$?"
    if [ ${RETURN_CODE} -ne 0 ]; then
        return ${RETURN_CODE}
    fi

    displayAndExec "Creating log directory..." debian_create_log_directory
    RETURN_CODE="$?"
    if [ ${RETURN_CODE} -ne 0 ]; then
        return ${RETURN_CODE}
    fi

    displayAndExec "Creating PID directory..." debian_create_pid_directory
    RETURN_CODE="$?"
    if [ ${RETURN_CODE} -ne 0 ]; then
        return ${RETURN_CODE}
    fi

    displayAndExec "Copying CentralReport init.d script..." debian_copy_startup_script
    RETURN_CODE="$?"
    if [ ${RETURN_CODE} -ne 0 ]; then
        return ${RETURN_CODE}
    fi

    # Cleaning screen
    clear

    # CR config assistant
    debian_launch_config_assistant

    debian_start_cr
    RETURN_CODE="$?"
    if [ ${RETURN_CODE} -ne 0 ]; then
        return ${RETURN_CODE}
    fi

    return 0
}
#
# Launchs the CentralReport unistall for Debian
#
# PARAMETERS: None
# RETURN:
#   0 = CentralReport has been deleted from this host
#   The error code otherwise
#
function debian_uninstall {

    # Uninstall only can perform if current user is root (or have administrative privileges)
    if [[ $EUID -ne 0 ]]; then
        echo " "
        logError "You must be root to uninstall CentralReport!"
        exit 1
    fi

    # Check if CentralReport is already running, and stop it.
    displayAndExec "Stopping CentralReport..." debian_stop_cr
    RETURN_CODE="$?"
    if [ ${RETURN_CODE} -ne 0 ]; then
        return ${RETURN_CODE}
    fi

    # Delete startup plist file
    displayAndExec "Removing CentralReport init.d script..." debian_remove_startup_script
    RETURN_CODE="$?"
    if [ ${RETURN_CODE} -ne 0 ]; then
        return ${RETURN_CODE}
    fi

    # Delete CR bin files
    displayAndExec "Removing CentralReport binary file..." debian_remove_bin
    RETURN_CODE="$?"
    if [ ${RETURN_CODE} -ne 0 ]; then
        return ${RETURN_CODE}
    fi

    # Delete CR lib files
    displayAndExec "Removing CentralReport library..." debian_remove_lib
    RETURN_CODE="$?"
    if [ ${RETURN_CODE} -ne 0 ]; then
        return ${RETURN_CODE}
    fi

    # Delete CR configuration directory
    displayAndExec "Removing CentralReport configuration directory..." debian_remove_config_directory
    RETURN_CODE="$?"
    if [ ${RETURN_CODE} -ne 0 ]; then
        return ${RETURN_CODE}
    fi

    # Delete CR log file
    displayAndExec "Removing CentralReport log directory..." debian_remove_log_directory
    RETURN_CODE="$?"
    if [ ${RETURN_CODE} -ne 0 ]; then
        return ${RETURN_CODE}
    fi

    # Delete CR PID file
    displayAndExec "Removing CentralReport PID directory..." debian_remove_pid_directory
    RETURN_CODE="$?"
    if [ ${RETURN_CODE} -ne 0 ]; then
        return ${RETURN_CODE}
    fi

    # Delete CR config file
    displayAndExec "Removing CentralReport user..." debian_remove_user
    RETURN_CODE="$?"
    if [ ${RETURN_CODE} -ne 0 ]; then
        return ${RETURN_CODE}
    fi

    return 0
}
