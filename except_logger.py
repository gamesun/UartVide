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


import os, io, logging, traceback

log_path_file = os.path.join(os.path.expanduser('~'), 'MyTerm', 'error.log')
log_path_dir = os.path.join(os.path.expanduser('~'), 'MyTerm')

if not os.path.isdir(log_path_dir):
    os.makedirs(os.path.join(os.path.expanduser('~'), 'MyTerm'))

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s:%(levelname)s:%(name)s:%(message)s',
    filename=log_path_file,
    filemode='a'
)

logger = logging.getLogger('MyTerm')

def exceptHook(excType, excValue, tracebackobj):
    """
    Global function to catch unhandled exceptions.

    @param excType exception type
    @param excValue exception value
    @param tracebackobj traceback object
    """

    separator = '-' * 80 + '\n'
    tbinfofile = io.StringIO()
    traceback.print_tb(tracebackobj, None, tbinfofile)
    tbinfofile.seek(0)
    tbinfo = tbinfofile.read()
    errmsg = '%s: \n%s' % (str(excType), str(excValue))
    msg = separator + errmsg + '\n\n' + tbinfo + separator

    for line in msg.rstrip().splitlines():
        logger.log(logging.ERROR, line.rstrip())