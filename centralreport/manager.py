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
from cr.utils.web import check_port

cr_config = None


class MainCli(cr.cli.WindowCli):
    def __init__(self):
        cr.cli.WindowCli.__init__(self)

        # Daemon status
        self.status_text = urwid.Text('Daemon status unknown')
        self.status = urwid.AttrMap(self.status_text, 'text red')
        self.refresh_daemon_status()

        status_buttons = [cr.cli.create_button('Start', self.start_daemon),
                          cr.cli.create_button('Stop', self.stop_daemon),
                          cr.cli.create_button('Restart', self.restart_daemon)]


        # Standalone config
        self.standalone_status_text = urwid.Text('Standalone app status unknown')
        self.standalone_status = urwid.AttrMap(self.standalone_status_text, 'text red')
        self.refresh_standalone_status()

        button_app = cr.cli.create_button('Modify standalone app config', self.update_app_config)

        button_quit = cr.cli.create_button('Save and Quit', self.quit)

        self.items = [urwid.Divider(),
                      self.status] + \
                     status_buttons + \
                     [urwid.Divider(),
                      self.standalone_status,
                      button_app,
                      urwid.Divider(),
                      urwid.Divider(),
                      urwid.Divider(),
                      button_quit]

        self.content = urwid.ListBox(urwid.SimpleListWalker(self.items))

    def refresh_daemon_status(self):
        pid = system.execute_command('/usr/local/bin/centralreport pid')
        if int(pid) == 0:
            self.status_text.set_text('CentralReport is not running')
            self.status.set_attr_map({None: 'text red'})
        else:
            self.status_text.set_text('CentralReport is running with PID %s' % int(pid))
            self.status.set_attr_map({None: 'text green'})

    def refresh_standalone_status(self):
        if convert_text_to_bool(Config.get_config_value('Webserver', 'enable')) is True:
            self.standalone_status_text.set_text('Standalone app is enabled')
            self.standalone_status.set_attr_map({None: 'text green'})
        else:
            self.standalone_status_text.set_text('Standalone app is disabled')
            self.standalone_status.set_attr_map({None: 'text red'})

    def update_app_config(self, state):
        standalone = StandaloneCli()
        standalone.display()
        self.refresh_standalone_status()

    def stop_daemon(self, button):
        self.status_text.set_text('Stopping CentralReport...')
        self.status.set_attr_map({None: 'text yellow'})
        self.main_loop.draw_screen()

        system.execute_command('/usr/local/bin/centralreport stop')
        self.refresh_daemon_status()

    def start_daemon(self, button):
        self.status_text.set_text('Starting CentralReport...')
        self.status.set_attr_map({None: 'text yellow'})
        self.main_loop.draw_screen()

        system.execute_command('/usr/local/bin/centralreport start')
        self.refresh_daemon_status()

    def restart_daemon(self, button):
        self.status_text.set_text('Restarting CentralReport...')
        self.status.set_attr_map({None: 'text yellow'})
        self.main_loop.draw_screen()

        system.execute_command('/usr/local/bin/centralreport restart')
        self.refresh_daemon_status()

    def quit(self, button):
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

        chosen_port = int(self.port_edit_box.value())
        actual_port = int(cr_config.get_config_value('Webserver', 'port'))

        if self.items[0].state:
            if chosen_port != actual_port and check_port('127.0.0.1', chosen_port) is True:
                error_dialog = cr.cli.DialogCli('This port is already used by another application. Please choose a '
                                                'free port.')
                error_dialog.display()
                return

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
                       'configuration later executing "centralreport manager" or editing the configuration ' \
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
        print 'Restarting the CentralReport daemon...'
        system.execute_command('/usr/local/bin/centralreport restart')

    exit(0)
