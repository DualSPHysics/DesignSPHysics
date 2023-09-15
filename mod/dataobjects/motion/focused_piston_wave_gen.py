#!/usr/bin/env python3.7
# -*- coding: utf-8 -*-
""" DesignSPHysics Focused Piston Wave gen data """

from random import randint

from mod.enums import IrregularDiscretization, IrregularSpectrum, MotionType
from mod.dataobjects.motion.wave_gen import WaveGen

class FocusedPistonWaveGen(WaveGen):
    """ Piston Focused Wave Generator.

    Attributes:
        spectrum: Spectrum type selected for the generation
        discretization: Type of discretization for the spectrum
        peak_coef: Peak enhancement coefficient
        waves: Number of waves to create irregular waves
        randomseed: Random seed to initialize RNG
        ramptime: Time of ramp
        savemotion_*: Saves motion data
        piston_dir: Movement direction (def [1,0,0])
        xf: Focused location
        fphase: Focused phase [deg]
        maxwaveh_nwaves: Number of waves to compute maximum wave H
        maxwaveh_time: Time to compute maximum wave H
        fpretime: Initial extra time for focus generation
        fmovtime: Final time for paddle motion
        fmovramp: Final ramp time before final time motion 
    """

    def __init__(self, wave_order=1, start=0, duration=0, depth=0, wave_height=0.5,
                 wave_period=1, gainstroke=1.0, spectrum=IrregularSpectrum.JONSWAP,
                 discretization=IrregularDiscretization.STRETCHED,
                 peak_coef=0.1, waves=128, randomseed=randint(0, 9999), ramptime=0, savemotion_time=30, 
                 savemotion_timedt=0.05, savemotion_xpos=2, savemotion_zpos=-0.15, piston_dir=None, 
                 xf=12.5, fphase=0, maxwaveh_nwaves=1000, maxwaveh_time=0, fpretime=5, 
                 fmovtime=0, fmovramp=0):
        WaveGen.__init__(self, wave_order, start, duration, depth, wave_height, wave_period, gainstroke)
        self.type = MotionType.FOCUSED_PISTON_WAVE_GENERATOR
        self.spectrum = spectrum
        self.discretization = discretization
        self.peak_coef = peak_coef
        self.waves = waves
        self.randomseed = randomseed
        self.ramptime = ramptime
        self.savemotion_time = savemotion_time
        self.savemotion_timedt = savemotion_timedt
        self.savemotion_xpos = savemotion_xpos
        self.savemotion_zpos = savemotion_zpos
        self.piston_dir = piston_dir or [1, 0, 0]
        self.xf = xf
        self.fphase = fphase
        self.maxwaveh_nwaves = maxwaveh_nwaves
        self.maxwaveh_time = maxwaveh_time
        self.fpretime = fpretime
        self.fmovtime = fmovtime
        self.fmovramp = fmovramp