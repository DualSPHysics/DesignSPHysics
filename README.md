# DesignSPHysics

DesignSPHysics is a software module built into [FreeCAD](http://www.freecadweb.org/) that provides a Graphical User Interface for [DualSPHysics](http://dual.sphysics.org/). It is under development since September 2016 and in Beta stage.

Check the [Official Webpage](http://design.sphysics.org) for downloads and more information.

![Screenshot](https://design.sphysics.org/img/github-shot-21112019.png)

## Project Overview
DesignSPHysics enables the user to create cases with solids and fluids and exports it to a DualSPHysics compatible format. In addition, it does the hard work for the user, generating the case data automatically, simulating, and post-processing, all inside FreeCAD.

## News
### Training courses
 * [19th SPHERIC World Conference](https://spheric2025.upc.edu/), Barcelona, Spain, on **16-19 June, 2025**.
 * [8th DualSPHysics Workshop](https://dual.sphysics.org/8thworkshop/), Ourense, Spain, on **27-29 January, 2026**.
#### Past events
 * [SPH modelling For Engineering applications](https://sites.google.com/view/hykudsph/home?authuser=0), Braunschweig, Germany, on **25-27 March 2025**.
 * [4th Hands-on course on experimental and numerical modelling of wave-structure interaction](https://sites.google.com/unifi.it/hands-on-course-2024), Florence, Italy, on **1-5 July 2024**.
 * [7th DualSPHysics Workshop](https://dual.sphysics.org/7thworkshop/), Bari, Italy, on **19-21 March, 2024**.

### Releases
 * [v0.8.0](https://github.com/DualSPHysics/DesignSPHysics/releases/tag/0.8.0) (22-05-2023). See [CHANGELOG file](CHANGELOG.md)
 * [v0.7.0](https://github.com/DualSPHysics/DesignSPHysics/releases/tag/0.7.0) (15-09-2023).

It includes support for pre-processing with GenCase, simulation with DualSPHysics and post-processign with several tools of the DualSPHysics package.

In the future the code will be modular, so integration with different SPH solvers can be used. Right now it's optimized to be used with DualSPHysics

It is developed as a FreeCAD module with a macro bootstrapper, in Python 3.5+, using the QT libraries via PySide.

## Installation

To install DesignSPHysics, you have two options:

### Installing a Release Version
1. Open FreeCAD 0.18+ and navigate to `Macro -> Macros...`.
2. Press the `Addons...` button in the bottom-right corner, search for DesignSPHysics, and click `Install / Update`.
3. Reboot FreeCAD as advised, and you're ready to use the module.

### Installing a Development Build
1. Clone the branch of your choice from the repository and rename the folder to `DesignSPHysics`.
2. Copy this folder to the `Mod` folder in your FreeCAD installation directory:
    * On Windows: `%appdata%/FreeCAD/Mod`
    * On Linux: `~/.FreeCAD/Mod`
3. Copy the `DesignSPHysics.FCMacro` file from the repository into the FreeCAD macro directory:
    * On Windows: `%appdata%/FreeCAD/Macro`
    * On Linux: `~/.FreeCAD/Macro`


## Help and Support

For assistance, you can:

- Visit the [DualSPHysics forum](https://github.com/DualSPHysics/DualSPHysics/discussions).
- Check the [DesignSPHysics Wiki](http://design.sphysics.org/wiki).
- Post an [issue on GitHub](https://github.com/DualSPHysics/DesignSPHysics/issues).
- Contact contributors via the [CONTRIBUTING file](CONTRIBUTING.md).


## Contributing

Contributions are welcome! Please refer to the [CONTRIBUTING file](CONTRIBUTING.md) for detailed guidelines on how to contribute to the project.


## Copyright and License
Copyright (C) 2025, 
Ivan Martinez Estevez, Andres Vieira

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
