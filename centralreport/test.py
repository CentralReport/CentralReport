import centralreport
import sys

# CentralReport - Indev version
# Project by Charles-Emmanuel CAMUS - Avril 2012

# This test file can launch CentralReport on dev host, without installation.
# Please verify CR is not installed on your host before launch this script.

print('--- CentralReport debug mode. ---')
print('This tool is only for debug purpose. For running CR in production env, '
      'use python centralreport.py start instead.')
print('---------------------------------')
print('')

cr = centralreport.CentralReport("/tmp/centralreport_debug.pid")
return_value = cr.debug()

print('')
print('---------------------------------')
print('Ending debug mode')
print('---------------------------------')

# Ok !
sys.exit(0)
