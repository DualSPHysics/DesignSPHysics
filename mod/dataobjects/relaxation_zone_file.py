#!/usr/bin/env python3.7
# -*- coding: utf-8 -*-
""" DesignSPHysics Relaxation Zone File data. """

from mod.dataobjects.relaxation_zone import RelaxationZone


class RelaxationZoneFile(RelaxationZone):
    """ Relaxation zone with external file wave definition """

    def __init__(self, start=0, duration=0, depth=1, swl=1, filesvel="", filesvelx_initial=0,
                 filesvelx_count=5, usevelz=False, movedata=None, dpz=2, smooth=0, center=None, width=0.5,
                 coefdir=None, coefdt=1000, function_psi=0.9, function_beta=1, driftcorrection=0,
                 driftinitialramp=0):
        self.driftinitialramp = driftinitialramp
        self.smooth = smooth
        self.dpz = dpz
        self.movedata = [0, 0, 0] if movedata is None else movedata
        self.usevelz = usevelz
        self.filesvelx_count = filesvelx_count
        self.filesvelx_initial = filesvelx_initial
        self.filesvel = filesvel
        self.start = start
        self.duration = duration
        self.depth = depth
        self.swl = swl
        self.center = [0, 0, 0] if center is None else center
        self.width = width
        self.coefdir = [1, 0, 0] if coefdir is None else coefdir
        self.coefdt = coefdt
        self.function_psi = function_psi
        self.function_beta = function_beta
        self.driftcorrection = driftcorrection
