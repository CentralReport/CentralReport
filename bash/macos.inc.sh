#!/bin/bash

# CentralReport Unix/Linux Indev version.
# By careful! Don't use in production environment!

# This file contain all functions to manage CR install/unistall on a Mac.



# --
# CentralReport daemon functions
# --

function macos_start_cr {

    echo -e "\nStarting CentralReport..."

    if [ -f ${PID_FILE} ]; then
        echo "CentralReport is already running!"
        return 0

    else
        sudo python ${INSTALL_DIR}/centralreport.py start

        if [ $? -ne "0" ]; then
            displayError "Error on starting CentralReport (Error code : $?)"
            return 1
        else
            # Waiting three seconds before all CR threads really started.
            sleep 3

            echo "CentralReport started"
            return 0
        fi
    fi


}

function macos_stop_cr {

    echo -e "\nStopping CentralReport..."

    if [ ! -f ${PID_FILE} ]; then
        echo "CentralReport is already stopped!"
        return 0
    else
        sudo python ${INSTALL_DIR}/centralreport.py stop
        RETURN_CODE="$?"
        
        if [ ${RETURN_CODE} -ne "0" ] && [ ${RETURN_CODE} -ne "143" ]; then
            displayError "Error on stopping CentralReport (Error code : ${RETURN_CODE})"
            return ${RETURN_CODE}
        else
            # Waiting three seconds before all CR threads really stopped.
            sleep 3

            echo "CentralReport stopped"
            return 0
        fi
    fi
}



# --
# CentralReport config assistant
# --
function macos_config_assistant {

    echo -e "\033[1;32mLauching CentralReport configuration assistant..."
    echo -e "\033[0m"

    sudo python ${CONFIG_ASSISTANT} < /dev/tty

    return 0

}




# --
# Uninstall functions
# --

function macos_remove_bin {

    if [ -d ${INSTALL_DIR} ]; then
        displayAndExec "Remove existing install directory..." sudo rm -rfv ${INSTALL_DIR}

        if [ $? -ne "0" ]; then
            displayError "Error on deleting CentralReport bin directory at ${INSTALL_DIR} (Error code : $?)"
            return 1
        else
            echo "Done!"
            return 0
        fi
    else
        echo "CentralReport bin directory doesn't exist."
        return 0
    fi
}

function macos_remove_config {

    if [ -f ${CONFIG_FILE} ]; then
        displayAndExec "Remove existing config file..." sudo rm -fv ${CONFIG_FILE}

        if [ $? -ne "0" ]; then
            displayError "Error on deleting CentralReport config file at ${CONFIG_FILE} (Error code : $?)"
            return 1
        else
            echo "Done!"
            return 0
        fi
    else
        echo "CentralReport config file not found."
        return 0
    fi
}

function macos_remove_startup_plist {

    if [ -f ${STARTUP_PLIST} ]; then
        displayAndExec "Remove existing startup plist file..." sudo rm -fv ${STARTUP_PLIST}

        if [ $? -ne "0" ]; then
            displayError "Error on deleting startup plist file at ${STARTUP_PLIST} (Error code : $?)"
            return 1
        else
            echo "Done!"
            return 0
        fi
    else
        echo "Startup plist file not found."
        return 0
    fi
}






# --
# Install functions
# --

function macos_cp_bin {
    # Copy CentralReport files in the right directory.

    echo -e "\nCopy CentralReport in the good directory..."

    # It's possible that /usr/local and /usr/local/bin doesn't exist. We will creating them in this case.
    if [ ! -d "/usr/local" ]; then
        sudo mkdir /usr/local
    fi
    if [ ! -d "/usr/local/bin" ]; then
            sudo mkdir /usr/local/bin
    fi

    sudo mkdir ${INSTALL_DIR}

    if [ $? -ne "0" ]; then
          displayError "Error on creating CentralReport dir at ${INSTALL_DIR} (Error code : $?)"
          return 1
    else
        sudo cp -R -f -v centralreport ${PARENT_DIR}

        if [ $? -ne "0" ]; then
            displayError "Error on copying CentralReport bin files in ${PARENT_DIR} (Error code : $?)"
            return 1
        else
            echo "Copy : Done !"
            return 0
        fi
    fi
}

function macos_cp_startup_plist {
    # Copy startup plist for launchd in the right directory.

    echo -e "\nCopy startup plist in the good directory..."

    sudo cp -f -v ${STARTUP_PLIST_INSTALL} ${STARTUP_PLIST}
    if [ $? -ne "0" ]; then
      displayError "Error on copying startup plist at ${STARTUP_PLIST} (Error code : $?)"
      return 1
    else
        echo "Done!"
        return 0
    fi
}








# --
# Install procedure
# --

function macos_install {

    # Use root privileges with sudo.
    echo -e "\n\nPlease use your administrator password to install CentralReport on this Mac."
    sudo -v
    if [ $? -ne 0 ]; then
        displayError "Impossible to use root privileges"
        return 1
    fi

    displayTitle "Removing any existing installation"

    # Uninstall existing previous installation, if exist
    macos_stop_cr
    if [ $? -ne 0 ]; then
        return 1
    fi

    # Delete CR bin files
    macos_remove_bin
    if [ $? -ne 0 ]; then
        return 1
    fi

    # Delete startup plist file
    macos_remove_startup_plist
    if [ $? -ne 0 ]; then
        return 1
    fi



    displayTitle "Installing CentralReport"

    macos_cp_bin
    if [ $? -ne 0 ]; then
        return 1
    fi

    macos_cp_startup_plist
    if [ $? -ne 0 ]; then
        return 1
    fi




    displayTitle "Starting installing thirparties software"
    echo " (Please consult http://github.com/miniche/CentralReport for licenses) "

    # First, we install CherryPy...
    displayAndExec "CherryPy" sudo easy_install CherryPy
    if [ $? -ne 0 ]; then
        return 1
    fi


    # Then, installing Jinja2 Templates...
    displayAndExec "Jinja" sudo easy_install Jinja2
    if [ $? -ne 0 ]; then
        return 1
    fi


    # Finally, installing Routes library...
    displayAndExec "Routes" sudo easy_install routes
    if [ $? -ne 0 ]; then
        return 1
    fi


    # Cleaning screen
    clear

    # CR config assistant
    macos_config_assistant

    echo " "
    echo " ** Starting CentralReport... ** "
    macos_start_cr
    if [ $? -ne 0 ]; then
        return 1
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

    displayTitle "Removing CentralReport files and directories"

    # Check if CentralReport is already running, and stop it.
    macos_stop_cr
    if [ $? -ne 0 ]; then
        return 1
    fi

    # Delete CR bin files
    macos_remove_bin
    if [ $? -ne 0 ]; then
        return 1
    fi

    # Delete CR config file
    macos_remove_config
    if [ $? -ne 0 ]; then
        return 1
    fi

    # Delete startup plist file
    macos_remove_startup_plist
    if [ $? -ne 0 ]; then
        return 1
    fi

    return 0
}
