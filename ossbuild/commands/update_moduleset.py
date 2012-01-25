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

import os

from optparse import make_option
import jhbuild.commands.base as jcommands
from jhbuild.commands import Command
from jhbuild.errors import FatalError

from ossbuild.commands import register_command

HEADER = """\
<?xml version="1.0" standalone="no"?> <!--*- mode: nxml -*-->
<!DOCTYPE moduleset SYSTEM "moduleset.dtd">
<?xml-stylesheet type="text/xsl" href="moduleset.xsl"?>
<moduleset>
"""

class cmd_update_moduleset(Command):
    doc = N_('Updates the main moduleset')

    name = 'update_moduleset'
    usage_args = N_('[ options ... ] program [ arguments ... ]')

    def __init__(self):
        Command.__init__(self, [
            #FIXME: Don't hardcode default values
            make_option('--moduleset', metavar='MODULE',
                        action='store', dest='moduleset', default = None,
                        help=_('name of the moduleset')),
            make_option('--modulesetsdir', metavar='MODULE',
                        action='store', dest='modulesets_dir', default = None,
                        help=_('Directory lookup for available modules ')),
            ])
        self.modulesets = []

    def _find_repos_and_modules(self, dir, moduleset):
        names = os.listdir(dir)
        self.modulesets = [os.path.join(dir, x) for x in names
                           if os.path.isfile(os.path.join(dir,x))
                           and x.endswith('.modules')
                           and x != "%s.modules" % moduleset
                           and x != "bootstrap-msys.modules"]
        self.repos = [os.path.join(dir,x) for x in names
                           if os.path.isfile(os.path.join(dir,x))
                           and x.endswith('.repos')]

    def _write_moduleset(self, path):
        try:
            f = open(path, 'w+')
        except IOError, e:
            raise FatalError(_("Could not open the moduleset file: %s.") % e)
        f.write(HEADER)
        for repo in self.repos:
            try:
                r = open(repo, 'r+')
                f.write(r.read())
                r.close()
            except Exception, e:
                # FIXME: log warning
                print e
        f.write('\n')
        for m in self.modulesets:
            f.write('  <include href="%s"/>\n' % m)
        f.write("</moduleset>")

    def run(self, config, options, args, help=None):
        moduleset = options.moduleset or config.moduleset
        modulesets_dir = options.modulesets_dir or config.modulesets_dir
        if moduleset is None:
            raise FatalError(_("You must specify a moduleset as an option "
                               "if it's not specified in the configuration"))
        if modulesets_dir is None:
            raise FatalError(_("You must specify a modulesets dir as an option "
                               "if it's not specified in the configuration"))
        if not os.path.isdir(modulesets_dir):
            raise FatalError(_("The modulesets path doesn't exists"))

        moduleset_path = os.path.join(modulesets_dir, '%s.modules' % moduleset)

        self._find_repos_and_modules(modulesets_dir, moduleset)
        self._write_moduleset(moduleset_path)

    @staticmethod
    def update(config):
        options = DummyOptions()
        cmd = cmd_update_moduleset()
        cmd.run(config, options, None)


class DummyOptions(object):
    moduleset = None
    modulesets_dir = None


register_command(cmd_update_moduleset)
