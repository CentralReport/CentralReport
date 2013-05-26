# -*- coding: utf-8 -*-

"""
    CentralReport - Online module
        Contains all classes and functions used for the interaction with the Online server
        Please see http://centralreport.net

    https://github.com/CentralReport
"""

import json
import os.path

from jinja2 import Environment, FileSystemLoader

from cr import data
from cr.errors import OnlineError
from cr import log
from cr.utils import web


# Main routes. Use the HATEOAS concept (http://en.wikipedia.org/wiki/HATEOAS).
# They are empty when CR is starting, they will be gotten dynamically from the server.
route_user_check = 'http://centralreport.net/api/users/%key%'
route_host_check = ''
route_host_add = ''
route_checks_add = ''

user_key = None
host_uuid = None

jinja_env = None  # jinja2.Environment object used to generate JSON output for the webservices.


def initialize_online():
    """
        [WIP] Initializes the connection with the CentralReport Online server
    """

    global jinja_env
    global route_user_check
    global route_host_check
    global route_host_add
    global route_checks_add

    if jinja_env is None:
        current_dir = os.path.dirname(os.path.abspath(__file__))
        jinja_env = Environment(loader=FileSystemLoader(os.path.join(current_dir, 'static/online/')))

    if route_user_check == '':
        raise ValueError('The user check route is unknown!')

    if route_host_check == '':
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

    if route_checks_add == '':
        log.log_warning('Unable to setup the communication with CentralReport Online. Please check previous logs.')
        return False

    return True


def check_user_key():
    """
        [WIP] Checks if the 'User token' is valid on the online server
    """

    global route_user_check
    global route_host_check
    global route_host_add

    route_user_check = route_user_check.replace('%key%', user_key)
    ws_user = web.send_data(web.METHOD_GET, route_user_check, None, None)

    if ws_user.code == 404:
        raise OnlineError(1, 'The key %s is not a valid key on the remote server!' % user_key)
    elif ws_user.code != 200:
        raise OnlineError(2, 'The server has returned a unknown response. Code: %s' % ws_user.code)
    else:
        # This key seems valid! Getting all routes available with HATEOAS
        try:
            remote_json = json.loads(ws_user.text)
            route_host_check = remote_json['links']['hosts']
            route_host_add = remote_json['links']['addHost']
        except:
            route_host_check = ''
            route_host_add = ''
            raise OnlineError(3, 'Error reading the JSON returned by the server!')

    return True


def check_host():
    """
        [WIP] Checks if the host is registered on the online server
    """

    global route_user_check
    global route_host_check
    global route_checks_add

    if route_host_check == '':
        raise ValueError('The host route is unknown!')

    if route_host_check != '':
        # We can now check if the current host is registered on the remote server
        route_host_check = route_host_check.replace('%key%', user_key)
        route_host_check = route_host_check.replace('%uuid%', host_uuid)
        ws_host = web.send_data(web.METHOD_GET, route_host_check, None, None)

        if ws_host.code == 401:
            route_checks_add = ''
            raise OnlineError(1, 'This host must be validated on CentralReport Online')
        elif ws_host.code == 200:
            log.log_info('Host registered on the remote server')

            try:
                remote_json = json.loads(ws_host.text)
                route_checks_add = remote_json['links']['checks']
            except:
                log.log_error()
                raise OnlineError(2, 'Error reading the JSON returned by the remote server!')

        elif ws_host.code == 404:
            return False

    return True


def register_host():
    """
        [WIP] Registers the current host on the online server
    """

    global jinja_env
    global route_host_add
    global route_checks_add

    if data.host_info is None:
        raise ValueError('Host data not available!')

    if route_host_add == '':
        raise ValueError('The host route is unknown!')

    route_host_add = route_host_add.replace('%key%', user_key)

    log.log_debug('Generating the JSON template...')
    template = jinja_env.get_template('host_registration.json')
    json_vars = dict()
    json_vars['uuid'] = host_uuid

    host_json = template.render(json_vars)
    log.log_debug(host_json)

    ws_host_registration = web.send_data(web.METHOD_POST, route_host_add, host_json)

    if ws_host_registration.code == 200:
        log.log_info('Host registered! Waiting for user approval.')
        route_checks_add = ''
    elif ws_host_registration.code == 400:
        raise OnlineError(1, 'Bad request registering the host on CentralReport Online.')
    elif ws_host_registration.code == 409:
        log.log_info('Host already registered on CentralReport Online!')

    return True


def send_check():
    """
        [WIP] Sends the last check to the online server
    """

    global route_checks_add

    if data.last_check is None:
        raise ValueError('No check available!')

    if route_checks_add == '':
        raise ValueError('The Checks route is unknown!')

    if initialize_online() is False:
        raise OnlineError(1, 'Wrong configuration for CentralReport Online')

    log.log_debug('Sending the last check to CentralReport Online...')

    route_checks_add = route_checks_add.replace('%key%', user_key)
    route_checks_add = route_checks_add.replace('%uuid%', host_uuid)

    log.log_debug('Generating the JSON template...')
    template = jinja_env.get_template('send_checks.json')
    json_vars = dict()

    check_json = template.render(json_vars)
    log.log_debug(check_json)

    ws_checks = web.send_data(web.METHOD_POST, route_checks_add, check_json)

    if ws_checks.code == 400:
        raise OnlineError(1, 'Data refused by the remote server: bad data')
    elif ws_checks.code == 404:
        raise OnlineError(2, 'Wrong KEY or UUID!')
    elif ws_checks.code == 409:
        raise OnlineError(3, 'Check already sent!')
    elif ws_checks.code != 200:
        raise OnlineError(4, 'Unkown answer code %s!' % ws_checks.code)

    log.log_info('Check sent successfully!')
    return True
