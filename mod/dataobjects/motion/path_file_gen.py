#!/usr/bin/env python3.7
# -*- coding: utf-8 -*-
""" DesignSPHysics File Generator data. """

from mod.enums import MotionType

from mod.dataobjects.motion.wave_gen import WaveGen


class PathFileGen(WaveGen):
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

    def __init__(self, duration=0, filename="", fields=7, fieldtime=0, fieldx=1, fieldy=2, fieldz=3,fieldang1=4, fieldang2=5, fieldang3=6,
                 center=None, intrinsic = False,movecenter=True,axes = "XYZ",anglesunits="degrees"):
        WaveGen.__init__(self)
        self.anglesunits = anglesunits
        if center is None:
            center = [0.0, 0.0, 0.0]
        self.duration = duration
        self.type = MotionType.FILE_PATH_GENERATOR
        self.filename = filename
        self.fields = fields
        self.fieldtime = fieldtime
        self.fieldx = fieldx
        self.fieldy = fieldy
        self.fieldz = fieldz
        self.fieldang1 = fieldang1
        self.fieldang2 = fieldang2
        self.fieldang3 = fieldang3
        self.center = center
        self.intrinsic = intrinsic
        self.axes = axes
        self.movecenter=movecenter


