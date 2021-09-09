#!/usr/bin/env python3.7
# -*- coding: utf-8 -*-
""" DesignSPHysics Irregular Piston Wave gen data """

from random import randint

from mod.enums import IrregularDiscretization, IrregularSpectrum, MotionType
from mod.dataobjects.motion.wave_gen import WaveGen
from mod.dataobjects.awas import AWAS


class IrregularPistonWaveGen(WaveGen):
    """ Piston Regular Wave Generator.

    Attributes:
        spectrum: Spectrum type selected for the generation
        discretization: Type of discretization for the spectrum
        peak_coef: Peak enhancement coefficient
        waves: Number of waves to create irregular waves
        randomseed: Random seed to initialize RNG
        serieini: Initial time in irregular wave serie
        ramptime: Time of ramp
        piston_dir: Movement direction (def [1,0,0])
    """

    def __init__(self, wave_order=1, start=0, duration=0, depth=0, wave_height=0.5,
                 wave_period=1, gainstroke=1.0, spectrum=IrregularSpectrum.JONSWAP,
                 discretization=IrregularDiscretization.STRETCHED,
                 peak_coef=0.1, waves=50, randomseed=randint(0, 9999), serieini=0, ramptime=0,
                 serieini_autofit=True, savemotion_time=30, savemotion_timedt=0.05, savemotion_xpos=2,
                 savemotion_zpos=-0.15, saveserie_timemin=0, saveserie_timemax=1300, saveserie_timedt=0.05,
                 saveserie_xpos=0, saveseriewaves_timemin=0, saveseriewaves_timemax=1000, saveseriewaves_xpos=2,
                 piston_dir=None, awas=None):
        WaveGen.__init__(self, wave_order, start, duration, depth, wave_height, wave_period, gainstroke)
        self.type = MotionType.IRREGULAR_PISTON_WAVE_GENERATOR
        self.spectrum = spectrum
        self.discretization = discretization
        self.peak_coef = peak_coef
        self.waves = waves
        self.randomseed = randomseed
        self.serieini = serieini
        self.serieini_autofit = serieini_autofit
        self.ramptime = ramptime
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
        self.piston_dir = piston_dir or [1, 0, 0]
        self.awas = AWAS() if awas is None else awas
