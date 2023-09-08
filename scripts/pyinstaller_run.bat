@echo off

if exist ".\envsetup.bat" (
  call .\envsetup.bat
) else (
  echo "%cd%\.\envsetup.bat not found!"
  pause
  exit
)

%PY_PATH%\Scripts\pyinstaller --noconfirm pyinstaller_cfg.spec

pause