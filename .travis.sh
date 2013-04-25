#!/bin/sh
echo "CentralReport build tes test"
echo "========================================"
echo "Check installation script"
echo "========================================"
echo " "
./install.sh autoinstall
echo " "
echo "Check if the service is running"
echo "========================================"
echo " "
service centralreport status
echo " "
echo "Check uninstallation script"
echo "========================================"
echo " "
./uninstall.sh autouninstall
echo " "
echo "========================================"
