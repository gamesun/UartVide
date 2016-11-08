#!/usr/bin/env python
# -*- coding: UTF-8 -*-
#
# Copyright (c) 2013-2014, gamesun
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are
# met:
#
#     * Redistributions of source code must retain the above copyright
# notice, this list of conditions and the following disclaimer.
#     * Redistributions in binary form must reproduce the above
# copyright notice, this list of conditions and the following disclaimer
# in the documentation and/or other materials provided with the
# distribution.
#     * Neither the name of gamesun nor the names of its contributors
# may be used to endorse or promote products derived from this software
# without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY GAMESUN "AS IS" AND ANY EXPRESS OR
# IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL GAMESUN BE LIABLE FOR ANY DIRECT,
# INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
# (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
# SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION)
# HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT,
# STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING
# IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.
#

from wx.lib.embeddedimage import PyEmbeddedImage

icon32 = PyEmbeddedImage(
    "iVBORw0KGgoAAAANSUhEUgAAACAAAAAgCAYAAABzenr0AAAABHNCSVQICAgIfAhkiAAAAz9J"
    "REFUWIXlVs9L40AU/pJMFRWKELwZ/SMEQQi4ngQR/CdEj9vVg4ceakHvey142asnEX9QEGEh"
    "UFHqyYP0tCB4Moe10CQzk8keZIZJmmq72LKwDx5J05d83/veezMD/O9m3N3dTV9fX1c8zyuN"
    "Eth13e97e3vfyP39fcnzvJLjOJiYmBgJeBAE8DyvVKvVfpNms7ls2zbK5fJIwKWVy2U0m81l"
    "AgC2bQMAXl9fUalU8PT0NBRQx3FQrVZRLBZh2zba7TaIHnB0dITj4+OhgANAo9GA4zjY2dlR"
    "z0he4MbGBsbHx1M+NjbW9ZsQAsMwwDkHpRRRFKmr7pRShGGIk5OTLiwzj4BhGJifn8fW1hbm"
    "5ubUM9M0YRiGuieEgBAC0zTVfzJWv3/PchVIkgQzMzNwXReu6+Li4gJXV1cQQkAIgTiOwTlX"
    "AJxzcM6RJAmSJIEQAkmSqG+9Z7kKCCFwe3uLw8NDvLy8YG1tDbu7uygUCuCcgzGGKIoQBAE6"
    "nQ7CMARjDIwxcM4Rx7FySVgI0b8C8qV2u41Op6MykSBCCHDOlbxJkihV3iPSNwHOOZaWltTa"
    "UK/XcX5+DsYYCCHgnMOyrBQBvTSShE5GlqwvAowxPD8/4+bmBpeXl2i1WiCEYHFxEaurq10N"
    "1mq1cHp6qpSRzhgDpVQRGYjA4+MjqtUqCCEoFAqI4xiUUszOzmJycjIV//DwgCAIlAq6EnJE"
    "ByJAKVUdLevHOYfneWg0Gl1jl42VJCSBgRWIoihV1ziOYVmWcjnn+ozLeL0XZCNKIgMpIIRQ"
    "Cw0hBJZlqcyl6yZnXx87vR8GIhBFUaqWevb6apgtQVYF+b6+cPVFIAzDVOY6uE4AeJuEPAJZ"
    "En+lgMzeNM2eBKRlSeiLkPSBFLAsS200WXBZf70E8prtBV2FgQno0svuz+56vRTQm3FgBWTj"
    "SMC85svrASA9Dbr32hVzCegZ6RtPHriMzarw0Tb8IYFehD7bUgQ2Nzc/HSBrWQwCAL7vIwgC"
    "FIvF1IFxWBYEAXzffztXLiws/Dw7O/tycHCgjufDNt/34fs+1tfXfxoAUKvV9uv1+lfG2PQo"
    "CExNTf1aWVn5sb29vT8KvH/b/gArZAfevTaT9AAAAABJRU5ErkJggg==")
geticon32Data = icon32.GetData
geticon32Image = icon32.GetImage
geticon32Bitmap = icon32.GetBitmap
geticon32Icon = icon32.GetIcon

