# CentralReport - Indev version
# Project by Charles-Emmanuel CAMUS - Avril 2012

import os, cherrypy, threading
from mako.lookup import TemplateLookup
from webHomePages import WebHomePages
from utils.config import ConfigGetter

#class WebServer(threading.Thread):
class WebServer():

    current_dir = os.path.dirname(os.path.abspath(__file__))
    lookup = TemplateLookup(directories=[os.path.join(current_dir,'tpl')])

    #def run(self):
    def __init__(self):
        """
        Manage the small webserver
        """

        # Start home
        #cherrypy.tree.graft(WebHomePages(), '/')

        # Update the configuration...
        cherrypy.config.update({'server.socket_host': ConfigGetter.config_webserver_interface, 'server.socket_port': ConfigGetter.config_webserver_port})
        cherrypy.config.update({'tools.staticdir.root' : WebServer.current_dir})

        # Serving static content
        confStaticContent = {'/statics' : {'tools.staticdir.dir': 'statics','tools.staticdir.on': True},
                             '/css' : {'tools.staticdir.dir': 'css','tools.staticdir.on': True},
                             '/img' : {'tools.staticdir.dir': 'img','tools.staticdir.on': True},
                             '/js' : {'tools.staticdir.dir': 'js','tools.staticdir.on': True}}

        cherrypy.tree.mount(WebHomePages(self.lookup), '/',confStaticContent)

        # Go go go!
        cherrypy.engine.start()
        cherrypy.engine.block()