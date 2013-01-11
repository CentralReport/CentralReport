#!/bin/bash

# CentralReport Unix/Linux Indev version.
# Be careful! Don't use in production environment!

# This file contain all functions to manage CR install/unistall on a Mac.



# --
# CentralReport daemon functions
# --

function macos_start_cr {

    writeLog "Starting CentralReport..."

    if [ -f ${PID_FILE} ]; then
        writeInfo "CentralReport is already running!"
        return 0

    else
        sudo python ${INSTALL_DIR}/centralreport.py start
        RETURN_CODE="$?"

        if [ ${RETURN_CODE} -ne "0" ]; then
            writeError "Error when starting CentralReport (Error code : ${RETURN_CODE})"
            return ${RETURN_CODE}
        else
            # Waiting three seconds before all CR threads really started.
            sleep 3

            writeInfo "CentralReport started"
            return 0
        fi
    fi


}

function macos_stop_cr {

    writeLog "Stopping CentralReport..."

    if [ ! -f ${PID_FILE} ]; then
        writeInfo "CentralReport is already stopped!"
        return 0
    else
        sudo python ${INSTALL_DIR}/centralreport.py stop
        RETURN_CODE="$?"

        if [ ${RETURN_CODE} -ne "0" ] && [ ${RETURN_CODE} -ne "143" ]; then
            writeError "Error when stopping CentralReport (Error code : ${RETURN_CODE})"
            return ${RETURN_CODE}

        else
            writeInfo "CentralReport stopped"
            return 0
        fi
    fi
}



# --
# CentralReport config assistant
# --
function macos_config_assistant {

    writeConsole "\033[1;32m"
    writeInfo "Lauching CentralReport configuration wizard..."
    writeConsole "\033[0m"

    sudo python ${CONFIG_ASSISTANT} < /dev/tty

    return 0

}




# --
# Uninstall functions
# --

function macos_remove_bin {

    writeLog "Removing CentralReport bin files..."

    if [ -d ${INSTALL_DIR} ]; then
        displayAndExec "Remove existing install directory..." sudo rm -rfv ${INSTALL_DIR}
        RETURN_CODE="$?"

        if [ ${RETURN_CODE} -ne "0" ]; then
            writeError "Error on deleting CentralReport bin directory at ${INSTALL_DIR} (Error code : ${RETURN_CODE})"
            return ${RETURN_CODE}
        else
            writeLog "CentralReport bin files removed"
            return 0
        fi
    else
        writeInfo "CentralReport bin directory doesn't exist!"
        return 0
    fi
}

function macos_remove_config {

    writeLog "Removing CentralReport config file..."

    if [ -f ${CONFIG_FILE} ]; then
        displayAndExec "Remove existing config file..." sudo rm -fv ${CONFIG_FILE}
        RETURN_CODE="$?"

        if [ ${RETURN_CODE} -ne "0" ]; then
            writeError "Error on deleting CentralReport config file at ${CONFIG_FILE} (Error code : ${RETURN_CODE})"
            return ${RETURN_CODE}
        else
            writeLog "CentralReport config file removed"
            return 0
        fi
    else
        writeInfo "CentralReport config file not found!"
        return 0
    fi
}

function macos_remove_startup_plist {

    writeLog "Removing startup plist..."

    if [ -f ${STARTUP_PLIST} ]; then
        displayAndExec "Remove existing startup plist file..." sudo rm -fv ${STARTUP_PLIST}
        RETURN_CODE="$?"

        if [ $? -ne "0" ]; then
            writeError "Error on deleting startup plist file at ${STARTUP_PLIST} (Error code : ${RETURN_CODE})"
            return ${RETURN_CODE}
        else
            writeLog "Startup plist removed"
            return 0
        fi
    else
        writeInfo "Startup plist file not found!"
        return 0
    fi
}






# --
# Install functions
# --

function macos_cp_bin {
    # Copy CentralReport files in the right directory.

    # It's possible that /usr/local and /usr/local/bin doesn't exist. We will creating them in this case.
    if [ ! -d "/usr/local" ]; then
        sudo mkdir /usr/local
    fi
    if [ ! -d "/usr/local/bin" ]; then
        sudo mkdir /usr/local/bin
    fi

    sudo mkdir ${INSTALL_DIR}
    RETURN_CODE="$?"

    if [ ${RETURN_CODE} -ne "0" ]; then
          displayError "Error on creating CentralReport dir at ${INSTALL_DIR} (Error code : ${RETURN_CODE})"
          return ${RETURN_CODE}
    else
        displayAndExec "Copying CentralReport in the good directory..." sudo cp -R -f -v centralreport ${PARENT_DIR}
        RETURN_CODE="$?"

        if [ ${RETURN_CODE} -ne "0" ]; then
            displayError "Error on copying CentralReport bin files in ${PARENT_DIR} (Error code : ${RETURN_CODE})"
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
      displayError "Error on copying startup plist at ${STARTUP_PLIST} (Error code : ${RETURN_CODE})"
      return ${RETURN_CODE}
    else
        return 0
    fi
}








# --
# Install procedure
# --

function macos_install {

    # Use root privileges with sudo.
    writeConsole "\n\nPlease use your administrator password to install CentralReport on this Mac."
    sudo -v
    if [ $? -ne 0 ]; then
        writeError "Impossible to use root privileges!"
        return 1
    fi

    writeTitle "Removing any existing installation..."

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



    writeTitle "Installing CentralReport..."

    macos_cp_bin
    RETURN_CODE="$?"
    if [ ${RETURN_CODE} -ne 0 ]; then
        return ${RETURN_CODE}
    fi

    macos_cp_startup_plist
    RETURN_CODE="$?"
    if [ ${RETURN_CODE} -ne 0 ]; then
        return ${RETURN_CODE}
    fi




    writeTitle "Installing third-party softwares..."
    writeInfo " (Please consult http://github.com/miniche/CentralReport for licenses)"

    # First, we install CherryPy...
    displayAndExec "CherryPy" sudo easy_install CherryPy
    RETURN_CODE="$?"
    if [ ${RETURN_CODE} -ne 0 ]; then
        return ${RETURN_CODE}
    fi


    # Then, installing Jinja2 Templates...
    displayAndExec "Jinja" sudo easy_install Jinja2
    RETURN_CODE="$?"
    if [ ${RETURN_CODE} -ne 0 ]; then
        return ${RETURN_CODE}
    fi


    # Finally, installing Routes library...
    displayAndExec "Routes" sudo easy_install routes
    RETURN_CODE="$?"
    if [ ${RETURN_CODE} -ne 0 ]; then
        return ${RETURN_CODE}
    fi


    # Cleaning screen
    clear

    # CR config assistant
    macos_config_assistant

    writeConsole " "
    writeInfo " ** Starting CentralReport... ** "
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
        displayError "Impossible to use root privileges"
        return 1
    fi

    displayTitle "Removing CentralReport files and directories..."

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
