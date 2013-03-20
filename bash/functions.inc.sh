#!/bin/sh

# ------------------------------------------------------------
# CentralReport Unix/Linux - install/uninstall functions
# Alpha version. Don't use in production environment!
# ------------------------------------------------------------
# https://github.com/miniche/CentralReport/
# ------------------------------------------------------------

# --
# Start / Stop the CentralReport daemon
# --


function start_cr(){

    if [ -f /usr/local/bin/centralreport ]; then
        if [ "${CURRENT_OS}" == $"{OS_MAC}" ]; then
            execute_privileged_command launchctl load -w ${STARTUP_PLIST}
        else
            execute_privileged_command /usr/local/bin/centralreport start
        fi

        RETURN_CODE="$?"
        if [ ${RETURN_CODE} -ne "0" ]; then
            logError "Error starting CentralReport (Error code: ${RETURN_CODE})!"
            return ${RETURN_CODE}
        fi
    fi

    return 0
}

function stop_cr(){

    if [ -f /usr/local/bin/centralreport ]; then
        execute_privileged_command /usr/local/bin/centralreport stop
        RETURN_CODE="$?"

        if [ ${RETURN_CODE} -ne "0" ] && [ ${RETURN_CODE} -ne "143" ]; then
            logError "Error stopping CentralReport (Error code: ${RETURN_CODE})!"
            return ${RETURN_CODE}
        fi
    fi

    return 0
}

function launch_config_assistant(){

    logFile "Launching the CentralReport configuration wizard..."
    printBox blue "Launching the CentralReport configuration wizard..."

    execute_privileged_command python ${CONFIG_ASSISTANT} < /dev/tty

    return 0
}


# --
# Functions related to installation
# --

function copy_bin(){

    # In some cases, /usr/local and /usr/local/bin don't exist. We will create them in this case.
    if [ ! -d "/usr/local" ]; then
         execute_privileged_command mkdir /usr/local
    fi
    if [ ! -d "/usr/local/bin" ]; then
         execute_privileged_command mkdir /usr/local/bin
    fi

    execute_privileged_command cp -f utils/bin/centralreport ${CR_BIN_FILE}
    RETURN_CODE="$?"

    if [ ${RETURN_CODE} -ne "0" ]; then
        logError "Error copying the CentralReport binary script in ${CR_BIN_FILE} (Error code: ${RETURN_CODE})"
        return ${RETURN_CODE}

    else
        execute_privileged_command chmod +x ${CR_BIN_FILE}
        RETURN_CODE="$?"

        if [ ${RETURN_CODE} -ne "0" ]; then
            logError "Error applying chmod on ${CR_BIN_FILE} (Error code: ${RETURN_CODE})"
            return ${RETURN_CODE}
        fi
    fi

    return 0
}

function copy_lib(){

    # In some cases, /usr/local and /usr/local/bin don't exist. We will create them in this case.
    if [ ! -d "/usr/local" ]; then
         execute_privileged_command mkdir /usr/local
    fi
    if [ ! -d "/usr/local/lib" ]; then
         execute_privileged_command mkdir /usr/local/lib
    fi

    execute_privileged_command mkdir ${CR_LIB_DIR}
    RETURN_CODE="$?"

    if [ ${RETURN_CODE} -ne "0" ]; then
          logError "Error creating the CentralReport library directory at ${CR_LIB_DIR} (Error code: ${RETURN_CODE})"
          return ${RETURN_CODE}
    fi

    execute_privileged_command cp -R -f centralreport ${CR_LIB_DIR_RELATIVE}
    RETURN_CODE="$?"

    if [ ${RETURN_CODE} -ne "0" ]; then
        logError "Error copying the CentralReport libraries in ${CR_LIB_DIR} (Error code: ${RETURN_CODE})"
        return ${RETURN_CODE}
    fi

    execute_privileged_command chmod +x ${CR_LIB_DAEMON}
    RETURN_CODE="$?"

    if [ ${RETURN_CODE} -ne "0" ]; then
        logError "Error applying chmod on ${CR_LIB_DAEMON} (Error code: ${RETURN_CODE})"
        return ${RETURN_CODE}
    fi

    return 0
}

