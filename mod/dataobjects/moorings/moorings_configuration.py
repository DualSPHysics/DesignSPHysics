#!/usr/bin/env python3.7
# -*- coding: utf-8 -*-
""" DesignSPHysics MoorDyn coupling configuration. """

from mod.enums import MooringsConfigurationMethod

from mod.dataobjects.moorings.moorings_save_options import MooringsSaveOptions
from mod.dataobjects.moorings.moordyn.moordyn_configuration import MoorDynConfiguration


class MooringsConfiguration():
    """ A moorings configuration structure to use with MoorDyn under DualSPHysics. """

    def __init__(self):
        self.enabled = False
        self.saveoptions: MooringsSaveOptions = MooringsSaveOptions()
        self.moored_floatings: list = list()  # MKBound (int)
        self.configuration_method: MooringsConfigurationMethod = MooringsConfigurationMethod.EMBEDDED
        self.moordyn_xml: str = ""
        self.moordyn_configuration: MoorDynConfiguration = MoorDynConfiguration()
