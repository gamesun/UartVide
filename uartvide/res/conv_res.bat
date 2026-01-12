@echo off

if exist "..\..\scripts\envsetup.bat" (
  call ..\..\scripts\envsetup.bat
) else (
  echo "%cd%\..\..\scripts\envsetup.bat not found!"
  pause
  exit
)

%PY_PATH%\Scripts\pyside2-rcc.exe resources.qrc -o resources_rc.py

pause