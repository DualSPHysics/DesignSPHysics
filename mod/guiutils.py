#!/usr/bin/env python3.7
# -*- coding: utf-8 -*-
'''DesignSPHysics GUI Utils.

This module stores functionality useful for GUI
operations in DesignSPHysics.

'''

import os
import subprocess

from PySide import QtGui, QtCore

import mod.utils
import mod.constants
from mod.dialog_tools import error_dialog


def h_line_generator():
    ''' Generates an horizontal line that can be used as a separator.'''
    to_ret = QtGui.QFrame()
    to_ret.setFrameShape(QtGui.QFrame.HLine)
    to_ret.setFrameShadow(QtGui.QFrame.Sunken)
    return to_ret


def v_line_generator():
    ''' Generates a vertical line that can be used as a separator'''
    to_ret = QtGui.QFrame()
    to_ret.setFrameShape(QtGui.QFrame.VLine)
    to_ret.setFrameShadow(QtGui.QFrame.Sunken)
    return to_ret


def get_icon(file_name, return_only_path=False):
    ''' Returns a QIcon to use with DesignSPHysics.
    Retrieves a file with filename (like image.png) from the images folder. '''
    file_to_load = os.path.dirname(os.path.abspath(__file__)) + "/../images/{}".format(file_name)
    if os.path.isfile(file_to_load):
        return file_to_load if return_only_path else QtGui.QIcon(file_to_load)
    else:
        raise IOError("File {} not found in images folder".format(file_name))


def widget_state_config(widgets, config):
    ''' Takes an widget dictionary and a config string to
        enable and disable certain widgets base on a case. '''
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
        widgets['post_proc_boundaryvtk_button'].setEnabled(False)
        widgets['post_proc_flowtool_button'].setEnabled(False)
        widgets["objectlist_table"].setEnabled(False)
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
        widgets['post_proc_boundaryvtk_button'].setEnabled(False)
        widgets['post_proc_flowtool_button'].setEnabled(False)
        widgets["casecontrols_bt_addfillbox"].setEnabled(True)
        widgets["casecontrols_bt_addgeo"].setEnabled(True)
        widgets["summary_bt"].setEnabled(True)
        widgets["toggle3dbutton"].setEnabled(True)
        widgets["dampingbutton"].setEnabled(True)
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
        widgets['post_proc_boundaryvtk_button'].setEnabled(True)
        widgets['post_proc_flowtool_button'].setEnabled(True)
    elif config == "simulation not done":
        widgets['post_proc_partvtk_button'].setEnabled(True)
        widgets['post_proc_computeforces_button'].setEnabled(True)
        widgets['post_proc_floatinginfo_button'].setEnabled(True)
        widgets['post_proc_measuretool_button'].setEnabled(True)
        widgets['post_proc_isosurface_button'].setEnabled(True)
        widgets['post_proc_boundaryvtk_button'].setEnabled(True)
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
        widgets['post_proc_boundaryvtk_button'].setEnabled(False)
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
        widgets['post_proc_boundaryvtk_button'].setEnabled(True)
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
        widgets['post_proc_boundaryvtk_button'].setEnabled(True)
        widgets['post_proc_flowtool_button'].setEnabled(True)
    elif config == "sim finished":
        widgets['post_proc_partvtk_button'].setEnabled(True)
        widgets['post_proc_computeforces_button'].setEnabled(True)
        widgets['post_proc_floatinginfo_button'].setEnabled(True)
        widgets['post_proc_measuretool_button'].setEnabled(True)
        widgets['post_proc_isosurface_button'].setEnabled(True)
        widgets['post_proc_boundaryvtk_button'].setEnabled(True)
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
        widgets['post_proc_boundaryvtk_button'].setEnabled(False)
        widgets['post_proc_flowtool_button'].setEnabled(False)
    elif config == "export cancel":
        widgets['post_proc_partvtk_button'].setEnabled(True)
        widgets['post_proc_computeforces_button'].setEnabled(True)
        widgets['post_proc_floatinginfo_button'].setEnabled(True)
        widgets['post_proc_measuretool_button'].setEnabled(True)
        widgets['post_proc_isosurface_button'].setEnabled(True)
        widgets['post_proc_boundaryvtk_button'].setEnabled(True)
        widgets['post_proc_flowtool_button'].setEnabled(True)
    elif config == "export finished":
        widgets['post_proc_partvtk_button'].setEnabled(True)
        widgets['post_proc_computeforces_button'].setEnabled(True)
        widgets['post_proc_floatinginfo_button'].setEnabled(True)
        widgets['post_proc_measuretool_button'].setEnabled(True)
        widgets['post_proc_isosurface_button'].setEnabled(True)
        widgets['post_proc_boundaryvtk_button'].setEnabled(True)
        widgets['post_proc_flowtool_button'].setEnabled(True)


