; Inno setup Script
; 

#define Name "UartVide-SCT"
#define Version "1.2"
#define Copyright "Copyright (C) 2013-2026 gamesun"

[Setup]
AppId={{48E4C77E-F19E-44F1-98CC-F4F3F466637B}
AppName={#Name}
AppVersion={#Version}
DefaultDirName={autopf}\{#Name}
DefaultGroupName={#Name}
UninstallDisplayIcon={app}\{#Name}.exe
UninstallDisplayName={#Name} {#Version}
VersionInfoVersion={#Version}
AppPublisher=gamesun
AppPublisherURL=http://sourceforge.net/projects/myterm/
AppCopyright={#Copyright}
OutputBaseFilename={#Name}-{#Version}-win64
OutputDir=Release
DisableDirPage=no
DisableProgramGroupPage=no
LicenseFile=..\LICENSE.txt
ShowTasksTreeLines=yes
AppMutex={#Name}Mutex
SetupMutex={#Name}Mutex
WizardStyle=modern
PrivilegesRequired=lowest
DisableWelcomePage=no
CloseApplicationsFilter=*.*

[Files]
Source: "dist\uartvide-sct\*"; DestDir: "{app}"; Flags: recursesubdirs
Source: "..\LICENSE.txt"; DestDir: "{app}"
Source: "..\readme.htm"; DestDir: "{app}"

[Dirs]
Name: "{app}\Settings"; Flags: uninsneveruninstall

; [UninstallDelete]
; Type: filesandordirs; Name: "{app}\Settings"

[Icons]
; add icon to desktop
Name: "{autodesktop}\{#Name} {#Version}"; Filename: "{app}\{#Name}.exe"

; add icons to Start Menu/All Programs
Name: "{autoprograms}\{#Name} {#Version}\{#Name} {#Version}"; Filename: "{app}\{#Name}.exe"; WorkingDir: "{app}"
Name: "{autoprograms}\{#Name} {#Version}\Uninstall {#Name} {#Version}"; Filename: "{uninstallexe}"

[Run]
Filename: "{app}\{#Name}.exe"; Description: "Launch application"; \
    Flags: postinstall nowait skipifsilent


[code]

function IsAppRunning(const FileName: string): Boolean;
var
  FWMIService: Variant;
  FSWbemLocator: Variant;
  FWbemObjectSet: Variant;
begin
  Result := false;
  FSWbemLocator := CreateOleObject('WBEMScripting.SWBEMLocator');
  FWMIService := FSWbemLocator.ConnectServer('', 'root\CIMV2', '', '');
  FWbemObjectSet := FWMIService.ExecQuery(Format('SELECT Name FROM Win32_Process Where Name="%s"',[FileName]));
  Result := (FWbemObjectSet.Count > 0);
  FWbemObjectSet := Unassigned;
  FWMIService := Unassigned;
  FSWbemLocator := Unassigned;
end;

function InitializeUninstall(): Boolean;
begin
  if IsAppRunning('{#Name}.exe') then
    begin
      MsgBox('checked APP({#Name}.exe) is running, Please close it and retry!', mbError, MB_OK);
    end
  else
    begin
      Result := MsgBox('Uninstall:' #13#13 'Do you really want to start Uninstall?', mbConfirmation, MB_YESNO) = idYes;
    end
end;
