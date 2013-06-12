#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
    CentralReport - CLI module (WIP)
        Manages the common line interface

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

screen = None

frame = None

header = None

main = None

footer = None


class WindowCli(object):
    def __init__(self):
        self.content = None

    def display(self):
        global main
        main = self.content

        try:
            display_screen(self.input_handle)
        except urwid.ExitMainLoop:
            pass

    def input_handle(self, input):
        return False


def init_screen():
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
    global frame
    global screen

    frame = urwid.Frame(main, header, footer)
    main_loop = urwid.MainLoop(frame, screen=screen, handle_mouse=False, unhandled_input=input_handle)

    try:
        main_loop.run()
    except KeyboardInterrupt:
        quit()


def generate_blank_characters(number):
    chars = ''
    for i in range (0, number):
        chars += ' '

    return chars


def quit():
    global screen

    if screen is not None:
        screen.clear()

    raise urwid.ExitMainLoop()


def create_radio_item(g, name, callback):
    button = urwid.RadioButton(g, name, on_state_change=callback)
    button = urwid.AttrWrap(button, 'button normal', 'select')
    return button


def create_button(text, callback):
    button = urwid.Button(text, callback)
    button = urwid.AttrWrap(button, 'button normal', 'select')
    return button
