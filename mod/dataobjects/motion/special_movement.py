#!/usr/bin/env python3.7
# -*- coding: utf-8 -*-
""" DesignSPHysics Special Movement data. """

from mod.enums import MotionType

from mod.dataobjects.motion.wave_gen import WaveGen


class SpecialMovement():
    """ DualSPHysics compatible special movement.
        It includes regular/irregular wave generators and file movements

        Attributes:
            name: Name for this motion given by the user
            generator: Generator assigned
        """

    def __init__(self, name="New Movement", generator=None):
        self.name = name
        self.type = MotionType.WAVE
        self.generator = generator

    def set_wavegen(self, generator):
        """ Sets the wave generator for the special movement """
        if isinstance(generator, WaveGen):
            self.generator = generator
        else:
            raise TypeError("You are trying to set a non-generator object.")

    def __str__(self):
        to_ret = "SpecialMovement <{}> with an {}".format(
            self.name, self.generator.__class__.__name__) + "\n"
        return to_ret
