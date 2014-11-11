# -*- coding: utf-8 -*-

"""
    CentralReport - Server module
        This module handles webpages displayed on the user screen

    https://github.com/CentralReport
"""

from flask import redirect

from cr.web import server
import cr.host
from cr.tools import Config


@server.app.route('/')
def index():
    """
        Main entry (http://localhost:port/)
    """
    return redirect("/app")


@server.app.route('/app')
def app():
    tmpl = server.app.jinja_env.get_template('app.tpl')

    tmpl_vars = dict()

    tmpl_vars['hostname'] = cr.host.get_current_host().hostname
    tmpl_vars['os_name'] = cr.host.get_current_host().os_name
    tmpl_vars['os_version'] = cr.host.get_current_host().os_version
    tmpl_vars['CR_version'] = Config.CR_VERSION
    tmpl_vars['CR_version_name'] = Config.CR_VERSION_NAME

    return tmpl.render(tmpl_vars)
