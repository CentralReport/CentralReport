# -*- coding: utf-8 -*-

"""
    CentralReport - Server module
        This module handles the "/api" route in the webserver
        Gives raw data about the current host and the last check

    https://github.com/CentralReport
"""

import datetime

import flask

from cr.web import server
from cr import data
import cr.host
from cr.utils.date import datetime_to_timestamp
from cr.utils import text
from cr.tools import Config


STATE_ALERT = 'alert'
STATE_OK = 'ok'
STATE_WARNING = 'warning'

CHECK_ENABLED = 'True'
CHECK_DISABLED = 'False'


@server.app.route('/api/checks')
def api_check():
    """
    Entry point of /api/checks
    @return: flask.Response
    """
    tmpl = server.app.jinja_env.get_template('json/checks.json')
    tmpl_vars = dict()

    # Date and system status
    tmpl_vars['last_timestamp'] = datetime_to_timestamp(data.last_check.date)
    tmpl_vars['current_timestamp'] = datetime_to_timestamp(datetime.datetime.now())
    try:
        tmpl_vars['checks_interval'] = int(Config.get_config_value('Checks', 'interval'))
    except NameError:
        tmpl_vars['checks_interval'] = int(Config.CR_CONFIG_DEFAULT_CHECKS_INTERVAL)

    # Uptime
    tmpl_vars['uptime_seconds'] = data.last_check.load.uptime
    tmpl_vars['boot_date'] = datetime_to_timestamp(data.last_check.date) - int(data.last_check.load.uptime)

    # CPU
    tmpl_vars = _get_cpu_info(tmpl_vars)
    tmpl_vars = _get_memory_info(tmpl_vars)
    tmpl_vars = _get_swap_info(tmpl_vars)
    tmpl_vars = _get_load_info(tmpl_vars)


    return flask.Response(response=tmpl.render(tmpl_vars),
                          status=200,
                          mimetype="application/json")


@server.app.route('/api/host')
def api_host():
    """
    Entry point of /api/host
    @return: flask.Response
    """

    tmpl = server.app.jinja_env.get_template('json/host.json')
    tmpl_vars = dict()
    tmpl_vars['hostname'] = cr.host.get_current_host().hostname
    tmpl_vars['os_name'] = cr.host.get_current_host().os_name
    tmpl_vars['os_version'] = cr.host.get_current_host().os_version
    tmpl_vars['architecture'] = cr.host.get_current_host().architecture
    tmpl_vars['cpu_count'] = cr.host.get_current_host().cpu_count
    tmpl_vars['cpu_model'] = cr.host.get_current_host().cpu_model
    tmpl_vars['kernel_name'] = cr.host.get_current_host().kernel_name
    tmpl_vars['kernel_version'] = cr.host.get_current_host().kernel_version
    tmpl_vars['uuid'] = cr.host.get_current_host().uuid

    return flask.Response(response=tmpl.render(tmpl_vars),
                          status=200,
                          mimetype="application/json")

def _get_cpu_info(tmpl_vars):
    """
    Gets template variables filled with the last CPU check
    @param tmpl_vars:
    @return: Dictionary of template variables
    """
    tmpl_vars['cpu_user'] = data.last_check.cpu.user
    tmpl_vars['cpu_system'] = data.last_check.cpu.system
    tmpl_vars['cpu_idle'] = data.last_check.cpu.idle

    cpu_percent = int(data.last_check.cpu.user) + int(data.last_check.cpu.system)
    if int(Config.get_config_value('Alerts', 'cpu_alert')) <= cpu_percent:
        tmpl_vars['cpu_state'] = STATE_ALERT
    elif int(Config.get_config_value('Alerts', 'cpu_warning')) <= cpu_percent:
        tmpl_vars['cpu_state'] = STATE_WARNING
    else:
        tmpl_vars['cpu_state'] = STATE_OK

    return tmpl_vars


