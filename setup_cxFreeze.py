#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
#
#############################################################################
##
## Copyright (c) 2013-2016, gamesun
## All right reserved.
##
## This file is part of MyTerm.
##
## MyTerm is free software: you can redistribute it and/or modify
## it under the terms of the GNU General Public License as published by
## the Free Software Foundation, either version 3 of the License, or
## (at your option) any later version.
##
## MyTerm is distributed in the hope that it will be useful, but
## WITHOUT ANY WARRANTY; without even the implied warranty of
## MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
## GNU General Public License for more details.
##
## You should have received a copy of the GNU General Public License
## along with MyTerm.  If not, see <http://www.gnu.org/licenses/>.
##
#############################################################################


import sys
from cx_Freeze import setup, Executable
import appInfo

base = None
if sys.platform == 'win32':
    base = 'Win32GUI'

options = {
    'build_exe': {'includes': 'atexit'},
}

executables = [
    Executable(
        script='myterm.py', 
        base=base,
        targetName=appInfo.title + '.exe',
        icon='icon/icon.ico',
#        copyright=appInfo.copyright,
    )
]

setup(name=appInfo.title,
      version=appInfo.version,
#      description='',
      options=options,
      executables=executables
      )
