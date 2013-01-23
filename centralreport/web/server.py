#!/usr/bin/python
# -*- coding: utf-8 -*-

# CentralReport - Indev version
# Project by Charles-Emmanuel CAMUS - Avril 2012

import cherrypy
import cr.utils.date as crUtilsDate
import cr.utils.text as crUtilsText
import datetime
import os
import routes
import threading
from cr.threads import Checks
from cr.tools import Config
from jinja2 import Environment, FileSystemLoader


class WebServer(threading.Thread):

    current_dir = os.path.dirname(os.path.abspath(__file__))
    env = Environment(loader=FileSystemLoader(os.path.join(current_dir, 'tpl')))

    def __init__(self):
        """
            Manages the small webserver.
        """

        threading.Thread.__init__(self)

        # Register events...
        cherrypy.engine.subscribe('graceful', self.stop)

        # Update the configuration...
        cherrypy.config.update({'server.socket_host': Config.getConfigValue('Webserver', 'interface'),
                                'server.socket_port': int(Config.getConfigValue('Webserver', 'port'))})
        cherrypy.config.update({'tools.staticdir.root': WebServer.current_dir})
        cherrypy.config.update({'log.screen': False})

        # Serving static content
        confStaticContent = {
            '/statics': {
                'tools.staticdir.dir': 'statics',
                'tools.staticdir.on': True
                },
            '/css': {
                'tools.staticdir.dir': 'css',
                'tools.staticdir.on': True
                },
            '/img': {
                'tools.staticdir.dir': 'img',
                'tools.staticdir.on': True
                },
            '/js': {
                'tools.staticdir.dir': 'js',
                'tools.staticdir.on': True
                },
            '/media': {
                'tools.staticdir.dir': 'media',
                'tools.staticdir.on': True
                },
            '/api/check': {
                'request.dispatch': self.setupRoutes()
                }
            }

        # Using Pages class (see below)

        webApplication = cherrypy.tree.mount(Pages(self.env), '/', confStaticContent)

        # Disable screen log (standard out)

        if False == Config.CR_CONFIG_ENABLE_DEBUG_MODE:
            cherrypy.log.error_log.propagate = False
            cherrypy.log.access_log.propagate = False

        self.start()

    def setupRoutes(self):
        dispatcher = cherrypy.dispatch.RoutesDispatcher()
        dispatcher.connect('api_date_check', '/api/check/date', controller=Pages(self.env).api_date_check)
        dispatcher.connect('api_full_check', '/api/check/full', controller=Pages(self.env).api_full_check)
        dispatcher.connect('api_disks_check', '/api/check/disks', controller=Pages(self.env).api_disks_check)

        return dispatcher

    def run(self):
        """
            Starts the web server.
        """

        # Go go go!
        # cherrypy.engine.start() --> Consumes lot of CPU, updated with cherrypy.server.start()

        cherrypy.server.start()
        cherrypy.engine.block()

    def stop(self):
        """
            Stops the web server.
        """

        cherrypy.engine.stop()


