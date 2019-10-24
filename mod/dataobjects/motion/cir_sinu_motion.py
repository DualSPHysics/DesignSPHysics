#!/usr/bin/env python3.7
# -*- coding: utf-8 -*-
""" DesignSPHysics Circular Sinusoidal motion data. """

from mod.enums import MotionType

from mod.dataobjects.motion.base_motion import BaseMotion


class CirSinuMotion(BaseMotion):
    """ DualSPHysics sinusoidal circular motion.

        Attributes:
            reference: Point of the object that rotates with the axis
            axis1: Starting point of the vector that defines the rotation axis
            axis2: Finishing point of the vector that defines the rotation axis
            freq: Frequency
            ampl: Amplitude
            phase: Phase
        """

    def __init__(self, reference=None, duration=1, axis1=None, axis2=None, freq=0, ampl=0, phase=0):
        BaseMotion.__init__(self, duration)
        self.type = MotionType.SINUSOIDAL_CIRCULAR
        self.reference = reference or [0, 0, 0]
        self.axis1 = axis1 or [0, 0, 0]
        self.axis2 = axis2 or [0, 0, 0]
        self.freq = freq
        self.ampl = ampl
        self.phase = phase

    def __str__(self):
        return "CirSinuMotion [Duration: {} ; Frequency: {} ; Amplitude: {} ; " "Phase: {} ; Reference: {} ; Axis: [{}, {}]]".format(
            self.duration,
            self.freq,
            self.ampl,
            self.phase,
            self.reference,
            self.axis1,
            self.axis2
        )
