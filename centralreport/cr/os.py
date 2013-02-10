# -*- coding: utf-8 -*-

"""
    CentralReport - os module
        Contains functions to interact with the operating system

    https://github.com/miniche/CentralReport/
"""

import subprocess


def WIP_executeCommand(str_command):
    """
        This function executes an os command. Command can contains pipes, executed as subcommands.
        Returns the result of the command (string).
    """
    # Command can contains pipes. At each pipe, we execute a "subcommand".
    list_pipes = str_command.split("|")

    # Catch all commands result in a list. Used for subcommands
    list_results = []

    for i in range(0, len(list_pipes)):
        list_pipes[i] = list_pipes[i].strip()
        list_command = list_pipes[i].split(" ")

        # If it's not the first occurence, stdin is the last command executed.
        if 0 == i:
            list_results.append(subprocess.Popen(list_command, stdout=subprocess.PIPE))
        else:
            list_results.append(subprocess.Popen(list_command, stdout=subprocess.PIPE, stdin=list_results[i - 1].stdout))

    # Getting result of the last command, and return it.
    return list_results[len(list_results) - 1].communicate()[0]
