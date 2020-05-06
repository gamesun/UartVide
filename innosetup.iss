; Inno setup Script
; 

#define AppName "MyTerm"
#define AppVersion "2.1.0"

[Setup]
AppName={#AppName}
AppVersion={#AppVersion}
DefaultDirName={pf}\{#AppName}
DefaultGroupName={#AppName}
UninstallDisplayIcon={app}\{#AppName}.exe
UninstallDisplayName={#AppName} {#AppVersion}
VersionInfoVersion={#AppVersion}
AppPublisher="gamesun"
AppCopyright="Copyright (C) 2013-2020 gamesun"
OutputBaseFilename={#AppName}-{#AppVersion}-win32
OutputDir=Release
DisableDirPage=no
DisableProgramGroupPage=no
LicenseFile=LICENSE.txt

[Files]
Source: "build\exe.win32-3.4\*"; DestDir: "{app}"
Source: "build\exe.win32-3.4\imageformats\*"; DestDir: "{app}\imageformats"
;Source: "build\exe.win32-3.4\platforms\*"; DestDir: "{app}\platforms"
Source: "LICENSE.txt"; DestDir: "{app}"
Source: "whatsnew.htm"; DestDir: "{app}"
Source: "Readme.txt"; DestDir: "{app}"; Flags: isreadme

[Icons]
; add icon to desktop
Name: "{commondesktop}\{#AppName}"; Filename: "{app}\{#AppName}.exe"

; add icons to Start Menu/All Programs
Name: "{group}\{#AppName}"; Filename: "{app}\{#AppName}.exe"; WorkingDir: "{app}"
Name: "{group}\Uninstall {#AppName}"; Filename: "{uninstallexe}"

[Run]
Filename: "{app}\{#AppName}.exe"; Description: "Launch application"; \
    Flags: postinstall nowait skipifsilent
Filename: "{app}\whatsnew.htm"; Description: "See what's new"; \
    Flags: postinstall nowait skipifsilent shellexec
