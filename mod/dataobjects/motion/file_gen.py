#!/usr/bin/env python3.7
# -*- coding: utf-8 -*-
""" DesignSPHysics File Generator data. """

from mod.enums import MotionType

from mod.dataobjects.motion.wave_gen import WaveGen


class FileGen(WaveGen):
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

    def __init__(self, duration=0, filename="", fields=0, fieldtime=0, fieldx=0, fieldy=0, fieldz=0):
        WaveGen.__init__(self)
        self.duration = duration
        self.type = MotionType.FILE_GENERATOR
        self.filename = filename
        self.fields = fields
        self.fieldtime = fieldtime
        self.fieldx = fieldx
        self.fieldy = fieldy
        self.fieldz = fieldz
