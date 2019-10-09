#!/usr/bin/env python3.7
# -*- coding: utf-8 -*-
""" DesignSPHysics VelData attribute data. """


class MLPiston2DVeldata():
    """ VelData attribute for MLPiston2D """

    def __init__(self, filevelx="", posy=0, timedataini=0):
        self.filevelx = filevelx
        self.posy = posy
        self.timedataini = timedataini
