#!/bin/bash

# ------------------------------------------------------------
# CentralReport Unix/Linux - OS X functions
# Alpha version. Don't use in production environment!
# ------------------------------------------------------------
# https://github.com/miniche/CentralReport/
# ------------------------------------------------------------

# This file contains all functions to manage CR install/unistall on a Mac.

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
function macos_start_cr {

    logFile "Starting CentralReport..."

    if [ -f ${CR_PID_FILE} ]; then
        logInfo "CentralReport is already running!"
        return 0

    else
        sudo python ${INSTALL_DIR}/centralreport.py start
        RETURN_CODE="$?"

        if [ ${RETURN_CODE} -ne "0" ]; then
            logError "Error starting CentralReport (Error code: ${RETURN_CODE})"
            return ${RETURN_CODE}
        else
            # Waiting three seconds before all CR threads really started.
            sleep 3

            logInfo "CentralReport started"
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
function macos_stop_cr {

    logFile "Stopping CentralReport..."

    if [ ! -f ${CR_PID_FILE} ]; then
        logInfo "CentralReport is already stopped!"
        return 0
    else
        sudo python ${INSTALL_DIR}/centralreport.py stop
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
function macos_launch_config_assistant {

    logFile "Launching CentralReport configuration wizard..."

    printBox blue "Launching CentralReport configuration wizard..."

    sudo python ${CONFIG_ASSISTANT} < /dev/tty

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
function macos_remove_bin {

    logFile "Removing CentralReport binary script..."

    if [ -f ${CR_BIN_FILE} ]; then
        sudo rm -f ${CR_BIN_FILE}
        RETURN_CODE="$?"

        if [ ${RETURN_CODE} -ne "0" ]; then
            logError "Error deleting CentralReport binary script at ${CR_BIN_FILE} (Error code: ${RETURN_CODE})"
            return ${RETURN_CODE}
        else
            logFile "CentralReport binary script have been removed"
            return 0
        fi
    else
        logInfo "CentralReport binary script doesn't exist!"
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
function macos_remove_lib {

    logFile "Removing CentralReport lib files..."

    if [ -d ${CR_LIB_DIR} ]; then
        sudo rm -rf ${CR_LIB_DIR}
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
# Removes the configuration directory
#
# PARAMETERS: None
# RETURN:
#   0 = Success
#   The error code otherwise
#
function macos_remove_config {

    logFile "Removing CentralReport config file..."

    if [ -f ${CONFIG_FILE} ]; then
        sudo rm -f ${CONFIG_FILE}
        RETURN_CODE="$?"

        if [ ${RETURN_CODE} -ne "0" ]; then
            logError "Error deleting CentralReport config file at ${CONFIG_FILE} (Error code: ${RETURN_CODE})"
            return ${RETURN_CODE}
        else
            logFile "CentralReport config file removed"
            return 0
        fi
    else
        logInfo "CentralReport config file not found!"
        return 0
    fi
}

#
# Removes the CentralReport startup plist
#
# PARAMETERS: None
# RETURN:
#   0 = Success
#   The error code otherwise
#
function macos_remove_startup_plist {

    logFile "Removing startup plist..."

    if [ -f ${STARTUP_PLIST} ]; then
        sudo rm -f ${STARTUP_PLIST}
        RETURN_CODE="$?"

        if [ $? -ne "0" ]; then
            logError "Error deleting startup plist file at ${STARTUP_PLIST} (Error code: ${RETURN_CODE})"
            return ${RETURN_CODE}
        else
            logFile "Startup plist removed"
        fi
    else
        logInfo "Startup plist file not found!"
    fi

    return 0
}

#
# Removes the directory which store the PID.
#
# PARAMETERS: None
# RETURN:
#   0 = Success
#   The error code otherwise
#
function macos_remove_pid_directory {

    logFile "Removing PID directory..."

    if [ -d ${CR_PID_DIR} ]; then
        sudo rm -R -f ${CR_PID_DIR}
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
# Removes the directory which store log files.
#
# PARAMETERS: None
# RETURN:
#   0 = Success
#   The error code otherwise
#
function macos_remove_log_directory {

    logFile "Removing log directory..."

    if [ -d ${CR_LOG_DIR} ]; then
        sudo rm -R -f ${CR_LOG_DIR}
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
function macos_cp_bin {
    # In some cases, /usr/local and /usr/local/bin doesn't exist. We will creating them in this case.
    if [ ! -d "/usr/local" ]; then
        sudo mkdir /usr/local
    fi
    if [ ! -d "/usr/local/bin" ]; then
        sudo mkdir /usr/local/bin
    fi


    sudo cp -f utils/bin/centralreport ${CR_BIN_FILE}
    RETURN_CODE="$?"

    if [ ${RETURN_CODE} -ne "0" ]; then
        logError "Error copying CentralReport binary script in ${CR_BIN_FILE} (Error code: ${RETURN_CODE})"
        return ${RETURN_CODE}
    else
        sudo chmod +x ${CR_BIN_FILE}
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
function macos_cp_lib {

    # In some cases, /usr/local and /usr/local/bin doesn't exist. We will creating them in this case.
    if [ ! -d "/usr/local" ]; then
        sudo mkdir /usr/local
    fi
    if [ ! -d "/usr/local/lib" ]; then
        sudo mkdir /usr/local/lib
    fi

    sudo mkdir ${CR_LIB_DIR}
    RETURN_CODE="$?"

    if [ ${RETURN_CODE} -ne "0" ]; then
          logError "Error creating CentralReport library directory at ${CR_LIB_DIR} (Error code: ${RETURN_CODE})"
          return ${RETURN_CODE}
    else
        sudo cp -R -f centralreport ${CR_LIB_DIR_RELATIVE}
        RETURN_CODE="$?"

        if [ ${RETURN_CODE} -ne "0" ]; then
            logError "Error copying CentralReport libraries in ${CR_LIB_DIR} (Error code: ${RETURN_CODE})"
            return ${RETURN_CODE}
        else
            return 0
        fi
    fi

}

#
# Copies the CentralReport startup plist for Launchd.
#
# PARAMETERS: None
# RETURN:
#   0 = Success
#   The error code otherwise
#
function macos_cp_startup_plist {

    sudo cp -f -v ${STARTUP_PLIST_INSTALL} ${STARTUP_PLIST}
    RETURN_CODE="$?"

    if [ ${RETURN_CODE} -ne "0" ]; then
      logError "Error copying startup plist at ${STARTUP_PLIST} (Error code: ${RETURN_CODE})"
      return ${RETURN_CODE}
    else
        return 0
    fi
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
function  macos_create_pid_directory {

    if [ -d ${CR_PID_DIR} ]; then
        logFile "PID directory already exist!"
    else
        sudo mkdir ${CR_PID_DIR}
        RETURN_CODE="$?"

        if [ ${RETURN_CODE} -ne "0" ]; then
            logError "Error creating the PID directory at ${CR_PID_DIR} (Error code: ${RETURN_CODE})"
            return ${RETURN_CODE}
        fi
    fi

    sudo chown -R _centralreport:daemon ${CR_PID_DIR}
    RETURN_CODE="$?"

    if [ ${RETURN_CODE} -ne "0" ]; then
        logError "Error updating owner of ${CR_PID_DIR} (Error code: ${RETURN_CODE})"
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
function macos_create_log_directory {

    if [ -d ${CR_LOG_DIR} ]; then
        logFile "Log directory already exist!"
    else
        sudo mkdir ${CR_LOG_DIR}
        RETURN_CODE="$?"

        if [ ${RETURN_CODE} -ne "0" ]; then
            logError "Error creating the log directory at ${CR_LOG_DIR} (Error code: ${RETURN_CODE})"
            return ${RETURN_CODE}
        fi
    fi

    sudo chown -R _centralreport:wheel ${CR_LOG_DIR}
    RETURN_CODE="$?"

    if [ ${RETURN_CODE} -ne "0" ]; then
        logError "Error updating owner of ${CR_LOG_DIR} (Error code: ${RETURN_CODE})"
        return ${RETURN_CODE}
    fi

    return 0
}

# --
# Related to CentralReport user
# --

#
# Adds the CentralReport user for security purposes
# This function verifies if CR already exist or not and will also create a dedicated group.
#
# PARAMETERS: None
# RETURN:
#   0 = CentralReport user now available
#   The error code otherwise
#
function macos_user_new {

    # Scheme of this (big) function:

    #   _centralreport user already exits?
    #       -> if not: find a UniqueID available in 0-499 (otherwise, exit)
    #           -> Be sure that the UniqueID found is really unique (otherwise, exit)
    #           -> _centralreport group already exists?
    #               -> if not, UniqueID is available in groups?
    #                   -> if not, find a PrimaryGroupID available in 0-499
    #                   -> Be sure the PrimaryGroupID found is really unique
    #               -> Create a new group with UGID or UID
    #               -> Be sure that the group is created
    #       -> Create a new user with UID
    #       -> Be sure that the user is created


    macos_user_verify
    local GROUP_UNIQUE_ID="$?"
    if [ ${GROUP_UNIQUE_ID} -ne 0 ]; then
        logFile "CentralReport user already exists. Skipping this step."
        return 0
    fi

    logFile "CentralReport user doesn't exist. Creating the dedicated user..."

    # Getting the last Unique ID available for system users.
    # From: http://superuser.com/questions/553374/find-available-ids-lower-than-500-vis-dscl
    local continue="no"
    local number_used="dontknow"
    local fnumber_work_backwards_from=499
    local fnumber=${fnumber_work_backwards_from}
    local user_id=0
    until [ ${continue} = "yes" ] ; do
      if [ `dscl . -list /Users UniqueID | awk '{print $2, "\t", $1}' | sort -ug | grep -c "${fnumber}"` -gt 0 ] ; then
        number_used=true
      else
        number_used=false
      fi
      if [ ${number_used} = "true" ] ; then
        fnumber=`expr ${fnumber} - 1`
      else
        user_id="${fnumber}"
        continue="yes"
      fi
    done;

    logFile "New UniqueID available: ${user_id}"

    if [ ${user_id} -eq 0 ]; then
        logError "Enable to find an available UniqueID for CentralReport user."
        return 1
    elif [ ${user_id} -le 100 ]; then
        logError "Enable to find an available UniqueID for CentralReport greater than 100."
        return 1
    fi

    # Now, we must check in the UID is really available.
    if dscl . -readall /Users | grep -q "UniqueID: *${user_id}$" ; then
	    logError "UID ${user_id} is already in use"
	    return 1
    fi

    # Checks if CentralReport group already exists.
    macos_group_verify
    GROUP_UNIQUE_ID="$?"
    if [ ${GROUP_UNIQUE_ID} -ne 0 ]; then
        logFile "CentralReport group already exists. Skipping this step."
    else

        # CentralReport group doesn't exist. So, the same UGID as UID is available?
        if dscl . -readall /Groups | grep -q "PrimaryGroupID: *${user_id}$" ; then
            logFile "UGID ${user_id} is already in use. Find a new one."

            # Creating a new group...
            logFile "Creating a new group for CentralReport..."

            # We get the last Primary Group ID available for system groups.
            continue="no"
            number_used="dontknow"
            fnumber_work_backwards_from=499
            fnumber=${fnumber_work_backwards_from}
            GROUP_UNIQUE_ID=0
            until [ ${continue} = "yes" ] ; do
                if [ `dscl . -list /Users UniqueID | awk '{print $2, "\t", $1}' | sort -ug | grep -c "${fnumber}"` -gt 0 ] ; then
                    number_used=true
                else
                    number_used=false
                fi

                if [ ${number_used} = "true" ] ; then
                    fnumber=`expr ${fnumber} - 1`
                else
                    GROUP_UNIQUE_ID="${fnumber}"
                    continue="yes"
                fi
            done;

            logFile "New PrimaryGroupID available: ${GROUP_UNIQUE_ID}"

            if [ ${user_id} -eq 0 ]; then
                logError "Enable to find an available PrimaryGroupID for CentralReport group."
                return 1
            elif [ ${user_id} -le 100 ]; then
                logError "Enable to find an available PrimaryGroupID for CentralReport group greater than 100."
                return 1
            fi
        else
            # We can use the same ID for the user and the group.
            logFile "${user_id} UID is also available for UGID"
            GROUP_UNIQUE_ID=${user_id}
        fi

        # Now, we must check in the UGID is really available.
        if dscl . -readall /Groups | grep -q "PrimaryGroupID: *${GROUP_UNIQUE_ID}$" ; then
            logError "UGID ${GROUP_UNIQUE_ID} is already in use"
            return 1
        fi

        # Good, isn't it? Victoire de canard!
        # We can add our group now!
        logFile "Executing critical commands... Please wait..."
        sudo dscl . create /Groups/_centralreport
        sudo dscl . create /Groups/_centralreport PrimaryGroupID ${GROUP_UNIQUE_ID}

        # Checking if the group have been created
        macos_group_verify
        GROUP_UNIQUE_ID="$?"
        if [ ${GROUP_UNIQUE_ID} -eq 0 ]; then
            logFile "Error creating the CentralReport group."
            return 1
        fi

        logFile "Group successfully created!"
    fi

    # Now, we can create our user. The victory is near!
    sudo dscl . -create /Users/_centralreport
    sudo dscl . -create /Users/_centralreport UserShell /bin/bash
    sudo dscl . -create /Users/_centralreport RealName "CentralReport daemon"
    sudo dscl . -create /Users/_centralreport UniqueID ${user_id}
    sudo dscl . -create /Users/_centralreport PrimaryGroupID ${GROUP_UNIQUE_ID}
    sudo dscl . -create /Users/_centralreport NFSHomeDirectory /usr/local/lib/centralreport
    sudo dscl . -passwd /Users/_centralreport "*"

    # Checking if the user have been created
    macos_user_verify
    USER_UNIQUE_ID="$?"
    if [ ${USER_UNIQUE_ID} -eq 0 ]; then
        logFile "Error creating the CentralReport user."
        return 1
    fi

    logFile "CentralReport user successfully created!"
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
function macos_user_del {

    macos_user_verify
    RETURN_CODE="$?"
    if [ ${RETURN_CODE} -eq 0 ]; then
        logConsole "CentralReport user doesn't exist on this host!"
    else
        logFile "Deleting CentralReport user..."
        sudo dscl . -delete /Users/_centralreport
    fi

    return 0
}

#
# Verifies if the CentralReport user is already available on this host.
#
# PARAMETERS: None
# RETURN:
#   0 = CentralReport user doesn't exist
#   1 = CentralReport user already exist
#
function macos_user_verify {

    USER_UNIQUE_ID=$(dscl . -list /Users UniqueID | grep _centralreport | awk '{print $2}')
    if [ -z ${USER_UNIQUE_ID} ]; then
        return 0
    else
        return ${USER_UNIQUE_ID}
    fi
}

# --
# Related to CentralReport group
# --

#
# Deletes the CentralReport group from this host.
#
# PARAMETERS: None
# RETURN:
#   0 = Success
#
function macos_group_del {

    macos_group_verify
    RETURN_CODE="$?"
    if [ ${RETURN_CODE} -eq 0 ]; then
        logConsole "CentralReport group doesn't exist on this host!"
    else
        logFile "Deleting CentralReport group..."
        sudo dscl . -delete /Groups/_centralreport
    fi

    return 0
}

#
# Verifies if the CentralReport group is already available on this host.
#
# PARAMETERS: None
# RETURN:
#   0 = CentralReport group doesn't exist
#   1 = CentralReport group already exist
#
function macos_group_verify {

    UGID=$(dscl . -list /Groups PrimaryGroupID | grep _centralreport | awk '{print $2}')
    if [ -z ${UGID} ]; then
        return 0
    else
        return ${UGID}
    fi

}

# --
# Install/Uninstall procedures
# --

#
# Launchs the CentralReport installer for Mac OS X.
#
# PARAMETERS: None
# RETURN:
#   0 = CentralReport has been installed
#   The error code otherwise
#
function macos_install {

    # Use root privileges with sudo.
    logConsole "\n\nPlease use your administrator password to install CentralReport on this Mac."
    sudo -v
    if [ $? -ne 0 ]; then
        logError "Unable to use root privileges!"
        return 1
    fi

    printTitle "Removing any existing installation..."

    # Uninstall existing previous installation, if exist
    displayAndExec "Stopping CentralReport..." macos_stop_cr
    RETURN_CODE="$?"
    if [ ${RETURN_CODE} -ne 0 ]; then
        return ${RETURN_CODE}
    fi

    # Delete CR binary script
    displayAndExec "Removing binary file..." macos_remove_bin
    RETURN_CODE="$?"
    if [ ${RETURN_CODE} -ne 0 ]; then
        return ${RETURN_CODE}
    fi

    # Delete CR lib files
    displayAndExec "Removing CentralReport library..." macos_remove_lib
    RETURN_CODE="$?"
    if [ ${RETURN_CODE} -ne 0 ]; then
        return ${RETURN_CODE}
    fi

    # Delete startup plist file
    displayAndExec "Removing startup plist..." macos_remove_startup_plist
    RETURN_CODE="$?"
    if [ ${RETURN_CODE} -ne 0 ]; then
        return ${RETURN_CODE}
    fi

    printTitle "Installing CentralReport..."

    displayAndExec "Creating system user..." macos_user_new
    RETURN_CODE="$?"
    if [ ${RETURN_CODE} -ne 0 ]; then
        return ${RETURN_CODE}
    fi

    displayAndExec "Copying CentralReport binary file..." macos_cp_bin
    RETURN_CODE="$?"
    if [ ${RETURN_CODE} -ne 0 ]; then
        return ${RETURN_CODE}
    fi

    displayAndExec "Copying CentralReport library..." macos_cp_lib
    RETURN_CODE="$?"
    if [ ${RETURN_CODE} -ne 0 ]; then
        return ${RETURN_CODE}
    fi

    displayAndExec "Creating log directory..." macos_create_log_directory
    RETURN_CODE="$?"
    if [ ${RETURN_CODE} -ne 0 ]; then
        return ${RETURN_CODE}
    fi

    displayAndExec "Creating PID directory..." macos_create_pid_directory
    RETURN_CODE="$?"
    if [ ${RETURN_CODE} -ne 0 ]; then
        return ${RETURN_CODE}
    fi

    displayAndExec "Copying CentralReport startup plist..." macos_cp_startup_plist
    RETURN_CODE="$?"
    if [ ${RETURN_CODE} -ne 0 ]; then
        return ${RETURN_CODE}
    fi

    printTitle "Installing third-party softwares..."
    logInfo " (Please consult http://github.com/miniche/CentralReport for licenses)"

    # First, we install CherryPy...
    displayAndExec "Installing CherryPy..." sudo easy_install CherryPy
    RETURN_CODE="$?"
    if [ ${RETURN_CODE} -ne 0 ]; then
        return ${RETURN_CODE}
    fi

    # Then, installing Jinja2 Templates...
    displayAndExec "Installing Jinja 2..." sudo easy_install Jinja2
    RETURN_CODE="$?"
    if [ ${RETURN_CODE} -ne 0 ]; then
        return ${RETURN_CODE}
    fi

    # Finally, installing Routes library...
    displayAndExec "Installing Routes..." sudo easy_install routes
    RETURN_CODE="$?"
    if [ ${RETURN_CODE} -ne 0 ]; then
        return ${RETURN_CODE}
    fi

    # Cleaning screen
    clear

    # CR config assistant
#    macos_config_assistant
#
#    logConsole " "
#    logInfo " ** Starting CentralReport... ** "
#    macos_start_cr
#    RETURN_CODE="$?"
#    if [ ${RETURN_CODE} -ne 0 ]; then
#        return ${RETURN_CODE}
#    fi

    # Deleting sudo privileges for this session...
    sudo -k

    return 0
}

#
# Launchs the CentralReport uninstall for Mac OS X.
#
# PARAMETERS: None
# RETURN:
#   0 = CentralReport has been installed
#   The error code otherwise
#
function macos_uninstall {

    echo -e "\n\nPlease use your administrator password to uninstall CentralReport on this Mac."
    sudo -v
    if [ $? -ne 0 ]; then
        logError "Enable to use root privileges"
        return 1
    fi

    printTitle "Removing CentralReport files and directories..."

    # Check if CentralReport is already running, and stop it.
    displayAndExec "Stopping CentralReport..." macos_stop_cr
    RETURN_CODE="$?"
    if [ ${RETURN_CODE} -ne 0 ]; then
        return ${RETURN_CODE}
    fi

    # Delete startup plist file
    displayAndExec "Removing CentralReport startup plist..." macos_remove_startup_plist
    RETURN_CODE="$?"
    if [ ${RETURN_CODE} -ne 0 ]; then
        return ${RETURN_CODE}
    fi

    # Delete CR bin files
    displayAndExec "Removing CentralReport binary script..." macos_remove_bin
    RETURN_CODE="$?"
    if [ ${RETURN_CODE} -ne 0 ]; then
        return ${RETURN_CODE}
    fi

    # Delete CR lib files
    displayAndExec "Removing CentralReport library..." macos_remove_lib
    RETURN_CODE="$?"
    if [ ${RETURN_CODE} -ne 0 ]; then
        return ${RETURN_CODE}
    fi

    # Delete CR config file
    displayAndExec "Removing CentralReport configuration files..." macos_remove_config
    RETURN_CODE="$?"
    if [ ${RETURN_CODE} -ne 0 ]; then
        return 1
    fi

    # Delete startup log directory
    displayAndExec "Removing CentralReport log directory..." macos_remove_log_directory
    RETURN_CODE="$?"
    if [ ${RETURN_CODE} -ne 0 ]; then
        return ${RETURN_CODE}
    fi

    # Delete startup pid directory
    displayAndExec "Removing CentralReport PID directory..." macos_remove_pid_directory
    RETURN_CODE="$?"
    if [ ${RETURN_CODE} -ne 0 ]; then
        return ${RETURN_CODE}
    fi

    # Delete CentralReport user...
    displayAndExec "Removing CentralReport user..." macos_user_del
    RETURN_CODE="$?"
    if [ ${RETURN_CODE} -ne 0 ]; then
        return ${RETURN_CODE}
    fi

    # Delete CentralReport group...
    displayAndExec "Removing CentralReport group..." macos_group_del
    RETURN_CODE="$?"
    if [ ${RETURN_CODE} -ne 0 ]; then
        return ${RETURN_CODE}
    fi

    return 0
}
