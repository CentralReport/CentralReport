#!/bin/bash

# CentralReport Unix/Linux Indev version.
# By careful! Don't use in production environment!

# This file contain all functions to manage CR install/unistall on a Mac.



# --
# CentralReport daemon functions
# --

function macos_start_cr {

    echo "Starting CentralReport..."

    if [ -f ${PID_FILE} ]; then
        echo "CentralReport is already running!"
        return 1

    else
        python ${INSTALL_DIR}/run.py start

        if [ $? -ne "0" ]; then
            displayError "Error on starting CentralReport (Error code : $?)"
            return 0
        else
            echo "CentralReport started?"
            return 1
        fi
    fi


}

function macos_stop_cr {

    echo "Stopping CentralReport..."

    if [ ! -f ${PID_FILE} ]; then
            echo "CentralReport is already stopped!"
            return 1
    else
        python ${INSTALL_DIR}/run.py stop

        if [ $? -ne "0" ]; then
            displayError "Error on stopping CentralReport (Error code : $?)"
            return 0
        else
            echo "CentralReport stopped"
            return 1
        fi
    fi
}









# --
# Uninstall functions
# --

function macos_remove_bin {
    echo "Remove existing install directory..."

    if [ -d ${INSTALL_DIR} ]; then
        sudo rm -rfv $INSTALL_DIR

        if [ $? -ne "0" ]; then
            displayError "Error on deleting CentralReport bin directory at ${INSTALL_DIR} (Error code : $?)"
            return 0
        else
            echo "Done!"
            return 1
        fi
    else
        echo "CentralReport bin directory doesn't exist."
        return 1
    fi
}

function macos_remove_config {
    echo "Remove existing config file..."

    if [ -f ${CONFIG_FILE} ]; then
        sudo rm -fv $CONFIG_FILE

        if [ $? -ne "0" ]; then
            displayError "Error on deleting CentralReport config file at ${CONFIG_FILE} (Error code : $?)"
            return 0
        else
            echo "Done!"
            return 1
        fi
    else
        echo "CentralReport config file not found."
        return 1
    fi
}

function macos_remove_startup_plist {
    echo "Remove existing startup plist file..."

    if [ -f ${STARTUP_PLIST} ]; then
        sudo rm -fv $STARTUP_PLIST

        if [ $? -ne "0" ]; then
            displayError "Error on deleting startup plist file at ${STARTUP_PLIST} (Error code : $?)"
            return 0
        else
            echo "Done!"
            return 1
        fi
    else
        echo "Startup plist file not found."
        return 1
    fi
}






# --
# Install functions
# --

function macos_cp_bin {
    # Copy CentralReport files in the right directory.

    echo " "
    echo "Copy CentralReport in the good directory..."

    sudo mkdir ${INSTALL_DIR}

    if [ $? -ne "0" ]; then
          displayError "Error on creating CentralReport dir at ${INSTALL_DIR} (Error code : $?)"
          return 0
    else
        sudo cp -R -f -v centralreport ${PARENT_DIR}

        if [ $? -ne "0" ]; then
            displayError "Error on copying CentralReport bin files in ${PARENT_DIR} (Error code : $?)"
            return 0
        else
            echo "Copy : Done !"
            return 1
        fi
    fi
}

function macos_cp_startup_plist {
    # Copy startup plist for launchd in the right directory.

    echo " "
    echo "Copy startup plist in the good directory..."

    sudo cp -f -v ${STARTUP_PLIST_INSTALL} ${STARTUP_PLIST}

    if [ $? -ne "0" ]; then
      displayError "Error on copying startup plist at ${STARTUP_PLIST} (Error code : $?)"
      return 0
    else
        echo "Done!"
        return 1
    fi
}










function install_on_macos {

    # Check if CentralReport is already running!
    macos_stop_cr

    # We check if we found datas about CentralReport
    macos_remove_bin
    macos_remove_config
    macos_remove_startup_plist

    echo " "
    echo " ** Starting installation ** "
    echo " "

    macos_cp_bin
    macos_cp_startup_plist


    echo " "
    echo " ** Starting installing thirparties software ** "
    echo " (Please consult http://github.com/miniche/CentralReport for licenses) "
    echo " "


    # First, we install CherryPy
    echo "Installing CherryPy"
    echo "Untar CherryPy..."
    tar -xzvf ${CHERRYPY_TAR} -C thirdparties/

    echo "Installing CherryPy..."
    cd ${CHERRYPY_DIR};
    sudo python setup.py install
    cd ../../;

    echo "Deleting install files..."
    sudo rm -Rf ${CHERRYPY_DIR}

    echo "CherryPy is installed!"
    echo " "



    # Then, installing Mako Templates...
    echo "Installing Mako Templates"
    echo "Untar Mako..."
    tar -xzvf ${MAKO_TAR} -C thirdparties/

    echo "Installing Mako..."
    cd ${MAKO_DIR};
    sudo python setup.py install
    cd ../../;

    echo "Deleting install files..."
    sudo rm -Rf ${MAKO_DIR}

    echo "Mako is installed!"
    echo " "


    echo " "
    echo " ** Starting CentralReport... ** "
    python ${INSTALL_DIR}/run.py start
}

