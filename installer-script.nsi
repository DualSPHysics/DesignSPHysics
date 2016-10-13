; example1.nsi
;
; This script is perhaps one of the simplest NSIs you can make. All of the
; optional settings are left to their default settings. The installer simply 
; prompts the user asking them where to install, and drops a copy of example1.nsi
; there. 

;--------------------------------

; The name of the installer
Name "DSPH Installer"

; The file to write
OutFile "setup.exe"

; The default installation directory
InstallDir $APPDATA\FreeCAD\Macro

; Request application privileges for Windows Vista
RequestExecutionLevel user

;--------------------------------

; Pages

Page directory
Page instfiles

;--------------------------------

; The stuff to install
Section "" ;No components page, name is not important

  ; Set output path to the installation directory.
  SetOutPath $INSTDIR
  
  ; Put file there
  File DSPH.py
  SetOutPath $INSTDIR\DSPH_Images
  File /nonfatal /a /r "DSPH_Images\"
  
SectionEnd ; end the section
