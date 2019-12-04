#!/usr/bin/env python3.7
# -*- coding: utf-8 -*-
""" DesignSPHysics MoorDyn Line. """

from mod.dataobjects.moorings.moordyn.moordyn_vessel_connection import MoorDynVesselConnection
from mod.dataobjects.moorings.moordyn.moordyn_fix_connection import MoorDynFixConnection
from mod.dataobjects.moorings.moordyn.moordyn_connect_connection import MoorDynConnectConnection


class MoorDynLine():
    """ MoorDyn line representation. """

    def __init__(self, line_id=-1):
        super().__init__()
        self.line_id: int = line_id

        # Not more than 2 connections allowed.
        self.vessel_connection: MoorDynVesselConnection = MoorDynVesselConnection()
        self.fix_connection: MoorDynFixConnection = MoorDynVesselConnection()
        self.connect_connection: MoorDynConnectConnection = MoorDynVesselConnection()
        self.length: float = 1.0
        self.segments: int = 20

        # Default overrides
        self.ea: str = None
        self.diameter: str = None
        self.massDenInAir: float = None
        self.ba: float = None
        self.can: float = None
        self.cat: float = None
        self.cdn: float = None
        self.cdt: float = None
        self.outputFlags: str = None
