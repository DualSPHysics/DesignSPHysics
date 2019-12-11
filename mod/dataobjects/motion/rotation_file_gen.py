#!/usr/bin/env python3.7
# -*- coding: utf-8 -*-
""" DesignSPHysics Rotation-File based motion data """

from mod.enums import MotionType

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

    def __init__(self, duration=0, filename="", anglesunits="degrees", axisp1=None, axisp2=None):
        WaveGen.__init__(self)
        self.duration = duration
        self.type = MotionType.FILE_ROTATIONAL_GENERATOR
        self.anglesunits = anglesunits
        self.filename = filename
        self.axisp1 = axisp1 or [0, 0, 0]
        self.axisp2 = axisp2 or [0, 0, 0]
