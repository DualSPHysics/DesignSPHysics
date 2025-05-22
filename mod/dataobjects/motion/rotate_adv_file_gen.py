#!/usr/bin/env python3.7
# -*- coding: utf-8 -*-
""" DesignSPHysics File Generator data. """

from mod.enums import MotionType

from mod.dataobjects.motion.wave_gen import WaveGen


class RotateAdvFileGen(WaveGen):
    """ File Generator. Loads movements from file

    Attributes:
        duration: Duration in seconds
        filename: File path to use
        fields: Number of columns of the file
        fieldtime: Column with time
        fieldx: Column with X-position
        fieldy: Column with Y-position
        fieldz: Column with Z-position
    """

    def __init__(self, duration=0, filename="", fields=4, fieldtime=0, fieldang1=1, fieldang2=2, fieldang3=3,
                 center=None, intrinsic = False,axes = "XYZ",anglesunits="degrees"):
        WaveGen.__init__(self)
        self.anglesunits = anglesunits
        if center is None:
            center = [0.0, 0.0, 0.0]
        self.duration = duration
        self.type = MotionType.FILE_ROTATE_ADV_GENERATOR
        self.filename = filename
        self.fields = fields
        self.fieldtime = fieldtime
        self.fieldang1 = fieldang1
        self.fieldang2 = fieldang2
        self.fieldang3 = fieldang3
        self.center = center
        self.intrinsic = intrinsic
        self.axes=axes

