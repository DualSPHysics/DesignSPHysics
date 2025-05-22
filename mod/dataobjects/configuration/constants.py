#!/usr/bin/env python3.7
# -*- coding: utf-8 -*-
""" DesignSPHysics case constants dataobject """

class Constants():
    """ DualSPHysics case constants definition dataobject. """

    def __init__(self):
        self.lattice_bound: int = 1
        self.lattice_fluid: int = 1
        self.pointref: list = [0, 0, 0]
        self.setpointref_hdp : bool = False
        self.gravity: list = [0, 0, -9.81]
        self.rhop0: float = 1000
        self.rhopgradient: int = 2
        self.hswl: float = 0
        self.hswl_auto: bool = True
        self.gamma: float = 7
        self.speedsystem: float = 0
        self.speedsystem_auto: bool = True
        self.coefsound: float = 20
        self.speedsound: float = 0
        self.speedsound_auto: bool = True
        self.coefh: float = 1.2
        self.hdp: float = 1.5
        self.use_hdp : bool = False
        self.h_constant_name : str = "coefh"
        self.h_constant : float = self.coefh
        self.cflnumber: float = 0.2
        self.h: float = 0
        self.h_auto: bool = True
        self.b: float = 0
        self.b_auto: bool = True
        self.massbound: float = 0
        self.massbound_auto: bool = True
        self.massfluid: float = 0
        self.massfluid_auto: bool = True
