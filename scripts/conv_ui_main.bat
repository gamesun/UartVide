@echo off

if exist ".\envsetup.bat" (
  call .\envsetup.bat
) else (
  echo "%cd%\.\envsetup.bat not found!"
  pause
  exit
)

%PY_PATH%\Scripts\pyside2-uic.exe ../ui/mainwindow.ui -o ../src/ui_mainwindow.py

rem pause