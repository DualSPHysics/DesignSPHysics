#!/usr/bin/env python3.7
# -*- coding: utf-8 -*-

''' Executable related tools. '''

from os import path, environ, chdir
from sys import platform

from PySide import QtCore

import FreeCADGui


def executable_contains_string(executable: str, string: str) -> bool:
    ''' Returns whether the standard output of the executable contains the passed string.
        The string passed as a parameters is not case sensitive. '''
    refocus_cwd()
    if path.isfile(executable):
        process = QtCore.QProcess(FreeCADGui.getMainWindow())

        if platform in ("linux", "linux2"):
            environ["LD_LIBRARY_PATH"] = path.dirname(executable)

        process.start('"{}" -ver'.format(executable))
        process.waitForFinished()
        output = str(process.readAllStandardOutput())

        return string.lower() in output.lower()

    return False


def refocus_cwd():
    ''' Ensures the current working directory is the DesignSPHysics folder '''
    chdir("{}/..".format(path.dirname(path.abspath(__file__))))


def are_executables_bundled():
    ''' Returns if the DualSPHysics executable directory exists'''
    dsph_execs_path = "{}/../dualsphysics/bin/".format(path.dirname(path.realpath(__file__)))
    return path.isdir(dsph_execs_path)
