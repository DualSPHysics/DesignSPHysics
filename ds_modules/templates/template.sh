#!/bin/bash

echo "------- Autoexported by {app_name} -------"

# "name" and "dirout" are named according to the testcase

name={case_name}
dirout=${{name}}_out


# "executables" are renamed and called from their directory

gencase="{gcpath}"
dualsphysics="{dsphpath}"
partvtk="{pvtkpath}"

# Library path must be indicated properly

current=$(pwd)
cd "{lib_path}"
path_so=$(pwd)
cd $current
export LD_LIBRARY_PATH=$path_so

echo "This script executes GenCase for the case saved, that generates output files in the *_out dir. Then, executes a simulation on CPU/GPU of the case. Last, it exports all the geometry generated in VTK files for viewing with ParaView."
read -n1 -r -p "Press any key to continue..." key

# "dirout" is created to store results or it is cleaned if it already exists

if [ -e $dirout ]; then
  rm -f -r $dirout
fi
mkdir $dirout


# CODES are executed according the selected parameters of execution in this testcase
errcode=0

if [ $errcode -eq 0 ]; then
  $gencase ${{name}}_Def $dirout/${{name}} -save:all
  errcode=$?
fi

if [ $errcode -eq 0 ]; then
  $dualsphysics $dirout/${{name}} $dirout -svres {exec_params}
  errcode=$?
fi

if [ $errcode -eq 0 ]; then
  $partvtk -dirin $dirout -savevtk $dirout/PartFluid -onlytype:-all,+fluid
  errcode=$?
fi


if [ $errcode -eq 0 ]; then
  echo All done
else
  echo Execution aborted
fi
read -n1 -r -p "Press any key to continue..." key
echo
