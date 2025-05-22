#!/usr/bin/env python3.7
# -*- coding: utf-8 -*-
""" DesignSPHysics Relaxation zone data. """


class RelaxationZone():
    """ Base class for Relaxation Zone objects """

    def __init__(self, start=0, duration=0, depth=1,coefdt=1000, function_psi=0.9, function_beta=1,swl=1,center=None, width=0.5) :
        self.start = start
        self.duration = duration
        self.depth = depth
        self.coefdt = coefdt
        self.function_psi = function_psi
        self.function_beta = function_beta
        self.swl = swl
        self.center = [0, 0, 0] if center is None else center
        self.width = width