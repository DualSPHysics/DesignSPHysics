#!/usr/bin/env python3.7
# -*- coding: utf-8 -*-

""" Standard output and error related tools. """

from inspect import getframeinfo, stack
from os import path

import FreeCAD

from mod.constants import APP_NAME, DISK_DUMP_FILE_NAME

from mod.dataobjects.application_settings import ApplicationSettings


def log(message):
    """ Prints a log in the default output."""
    if ApplicationSettings.the().verbose_enabled:
        caller = getframeinfo(stack()[1][0])
        FreeCAD.Console.PrintMessage("[{}] {}:{} -> {}\n".format(APP_NAME, path.basename(caller.filename), caller.lineno, message))


def warning(message):
    """ Prints a warning in the default output. """
    if ApplicationSettings.the().verbose_enabled:
        caller = getframeinfo(stack()[1][0])
        FreeCAD.Console.PrintWarning("[WARNING][{}] {}:{} -> {}\n".format(APP_NAME, path.basename(caller.filename), caller.lineno, message))


def error(message):
    """ Prints an error in the default output."""
    if ApplicationSettings.the().verbose_enabled:
        caller = getframeinfo(stack()[1][0])
        FreeCAD.Console.PrintError("[ERROR][{}] {}:{} -> {}\n".format(APP_NAME, path.basename(caller.filename), caller.lineno, message))


def debug(message):
    """ Prints a debug message in the default output"""
    if ApplicationSettings.the().debug_enabled:
        caller = getframeinfo(stack()[1][0])
        FreeCAD.Console.PrintWarning("[DEBUG][{}] {}:{} -> {}\n".format(APP_NAME, path.basename(caller.filename), caller.lineno, message))


def dump_to_disk(text):
    """ Dumps text content into a file on disk """
    with open("/tmp/{}".format(DISK_DUMP_FILE_NAME), "w", encoding="utf-8") as error_dump:
        error_dump.write(str(text))


def print_license():
    """ Prints this software license. """
    licpath = "{}{}".format(path.abspath(__file__).split("mod")[0], "LICENSE")
    if path.isfile(licpath) and ApplicationSettings.the().verbose_enabled:
        with open(licpath, encoding="utf-8") as licfile:
            FreeCAD.Console.PrintMessage(licfile.read())
            FreeCAD.Console.PrintMessage("\n\n")
