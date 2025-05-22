#!/usr/bin/env python3.7
# -*- self.get_save_file: utf-8 -*-
""" DesignSPHysics application settings. """

import os
import json

import FreeCAD

from mod.constants import VERSION
from mod.functions import get_os


class ApplicationSettings():
    """ A data structure to hold application-wide settings not reliying on the opened case. """
    __instance: "ApplicationSettings" = None

    _os_available={0:"Windows",1:"Linux"}

    def __init__(self):
        """ Virtually private constructor. """
        if ApplicationSettings.__instance is not None:
            raise Exception("ApplicationSettings class is a singleton and should not be initialized twice")
        ApplicationSettings.__instance = self
        self.json_version: int = 1
        self.app_version: str = VERSION
        self.debug_enabled: bool = False
        self.verbose_enabled: bool = False
        self.notify_on_outdated_version_enabled: bool = True
        self.force_moordynplus_support_enabled: bool = False
        self.basic_visualization:bool = True
        #Variables for custom script generation
        self.execs_path = ""
        self.custom_script_text = ""
        self.restore_from_disk()
        #self.gencase_num_threads=0
        self.os_available_list=list(self._os_available.values())
        os_to_index = {v: k for k, v in self._os_available.items()}
        self.os_index = os_to_index.get(get_os())

    @staticmethod
    def the() -> "ApplicationSettings":
        """ Static access method. """
        if ApplicationSettings.__instance is None:
            ApplicationSettings()
        return ApplicationSettings.__instance

    def get_save_file(self) -> str:
        """ Returns the path of the configuration file saved in the FreeCAD user directory. """
        return "{datadir}/designsphysics-settings.json".format(datadir=FreeCAD.getUserAppDataDir())

    def restore_from_disk(self) -> None:
        """ Tries to restore the saved paths from the persisted ones if they exist."""
        config_file: str = self.get_save_file()
        if not os.path.exists(config_file):
            return
        with open(config_file, "r", encoding="utf-8") as save_file:
            disk_data: dict = json.load(save_file)
            if "debug_enabled" in disk_data.keys():
                self.debug_enabled = disk_data["debug_enabled"]
            if "verbose_enabled" in disk_data.keys():
                self.verbose_enabled = disk_data["verbose_enabled"]
            if "notify_on_outdated_version_enabled" in disk_data.keys():
                self.notify_on_outdated_version_enabled = disk_data["notify_on_outdated_version_enabled"]
            if "force_moordynplus_support_enabled" in disk_data.keys():
                self.force_moordynplus_support_enabled = disk_data["force_moordynplus_support_enabled"]
            if "linux_os" in disk_data.keys():
                self.linux_os = disk_data["linux_os"]
            if "execs_path" in disk_data.keys():
                self.execs_path = disk_data["execs_path"]
            if "custom_script_text" in disk_data.keys():
                self.custom_script_text = disk_data["custom_script_text"]
            if "basic_visualization" in disk_data.keys():
                self.basic_visualization = disk_data["basic_visualization"]

    def persist(self) -> None:
        """ Persists the current settings to disk for next instantiations to load. """
        with open(self.get_save_file(), "w", encoding="utf-8") as save_file:
            json.dump(self.__dict__, save_file, indent=4)
