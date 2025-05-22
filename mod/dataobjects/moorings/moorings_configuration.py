#!/usr/bin/env python3.7
# -*- coding: utf-8 -*-
""" DesignSPHysics MoorDynPlus coupling configuration. """

from mod.enums import MooringsConfigurationMethod

from mod.dataobjects.moorings.moorings_save_options import MooringsSaveOptions
from mod.dataobjects.moorings.moordynplus.moordynplus_configuration import MoorDynPlusConfiguration
from mod.functions import migrate_state

class MooringsConfiguration():
    """ A moorings configuration structure to use with MoorDynPlus under DualSPHysics. """

    def __init__(self):
        self.enabled = False
        self.saveoptions: MooringsSaveOptions = MooringsSaveOptions()
        self.moored_floatings: list = list()  # MKBound (int)
        self.configuration_method: MooringsConfigurationMethod = MooringsConfigurationMethod.EMBEDDED
        self.moordynplus_xml: str = ""
        self.moordynplus_configuration: MoorDynPlusConfiguration = MoorDynPlusConfiguration()
    
    def __setstate__(self, state: dict):
        # Attribute renaming map (old -> new)
        rename_map = {
            'moordyn_xml': 'moordynplus_xml',  # Add other renames if needed
            'moordyn_configuration': 'moordynplus_configuration',
        }

        # Handle missing attributes (backward compatibility)
        default_attrs = dict()

        # Restore the state
        self.__dict__.update(migrate_state(rename_map,default_attrs,state))
