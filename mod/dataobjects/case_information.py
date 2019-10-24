#!/usr/bin/env python3.7
# -*- coding: utf-8 -*-
""" DesignSPHysics Case Information Data """

from PySide import QtCore, QtGui


class CaseInformation():
    """ Stores miscellaneous information related with the case. """

    def __init__(self):
        self.is_gencase_done: bool = False
        self.is_simulation_done: bool = False
        self.previous_particle_number: int = 0
        self.particle_number: int = 0
        self.particles_out: int = 0
        self.exported_parts: int = 0
        self.run_additional_parameters: str = ""
        self.needs_to_run_gencase: bool = True
        self.current_info_dialog: QtGui.QDialog = None
        self.current_output: str = ""
        self.measuretool_points: list = []
        self.measuretool_grid: list = []
        self.objectlist_table: QtGui.QTableWidget = None
        self.last_3d_width: float = -1.0
        self.global_movements: list = list() # [Movement]
