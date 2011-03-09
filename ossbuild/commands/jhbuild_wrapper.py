# ossbuild - a multiplatform build environment for FOSS
# Copyright (C) Andoni Morales Alastruey 2011
#
#   jhbuild_wrapper.py: a wrapper the base command of jhbuild
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

import jhbuild.commands.base as jcommands
from ossbuild.commands import register_command


class cmd_update(jcommands.cmd_update):
    pass
register_command(cmd_update)

class cmd_updateone(jcommands.cmd_updateone):
    pass
register_command(cmd_updateone)

class cmd_cleanone(jcommands.cmd_cleanone):
    pass
register_command(cmd_cleanone)

class cmd_build(jcommands.cmd_build):
    pass
register_command(cmd_build)

class cmd_buildone(jcommands.cmd_buildone):
    pass
register_command(cmd_buildone)

class cmd_run(jcommands.cmd_run):
    pass
register_command(cmd_run)

class cmd_shell(jcommands.cmd_shell):
    pass
register_command(cmd_shell)

class cmd_list(jcommands.cmd_list):
    pass
register_command(cmd_list)
