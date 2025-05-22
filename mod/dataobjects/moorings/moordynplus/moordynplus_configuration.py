#!/usr/bin/env python3.7
# -*- coding: utf-8 -*-
""" DesignSPHysics MoorDynPlus specific configuration. """

from mod.dataobjects.moorings.moordynplus.moordynplus_solver_options import MoorDynPlusSolverOptions
from mod.dataobjects.moorings.moordynplus.moordynplus_line_default_configuration import MoorDynPlusLineDefaultConfiguration
from mod.dataobjects.moorings.moordynplus.moordynplus_output_configuration import MoorDynPlusOutputConfiguration


class MoorDynPlusConfiguration():
    """ A MoorDynPlus specific configuration object to couple with the already existing solver. """

    def __init__(self):
        self.solver_options: MoorDynPlusSolverOptions = MoorDynPlusSolverOptions()
        self.bodies: list = list()  # MoorDynPlusBody
        self.connects: list = list()  # MoorDynPlusConnect
        self.line_default_configuration: MoorDynPlusLineDefaultConfiguration = MoorDynPlusLineDefaultConfiguration()
        self.lines: list = list()  # MoorDynPlusLine
        self.output_configuration: MoorDynPlusOutputConfiguration = MoorDynPlusOutputConfiguration()