def _get_memory_info(tmpl_vars):
    """
    Gets template variables filled with the last memory check
    @param tmpl_vars:
    @return: Dictionary of template variables
    """
    tmpl_vars['memory_total'] = data.last_check.memory.total
    tmpl_vars['memory_free'] = data.last_check.memory.free
    tmpl_vars['memory_active'] = data.last_check.memory.active
    tmpl_vars['memory_inactive'] = data.last_check.memory.inactive
    tmpl_vars['memory_resident'] = data.last_check.memory.resident

    memory_percent = ((int(data.last_check.memory.total) - int(data.last_check.memory.free)) * 100) / int(data.last_check.memory.total)
    if memory_percent >= int(Config.get_config_value('Alerts', 'memory_alert')):
        tmpl_vars['memory_state'] = STATE_ALERT
    elif memory_percent >= int(Config.get_config_value('Alerts', 'memory_warning')):
        tmpl_vars['memory_state'] = STATE_WARNING
    else:
        tmpl_vars['memory_state'] = STATE_OK

    return tmpl_vars


def _get_swap_info(tmpl_vars):
    """
    Gets template variables filled with the last swap check
    @param tmpl_vars:
    @return: Dictionary of template variables
    """
    if int(data.last_check.memory.swap_size) != 0:
        tmpl_vars['swap_used'] = data.last_check.memory.swap_used
        tmpl_vars['swap_free'] = data.last_check.memory.swap_free
        tmpl_vars['swap_total'] = data.last_check.memory.swap_size

        # On Mac, the swap is unlimited (only limited by the available hard drive size)
        if data.last_check.memory.swap_size == data.last_check.memory.total:
            tmpl_vars['swap_configuration'] = 'unlimited'
        else:
            tmpl_vars['swap_configuration'] = 'limited'

        swap_percent = int(data.last_check.memory.swap_used) * 100 / int(data.last_check.memory.swap_size)
        if swap_percent >= int(Config.get_config_value('Alerts', 'swap_alert')):
            tmpl_vars['swap_state'] = STATE_ALERT
        elif swap_percent >= int(Config.get_config_value('Alerts', 'swap_warning')):

            tmpl_vars['swap_state'] = STATE_WARNING
        else:
            tmpl_vars['swap_state'] = STATE_OK
    else:
        # No swap available on this host
        tmpl_vars['swap_configuration'] = 'undefined'

    return tmpl_vars


def _get_load_info(tmpl_vars):
    """
    Gets template variables filled with the last load average check
    @param tmpl_vars:
    @return: Dictionary of template variables
    """
    tmpl_vars['load_1m'] = data.last_check.load.last1m
    tmpl_vars['load_5m'] = data.last_check.load.last5m
    tmpl_vars['load_15m'] = data.last_check.load.last15m

    load_percent = (float(data.last_check.load.last1m) * 100) / int(cr.host.get_current_host().cpu_count)
    if load_percent >= int(Config.get_config_value('Alerts', 'load_alert')):
        tmpl_vars['load_state'] = STATE_ALERT
    elif load_percent >= int(Config.get_config_value('Alerts', 'load_warning')):
        tmpl_vars['load_state'] = STATE_WARNING
    else:
        tmpl_vars['load_state'] = STATE_OK

    return tmpl_vars


@server.app.route('/api/check/disks')
def api_check_disk():
    tmpl = server.app.jinja_env.get_template('blocks/disks.block.tpl')
    tmpl_vars = dict()

    if data.last_check.disks is not None:
        all_disks = []

        for disk in data.last_check.disks.disks:
            check_disk = {
                'name': str.replace(disk.display_name, '/dev/', '').decode('utf-8'),
                'free': text.convert_byte(disk.free),
                'total': text.convert_byte(disk.size),
                'percent': int(round(disk.used, 0) * 100 / int(disk.size))
            }

            all_disks.append(check_disk)

        tmpl_vars['disks'] = all_disks

    return flask.Response(response=tmpl.render(tmpl_vars),
                          status=200,
                          mimetype="application/json")
