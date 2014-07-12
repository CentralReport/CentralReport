# -*- coding: utf-8 -*-

"""
    CentralReport - Server module
        This module handles the "/api" route in the webserver
        Gives raw data about the current host and the last check

    https://github.com/CentralReport
"""

import datetime
import json

import flask

from cr.web import server
from cr import data
import cr.host
from cr.utils.date import datetime_to_timestamp
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
    try:
        interval = int(Config.get_config_value('Checks', 'interval'))
    except NameError:
        interval = int(Config.CR_CONFIG_DEFAULT_CHECKS_INTERVAL)

    vars = {
        'date': datetime_to_timestamp(data.last_check.date),
        'interval': interval,
        'system': {
            'timestamp': datetime_to_timestamp(datetime.datetime.now())
        },
        'uptime': {
            'seconds': data.last_check.load.uptime,
            'boot_date': datetime_to_timestamp(data.last_check.date) - int(data.last_check.load.uptime)
        },
        'cpu': _get_cpu_info(),
        'memory': _get_memory_info(),
        'swap': _get_swap_info(),
        'load': _get_load_info(),
        'disks': _get_disks_info()
    }

    return flask.Response(response=json.dumps(vars),
                          status=200,
                          mimetype="application/json")


@server.app.route('/api/host')
def api_host():
    """
    Entry point of /api/host
    @return: flask.Response
    """

    vars = {
        'hostname': cr.host.get_current_host().hostname,
        'os_name': cr.host.get_current_host().os_name,
        'os_version': cr.host.get_current_host().os_version,
        'os_family': cr.host.get_current_host().family,
        'os_variant': cr.host.get_current_host().variant,
        'architecture': cr.host.get_current_host().architecture,
        'cpu_count': cr.host.get_current_host().cpu_count,
        'cpu_model': cr.host.get_current_host().cpu_model,
        'kernel_name': cr.host.get_current_host().kernel_name,
        'kernel_version': cr.host.get_current_host().kernel_version,
        'uuid': cr.host.get_current_host().uuid
    }

    return flask.Response(response=json.dumps(vars),
                          status=200,
                          mimetype="application/json")

def _get_cpu_info():
    """
    Gets template variables filled with the last CPU check
    @return: Dictionary of template variables
    """

    vars = {
        'percent': int(data.last_check.cpu.user) + int(data.last_check.cpu.system),
        'user': data.last_check.cpu.user,
        'system': data.last_check.cpu.system,
        'idle': data.last_check.cpu.idle
    }

    if int(Config.get_config_value('Alerts', 'cpu_alert')) <= vars['percent']:
        vars['state'] = STATE_ALERT
    elif int(Config.get_config_value('Alerts', 'cpu_warning')) <= vars['percent']:
        vars['state'] = STATE_WARNING
    else:
        vars['state'] = STATE_OK

    return vars


def _get_memory_info():
    """
    Gets template variables filled with the last memory check
    @return: Dictionary of template variables
    """

    vars = {
        'percent': (int(data.last_check.memory.total) - int(data.last_check.memory.free)) * 100 / int(data.last_check.memory.total),
        'total': data.last_check.memory.total,
        'active': data.last_check.memory.active,
        'inactive': data.last_check.memory.inactive,
        'resident': data.last_check.memory.resident,
        'free': data.last_check.memory.free
    }

    if vars['percent'] >= int(Config.get_config_value('Alerts', 'memory_alert')):
        vars['sate'] = STATE_ALERT
    elif vars['percent'] >= int(Config.get_config_value('Alerts', 'memory_warning')):
        vars['state'] = STATE_WARNING
    else:
        vars['state'] = STATE_OK

    return vars


def _get_swap_info():
    """
    Gets template variables filled with the last swap check
    @return: Dictionary of template variables
    """

    vars = dict()

    if int(data.last_check.memory.swap_size) != 0:
        # On Mac, the swap is unlimited (only limited by the available hard drive size)
        if data.last_check.memory.swap_size == data.last_check.memory.total:
            vars['configuration'] = 'unlimited'
        else:
            vars['configuration'] = 'limited'

        vars['percent'] = int(data.last_check.memory.swap_used) * 100 / int(data.last_check.memory.swap_size)
        vars['used'] = data.last_check.memory.swap_used
        vars['free'] = data.last_check.memory.swap_free
        vars['total'] = data.last_check.memory.swap_size

        if vars['percent'] >= int(Config.get_config_value('Alerts', 'swap_alert')):
            vars['state'] = STATE_ALERT
        elif vars['percent'] >= int(Config.get_config_value('Alerts', 'swap_warning')):
            vars['state'] = STATE_WARNING
        else:
            vars['state'] = STATE_OK
    else:
        # No swap available on this host
        vars['configuration'] = 'undefined'

    return vars


def _get_load_info():
    """
    Gets template variables filled with the last load average check
    @return: Dictionary of template variables
    """

    vars = {
        '1m': data.last_check.load.last1m,
        '5m': data.last_check.load.last5m,
        '15m': data.last_check.load.last15m
    }

    load_percent = (float(data.last_check.load.last1m) * 100) / int(cr.host.get_current_host().cpu_count)
    if load_percent >= int(Config.get_config_value('Alerts', 'load_alert')):
        vars['state'] = STATE_ALERT
    elif load_percent >= int(Config.get_config_value('Alerts', 'load_warning')):
        vars['state'] = STATE_WARNING
    else:
        vars['state'] = STATE_OK

    return vars


def _get_disks_info():
    """
    Gets template variables filled with disks data
    @return: Dictionary of template variables
    """
    all_disks = []
    if data.last_check.disks is not None:
        for disk in data.last_check.disks.disks:
            check_disk = {
                'name': disk.name.decode('utf-8'),
                'display_name': disk.display_name.decode('utf-8'),
                'uuid': disk.uuid,
                'used': disk.used,
                'free': disk.free,
                'size': disk.size,
                'percent': int(round(disk.used, 0) * 100 / int(disk.size))
            }

            if check_disk['percent'] >= int(Config.get_config_value('Alerts', 'disk_alert')):
                check_disk['state'] = STATE_ALERT
            elif check_disk['percent'] >= int(Config.get_config_value('Alerts', 'disk_warning')):
                check_disk['state'] = STATE_WARNING
            else:
                check_disk['state'] = STATE_OK

            all_disks.append(check_disk)

    return all_disks
