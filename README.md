# DualSPHysics for FreeCAD
DualSPHysics for FreeCAD is a module intended for use with the simulator [DualSPHysics](http://dual.sphysics.org/) and [FreeCAD](http://www.freecadweb.org/?lang=es_ES)

Check the [Official Webpage](http://dual.sphysics.org/gui)

## Description
DSPH for FreeCAD enables the user to create cases with solids and fluids and exports it to DualSPHysics compatbile format. In addition, it does the hard work for the user, generating the case automatically, simulating, and exporting, all inside FreeCAD.

It is developed as a FreeCAD macro, in python 2.7.

## Installation instructions
To install DualSPHysics for FreeCAD you have 2 options: Using an installer (release version) or using a development build (git)

### Installing a release version
To install a release version go to the download section of the [official webpage](http://dual.sphysics.org/gui) and download the appropiate binary. Execute the installer (installer.exe on Windows and installer on GNU/Linux) to open the installer. Then press install and it will copy the needed scripts in FreeCAD's macro default folder.

### Installing a develompent build
Clone this repository and copy DSHP.py and DSPH_Images to FreeCAD macro directory (%appdata%/FreeCAD/Macro on Windows; ~/.FreeCAD/Macro on GNU/Linux)

## Where to get help
You can check the [DualSPHysics for FreeCAD Wiki](http://dual.sphysics.org/wiki) to get help.
