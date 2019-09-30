#!/usr/bin/env python3.7
# -*- coding: utf-8 -*-
'''DesignSPHysics GUI Utils.

This module stores functionality useful for GUI
operations in DesignSPHysics.

'''

import os

from PySide import QtGui


def h_line_generator() -> QtGui.QFrame:
    ''' Generates an horizontal line that can be used as a separator.'''
    to_ret = QtGui.QFrame()
    to_ret.setFrameShape(QtGui.QFrame.HLine)
    to_ret.setFrameShadow(QtGui.QFrame.Sunken)
    return to_ret


def v_line_generator() -> QtGui.QFrame:
    ''' Generates a vertical line that can be used as a separator'''
    to_ret = QtGui.QFrame()
    to_ret.setFrameShape(QtGui.QFrame.VLine)
    to_ret.setFrameShadow(QtGui.QFrame.Sunken)
    return to_ret


def get_icon(file_name, return_only_path=False) -> QtGui.QIcon:
    ''' Returns a QIcon to use with DesignSPHysics. Retrieves a file with filename (like image.png) from the images folder. '''
    file_to_load = os.path.dirname(os.path.abspath(__file__)) + "/../images/{}".format(file_name)
    if os.path.isfile(file_to_load):
        return file_to_load if return_only_path else QtGui.QIcon(file_to_load)
    raise IOError("File {} not found in images folder".format(file_name))


