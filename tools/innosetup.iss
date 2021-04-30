; Inno setup Script
; 

#define AppName "MyTerm"
#define AppVersion "2.3.0"

[Setup]
AppName={#AppName} {#AppVersion}
AppVersion={#AppVersion}
AppVerName={#AppName} {#AppVersion}
DefaultDirName={autopf32}\{#AppName} {#AppVersion}
DefaultGroupName={#AppName} {#AppVersion}
UninstallDisplayIcon={app}\{#AppName}.exe
UninstallDisplayName={#AppName} {#AppVersion}
VersionInfoVersion={#AppVersion}
AppPublisher=gamesun
AppPublisherURL=http://sourceforge.net/projects/myterm/
AppCopyright=Copyright (C) 2013-2021 gamesun
OutputBaseFilename={#AppName}-{#AppVersion}-win32
OutputDir=Release
DisableDirPage=no
DisableProgramGroupPage=no
LicenseFile=LICENSE.txt
ShowTasksTreeLines=yes
AppMutex={#AppName}Mutex
SetupMutex={#AppName}Mutex
WizardStyle=modern
PrivilegesRequired=lowest
DisableWelcomePage=no
CloseApplicationsFilter=*.*

[Files]
Source: "dist\{#AppName}\*"; DestDir: "{app}"; Flags: recursesubdirs
Source: "LICENSE.txt"; DestDir: "{app}"
Source: "whatsnew.htm"; DestDir: "{app}"

[UninstallDelete]
Type: filesandordirs; Name: "{app}\Settings"

[Icons]
; add icon to desktop
Name: "{userdesktop}\{#AppName} {#AppVersion}"; Filename: "{app}\{#AppName}.exe"

; add icons to Start Menu/All Programs
Name: "{userprograms}\{#AppName} {#AppVersion}\{#AppName} {#AppVersion}"; Filename: "{app}\{#AppName}.exe"; WorkingDir: "{app}"
Name: "{userprograms}\{#AppName} {#AppVersion}\Uninstall {#AppName} {#AppVersion}"; Filename: "{uninstallexe}"

[Run]
Filename: "{app}\{#AppName}.exe"; Description: "Launch application"; \
    Flags: postinstall nowait skipifsilent
Filename: "{app}\whatsnew.htm"; Description: "See what's new"; \
    Flags: postinstall nowait skipifsilent shellexec