function copy_init_file(){

    if [ "${CURRENT_OS}" == "${OS_MAC}" ]; then
        # More details about the plist here:
        # https://developer.apple.com/library/mac/#documentation/darwin/reference/manpages/man5/launchd.plist.5.html

        sudo cp -f ${STARTUP_PLIST_INSTALL} ${STARTUP_PLIST}
        RETURN_CODE="$?"

        if [ ${RETURN_CODE} -ne "0" ]; then
            logError "Error copying the startup plist at ${STARTUP_PLIST} (Error code: ${RETURN_CODE})"
            return ${RETURN_CODE}
        fi

    else
        cp -f -v ${STARTUP_DEBIAN_INSTALL} ${STARTUP_DEBIAN}
        RETURN_CODE="$?"

        if [ ${RETURN_CODE} -ne "0" ]; then
            logError "Error copying the startup script at ${STARTUP_PLIST} (Error code: ${RETURN_CODE})"
            return ${RETURN_CODE}
        else
            chmod 755 ${STARTUP_DEBIAN}

            update-rc.d centralreport defaults
            RETURN_CODE="$?"

            if [ ${RETURN_CODE} -ne "0" ]; then
                logError "Error registering the startup script with update-rc.d (Error code: ${RETURN_CODE})"
                return ${RETURN_CODE}
            else
                return 0
            fi
        fi
    fi

    return 0
}

function create_config_directory(){

    if [ -d ${CR_CONFIG_DIR} ]; then
        logFile "The config directory already exist!"
    else
        execute_privileged_command mkdir ${CR_CONFIG_DIR}
        RETURN_CODE="$?"

        if [ ${RETURN_CODE} -ne "0" ]; then
            logError "Error creating the config directory at ${CR_CONFIG_DIR} (Error code: ${RETURN_CODE})"
            return ${RETURN_CODE}
        fi
    fi

    if [ "${CURRENT_OS}" == "${OS_MAC}" ]; then
        CR_USER="${CR_USER_MAC}"
        CR_GROUP="${CR_GROUR_MAC}"
    else
        CR_USER="${CR_USER_DEBIAN}"
        CR_GROUP="${CR_GROUP_DEBIAN}"
    fi

    execute_privileged_command chown -R ${CR_USER}:${CR_GROUP} ${CR_CONFIG_DIR}
    RETURN_CODE="$?"

    if [ ${RETURN_CODE} -ne "0" ]; then
        logError "Error updating the owner of ${CR_CONFIG_DIR} (Error code: ${RETURN_CODE})"
        return ${RETURN_CODE}
    fi

    return 0
}

function create_log_directory(){
    if [ -d ${CR_LOG_DIR} ]; then
        logFile "The log directory already exist!"
    else
        execute_privileged_command mkdir ${CR_LOG_DIR}
        RETURN_CODE="$?"

        if [ ${RETURN_CODE} -ne "0" ]; then
            logError "Error creating the log directory at ${CR_LOG_DIR} (Error code: ${RETURN_CODE})"
            return ${RETURN_CODE}
        fi
    fi

    if [ "${CURRENT_OS}" == "${OS_MAC}" ]; then
        CR_USER="${CR_USER_MAC}"
        CR_GROUP="${CR_GROUR_MAC}"
    else
        CR_USER="${CR_USER_DEBIAN}"
        CR_GROUP="${CR_GROUP_DEBIAN}"
    fi

    execute_privileged_command chown -R ${CR_USER}:${CR_GROUP} ${CR_LOG_DIR}
    RETURN_CODE="$?"

    if [ ${RETURN_CODE} -ne "0" ]; then
        logError "Error updating owner of ${CR_LOG_DIR} (Error code: ${RETURN_CODE})"
        return ${RETURN_CODE}
    fi

    return 0
}

# --
# Unistall functions
# --

