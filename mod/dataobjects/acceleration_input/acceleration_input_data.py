#!/usr/bin/env python3.7
# -*- coding: utf-8 -*-
""" DesignSPHysics Accelration Input Data (Datafile based) dataobject """
from typing import List


class AccelerationInputData():
    """ Acceleration Input Data """

    def __init__(self, label="Acceleration Input", time_start:float=0.0,time_end:float=0.0,is_fluid:bool=True, mkfluid:int=0,mkbound:int=0, acccentre:list=[0, 0, 0], globalgravity:bool=True, datafile:str=""):
        self.label = label
        self.time_start=time_start
        self.time_end=time_end
        self.is_fluid=is_fluid
        self.mkfluid = mkfluid
        self.mkbound = mkbound
        self.acccentre = acccentre
        self.globalgravity = globalgravity
        self.datafile = datafile

    def to_dict(self):
        return vars(self)
