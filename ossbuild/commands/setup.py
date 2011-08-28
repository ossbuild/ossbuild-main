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
import platform

from optparse import make_option
import jhbuild
import jhbuild.commands.base as jcommands
from jhbuild.commands import Command
from jhbuild.errors import FatalError
from jhbuild.utils.subprocess_win32 import real_subprocess
from jhbuild.utils.httpcache import load
from jhbuild.utils.unpack import unpack_tar_file

from ossbuild.commands import register_command

MSYS_PACKAGES = ['msys-cvs', 'msys-patch', 'msys-wget']

MINGW_W32_i686_LINUX ="http://downloads.sourceforge.net/project/mingw-w64/Toolchains%20targetting%20Win32/Automated%20Builds/mingw-w32-1.0-bin_i686-linux_20110822.tar.bz2"
W32_i686_LINUX_SYSROOT = "/home/mingw64/m64bs/linux-x86-x86/build/build/root/i686-w64-mingw32/lib"

SED = "sed -i s/%s/%s/g %s"

MINGW_W32_x84_64_LINUX ="http://downloads.sourceforge.net/project/mingw-w64/Toolchains%20targetting%20Win32/Automated%20Builds/mingw-w32-1.0-bin_x86_64-linux_20110819.tar.bz2"

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
        buildscript = jhbuild.frontends.get_buildscript(config, [])
        if platform.system() == 'Windows':
            self.windows_setup(config, buildscript)
        else:
            self.unix_setup(config, buildscript)

    def windows_setup(self, config, buildscript):
        for pkg in MSYS_PACKAGES:
            self.command('mingw-get install %s' % pkg)
        self.command('ossbuild bootstrap')

    def mingw_root(self, prefix, target='w32'):
        return os.path.join(prefix, "mingw", target)

    def unix_setup(self, config, buildscript):
        self.install_mingw_w32(config, buildscript)
        
    def fix_lib_paths(self, buildscript, orig_sysroot, new_sysroot, lib_path):
        def escape(s):
            return s.replace('/', '\\/')
        for path in [f for f in os.listdir(lib_path) if f.endswith('la')]:
            sed_cmd = SED % (escape(orig_sysroot), escape(new_sysroot),
                             os.path.abspath(os.path.join(lib_path, path))) 
            buildscript.execute(sed_cmd.split(' '))
        
    def install_mingw_w32(self, config, buildscript):
        buildscript.set_action(_("Downloading MinGW W32"), self)
        path = load(MINGW_W32_i686_LINUX)
        mingw_root = self.mingw_root(os.path.join(config.prefix, '..'), 'w32')
        buildscript.set_action(_("Extracting %s") % os.path.basename(path), self)
        unpack_tar_file(path, mingw_root)
        buildscript.set_action(_("Fixing lib paths"), self)
        self.fix_lib_paths(buildscript, W32_i686_LINUX_SYSROOT,
                           os.path.join(mingw_root, 'i686-w64-mingw32', 'lib'),
                           '%s/i686-w64-mingw32/lib32' % mingw_root) 
        
        
register_command(cmd_setup)