class Pages:

    def __init__(self, env_template):
        self.env = env_template

    @cherrypy.expose
    def index(self):
        tmpl = self.env.get_template('index.tpl')

        tmpl_vars = dict()

        # Host informations
        tmpl_vars['hostname'] = Checks.hostEntity.hostname
        tmpl_vars['os_name'] = Checks.hostEntity.osName
        tmpl_vars['os_version'] = Checks.hostEntity.osVersion

        if Config.HOST_CURRENT == Config.HOST_MAC:
            tmpl_vars['host_os'] = 'MAC'
        elif Config.HOST_CURRENT == Config.HOST_UBUNTU:
            tmpl_vars['host_os'] = 'UBUNTU'
        elif Config.HOST_CURRENT == Config.HOST_DEBIAN:
            tmpl_vars['host_os'] = 'DEBIAN'

        tmpl_vars['CR_version'] = Config.CR_VERSION
        tmpl_vars['CR_version_name'] = Config.CR_VERSION_NAME

        if Checks.last_check_date is None:
            tmpl_vars['last_check'] = 'Never'
        else:
            tmpl_vars['last_check'] = Checks.last_check_date.strftime("%Y-%m-%d %H:%M:%S")

        # CPU stats
        if Checks.last_check_cpu is not None:
            tmpl_vars['cpu_percent'] = 100 - int(Checks.last_check_cpu.idle)
            tmpl_vars['cpu_user'] = Checks.last_check_cpu.user
            tmpl_vars['cpu_system'] = Checks.last_check_cpu.system
            tmpl_vars['cpu_count'] = Checks.hostEntity.cpuCount

            if int(tmpl_vars['cpu_percent']) >= int(Config.getConfigValue('Alerts', 'cpu_alert')):
                tmpl_vars['cpu_alert'] = True
            elif int(tmpl_vars['cpu_percent']) >= int(Config.getConfigValue('Alerts', 'cpu_warning')):
                tmpl_vars['cpu_warning'] = True
            else:
                tmpl_vars['cpu_ok'] = True

        # Memory and swap stats
        if Checks.last_check_memory is not None:

            # First : Memory stats
            tmpl_vars['memory_percent'] = ((int(Checks.last_check_memory.total) - int(
                Checks.last_check_memory.free)) * 100) / int(Checks.last_check_memory.total)
            tmpl_vars['memory_free'] = crUtilsText.convertByte(Checks.last_check_memory.free)
            tmpl_vars['memory_total'] = crUtilsText.convertByte(Checks.last_check_memory.total)
            tmpl_vars['memory_used'] = crUtilsText.convertByte(
                float(Checks.last_check_memory.total) - float(Checks.last_check_memory.free))

            # Memory status
            if int(tmpl_vars['memory_percent']) >= int(Config.getConfigValue('Alerts', 'memory_alert')):
                tmpl_vars['memory_alert'] = True
            elif int(tmpl_vars['memory_percent']) >= int(Config.getConfigValue('Alerts', 'memory_warning')):
                tmpl_vars['memory_warning'] = True
            else:
                tmpl_vars['memory_ok'] = True

            # Last : swap stats
            if 0 != int(Checks.last_check_memory.swapSize):
                tmpl_vars['swap_percent'] = int(Checks.last_check_memory.swapUsed) * 100 / int(
                    Checks.last_check_memory.swapSize)
                tmpl_vars['swap_used'] = crUtilsText.convertByte(Checks.last_check_memory.swapUsed)

                tmpl_vars['swap_free'] = crUtilsText.convertByte(Checks.last_check_memory.swapFree)
                tmpl_vars['swap_size'] = crUtilsText.convertByte(Checks.last_check_memory.swapSize)

                # On Mac, the swap is unlimited (only limited by the available hard drive size)
                if Checks.last_check_memory.swapSize == Checks.last_check_memory.total:

                    tmpl_vars['swap_configuration'] = 'unlimited'
                else:
                    tmpl_vars['swap_configuration'] = 'limited'

                if isinstance(tmpl_vars['swap_percent'], int):
                    if int(tmpl_vars['swap_percent']) >= int(Config.getConfigValue('Alerts', 'swap_alert')):
                        tmpl_vars['swap_alert'] = True
                    elif int(tmpl_vars['swap_percent']) >= int(Config.getConfigValue('Alerts', 'swap_warning')):

                        tmpl_vars['swap_warning'] = True
                    else:
                        tmpl_vars['swap_ok'] = True
                else:
                    tmpl_vars['swap_ok'] = True
            else:

                # No swap available on this host

                tmpl_vars['swap_configuration'] = 'undefined'

        # Load average stats
        if Checks.last_check_loadAverage is not None:
            tmpl_vars['loadaverage'] = Checks.last_check_loadAverage.last1m
            tmpl_vars['loadaverage_percent'] = (float(Checks.last_check_loadAverage.last1m) * 100) / int(
                Checks.hostEntity.cpuCount)

            if int(tmpl_vars['loadaverage_percent']) >= int(Config.getConfigValue('Alerts', 'load_alert')):
                tmpl_vars['load_alert'] = True
            elif int(tmpl_vars['loadaverage_percent']) >= int(Config.getConfigValue('Alerts', 'load_warning')):
                tmpl_vars['load_warning'] = True
            else:
                tmpl_vars['load_ok'] = True

        # Uptime stats (checked in load average collector)
        if Checks.last_check_loadAverage is not None:
            tmpl_vars['uptime'] = crUtilsText.secondsToPhraseTime(int(Checks.last_check_loadAverage.uptime))
            tmpl_vars['uptime_seconds'] = crUtilsText.numberSeparators(str(Checks.last_check_loadAverage.uptime))
            tmpl_vars['start_date'] = datetime.datetime.fromtimestamp(
                crUtilsDate.datetimeToTimestamp(Checks.last_check_date) - int(
                    Checks.last_check_loadAverage.uptime)).strftime("%Y-%m-%d %H:%M:%S")

        # DIsks stats

        if Checks.last_check_disk is not None:
            allChecksDisk = []

            for disk in Checks.last_check_disk.checks:
                checkDisk = {}

                # TODO : Find a better solution to decode UTF8
                checkDisk['name'] = str.replace(disk.name, '/dev/', '').decode('utf-8')
                checkDisk['free'] = crUtilsText.convertByte(disk.free)
                checkDisk['total'] = crUtilsText.convertByte(disk.size)
                checkDisk['percent'] = int(round(disk.used, 0) * 100 / int(disk.size))

                allChecksDisk.append(checkDisk)

            tmpl_vars['disks'] = allChecksDisk

        return tmpl.render(tmpl_vars)

    @cherrypy.expose
    def dashboard(self):
        tmpl = self.env.get_template('dashboard_mac.tpl')
        tmpl_vars = dict()

        tmpl_vars['last_check'] = Checks.last_check_date.strftime("%Y-%m-%d %H:%M:%S")
        tmpl_vars['host'] = Checks.hostEntity
        tmpl_vars['cpu'] = Checks.last_check_cpu
        tmpl_vars['memory'] = Checks.last_check_memory
        tmpl_vars['loadaverage'] = Checks.last_check_loadAverage
        tmpl_vars['disks'] = Checks.last_check_disk

        return tmpl.render(tmpl_vars)

    def error_page_404(status, message, traceback, version):
        """
            Returns the 404 error.
        """

        return "Oups... Error %s - Well, I'm so sorry but this page doesn't really exist!" % status

    cherrypy.config.update({'error_page.404': error_page_404})

    @cherrypy.expose()
    def api_date_check(self):
        tmpl = self.env.get_template('json/date_check.json')
        cherrypy.response.headers['Content-Type'] = 'application/json'
        tmpl_vars = dict()

        if Checks.last_check_date is None:
            tmpl_vars['last_timestamp'] = '0'
            tmpl_vars['last_fulldate'] = 'Never'
        else:
            tmpl_vars['last_timestamp'] = crUtilsDate.datetimeToTimestamp(Checks.last_check_date)
            tmpl_vars['last_fulldate'] = Checks.last_check_date.strftime("%Y-%m-%d %H:%M:%S")

        tmpl_vars['current_timestamp'] = crUtilsDate.datetimeToTimestamp(datetime.datetime.now())

        try:
            tmpl_vars['checks_interval'] = int(Config.getConfigValue('Checks', 'interval'))
        except:
            tmpl_vars['checks_interval'] = int(Config.CR_CONFIG_DEFAULT_CHECKS_INTERVAL)

        return tmpl.render(tmpl_vars)

    @cherrypy.expose()
    def api_full_check(self):
        tmpl = self.env.get_template('json/full_check.json')
        cherrypy.response.headers['Content-Type'] = 'application/json'
        tmpl_vars = dict()

        if Checks.last_check_date is None:
            tmpl_vars['last_timestamp'] = '0'
            tmpl_vars['last_fulldate'] = 'Never'
        else:
            tmpl_vars['last_timestamp'] = crUtilsDate.datetimeToTimestamp(Checks.last_check_date)
            tmpl_vars['last_fulldate'] = Checks.last_check_date.strftime("%Y-%m-%d %H:%M:%S")
            tmpl_vars['current_timestamp'] = crUtilsDate.datetimeToTimestamp(datetime.datetime.now())

            # CPU Check informations
            if Checks.last_check_cpu is None:
                tmpl_vars['cpu_check_enabled'] = 'False'
            else:
                tmpl_vars['cpu_check_enabled'] = 'True'

                tmpl_vars['cpu_percent'] = int(Checks.last_check_cpu.user) + int(Checks.last_check_cpu.system)
                tmpl_vars['cpu_user'] = Checks.last_check_cpu.user
                tmpl_vars['cpu_system'] = Checks.last_check_cpu.system

                if int(Config.getConfigValue('Alerts', 'cpu_alert')) <= int(tmpl_vars['cpu_percent']):
                    tmpl_vars['cpu_state'] = "alert"
                elif int(Config.getConfigValue('Alerts', 'cpu_warning')) <= int(tmpl_vars['cpu_percent']):
                    tmpl_vars['cpu_state'] = "warning"
                else:
                    tmpl_vars['cpu_state'] = 'ok'

            # Memory check informations
            if Checks.last_check_memory is None:
                tmpl_vars['memory_check_enabled'] = 'False'
            else:
                tmpl_vars['memory_check_enabled'] = "True"

                tmpl_vars['memory_percent'] = ((int(Checks.last_check_memory.total) - int(
                    Checks.last_check_memory.free)) * 100) / int(Checks.last_check_memory.total)
                tmpl_vars['memory_free'] = crUtilsText.convertByte(Checks.last_check_memory.free)
                tmpl_vars['memory_total'] = crUtilsText.convertByte(Checks.last_check_memory.total)
                tmpl_vars['memory_used'] = crUtilsText.convertByte(
                    float(Checks.last_check_memory.total) - float(Checks.last_check_memory.free))

                if int(tmpl_vars['memory_percent']) >= int(Config.getConfigValue('Alerts', 'memory_alert')):
                    tmpl_vars['memory_state'] = "alert"
                elif int(tmpl_vars['memory_percent']) >= int(Config.getConfigValue('Alerts', 'memory_warning')):
                    tmpl_vars['memory_state'] = "warning"
                else:
                    tmpl_vars['memory_state'] = 'ok'

                # Last : swap stats
                if 0 != int(Checks.last_check_memory.swapSize):
                    tmpl_vars['swap_percent'] = int(Checks.last_check_memory.swapUsed) * 100 / int(
                        Checks.last_check_memory.swapSize)
                    tmpl_vars['swap_used'] = crUtilsText.convertByte(Checks.last_check_memory.swapUsed)

                    tmpl_vars['swap_free'] = crUtilsText.convertByte(Checks.last_check_memory.swapFree)
                    tmpl_vars['swap_size'] = crUtilsText.convertByte(Checks.last_check_memory.swapSize)

                    # On Mac, the swap is unlimited (only limited by the available hard drive size)
                    if Checks.last_check_memory.swapSize == Checks.last_check_memory.total:

                        tmpl_vars['swap_configuration'] = 'unlimited'
                    else:
                        tmpl_vars['swap_configuration'] = 'limited'

                    if isinstance(tmpl_vars['swap_percent'], int):
                        if int(tmpl_vars['swap_percent']) >= int(Config.getConfigValue('Alerts', 'swap_alert')):
                            tmpl_vars['swap_state'] = 'alert'
                        elif int(tmpl_vars['swap_percent']) >= int(Config.getConfigValue('Alerts', 'swap_warning')):

                            tmpl_vars['swap_state'] = 'warning'
                        else:
                            tmpl_vars['swap_state'] = 'ok'
                    else:
                        tmpl_vars['swap_state'] = 'ok'
                else:

                    # No swap available on this host
                    tmpl_vars['swap_configuration'] = 'undefined'

            # Load average
            if Checks.last_check_loadAverage is None:
                tmpl_vars['load_check_enabled'] = 'False'
            else:
                tmpl_vars['load_check_enabled'] = "True"

                tmpl_vars['load_last_one'] = Checks.last_check_loadAverage.last1m
                tmpl_vars['load_percent'] = (float(Checks.last_check_loadAverage.last1m) * 100) / int(
                    Checks.hostEntity.cpuCount)

                if int(tmpl_vars['load_percent']) >= int(Config.getConfigValue('Alerts', 'load_alert')):
                    tmpl_vars['load_state'] = "alert"
                elif int(tmpl_vars['load_percent']) >= int(Config.getConfigValue('Alerts', 'load_warning')):
                    tmpl_vars['load_state'] = "warning"
                else:
                    tmpl_vars['load_state'] = 'ok'

                tmpl_vars['uptime_full_text'] = crUtilsText.secondsToPhraseTime(
                    int(Checks.last_check_loadAverage.uptime))
                tmpl_vars['uptime_seconds'] = crUtilsText.numberSeparators(str(Checks.last_check_loadAverage.uptime))
                tmpl_vars['start_date'] = datetime.datetime.fromtimestamp(
                    crUtilsDate.datetimeToTimestamp(Checks.last_check_date) - int(
                        Checks.last_check_loadAverage.uptime)).strftime("%Y-%m-%d %H:%M:%S")

        return tmpl.render(tmpl_vars)

    @cherrypy.expose()
    def api_disks_check(self):
        tmpl = self.env.get_template('blocks/disks.block.tpl')
        tmpl_vars = dict()

        if None != Checks.last_check_disk:
            allChecksDisk = []

            for disk in Checks.last_check_disk.checks:
                checkDisk = {}
                checkDisk['name'] = str.replace(disk.name, '/dev/', '').decode('utf-8')
                checkDisk['free'] = crUtilsText.convertByte(disk.free)
                checkDisk['total'] = crUtilsText.convertByte(disk.size)
                checkDisk['percent'] = int(round(disk.used, 0) * 100 / int(disk.size))

                allChecksDisk.append(checkDisk)

            tmpl_vars['disks'] = allChecksDisk

        return tmpl.render(tmpl_vars)
