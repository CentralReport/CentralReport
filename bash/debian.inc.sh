#!/bin/bash

# CentralReport Unix/Linux Indev version.
# By careful! Don't use in production environment!

# This file contain all functions to manage CR install/unistall on a Debian/Ubuntu distribution.


# --
# CentralReport daemon functions
# --
function debian_start_cr {

    if [ -f ${PID_FILE} ]; then
        echo "CentralReport is already running!"
        return 0

    else
        python ${INSTALL_DIR}/centralreport.py start

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

function debian_stop_cr {

    displaytTitle "Stopping CentralReport..."

    if [ ! -f ${PID_FILE} ]; then
            echo "CentralReport is already stopped!"
            return 0
    else
        python ${INSTALL_DIR}/centralreport.py stop

        if [ $? -ne "0" ]; then
            displayError "Error on stopping CentralReport (Error code : $?)"
            return 1
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
function debian_config_assistant {

    echo -e "\033[44m\033[1;37m"
    displaytTitle "Lauching CentralReport configuration assistant..."
    echo -e "\033[0m"

    python ${CONFIG_ASSISTANT} < /dev/tty

    return 0
}

# --
# Uninstall functions
# --

function debian_remove_bin {

    if [ -d ${INSTALL_DIR} ]; then
        displayAndExec "Remove existing install directory..." rm -rfv $INSTALL_DIR

        if [ $? -ne "0" ]; then
            displayError "Error on deleting CentralReport bin directory at ${INSTALL_DIR} (Error code : $?)"
            return 1
        else
            return 0
        fi
    else
        echo "CentralReport bin directory doesn't exist."
        return 0
    fi
}

function debian_remove_config {

    if [ -f ${CONFIG_FILE} ]; then
        displayAndExec "Remove existing config file..." rm -fv $CONFIG_FILE

        if [ $? -ne "0" ]; then
            displayError "Error on deleting CentralReport config file at ${CONFIG_FILE} (Error code : $?)"
            return 1
        else
            return 0
        fi
    else
        echo "CentralReport config file not found."
        return 0
    fi
}

function debian_remove_startup_script {

    if [ -f ${STARTUP_DEBIAN} ]; then
        displayAndExec "Remove existing startup script..." rm -rfv $STARTUP_DEBIAN

        if [ $? -ne "0" ]; then
            displayError "Error on deleting startup script at ${STARTUP_DEBIAN} (Error code : $?)"
            return 1
        else

        displayAndExec "Removing startup service" update-rc.d -f centralreport.sh remove

            if [ $? -ne "0" ]; then
                displayError "Error on removing startup script with update-rc.d (Error code : $?)"
                return 1
            else
                return 0
            fi
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
function debian_cp_bin {
    # Copy CentralReport files in the right directory.
    mkdir ${INSTALL_DIR}

    if [ $? -ne "0" ]; then
          displayError "Error on creating CentralReport dir at ${INSTALL_DIR} (Error code : $?)"
          return 1
    else
        displayAndExec "Copy CentralReport in the good directory..." cp -R -f -v centralreport ${PARENT_DIR}

        if [ $? -ne "0" ]; then
            displayError "Error on copying CentralReport bin files in ${PARENT_DIR} (Error code : $?)"
            return 1
        else
            return 0
        fi
    fi
}

function debian_cp_startup_plist {
    # Copy startup plist for launchd in the right directory.

    displayAndExec "Copy startup script in the good directory..." cp -f -v ${STARTUP_DEBIAN_INSTALL} ${STARTUP_DEBIAN}
    if [ $? -ne "0" ]; then
      displayError "Error on copying startup script at ${STARTUP_PLIST} (Error code : $?)"
      return 1
    else
        chmod 755 ${STARTUP_DEBIAN}

        displayAndExec "Registering startup script" update-rc.d centralreport.sh defaults

        if [ $? -ne "0" ]; then
          displayError "Error on registering startup script with update-rc.d (Error code : $?)"
          return 1
        else
            return 0
        fi
    fi
}

# --
# Install procedure
# --
function debian_install {

    # Install only can perform if current user is root (or have administrative privileges)
    if [[ $EUID -ne 0 ]]; then
        echo " "
        displayError "You must be root to run CentralReport installer!"
        exit 1
    fi

    # Uninstall previsous installation, if exist.
    debian_stop_cr
    if [ $? -ne 0 ]; then
        return 1
    fi

    # Delete CR bin files
    debian_remove_bin
    if [ $? -ne 0 ]; then
        return 1
    fi

    # Delete startup plist file
    debian_remove_startup_script
    if [ $? -ne 0 ]; then
        return 1
    fi

    displaytTitle "Starting installation"

    debian_cp_bin
    if [ $? -ne 0 ]; then
        return 1
    fi

    debian_cp_startup_plist
    if [ $? -ne 0 ]; then
        return 1
    fi

    displaytTitle "Starting installing thirparties software"
    echo " (Please consult http://github.com/miniche/CentralReport for licenses) "

    # First, we install CherryPy
    displaytTitle "Installing CherryPy"
    displayAndExec "Untar CherryPy..." tar -xzvf ${CHERRYPY_TAR} -C thirdparties/

    cd ${CHERRYPY_DIR};
    displayAndExec "Installing CherryPy..." python setup.py install
    cd ../../;

    displayAndExec "Deleting install files..." rm -Rf ${CHERRYPY_DIR}

    # First, we install Setuptools
    displaytTitle "Installing Setuptools"
    displayAndExec "Untar Setuptools..." tar -xzvf ${SETUPTOOLS_TAR} -C thirdparties/

    cd ${SETUPTOOLS_DIR};
    displayAndExec "Installing Setuptools..." python setup.py install
    cd ../../;

    displayAndExec "Deleting install files..." rm -Rf ${SETUPTOOLS_DIR}

    # Then, installing Jinja2 Templates...
    displaytTitle "Installing Jinja2"
    displayAndExec "Untar Jinja2..." tar -xzvf ${JINJA_TAR} -C thirdparties/

    cd ${JINJA_DIR};
    displayAndExec "Installing Jinja2..." python setup.py install
    cd ../../;

    displayAndExec "Deleting install files..." rm -Rf ${JINJA_DIR}

    # CR config assistant
    debian_config_assistant

    displaytTitle "Starting CentralReport..."
    debian_start_cr
    if [ $? -ne 0 ]; then
        return 1
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
        displayError "You must be root to uninstall CentralReport!"
        exit 1
    fi

    # Check if CentralReport is already running, and stop it.
    debian_stop_cr
    if [ $? -ne 0 ]; then
        return 1
    fi

    # Delete CR bin files
    debian_remove_bin
    if [ $? -ne 0 ]; then
        return 1
    fi

    # Delete CR config file
    debian_remove_config
    if [ $? -ne 0 ]; then
        return 1
    fi

    # Delete startup plist file
    debian_remove_startup_script
    if [ $? -ne 0 ]; then
        return 1
    fi

    return 0
}
