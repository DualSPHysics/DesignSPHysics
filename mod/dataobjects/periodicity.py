#!/usr/bin/env python3.7
# -*- coding: utf-8 -*-
""" DesignSPHysics Periodicity data. """


from mod.dataobjects.periodicity_info import PeriodicityInfo


class Periodicity():
    """ Periodicity information for the current case """

    def __init__(self):
        self.x_periodicity: PeriodicityInfo = PeriodicityInfo()
        self.y_periodicity: PeriodicityInfo = PeriodicityInfo()
        self.z_periodicity: PeriodicityInfo = PeriodicityInfo()
