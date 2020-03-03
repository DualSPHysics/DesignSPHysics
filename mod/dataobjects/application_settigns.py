#!/usr/bin/env python3.7
# -*- coding: utf-8 -*-
""" DesignSPHysics application settings. """


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

    @staticmethod
    def the() -> "ApplicationSettings":
        """ Static access method. """
        if ApplicationSettings.__instance is None:
            ApplicationSettings()
        return ApplicationSettings.__instance