function delete_bin(){
    logFile "Removing the CentralReport binary script..."

    if [ -f ${CR_BIN_FILE} ]; then
        execute_privileged_command rm -f ${CR_BIN_FILE}
        RETURN_CODE="$?"

        if [ ${RETURN_CODE} -ne "0" ]; then
            logError "Error deleting the CentralReport binary script at ${CR_BIN_FILE} (Error code: ${RETURN_CODE})"
            return ${RETURN_CODE}
        else
            logFile "CentralReport binary script have been removed"
        fi
    else
        logInfo "CentralReport binary script doesn't exist!"
    fi

    return 0
}

function delete_lib(){
    logFile "Removing CentralReport libraries..."

    if [ -d ${CR_LIB_DIR} ]; then
        execute_privileged_command rm -rf ${CR_LIB_DIR}
        RETURN_CODE="$?"

        if [ ${RETURN_CODE} -ne "0" ]; then
            logError "Error deleting the CentralReport libraries directory at ${CR_LIB_DIR} (Error code: ${RETURN_CODE})"
            return ${RETURN_CODE}
        else
            logFile "CentralReport lib files removed"
        fi
    else
        logInfo "CentralReport lib directory doesn't exist!"
    fi

    return 0
}

function delete_init_file(){

    if [ "${CURRENT_OS}" == "${OS_MAC}" ]; then
        logFile "Removing the startup plist..."

        if [ -f ${STARTUP_PLIST} ]; then
            execute_privileged_command rm -f ${STARTUP_PLIST}
            RETURN_CODE="$?"

            if [ ${RETURN_CODE} -ne "0" ]; then
                logError "Error deleting the startup plist file at ${STARTUP_PLIST} (Error code: ${RETURN_CODE})"
                return ${RETURN_CODE}
            else
                logFile "Startup plist removed"
            fi
        else
            logInfo "Startup plist file not found!"
        fi

    else
        logFile "Removing the startup script..."

        if [ -f ${STARTUP_DEBIAN} ]; then
            rm -rf ${STARTUP_DEBIAN}
            RETURN_CODE="$?"

            if [ ${RETURN_CODE} -ne "0" ]; then
                logError "Error deleting the startup script at ${STARTUP_DEBIAN} (Error code: ${RETURN_CODE})"
                return ${RETURN_CODE}
            else

                update-rc.d -f centralreport remove
                RETURN_CODE="$?"

                if [ ${RETURN_CODE} -ne "0" ]; then
                    logError "Error removing the startup script with update-rc.d (Error code: ${RETURN_CODE})"
                    return ${RETURN_CODE}
                else
                    logFile "Startup script deleted"
                fi
            fi
        else
            logInfo "Startup plist file not found!"
        fi
    fi

    return 0
}

function delete_config_directory(){
    logFile "Removing the CentralReport config dir..."

    if [ -d ${CR_CONFIG_DIR} ]; then
        execute_privileged_command rm -rf ${CR_CONFIG_DIR}
        RETURN_CODE="$?"

        if [ ${RETURN_CODE} -ne "0" ]; then
            logError "Error deleting the CentralReport config dir at ${CR_CONFIG_DIR} (Error code: ${RETURN_CODE})"
            return ${RETURN_CODE}
        else
            logFile "CentralReport config dir deleted"
        fi
    else
        logInfo "CentralReport config dir not found!"
    fi

    return 0
}

function delete_log_directory(){
    logFile "Removing the log directory..."

    if [ -d ${CR_LOG_DIR} ]; then
        execute_privileged_command rm -R -f ${CR_LOG_DIR}
        RETURN_CODE="$?"

        if [ $? -ne "0" ]; then
            logError "Error deleting the log directory at ${CR_LOG_DIR} (Error code: ${RETURN_CODE})"
            return ${RETURN_CODE}
        else
            logFile "Log directory deleted"
        fi
    else
        logInfo "Log directory already deleted!"
    fi

    return 0
}

