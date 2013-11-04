#!/bin/bash

# ------------------------------------------------------------
# CentralReport Unix/Linux packager functions
# Alpha version. Don't use in production environment!
# ------------------------------------------------------------
# https://github.com/CentralReport
# ------------------------------------------------------------

#
# Reads a whitelist file and copies folders/files into the destination directory
#
# PARAMETERS:
#   $1: The whitelist file (relative or absolute path)
#   $2: The destination folder (relative or absolute path)
# RETURN:
#   0:  All the whitelist has been read without error
#   1:  Error copying an item
#   2:  Error finding an item in the origin folder
#
function read_whitelist(){

    for line in $(cat "$1");
    do
        if [[ ${line} == "#"* ]] || [[ ${line} == ";"* ]]; then
            continue
        fi

        if [ -d ${line} ]; then
            sudo cp -R ${line} "${2}${line}"
            if [ "$?" -ne "0" ]; then
                logError "Error copying ${line}!"
                return 1
            fi

        elif [ -f ${line} ]; then
            sudo cp ${line} "${2}${line}"
            if [ "$?" -ne "0" ]; then
                logError "Error copying ${line}!"
                return 1
            fi

        else
            logError "Missing file or directory: ${line}"
            return 2
        fi
    done

    return 0

}

#
# Reads a blacklist file and deletes folders/files from the destination directory
#
# PARAMETERS:
#   $1: The blacklist file (relative or absolute path)
#   $2: The destination folder (relative or absolute path)
# RETURN:
#   0:  All the blacklist has been read without error
#   1:  Error copying an item
#   2:  Error finding an item in the destination folder
#
function read_blacklist(){

    for line in $(cat "$1");
    do
        if [[ ${line} == "*"* ]] ; then
            find "${2}" -name "${line}" -exec sudo rm -rf {} \;
        elif [[ ${line} != "#"* ]] && [[ ${line} != ";"* ]] ; then
            if [ -d ${line} ]; then
                sudo rm -R ${line} "${2}${line}"
                if [ "$?" -ne "0" ]; then
                    logError "Error removing ${2}${line}!"
                    return 1
                fi

            elif [ -f ${line} ]; then
                sudo rm ${line} "${2}${line}"
                if [ "$?" -ne "0" ]; then
                    logError "Error removing ${2}${line}!"
                    return 1
                fi

            else
                logError "Missing file or directory: ${line}"
                return 2
            fi
        fi
    done

    return 0

}

#
# Creates the installer package
#
# PARAMETERS: None
# RETURN:
#   0:  The installer package has been created successfully
#   1:  Error processing the whitelist
#   2:  Error processing the blacklist
#   3:  Error creating the final package
#
function create_installer(){

    logConsole "Preparing the installer package..."

    cd "${CR_PROJECT_ROOT}"

    read_whitelist "./tools/packager/installer_whitelist.txt" "${CR_PACKAGES_ROOT}${CR_PACKAGE_INSTALLER_FOLDER}"
    if [ "$?" -ne "0" ]; then
        logError "Error processing the whitelist!"
        return 1
    fi

    read_blacklist "./tools/packager/installer_blacklist.txt" "${CR_PACKAGES_ROOT}${CR_PACKAGE_INSTALLER_FOLDER}"
    if [ "$?" -ne "0" ]; then
        logError "Error processing the blacklist!"
        return 2
    fi

    logConsole "Creating the installer package..."

    # We must be in this folder to generate a clean archive
    cd "${CR_PACKAGES_ROOT}"
    sudo tar -czf ${CR_PACKAGE_INSTALLER_NAME} ${CR_PACKAGE_INSTALLER_FOLDER}

    if [ "$?" -ne "0" ] || [ ! -f ${CR_PACKAGE_INSTALLER_NAME} ]; then
        logError "Error creating the installer package!"
        cd "${CR_PROJECT_ROOT}"

        return 3
    fi

    cd "${CR_PROJECT_ROOT}"
    return 0

}

#
# Creates the uninstaller package
#
# PARAMETERS: None
# RETURN:
#   0:  The uninstaller package has been created successfully
#   1:  Error processing the whitelist
#   2:  Error processing the blacklist
#   3:  Error creating the final package
#
function create_uninstaller(){

    logConsole "Preparing the uninstaller package..."

    cd "${CR_PROJECT_ROOT}"

    read_whitelist "./tools/packager/uninstaller_whitelist.txt" "${CR_PACKAGES_ROOT}${CR_PACKAGE_UNINSTALLER_FOLDER}"
    if [ "$?" -ne "0" ]; then
        logError "Error processing the whitelist!"
        return 1
    fi

    read_blacklist "./tools/packager/uninstaller_blacklist.txt" "${CR_PACKAGES_ROOT}${CR_PACKAGE_UNINSTALLER_FOLDER}"
    if [ "$?" -ne "0" ]; then
        logError "Error processing the blacklist!"
        return 1
    fi

    logConsole "Creating the uninstaller package..."

    # We must be in this folder to generate a clean archive
    cd "${CR_PACKAGES_ROOT}"
    sudo tar -czf ${CR_PACKAGE_UNINSTALLER_NAME} ${CR_PACKAGE_UNINSTALLER_FOLDER}

    if [ "$?" -ne "0" ] || [ ! -f ${CR_PACKAGE_UNINSTALLER_NAME} ]; then
        logError "Error creating the uninstaller package!"
        cd "${CR_PROJECT_ROOT}"

        return 3
    fi

    cd "${CR_PROJECT_ROOT}"
    return 0

}

#
# Generates the two packages: the installer and the uninstaller
#
# PARAMETERS: None
# RETURN:
#   0:  The packages have been created successfully
#   1:  Error creating the installer package
#   2:  Error creating the uninstaller package
#
function create_packages(){

    create_installer
    if [ "$?" -ne "0" ]; then
        logError "Error creating the installer package!"
        return 1
    fi

    create_uninstaller
    if [ "$?" -ne "0" ]; then
        logError "Error creating the uninstaller package!"
        return 2
    fi

    logConsole "Copying online scripts..."
    cd "${CR_PROJECT_ROOT}"
    sudo cp ${CR_INSTALLER_SCRIPT} "${CR_PACKAGES_ROOT}${CR_INSTALLER_SCRIPT_NAME}"
    sudo cp ${CR_UNINSTALLER_SCRIPT} "${CR_PACKAGES_ROOT}${CR_UNINSTALLER_SCRIPT_NAME}"

    return 0
}
