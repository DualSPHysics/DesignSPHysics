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
GRAVITY = "Gravitational acceleration."
RHOP0 = "Reference density of the fluid."
HSWL = "Maximum still water level to calculate speedofsound using coefsound."
GAMMA = "Polytropic constant for water used in the state equation."
SPEEDSYSTEM = "Maximum system speed (by default the dam-break propagation is used)."
COEFSOUND = "Coefficient to multiply speedsystem."
SPEEDSOUND = "Speed of sound to use in the simulation (by default speedofsound=coefsound*speedsystem)."
COEFH = "Coefficient to calculate the smoothing length (h=coefh*sqrt(3*dp^2) in 3D)."
CFLNUMBER = "Coefficient to multiply dt."
