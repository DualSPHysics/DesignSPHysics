#!/usr/bin/env python3.7
# -*- coding: utf-8 -*-
""" DesignSPHysics Executable Paths data """



import os
import sys
import pickle

from mod.tools.executable_tools import executable_contains_string, get_executable_info_flag
from mod.tools.file_tools import get_saved_config_file, get_default_config_file
from mod.tools.dialog_tools import error_dialog, warning_dialog
from mod.tools.stdout_tools import debug

from mod.constants import LINE_END
from mod.constants import PICKLE_PROTOCOL


class ExecutablePaths():
    """ Executables used by the application """

    def __init__(self):
        self.gencase: str = ""
        self.dsphysics: str = ""
        self.partvtk: str = ""
        self.floatinginfo: str = ""
        self.computeforces: str = ""
        self.measuretool: str = ""
        self.isosurface: str = ""
        self.boundaryvtk: str = ""
        self.flowtool: str = ""
        self.bathymetrytool: str = ""
        self.paraview: str = ""
        self.vres: str = ""
        self.surfacesstl: str = ""

        self.load_defaults()
        self.restore_from_disk()

    def check_and_filter(self):
        """ Filters the executable removing those not matching the correct application.
            Returns whether or not all of them were correctly set. """
        execs_correct: bool = True
        self.load_defaults()
        self.restore_from_disk()
        execs_to_check = {
            "gencase": self.gencase,
            "dualsphysics": self.dsphysics,
            "partvtk": self.partvtk,
            "floatinginfo": self.floatinginfo,
            "computeforces": self.computeforces,
            "measuretool": self.measuretool,
            "isosurface": self.isosurface,
            "boundaryvtk": self.boundaryvtk,
            "flowtool": self.flowtool,
            "bathymetrytool": self.bathymetrytool,
            "surfacesstl": self.surfacesstl
        }

        bad_executables: list = list()

        for word, executable in execs_to_check.items():
            if not executable_contains_string(executable, word):
                warning_dialog("Executable {} is not valid".format(executable))
                execs_correct = False
                bad_executables.append(executable)

        if not execs_correct:
            error_dialog("One or more of the executables set on the configuration is not correct. Please see the details below.",
                         "These executables do not correspond to their appropriate tool or do not have execution permissions:\n\n{}".format(LINE_END.join(bad_executables)))

        self.persist()
        return execs_correct

    def supports_moorings(self) -> bool:
        """ Returns whether this package supports Moorings + MoorDynPlus or not. """
        supports_moorings="MoorDyn_Coupling" in (get_executable_info_flag(self.dsphysics)["Features"]) or "MoorDynPlus_Coupling" in get_executable_info_flag(self.dsphysics)["Features"]
        return supports_moorings


    def supports_chrono(self) -> bool:
        """ Returns whether this package supports CHRONO or not. """
        return bool(get_executable_info_flag(self.dsphysics)["Features"]["CHRONO_Coupling"])

    def supports_ddt_fourtakas(self) -> bool:
        """ Returns whether this package supports Fourtakas DDT or not. """
        return bool(get_executable_info_flag(self.dsphysics)["Features"]["DDT_Fourtakas"])

    def load_defaults(self) -> None:
        """ Load the default executables if they're bundled with DesignSPHysics. """
        default_data: dict = get_default_config_file()
        self.gencase = default_data["gencase"]
        self.dsphysics = default_data["dsphysics"]
        self.partvtk = default_data["partvtk"]
        self.floatinginfo = default_data["floatinginfo"]
        self.computeforces = default_data["computeforces"]
        self.measuretool = default_data["measuretool"]
        self.isosurface = default_data["isosurface"]
        self.boundaryvtk = default_data["boundaryvtk"]
        self.flowtool = default_data["flowtool"]
        self.bathymetrytool = default_data["bathymetrytool"]
        self.vres = default_data["dsphysics"]
        self.surfacesstl = default_data["surfacesstl"]

    def restore_from_disk(self) -> None:
        """ Tries to restore the saved paths from the persisted ones if they exist."""
        config_file: str = get_saved_config_file()
        # Check if file exists and has content
        if not os.path.exists(config_file) or os.path.getsize(config_file) == 0:
           return
        
        with open(config_file, "rb") as picklefile:
            obj: ExecutablePaths = pickle.load(picklefile)
            self.gencase = obj.gencase
            # self.dsphysics = obj.dsphysics # Commented to avoid incompatibilities from previous DS codes
            self.partvtk = obj.partvtk
            self.floatinginfo = obj.floatinginfo
            self.computeforces = obj.computeforces
            self.measuretool = obj.measuretool
            self.isosurface = obj.isosurface
            self.boundaryvtk = obj.boundaryvtk
            self.flowtool = obj.flowtool
            self.bathymetrytool = obj.bathymetrytool
            self.paraview = obj.paraview
            # self.vres = obj.dsphysics # Commented to avoid incompatibilities from previous DS codes
            self.surfacesstl = obj.surfacesstl

    def persist(self) -> None:
        """ Persists the current executable paths to disk for next Case instantiations to load. """
        with open(get_saved_config_file(), "wb") as picklefile:
            pickle.dump(self, picklefile, PICKLE_PROTOCOL)

    def __str__(self):
        return (
            "Gencase: {gencase}\n"
            "Dsphysics: {dsphysics}\n"
            "PartVTK: {partvtk}\n"
            "Floatinginfo: {floatinginfo}\n"
            "Computeforces: {computeforces}\n"
            "Measuretool: {measuretool}\n"
            "Isosurface: {isosurface}\n"
            "Boundaryvtk: {boundaryvtk}\n"
            "Flowtool: {flowtool}\n"
            "BathymetryTool: {bathymetrytool}\n"
            "Paraview: {paraview}\n"
        ).format(**self.__dict__)
