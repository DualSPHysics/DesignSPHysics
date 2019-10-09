#!/usr/bin/env python3.7
# -*- coding: utf-8 -*-
"""DesignSPHysics GUI Utils.

This module stores functionality useful for GUI
operations in DesignSPHysics.

"""

import os

from PySide import QtGui


def h_line_generator() -> QtGui.QFrame:
    """ Generates an horizontal line that can be used as a separator."""
    to_ret = QtGui.QFrame()
    to_ret.setFrameShape(QtGui.QFrame.HLine)
    to_ret.setFrameShadow(QtGui.QFrame.Sunken)
    return to_ret


def v_line_generator() -> QtGui.QFrame:
    """ Generates a vertical line that can be used as a separator"""
    to_ret = QtGui.QFrame()
    to_ret.setFrameShape(QtGui.QFrame.VLine)
    to_ret.setFrameShadow(QtGui.QFrame.Sunken)
    return to_ret


def get_icon(file_name, return_only_path=False) -> QtGui.QIcon:
    """ Returns a QIcon to use with DesignSPHysics. Retrieves a file with filename (like image.png) from the images folder. """
    file_to_load = os.path.dirname(os.path.abspath(__file__)) + "/../images/{}".format(file_name)
    if os.path.isfile(file_to_load):
        return file_to_load if return_only_path else QtGui.QIcon(file_to_load)
    raise IOError("File {} not found in images folder".format(file_name))
