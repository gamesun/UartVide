#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
#
#############################################################################
##
## Copyright (c) 2013-2024, gamesun
## All right reserved.
##
## This file is part of UartVide(MyTerm).
##
## UartVide(MyTerm) is free software: you can redistribute it and/or
## modify it under the terms of the GNU General Public License as
## published by the Free Software Foundation, either version 3 of the
## License, or (at your option) any later version.
##
## UartVide(MyTerm) is distributed in the hope that it will be useful,
## but WITHOUT ANY WARRANTY; without even the implied warranty of
## MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
## GNU General Public License for more details.
##
## You should have received a copy of the GNU General Public License along
## with UartVide(MyTerm).  If not, see <http://www.gnu.org/licenses/>.
##
#############################################################################


import os

if os.name == 'nt':
    setting_root = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'Settings')
elif os.name == 'posix':
    setting_root = os.path.join(os.path.expanduser('~'), '.uartvide')

def ensure_root():
    if not os.path.isdir(setting_root):
        os.makedirs(setting_root)
    
def get_config_path(file_name):
    ensure_root()
    return os.path.join(setting_root, file_name)

