#!/usr/bin/env python3.7
# -*- coding: utf-8 -*-
""" DesignSPHysics Inlet/Outlet elevation info. """
from typing import List

from mod.enums import InletOutletElevationType, InletOutletZSurfMode


class InletOutletElevationInfo():
    """ Stores Inlet/Outlet elevation information and parameters. """

    def __init__(self):
        self.elevation_enabled:bool = False
        self.elevation_type: InletOutletElevationType = InletOutletElevationType.FIXED
        self.savevtk: bool = False
        self.remove: bool = False
        self.zsurf_mode: InletOutletZSurfMode = InletOutletZSurfMode.FIXED
        self.zsurf: float = 0.0
        self.zsurftimes: list = []  # [(float(time), float(value))]
        self.zsurffile: str = ""
        self.meshdata: ZSurfMeshData = ZSurfMeshData()
        self.zsurfmin: float = 0.0
        self.zsurffit: float = 0.0

    def save_fixed(self, values):
        self.zsurf = values["zsurf"]

    def save_variable_timelist(self, values):
        self.savevtk = values["savevtk"]
        self.remove = values["remove"]
        self.zsurftimes = values["zsurftimes"]

    def save_variable_csv_file(self, values):
        self.savevtk = values["savevtk"]
        self.remove = values["remove"]
        self.zsurffile = values["zsurffile"]

    def save_variable_meshdata(self, values):
        self.savevtk = values["savevtk"]
        self.remove = values["remove"]
        self.meshdata.save(values["meshdata"])

    def save_automatic(self, values):
        self.savevtk = values["savevtk"]
        self.remove = values["remove"]
        self.zsurfmin = values["zsurfmin"]
        self.zsurffit = values["zsurffit"]

class ZSurfMeshData:

    def __init__(self, file: str = "", initial_time: float = 0.0,
                 timeloop_tbegin: float = 0.0, timeloop_tend: float = 0.0, setpos: List = [0.0, 0.0, 0.0],
                 ) -> None:
        self.file = file
        self.initial_time = initial_time
        self.timeloop_tbegin = timeloop_tbegin
        self.timeloop_tend = timeloop_tend
        self.setpos = setpos

    def save(self, values):
        self.file = values["file"]
        self.initial_time = values["initial_time"]
        self.timeloop_tbegin = values["timeloop_tbegin"]
        self.timeloop_tend = values["timeloop_tend"]
        self.setpos = values["setpos"]
