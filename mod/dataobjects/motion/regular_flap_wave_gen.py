#!/usr/bin/env python3.7
# -*- coding: utf-8 -*-
""" DesignSPHysics Regular Flap wave generator data. """

from mod.enums import MotionType

from mod.dataobjects.motion.wave_gen import WaveGen


class RegularFlapWaveGen(WaveGen):
    """ Flap Regular Wave Generator.

    Attributes:
        phase: Initial wave phase in function of PI
        ramp: Periods of ramp
        variable_draft: Position of the wavemaker hinge
        flapaxis0: Point 0 of axis rotation
        flapaxis1: Point 1 of axis rotation
    """

    def __init__(self, wave_order=2, start=0, duration=0, depth=0, wave_height=0.5,
                 wave_period=1, gainstroke=1.0, phase=0, ramp=0, disksave_periods=24, disksave_periodsteps=20, disksave_xpos=2,
                 disksave_zpos=-0.15, variable_draft=0.0, flapaxis0=None, flapaxis1=None):
        WaveGen.__init__(self, wave_order, start, duration, depth, wave_height, wave_period, gainstroke)
        self.type = MotionType.REGULAR_FLAP_WAVE_GENERATOR
        self.phase = phase
        self.ramp = ramp
        self.variable_draft = variable_draft
        self.flapaxis0 = flapaxis0 or [0, -1, 0]
        self.flapaxis1 = flapaxis1 or [0, 1, 0]
        self.disksave_periods = disksave_periods
        self.disksave_periodsteps = disksave_periodsteps
        self.disksave_xpos = disksave_xpos
        self.disksave_zpos = disksave_zpos
