#!/bin/bash

# CentralReport Unix/Linux Indev version.
# By careful! Don't use in production environment!

function install_on_macos()
{
    # Check if CentralReport is already running!
    echo "Checking if CentralReport is already running"
    if [ -f ${PID_FILE} ]; then
        echo "CentralReport is already running! Trying to stop it..."
        sudo python ${INSTALL_DIR}/run.py stop
        echo "Done!"
    fi

    # We check if we found datas about CentralReport
    echo "Checking if install directory already exist"
    if [ -d ${INSTALL_DIR} ]; then
        echo "Remove existing install directory"
        sudo rm -rfv $INSTALL_DIR
        echo "Done!"
    fi

    echo "Checking if a config file already exist"
    if [ -f ${CONFIG_FILE} ]; then
        echo "Remove existing config file"
        sudo rm -fv $CONFIG_FILE
        echo "Done!"
    fi

    echo "Checking if the startup plist already exist"
    if [ -f ${STARTUP_PLIST} ]; then
        echo "Remove existing startup plist"
        sudo rm -rfv $STARTUP_PLIST
        echo "Done!"
    fi

    echo " "
    echo " ** Starting installation ** "
    echo " "

    echo "Copy CentralReport in the good directory..."
    echo " -- "
    sudo mkdir ${INSTALL_DIR}
    sudo cp -R -f -v centralreport ${PARENT_DIR}
    echo " -- "
    echo "Copy : Done !"

    echo " "
    echo "Copy startup plist in the good directory..."
    sudo cp -f -v ${STARTUP_PLIST_INSTALL} ${STARTUP_PLIST}
    echo "Done!"


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
}
