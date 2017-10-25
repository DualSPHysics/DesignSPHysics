@echo off

echo "------- Autoexported by DesignSPHysics -------"

rem "name" and "dirout" are named according to the testcase

set name="dam-break"
set dirout=%name%_out

rem "executables" are renamed and called from their directory

set gencase="/home/ndrs/.FreeCAD/Mod/DesignSPHysics/dsphfc/../dualsphysics/EXECS/GenCase4_linux64"
set dualsphysics="/home/ndrs/.FreeCAD/Mod/DesignSPHysics/dsphfc/../dualsphysics/EXECS/DualSPHysics4_linux64"
set partvtk="/home/ndrs/.FreeCAD/Mod/DesignSPHysics/dsphfc/../dualsphysics/EXECS/PartVTK4_linux64"

echo "This script executes GenCase for the case saved, that generates output files in the *_Out dir. Then, executes a simulation on CPU/GPU of the case. Last, it exports all the geometry generated in VTK files for viewing with ParaView."
pause

rem "dirout" is created to store results or it is removed if it already exists

if exist %dirout% del /Q %dirout%\*.*
if not exist %dirout% mkdir %dirout%

%gencase% %name%_Def %dirout%/%name% -save:all
if not "%ERRORLEVEL%" == "0" goto fail

%dualsphysics% %dirout%/%name% %dirout% -svres -cpu 
if not "%ERRORLEVEL%" == "0" goto fail

%partvtk% -dirin %dirout% -savevtk %dirout%/PartFluid
if not "%ERRORLEVEL%" == "0" goto fail

:success
echo "------- Execution complete. If results were not the exepected ones check for errors. Make sure your case has a correct DP specification. -------"
goto end

:fail
echo Execution aborted.

:end
pause
