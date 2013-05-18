# -*- coding: utf-8 -*-

"""
    CentralReport - Server module
        Manages internal web server

    https://github.com/CentralReport
"""

import datetime
import os
import sys
import threading

# By che: Temporary section. Will be improved soon.
# Testing importing zip libraries...
sys.path.insert(0, os.path.abspath(__file__ + '/../../libs/jinja2-2.6.zip'))
sys.path.insert(0, os.path.abspath(__file__ + '/../../libs/cherrypy-3.2.2.zip'))

import cherrypy
import jinja2
# End of temporary section by che.

from cr.utils.date import datetime_to_timestamp
from cr.utils import text
from cr.threads import Checks
from cr.tools import Config


class WebServer(threading.Thread):

    current_dir = os.path.dirname(os.path.abspath(__file__))
    env = jinja2.Environment(loader=jinja2.FileSystemLoader(os.path.join(current_dir, 'tpl')))

    def __init__(self):
        """
            Manages the small webserver.
        """

        threading.Thread.__init__(self)

        # Register events...
        cherrypy.engine.subscribe('graceful', self.stop)

        # Update the configuration...
        cherrypy.config.update({'server.socket_host': Config.get_config_value('Webserver', 'interface'),
                                'server.socket_port': int(Config.get_config_value('Webserver', 'port'))})
        cherrypy.config.update({'tools.staticdir.root': WebServer.current_dir})
        cherrypy.config.update({'log.screen': False})

        # Serving static content
        conf_static_content = {
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
            }
        }

        # Using Pages class (see below)
        webApplication = cherrypy.tree.mount(Pages(), '/', conf_static_content)

        # Disable screen log (standard out)

        if not Config.CR_CONFIG_ENABLE_DEBUG_MODE:
            cherrypy.log.error_log.propagate = False
            cherrypy.log.access_log.propagate = False

        self.start()

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


