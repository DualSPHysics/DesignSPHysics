#!/usr/bin/env python3.7
# -*- coding: utf-8 -*-
""" DesignSPHysics AWAS Configuration data """

from mod.enums import AWASWaveOrder, AWASSaveMethod
from mod.dataobjects.awas_correction import AWASCorrection


class AWAS():
    """ AWAS configuration.

    Attributes:
        startawas: Time to start AWAS correction
        swl: "Still water level (free-surface water)
        elevation: Order wave to calculate elevation 1:1st order, 2:2nd order
        gaugex: Position in X from piston to measure free-surface water
        gaugey: Position in Y to measure free-surface water
        gaugezmin: Minimum position in Z to measure free-surface water, it must be in water
        gaugezmax: Maximum position in Z to measure free-surface water (def=domain limits)
        gaugedp: Resolution to measure free-surface water, it uses Dp*gaugedp
        coefmasslimit: Coefficient to calculate mass of free-surface
        savedata: Saves CSV with information
        limitace: Factor to limit maximum value of acceleration, with 0 disabled
        correction: Drift correction configuration
    """

    def __init__(self, enabled=False, startawas=0, swl=0, elevation=AWASWaveOrder.SECOND_ORDER,
                 gaugex=0, gaugey=0, gaugezmin=0, gaugezmax=0, gaugedp=0, coefmasslimit=0,
                 savedata=AWASSaveMethod.BY_PART, limitace=0, correction=None):
        self.enabled = enabled
        self.startawas = startawas
        self.swl = swl
        self.elevation = elevation
        self.gaugex = gaugex
        self.gaugey = gaugey
        self.gaugezmin = gaugezmin
        self.gaugezmax = gaugezmax
        self.gaugedp = gaugedp
        self.coefmasslimit = coefmasslimit
        self.savedata = savedata
        self.limitace = limitace
        self.correction = correction if correction is not None else AWASCorrection()
