#!/usr/bin/env python3.7
# -*- coding: utf-8 -*-
""" DesignSPHysics Damping data. """

class Damping():
    """ DualSPHysics damping settings """

    def __init__(self, enabled=True, overlimit=1, redumax=10):
        self.enabled = enabled
        self.overlimit = overlimit
        self.redumax = redumax

    def __str__(self):
        to_ret = ""
        to_ret += "Damping configuration structure ({})\n".format("enabled" if self.enabled else "disabled")
        to_ret += "Overlimit: {}\n".format(self.overlimit)
        to_ret += "Redumax: {}".format(self.redumax)
        return to_ret
