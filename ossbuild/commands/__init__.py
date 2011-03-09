# ossbuild - a multiplatform build environment for FOSS
# Copyright (C) 2001-2006  James Henstridge
# Copyright (C) 2011 Andoni Morales
#
#   __init__.py: a package holding the various ossbuild subcommands
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA

__metaclass__ = type
__all__ = [
    'register_command',
    'run'
    ]

import optparse
import sys

from jhbuild.errors import UsageError, FatalError

def print_help():
    import os
    thisdir = os.path.abspath(os.path.dirname(__file__))

    # import all available commands
    for fname in os.listdir(os.path.join(thisdir)):
        name, ext = os.path.splitext(fname)
        if not ext == '.py':
            continue
        try:
            __import__('ossbuild.commands.%s' % name)
        except ImportError:
            pass

    uprint(_('OSSBuild commands are:'))
    commands = [(x.name, x.doc) for x in get_commands().values()]
    commands.sort()
    for name, description in commands:
        uprint('  %-15s %s' % (name, description))
    print
    uprint(_('For more information run "ossbuild <command> --help"'))

# handle registration of new commands
_commands = {}
def register_command(command_class):
    _commands[command_class.name] = command_class

from jhbuild.commands import cmd_help
register_command(cmd_help)

def get_commands():
    return _commands

def run(command, config, args, help):
    # if the command hasn't been registered, load a module by the same name
    if command not in _commands:
        try:
            __import__('ossbuild.commands.%s' % command)
        except ImportError:
            pass
    if command not in _commands:
        raise FatalError(_('command not found'))

    command_class = _commands[command]

    cmd = command_class()
    return cmd.execute(config, args, help)


from ossbuild.commands import jhbuild_wrapper
