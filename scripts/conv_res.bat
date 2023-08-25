@echo off

if exist ".\envsetup.bat" (
  call .\envsetup.bat
) else (
  echo "%cd%\.\envsetup.bat not found!"
  pause
  exit
)

%PY_PATH%\Scripts\pyside2-rcc.exe ../res/resources.qrc -o ../src/resources.py

pause