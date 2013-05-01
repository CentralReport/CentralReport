#!/bin/sh

# Travis tests. Must be refactored when Bash/Python
# unit tests will be available.

echo "========================================"
echo "Check installation script"
echo "========================================"
echo " "
./install.sh -s
echo " "
echo "Check if the service is running"
echo "========================================"
echo " "
service centralreport status
echo " "
echo "Check uninstallation script"
echo "========================================"
echo " "
./uninstall.sh -s
echo " "
echo "========================================"
