# -*- coding: utf-8 -*-

"""
    CentralReport - Online module
        Contains all classes and functions used for the interaction with the Online server
        Please see http://centralreport.net

    https://github.com/miniche/CentralReport/
"""

import json

from cr.utils import web
from cr import log

# Main routes. Use the HATEOAS concept (http://en.wikipedia.org/wiki/HATEOAS).
# They are empty when CR is starting, they will be gotten dynamically from the server.
route_user_check = 'http://centralreport.net/api/users/%key%'
route_host_check = ''
route_host_add = ''
route_checks_add = ''

user_key = None
host_uuid = None


def check_key():
    """
        [WIP] Checks if the 'User token' is valid on the online server
    """

    global route_user_check
    global route_host_check
    global route_host_add

    route_user_check = route_user_check.replace('%key%', user_key)
    ws_user = web.send_data(web.METHOD_GET, route_user_check, None, None)

    if ws_user.code == 404:
        log.log_error('The key %s is not a valid key on the remote server!' % user_key)
    elif ws_user.code != 200 or ws_user.headers.count('application/json') == 0:
        log.log_error('The server has returned a unknown response.')
        log.log_error('Code: %s - Content: %s' % (ws_user.code, ws_user.text))
    else:
        # This key seems valid! Getting all routes available with HATEOAS
        try:
            remote_json = json.loads(ws_user.text)
            route_host_check = remote_json['links']['hosts']
            route_host_add = remote_json['links']['addHost']
        except:
            log.log_error('Error reading the JSON returned by the remote server!')
            route_host_check = ''
            route_host_add = ''


def check_host():
    """
        [WIP] Checks if the host is registered on the online server
    """

    global route_user_check
    global route_host_check
    global route_checks_add

    if route_host_check != '':
        # We can now check if the current host is registered on the remote server
        route_host_check = route_host_check.replace('%key%', user_key)
        route_host_check = route_host_check.replace('%uuid%', host_uuid)
        ws_host = web.send_data(web.METHOD_GET, route_host_check, None, None)

        if ws_host.code == 401:
            log.log_info('Please validate this host on the remote server!')
            route_checks_add = ''
        elif ws_host.code == 200:
            log.log_info('Host registered on the remote server')

            try:
                remote_json = json.loads(ws_host.text)
                route_checks_add = remote_json['links']['checks']
            except:
                log.log_error('Error reading the JSON returned by the remote server!')
                route_checks_add = ''

        elif ws_host.code == 404:
            log.log_info('Host not registered. Registering this host the the remote server...')


def register_host(host_json):
    """
        [WIP] Registers the current host on the online server
    """

    global route_host_add
    global route_checks_add

    route_host_add = route_host_add.replace('%key%', user_key)

    ws_host_registration = web.send_data(web.METHOD_POST, route_host_add, host_json)

    if ws_host_registration.code == 200:
        log.log_info('Host registered! Waiting for user approval.')
        route_checks_add = ''
    elif ws_host_registration.code == 400:
        log.log_error('Bad request registering the host on CentralReport Online.')
    elif ws_host_registration.code == 409:
        log.log_info('Host already registered on CentralReport Online!')


def send_check(check_json):
    """
        [WIP] Sends a check to the online server
    """

    global route_checks_add

    log.log_debug('Sending the last check to CentralReport Online...')

    route_checks_add = route_checks_add.replace('%key%', user_key)
    route_checks_add = route_checks_add.replace('%uuid%', host_uuid)

    ws_checks = web.send_data(web.METHOD_POST, route_checks_add, check_json)

    if ws_checks.code == 200:
        log.log_info('Check sent successfully!')
    elif ws_checks.code == 400:
        log.log_error('Incorrect data!')
    elif ws_checks.code == 404:
        log.log_error('Wrong KEY or UUID!')
    elif ws_checks.code == 409:
        log.log_error('Check already sent!')
    else:
        log.log_error('Unkown answer code %s!' % ws_checks.code)
