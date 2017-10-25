#!/bin/bash

echo "------- Autoexported by DesignSPHysics -------"

# "name" and "dirout" are named according to the testcase

name=dam-break
dirout=${name}_out


# "executables" are renamed and called from their directory

gencase="/home/ndrs/.FreeCAD/Mod/DesignSPHysics/dsphfc/../dualsphysics/EXECS/GenCase4_linux64"
dualsphysics="/home/ndrs/.FreeCAD/Mod/DesignSPHysics/dsphfc/../dualsphysics/EXECS/DualSPHysics4_linux64"
partvtk="/home/ndrs/.FreeCAD/Mod/DesignSPHysics/dsphfc/../dualsphysics/EXECS/PartVTK4_linux64"

# Library path must be indicated properly

current=$(pwd)
cd "/home/ndrs/.FreeCAD/Mod/DesignSPHysics/dsphfc/../dualsphysics/EXECS"
path_so=$(pwd)
cd $current
export LD_LIBRARY_PATH=$path_so

echo "This script executes GenCase for the case saved, that generates output files in the *_Out dir. Then, executes a simulation on CPU/GPU of the case. Last, it exports all the geometry generated in VTK files for viewing with ParaView."
read -n1 -r -p "Press any key to continue..." key

# "dirout" is created to store results or it is cleaned if it already exists

if [ -e $dirout ]; then
  rm -f -r $dirout
fi
mkdir $dirout


# CODES are executed according the selected parameters of execution in this testcase
errcode=0

if [ $errcode -eq 0 ]; then
  $gencase ${name}_Def $dirout/${name} -save:all
  errcode=$?
fi

if [ $errcode -eq 0 ]; then
  $dualsphysics $dirout/${name} $dirout -svres -cpu 
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
