#!/usr/bin/env python3.7
# -*- coding: utf-8 -*-
""" DesignSPHysics Rotation-File based motion data """

from mod.dataobjects.motion.wave_gen import WaveGen


class RotationFileGen(WaveGen):
    """ Rotation File Generator. Loads rotation movements from file

    Attributes:
        duration: Duration in seconds
        anglesunits: Units of the file (degrees, radians)
        filename: File path to use
        axisp1: Point 1 of the axis
        axisp2: Point 2 of the axis
    """

    def __init__(self, parent_movement=None, duration=0, filename="", anglesunits="degrees", axisp1=None, axisp2=None):
        super(RotationFileGen, self).__init__(parent_movement)
        if axisp1 is None:
            axisp1 = [0, 0, 0]
        if axisp2 is None:
            axisp2 = [0, 0, 0]
        self.duration = duration
        self.name = "File Wave Generator"
        self.anglesunits = anglesunits
        self.filename = filename
        self.axisp1 = axisp1
        self.axisp2 = axisp2
