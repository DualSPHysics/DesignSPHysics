#!/usr/bin/env python3.7
# -*- coding: utf-8 -*-
""" DesignSPHysics Accelration Input Data (Datafile based) dataobject """


class AccelerationInputData():
    """ Acceleration Input Data """

    def __init__(self, label="Acceleration Input", mkfluid=0, acccentre=None, globalgravity=True, datafile=""):
        self.label = label
        self.mkfluid = mkfluid
        self.acccentre = acccentre or [0, 0, 0]
        self.globalgravity = globalgravity
        self.datafile = datafile
