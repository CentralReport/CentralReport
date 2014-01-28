# -*- coding: utf-8 -*-

"""
    CentralReport - Online module
        Contains all classes and functions interacting with the Online server
        Please see http://centralreport.net

    https://github.com/CentralReport
"""

import json
import os.path

from jinja2 import Environment, FileSystemLoader

from cr import data
from cr.errors import OnlineError, OnlineNotValidated
from cr import host
from cr import log
from cr.utils import text
from cr.utils import web
from cr.tools import Config

# Main routes. Use the HATEOAS concept (http://en.wikipedia.org/wiki/HATEOAS).
# They are empty when CR is starting, they will be gotten dynamically from the server.
# TODO: Use HATEOAS for "route_host_check" when the CentralReport Online API will be updated
route_user_check = 'http://online.centralreport.net/api/users/%key%'
route_host_check = 'http://online.centralreport.net/api/users/%key%/hosts/%uuid%'
route_host_add = ''
route_checks_add = ''

jinja_env = None  # jinja2.Environment object used to generate JSON output for the web services.


def initialize_online():
    """
        Initializes the connection with the CentralReport Online server.
        This function performs all needed actions to check the user and the host status.

        @return: True if the connection with CentralReport Online is established, False otherwise.
    """

    global jinja_env
    global route_user_check
    global route_host_check
    global route_host_add
    global route_checks_add

    log.log_debug('Initializing the connection with CentralReport Online...')

    if jinja_env is None:
        current_dir = os.path.dirname(os.path.abspath(__file__))
        jinja_env = Environment(loader=FileSystemLoader(os.path.join(current_dir, 'static/online/')))

    if route_user_check == '':
        raise ValueError('The user check route is unknown!')

    if route_host_add == '':
        try:
            check_user_key()
        except OnlineError as e:
            log.log_error('Error %s: %s' % (e.code, e.message))
            return False

    if route_checks_add == '':
        try:
            return_check_host = check_host()
        except ValueError as e:
            log.log_error('Error: %s' % e.message)
            return False
        except OnlineError as e:
            log.log_warning('%s: %s' % (e.code, e.message))
            return False

        if return_check_host is False:
            # The host must be registered on the server before sending any check
            try:
                register_host()
            except ValueError as e:
                log.log_error('Error: %s' % e.message)
                return False
            except OnlineError as e:
                log.log_warning('%s: %s' % (e.code, e.message))
                return False

    if route_checks_add == '':
        log.log_warning('Unable to setup the communication with CentralReport Online. Please check previous logs.')
        return False

    return True


def check_user_key():
    """
       Checks whether the 'User key' is valid on the online server.

       @return: True if the 'user key' is valid, raise an OnlineError otherwise
    """

    global route_user_check
    global route_host_check
    global route_host_add

    log.log_info('Checking the user key on CentralReport Online...')

    online_key = Config.get_config_value('Online', 'key')

    if online_key == '':
        raise ValueError('No user key defined!')

    route_user_check = route_user_check.replace('%key%', online_key)
    ws_user = web.send_data(web.METHOD_GET, route_user_check, None, None)

    if ws_user.code == 404:
        raise OnlineError(1, 'The key %s is not a valid key on the remote server!' % online_key)
    elif ws_user.code != 200:
        raise OnlineError(2, 'The server has returned a unknown response. Code: %s' % ws_user.code)
    else:
        # This key seems valid! Getting all routes available with HATEOAS
        try:
            remote_json = json.loads(ws_user.text)
            route_host_add = remote_json['_links']['post_host']['href']
        except:
            route_host_check = ''
            route_host_add = ''
            raise OnlineError(3, 'Error reading the JSON returned by the server!')

    return True


def check_host():
    """
        Checks whether the host is registered on the online server

        @return: True if the current host is registered on the online server, False otherwise.
    """

    global route_user_check
    global route_host_check
    global route_checks_add

    log.log_info('Checking whether this host is registered on CentralReport Online...')

    online_key = Config.get_config_value('Online', 'key')

    if route_host_check == '':
        raise ValueError('The host route is unknown!')

    if route_host_check != '':
        # We can now check if the current host is registered on the remote server
        route_host_check = route_host_check.replace('%key%', online_key)
        route_host_check = route_host_check.replace('%uuid%', Config.get_config_value('General', 'uuid'))
        ws_host = web.send_data(web.METHOD_GET, route_host_check, None, None)

        if ws_host.code == 403:
            route_checks_add = ''
            raise OnlineNotValidated(1, 'This host must be validated on CentralReport Online')
        elif ws_host.code == 200:
            log.log_info('Host registered on the remote server')

            try:
                remote_json = json.loads(ws_host.text)
                route_checks_add = remote_json['_links']['post_checks']['href']
            except:
                log.log_debug(ws_host.text)
                raise OnlineError(2, 'Error reading the JSON returned by the remote server!')

        elif ws_host.code == 404:
            return False

    return True


