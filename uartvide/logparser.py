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

import datetime

class LogParser:

    def __init__(self) -> None:
        pass

    def parse(self, bytes):
        out = None
        if 18 <= len(bytes):
            if bytes[6:8] == b'\x43\x41':     # content
                isReport = True if bytes[8] == 1 else False
                ts_20ms = int.from_bytes(bytes[9:13], byteorder='big', signed=False)
                d = datetime.datetime.fromtimestamp(ts_20ms / 50, datetime.timezone.utc)
                time_str = d.strftime("%H:%M:%S.%f")[:-3]
                cmd_str = ' '.join(['%02X' % b for b in bytes[13:17]])
                # print(isReport, ts, cmd)
                if isReport:
                    out = f'[{time_str}]\t\t\t\t<---- {cmd_str}\n'
                else:
                    out = f'[{time_str}]\t{cmd_str} ---->\n'
        return out

