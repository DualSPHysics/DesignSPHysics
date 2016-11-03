@echo off
rem This script sets up build requirements to generate an exe with pyinstaller
mkdir release-windows
cd release-windows
pyinstaller --onefile --windowed --icon=..\installer\resource\install.ico ..\installer\installer.py
xcopy .\dist\installer.exe .\ /Y
xcopy ..\DSPH.py .\ /Y
xcopy ..\LICENSE .\ /Y
xcopy ..\DSPH_Images .\DSPH_Images\ /S /E /Y
xcopy ..\installer\resource .\resource\ /S /E /Y
del .\installer.spec /Q
rmdir .\build /S /Q
rmdir .\dist /S /Q
pause