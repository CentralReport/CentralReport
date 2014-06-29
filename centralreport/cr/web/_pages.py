# -*- coding: utf-8 -*-

"""
    CentralReport - Server module
        This module handles webpages displayed on the user screen

    https://github.com/CentralReport
"""

import datetime

from cr.web import server
from cr import data
import cr.host
from cr.utils.date import datetime_to_timestamp
from cr.utils import text
from cr.tools import Config


@server.app.route('/')
def index():
    """
        Main entry (http://localhost:port/)
    """

    tmpl = server.app.jinja_env.get_template('index.tpl')

    tmpl_vars = dict()

    # Host information
    tmpl_vars['hostname'] = cr.host.get_current_host().hostname
    tmpl_vars['os_name'] = cr.host.get_current_host().os_name
    tmpl_vars['os_version'] = cr.host.get_current_host().os_version

    if cr.host.get_current_host().os == cr.host.OS_MAC:
        tmpl_vars['host_os'] = 'MAC'
    elif cr.host.get_current_host().os == cr.host.OS_UBUNTU:
        tmpl_vars['host_os'] = 'UBUNTU'
    elif cr.host.get_current_host().os == cr.host.OS_DEBIAN:
        tmpl_vars['host_os'] = 'DEBIAN'
    elif cr.host.get_current_host().os == cr.host.OS_CENTOS:
        tmpl_vars['host_os'] = 'CENTOS'

    tmpl_vars['CR_version'] = Config.CR_VERSION
    tmpl_vars['CR_version_name'] = Config.CR_VERSION_NAME

    if data.last_check is None:
        tmpl_vars['last_check'] = 'Never'
    else:
        tmpl_vars['last_check'] = data.last_check.date.strftime("%Y-%m-%d %H:%M:%S")

    # CPU stats
    if data.last_check.cpu is not None:
        tmpl_vars['cpu_percent'] = 100 - int(data.last_check.cpu.idle)
        tmpl_vars['cpu_user'] = data.last_check.cpu.user
        tmpl_vars['cpu_system'] = data.last_check.cpu.system
        tmpl_vars['cpu_count'] = cr.host.get_current_host().cpu_count

        if int(tmpl_vars['cpu_percent']) >= int(Config.get_config_value('Alerts', 'cpu_alert')):
            tmpl_vars['cpu_alert'] = True
        elif int(tmpl_vars['cpu_percent']) >= int(Config.get_config_value('Alerts', 'cpu_warning')):
            tmpl_vars['cpu_warning'] = True
        else:
            tmpl_vars['cpu_ok'] = True

    # Memory and swap stats
    if data.last_check.memory is not None:

        # First: Memory stats
        tmpl_vars['memory_percent'] = ((int(data.last_check.memory.total) - int(
            data.last_check.memory.free)) * 100) / int(data.last_check.memory.total)
        tmpl_vars['memory_free'] = text.convert_byte(data.last_check.memory.free)
        tmpl_vars['memory_total'] = text.convert_byte(data.last_check.memory.total)
        tmpl_vars['memory_used'] = text.convert_byte(
            float(data.last_check.memory.total) - float(data.last_check.memory.free))

        # Memory status
        if int(tmpl_vars['memory_percent']) >= int(Config.get_config_value('Alerts', 'memory_alert')):
            tmpl_vars['memory_alert'] = True
        elif int(tmpl_vars['memory_percent']) >= int(Config.get_config_value('Alerts', 'memory_warning')):
            tmpl_vars['memory_warning'] = True
        else:
            tmpl_vars['memory_ok'] = True

        # Last: swap stats
        if 0 != int(data.last_check.memory.swap_size):
            tmpl_vars['swap_percent'] = int(data.last_check.memory.swap_used) * 100 / int(
                data.last_check.memory.swap_size)
            tmpl_vars['swap_used'] = text.convert_byte(data.last_check.memory.swap_used)

            tmpl_vars['swap_free'] = text.convert_byte(data.last_check.memory.swap_free)
            tmpl_vars['swap_size'] = text.convert_byte(data.last_check.memory.swap_size)

            # On Mac, the swap is unlimited (only limited by the available hard drive size)
            if data.last_check.memory.swap_size == data.last_check.memory.total:

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
    if data.last_check.load is not None:
        tmpl_vars['loadaverage'] = data.last_check.load.last1m
        tmpl_vars['loadaverage_percent'] = (float(data.last_check.load.last1m) * 100) / int(
            cr.host.get_current_host().cpu_count)

        if int(tmpl_vars['loadaverage_percent']) >= int(Config.get_config_value('Alerts', 'load_alert')):
            tmpl_vars['load_alert'] = True
        elif int(tmpl_vars['loadaverage_percent']) >= int(Config.get_config_value('Alerts', 'load_warning')):
            tmpl_vars['load_warning'] = True
        else:
            tmpl_vars['load_ok'] = True

    # Uptime stats (checked in load average collector)
    if data.last_check.load is not None:
        tmpl_vars['uptime'] = text.convert_seconds_to_phrase_time(int(data.last_check.load.uptime))
        tmpl_vars['uptime_seconds'] = text.add_number_separators(str(data.last_check.load.uptime))
        tmpl_vars['start_date'] = datetime.datetime.fromtimestamp(
            datetime_to_timestamp(data.last_check.date) - int(
                data.last_check.load.uptime)).strftime("%Y-%m-%d %H:%M:%S")

    # Disks stats

    if data.last_check.disks is not None:
        all_disks = []

        for disk in data.last_check.disks.disks:
            # TODO: Find a better solution to decode UTF8
            check_disk = {
                'name': str.replace(disk.display_name, '/dev/', '').decode('utf-8'),
                'free': text.convert_byte(disk.free),
                'total': text.convert_byte(disk.size),
                'percent': int(round(disk.used, 0) * 100 / int(disk.size))
            }

            all_disks.append(check_disk)

        tmpl_vars['disks'] = all_disks

    return tmpl.render(tmpl_vars)
