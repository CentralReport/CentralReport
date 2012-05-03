# CentralReport - Indev version
# Project by Charles-Emmanuel CAMUS - Avril 2012

import cherrypy
from collectors.Collector import Collector
from threads.ThreadMac import ThreadMac

class WebHomePages:

    def __init__(self,lookupTemplate):
        self.lookup = lookupTemplate

    @cherrypy.expose
    def index(self):
        tmpl = self.lookup.get_template("index.tpl")

        tmpl_vars = []

        if Collector.host_current == Collector.host_MacOS:
            # It's a mac
            tmpl_vars = dict(cpu_idle=ThreadMac.last_dict_cpu['idle'],cpu_system=ThreadMac.last_dict_cpu['system'],cpu_user=ThreadMac.last_dict_cpu['user'])
            tmpl_vars['mem_free'] = ThreadMac.last_dict_memory['mem_free']
            tmpl_vars['mem_active'] = ThreadMac.last_dict_memory['mem_active']
            tmpl_vars['mem_inactive'] = ThreadMac.last_dict_memory['mem_inactive']
            tmpl_vars['mem_total'] = ThreadMac.last_dict_memory['mem_total']

            tmpl_vars['load_1m'] = ThreadMac.last_dict_loadavg['load1m']
            tmpl_vars['load_5m'] = ThreadMac.last_dict_loadavg['load5m']
            tmpl_vars['load_15m'] = ThreadMac.last_dict_loadavg['load15m']

        return tmpl.render(**tmpl_vars)


    def error_page_404(status, message, traceback, version):
        """
        Our 404 error.
        """
        return "Oups... Error %s - Well, I'm very sorry but this page doesn't really exist!" % status
    cherrypy.config.update({'error_page.404': error_page_404})


    @cherrypy.expose
    def test(self):
        return '<h1>This is a test</h1> ... and it works!'