class Api:

    """
        This class handles the "/api" route in the webserver
        Gives raw data about the current host and the last check
    """

    STATE_ALERT = 'alert'
    STATE_OK = 'ok'
    STATE_WARNING = 'warning'

    CHECK_ENABLED = 'True'
    CHECK_DISABLED = 'False'

    @cherrypy.expose()
    def check(self, route):
        """
            Gets information about checks

            @param route: Can be 'date', 'full' or 'disk'
        """

        if route == 'date':
            tmpl = WebServer.env.get_template('json/date_check.json')
            cherrypy.response.headers['Content-Type'] = 'application/json'
            tmpl_vars = dict()

            if Checks.last_check is None:
                tmpl_vars['last_timestamp'] = '0'
                tmpl_vars['last_fulldate'] = 'Never'
            else:
                tmpl_vars['last_timestamp'] = datetime_to_timestamp(Checks.last_check.date)
                tmpl_vars['last_fulldate'] = Checks.last_check.date.strftime("%Y-%m-%d %H:%M:%S")

            tmpl_vars['current_timestamp'] = datetime_to_timestamp(datetime.datetime.now())

            try:
                tmpl_vars['checks_interval'] = int(Config.get_config_value('Checks', 'interval'))
            except:
                tmpl_vars['checks_interval'] = int(Config.CR_CONFIG_DEFAULT_CHECKS_INTERVAL)

            return tmpl.render(tmpl_vars)

        elif route == 'full':
            tmpl = WebServer.env.get_template('json/full_check.json')
            cherrypy.response.headers['Content-Type'] = 'application/json'
            tmpl_vars = dict()

            if Checks.last_check is None:
                tmpl_vars['last_timestamp'] = '0'
                tmpl_vars['last_fulldate'] = 'Never'
            else:
                tmpl_vars['last_timestamp'] = datetime_to_timestamp(Checks.last_check.date)
                tmpl_vars['last_fulldate'] = Checks.last_check.date.strftime("%Y-%m-%d %H:%M:%S")
                tmpl_vars['current_timestamp'] = datetime_to_timestamp(datetime.datetime.now())

                # CPU Check information
                if Checks.last_check.cpu is None:
                    tmpl_vars['cpu_check_enabled'] = Api.CHECK_DISABLED
                else:
                    tmpl_vars['cpu_check_enabled'] = Api.CHECK_ENABLED

                    tmpl_vars['cpu_percent'] = int(Checks.last_check.cpu.user) + int(Checks.last_check.cpu.system)
                    tmpl_vars['cpu_user'] = Checks.last_check.cpu.user
                    tmpl_vars['cpu_system'] = Checks.last_check.cpu.system

                    if int(Config.get_config_value('Alerts', 'cpu_alert')) <= int(tmpl_vars['cpu_percent']):
                        tmpl_vars['cpu_state'] = Api.STATE_ALERT
                    elif int(Config.get_config_value('Alerts', 'cpu_warning')) <= int(tmpl_vars['cpu_percent']):
                        tmpl_vars['cpu_state'] = Api.STATE_WARNING
                    else:
                        tmpl_vars['cpu_state'] = Api.STATE_OK

                # Memory check information
                if Checks.last_check.memory is None:
                    tmpl_vars['memory_check_enabled'] = Api.CHECK_DISABLED
                else:
                    tmpl_vars['memory_check_enabled'] = Api.CHECK_ENABLED

                    tmpl_vars['memory_percent'] = ((int(Checks.last_check.memory.total) - int(
                        Checks.last_check.memory.free)) * 100) / int(Checks.last_check.memory.total)
                    tmpl_vars['memory_free'] = text.convert_byte(Checks.last_check.memory.free)
                    tmpl_vars['memory_total'] = text.convert_byte(Checks.last_check.memory.total)
                    tmpl_vars['memory_used'] = text.convert_byte(
                        float(Checks.last_check.memory.total) - float(Checks.last_check.memory.free))

                    if int(tmpl_vars['memory_percent']) >= int(Config.get_config_value('Alerts', 'memory_alert')):
                        tmpl_vars['memory_state'] = Api.STATE_ALERT
                    elif int(tmpl_vars['memory_percent']) >= int(Config.get_config_value('Alerts', 'memory_warning')):
                        tmpl_vars['memory_state'] = Api.STATE_WARNING
                    else:
                        tmpl_vars['memory_state'] = Api.STATE_OK

                    # Last: swap stats
                    if 0 != int(Checks.last_check.memory.swap_size):
                        tmpl_vars['swap_percent'] = int(Checks.last_check.memory.swap_used) * 100 / int(
                            Checks.last_check.memory.swap_size)
                        tmpl_vars['swap_used'] = text.convert_byte(Checks.last_check.memory.swap_used)
                        tmpl_vars['swap_free'] = text.convert_byte(Checks.last_check.memory.swap_free)
                        tmpl_vars['swap_size'] = text.convert_byte(Checks.last_check.memory.swap_size)

                        # On Mac, the swap is unlimited (only limited by the available hard drive size)
                        if Checks.last_check.memory.swap_size == Checks.last_check.memory.total:
                            tmpl_vars['swap_configuration'] = 'unlimited'
                        else:
                            tmpl_vars['swap_configuration'] = 'limited'

                        if isinstance(tmpl_vars['swap_percent'], int):
                            if int(tmpl_vars['swap_percent']) >= int(Config.get_config_value('Alerts', 'swap_alert')):
                                tmpl_vars['swap_state'] = Api.STATE_ALERT
                            elif int(tmpl_vars['swap_percent']) >= int(Config.get_config_value('Alerts', 'swap_warning')):

                                tmpl_vars['swap_state'] = Api.STATE_WARNING
                            else:
                                tmpl_vars['swap_state'] = Api.STATE_OK
                        else:
                            tmpl_vars['swap_state'] = Api.STATE_OK
                    else:

                        # No swap available on this host
                        tmpl_vars['swap_configuration'] = 'undefined'

                # Load average
                if Checks.last_check.load is None:
                    tmpl_vars['load_check_enabled'] = Api.CHECK_DISABLED
                else:
                    tmpl_vars['load_check_enabled'] = Api.CHECK_ENABLED

                    tmpl_vars['load_last_one'] = Checks.last_check.load.last1m
                    tmpl_vars['load_percent'] = (float(Checks.last_check.load.last1m) * 100) / int(
                        Checks.host_infos.cpu_count)

                    if int(tmpl_vars['load_percent']) >= int(Config.get_config_value('Alerts', 'load_alert')):
                        tmpl_vars['load_state'] = Api.STATE_ALERT
                    elif int(tmpl_vars['load_percent']) >= int(Config.get_config_value('Alerts', 'load_warning')):
                        tmpl_vars['load_state'] = Api.STATE_WARNING
                    else:
                        tmpl_vars['load_state'] = Api.STATE_OK

                    tmpl_vars['uptime_full_text'] = text.convert_seconds_to_phrase_time(
                        int(Checks.last_check.load.uptime))
                    tmpl_vars['uptime_seconds'] = text.add_number_separators(str(Checks.last_check.load.uptime))
                    tmpl_vars['start_date'] = datetime.datetime.fromtimestamp(
                        datetime_to_timestamp(Checks.last_check.date) - int(
                            Checks.last_check.load.uptime)).strftime("%Y-%m-%d %H:%M:%S")

            return tmpl.render(tmpl_vars)

        elif route == 'disks':
            tmpl = WebServer.env.get_template('blocks/disks.block.tpl')
            tmpl_vars = dict()

            if Checks.last_check.disks is not None:
                all_disks = []

                for disk in Checks.last_check.disks.disks:
                    check_disk = {
                        'name': str.replace(disk.name, '/dev/', '').decode('utf-8'),
                        'free': text.convert_byte(disk.free),
                        'total': text.convert_byte(disk.size),
                        'percent': int(round(disk.used, 0) * 100 / int(disk.size))
                    }

                    all_disks.append(check_disk)

                tmpl_vars['disks'] = all_disks

            return tmpl.render(tmpl_vars)


