#!/bin/bash

# WIP: This script executes tests with Vagrant

vagrant up cr_debian_squeeze_64
vagrant ssh cr_debian_squeeze_64 --command "python /vagrant/centralreport/tests.py"

if [ "$?" -eq 0 ]; then
    echo "All tests OK"
else
    echo "Error executing tests..."
fi

vagrant destroy cr_debian_squeeze_64 --force

# Testing multiple VMs...
vagrant up cr_centos_6_4_64
vagrant ssh cr_centos_6_4_64 --command "python /vagrant/centralreport/tests.py"

if [ "$?" -eq 0 ]; then
    echo "All tests OK"
else
    echo "Error executing tests..."
fi

vagrant destroy cr_centos_6_4_64 --force
