#!/usr/bin/env python3.7
# -*- coding: utf-8 -*-
"""DesignSPHysics Execution Parameters.

This file contains a collection of 
Execution Parameters to add
in a DSPH related case.

"""

import sys

# Copyright (C) 2019
# EPHYSLAB Environmental Physics Laboratory, Universidade de Vigo
#
# This file is part of DesignSPHysics.
#
# DesignSPHysics is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# DesignSPHysics is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with DesignSPHysics.  If not, see <http://www.gnu.org/licenses/>.


class DomainFixedParameter(object):
    """ Fixed Domain for a DSPH case.

    Attributes:
        xmin = Minimun X coordinate for the fixed domain
        xmax = Maximum X coordinate for the fixed domain
        ymin = Minimun Y coordinate for the fixed domain
        ymax = Maximum Y coordinate for the fixed domain
        zmin = Minimun Z coordinate for the fixed domain
        zmax = Maximum Z coordinate for the fixed domain
    """

    def __init__(self, enabled, xmin, xmax, ymin, ymax, zmin, zmax):
        self.enabled = enabled
        self.xmin = xmin
        self.xmax = xmax
        self.ymin = ymin
        self.ymax = ymax
        self.zmin = zmin
        self.zmax = zmax

    def __str__(self):
        to_ret = """
            Enabled: {}\n
            Xmin & Xmax: {} ; {}\n
            Ymin & Ymax: {} ; {}\n
            Zmin & Zmax: {} ; {}\n
            """
        return to_ret.format(self.enabled, self.xmin, self.xmax, self.ymin, self.ymax,
                     self.zmin, self.zmax)
