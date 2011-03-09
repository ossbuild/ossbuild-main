# ossbuild - a multiplatform build environment for FOSS
# Copyright (C) 2001-2006  James Henstridge
# Copyright (C) 2011 Andoni Morales
#
#   main.py: parses command line arguments and starts the build
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

import sys, os, errno
import optparse
import traceback
import logging

import gettext
import __builtin__
__builtin__.__dict__['N_'] = lambda x: x

import gettext

import jhbuild.main
import ossbuild.config
from jhbuild.main import LoggingFormatter, _encoding
from jhbuild.errors import UsageError, FatalError
from jhbuild.moduleset import warn_local_modulesets

import ossbuild.commands


def print_help(parser):
    parser.print_help()
    print ossbuild.commands.print_help()
    parser.exit()

def main():
    args = sys.argv[1:]

    localedir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'mo'))
    if not os.path.exists(localedir):
        localedir = None
    gettext.install('jhbuild', localedir=localedir, unicode=True)

    if hasattr(os, 'getuid') and os.getuid() == 0:
        sys.stderr.write(_('You should not run ossbuild as root.\n').encode(_encoding, 'replace'))
        sys.exit(1)

    logging.getLogger().setLevel(logging.INFO)
    logging_handler = logging.StreamHandler()
    logging_handler.setFormatter(LoggingFormatter())
    logging.getLogger().addHandler(logging_handler)
    parser = optparse.OptionParser(
        usage=_('%prog [ -f config ] command [ options ... ]'),
        add_help_option=False,
        description=_('Build a set of modules from diverse repositories in correct dependency order (such as GNOME).'))
    parser.disable_interspersed_args()
    parser.add_option('-h', '--help', action='callback',
                      callback=lambda *args: print_help(parser),
                      help=_("Display this help and exit"))
    parser.add_option('--help-commands', action='callback',
                      callback=lambda *args: print_help(parser),
                      help=optparse.SUPPRESS_HELP)
    parser.add_option('-f', '--file', action='store', metavar='CONFIG',
                      type='string', dest='configfile',
                      default=os.environ.get("OSSBUILDRC",
                                             os.path.join(os.environ['HOME'],
                                             '.ossbuildrc')),
                      help=_('use a non default configuration file'))
    parser.add_option('-m', '--moduleset', action='store', metavar='URI',
                      type='string', dest='moduleset', default=None,
                      help=_('use a non default module set'))
    parser.add_option('--no-interact', action='store_true',
                      dest='nointeract', default=False,
                      help=_('do not prompt for input'))

    options, args = parser.parse_args(args)

    try:
        config = ossbuild.config.Config(options.configfile)
    except FatalError, exc:
        sys.stderr.write('ossbuild: %s\n' % exc.args[0].encode(_encoding, 'replace'))
        sys.exit(1)

    if options.moduleset: config.moduleset = options.moduleset
    if options.nointeract: config.interact = False

    if not args or args[0][0] == '-':
        command = 'build' # default to cvs update + compile
    else:
        command = args[0]
        args = args[1:]

    warn_local_modulesets(config)

    try:
        rc = ossbuild.commands.run(command, config, args, help=lambda: print_help(parser))
    except UsageError, exc:
        sys.stderr.write('ossbuild %s: %s\n' % (command, exc.args[0].encode(_encoding, 'replace')))
        parser.print_usage()
        sys.exit(1)
    except FatalError, exc:
        sys.stderr.write('ossbuild %s: %s\n' % (command, exc.args[0].encode(_encoding, 'replace')))
        sys.exit(1)
    except KeyboardInterrupt:
        uprint(_('Interrupted'))
        sys.exit(1)
    except EOFError:
        uprint(_('EOF'))
        sys.exit(1)
    except IOError, e:
        if e.errno != errno.EPIPE:
            raise
        sys.exit(0)
    if rc:
        sys.exit(rc)

if __name__ == "__main__":
    main()
