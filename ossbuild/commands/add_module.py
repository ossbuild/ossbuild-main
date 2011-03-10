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

TARBALL_TEMPLATE = """\
<tarball id="%(package)s" version="%(version)s">
    <source href="%(url)s"
            md5sum="%(md5sum)s"/>
    <dependencies>%(deps)s</dependencies>
</tarball>
"""

AUTOTOOLS_TEMPLATE = """\
<autotools id="%(package)s">
    <branch repo="%(repo)s" module="%(module)s"/>
    <dependencies>%(deps)s</dependencies>
</autotools>
"""

AUTOTOOLS_TYPE = 'autotools'
TARBALL_TYPE = 'tarball'

MODULE_TYPES = {AUTOTOOLS_TYPE: AUTOTOOLS_TEMPLATE,
                TARBALL_TYPE: TARBALL_TEMPLATE}

class cmd_add_module(Command):
    doc = N_('Adds a new module')

    name = 'add_module'
    usage_args = N_('[ options ... ] module')

    def __init__(self):
        Command.__init__(self, [
            make_option('--modulesetsdir',
                        action='store', dest='modulesets_dir', default=None,
                        help=_('Modulesets directory')),
            make_option('--type',
                        action='store', dest='type', default='tarball',
                        help=_('Module type [%s] (default=tarball)' %
                               ','.join(MODULE_TYPES.keys()))),
            make_option('--deps',
                        action='store', dest='deps', default="",
                        help=_('Module dependencies (list of ":" separated '
                               'values)')),
            make_option('--version',
                        action='store', dest='version', default=None,
                        help=_('Module version (only applies to "tarball" type)')),
            make_option('--url',
                        action='store', dest='url', default=None,
                        help=_('URL of the package (only applies to "tarball" type)')),
            make_option('--md5sum',
                        action='store', dest='md5sum', default=None,
                        help=_('MD5 of the tarball (only applies to "tarball" type)')),
            make_option('--repo',
                        action='store', dest='repo', default=None,
                        help=_('Sources repository (only applies to "autotools" type)')),
            make_option('--repo-module',
                        action='store', dest='repo_module', default=None,
                        help=_('Name of the module in the repository '
                               '(only applies to "autotools" type)')),
            ])

    def _parse_options(self, options, config):
        self.modulesets_dir = options.modulesets_dir or config.modulesets_dir
        if self.modulesets_dir is None:
            raise FatalError(_("You must specify a modulesets dir as an option "
                               "if it's not specified in the configuration"))

        self.type = options.type
        if self.type not in MODULE_TYPES:
            raise UsageError(_("Module type is not a valid options"))

        if self.type == TARBALL_TYPE:
            if None in [options.version, options.url, options.md5sum]:
                raise UsageError(_('One of the required property is missing.'))
            self.version = options.version
            self.url = options.url
            self.md5sum = options.md5sum

        if self.type == AUTOTOOLS_TYPE:
            if None in [options, options.url, options.md5sum]:
                raise UsageError(_('One of the required property is missing.'))
            self.repo = options.repo
            self.module = options.module

        self.deps = options.deps

    def _fill_template(self):
        template = MODULE_TYPES[self.type]

        if self.type == TARBALL_TYPE:
            return template % dict(package=self.package, version=self.version,
                url=self.url, md5sum=self.md5sum, deps=self.deps)

        if self.type == AUTOTOOLS_TYPE:
            return template % dict(pacakge=self.package, version=self.version,
                repo=self.repo, module=self.module, deps=self.deps)

    def _write_template(self, template):
        path = os.path.join(self.modulesets_dir, "%s.modules" % self.package)
        if os.path.exists(path):
            raise FatalError(_('The module file aready exists, edit it '
                               'manually(%s)') % path)
        try:
            f = open(path, 'w+')
            f.write(HEADER)
            f.write(template)
            f.write("</moduleset>")
            f.close()
        except IOError, e:
            raise FatalError(_('Error creating module: %s') % e)

    def run(self, config, options, args, help=None):
        if len(args) != 1:
            self.parser.error(_('This command requires a module parameter.'))
        self.package = args[0]
        self._parse_options(options, config)
        self._write_template(self._fill_template())

register_command(cmd_add_module)
