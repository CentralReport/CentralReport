#!/bin/sh
sudo ./install.sh autoinstall
service centralreport status
sudo ./uninstall.sh autouninstall
