# -*- coding: utf-8 -*-

"""
    CentralReport - Server module
        Manages internal web server

    https://github.com/CentralReport
"""

import threading

from flask import Flask

from cr.tools import Config

#: @type app: Flask
app = Flask(__name__)


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

        app.run(
            host=Config.get_config_value('Webserver', 'interface'),
            port=int(Config.get_config_value('Webserver', 'port'))
        )
