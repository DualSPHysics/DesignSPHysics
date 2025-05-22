#!/usr/bin/env python3.7
# -*- coding: utf-8 -*-
""" DesignSPHysics MoorDynPlus Line. """

from mod.dataobjects.moorings.moordynplus.moordynplus_vessel_connection import MoorDynPlusVesselConnection
from mod.dataobjects.moorings.moordynplus.moordynplus_fix_connection import MoorDynPlusFixConnection
from mod.dataobjects.moorings.moordynplus.moordynplus_connect_connection import MoorDynPlusConnectConnection


class MoorDynPlusLine():
    """ MoorDynPlus line representation. """

    def __init__(self, line_id=-1):
        self.line_id: int = line_id

        # Not more than 2 connections allowed.
        self.vessel_connection: MoorDynPlusVesselConnection = None
        self.vessel2_connection: MoorDynPlusVesselConnection = None
        self.fix_connection: MoorDynPlusFixConnection = None
        self.connect_connection: MoorDynPlusConnectConnection = None
        self.connect2_connection: MoorDynPlusConnectConnection = None
        self.length: float = 1.0
        self.segments: int = 20

        # Default overrides
        self.ea: float = None
        self.diameter: float = None
        self.massDenInAir: float = None
        self.ba: float = None
        self.can: float = None
        self.cat: float = None
        self.cdn: float = None
        self.cdt: float = None
        self.outputFlags: str = None
