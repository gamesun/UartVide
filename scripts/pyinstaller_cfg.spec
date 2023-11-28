# -*- mode: python ; coding: utf-8 -*-


block_cipher = None

import os
if os.name == 'nt':
    icon_file = '../uartvide/res/uartvide-icon/uartvide.ico'
elif os.name == 'posix':
    icon_file = '../uartvide/res/uartvide-icon/uartvide_32.png'

a = Analysis(['../uartvide/uartvide.py'],
             pathex=[],
             binaries=[],
             datas=[],
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          [],
          exclude_binaries=True,
          name='uartvide-sct',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=False,
          console=False,
          version='version_info.txt',
          icon=icon_file)
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=False,
               upx_exclude=['qwindows.dll', 'qwindowsvistastyle.dll', 'qico.dll'],
               name='uartvide-sct')
