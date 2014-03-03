# -*- coding: utf-8 -*-

"""
    CentralReport - Libs modules
        Loads and registers libraries

    https://github.com/CentralReport
"""
import os
import sys

_current_dir = os.path.dirname(__file__)
_binaries_dir = os.path.abspath(os.path.join(_current_dir, "../libs/"))


def register_libraries():
    """ Adds to sys.path available libraries """

    global _binaries_dir

    for binary in os.listdir(_binaries_dir):
        if binary.endswith(('.zip', '.egg', '.whl')):
            sys.path.insert(0, os.path.join(_binaries_dir, binary))