function delete_pid_directory(){
    logFile "Removing the PID directory..."

    if [ -d ${CR_PID_DIR} ]; then
        execute_privileged_command rm -R -f ${CR_PID_DIR}
        RETURN_CODE="$?"

        if [ $? -ne "0" ]; then
            logError "Error deleting the pid directory at ${CR_PID_DIR} (Error code: ${RETURN_CODE})"
            return ${RETURN_CODE}
        else
            logFile "PID directory deleted"
        fi
    else
        logInfo "PID directory already deleted!"
    fi

    return 0
}

# --
# CentralReport User functions
# --

function create_cr_user(){

    RETURN_CODE=$(verify_cr_user)
    if [ ${RETURN_CODE} -ne 0 ]; then
        logFile "CentralReport user already exists. Skipping this step."
    else

        if [ "${CURRENT_OS}" == "${OS_MAC}" ]; then
            # Mac OS includes on each client an OpenDirectory server.
            # So, it's a better more complex to add a simple user than on Linux.

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


            local GROUP_UNIQUE_ID=$(verify_cr_user)
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
                cr_check_user=$(dscl . -list /Users UniqueID \
                                | awk '{print $2, "\t", $1}' \
                                | sort -ug | grep -c "${fnumber}")

                if [ ${cr_check_user} -gt 0 ]; then
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
                logError "Unable to find an available UniqueID for the CentralReport user."
                return 1
            elif [ ${user_id} -le 100 ]; then
                logError "Unable to find an available UniqueID, greater than 100, for the CentralReport user."
                return 1
            fi

            # Now, we must check in the UID is really available.
            if dscl . -readall /Users | grep -q "UniqueID: *${user_id}$" ; then
                logError "UID ${user_id} is already in use"
                return 1
            fi

            # Checks if CentralReport group already exists.
            GROUP_UNIQUE_ID=$(verify_cr_group)
            if [ ${GROUP_UNIQUE_ID} -ne 0 ]; then
                logFile "CentralReport group already exists. Skipping this step."
            else
                logFile "CentralReport group doesn't exist"

                # So, the same UGID as UID is available?
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
                        cr_check_group=$(dscl . -list /Users UniqueID \
                                        | awk '{print $2, "\t", $1}' \
                                        | sort -ug \
                                        | grep -c "${fnumber}")

                        if [ ${cr_check_group} -gt 0 ] ; then
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
                        logError "Unable to find an available PrimaryGroupID for the CentralReport group."
                        return 1
                    elif [ ${user_id} -le 100 ]; then
                        logError "Unable to find an available PrimaryGroupID for the CentralReport group greater than 100."
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

                # We can add our group now!
                logFile "Creating the CentralReport group..."
                sudo dscl . create /Groups/_centralreport
                sudo dscl . create /Groups/_centralreport PrimaryGroupID ${GROUP_UNIQUE_ID}

                # Checking if the group have been created
                RETURN_CODE=$(verify_cr_group)
                logFile "GroupID: ${GROUP_UNIQUE_ID}"
                if [ "${RETURN_CODE}" -eq 0 ]; then
                    logFile "Error creating the CentralReport group."
                    return 1
                fi

                logFile "Group successfully created!"
            fi

            logFile "Creating CentralReport user..."

            # Now, we can create our user. The victory is close!
            sudo dscl . -create /Users/_centralreport
            sudo dscl . -create /Users/_centralreport UserShell /bin/bash
            sudo dscl . -create /Users/_centralreport RealName "CentralReport daemon"
            sudo dscl . -create /Users/_centralreport UniqueID ${user_id}
            sudo dscl . -create /Users/_centralreport PrimaryGroupID ${GROUP_UNIQUE_ID}
            sudo dscl . -create /Users/_centralreport NFSHomeDirectory /usr/local/lib/centralreport

            # Hiding the user
            # http://superuser.com/questions/70156/hide-users-from-mac-os-x-snow-leopard-logon-screen
            sudo dscl . -delete /Users/_centralreport AuthenticationAuthority
            sudo dscl . -create /Users/_centralreport Password "*"

            # Registring the _centralreport user in the _centralreport group
            sudo dscl . -append /Groups/_centralreport GroupMembership _centralreport

            # Checking that the user has been created
            USER_UNIQUE_ID=$(verify_cr_user)
            if [ "${USER_UNIQUE_ID}" -eq 0 ]; then
                logFile "Error creating the CentralReport user."
                return 1
            fi

        else
            useradd --system \
                    --home /usr/local/lib/centralreport/ \
                    --shell /bin/bash \
                    --user-group \
                    --comment "CentralReport Daemon" \
                    centralreport

            RETURN_CODE="$?"

            if [ ${RETURN_CODE} -ne 0 ]; then
                logConsole " "
                logError "Error creating the CentralReport user (Error code: ${RETURN_CODE})"
                return ${RETURN_CODE}
            fi
        fi
    fi

    return 0
}

