#!/bin/bash

# CentralReport Unix/Linux Indev version.
# By careful! Don't use in production environment!

# This file contain all functions to manage CR install/unistall on a Debian/Ubuntu distribution.



# --
# CentralReport daemon functions
# --

function debian_start_cr {

    echo -e "\nStarting CentralReport..."

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

    echo -e "\nStopping CentralReport..."

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

    echo -e "\033[1;32mLauching CentralReport configuration assistant..."
    echo -e "\033[0m"

    python ${CONFIG_ASSISTANT}

    return 0

}




# --
# Uninstall functions
# --

function debian_remove_bin {

    echo -e "\nRemove existing install directory..."

    if [ -d ${INSTALL_DIR} ]; then
        rm -rfv $INSTALL_DIR

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

function debian_remove_config {

    echo -e "\nRemove existing config file..."

    if [ -f ${CONFIG_FILE} ]; then
        rm -fv $CONFIG_FILE

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

function debian_remove_startup_script {

    echo -e "\nRemove existing startup plist file..."

    if [ -f ${STARTUP_DEBIAN} ]; then
        rm -rfv $STARTUP_DEBIAN

        if [ $? -ne "0" ]; then
            displayError "Error on deleting startup script at ${STARTUP_DEBIAN} (Error code : $?)"
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

function debian_cp_bin {
    # Copy CentralReport files in the right directory.

    echo -e "\nCopy CentralReport in the good directory..."

    mkdir ${INSTALL_DIR}

    if [ $? -ne "0" ]; then
          displayError "Error on creating CentralReport dir at ${INSTALL_DIR} (Error code : $?)"
          return 1
    else
        cp -R -f -v centralreport ${PARENT_DIR}

        if [ $? -ne "0" ]; then
            displayError "Error on copying CentralReport bin files in ${PARENT_DIR} (Error code : $?)"
            return 1
        else
            echo "Copy : Done !"
            return 0
        fi
    fi
}

function debian_cp_startup_plist {
    # Copy startup plist for launchd in the right directory.

    echo -e "\nCopy startup script in the good directory..."

    cp -f -v ${STARTUP_DEBIAN_INSTALL} ${STARTUP_DEBIAN}
    if [ $? -ne "0" ]; then
      displayError "Error on copying startup script at ${STARTUP_PLIST} (Error code : $?)"
      return 1
    else
        chmod 755 ${STARTUP_DEBIAN}

        update-rc.d centralreport.sh defaults

        if [ $? -ne "0" ]; then
          displayError "Error on registering startup script with update-rc.d (Error code : $?)"
          return 1
        else
            echo "Done!"
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


    echo " "
    echo " ** Starting installation ** "
    echo " "

    debian_cp_bin
    if [ $? -ne 0 ]; then
        return 1
    fi

    debian_cp_startup_plist
    if [ $? -ne 0 ]; then
        return 1
    fi




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
    python setup.py install
    cd ../../;

    echo "Deleting install files..."
    rm -Rf ${CHERRYPY_DIR}

    echo "CherryPy is installed!"
    echo " "



    # Then, installing Jinja2 Templates...
    echo "Installing Jinja2"
    echo "Untar Jinja2..."
    tar -xzvf ${JINJA_TAR} -C thirdparties/

    echo "Installing Jinja2..."
    cd ${JINJA_DIR};
    python setup.py install
    cd ../../;

    echo "Deleting install files..."
    rm -Rf ${JINJA_DIR}

    echo "Jinja2 is installed!"
    echo " "

    # Cleaning screen
    clear

    # CR config assistant
    debian_config_assistant

    echo " "
    echo " ** Starting CentralReport... ** "
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
