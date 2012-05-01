# CentralReport - Indev version
# Project by Charles-Emmanuel CAMUS - Avril 2012

import cherrypy
from mako.template import Template
from mako.lookup import TemplateLookup

class WebHomePages:

    def __init__(self,lookupTemplate):
        self.lookup = lookupTemplate

    @cherrypy.expose
    def index(self):
        return "Welcome - It works!"

    def error_page_404(status, message, traceback, version):
        return "Oups... Error %s - Well, I'm very sorry but this page doesn't really exist!" % status
    cherrypy.config.update({'error_page.404': error_page_404})

    @cherrypy.expose
    def test(self):
        tmpl = self.lookup.get_template("index.tpl")
        tmpl_vars = dict(hello="Hello, my beautiful world!")
        return tmpl.render(**tmpl_vars)