class Pages:
    """
        This class handles webpages displayed on the user screen
    """

    api = Api()

    @cherrypy.expose
    def index(self):
        """
            Main entry (http://localhost:port/)
        """

        tmpl = WebServer.env.get_template('index.tpl')

        tmpl_vars = dict()

        # Host information
        tmpl_vars['hostname'] = Checks.host_infos.hostname
        tmpl_vars['os_name'] = Checks.host_infos.os_name
        tmpl_vars['os_version'] = Checks.host_infos.os_version

        if Config.HOST_CURRENT == Config.HOST_MAC:
            tmpl_vars['host_os'] = 'MAC'
        elif Config.HOST_CURRENT == Config.HOST_UBUNTU:
            tmpl_vars['host_os'] = 'UBUNTU'
        elif Config.HOST_CURRENT == Config.HOST_DEBIAN:
            tmpl_vars['host_os'] = 'DEBIAN'

        tmpl_vars['CR_version'] = Config.CR_VERSION
        tmpl_vars['CR_version_name'] = Config.CR_VERSION_NAME

        if Checks.last_check is None:
            tmpl_vars['last_check'] = 'Never'
        else:
            tmpl_vars['last_check'] = Checks.last_check.date.strftime("%Y-%m-%d %H:%M:%S")

        # CPU stats
        if Checks.last_check.cpu is not None:
            tmpl_vars['cpu_percent'] = 100 - int(Checks.last_check.cpu.idle)
            tmpl_vars['cpu_user'] = Checks.last_check.cpu.user
            tmpl_vars['cpu_system'] = Checks.last_check.cpu.system
            tmpl_vars['cpu_count'] = Checks.host_infos.cpu_count

            if int(tmpl_vars['cpu_percent']) >= int(Config.get_config_value('Alerts', 'cpu_alert')):
                tmpl_vars['cpu_alert'] = True
            elif int(tmpl_vars['cpu_percent']) >= int(Config.get_config_value('Alerts', 'cpu_warning')):
                tmpl_vars['cpu_warning'] = True
            else:
                tmpl_vars['cpu_ok'] = True

        # Memory and swap stats
        if Checks.last_check.memory is not None:

            # First: Memory stats
            tmpl_vars['memory_percent'] = ((int(Checks.last_check.memory.total) - int(
                Checks.last_check.memory.free)) * 100) / int(Checks.last_check.memory.total)
            tmpl_vars['memory_free'] = text.convert_byte(Checks.last_check.memory.free)
            tmpl_vars['memory_total'] = text.convert_byte(Checks.last_check.memory.total)
            tmpl_vars['memory_used'] = text.convert_byte(
                float(Checks.last_check.memory.total) - float(Checks.last_check.memory.free))

            # Memory status
            if int(tmpl_vars['memory_percent']) >= int(Config.get_config_value('Alerts', 'memory_alert')):
                tmpl_vars['memory_alert'] = True
            elif int(tmpl_vars['memory_percent']) >= int(Config.get_config_value('Alerts', 'memory_warning')):
                tmpl_vars['memory_warning'] = True
            else:
                tmpl_vars['memory_ok'] = True

            # Last: swap stats
            if 0 != int(Checks.last_check.memory.swap_size):
                tmpl_vars['swap_percent'] = int(Checks.last_check.memory.swap_used) * 100 / int(
                    Checks.last_check.memory.swap_size)
                tmpl_vars['swap_used'] = text.convert_byte(Checks.last_check.memory.swap_used)

                tmpl_vars['swap_free'] = text.convert_byte(Checks.last_check.memory.swap_free)
                tmpl_vars['swap_size'] = text.convert_byte(Checks.last_check.memory.swap_size)

                # On Mac, the swap is unlimited (only limited by the available hard drive size)
                if Checks.last_check.memory.swap_size == Checks.last_check.memory.total:

                    tmpl_vars['swap_configuration'] = 'unlimited'
                else:
                    tmpl_vars['swap_configuration'] = 'limited'

                if isinstance(tmpl_vars['swap_percent'], int):
                    if int(tmpl_vars['swap_percent']) >= int(Config.get_config_value('Alerts', 'swap_alert')):
                        tmpl_vars['swap_alert'] = True
                    elif int(tmpl_vars['swap_percent']) >= int(Config.get_config_value('Alerts', 'swap_warning')):

                        tmpl_vars['swap_warning'] = True
                    else:
                        tmpl_vars['swap_ok'] = True
                else:
                    tmpl_vars['swap_ok'] = True
            else:

                # No swap available on this host

                tmpl_vars['swap_configuration'] = 'undefined'

        # Load average stats
        if Checks.last_check.load is not None:
            tmpl_vars['loadaverage'] = Checks.last_check.load.last1m
            tmpl_vars['loadaverage_percent'] = (float(Checks.last_check.load.last1m) * 100) / int(
                Checks.host_infos.cpu_count)

            if int(tmpl_vars['loadaverage_percent']) >= int(Config.get_config_value('Alerts', 'load_alert')):
                tmpl_vars['load_alert'] = True
            elif int(tmpl_vars['loadaverage_percent']) >= int(Config.get_config_value('Alerts', 'load_warning')):
                tmpl_vars['load_warning'] = True
            else:
                tmpl_vars['load_ok'] = True

        # Uptime stats (checked in load average collector)
        if Checks.last_check.load is not None:
            tmpl_vars['uptime'] = text.convert_seconds_to_phrase_time(int(Checks.last_check.load.uptime))
            tmpl_vars['uptime_seconds'] = text.add_number_separators(str(Checks.last_check.load.uptime))
            tmpl_vars['start_date'] = datetime.datetime.fromtimestamp(
                datetime_to_timestamp(Checks.last_check.date) - int(
                    Checks.last_check.load.uptime)).strftime("%Y-%m-%d %H:%M:%S")

        # Disks stats

        if Checks.last_check.disks is not None:
            all_disks = []

            for disk in Checks.last_check.disks.disks:
                # TODO: Find a better solution to decode UTF8
                check_disk = {
                    'name': str.replace(disk.name, '/dev/', '').decode('utf-8'),
                    'free': text.convert_byte(disk.free),
                    'total': text.convert_byte(disk.size),
                    'percent': int(round(disk.used, 0) * 100 / int(disk.size))
                }

                all_disks.append(check_disk)

            tmpl_vars['disks'] = all_disks

        return tmpl.render(tmpl_vars)

    def error_page_404(status, message, traceback, version):
        """
            Handles the 404 error.
        """

        return "Oups... Error %s - Well, I'm so sorry but this page doesn't really exist!" % status

    cherrypy.config.update({'error_page.404': error_page_404})