def register_host():
    """
        Registers the current host on the online server

        @return: True if the current host is registered on the online server successfully.
    """

    global jinja_env
    global route_host_add
    global route_checks_add

    log.log_info('Registering this host on CentralReport Online...')

    if route_host_add == '':
        raise ValueError('The host route is unknown!')

    route_host_add = route_host_add.replace('%key%', Config.get_config_value('Online', 'key'))

    log.log_debug('Generating the JSON template...')
    template = jinja_env.get_template('host_registration.json')

    json_vars = dict()
    json_vars['uuid'] = Config.get_config_value('General', 'uuid')
    json_vars['hostname'] = host.get_current_host().hostname
    json_vars['model'] = host.get_current_host().model
    json_vars['cpu_model'] = host.get_current_host().cpu_model
    json_vars['cpu_count'] = host.get_current_host().cpu_count
    json_vars['os_name'] = host.get_current_host().os_name
    json_vars['os_version'] = host.get_current_host().os_version
    json_vars['kernel_name'] = host.get_current_host().kernel_name
    json_vars['kernel_version'] = host.get_current_host().kernel_version
    json_vars['architecture'] = host.get_current_host().architecture
    json_vars['agent'] = Config.CR_AGENT_NAME
    json_vars['agent_version'] = Config.CR_VERSION
    json_vars['host_type'] = 'host'

    host_json = text.clean(template.render(json_vars))
    log.log_debug(host_json)

    ws_host_registration = web.send_data(web.METHOD_POST, route_host_add, host_json)
    if ws_host_registration.code == 201:
        log.log_info('Host registered! Waiting for user approval.')
        route_checks_add = ''
    elif ws_host_registration.code == 400:
        log.log_debug(ws_host_registration.text)
        raise OnlineError(1, 'Bad request registering the host on CentralReport Online.')
    elif ws_host_registration.code == 409:
        log.log_info('Host already registered on CentralReport Online!')
    elif ws_host_registration.code != 200:
        log.log_debug(ws_host_registration.text)
        raise OnlineError(1, 'The Online server had returned an error registering the host.')

    return True


def send_check():
    """
        Sends the last check to the online server

        @return: True if the last check has been sent.
    """

    global route_checks_add
    global route_host_add

    log.log_debug('Sending the last check to CentralReport Online...')

    if data.last_check is None:
        raise ValueError('No check available!')

    if initialize_online() is False:
        raise OnlineError(1, 'Wrong configuration for CentralReport Online')

    if route_checks_add == '':
        raise ValueError('The Checks route is unknown!')

    log.log_debug('Generating the JSON template...')

    template = jinja_env.get_template('send_checks.json')

    json_vars = dict()
    json_vars['date'] = data.last_check.date.strftime("%Y-%m-%d %H:%M:%S")
    json_vars['load_uptime'] = data.last_check.load.uptime
    json_vars['load_last1m'] = data.last_check.load.last1m
    json_vars['load_last5m'] = data.last_check.load.last5m
    json_vars['load_last15m'] = data.last_check.load.last15m
    json_vars['cpu_idle'] = data.last_check.cpu.idle
    json_vars['cpu_system'] = data.last_check.cpu.system
    json_vars['cpu_user'] = data.last_check.cpu.user
    json_vars['memory_total'] = long(data.last_check.memory.total)
    json_vars['memory_active'] = long(data.last_check.memory.active)
    json_vars['memory_inactive'] = long(data.last_check.memory.inactive)
    json_vars['memory_resident'] = long(data.last_check.memory.resident)
    json_vars['memory_free'] = long(data.last_check.memory.free)
    json_vars['swap_size'] = long(data.last_check.memory.swap_size)
    json_vars['swap_used'] = long(data.last_check.memory.swap_used)
    json_vars['swap_free'] = long(data.last_check.memory.swap_free)

    all_disks = []
    for disk in data.last_check.disks.disks:
        if disk.uuid:
            disk_json = {
                'name': disk.name,
                'display_name': disk.display_name,
                'uuid': disk.uuid,
                'size': long(disk.size),
                'used': long(disk.used),
                'free': long(disk.free)
            }
            all_disks.append(disk_json)
    json_vars['disks'] = all_disks

    check_json = text.clean(template.render(json_vars))
    log.log_debug(check_json)

    ws_checks = web.send_data(web.METHOD_POST, route_checks_add, check_json)
    if ws_checks.code == 400:
        log.log_debug(ws_checks.text)
        raise OnlineError(1, 'Data refused by the remote server')
    elif ws_checks.code == 404:
        log.log_debug(ws_checks.text)
        route_checks_add = ''
        route_host_add = ''
        raise OnlineError(2, 'Wrong KEY or UUID!')
    elif ws_checks.code == 409:
        log.log_debug(ws_checks.text)
        raise OnlineError(3, 'Check already sent!')
    elif ws_checks.code != 201:
        log.log_debug(ws_checks.text)
        raise OnlineError(4, 'Unknown answer code %s!' % ws_checks.code)

    log.log_info('Check sent successfully!')

    return True
