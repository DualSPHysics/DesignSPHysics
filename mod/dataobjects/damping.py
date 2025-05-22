#!/usr/bin/env python3.7
# -*- coding: utf-8 -*-
""" DesignSPHysics Damping data. """
from mod.dataobjects.properties.faces_property import FacesProperty
from mod.enums import DampingType


class Damping:
    """ DualSPHysics damping settings """

    def __init__(self, damping_type:DampingType=DampingType.ZONE,enabled:bool=True,  overlimit:float=1, redumax:float=10,factorxyz:list=[1,1,1],
                 usedomain:bool=False,domain_zmin:float=0,domain_zmax:float=0,points:list=[]):
        self.damping_type:DampingType=damping_type
        self.enabled = enabled
        self.overlimit = overlimit
        self.redumax = redumax
        self.factorxyz = factorxyz
        self.usedomain=usedomain  #DOMAIN VALE PARA TODAS?
        self.domain_zmin=domain_zmin
        self.domain_zmax=domain_zmax
        self.points=points
        self.damping_directions=FacesProperty()

    def __str__(self):
        to_ret = ""
        to_ret += "Damping configuration structure ({})\n".format("enabled" if self.enabled else "disabled")
        to_ret += "Overlimit: {}\n".format(self.overlimit)
        to_ret += "Redumax: {}".format(self.redumax)
        return to_ret
