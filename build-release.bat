@echo off
rem This script sets up build requirements to generate an exe with pyinstaller
mkdir release-windows
cd release-windows
pyinstaller --onefile --windowed --icon=..\installer\resource\install.ico ..\installer\installer.py
xcopy .\dist\installer.exe .\ /Y
xcopy ..\installer\resource .\resource\ /S /E /Y
xcopy ..\DesignSPHysics.py .\resource /Y
xcopy ..\DesignSPHysics.FCMacro .\resource /Y
xcopy ..\default-config.json .\resource /Y
xcopy ..\LICENSE .\resource /Y
xcopy ..\images .\resource\images\ /S /E /Y
xcopy ..\mod .\resource\mod\ /S /E /Y
xcopy ..\dualsphysics .\resource\dualsphysics\ /S /E /Y
del .\installer.spec /Q
rmdir .\build /S /Q
rmdir .\dist /S /Q