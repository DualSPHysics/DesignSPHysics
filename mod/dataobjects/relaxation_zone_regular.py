#!/usr/bin/env python3.7
# -*- coding: utf-8 -*-
""" DesignSPHysics Regular Relaxation Zone data. """

from mod.dataobjects.relaxation_zone import RelaxationZone

class RelaxationZoneRegular(RelaxationZone):
    """ Relaxation zone for regular wave generation """

    def __init__(self, start=0, duration=0, waveorder=1, waveheight=1, waveperiod=2, depth=1, swl=1, center=None,
                 width=0.5, phase=0, ramp=0,
                 savemotion_periods=24, savemotion_periodsteps=20, savemotion_xpos=0, savemotion_zpos=0,
                 coefdir=None, coefdt=1000, function_psi=0.9, function_beta=1, driftcorrection=0):
        self.start = start
        self.duration = duration
        self.waveorder = waveorder
        self.waveheight = waveheight
        self.waveperiod = waveperiod
        self.depth = depth
        self.swl = swl
        self.center = [0, 0, 0] if center is None else center
        self.width = width
        self.phase = phase
        self.ramp = ramp
        self.savemotion_periods = savemotion_periods
        self.savemotion_periodsteps = savemotion_periodsteps
        self.savemotion_xpos = savemotion_xpos
        self.savemotion_zpos = savemotion_zpos
        self.coefdir = [1, 0, 0] if coefdir is None else coefdir
        self.coefdt = coefdt
        self.function_psi = function_psi
        self.function_beta = function_beta
        self.driftcorrection = driftcorrection
