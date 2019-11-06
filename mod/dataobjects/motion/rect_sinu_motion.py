#!/usr/bin/env python3.7
# -*- coding: utf-8 -*-
""" DesignSPHysics Sinusoidal Rectilinar Motion data. """

from mod.enums import MotionType

from mod.dataobjects.motion.base_motion import BaseMotion


class RectSinuMotion(BaseMotion):
    """ DualSPHysics sinusoidal rectilinear motion.

        Attributes:
            freq: Frequency (vector)
            ampl: Amplitude (vector)
            phase: Phase (vector)
        """

    def __init__(self, duration=1, freq=None, ampl=None, phase=None):
        BaseMotion.__init__(self, duration)
        self.type = MotionType.SINUSOIDAL_RECTILINEAR
        self.freq = freq or [0, 0, 0]
        self.ampl = ampl or [0, 0, 0]
        self.phase = phase or [0, 0, 0]

    def __str__(self):
        return "RectSinuMotion [Duration: {} ; Frequency: {} ; Amplitude: {} ; Phase: {}".format(
            self.duration,
            self.freq,
            self.ampl,
            self.phase
        )
