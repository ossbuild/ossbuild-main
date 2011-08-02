# ossbuild - a multiplatform build environment for FOSS
# Copyright (C) Andoni Morales Alastruey 2011
#
#   setup_system.py: setup the build system (MINGW, Msys and other bootstrap things)
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

import os
import shlex

from optparse import make_option
import jhbuild.commands.base as jcommands
from jhbuild.commands import Command
from jhbuild.errors import FatalError
from jhbuild.utils.subprocess_win32 import real_subprocess

from ossbuild.commands import register_command

MSYS_PACKAGES = ['msys-cvs', 'msys-patch', 'msys-wget']

class cmd_setup(Command):
    doc = N_('Setup the build system')

    name = 'setup'

    def __init__(self):
        Command.__init__(self, [])

    def command(self, command, raise_error=False):
        try:
            real_subprocess.call(shlex.split(command))
        except Exception, e:
            raise e
            if raise_error:
                raise

    def run(self, config, options, args, help=None):
        for pkg in MSYS_PACKAGES:
            self.command('mingw-get install %s' % pkg)
        self.command('ossbuild bootstrap')

register_command(cmd_setup)
