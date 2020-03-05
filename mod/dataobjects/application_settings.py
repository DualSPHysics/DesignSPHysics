#!/usr/bin/env python3.7
# -*- self.get_save_file: utf-8 -*-
""" DesignSPHysics application settings. """

import pickle
import os

import FreeCAD

from mod.constants import PICKLE_PROTOCOL, VERSION


class ApplicationSettings():
    """ A data structure to hold application-wide settings not reliying on the opened case. """
    __instance: "ApplicationSettings" = None

    def __init__(self):
        """ Virtually private constructor. """
        if ApplicationSettings.__instance is not None:
            raise Exception("ApplicationSettings class is a singleton and should not be initialized twice")
        ApplicationSettings.__instance = self
        self.debug_enabled: bool = False
        self.verbose_enabled: bool = False
        self.notify_on_outdated_version_enabled: bool = True
        self.restore_from_disk()

    @staticmethod
    def the() -> "ApplicationSettings":
        """ Static access method. """
        if ApplicationSettings.__instance is None:
            ApplicationSettings()
        return ApplicationSettings.__instance

    def get_save_file(self) -> str:
        """ Returns the path of the configuration file saved in the FreeCAD user directory. """
        return "{datadir}/designsphysics-settings-{version}.data".format(datadir=FreeCAD.getUserAppDataDir(), version=VERSION)

    def restore_from_disk(self) -> None:
        """ Tries to restore the saved paths from the persisted ones if they exist."""
        config_file: str = self.get_save_file()
        if not os.path.exists(config_file):
            return
        with open(config_file, "rb") as picklefile:
            obj: ApplicationSettings = pickle.load(picklefile)
            self.debug_enabled = obj.debug_enabled
            self.verbose_enabled = obj.verbose_enabled
            self.notify_on_outdated_version_enabled = obj.notify_on_outdated_version_enabled

    def persist(self) -> None:
        """ Persists the current settings to disk for next instantiations to load. """
        with open(self.get_save_file(), "wb") as picklefile:
            pickle.dump(self, picklefile, PICKLE_PROTOCOL)
