# -*- coding: utf-8 -*-

"""
    CentralReport - Server module
        Manages internal web server

    https://github.com/CentralReport
"""

import threading

from flask import Flask
from web import _server
_server.app = Flask(__name__)

from cr.tools import Config
from web import api
from web import pages


class WebServer(threading.Thread):

    def __init__(self):
        """
            Manages the small webserver.
        """

        threading.Thread.__init__(self)
        self.start()

    def run(self):
        """
            Starts the web server.
        """

        _server.app.run(
            host=Config.get_config_value('Webserver', 'interface'),
            port=int(Config.get_config_value('Webserver', 'port'))
        )
