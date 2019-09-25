#!/usr/bin/env python3.7
# -*- coding: utf-8 -*-
''' DesignSPHysics Executable Paths data '''

from mod.executable_tools import executable_contains_string


class ExecutablePaths():
    ''' Executables used by the application '''

    def __init__(self):
        # FIXME: This should try to retrieve default paths from a previously saved file or app defaults
        self.gencase: str = ''
        self.dsphysics: str = ''
        self.partvtk4: str = ''
        self.floatinginfo: str = ''
        self.computeforces: str = ''
        self.measuretool: str = ''
        self.isosurface: str = ''
        self.boundaryvtk: str = ''
        self.flowtool: str = ''
        self.paraview: str = ''

    def check_and_filter(self):
        ''' Filters the executable removing those not matching the correct application.
            Returns whether or not all of them were correctly set. '''
        execs_correct: bool = True
        execs_to_check = {
            "gencase": self.gencase,
            "dualsphysics": self.dsphysics,
            "partvtk4": self.partvtk4,
            "floatinginfo": self.floatinginfo,
            "computeforces": self.computeforces,
            "measuretool": self.measuretool,
            "isosurface": self.isosurface,
            "boundaryvtk": self.boundaryvtk,
            "flowtool": self.flowtool
        }

        for word, executable in execs_to_check.items():
            if not executable_contains_string(executable, word):
                execs_correct = False
                executable = ""

        return execs_correct
