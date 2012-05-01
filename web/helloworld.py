# Test for CherryPy

import cherrypy
from cherrypy.scaffold import Root
from mako.template import Template
from mako.lookup import TemplateLookup
import os

lookup = TemplateLookup(directories=['tpl'])
current_dir = os.path.dirname(os.path.abspath(__file__))

class HelloWorld:


    def index(self):
        return "Hello world!"
    index.exposed = True

    @cherrypy.expose
    def test(self):
        tmpl = lookup.get_template("index.tpl")
        tmpl_vars = dict(hello="Hello, my beautiful world!")
        return tmpl.render(**tmpl_vars)


# Added : a true config file
#cherrypy.config.update('web.conf')

cherrypy.config.update({'server.socket_host': '0.0.0.0', 'server.socket_port': 8081})

conf = {'/': {'tools.staticdir.on': True,
              'tools.staticdir.dir':os.path.join(current_dir,'')}}

#conf = {'/': {'tools.staticdir.on': True,'tools.staticdir.dir':os.path.join(current_dir,'')},
#        '/statics': {'tools.staticdir.on': True,'tools.staticdir.dir': 'statics'},
#        '/che': {'tools.staticdir.on': True,'tools.staticdir.dir': 'che'}}

cherrypy.quickstart(HelloWorld(),"/",config=conf)
#cherrypy.quickstart(HelloWorld(),"/")