#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
#
#############################################################################
##
## Copyright (c) 2013-2026, gamesun
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
from PySide2.QtCore import QObject, Signal

class LogParser:

    def __init__(self) -> None:
        pass

    def parse(self, bytes):
        out = ''
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


class CommandDetector(QObject):
    commandDetected = Signal(list)
    unknownData = Signal(list)

    def __init__(self, parent=None):
        super().__init__(parent)

        self._basic_status = 'h1'  # h1,h2,h3,l1,l2,typ,pld
        self._basic_len = 0
        self._basic_typ = 0
        self._basic_len_cnt = 0
        self._basic_buf = b''
        self._basic_header = b'\x84\xa9\x61'

    def setHeader(self, basic_header, log_header):
        self._basic_header = basic_header

    def parse(self, bytes):
        for b in bytes:
            self.__parse_basic(b)
        self.__flush_buff()

    def __parse_basic(self, byte):
        byte = byte.to_bytes(1, 'big')
        if 'h1' == self._basic_status:
            if byte == self._basic_header[0:1]:
                self.__flush_buff()
                self._basic_status = 'h2'
                self._basic_buf = byte
                self._basic_len_cnt = 0
            else:
                self._basic_buf = self._basic_buf + byte
        elif 'h2' == self._basic_status:
            if byte == self._basic_header[1:2]:
                self._basic_status = 'h3'
                self._basic_buf = self._basic_buf + byte
        elif 'h3' == self._basic_status:
            if byte == self._basic_header[2:3]:
                self._basic_status = 'l1'
                self._basic_buf = self._basic_buf + byte
        elif 'l1' == self._basic_status:
            self._basic_status = 'l2'
            self._basic_buf = self._basic_buf + byte
        elif 'l2' == self._basic_status:
            self._basic_status = 'typ'
            self._basic_buf = self._basic_buf + byte
            self._basic_len = int.from_bytes(self._basic_buf[-2:], byteorder='big', signed=False)
            if self._basic_len % 2:
                self._basic_len = self._basic_len + 1
            self._basic_len = self._basic_len + 6
            self._basic_len_cnt = 6
        elif 'typ' == self._basic_status:
            self._basic_status = 'pld'
            self._basic_buf = self._basic_buf + byte
            self._basic_typ = byte
        elif 'pld' == self._basic_status:    # payload
            self._basic_buf = self._basic_buf + byte
            self._basic_len_cnt = self._basic_len_cnt + 1
            if self._basic_len <= self._basic_len_cnt:
                self.commandDetected.emit([datetime.datetime.now().time(), self._basic_buf])
                # print('parser end', 'Rx:'+''.join('%02X ' % t for t in self._parser_buf))
                self._basic_status = 'h1'
                self._basic_buf = b''
                self._basic_len_cnt = 0
        else:
            self._basic_status = 'h1'
    
    def __flush_buff(self):
        if len(self._basic_buf):
            self.unknownData.emit([datetime.datetime.now().time(), self._basic_buf])
            self._basic_buf = b''

