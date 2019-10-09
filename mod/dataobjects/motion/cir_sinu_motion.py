#!/usr/bin/env python3.7
# -*- coding: utf-8 -*-
""" DesignSPHysics Circular Sinusoidal motion data. """

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

    def __init__(self, reference=None, duration=1, axis1=None, axis2=None, freq=None, ampl=None, phase=None,
                 parent_movement=None):
        if reference is None:
            reference = [0, 0, 0]
        if axis1 is None:
            axis1 = [0, 0, 0]
        if axis2 is None:
            axis2 = [0, 0, 0]
        if freq is None:
            freq = 0
        if ampl is None:
            ampl = 0
        if phase is None:
            phase = 0
        BaseMotion.__init__(self, duration)
        self.type = "Sinusoidal Circular Motion"
        self.parent_movement = parent_movement
        self.reference = reference
        self.axis1 = axis1
        self.axis2 = axis2
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
            self.axis2)
