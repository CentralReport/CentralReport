# System and Unit tests

This folder will contain scripts to perform automatic tests.
They will be used with Travis and Vagrant.


**To perform tests, use the script:**
```bash
run_tests.sh
```

The options are:
* -a: Performs all tests
* -p: Performs all Python unit tests
* -s: Performs all system tests (global behavior)
* -v: Performs tests on virtual machines with Vagrant

## Python unit tests
Python unit tests check functions and methods written in Python, inside the CentralReport package.
The library "unittest" is used to perform test suites.

## System tests
The system tests check the global behavior of CentralReport. The following tasks are executed:
* Check the installer
* Check whether CentralReport is running after the installation
* Check the uninstaller

## Vagrant
CentralReport is supported on multiple operating systems: we use Vagrant with VirtualBox To checks the behavior of CR
on each OS. Python unit tests and System tests are performed in this case.

**Important:** You must have Vagrant and VirtualBox to perform these tests. Vagrant boxes are hosting on a CentralReport
server. The size of each box is approximately 300 MB.
