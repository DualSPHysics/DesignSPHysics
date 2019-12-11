#!/usr/bin/env python3.7
# -*- coding: utf-8 -*-
""" DesignSPHysics Relaxation Zone Irregular data """

from random import randint

from mod.enums import IrregularSpectrum, IrregularDiscretization
from mod.dataobjects.relaxation_zone import RelaxationZone


class RelaxationZoneIrregular(RelaxationZone):
    """ Relaxation zone for irregular wave generation """

    def __init__(self, start=0, duration=0, peakcoef=3.3, spectrum=IrregularSpectrum.JONSWAP,
                 discretization=IrregularDiscretization.REGULAR, waveorder=1, waveheight=1,
                 waveperiod=2, waves=50, randomseed=randint(0, 9999), depth=1, swl=1, center=None,
                 width=0.5, ramptime=0, serieini=0,
                 savemotion_time=50, savemotion_timedt=0.1, savemotion_xpos=0, savemotion_zpos=0,
                 saveserie_timemin=0, saveserie_timemax=100, saveserie_timedt=0.1, saveserie_xpos=0,
                 saveseriewaves_timemin=0, saveseriewaves_timemax=1000, saveseriewaves_xpos=0,
                 coefdir=None, coefdt=1000, function_psi=0.9, function_beta=1, driftcorrection=0):
        self.start = start
        self.duration = duration
        self.peakcoef = peakcoef
        self.spectrum = spectrum
        self.discretization = discretization
        self.waveorder = waveorder
        self.waveheight = waveheight
        self.waveperiod = waveperiod
        self.waves = waves
        self.randomseed = randomseed
        self.depth = depth
        self.swl = swl
        self.center = [0, 0, 0] if center is None else center
        self.width = width
        self.ramptime = ramptime
        self.serieini = serieini
        self.savemotion_time = savemotion_time
        self.savemotion_timedt = savemotion_timedt
        self.savemotion_xpos = savemotion_xpos
        self.savemotion_zpos = savemotion_zpos
        self.saveserie_timemin = saveserie_timemin
        self.saveserie_timemax = saveserie_timemax
        self.saveserie_timedt = saveserie_timedt
        self.saveserie_xpos = saveserie_xpos
        self.saveseriewaves_timemin = saveseriewaves_timemin
        self.saveseriewaves_timemax = saveseriewaves_timemax
        self.saveseriewaves_xpos = saveseriewaves_xpos
        self.coefdir = [1, 0, 0] if coefdir is None else coefdir
        self.coefdt = coefdt
        self.function_psi = function_psi
        self.function_beta = function_beta
        self.driftcorrection = driftcorrection