def case_summary(orig_data):
    ''' Displays a dialog with a summary of the current opened case. '''

    # TODO: This should be implemented as a custom class like CaseSummary(QtGui.QDialog)

    if not mod.utils.valid_document_environment():
        return

    # Data copy to avoid referencing issues
    data = dict(orig_data)

    # Preprocess data to show in data copy
    data['gravity'] = "({}, {}, {})".format(*data['gravity'])
    if data['project_name'] == "":
        data['project_name'] = "<i>{}</i>".format(mod.utils.__("Not yet saved"))

    if data['project_path'] == "":
        data['project_path'] = "<i>{}</i>".format(mod.utils.__("Not yet saved"))

    for k in ['gencase_path', 'dsphysics_path', 'partvtk4_path']:
        if data[k] == "":
            data[k] = "<i>{}</i>".format(
                mod.utils.__("Executable not correctly set"))

    data['stepalgorithm'] = {
        '1': 'Verlet',
        '2': 'Symplectic'
    }[str(data['stepalgorithm'])]
    data['project_mode'] = '3D' if data['3dmode'] else '2D'

    #data['incz'] = float(data['incz']) * 100
    data['partsoutmax'] = float(data['partsoutmax']) * 100

    # Setting certain values to automatic
    for x in ['hswl', 'speedsystem', 'speedsound', 'h', 'b', 'massfluid', 'massbound']:
        data[x] = '<u>Automatic</u>' if data[x + '_auto'] else data[x]

    # region Formatting objects info
    data['objects_info'] = ""
    if len(data['simobjects']) > 1:
        data['objects_info'] += "<ul>"
        # data['simobjects'] is a dict with format
        # {'key': ['mk', 'type', 'fill']} where key is an internal name.
        for key, value in data['simobjects'].items():
            if key.lower() == 'case_limits':
                continue
            fc_object = mod.utils.get_fc_object(key)
            is_floating = mod.utils.__('Yes') if str(
                value[0]) in data['floating_mks'].keys() else mod.utils.__('No')
            is_floating = mod.utils.__('No') if value[
                1].lower() == "fluid" else is_floating
            has_initials = mod.utils.__('Yes') if str(
                value[0]) in data['initials_mks'].keys() else mod.utils.__('No')
            has_initials = mod.utils.__('No') if value[
                1].lower() == "bound" else has_initials
            real_mk = value[0] + 11 if value[
                1].lower() == "bound" else value[0] + 1
            data['objects_info'] += "<li><b>{label}</b> (<i>{iname}</i>): <br/>" \
                                    "Type: {type} (MK{type}: <b>{mk}</b> ; MK: <b>{real_mk}</b>)<br/>" \
                                    "Fill mode: {fillmode}<br/>" \
                                    "Floating: {floats}<br/>" \
                                    "Initials: {initials}</li><br/>".format(label=fc_object.Label, iname=key,
                                                                            type=value[1].title(), mk=value[0],
                                                                            real_mk=str(
                                                                                real_mk),
                                                                            fillmode=value[2].title(
                                                                            ),
                                                                            floats=is_floating,
                                                                            initials=has_initials)
        data['objects_info'] += "</ul>"
    else:
        data['objects_info'] += mod.utils.__(
            "No objects were added to the simulation yet.")
    # endregion Formatting objects info

    # region Formatting movement info
    data['movement_info'] = ""
    if len(data['simobjects']) > 1:
        data['movement_info'] += "<ul>"
        for mov in data['global_movements']:
            try:
                movtype = mov.type
            except AttributeError:
                movtype = mov.__class__.__name__

            mklist = list()
            for key, value in data['motion_mks'].items():
                if mov in value:
                    mklist.append(str(key))

            data['movement_info'] += "<li>{movtype} <u>{movname}</u><br/>" \
                                     "Applied to MKBound: {mklist}</li><br/>".format(movtype=movtype, movname=mov.name, mklist=', '.join(mklist))

        data['movement_info'] += "</ul>"
    else:
        data['movement_info'] += "No movements were defined in this case."

    # Create a string with MK used (of each type)
    data['mkboundused'] = list()
    data['mkfluidused'] = list()
    for element in data['simobjects'].values():
        if element[1].lower() == 'bound':
            data['mkboundused'].append(str(element[0]))
        elif element[1].lower() == 'fluid':
            data['mkfluidused'].append(str(element[0]))

    data['mkboundused'] = ", ".join(
        data['mkboundused']) if data['mkboundused'] else "None"
    data['mkfluidused'] = ", ".join(
        data['mkfluidused']) if data['mkfluidused'] else "None"

    data['last_number_particles'] = data['last_number_particles'] if data['last_number_particles'] >= 0 else "GenCase wasn't executed"

    # endregion Formatting movement info
    # Dialog creation and template filling
    main_window = QtGui.QDialog()
    main_layout = QtGui.QVBoxLayout()
    info = QtGui.QTextEdit()

    lib_folder = os.path.dirname(os.path.realpath(__file__))

    try:
        with open("{}/templates/case_summary_template.html".format(lib_folder),
                  "r") as input_template:
            info_text = input_template.read().format(**data)
    except:
        error_dialog("An error occurred trying to load the template file and format it.")
        return

    info.setText(info_text)
    info.setReadOnly(True)

    main_layout.addWidget(info)
    main_window.setLayout(main_layout)
    main_window.setModal(True)
    main_window.setMinimumSize(500, 650)
    main_window.exec_()


