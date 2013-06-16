#!/bin/bash

# WIP: This script executes tests with Vagrant

vagrant up
vagrant ssh --command "python /vagrant/centralreport/tests.py"

if [ "$?" -eq 0 ]; then
    echo "All tests OK"
else
    echo "Error executing tests..."
fi

vagrant destroy --force
