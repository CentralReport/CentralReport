# -*- coding: utf-8 -*-

"""
    CentralReport - system module
        Contains functions to interact with the operating system

    https://github.com/miniche/CentralReport/
"""

import shlex
import subprocess


def execute_command(str_command):
    """
        This function executes an os command. str_command can contain pipes, executed as subcommands.
        If your command contains vars with a space, use " " to escape words (eg: "Volume Name")
        If you want to use a double quote (") in your command, escape it with \\ (eg: \\":\\" return ":")

        Returns the result of the command (string).
    """

    # Command can contain pipes. At each pipe, we execute a "subcommand".
    list_pipes = str_command.split('|')

    # Catch all commands result in a list. Used for subcommands stdout/stdin
    list_results = []

    for i in range(0, len(list_pipes)):
        list_command = shlex.split(list_pipes[i])

        # If it's not the first occurence, stdin is the last command executed.
        if 0 == i:
            list_results.append(subprocess.Popen(list_command, stdout=subprocess.PIPE))
        else:
            list_results.append(subprocess.Popen(list_command, stdout=subprocess.PIPE, stdin=list_results[i - 1].stdout))
            # Ends the previous subprocess (http://docs.python.org/2/library/subprocess.html#replacing-shell-pipeline)
            list_results[len(list_results) - 2].stdout.close()

    # Getting result of the last command, and return it.
    return list_results[len(list_results) - 1].communicate()[0]
