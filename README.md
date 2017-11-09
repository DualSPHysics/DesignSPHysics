# DesignSPHysics
DesignSPHysics is a module intended for use with the simulator [DualSPHysics](http://dual.sphysics.org/) and [FreeCAD](http://www.freecadweb.org/?lang=es_ES)

It is under development since September 2016 and in Beta stage.

Check the [Official Webpage](http://design.sphysics.org)

![Screenshot](http://design.sphysics.org/img/github-shot.png)

## Description
DSPH for FreeCAD enables the user to create cases with solids and fluids and exports it to DualSPHysics compatbile format. In addition, it does the hard work for the user, generating the case automatically, simulating, and post-processing, all inside FreeCAD.

It includes support for pre-processing with GenCase, simulation with DualSPHysics and post-processign with several tools of the DualSPHysics package.

In the future the code will be modular, so integration with different SPH solvers can be used. Right now it's optimized to be used with DualSPHysics 4.X

It is developed as a FreeCAD module with a macro bootstrapper, in python 2.7.

## Installation instructions
To install DesignSPHysics you have 2 options: Using an installer (release version) or using a development build (git)

### Installing a release version
To install a release version go to the download section of the [official webpage](http://design.sphysics.org) and download the appropriate binary.

Execute the installer (installer.exe on Windows and installer on GNU/Linux) to open the installer. Then press install and it will copy the needed scripts in FreeCAD's macro default folder.

### Installing a develompent build
Clone this repository and rename the folder to 'DesignSPHysics'. Then copy the folder to the Mod folder of the FreeCAD installation directory. 

By default, for example, in Windows, it is located in `C:\Program Files\FreeCAD 0.16\Mod\`

Then copy the file `DesignSPHysics.FCMacro` of this repository into the FreeCAD macro directory (`%appdata%/FreeCAD/Macro` on Windows; `~/.FreeCAD/Macro` on GNU/Linux)


## Where to get help
You can check the [DesignSPHysics Wiki](http://design.sphysics.org/wiki) to get help.

## Contributing
Right now the application is in early stages, so the best way to contribute right now is to post issues and suggestions for the code.

Pull request will be considered but as it is under heavy development right now a lot of things are about to change, so new code / new functionalities are a bit tricky to integrate.

## Copyright and License
Copyright (C) 2017 - Andrés Vieira (anvieiravazquez@gmail.com)
EPHYSLAB Environmental Physics Laboratory, Universidade de Vigo
EPHYTECH Environmental Physics Technologies

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