function remove_cr_user(){

    local USER_ID=$(verify_cr_user)
    if [ "${USER_ID}" -eq 0 ]; then
        logConsole "CentralReport user already deleted. Skipping this step."
    else
        if [ "${CURRENT_OS}" == "${OS_MAC}" ]; then
            logFile "Deleting CentralReport user..."
            sudo dscl . -delete /Users/_centralreport
        else
            userdel centralreport
            RETURN_CODE="$?"

            if [ ${RETURN_CODE} -ne 0 ]; then
                logConsole " "
                logError "Error deleting the CentralReport user (Error code: ${RETURN_CODE})"
                return ${RETURN_CODE}
            fi
        fi
    fi

    return 0
}

function remove_cr_group(){

    if [ "${CURRENT_OS}" == "${OS_MAC}" ]; then
        local GROUP_ID=$(verify_cr_group)
        if [ "${GROUP_ID}" -eq 0 ]; then
            logConsole "CentralReport group doesn't exist on this host!"
        else
            logFile "Deleting the CentralReport group..."
            sudo dscl . -delete /Groups/_centralreport
        fi
    fi

    return 0
}

function verify_cr_user(){

    if [ "${CURRENT_OS}" == "${OS_MAC}" ]; then
        USER_UNIQUE_ID=$(dscl . -list /Users UniqueID | grep _centralreport | awk '{print $2}')
        if [ -z "${USER_UNIQUE_ID}" ]; then
            echo "0"
        else
            echo "${USER_UNIQUE_ID}"
        fi

    else
        CR_USER_FOUND=$(cat /etc/passwd | grep 'centralreport')
        if [ -z "${CR_USER_FOUND}" ]; then
            echo "0"
        else
            echo "1"
        fi
    fi
}

function verify_cr_group(){

    if [ "${CURRENT_OS}" == "${OS_MAC}" ]; then
        UGID=$(dscl . -list /Groups PrimaryGroupID | grep _centralreport | awk '{print $2}')
        if [ ! -z "${UGID}" ]; then
            echo "${UGID}"
        fi
    fi

    echo 0
}

# --
# Global functions
# --

