#!/usr/bin/env python3.7
# -*- coding: utf-8 -*-
""" DesignSPHysics AccelrationInput data. """


class AccelerationInput():
    """ Acceleration Input control structure. Includes enabling/disabling and a list
    of AccelerationInputData objects"""

    def __init__(self, enabled=False, acclist=None):
        self.enabled = enabled
        self.acclist = acclist or []

    def set_list(self, acclist):
        """ Sets the acceleration input list. """
        self.acclist = acclist

    def set_enabled(self, state):
        """ Enables/Disables acceleration input. """
        self.enabled = state
