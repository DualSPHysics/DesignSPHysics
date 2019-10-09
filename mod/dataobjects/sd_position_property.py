#!/usr/bin/env python3.7
# -*- coding: utf-8 -*-
""" DesignSPHysics Simulation Domain position property dat """

from mod.enums import SDPositionPropertyType


class SDPositionProperty():
    """ Position property for Simulation Domain """

    def __init__(self, sdptype=SDPositionPropertyType.DEFAULT, value=0.0):
        self.type: SDPositionPropertyType = sdptype
        self.value: float = value
