#!/usr/bin/env python3.7
# -*- coding: utf-8 -*-
''' DesignSPHysics Regular Flap wave generator data. '''


from mod.dataobjects.wave_gen import WaveGen


class RegularFlapWaveGen(WaveGen):
    ''' Flap Regular Wave Generator.

    Attributes:
        phase: Initial wave phase in function of PI
        ramp: Periods of ramp
        variable_draft: Position of the wavemaker hinge
        flapaxis0: Point 0 of axis rotation
        flapaxis1: Point 1 of axis rotation
    '''

    def __init__(self, parent_movement=None, wave_order=2, start=0, duration=0, depth=0, wave_height=0.5,
                 wave_period=1, phase=0, ramp=0, disksave_periods=24,
                 disksave_periodsteps=20, disksave_xpos=2, disksave_zpos=-0.15, variable_draft=0.0, flapaxis0=None,
                 flapaxis1=None):
        super(RegularFlapWaveGen, self).__init__(parent_movement, wave_order,
                                                 start, duration, depth, wave_height, wave_period)
        self.type = "Regular Flap Wave Generator"
        self.phase = phase
        self.ramp = ramp
        self.variable_draft = variable_draft
        self.flapaxis0 = [0, -1, 0] if flapaxis0 is None else flapaxis0
        self.flapaxis1 = [0, 1, 0] if flapaxis1 is None else flapaxis1
        self.disksave_periods = disksave_periods
        self.disksave_periodsteps = disksave_periodsteps
        self.disksave_xpos = disksave_xpos
        self.disksave_zpos = disksave_zpos