def widget_state_config(widgets, config):
    ''' Takes an widget dictionary and a config string to
        enable and disable certain widgets base on a case. '''

    # FIXME: Refactor this. It's hideous
    return

    if config == "no case":
        widgets["casecontrols_bt_savedoc"].setEnabled(False)
        widgets["rungencase_bt"].setEnabled(False)
        widgets["constants_button"].setEnabled(False)
        widgets["execparams_button"].setEnabled(False)
        widgets["casecontrols_bt_addfillbox"].setEnabled(False)
        widgets["casecontrols_bt_addgeo"].setEnabled(False)
        widgets["ex_button"].setEnabled(False)
        widgets["ex_additional"].setEnabled(False)
        widgets["ex_selector_combo"].setEnabled(False)
        widgets['post_proc_partvtk_button'].setEnabled(False)
        widgets['post_proc_computeforces_button'].setEnabled(False)
        widgets['post_proc_floatinginfo_button'].setEnabled(False)
        widgets['post_proc_measuretool_button'].setEnabled(False)
        widgets['post_proc_isosurface_button'].setEnabled(False)
        widgets['post_proc_flowtool_button'].setEnabled(False)
        widgets["dock_object_list_table_widget"].setEnabled(False)
        widgets["dp_input"].setEnabled(False)
        widgets["summary_bt"].setEnabled(False)
        widgets["toggle3dbutton"].setEnabled(False)
        widgets["dampingbutton"].setEnabled(False)
    elif config == "new case":
        widgets["constants_button"].setEnabled(True)
        widgets["execparams_button"].setEnabled(True)
        widgets["casecontrols_bt_savedoc"].setEnabled(True)
        widgets["rungencase_bt"].setEnabled(True)
        widgets["dp_input"].setEnabled(True)
        widgets["ex_selector_combo"].setEnabled(False)
        widgets["ex_button"].setEnabled(False)
        widgets["ex_additional"].setEnabled(False)
        widgets['post_proc_partvtk_button'].setEnabled(False)
        widgets['post_proc_computeforces_button'].setEnabled(False)
        widgets['post_proc_floatinginfo_button'].setEnabled(False)
        widgets['post_proc_measuretool_button'].setEnabled(False)
        widgets['post_proc_isosurface_button'].setEnabled(False)
        widgets['post_proc_flowtool_button'].setEnabled(False)
        widgets["casecontrols_bt_addfillbox"].setEnabled(True)
        widgets["casecontrols_bt_addgeo"].setEnabled(True)
        widgets["summary_bt"].setEnabled(True)
        widgets["toggle3dbutton"].setEnabled(True)
        widgets["dampingbutton"].setEnabled(True)
        widgets["dock_object_list_table_widget"].setEnabled(True)
    elif config == "gencase done":
        widgets["ex_selector_combo"].setEnabled(True)
        widgets["ex_button"].setEnabled(True)
        widgets["ex_additional"].setEnabled(True)
    elif config == "gencase not done":
        widgets["ex_selector_combo"].setEnabled(False)
        widgets["ex_button"].setEnabled(False)
        widgets["ex_additional"].setEnabled(False)
    elif config == "load base":
        widgets["constants_button"].setEnabled(True)
        widgets["execparams_button"].setEnabled(True)
        widgets["casecontrols_bt_savedoc"].setEnabled(True)
        widgets["rungencase_bt"].setEnabled(True)
        widgets["dp_input"].setEnabled(True)
        widgets["casecontrols_bt_addfillbox"].setEnabled(True)
        widgets["casecontrols_bt_addgeo"].setEnabled(True)
        widgets["summary_bt"].setEnabled(True)
        widgets["toggle3dbutton"].setEnabled(True)
        widgets["dampingbutton"].setEnabled(True)
    elif config == "simulation done":
        widgets['post_proc_partvtk_button'].setEnabled(True)
        widgets['post_proc_computeforces_button'].setEnabled(True)
        widgets['post_proc_floatinginfo_button'].setEnabled(True)
        widgets['post_proc_measuretool_button'].setEnabled(True)
        widgets['post_proc_isosurface_button'].setEnabled(True)
        widgets['post_proc_flowtool_button'].setEnabled(True)
    elif config == "simulation not done":
        widgets['post_proc_partvtk_button'].setEnabled(True)
        widgets['post_proc_computeforces_button'].setEnabled(True)
        widgets['post_proc_floatinginfo_button'].setEnabled(True)
        widgets['post_proc_measuretool_button'].setEnabled(True)
        widgets['post_proc_isosurface_button'].setEnabled(True)
        widgets['post_proc_flowtool_button'].setEnabled(True)
    elif config == "execs not correct":
        widgets["ex_selector_combo"].setEnabled(False)
        widgets["ex_button"].setEnabled(False)
        widgets["ex_additional"].setEnabled(False)
        widgets['post_proc_partvtk_button'].setEnabled(False)
        widgets['post_proc_computeforces_button'].setEnabled(False)
        widgets['post_proc_floatinginfo_button'].setEnabled(False)
        widgets['post_proc_measuretool_button'].setEnabled(False)
        widgets['post_proc_isosurface_button'].setEnabled(False)
        widgets['post_proc_flowtool_button'].setEnabled(False)
    elif config == "sim start":
        widgets["ex_button"].setEnabled(False)
        widgets["ex_additional"].setEnabled(False)
        widgets["ex_selector_combo"].setEnabled(False)
        widgets['post_proc_partvtk_button'].setEnabled(True)
        widgets['post_proc_computeforces_button'].setEnabled(True)
        widgets['post_proc_floatinginfo_button'].setEnabled(True)
        widgets['post_proc_measuretool_button'].setEnabled(True)
        widgets['post_proc_isosurface_button'].setEnabled(True)
        widgets['post_proc_flowtool_button'].setEnabled(True)
    elif config == "sim cancel":
        widgets["ex_selector_combo"].setEnabled(True)
        widgets["ex_button"].setEnabled(True)
        widgets["ex_additional"].setEnabled(True)
        # Post-proccessing is enabled on cancel, to evaluate only currently exported parts
        widgets['post_proc_partvtk_button'].setEnabled(True)
        widgets['post_proc_computeforces_button'].setEnabled(True)
        widgets['post_proc_floatinginfo_button'].setEnabled(True)
        widgets['post_proc_measuretool_button'].setEnabled(True)
        widgets['post_proc_isosurface_button'].setEnabled(True)
        widgets['post_proc_flowtool_button'].setEnabled(True)
    elif config == "sim finished":
        widgets['post_proc_partvtk_button'].setEnabled(True)
        widgets['post_proc_computeforces_button'].setEnabled(True)
        widgets['post_proc_floatinginfo_button'].setEnabled(True)
        widgets['post_proc_measuretool_button'].setEnabled(True)
        widgets['post_proc_isosurface_button'].setEnabled(True)
        widgets['post_proc_flowtool_button'].setEnabled(True)
    elif config == "sim error":
        widgets["ex_selector_combo"].setEnabled(True)
        widgets["ex_button"].setEnabled(True)
        widgets["ex_additional"].setEnabled(True)
    elif config == "export start":
        widgets['post_proc_partvtk_button'].setEnabled(False)
        widgets['post_proc_computeforces_button'].setEnabled(False)
        widgets['post_proc_floatinginfo_button'].setEnabled(False)
        widgets['post_proc_measuretool_button'].setEnabled(False)
        widgets['post_proc_isosurface_button'].setEnabled(False)
        widgets['post_proc_flowtool_button'].setEnabled(False)
    elif config == "export cancel":
        widgets['post_proc_partvtk_button'].setEnabled(True)
        widgets['post_proc_computeforces_button'].setEnabled(True)
        widgets['post_proc_floatinginfo_button'].setEnabled(True)
        widgets['post_proc_measuretool_button'].setEnabled(True)
        widgets['post_proc_isosurface_button'].setEnabled(True)
        widgets['post_proc_flowtool_button'].setEnabled(True)
    elif config == "export finished":
        widgets['post_proc_partvtk_button'].setEnabled(True)
        widgets['post_proc_computeforces_button'].setEnabled(True)
        widgets['post_proc_floatinginfo_button'].setEnabled(True)
        widgets['post_proc_measuretool_button'].setEnabled(True)
        widgets['post_proc_isosurface_button'].setEnabled(True)
        widgets['post_proc_flowtool_button'].setEnabled(True)
