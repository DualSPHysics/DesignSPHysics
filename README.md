# DesignSPHysics
DesignSPHysics is a module intended for use with the simulator [DualSPHysics](http://dual.sphysics.org/) and [FreeCAD](http://www.freecadweb.org/?lang=es_ES)

Check the [Official Webpage](http://dual.sphysics.org/gui)

## Description
DSPH for FreeCAD enables the user to create cases with solids and fluids and exports it to DualSPHysics compatbile format. In addition, it does the hard work for the user, generating the case automatically, simulating, and exporting, all inside FreeCAD.

It is developed as a FreeCAD macro, in python 2.7.

## Installation instructions
To install DesignSPHysics you have 2 options: Using an installer (release version) or using a development build (git)

### Installing a release version
To install a release version go to the download section of the [official webpage](http://dual.sphysics.org/gui) and download the appropiate binary. Execute the installer (installer.exe on Windows and installer on GNU/Linux) to open the installer. Then press install and it will copy the needed scripts in FreeCAD's macro default folder.

### Installing a develompent build
Clone this repository and copy DSHP.py and DSPH_Images to FreeCAD macro directory (%appdata%/FreeCAD/Macro on Windows; ~/.FreeCAD/Macro on GNU/Linux)

## Where to get help
You can check the [DesignSPHysics Wiki](http://dual.sphysics.org/gui/wiki) to get help.

## Copyright and License
Copyright (C) 2016 - Andrés Vieira (anvieiravazquez@gmail.com)

EPHYSLAB Environmental Physics Laboratory, Universidade de Vigo

This file is part of DesignSPHysics.

DesignSPHysics is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

DesignSPHysics is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with DesignSPHysics.  If not, see <http://www.gnu.org/licenses/>.