#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
#
#############################################################################
##
## Copyright (c) 2013-2017, gamesun
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


title = 'MyTerm'
version = '2.0.2'
url = 'http://sourceforge.net/projects/myterm/'
author = 'gamesun'
copyright = 'Copyright (C) 2013-2017, gamesun'
aboutme = """
%(title)s %(ver)s
%(copyright)s

%(title)s is a RS232 serial port communication utility and runs on all platforms supported by PyQt including Windows, Linux.

Its features including 
  quick send custom commands
  configure the connection parameters
  detect the valid serial ports
  echo the sending data in local or not
  display data either in hexadecimal or ASCII format
  custom resizable and floatable widgets
  
%(title)s is licensed on all supported platforms under the GNU GPL v3.
For detail see LICENSE.txt. 
""" % dict(title=title, ver=version, copyright=copyright)

