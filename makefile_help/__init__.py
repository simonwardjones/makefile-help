import logging
import os
import pydoc
import re
from collections import defaultdict

import pkg_resources

__version__ = pkg_resources.get_distribution('makefile-help').version

logging.basicConfig()
logger = logging.getLogger(__file__)
logger.setLevel(logging.INFO)

TERMINAL_COLS = os.popen('tput cols', 'r').read()
MAX_LINE_LENGTH = min([200, int(TERMINAL_COLS)])
BUFFER = 5

BLUE = '\033[34m'
GREEN = '\033[32m'
CYAN = '\033[36m'
GREY = '\033[90m'
RED = '\033[31m'
YELLOW = '\033[33m'
RESET = '\033[39m'

DEFAULT_PATH = './Makefile'

HELP_BASE = f"""
{RED}Makefile help

{YELLOW}To see command run: {CYAN}
   $ make -n <command-name>

{YELLOW}Commands:

"""


def help_from_makefile(path=DEFAULT_PATH):
    """Get pretty help file string from Makefile"""
    with open(path, 'r') as fh:
        makefile = fh.read()
    commands_and_comments = re.findall(
        pattern=r'^(?P<rule>[\w -]*?):.*?(?:#+\s*(?P<comment>.*)\s*)?$',
        string=makefile,
        flags=re.MULTILINE)
    commands_by_section = defaultdict(list)
    for command_name, comment in commands_and_comments:
        section, desc = get_parts_from_comment(comment)
        commands_by_section[section].append((command_name, desc))
    logger.debug(f'Found commands_by_section {commands_by_section}')
    makefile_help = get_help_string(commands_by_section)
    return makefile_help


def get_parts_from_comment(comment):
    """Get the section and description from comment"""
    closed_section_match = re.match(
        pattern=r'@@(?P<section>.*?)@@\s*(?P<desc>.*)$',
        string=comment)
    if closed_section_match:
        section, desc = closed_section_match.groups()
        return section, desc
    open_section_match = re.match(
        pattern=r'@@(?P<section>\w+)\s*(?P<desc>.*)$',
        string=comment)
    if open_section_match:
        section, desc = open_section_match.groups()
        return section, desc
    return 'General Commands', comment


def wrap_desc(desc, command_max):
    """Wrap description if longer than line length"""
    line, *words = desc.split(' ')
    line_length = len(line) + command_max + BUFFER
    lines = []
    for word in words:
        if line_length + len(word) < MAX_LINE_LENGTH:
            line += f' {word}'
            line_length += len(word) + 1
        else:
            lines.append(line)
            line = word
            line_length = len(line) + command_max + BUFFER
    lines.append(line)
    return (f'\n{CYAN}' + (' ' * (command_max + BUFFER))).join(lines)


def get_help_string(commands_by_section):
    makefile_help = HELP_BASE
    if not commands_by_section:
        return makefile_help
    command_max = max(
        len(command_name)
        for section_commands in commands_by_section.values()
        for command_name, _ in section_commands)
    logger.debug(f'Command max length: {command_max}')
    for section, commands in commands_by_section.items():
        if len(commands_by_section) != 1 or section != 'General Commands':
            makefile_help += f'{GREY}{section}:\n'
        for command_name, desc in commands:
            if desc:
                command_name = command_name.ljust(command_max + BUFFER, ".")
            if len(desc) > MAX_LINE_LENGTH - command_max - BUFFER:
                desc = wrap_desc(desc, command_max)
            makefile_help += f'{GREEN}{command_name}{CYAN}{desc}\n'
        makefile_help += f'\n{RESET}'
    return makefile_help


if __name__ == "__main__":
    makefile_help = help_from_makefile()
    pydoc.pipepager(makefile_help, cmd='less -R')
