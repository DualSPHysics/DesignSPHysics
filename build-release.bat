@echo off
rem This script sets up build requirements to generate an exe with pyinstaller
mkdir release-windows
cd release-windows
pyinstaller --onefile --windowed --icon=..\installer\resource\install.ico ..\installer\installer.py
xcopy .\dist\installer.exe .\ /Y
xcopy ..\installer\resource .\resource\ /S /E /Y
xcopy ..\DesignSPHysics.py .\resource /Y
xcopy ..\DesignSPHysics.FCMacro .\resource /Y
xcopy ..\LICENSE .\resource /Y
xcopy ..\DSPH_Images .\resource\DSPH_Images\ /S /E /Y
xcopy ..\dsphfc .\resource\dsphfc\ /S /E /Y
xcopy ..\test-examples .\resource\test-examples\ /S /E /Y
xcopy ..\dualsphysics .\resource\dualsphysics\ /S /E /Y
del .\installer.spec /Q
rmdir .\build /S /Q
rmdir .\dist /S /Q