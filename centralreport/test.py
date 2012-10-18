import centralreport

# CentralReport - Indev version
# Project by Charles-Emmanuel CAMUS - Avril 2012

# This test file can launch CentralReport on dev host, without installation.
# Please verify CR is not installed on your host before launch this script.

cr = centralreport.CentralReport("/tmp/centralreport_debug.pid")
cr.run()

# Ok !
