#!/usr/bin/env python3.7
# -*- coding: utf-8 -*-
""" DesignSPHysics MoorDyn specific configuration. """

from mod.dataobjects.moorings.moordyn.moordyn_solver_options import MoorDynSolverOptions
from mod.dataobjects.moorings.moordyn.moordyn_line_default_configuration import MoorDynLineDefaultConfiguration
from mod.dataobjects.moorings.moordyn.moordyn_output_configuration import MoorDynOutputConfiguration


class MoorDynConfiguration():
    """ A MoorDyn specific configuration object to couple with the already existing solver. """

    def __init__(self):
        self.solver_options: MoorDynSolverOptions = MoorDynSolverOptions()
        self.bodies: list = list()  # MoorDynBody
        self.connects: list = list()  # MoorDynConnect
        self.line_default_configuration: MoorDynLineDefaultConfiguration = MoorDynLineDefaultConfiguration()
        self.lines: list = list()  # MoorDynLine
        self.output_configuration: MoorDynOutputConfiguration = MoorDynOutputConfiguration()