function install_cr(){

    # Deleting previous version...
    detect_010_version
    if [ "$?" -ne 0 ]; then
        delete_010_version
    fi

    printTitle "Removing any existing installation..."

    # Uninstall existing previous installation, if exist
    displayAndExec "Stopping CentralReport..." stop_cr
    RETURN_CODE="$?"
    if [ ${RETURN_CODE} -ne 0 ]; then
        return ${RETURN_CODE}
    fi

    # Delete CR binary script
    displayAndExec "Removing the binary file..." delete_bin
    RETURN_CODE="$?"
    if [ ${RETURN_CODE} -ne 0 ]; then
        return ${RETURN_CODE}
    fi

    # Delete CR lib files
    displayAndExec "Removing CentralReport libraries..." delete_lib
    RETURN_CODE="$?"
    if [ ${RETURN_CODE} -ne 0 ]; then
        return ${RETURN_CODE}
    fi

    # Delete startup plist file
    displayAndExec "Removing the init script..." delete_init_file
    RETURN_CODE="$?"
    if [ ${RETURN_CODE} -ne 0 ]; then
        return ${RETURN_CODE}
    fi

    printTitle "Installing CentralReport..."

    displayAndExec "Creating the system user..." create_cr_user
    RETURN_CODE="$?"
    if [ ${RETURN_CODE} -ne 0 ]; then
        return ${RETURN_CODE}
    fi

    displayAndExec "Copying the CentralReport binary file..." copy_bin
    RETURN_CODE="$?"
    if [ ${RETURN_CODE} -ne 0 ]; then
        return ${RETURN_CODE}
    fi

    displayAndExec "Copying CentralReport libaries..." copy_lib
    RETURN_CODE="$?"
    if [ ${RETURN_CODE} -ne 0 ]; then
        return ${RETURN_CODE}
    fi

    displayAndExec "Creating the CentralReport configuration directory..." create_config_directory
    RETURN_CODE="$?"
    if [ ${RETURN_CODE} -ne 0 ]; then
        return ${RETURN_CODE}
    fi

    displayAndExec "Creating the CentralReport log directory..." create_log_directory
    RETURN_CODE="$?"
    if [ ${RETURN_CODE} -ne 0 ]; then
        return ${RETURN_CODE}
    fi

    displayAndExec "Copying CentralReport init file..." copy_init_file
    RETURN_CODE="$?"
    if [ ${RETURN_CODE} -ne 0 ]; then
        return ${RETURN_CODE}
    fi

    # Cleaning screen
    clear

    # CR config assistant
    # TODO: Refactor config assistant

    printTitle "First launch of CentralReport..."
    start_cr
    RETURN_CODE="$?"
    if [ ${RETURN_CODE} -ne 0 ]; then
        return ${RETURN_CODE}
    fi
}

function uninstall_cr(){

    # Deleting previous version...
    detect_010_version
    if [ "$?" -ne 0 ]; then
        delete_010_version
    fi

    printTitle "Removing CentralReport files and directories..."

    # Check if CentralReport is already running, and stop it.
    displayAndExec "Stopping CentralReport..." stop_cr
    RETURN_CODE="$?"
    if [ ${RETURN_CODE} -ne 0 ]; then
        return ${RETURN_CODE}
    fi

    # Delete startup plist file
    displayAndExec "Removing the startup plist..." delete_init_file
    RETURN_CODE="$?"
    if [ ${RETURN_CODE} -ne 0 ]; then
        return ${RETURN_CODE}
    fi

    # Delete CR bin files
    displayAndExec "Removing the binary script..." delete_bin
    RETURN_CODE="$?"
    if [ ${RETURN_CODE} -ne 0 ]; then
        return ${RETURN_CODE}
    fi

    # Delete CR lib files
    displayAndExec "Removing CentralReport libraries..." delete_lib
    RETURN_CODE="$?"
    if [ ${RETURN_CODE} -ne 0 ]; then
        return ${RETURN_CODE}
    fi

    # Delete CR config file
    displayAndExec "Removing the CentralReport configuration directory..." delete_config_directory
    RETURN_CODE="$?"
    if [ ${RETURN_CODE} -ne 0 ]; then
        return 1
    fi

    # Delete startup log directory
    displayAndExec "Removing the CentralReport log directory..." delete_log_directory
    RETURN_CODE="$?"
    if [ ${RETURN_CODE} -ne 0 ]; then
        return ${RETURN_CODE}
    fi

    # Delete startup pid directory
    displayAndExec "Removing the CentralReport PID directory..." delete_pid_directory
    RETURN_CODE="$?"
    if [ ${RETURN_CODE} -ne 0 ]; then
        return ${RETURN_CODE}
    fi

    # Delete CentralReport user...
    displayAndExec "Removing the CentralReport user..." remove_cr_user
    RETURN_CODE="$?"
    if [ ${RETURN_CODE} -ne 0 ]; then
        return ${RETURN_CODE}
    fi

    # Delete CentralReport group...
    displayAndExec "Removing the CentralReport group..." remove_cr_group
    RETURN_CODE="$?"
    if [ ${RETURN_CODE} -ne 0 ]; then
        return ${RETURN_CODE}
    fi
}
