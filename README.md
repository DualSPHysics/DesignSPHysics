# DesignSPHysics

DesignSPHysics is a software module built into [FreeCAD](http://www.freecadweb.org/) that provides a Graphical User Interface for [DualSPHysics](http://dual.sphysics.org/). It is under development since September 2016 and in Beta stage.

Check the [Official Webpage](http://design.sphysics.org) for downloads and more information.

![Screenshot](https://design.sphysics.org/img/github-shot-21112019.png)

## News
### Training courses
 * [8th DualSPHysics Workshop](https://dual.sphysics.org/8thworkshop/), Ourense, Spain, on **27-29 January, 2026**.
#### Past events
 * [SPH modelling For Engineering applications](https://sites.google.com/view/hykudsph/home?authuser=0), Braunschweig, Germany, on **25-27 March 2025**.
 * [4th Hands-on course on experimental and numerical modelling of wave-structure interaction](https://sites.google.com/unifi.it/hands-on-course-2024), Florence, Italy, on **1-5 July 2024**.
 * [7th DualSPHysics Workshop](https://dual.sphysics.org/7thworkshop/), Bari, Italy, on **19-21 March, 2024**.

### Releases
 * [v0.7.0](https://github.com/DualSPHysics/DesignSPHysics/releases/tag/0.7.0) has been released (15-09-2023). See [CHANGELOG file](CHANGELOG.md)

## Description
DesignSPHysics enables the user to create cases with solids and fluids and exports it to a DualSPHysics compatible format. In addition, it does the hard work for the user, generating the case data automatically, simulating, and post-processing, all inside FreeCAD.

It includes support for pre-processing with GenCase, simulation with DualSPHysics and post-processign with several tools of the DualSPHysics package.

In the future the code will be modular, so integration with different SPH solvers can be used. Right now it's optimized to be used with DualSPHysics

It is developed as a FreeCAD module with a macro bootstrapper, in Python 3.5+, using the QT libraries via PySide.

## Installation instructions
To install DesignSPHysics you have 2 options: Using the FreeCAD Addon manager for an stable version, or installing manually whatever version that you like from git.

### Installing a release version
To install a release version, open FreeCAD 0.18+ and go to the menu *Macro -> Macros...* From there, press the *Addons...* button on the bottom right corner, search for DesignSPHysics and click *Install / Update*. FreeCAD will advise you to reboot the application and you'll be set.

Take in mind that as it includes DualSPHysics, the package may take a while to download.

To execute DesignSPHysics just open the same Macro dialog and double click DualSPHysics.

### Installing a development build
Clone the branch that you like from this repository and rename the folder to 'DesignSPHysics'. Then copy the folder to the Mod folder of the FreeCAD installation directory. 

> Note: in FreeCAD 1.0 - flatpak - the repo should be cloned here:
`/home/ubuntu/.var/app/org.freecad.FreeCAD/data/FreeCAD/Mod/`

By default, for example, in Windows, it is located in `%appdata%/FreeCAD/Mod` or in Linux in `~/.FreeCAD/Mod`

Then copy the file `DesignSPHysics.FCMacro` of this repository into the FreeCAD macro directory (`%appdata%/FreeCAD/Macro` on Windows; `~/.FreeCAD/Macro` on GNU/Linux)

## Where to get help
The new [DualSPHysics forum](https://github.com/DualSPHysics/DualSPHysics/discussions) is available for help on using the features available in the solver.

You can check the [DesignSPHysics Wiki](http://design.sphysics.org/wiki) to get help. Also, you can post an [issue here on GitHub](https://github.com/DualSPHysics/DesignSPHysics/issues) or send an email to any of the people found in the [CONTRIBUTING file](CONTRIBUTING.md). 

## Contributing and developing for DesignSPHysics
You can freely contribute to the project, if you want!. You can do it here on GitHub.

Please check the [CONTRIBUTING file](CONTRIBUTING.md) to view information about how to contribute to the project.

## Copyright and License
Copyright (C) 2019
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
