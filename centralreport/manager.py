#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
    CentralReport - Manager
        This CLI manager is used to modify the CentralReport configuration.

    https://github.com/CentralReport
"""

# The centralreport module is imported first to initialize third-party libraries
import centralreport

import getpass
import os
import sys

import urwid

import cr.cli
from cr import log
from cr import system
from cr.tools import Config

cr_config = None

class MainCli(cr.cli.WindowCli):
    def __init__(self):
        cr.cli.WindowCli.__init__(self)

        #TODO: Finish this part
        self.content = urwid.ListBox([urwid.Text('Not ready yet')])


class OnlineCli(cr.cli.WindowCli):
    """
        Manages the configuration related to the Online part
    """

    def __init__(self):
        cr.cli.WindowCli.__init__(self)

        self.title = 'Online agent configuration'
        self.subtitle = 'CentralReport Online is the best choice to monitor your host ' \
                        'easily, without complex configuration. \n' \
                        'You can get your account token at centralreport.net'

        self.port_caption = urwid.Text('Your account token: ', align='right')
        self.port_edit_box = urwid.Edit()
        self.port_edit = urwid.AttrMap(self.port_edit_box, 'text', 'select')
        self.port_columns = urwid.Columns([self.port_caption, self.port_edit])

        button_ok = cr.cli.create_button('OK', self.validate)
        button_ok_grid = urwid.GridFlow([button_ok], 6, 2, 0, 'center')

        self.menu = [urwid.Divider(),
                     urwid.Text(self.title),
                     urwid.Text(self.subtitle),
                     urwid.Divider(),
                     urwid.Divider(),
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

        self.title = 'Standalone configuration'
        self.subtitle = 'The standalone app is available through a web interface.'

        self.port_caption = urwid.Text('Port number: ', align='right')
        self.port_edit_box = urwid.IntEdit(default=int(cr_config.get_config_value('Webserver', 'port')))
        self.port_edit = urwid.AttrMap(self.port_edit_box, 'text', 'select')
        self.port_columns = urwid.Columns([self.port_caption, self.port_edit])

        button_ok = cr.cli.create_button('OK', self.validate)
        button_ok_grid = urwid.GridFlow([button_ok], 6, 2, 0, 'center')

        self.menu = [urwid.Divider(),
                     urwid.Text(self.title),
                     urwid.Text(self.subtitle),
                     urwid.Divider(),
                     self.port_columns,
                     urwid.Divider(),
                     button_ok_grid]

        self.list_box = urwid.ListBox(urwid.SimpleListWalker(self.menu))
        self.content = urwid.Columns([self.list_box], focus_column=0)

    def validate(self, state):
        """
            Triggered when the user press the "OK" button
        """

        if self.port_edit_box.value() == 0:
            cr_config.set_config_value('Webserver', 'enable', 'False')
            cr_config.set_config_value('Webserver', 'port', '0')
        else:
            cr_config.set_config_value('Webserver', 'enable', 'True')
            cr_config.set_config_value('Webserver', 'port', str(self.port_edit_box.value()))

        cr.cli.quit()


class WizardCli(cr.cli.WindowCli):
    """
        Displayed during the CentralReport installation
    """

    def __init__(self):
        cr.cli.WindowCli.__init__(self)

        self.title = 'Welcome to CentralReport!'
        self.subtitle = 'CentralReport always keeps an eye on your system. Receive alerts in real time, ' \
                        'follow up statistics evolution and much more. \n' \
                        'The project is open sourced and available at github.com/CentralReport. \n' \
                        'All the documentation can be found at docs.centralreport.net'

        self.caption = 'Please choose one mode:'

        self.group = list()
        self.items = list()
        self.radios = list()

        self.choices = [
            ['Standalone app only', 'Enables the internal web server'],
            ['CentralReport Online agent only', 'Only used as agent for centralreport.net'],
            ['Standalone app + CentralReport Online agent', 'Combines all local possibilities and the Online platform']
        ]

        for choise in self.choices:
            self.radios.append(cr.cli.create_radio_item(self.group, choise[0], self.on_state_change))

            self.items.append(self.radios[-1])
            self.items.append(urwid.Text(cr.cli.generate_blank_characters(6) + choise[1]))
            self.items.append(urwid.Divider())

        self.items[0].set_state(True)

        button_ok = cr.cli.create_button('OK', self.validate)
        button_ok_grid = urwid.GridFlow([button_ok], 6, 2, 0, 'center')

        self.menu = [urwid.Divider(),
                     urwid.Text(self.title),
                     urwid.Text(self.subtitle),
                     urwid.Divider(),
                     urwid.Text(self.caption),
                     urwid.Divider()] \
                    + self.items + \
                    [urwid.Divider(),
                     button_ok_grid]

        self.list_box = urwid.ListBox(urwid.SimpleListWalker(self.menu))
        self.content = urwid.Columns([self.list_box], focus_column=0)

    def on_state_change(self, item, state):
        """
            Default behavior when the user select one radio item
        """
        pass

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
        if self.radios[0].state:
            standalone = StandaloneCli()
            standalone.display()

        elif self.radios[1].state:
            online = OnlineCli()
            online.display()
        elif self.radios[2].state:
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

    cr_config.write_config_file()

    # CentralReport must be restarted to detect the new configuration
    system.execute_command('/usr/local/bin/centralreport restart')

    exit(0)
