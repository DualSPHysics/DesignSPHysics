#!/usr/bin/env python3.7
# -*- coding: utf-8 -*-
""" DesignSPHysics Executable Paths data """

import pickle
import os

from mod.executable_tools import executable_contains_string
from mod.file_tools import get_saved_config_file, get_default_config_file
from mod.stdout_tools import debug

from mod.constants import PICKLE_PROTOCOL


class ExecutablePaths():
    """ Executables used by the application """

    def __init__(self):
        self.gencase: str = ""
        self.dsphysics: str = ""
        self.partvtk4: str = ""
        self.floatinginfo: str = ""
        self.computeforces: str = ""
        self.measuretool: str = ""
        self.isosurface: str = ""
        self.boundaryvtk: str = ""
        self.flowtool: str = ""
        self.paraview: str = ""

        self.restore_from_disk()

    def check_and_filter(self):
        """ Filters the executable removing those not matching the correct application.
            Returns whether or not all of them were correctly set. """
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
                debug("Executable {} does not contain the word {}".format(executable, word))
                execs_correct = False
                executable = ""

        self.persist()
        return execs_correct

    def load_defaults(self) -> None:
        """ Load the default executables if they're bundled with DesignSPHysics. """
        default_data: dict = get_default_config_file()
        self.gencase = default_data["gencase"]
        self.dsphysics = default_data["dsphysics"]
        self.partvtk4 = default_data["partvtk4"]
        self.floatinginfo = default_data["floatinginfo"]
        self.computeforces = default_data["computeforces"]
        self.measuretool = default_data["measuretool"]
        self.isosurface = default_data["isosurface"]
        self.boundaryvtk = default_data["boundaryvtk"]
        self.flowtool = default_data["flowtool"]

    def restore_from_disk(self) -> None:
        """ Tries to restore the saved paths from the persisted ones if they exist."""
        config_file: str = get_saved_config_file()
        if not os.path.exists(config_file):
            self.load_defaults()
            return
        with open(config_file, "rb") as picklefile:
            obj: ExecutablePaths = pickle.load(picklefile)
            self.gencase = obj.gencase
            self.dsphysics = obj.dsphysics
            self.partvtk4 = obj.partvtk4
            self.floatinginfo = obj.floatinginfo
            self.computeforces = obj.computeforces
            self.measuretool = obj.measuretool
            self.isosurface = obj.isosurface
            self.boundaryvtk = obj.boundaryvtk
            self.flowtool = obj.flowtool
            self.paraview = obj.paraview

    def persist(self) -> None:
        """ Persists the current executable paths to disk for next Case instantiations to load. """
        with open(get_saved_config_file(), "wb") as picklefile:
            pickle.dump(self, picklefile, PICKLE_PROTOCOL)
