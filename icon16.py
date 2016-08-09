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

icon16 = PyEmbeddedImage(
    "iVBORw0KGgoAAAANSUhEUgAAACAAAAAgCAYAAABzenr0AAAABHNCSVQICAgIfAhkiAAABB1J"
    "REFUWIXll11v00gUhh9/u6FOqAoSlgIEWlHBXYW4Q7v7+0GIu8IFRaZS61IaxXHSejwzntkL"
    "ZLdpk6WIIi72SJHiyJ7znK/3OI7jevxJc/+od8D/5++/rLX2zwF4nkeapqRpSpIk3LlzB8dx"
    "foszay1nZ2fM53OOjo44OjrCBxgOh7x69Yo0TXnw4AGe93v6QmvN169fOT4+5s2bNxcA/X6f"
    "4XCI1pr9/X1msxllWdI0za049jyPfr9PkiT0ej2GwyEfP34E+A6wvr5Omqbs7e3x/v17sizj"
    "4OAAKeWtAIRhyKNHjxiNRuzu7vLixQvW19cvADzPIwgCyrJkf3+fw8NDTk9P8TyPXq8HQNM0"
    "OI6D53kre8RaS9M0NE2D1rr77rpud8bW1hZBEHRl9i8fMJ1O+fLlC9PpFK01SZJw//59HMeh"
    "rmscxyGO45U90jQNQgiklNR13X2klIzHY7TWTKfThWf8ZQdYa+n1ejx8+JDnz5+jlOLk5ASl"
    "FGEYdhG1Zozpoo3jGCklQgjOz88xxqCUQmuNEOJaXy0AtBZFEf1+n+3tbV6/fk1Zluzt7VGW"
    "5TXnLXhd1yiliOO4c+b7fgeyyv5TCeu6Zjqd4vs+o9GI4XBIFEXX7rPWYozBGMPPitrSDLSl"
    "ODw85N27d2xvb/Ps2TOSJKEoCoQQS+9XSi1c13X9w1FeCqC1pq5rrLWsra1hrWU8HjObzQiC"
    "gLt37xJFUdeMSinKsmQ+nzObzRBC/BpAW9ONjQ12d3eZz+e8ffuWpmm4d+8eaZqyublJHMcA"
    "VFXFt2/fyPMcIQRVVf06gJSS2WzGeDzm9PSUT58+4fs+vu8TxzFRFKG1BliIuK7r7rodSSnl"
    "ytFdWQIpJR8+fODs7AxjDPP5nDAMMcaQ5/lCCdqMnZ+fM5lMFiCqqurG96cyIIQgz3OKoiAM"
    "Q6IoIo5jqqr6oRC12Wj1QCn1cxloI2rrp5TqormpErZyLIRAa931y40A2iloa9yKTxAEncA4"
    "jtPtBGst1tqudO04GmM69WvPunEGhBBdpC2AlJKqqgiCYGGhNE2DUgqlVCdIVwFWTcNSAGNM"
    "t80uA3QP+f7SJrwapTEGKWWnlDcGuJyJdgteNtd1F35v1/BVJ63jZftjKYDned2Mh2G4sm5t"
    "va/aVVDHcXBdlyAIWFtbo9fr4fuLMS9cDQYDHj9+3B1+W29EURTx5MkTdnZ22NzcvA7Qdn2S"
    "JGxtbXWZuC2AOI67hTYYDBb6xQcoioIsy4jjmJcvX7Kzs3OrL6W+77OxscFgMMB1XbIsoyiK"
    "C4DJZMLnz58ZjUY8ffqUIAhuxfFVU0pxcHBAlmVMJpMLgOPjY4wxZFlGv9//z679FTPGUJYl"
    "RVFwcnLyHaBpGvI8J8/z3+L0R+b87/8d/wvSDfrPv2oxCwAAAABJRU5ErkJggg==")
geticon16Data = icon16.GetData
geticon16Image = icon16.GetImage
geticon16Bitmap = icon16.GetBitmap
geticon16Icon = icon16.GetIcon

