@echo off

echo "------- Autoexported by {app_name} -------"

rem "name" and "dirout" are named according to the testcase

set name="{case_name}"
set dirout=%name%_out

rem "executables" are renamed and called from their directory

set gencase="{gcpath}"
set dualsphysics="{dsphpath}"
set partvtk="{pvtkpath}"

echo "This script executes GenCase for the case saved, that generates output files in the *_out dir. Then, executes a simulation on CPU/GPU of the case. Last, it exports all the geometry generated in VTK files for viewing with ParaView."
pause

rem "dirout" is created to store results or it is removed if it already exists

if exist %dirout% del /Q %dirout%\*.*
if not exist %dirout% mkdir %dirout%

%gencase% %name%_Def %dirout%/%name% -save:all
if not "%ERRORLEVEL%" == "0" goto fail

%dualsphysics% %dirout%/%name% %dirout% -svres {exec_params}
if not "%ERRORLEVEL%" == "0" goto fail

%partvtk% -dirin %dirout% -savevtk %dirout%/PartFluid
if not "%ERRORLEVEL%" == "0" goto fail

:success
echo "------- Execution complete. If results were not the expected ones check for errors. Make sure your case has a correct DP specification. -------"
goto end

:fail
echo Execution aborted.

:end
pause
