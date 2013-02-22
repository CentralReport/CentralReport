#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
    CentralReport - Test script
        Launchs CentralReport in debug mode, without installation.
        Please verify CR is not installed on your host before launch this script.

    https://github.com/miniche/CentralReport/
"""

import sys
import os

import centralreport

print '--- CentralReport debug mode. ---'
print 'This tool is only for debug purpose. For running CR in production env, use python centralreport.py start instead.'
print '---------------------------------'
print ''

cr = centralreport.CentralReport('/tmp/centralreport_debug.pid')
return_value = cr.debug()

print ''
print '---------------------------------'
print 'Ending debug mode'
print '---------------------------------'

# CentralReport is now stopped, we can kill current process
os.system('kill %d' % os.getpid())
sys.exit(0)
