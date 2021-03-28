"""
Support for "auto-completing" commands. Essentially, bot commands that use the
best match logic adapter to be executed.

Experimental.
"""
from typing import List

from bot_modules.classes.Command import Command

def extend_with_commands(command_list: List[Command], raw_list: List[str]):
    """
    Inject the app's commands via the list training method by using this 
    function.
    """
    for command in command_list:
        raw_list.append(command.phrase)
        raw_list.append(command.response)

def match(response: str, command_list: List[Command]):
    for command in command_list:
        if command.match(response):
            return command

    return None
