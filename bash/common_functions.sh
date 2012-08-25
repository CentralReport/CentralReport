# CentralReport Unix/Linux Indev version.
# By careful! Don't use in production environment!


# OS
CURRENT_OS=
OS_MAC="MacOS"
OS_DEBIAN="Debian"


function getOS(){
    # Getting actual OS (Linux distrib or Unix OS)
    if [ $(uname -s) == "Darwin" ]; then
        CURRENT_OS=${OS_MAC}
    fi
}