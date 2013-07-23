#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
    CentralReport - Manager
        This CLI manager is used to modify the CentralReport configuration.

    https://github.com/CentralReport
"""

# The centralreport module is firstly imported to initialize third-party libraries
import centralreport

import getpass
import os
import sys

import urwid

import cr.cli
from cr import log
from cr import system
from cr.tools import Config
from cr.utils.text import convert_text_to_bool

cr_config = None


class MainCli(cr.cli.WindowCli):
    def __init__(self):
        cr.cli.WindowCli.__init__(self)
        self.draw()

    def draw(self):
        pid = system.execute_command('/usr/local/bin/centralreport pid')
        if int(pid) == 0:
            self.status = urwid.Text('CentralReport is not running')
            self.status = urwid.AttrMap(self.status, 'text red')
            status_buttons = [cr.cli.create_button('Start', self.update_app_config)]
        else:
            self.status = urwid.Text('CentralReport is running with PID %s' % int(pid))
            self.status = urwid.AttrMap(self.status, 'text green')
            status_buttons = [cr.cli.create_button('Stop', self.update_app_config),
                              cr.cli.create_button('Restart', self.update_app_config)]

        # Standalone config
        if convert_text_to_bool(Config.get_config_value('Webserver', 'enable')) is True:
            self.standalone_status = urwid.Text('Standalone app is enabled')
            self.standalone_status = urwid.AttrMap(self.standalone_status, 'text green')
        else:
            self.standalone_status = urwid.Text('Standalone app is disabled')
            self.standalone_status = urwid.AttrMap(self.standalone_status, 'text red')

        button_app = cr.cli.create_button('Modify standalone app config', self.update_app_config)

        # Online config
        self.online_status = urwid.Text('Online config is not available yet')
        self.online_status = urwid.AttrMap(self.online_status, 'text red')
        button_online = cr.cli.create_button('Modify online config', self.update_online_config)

        button_quit = cr.cli.create_button('Save and Quit', self.quit)

        self.items = [urwid.Divider(),
                      self.status] + \
                     status_buttons + \
                     [urwid.Divider(),
                      self.standalone_status,
                      button_app,
                      urwid.Divider(),
                      self.online_status,
                      button_online,
                      urwid.Divider(),
                      urwid.Divider(),
                      button_quit]

        self.content = urwid.ListBox(urwid.SimpleListWalker(self.items))

    def update_app_config(self, state):
        standalone = StandaloneCli()
        standalone.display()

    def update_online_config(self, state):
        online = OnlineCli()
        online.display()

    def stop_daemon(self, button):
        system.execute_command('/usr/local/bin/centralreport stop')
        self.draw()
        self.display()

    def quit(self, button):
        cr.cli.quit()


class OnlineCli(cr.cli.WindowCli):
    """
        Manages the configuration related to the Online part
    """

    def __init__(self):
        cr.cli.WindowCli.__init__(self)

        title = 'Online agent configuration'
        subtitle = 'CentralReport Online is the best choice to monitor your host ' \
                    'easily, without complex configuration. \n' \
                    'You can get your account token at centralreport.net'

        question = 'Do you want to add this host to your centralreport.net account?'

        self.group = list()
        self.items = list()
        self.radios = list()

        self.choices = ['Yes', 'No']

        for choice in self.choices:
            self.radios.append(cr.cli.create_radio_item(self.group, choice, None))
            self.items.append(self.radios[-1])

        if cr_config.get_config_value('Webserver', 'enable') != '':
            self.items[0].set_state(True)
        else:
            self.items[1].set_state(True)

        self.port_caption = urwid.Text('Your account token: ', align='right')
        self.port_edit_box = urwid.Edit()
        self.port_edit = urwid.AttrMap(self.port_edit_box, 'text', 'select')
        self.port_columns = urwid.Columns([self.port_caption, self.port_edit])

        button_ok = cr.cli.create_button('OK', self.validate)
        button_ok_grid = urwid.GridFlow([button_ok], 6, 2, 0, 'center')

        self.menu = [urwid.Divider(),
                     urwid.Text(title),
                     urwid.Divider(),
                     urwid.Text(subtitle),
                     urwid.Divider(),
                     urwid.Text(question)] + \
                    self.items + \
                    [urwid.Divider(),
                     self.port_columns,
                     urwid.Divider(),
                     button_ok_grid]

        self.list_box = urwid.ListBox(urwid.SimpleListWalker(self.menu))
        self.content = urwid.Columns([self.list_box], focus_column=0)

    def validate(self, state):
        """
            Triggered when the user press the "OK" button
        """

        #TODO: Update the configuration, after merging "feature-webservices" branch in "develop"
        cr.cli.quit()


class StandaloneCli(cr.cli.WindowCli):
    """
        Manages the configuration related to the local app
    """

    def __init__(self):
        cr.cli.WindowCli.__init__(self)

        title = 'Standalone app configuration'
        subtitle = 'CentralReport includes a web server. You can check your statistics with a simple web ' \
                   'browser, without any external service.'

        question = 'Do you want to activate the standalone app?'

        self.group = list()
        self.items = list()
        self.radios = list()

        self.choices = ['Yes', 'No']

        for choice in self.choices:
            self.radios.append(cr.cli.create_radio_item(self.group, choice, None))
            self.items.append(self.radios[-1])

        if convert_text_to_bool(cr_config.get_config_value('Webserver', 'enable')):
            self.items[0].set_state(True)
        else:
            self.items[1].set_state(True)

        self.port_caption = urwid.Text('Port number: ', align='right')
        self.port_edit_box = urwid.IntEdit(default=int(cr_config.get_config_value('Webserver', 'port')))
        self.port_edit = urwid.AttrMap(self.port_edit_box, 'text', 'select')
        self.port_columns = urwid.Columns([self.port_caption, self.port_edit])

        button_ok = cr.cli.create_button('OK', self.validate)
        button_ok_grid = urwid.GridFlow([button_ok], 6, 2, 0, 'center')

        self.menu = [urwid.Divider(),
                     urwid.Text(title),
                     urwid.Divider(),
                     urwid.Text(subtitle),
                     urwid.Divider(),
                     urwid.Text(question)] + \
                    self.items + \
                    [urwid.Divider(),
                     self.port_columns,
                     urwid.Divider(),
                     button_ok_grid]

        self.list_box = urwid.ListBox(urwid.SimpleListWalker(self.menu))
        self.content = urwid.Columns([self.list_box], focus_column=0)

    def validate(self, button):
        """
            Triggered when the user press the "OK" button
        """

        if self.items[0].state:
            cr_config.set_config_value('Webserver', 'enable', 'True')
            cr_config.set_config_value('Webserver', 'port', str(self.port_edit_box.value()))
        else:
            cr_config.set_config_value('Webserver', 'enable', 'False')

        cr.cli.quit()


class WizardCli(cr.cli.WindowCli):
    """
        Displayed during the CentralReport installation
    """

    def __init__(self):
        cr.cli.WindowCli.__init__(self)

        title = 'Welcome to CentralReport!'
        subtitle = 'CentralReport always keeps an eye on your system. Receive alerts in real time, ' \
                        'follow up statistics evolution and much more. \n' \
                        'The project is open sourced and available at github.com/CentralReport. \n' \
                        'All the documentation can be found at docs.centralreport.net'

        caption = 'This wizard helps you to configure main options. You will able to update the ' \
                       'configuration executing "centralreport manager" or editing the configuration ' \
                       'file located at /etc/centralreport/centralreport.cfg'

        button_ok = cr.cli.create_button('Start', self.validate)
        button_ok_grid = urwid.GridFlow([button_ok], 15, 2, 0, 'center')

        self.menu = [urwid.Divider(),
                     urwid.Text(title),
                     urwid.Divider(),
                     urwid.Text(subtitle),
                     urwid.Divider(),
                     urwid.Text(caption),
                     urwid.Divider(),
                     urwid.Divider(),
                     button_ok_grid]

        self.list_box = urwid.ListBox(urwid.SimpleListWalker(self.menu))
        self.content = urwid.Columns([self.list_box], focus_column=0)

    def input_handle(self, input):
        """
            Default behavior when the user press a key
        """
        if input in ('q', 'Q'):
            cr.cli.quit()
            return True

        return False

    def validate(self, state):
        """
            Triggered when the user press the "OK" button
        """
        standalone = StandaloneCli()
        standalone.display()
        online = OnlineCli()
        online.display()

        cr.cli.quit()


if __name__ == '__main__':
    if os.path.isfile('/usr/local/bin/centralreport') is False:
        print 'CentralReport must be installed on this host to run the CLI Manager!'
        exit(2)
    elif getpass.getuser() != 'root':
        print 'You must execute this manager as root to perform administrative operations!'
        exit(3)

    log.log_info('CLI Manager is starting...')

    cr_config = Config()
    cr_config.read_config_file()

    if len(sys.argv) == 1:
        cr.cli.init_screen()
        main_screen = MainCli()
        main_screen.display()
    else:
        if sys.argv[1] == 'wizard':
            cr.cli.init_screen()
            wizard_screen = WizardCli()
            wizard_screen.display()
        else:
            print 'CentralReport CLI Manager - Usage: \n' \
                  'manager.py [wizard]'
            exit(1)

    print 'Saving the new configuration...'
    cr_config.write_config_file()

    # CentralReport must be restarted to detect the new configuration
    if int(system.execute_command('/usr/local/bin/centralreport pid')) != 0:
        print 'Restarting CentralReport daemon...'
        system.execute_command('/usr/local/bin/centralreport restart')

    exit(0)
