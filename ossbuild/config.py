# ossbuild - a multiplatform build environment for FOSS
# Copyright (C) 2001-2006  James Henstridge
# Copyright (C) 2007-2008  Frederic Peters
# Copyright (C) 2011       Andoni Morales Alastruey
#
#   config.py: configuration file parser
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
import sys
import __builtin__

from jhbuild import config


__all__ = [ 'Config' ]

_defaults_file = os.path.join(os.path.dirname(__file__), 'defaults.ossbuildrc')
_default_ossbuildrc = os.path.join(os.environ['HOME'], '.ossbuild/ossbuildrc')

__builtin__.__dict__['SRCDIR'] = sys.path[0]

class Config(config.Config):
    _orig_environ = None

    def __init__(self, filename=_default_ossbuildrc):
        print filename
        config._defaults_file = _defaults_file
        config.Config.__init__(self, filename)
