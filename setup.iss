; Script generated by the Inno Setup Script Wizard.
; SEE THE DOCUMENTATION FOR DETAILS ON CREATING INNO SETUP SCRIPT FILES!

#define MyAppName "%(name)s"
#define MyAppVerName "%(name)s %(version)s"
#define MyAppURL "%(url)s"
#define MyAppExeName "%(name)s.exe"

[Setup]
; NOTE: The value of AppId uniquely identifies this application.
; Do not use the same AppId value in installers for other applications.
; (To generate a new GUID, click Tools | Generate GUID inside the IDE.)
AppId={{E279FAC7-0713-4CCC-8844-7AEE77BA9476}
AppName={#MyAppName}
AppVerName={#MyAppVerName}
AppSupportURL={#MyAppURL}
AppUpdatesURL={#MyAppURL}
DefaultDirName={pf}\%(name)s
DefaultGroupName={#MyAppName}
LicenseFile=%(source)s\LICENSE.txt
InfoBeforeFile=%(source)s\README.txt
OutputDir=%(source)s\dist
OutputBaseFilename=%(name)s-setup
Compression=lzma
SolidCompression=yes
AlwaysRestart=false
MinVersion=0,5.01.2600sp1
PrivilegesRequired=admin

[Languages]
Name: english; MessagesFile: compiler:Default.isl

[Tasks]
Name: desktopicon; Description: {cm:CreateDesktopIcon}; GroupDescription: {cm:AdditionalIcons}; 

[Files]
Source: %(source)s\dist-win32\%(name)s.exe; DestDir: {app}; Flags: ignoreversion restartreplace 
; NOTE: Don't use "Flags: ignoreversion" on any shared system files

[Registry]
Root: HKCR; Subkey: %(protocol)s; ValueType: string; ValueData: URL: %(protocol)s protocol handler; Flags: uninsdeletekey deletekey
Root: HKCR; Subkey: %(protocol)s; ValueType: string; ValueName: URL Protocol; Flags: uninsdeletekey deletekey
Root: HKCR; Subkey: %(protocol)s\DefaultIcon; ValueType: string; ValueData: {app}\%(name)s.exe; Flags: uninsdeletekey deletekey
Root: HKCR; Subkey: %(protocol)s\shell\open\command; ValueType: string; ValueData: "{app}\%(name)s ""%%1"""; Flags: uninsdeletekey deletekey
Root: HKCR; Subkey: %(protocol)ss; ValueType: string; ValueData: URL: %(protocol)ss protocol handler; Flags: uninsdeletekey deletekey
Root: HKCR; Subkey: %(protocol)ss; ValueType: string; ValueName: URL Protocol; Flags: uninsdeletekey deletekey
Root: HKCR; Subkey: %(protocol)ss\DefaultIcon; ValueType: string; ValueData: {app}\%(name)s.exe; Flags: uninsdeletekey deletekey
Root: HKCR; Subkey: %(protocol)ss\shell\open\command; ValueType: string; ValueData: "{app}\%(name)s ""%%1"""; Flags: uninsdeletekey deletekey

[Icons]
Name: {group}\{#MyAppName}; Filename: {app}\{#MyAppExeName}
Name: {commondesktop}\{#MyAppName}; Filename: {app}\{#MyAppExeName}; Tasks: desktopicon
Name: {commonstartup}\{#MyAppName}; Filename: {app}\{#MyAppExeName}
