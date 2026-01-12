@echo off

if exist "..\..\scripts\envsetup.bat" (
  call ..\..\scripts\envsetup.bat
) else (
  echo "%cd%\..\..\scripts\envsetup.bat not found!"
  pause
  exit
)

%PY_PATH%\Scripts\pyside2-uic.exe mainwindow.ui -o mainwindow_ui.py

pause