#!/usr/bin/env python3.7
# -*- coding: utf-8 -*-
""" DesignSPHysics Regular Piston Wave Generator data """

from mod.enums import MotionType

from mod.dataobjects.motion.wave_gen import WaveGen
from mod.dataobjects.awas import AWAS


class RegularPistonWaveGen(WaveGen):
    """ Piston Regular Wave Generator.

    Attributes:
        phase: Initial wave phase in function of PI
        ramp: Periods of ramp
        disksave_periods:
        disksave_periodsteps:
        disksave_xpos:
        disksave_zpos:
        piston_dir: Movement direction (def [1,0,0])
        awas: AWAS object
    """

    def __init__(self, wave_order=2, start=0, duration=0, depth=0, wave_height=0.5, wave_period=1, gainstroke=1.0, phase=0, ramp=0,
                 disksave_periods=24, disksave_periodsteps=20, disksave_xpos=2, disksave_zpos=-0.15, piston_dir=None, awas=None):
        WaveGen.__init__(self, wave_order, start, duration, depth, wave_height, wave_period, gainstroke)
        self.type = MotionType.REGULAR_PISTON_WAVE_GENERATOR
        self.phase = phase
        self.ramp = ramp
        self.disksave_periods = disksave_periods
        self.disksave_periodsteps = disksave_periodsteps
        self.disksave_xpos = disksave_xpos
        self.disksave_zpos = disksave_zpos
        self.piston_dir = piston_dir or [1, 0, 0]
        self.awas = AWAS() if awas is None else awas
