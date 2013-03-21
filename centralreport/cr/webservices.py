# -*- coding: utf-8 -*-

# CentralReport - Indev version
# Project by Charles-Emmanuel CAMUS - Avril 2012

#
# Warning: Not used. Only for testing purposes.
#


import json
import datetime
from sys import path as sysPath
from os import path as osPath

sysPath.insert(0, osPath.abspath(__file__ + '/../../libs/requests-1.1.0.zip'))

import requests
from cr.tools import Config
from cr.utils.date import datetime_to_timestamp
from cr.utils import text
import cr.threads


class WebServices:
    """
        PS: This class is not used for the moment.
        It has been created for testing purpose only.
    """

    @staticmethod
    def send_disks_check():

        if cr.threads.Checks.last_check_disk is not None:
            all_disks = []

            for disk in cr.threads.Checks.last_check_disk.checks:
                check_disk = {
                    'free': text.convert_byte(disk.free),
                    'total': text.convert_byte(disk.size),
                    'percent': int(round(disk.used, 0) * 100 / int(disk.size))
                }

                all_disks.append(check_disk)

                url = "http://httpbin.org/post"  # Will be replaced with CentralReport Online IP
                data = {"server":
                            {"name": cr.threads.Checks.hostEntity.hostname,
                             "diskcheck":
                                 {"disk1":
                                      [
                                          all_disks
                                      ]
                                 }
                            }
                }
                headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
                r = requests.post(url, data=json.dumps(data), headers=headers)
                print r.text

    @staticmethod
    def send_full_check():

        tmpl_vars = dict()

        if cr.threads.Checks.last_check_date is None:
            tmpl_vars['last_timestamp'] = '0'
            tmpl_vars['last_fulldate'] = 'Never'
        else:
            tmpl_vars['last_timestamp'] = datetime_to_timestamp(cr.threads.Checks.last_check_date)
            tmpl_vars['last_fulldate'] = cr.threads.Checks.last_check_date.strftime("%Y-%m-%d %H:%M:%S")
            tmpl_vars['current_timestamp'] = datetime_to_timestamp(datetime.datetime.now())

            # CPU Check informations
            if cr.threads.Checks.last_check_cpu is None:
                tmpl_vars['cpu_check_enabled'] = 'False'
            else:
                tmpl_vars['cpu_check_enabled'] = 'True'

                tmpl_vars['cpu_percent'] = int(cr.threads.Checks.last_check_cpu.user) + int(
                    cr.threads.Checks.last_check_cpu.system)
                tmpl_vars['cpu_user'] = cr.threads.Checks.last_check_cpu.user
                tmpl_vars['cpu_system'] = cr.threads.Checks.last_check_cpu.system

                if int(Config.get_config_value('Alerts', 'cpu_alert')) <= int(tmpl_vars['cpu_percent']):
                    tmpl_vars['cpu_state'] = "alert"
                elif int(Config.get_config_value('Alerts', 'cpu_warning')) <= int(tmpl_vars['cpu_percent']):
                    tmpl_vars['cpu_state'] = "warning"
                else:
                    tmpl_vars['cpu_state'] = 'ok'

            # Memory check informations
            if cr.threads.Checks.last_check_memory is None:
                tmpl_vars['memory_check_enabled'] = 'False'
            else:
                tmpl_vars['memory_check_enabled'] = "True"

                tmpl_vars['memory_percent'] = ((int(cr.threads.Checks.last_check_memory.total) - int(
                    cr.threads.Checks.last_check_memory.free)) * 100) / int(cr.threads.Checks.last_check_memory.total)
                tmpl_vars['memory_free'] = text.convert_byte(cr.threads.Checks.last_check_memory.free)
                tmpl_vars['memory_total'] = text.convert_byte(cr.threads.Checks.last_check_memory.total)
                tmpl_vars['memory_used'] = text.convert_byte(
                    float(cr.threads.Checks.last_check_memory.total) - float(cr.threads.Checks.last_check_memory.free))

                if int(tmpl_vars['memory_percent']) >= int(Config.get_config_value('Alerts', 'memory_alert')):
                    tmpl_vars['memory_state'] = "alert"
                elif int(tmpl_vars['memory_percent']) >= int(Config.get_config_value('Alerts', 'memory_warning')):
                    tmpl_vars['memory_state'] = "warning"
                else:
                    tmpl_vars['memory_state'] = 'ok'

                # Last: swap stats
                if 0 != int(cr.threads.Checks.last_check_memory.swap_size):
                    tmpl_vars['swap_percent'] = int(cr.threads.Checks.last_check_memory.swap_used) * 100 / int(
                        cr.threads.Checks.last_check_memory.swap_size)
                    tmpl_vars['swap_used'] = text.convert_byte(cr.threads.Checks.last_check_memory.swap_used)

                    tmpl_vars['swap_free'] = text.convert_byte(cr.threads.Checks.last_check_memory.swap_free)
                    tmpl_vars['swap_size'] = text.convert_byte(cr.threads.Checks.last_check_memory.swap_size)

                    # On Mac, the swap is unlimited (only limited by the available hard drive size)
                    if cr.threads.Checks.last_check_memory.swap_size == cr.threads.Checks.last_check_memory.total:

                        tmpl_vars['swap_configuration'] = 'unlimited'
                    else:
                        tmpl_vars['swap_configuration'] = 'limited'

                    if isinstance(tmpl_vars['swap_percent'], int):
                        if int(tmpl_vars['swap_percent']) >= int(Config.get_config_value('Alerts', 'swap_alert')):
                            tmpl_vars['swap_state'] = 'alert'
                        elif int(tmpl_vars['swap_percent']) >= int(Config.get_config_value('Alerts', 'swap_warning')):

                            tmpl_vars['swap_state'] = 'warning'
                        else:
                            tmpl_vars['swap_state'] = 'ok'
                    else:
                        tmpl_vars['swap_state'] = 'ok'
                else:

                    # No swap available on this host
                    tmpl_vars['swap_configuration'] = 'undefined'

            # Load average
            if cr.threads.Checks.last_check_loadAverage is None:
                tmpl_vars['load_check_enabled'] = 'False'
            else:
                tmpl_vars['load_check_enabled'] = "True"

                tmpl_vars['load_last_one'] = cr.threads.Checks.last_check_loadAverage.last1m
                tmpl_vars['load_percent'] = (float(cr.threads.Checks.last_check_loadAverage.last1m) * 100) / int(
                    cr.threads.Checks.hostEntity.cpu_count)

                if int(tmpl_vars['load_percent']) >= int(Config.get_config_value('Alerts', 'load_alert')):
                    tmpl_vars['load_state'] = "alert"
                elif int(tmpl_vars['load_percent']) >= int(Config.get_config_value('Alerts', 'load_warning')):
                    tmpl_vars['load_state'] = "warning"
                else:
                    tmpl_vars['load_state'] = 'ok'

                tmpl_vars['uptime_full_text'] = text.convert_seconds_to_phrase_time(
                    int(cr.threads.Checks.last_check_loadAverage.uptime))
                tmpl_vars['uptime_seconds'] = text.add_number_separators(
                    str(cr.threads.Checks.last_check_loadAverage.uptime))
                tmpl_vars['start_date'] = datetime.datetime.fromtimestamp(
                    datetime_to_timestamp(cr.threads.Checks.last_check_date) - int(
                        cr.threads.Checks.last_check_loadAverage.uptime)).strftime("%Y-%m-%d %H:%M:%S")

        url = "http://httpbin.org/post"  # Will be replaced with CentralReport Online IP
        data = {"server":
                    {'name': cr.threads.Checks.hostEntity.hostname, 'Infos': {
                        json.dumps(tmpl_vars)
                    }}
        }
        headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
        r = requests.post(url, data=json.dumps(data), headers=headers)
        print r.text
