# -*- coding: utf-8 -*-

"""
    CentralReport - Server module
        This module handles the "/api" route in the webserver
        Gives raw data about the current host and the last check

    https://github.com/CentralReport
"""

import datetime
import flask

from web import _server

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

@_server.app.route('/api/check/date')
def api_check_date():
    tmpl = _server.app.jinja_env.get_template('json/date_check.json')
    tmpl_vars = dict()

    if data.last_check is None:
        tmpl_vars['last_timestamp'] = '0'
        tmpl_vars['last_fulldate'] = 'Never'
    else:
        tmpl_vars['last_timestamp'] = datetime_to_timestamp(data.last_check.date)
        tmpl_vars['last_fulldate'] = data.last_check.date.strftime("%Y-%m-%d %H:%M:%S")

    tmpl_vars['current_timestamp'] = datetime_to_timestamp(datetime.datetime.now())

    try:
        tmpl_vars['checks_interval'] = int(Config.get_config_value('Checks', 'interval'))
    except:
        tmpl_vars['checks_interval'] = int(Config.CR_CONFIG_DEFAULT_CHECKS_INTERVAL)

    return flask.Response(response=tmpl.render(tmpl_vars),
                          status=200,
                          mimetype="application/json")

@_server.app.route('/api/check/full')
def api_check_full():
    tmpl = _server.app.jinja_env.get_template('json/full_check.json')
    tmpl_vars = dict()

    if data.last_check is None:
        tmpl_vars['last_timestamp'] = '0'
        tmpl_vars['last_fulldate'] = 'Never'
    else:
        tmpl_vars['last_timestamp'] = datetime_to_timestamp(data.last_check.date)
        tmpl_vars['last_fulldate'] = data.last_check.date.strftime("%Y-%m-%d %H:%M:%S")
        tmpl_vars['current_timestamp'] = datetime_to_timestamp(datetime.datetime.now())

        # CPU Check information
        if data.last_check.cpu is None:
            tmpl_vars['cpu_check_enabled'] = CHECK_DISABLED
        else:
            tmpl_vars['cpu_check_enabled'] = CHECK_ENABLED

            tmpl_vars['cpu_percent'] = int(data.last_check.cpu.user) + int(data.last_check.cpu.system)
            tmpl_vars['cpu_user'] = data.last_check.cpu.user
            tmpl_vars['cpu_system'] = data.last_check.cpu.system

            if int(Config.get_config_value('Alerts', 'cpu_alert')) <= int(tmpl_vars['cpu_percent']):
                tmpl_vars['cpu_state'] = STATE_ALERT
            elif int(Config.get_config_value('Alerts', 'cpu_warning')) <= int(tmpl_vars['cpu_percent']):
                tmpl_vars['cpu_state'] = STATE_WARNING
            else:
                tmpl_vars['cpu_state'] = STATE_OK

        # Memory check information
        if data.last_check.memory is None:
            tmpl_vars['memory_check_enabled'] = CHECK_DISABLED
        else:
            tmpl_vars['memory_check_enabled'] = CHECK_ENABLED

            tmpl_vars['memory_percent'] = ((int(data.last_check.memory.total) - int(
                data.last_check.memory.free)) * 100) / int(data.last_check.memory.total)
            tmpl_vars['memory_free'] = text.convert_byte(data.last_check.memory.free)
            tmpl_vars['memory_total'] = text.convert_byte(data.last_check.memory.total)
            tmpl_vars['memory_used'] = text.convert_byte(
                float(data.last_check.memory.total) - float(data.last_check.memory.free))

            if int(tmpl_vars['memory_percent']) >= int(Config.get_config_value('Alerts', 'memory_alert')):
                tmpl_vars['memory_state'] = STATE_ALERT
            elif int(tmpl_vars['memory_percent']) >= int(Config.get_config_value('Alerts', 'memory_warning')):
                tmpl_vars['memory_state'] = STATE_WARNING
            else:
                tmpl_vars['memory_state'] = STATE_OK

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
                        tmpl_vars['swap_state'] = STATE_ALERT
                    elif int(tmpl_vars['swap_percent']) >= int(Config.get_config_value('Alerts', 'swap_warning')):

                        tmpl_vars['swap_state'] = STATE_WARNING
                    else:
                        tmpl_vars['swap_state'] = STATE_OK
                else:
                    tmpl_vars['swap_state'] = STATE_OK
            else:

                # No swap available on this host
                tmpl_vars['swap_configuration'] = 'undefined'

        # Load average
        if data.last_check.load is None:
            tmpl_vars['load_check_enabled'] = CHECK_DISABLED
        else:
            tmpl_vars['load_check_enabled'] = CHECK_ENABLED
            tmpl_vars['load_last_one'] = data.last_check.load.last1m
            tmpl_vars['load_percent'] = (float(data.last_check.load.last1m) * 100) / int(
                cr.host.get_current_host().cpu_count)

            if int(tmpl_vars['load_percent']) >= int(Config.get_config_value('Alerts', 'load_alert')):
                tmpl_vars['load_state'] = STATE_ALERT
            elif int(tmpl_vars['load_percent']) >= int(Config.get_config_value('Alerts', 'load_warning')):
                tmpl_vars['load_state'] = STATE_WARNING
            else:
                tmpl_vars['load_state'] = STATE_OK

            tmpl_vars['uptime_full_text'] = text.convert_seconds_to_phrase_time(
                int(data.last_check.load.uptime))
            tmpl_vars['uptime_seconds'] = text.add_number_separators(str(data.last_check.load.uptime))
            tmpl_vars['start_date'] = datetime.datetime.fromtimestamp(
                datetime_to_timestamp(data.last_check.date) - int(
                    data.last_check.load.uptime)).strftime("%Y-%m-%d %H:%M:%S")

    return flask.Response(response=tmpl.render(tmpl_vars),
                          status=200,
                          mimetype="application/json")

@_server.app.route('/api/check/disks')
def api_check_disk():
    tmpl = _server.app.jinja_env.get_template('blocks/disks.block.tpl')
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
