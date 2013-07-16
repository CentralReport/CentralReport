#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
    CentralReport - CLI module (WIP)
        Manages the command line interface

    https://github.com/CentralReport
"""

import urwid

_palette = [
    ('header', 'white', 'dark blue', 'standout'),
    ('divider', 'black', 'dark cyan', 'standout'),
    ('error', 'white', 'dark red', 'standout'),
    ('text', 'light gray', 'default'),
    ('button normal', 'white', 'black', 'standout'),
    ('select', 'black', 'light gray', 'standout'),
    ('button disabled', 'dark gray', 'dark blue')
]

#: @type screen: urwid.Screen
screen = None

#: @type frame: urwid.Frame
frame = None

#: @type header: urwid.Text
header = None

#: @type main: urwid.Widget
main = None

#: @type footer: urwid.Text
footer = None


class WindowCli(object):
    """
        A default window to fill the "main" object of cr.cli
    """

    def __init__(self):
        self.content = None

    def display(self):
        """
            Displays the content on the screen
        """

        global main
        main = self.content

        try:
            display_screen(self.input_handle)
        except urwid.ExitMainLoop:
            pass

    def input_handle(self, input):
        """
            Default behavior when the user presses a key

            @type input: str
            @param input: The key code
        """
        return False


class DialogCli(WindowCli):
    def __init__(self):
        WindowCli.__init__(self)


def init_screen():
    """
        Initializes the screen with a header (3 lines) and a footer (1 line).
        The default background color is blue for the bars and black for the content.
        This function does not display anything, see display_screen().
    """

    global screen
    global frame
    global header
    global main
    global footer

    screen = urwid.raw_display.Screen()
    screen.register_palette(_palette)

    header = urwid.Text('\n CentralReport CLI Manager \n')
    header = urwid.AttrWrap(header, 'header')

    footer = urwid.Text(' Use arrow keys to move ')
    footer = urwid.AttrWrap(footer, 'header')

    content_list = [urwid.Text("No content available")]
    main = urwid.ListBox(content_list)


def display_screen(input_handle):
    """
        This function sends the content to the screen.

        @param input_handle: Callback function called when the user presses a key
    """

    global frame
    global screen

    frame = urwid.Frame(main, header, footer)
    main_loop = urwid.MainLoop(frame, screen=screen, handle_mouse=False, unhandled_input=input_handle)

    try:
        main_loop.run()
    except KeyboardInterrupt:
        quit()


def generate_blank_characters(number):
    """
        This function generates blank characters.

        @param number: The number of blank characters.
    """

    chars = ''
    for i in range(0, number):
        chars += ' '

    return chars


def quit():
    """
        This function exits the current urwid.MainLoop().
        If multiple MainLoop have been started, the previous MainLoop resumes.
    """

    global screen

    if screen is not None:
        screen.clear()

    raise urwid.ExitMainLoop()


def create_radio_item(group, name, callback):
    """
        Creates a radio item, in a group. See urwid.RadioButton for more details

        @type group: list
        @param group: Add the new button to this group

        @type name: str
        @param name: Name displayed

        @param callback: Callback function. Called when the user select this item.
    """

    button = urwid.RadioButton(group, name, on_state_change=callback)
    button = urwid.AttrWrap(button, 'button normal', 'select')
    return button


def create_button(text, callback):
    """
        Creates a button, in a group. See urwid.Button for more details

        @type text: str
        @param text: Text displayed in the button

        @param callback: Callback function. Called when the user presses this button.
    """

    button = urwid.Button(text, callback)
    button = urwid.AttrWrap(button, 'button normal', 'select')
    return button
