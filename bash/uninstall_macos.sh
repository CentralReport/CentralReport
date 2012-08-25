# CentralReport Unix/Linux Indev version.
# By careful! Don't use in production environment!

function uninstall_from_mac(){

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

}