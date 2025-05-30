#!/usr/bin/env python3.7
# -*- coding: utf-8 -*-
""" DesignSPHysics Case Information Data """

from mod.dataobjects.bathymetry_form_data import BathymetryFormData
from os.path import isdir, isfile, dirname
from pathlib import Path

from mod.functions import migrate_state
from mod.tools.file_tools import load_default_materials


class CaseInformation():
    """ Stores miscellaneous information related with the case. """

    def __init__(self):
        self.particle_number: int = 0
        self.run_additional_parameters: str = ""
        self.recommends_to_run_gencase: bool = True #Recommends to run gencase
        self.current_output: str = ""
        self.last_3d_width: float = -1.0
        self.global_movements: list = list()  # [Movement]
        self.global_materials: list = list()  # [MaterialProperty]
        self.last_used_directory: str = str(Path.home())
        self.last_used_bathymetry_data: BathymetryFormData = BathymetryFormData()
        self.is_simulation_done: bool = False

        self.load_default_materials()
    
    def __setstate__(self, state: dict):
        # Attribute renaming map (old -> new)
        rename_map = dict()
        
        # Handle missing attributes (backward compatibility)
        default_attrs = {
            'is_simulation_done': False,  # Add other renames if needed
        }

        # Restore the state
        self.__dict__.update(migrate_state(rename_map,default_attrs,state))

    def update_last_used_directory(self, new_path: str) -> None:
        """ Updates the last used directory with the folder from the provided path. """
        if not new_path:
            return
        if isdir(new_path):
            self.last_used_directory = new_path
        elif isfile(new_path):
            self.last_used_directory = dirname(new_path)

    def load_default_materials(self) -> None:
        """ Loads and initializes the default materials for a case. """
        self.global_materials = load_default_materials()
