#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-
"""DesignSPHysics Define Constants.

This file contains a collection of constants meant to use with DesignSPHysics.

"""


"""
Copyright (C) 2016 - Andrés Vieira (anvieiravazquez@gmail.com) & Lorena Docasar Vázquez (docasarlorena@gmail.com)
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
"""

# ------ DEFINE CONSTANTS  ------

""" --------- ToolTip -------------- """

GRAVITY = "Gravitational acceleration."
RHOP0 = "Reference density of the fluid."
HSWL = "Maximum still water level to calculate speedofsound using coefsound."
GAMMA = "Polytropic constant for water used in the state equation."
SPEEDSYSTEM = "Maximum system speed (by default the dam-break propagation is used)."
COEFSOUND = "Coefficient to multiply speedsystem."
SPEEDSOUND = "Speed of sound to use in the simulation (by default speedofsound=coefsound*speedsystem)."
COEFH = "Coefficient to calculate the smoothing length (h=coefh*sqrt(3*dp^2) in 3D)."
CFLNUMBER = "Coefficient to multiply dt."

""" --------- Help Window -------------- """

HELP_GRAVITYX = "Gravity X"
HELP_GRAVITYY = "Gravity Y"
HELP_GRAVITYZ = "Gravity Z"
HELP_RHOP0 = "Fluid reference density"
HELP_HSWL = "HSWL"
HELP_GAMMA = "Gamma"
HELP_SPEEDSYSTEM = "Speedsystem"
HELP_COEFSOUND = "Coefsound"
HELP_SPEEDSOUND = "Speedsound"
HELP_COEFH = "CoefH"
HELP_CFLNUMBER = "cflnumber"


# ------ EXECUTION PARAMETERS  ------

""" --------- ToolTip -------------- """

POSDOUBLE = "Precision in particle interaction 0:Simple, 1:Double, 2:Uses and saves double (default=0)"
STEPALGORITHM = "Step Algorithm 1:Verlet, 2:Symplectic (default=1)"
VERLETSTEPS = "Verlet only: Number of steps to apply Euler timestepping (default=40)"
KERNEL = "Interaction Kernel 1:Cubic Spline, 2:Wendland, 3:Gaussian (default=2)"
VISCOTREATMENT = "Viscosity formulation 1:Artificial, 2:Laminar+SPS (default=1)"
VISCO = "Viscosity value"
VISCOBOUNDFACTOR = "Multiply viscosity value with boundary (default=1)"
DELTASPH = "DeltaSPH value, 0.1 is the typical value, with 0 disabled (default=0)"
SHIFTING = "Shifting mode 0:None, 1:Ignore bound, 2:Ignore fixed, 3:Full (default=0)"
SHIFTINGCOEF = "Coefficient for shifting computation (default=-2)"
SHIFTINGTFS = "Threshold to detect free surface. Typically 1.5 for 2D and 2.75 for 3D (default=0)"
RIGIDALGORITHM = "Rigid Algorithm 1:SPH, 2:DEM, 3:Chrono (default=1)"
FTPAUSE = "Time to freeze the floatings at simulation start (warmup) (default=0)"
DTINI = "Initial time step (default=h/speedsound)"
DTMIN = "Minimum time step (default=coefdtmin*h/speedsound)"
COEFDTMIN = "Coefficient to calculate minimum time step dtmin=coefdtmin*h/speedsound (default=0.05)"
TIMEMAX = "Time of simulation"
TIMEOUT = "Time out data"
INCZ = "Increase of Z+ (default=0)"
PARTSOUTMAX = "%%/100 of fluid particles allowed to be excluded from domain (default=1)"
RHOPOUTMIN = "Minimum rhop valid (default=700)"
RHOPOUTMAX = "Maximum rhop valid (default=1300)"
DOMAINFIXED = "The domain is fixed with the specified values (xmin:ymin:zmin:xmax:ymax:zmax)"

""" --------- Help Window -------------- """

HELP_VERLETSTEPS = "Verlet Steps"
HELP_VISCO = "Viscosity value"
HELP_VISCOBOUNDFACROT = "Viscosity factor with boundary"
HELP_DELTASPH = "Delta SPH value"
HELP_SHIFTINGCOEF = "Shifting Coefficient"
HELP_SHIFTINGTFS = "Free surface detection threshold"
HELP_FTPAUSE = "Floating freeze time"
HELP_DTINI = "Initial time step"
HELP_DTMIN = "Minimium time step"
HELP_COEFDTMIN = "Coefficient for minimum time step"
HELP_TIMEMAX = "Time of simulation"
HELP_TIMEOUT = "Time out data"
HELP_INCZ = "Increase of Z+ (%)"
HELP_PARTSOUTMAX = "%%/100 of fluid particles allowed to be excluded from domain"
HELP_RHOPOUTMIN = "Minimum rhop valid"
HELP_RHOPOUTMAX = "Maximum rhop valid"

