#!/usr/bin/env python3.7
# -*- coding: utf-8 -*-
""" DesignSPHysics AWAS Correction data """

class AWASCorrection():
    """ AWAS drift correction property """

    def __init__(self, enabled=False, coefstroke=1.8, coefperiod=1, powerfunc=3):
        self.enabled = enabled
        self.coefstroke = coefstroke
        self.coefperiod = coefperiod
        self.powerfunc = powerfunc
