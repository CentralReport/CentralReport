# CentralReport - Indev version
# Project by Charles-Emmanuel CAMUS - Avril 2012

import os, cherrypy
from mako.template import Template
from mako.lookup import TemplateLookup
from webHomePages import WebHomePages

class WebServer:

    current_dir = os.path.dirname(os.path.abspath(__file__))
    lookup = TemplateLookup(directories=[os.path.join(current_dir,'tpl')])

    def __init__(self):
        """
        Manage the small webserver
        """

        # Start home
        #cherrypy.tree.graft(WebHomePages(), '/')

        # Update the configuration...
        cherrypy.config.update({'server.socket_host': '0.0.0.0', 'server.socket_port': 8080})
        cherrypy.config.update({'tools.staticdir.root' : WebServer.current_dir})

        # Serving static content
        cherrypy.tree.mount(WebHomePages(self.lookup), '/', {'/statics' : {
            'tools.staticdir.dir': 'statics',
            'tools.staticdir.on': True,
            }})

        # Go go go!
        cherrypy.engine.start()
        cherrypy.engine.block()