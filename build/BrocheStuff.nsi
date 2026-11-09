; BrocheStuff installer - per-user, no admin rights
Unicode true
!include "MUI2.nsh"
!include "x64.nsh"
!ifndef VER
  !define VER "0.0.0"
!endif
Name "BrocheStuff"
OutFile "BrocheStuff-Setup-${VER}.exe"
InstallDir "$LOCALAPPDATA\Programs\BrocheStuff"
InstallDirRegKey HKCU "Software\BrocheStuff" "InstallDir"
RequestExecutionLevel user
SetCompressor /SOLID lzma
VIProductVersion "${VER}.0"
VIAddVersionKey "ProductName" "BrocheStuff"
VIAddVersionKey "FileDescription" "BrocheStuff installer"
VIAddVersionKey "FileVersion" "${VER}"
VIAddVersionKey "ProductVersion" "${VER}"
VIAddVersionKey "CompanyName" "Achraf El Ghaffouli"
VIAddVersionKey "LegalCopyright" "Achraf El Ghaffouli"
!define MUI_ICON "app.ico"
!define MUI_UNICON "app.ico"
!define MUI_ABORTWARNING
!define MUI_FINISHPAGE_RUN "$INSTDIR\BrocheStuff.exe"
!define MUI_FINISHPAGE_SHOWREADME ""
!define MUI_FINISHPAGE_SHOWREADME_TEXT "$(DeskShort)"
!define MUI_FINISHPAGE_SHOWREADME_FUNCTION MakeDesk
!insertmacro MUI_PAGE_WELCOME
!insertmacro MUI_PAGE_DIRECTORY
!insertmacro MUI_PAGE_INSTFILES
!insertmacro MUI_PAGE_FINISH
!insertmacro MUI_UNPAGE_CONFIRM
!insertmacro MUI_UNPAGE_INSTFILES
!insertmacro MUI_LANGUAGE "French"
!insertmacro MUI_LANGUAGE "English"
LangString DeskShort ${LANG_FRENCH} "Créer un raccourci sur le Bureau"
LangString DeskShort ${LANG_ENGLISH} "Create a desktop shortcut"
Function .onInit
  ${If} ${Silent}
  ${EndIf}
FunctionEnd
Function MakeDesk
  CreateShortCut "$DESKTOP\BrocheStuff.lnk" "$INSTDIR\BrocheStuff.exe" "" "$INSTDIR\BrocheStuff.exe" 0
FunctionEnd
Section "BrocheStuff"
  SetOutPath "$INSTDIR"
  ; close a running copy so its files can be replaced
  nsExec::Exec 'taskkill /F /IM BrocheStuff.exe'
  File "pkg\BrocheStuff\BrocheStuff.exe"
  File "pkg\BrocheStuff\resources.neu"
  File "pkg\BrocheStuff\README.txt"
  File "pkg\BrocheStuff\FOR_IT.txt"
  File "pkg\BrocheStuff\SHA256SUMS.txt"
  WriteUninstaller "$INSTDIR\Uninstall.exe"
  CreateShortCut "$SMPROGRAMS\BrocheStuff.lnk" "$INSTDIR\BrocheStuff.exe" "" "$INSTDIR\BrocheStuff.exe" 0
  WriteRegStr HKCU "Software\BrocheStuff" "InstallDir" "$INSTDIR"
  !define UK "Software\Microsoft\Windows\CurrentVersion\Uninstall\BrocheStuff"
  WriteRegStr HKCU "${UK}" "DisplayName" "BrocheStuff"
  WriteRegStr HKCU "${UK}" "DisplayVersion" "${VER}"
  WriteRegStr HKCU "${UK}" "Publisher" "Achraf El Ghaffouli"
  WriteRegStr HKCU "${UK}" "DisplayIcon" "$INSTDIR\BrocheStuff.exe"
  WriteRegStr HKCU "${UK}" "InstallLocation" "$INSTDIR"
  WriteRegStr HKCU "${UK}" "UninstallString" '"$INSTDIR\Uninstall.exe"'
  WriteRegStr HKCU "${UK}" "QuietUninstallString" '"$INSTDIR\Uninstall.exe" /S'
  WriteRegDWORD HKCU "${UK}" "NoModify" 1
  WriteRegDWORD HKCU "${UK}" "NoRepair" 1
SectionEnd
Section "Uninstall"
  nsExec::Exec 'taskkill /F /IM BrocheStuff.exe'
  Delete "$INSTDIR\BrocheStuff.exe"
  Delete "$INSTDIR\resources.neu"
  Delete "$INSTDIR\README.txt"
  Delete "$INSTDIR\FOR_IT.txt"
  Delete "$INSTDIR\SHA256SUMS.txt"
  Delete "$INSTDIR\Uninstall.exe"
  RMDir "$INSTDIR"
  Delete "$SMPROGRAMS\BrocheStuff.lnk"
  Delete "$DESKTOP\BrocheStuff.lnk"
  DeleteRegKey HKCU "Software\Microsoft\Windows\CurrentVersion\Uninstall\BrocheStuff"
  DeleteRegKey HKCU "Software\BrocheStuff"
SectionEnd
