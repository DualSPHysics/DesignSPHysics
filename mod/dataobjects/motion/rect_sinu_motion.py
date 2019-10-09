#!/usr/bin/env python3.7
# -*- coding: utf-8 -*-
''' DesignSPHysics Sinusoidal Rectilinar Motion data. '''

from mod.dataobjects.motion.base_motion import BaseMotion


class RectSinuMotion(BaseMotion):
    ''' DualSPHysics sinusoidal rectilinear motion.

        Attributes:
            freq: Frequency (vector)
            ampl: Amplitude (vector)
            phase: Phase (vector)
        '''

    def __init__(self, duration=1, freq=None, ampl=None, phase=None, parent_movement=None):
        if freq is None:
            freq = [0, 0, 0]
        if ampl is None:
            ampl = [0, 0, 0]
        if phase is None:
            phase = [0, 0, 0]
        BaseMotion.__init__(self, duration)
        self.type = "Sinusoidal Rectilinear Motion"
        self.parent_movement = parent_movement
        self.freq = freq
        self.ampl = ampl
        self.phase = phase

    def __str__(self):
        return "RectSinuMotion [Duration: {} ; Frequency: {} ; Amplitude: {} ; Phase: {}".format(
            self.duration,
            self.freq,
            self.ampl,
            self.phase)
