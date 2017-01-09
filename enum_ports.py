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


import sys
import os

# chose an implementation, depending on os
#~ if sys.platform == 'cli':
#~ else:
if os.name == 'nt':  # sys.platform == 'win32':
    from serial.tools.list_ports_windows import comports
elif os.name == 'posix':
    from serial.tools.list_ports_posix import comports
    #~ elif os.name == 'java':
else:
    raise ImportError("Sorry: no implementation for your platform ('{}') available".format(os.name))


def enum_ports():
    hits = 0
    # get iteraror w/ or w/o filter
    iterator = sorted(comports())

    for i in iterator:
        yield i[0]

    # list them
    # for n, (port, desc, hwid) in enumerate(iterator, 1):
    #     sys.stdout.write("{:20}\n".format(port))
    #     sys.stdout.write("    desc: {}\n".format(desc))
    #     sys.stdout.write("    hwid: {}\n".format(hwid))
    #     hits += 1
    #
    # if hits:
    #     sys.stderr.write("{} ports found\n".format(hits))
    # else:
    #     sys.stderr.write("no ports found\n")
