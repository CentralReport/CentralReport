# CentralReport - Indev version
# Project by Charles-Emmanuel CAMUS - Avril 2012

import os, cherrypy, threading,cherrypy._cplogging
from mako.lookup import TemplateLookup
from webHomePages import WebHomePages
from utils.CRConfig import CRConfig

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

        # Register events...
        cherrypy.engine.subscribe('graceful',self.stop)

        # Update the configuration...
        cherrypy.config.update({'server.socket_host': CRConfig.config_webserver_interface, 'server.socket_port': CRConfig.config_webserver_port})
        cherrypy.config.update({'tools.staticdir.root' : WebServer.current_dir})

        # Serving static content
        confStaticContent = {'/statics' : {'tools.staticdir.dir': 'statics','tools.staticdir.on': True},
                             '/css' : {'tools.staticdir.dir': 'css','tools.staticdir.on': True},
                             '/img' : {'tools.staticdir.dir': 'img','tools.staticdir.on': True},
                             '/js' : {'tools.staticdir.dir': 'js','tools.staticdir.on': True}}

        webApplication = cherrypy.tree.mount(WebHomePages(self.lookup), '/',confStaticContent)

        # Disable screen log (standard out)
        # http://stackoverflow.com/questions/4056958/cherrypy-logging-how-do-i-configure-and-use-the-global-and-application-level-lo
        webApplication.log.screen = False
        webApplication.log.access_file = None

        # Go go go!
        cherrypy.engine.start()
        cherrypy.engine.block()

    def stop(self):
        """
            When CherryPy is stopping, we restart it.
        """
        #self.__init__()
        print("test")