def gencase_completed_dialog(particle_count=0, detail_text="No details", data=dict(), temp_data=dict()):
    ''' Creates a gencase save dialog with different options, like
    open the results with paraview, show details or dismiss. '''

    # TODO: This should be implemented as a custom class like GenCaseCompleteDialog(QtGui.QDialog)

    # Window Creation
    window = QtGui.QDialog()
    window.setWindowModality(QtCore.Qt.NonModal)
    window.setWindowTitle(mod.utils.__("Save & GenCase"))

    # Main Layout creation
    main_layout = QtGui.QVBoxLayout()

    # Main Layout elements
    info_message = QtGui.QLabel(
        mod.utils.__("Gencase exported {} particles.\nPress \"Details\" to check the output").format(
            str(particle_count)))

    button_layout = QtGui.QHBoxLayout()
    bt_open_with_paraview = QtGui.QPushButton(mod.utils.__("Open with Paraview"))
    temp_data['widget_saver'] = QtGui.QMenu()
    temp_data['widget_saver'].addAction("{}_MkCells.vtk".format(data['project_name']))
    temp_data['widget_saver'].addAction("{}_All.vtk".format(data['project_name']))
    temp_data['widget_saver'].addAction("{}_Fluid.vtk".format(data['project_name']))
    temp_data['widget_saver'].addAction("{}_Bound.vtk".format(data['project_name']))
    bt_open_with_paraview.setMenu(temp_data['widget_saver'])
    bt_details = QtGui.QPushButton(mod.utils.__("Details"))
    bt_ok = QtGui.QPushButton(mod.utils.__("Ok"))
    button_layout.addWidget(bt_open_with_paraview)
    button_layout.addWidget(bt_details)
    button_layout.addWidget(bt_ok)

    # Details popup window
    detail_text_dialog = QtGui.QDialog()
    detail_text_dialog.setMinimumWidth(650)
    detail_text_dialog.setModal(False)
    detail_text_dialog_layout = QtGui.QVBoxLayout()

    detail_text_area = QtGui.QTextEdit()
    detail_text_area.setText(detail_text)

    detail_text_dialog_layout.addWidget(detail_text_area)
    detail_text_dialog.setLayout(detail_text_dialog_layout)

    # Main Layout scaffolding
    main_layout.addWidget(info_message)
    main_layout.addLayout(button_layout)

    # Window logic
    detail_text_dialog.hide()

    if len(data["paraview_path"]) > 1:
        bt_open_with_paraview.show()
    else:
        bt_open_with_paraview.hide()

    def on_ok():
        detail_text_dialog.hide()
        window.accept()

    def on_view_details():
        if detail_text_dialog.isVisible():
            detail_text_dialog.hide()
        else:
            detail_text_dialog.show()
            detail_text_dialog.move(
                window.x() - detail_text_dialog.width() - 15,
                window.y() - abs(window.height() - detail_text_dialog.height()) / 2)

    def on_open_paraview_menu(action):
        try:
            subprocess.Popen(
                [
                    data['paraview_path'],
                    "--data={}\\{}".format(
                        data['project_path'] + '\\' +
                        data['project_name'] + '_out',
                        action.text()
                    )
                ],
                stdout=subprocess.PIPE)
            detail_text_dialog.hide()
            window.accept()
        except:
            error_dialog(
                "ERROR! \nCheck the ParaView executable path, it may have been saved from previously opened case!")
            return

    bt_ok.clicked.connect(on_ok)
    bt_details.clicked.connect(on_view_details)
    temp_data['widget_saver'].triggered.connect(on_open_paraview_menu)

    # Window scaffolding and execution
    window.setLayout(main_layout)
    window.show()
