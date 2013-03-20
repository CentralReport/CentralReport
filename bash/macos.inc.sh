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
function macos_start_cr {

    logFile "Starting CentralReport..."

    if [ -f ${PID_FILE} ]; then
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

function macos_stop_cr {

    logFile "Stopping CentralReport..."

    if [ ! -f ${PID_FILE} ]; then
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
function macos_config_assistant {

    logFile "Launching CentralReport configuration wizard..."

    printBox blue "Launching CentralReport configuration wizard..."

    sudo python ${CONFIG_ASSISTANT} < /dev/tty

    return 0
}




# --
# Uninstall functions
# --

function macos_remove_bin {

    logFile "Removing CentralReport binary script..."

    if [ -d ${CR_BIN_FILE} ]; then
        displayAndExec "Removing existing binary script..." sudo rm -f ${CR_BIN_FILE}
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

function macos_remove_lib {

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

function macos_remove_config {

    logFile "Removing CentralReport config file..."

    if [ -f ${CONFIG_FILE} ]; then
        displayAndExec "Removing existing config file..." sudo rm -f ${CONFIG_FILE}
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

function macos_remove_startup_plist {

    logFile "Removing startup plist..."

    if [ -f ${STARTUP_PLIST} ]; then
        displayAndExec "Removing existing startup plist file..." sudo rm -f ${STARTUP_PLIST}
        RETURN_CODE="$?"

        if [ $? -ne "0" ]; then
            logError "Error deleting startup plist file at ${STARTUP_PLIST} (Error code: ${RETURN_CODE})"
            return ${RETURN_CODE}
        else
            logFile "Startup plist removed"
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

function macos_cp_bin {
    # Copy CentralReport binary script in the right directory.
    # In some cases, /usr/local and /usr/local/bin doesn't exist. We will creating them in this case.
    if [ ! -d "/usr/local" ]; then
        sudo mkdir /usr/local
    fi
    if [ ! -d "/usr/local/bin" ]; then
        sudo mkdir /usr/local/bin
    fi


    displayAndExec "Copying CentralReport binary script in the good directory..." sudo cp -f utils/bin/centralreport ${CR_BIN_FILE}
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

function macos_cp_lib {
    # Copy CentralReport libraries in the right directory.
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
        displayAndExec "Copying CentralReport libraries in the good directory..." sudo cp -R -f centralreport ${CR_LIB_DIR}
        RETURN_CODE="$?"

        if [ ${RETURN_CODE} -ne "0" ]; then
            logError "Error copying CentralReport libraries in ${CR_LIB_DIR} (Error code: ${RETURN_CODE})"
            return ${RETURN_CODE}
        else
            return 0
        fi
    fi

}


function macos_cp_startup_plist {
    # Copy startup plist for launchd in the right directory.

    displayAndExec "Copying startup plist in the good directory..." sudo cp -f -v ${STARTUP_PLIST_INSTALL} ${STARTUP_PLIST}
    RETURN_CODE="$?"

    if [ ${RETURN_CODE} -ne "0" ]; then
      logError "Error copying startup plist at ${STARTUP_PLIST} (Error code: ${RETURN_CODE})"
      return ${RETURN_CODE}
    else
        return 0
    fi
}

# --
# Related to CentralReport user
# --

function macos_user_new {
    # Adds the CentralReport user for security purposes
    # PS: This function will also create a dedicated group.

    # Next: _centralreport user already exits?
    # Next:     -> if not: find a UniqueID available in 0-499 (otherwise, exit)
    # Next:         -> Be sure that the UniqueID found is really unique (otherwise, exit)
    # Next:         -> _centralreport group already exists?
    # Next:             -> if not, UniqueID is available in groups?
    # Next:                -> if not, find a PrimaryGroupID available in 0-499
    # Next:                -> Be sure the PrimaryGroupID found is really unique
    # Next:             -> Create a new group with UGID or UID
    # Next:             -> Be sure that the group is created
    # Next:     -> Create a new user with UID
    # Next:     -> Be sure that the user is created


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


function macos_user_del {
    # Deletes the CentralReport user

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


function macos_user_verify {
    # Checks if the CentralReport user already exist, or not
    # Returns 0 if the CR user doesn't exist. Returns the UniqueID otherwise.

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

function macos_group_new {
    # Adds the CentralReport user for security purposes

    RETURN_CODE="$?"
    sudo dscl . -create /Groups/_centralreport
    sudo dscl . -create /Groups/_centralreport PrimaryGroupID 1000
    if [ ${RETURN_CODE} -ne 0 ]; then
        logConsole " "
        logError "Error creating the CentralReport user (Error code: ${RETURN_CODE}"
        return 1
    fi

    return 0
}


function macos_group_del {
    # Deletes the CentralReport group

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


function macos_group_verify {
    # Checks if the CentralReport group already exist, or not
    # Returns 0 if the CR group doesn't exist. Returns the PrimaryGroupID otherwise.

    UGID=$(dscl . -list /Groups PrimaryGroupID | grep _centralreport | awk '{print $2}')
    if [ -z ${UGID} ]; then
        return 0
    else
        return ${UGID}
    fi

}

# --
# Install procedure
# --

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
    macos_stop_cr
    RETURN_CODE="$?"
    if [ ${RETURN_CODE} -ne 0 ]; then
        return ${RETURN_CODE}
    fi

    # Delete CR bin files
    macos_remove_bin
    RETURN_CODE="$?"
    if [ ${RETURN_CODE} -ne 0 ]; then
        return ${RETURN_CODE}
    fi

    # Delete startup plist file
    macos_remove_startup_plist
    RETURN_CODE="$?"
    if [ ${RETURN_CODE} -ne 0 ]; then
        return ${RETURN_CODE}
    fi

    printTitle "Installing CentralReport..."

    macos_user_new
    RETURN_CODE="$?"
    if [ ${RETURN_CODE} -ne 0 ]; then
        return ${RETURN_CODE}
    fi

    macos_cp_bin
    RETURN_CODE="$?"
    if [ ${RETURN_CODE} -ne 0 ]; then
        return ${RETURN_CODE}
    fi

    macos_cp_lib
    RETURN_CODE="$?"
    if [ ${RETURN_CODE} -ne 0 ]; then
        return ${RETURN_CODE}
    fi

    macos_cp_startup_plist
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
    macos_config_assistant

    logConsole " "
    logInfo " ** Starting CentralReport... ** "
    macos_start_cr
    RETURN_CODE="$?"
    if [ ${RETURN_CODE} -ne 0 ]; then
        return ${RETURN_CODE}
    fi

    # Deleting sudo privileges for this session...
    sudo -k

    return 0
}

# --
# Uninstall procedure
# --

function macos_uninstall {

    echo -e "\n\nPlease use your administrator password to uninstall CentralReport on this Mac."
    sudo -v
    if [ $? -ne 0 ]; then
        logError "Enable to use root privileges"
        return 1
    fi

    printTitle "Removing CentralReport files and directories..."

    # Check if CentralReport is already running, and stop it.
    macos_stop_cr
    RETURN_CODE="$?"
    if [ ${RETURN_CODE} -ne 0 ]; then
        return ${RETURN_CODE}
    fi

    # Delete CR bin files
    macos_remove_bin
    RETURN_CODE="$?"
    if [ ${RETURN_CODE} -ne 0 ]; then
        return ${RETURN_CODE}
    fi

    # Delete CR config file
    macos_remove_config
    RETURN_CODE="$?"
    if [ ${RETURN_CODE} -ne 0 ]; then
        return 1
    fi

    # Delete startup plist file
    macos_remove_startup_plist
    RETURN_CODE="$?"
    if [ ${RETURN_CODE} -ne 0 ]; then
        return ${RETURN_CODE}
    fi

    return 0
}
