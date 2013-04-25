#!/bin/sh
./install.sh autoinstall
service centralreport status
./uninstall.sh autouninstall
