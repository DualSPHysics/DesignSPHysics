#!/usr/bin/env python3.7
# -*- self.get_save_file: utf-8 -*-
""" DesignSPHysics application settings. """

import os
import json

import FreeCAD

from mod.constants import VERSION


class ApplicationSettings():
    """ A data structure to hold application-wide settings not reliying on the opened case. """
    __instance: "ApplicationSettings" = None

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
        self.force_moordyn_support_enabled: bool = False
        self.restore_from_disk()

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
            if "force_moordyn_support_enabled" in disk_data.keys():
                self.force_moordyn_support_enabled = disk_data["force_moordyn_support_enabled"]

    def persist(self) -> None:
        """ Persists the current settings to disk for next instantiations to load. """
        with open(self.get_save_file(), "w", encoding="utf-8") as save_file:
            json.dump(self.__dict__, save_file, indent=4)
