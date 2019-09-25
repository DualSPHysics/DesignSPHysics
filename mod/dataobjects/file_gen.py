#!/usr/bin/env python3.7
# -*- coding: utf-8 -*-
''' DesignSPHysics File Generator data. '''

from mod.dataobjects.wave_gen import WaveGen


class FileGen(WaveGen):
    ''' File Generator. Loads movements from file

    Attributes:
        duration: Duration in seconds
        filename: File path to use
        fields: Number of columns of the file
        fieldtime: Column with time
        fieldx: Column with X-position
        fieldy: Column with Y-position
        fieldz: Column with Z-position
    '''

    def __init__(self, parent_movement=None, duration=0, filename="", fields=0, fieldtime=0, fieldx=0, fieldy=0,
                 fieldz=0):
        super(FileGen, self).__init__(parent_movement)
        self.duration = duration
        self.name = "File Wave Generator"
        self.filename = filename
        self.fields = fields
        self.fieldtime = fieldtime
        self.fieldx = fieldx
        self.fieldy = fieldy
        self.fieldz = fieldz
