; SmartKey for Windows installer (Inno Setup 6). Per-user, no admin prompt, so the app can update itself.
;   iscc /DVersion=1.0.14 /DArch=x64 /DSrc=..\build\App Vikey.iss
#ifndef Version
  #define Version "0.0.0"
#endif
#ifndef Arch
  #define Arch "x64"
#endif
#ifndef Src
  #define Src "..\build\App"
#endif

[Setup]
AppId={{D447D06A-BCD6-4A33-B3F7-6A7816FEAE28}
AppName=SmartKey
AppVersion={#Version}
AppVerName=SmartKey {#Version}
AppPublisher=Hieu (SmartKey, based on Vikey by Tony Dinh)
AppPublisherURL=https://github.com/tdhieu94/SmartKey
AppSupportURL=https://github.com/tdhieu94/SmartKey/issues
AppUpdatesURL=https://github.com/tdhieu94/SmartKey/releases
VersionInfoVersion={#Version}
DefaultDirName={localappdata}\Programs\SmartKey
DisableDirPage=yes
DisableProgramGroupPage=yes
PrivilegesRequired=lowest
OutputDir=.\out
OutputBaseFilename=SmartKey-{#Version}-{#Arch}-Setup
SetupIconFile=..\App\Vikey.ico
UninstallDisplayIcon={app}\SmartKey.exe
UninstallDisplayName=SmartKey
Compression=lzma2/max
SolidCompression=yes
WizardStyle=modern
CloseApplications=yes
CloseApplicationsFilter=SmartKey.exe
RestartApplications=no
#if Arch == "arm64"
ArchitecturesAllowed=arm64
ArchitecturesInstallIn64BitMode=arm64
#else
ArchitecturesAllowed=x64compatible
ArchitecturesInstallIn64BitMode=x64compatible
#endif

[Languages]
Name: "en"; MessagesFile: "compiler:Default.isl"

[Messages]
; the few screens people see, in Vietnamese like the app
WelcomeLabel1=Cài đặt SmartKey
WelcomeLabel2=SmartKey {#Version} sẽ được cài cho tài khoản của bạn, không cần quyền quản trị.%n%nBấm Next để tiếp tục.
FinishedHeadingLabel=Đã cài xong SmartKey
FinishedLabel=SmartKey nằm ở khay hệ thống (góc dưới bên phải). Bấm Alt+Z để chuyển Anh/Việt.
ConfirmUninstall=Gỡ SmartKey khỏi máy?

[Files]
Source: "{#Src}\SmartKey.exe"; DestDir: "{app}"; Flags: ignoreversion

[Icons]
Name: "{autoprograms}\SmartKey"; Filename: "{app}\SmartKey.exe"

[Registry]
; the app's own "Mở SmartKey khi đăng nhập" entry goes away with the app
Root: HKCU; Subkey: "Software\Microsoft\Windows\CurrentVersion\Run"; ValueName: "SmartKey"; Flags: uninsdeletevalue dontcreatekey

[Run]
Filename: "{app}\SmartKey.exe"; Description: "Mở SmartKey"; Flags: nowait postinstall skipifsilent
; a self-update (SmartKey runs the installer silently with /RELAUNCH=1) brings the app back
Filename: "{app}\SmartKey.exe"; Flags: nowait; Check: ShouldRelaunch

[UninstallRun]
Filename: "{sys}\taskkill.exe"; Parameters: "/IM SmartKey.exe /F"; Flags: runhidden; RunOnceId: "KillSmartKey"

[Code]
function ShouldRelaunch: Boolean;
begin
  Result := ExpandConstant('{param:RELAUNCH|0}') = '1';
end;
