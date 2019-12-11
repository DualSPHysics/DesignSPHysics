#!/usr/bin/env python3.7
# -*- coding: utf-8 -*-
""" DesignsSPHysics Case Summary Dialog """

from PySide import QtGui

from mod.translation_tools import __
from mod.template_tools import get_template_text, obj_to_dict
from mod.freecad_tools import get_fc_object

from mod.constants import CASE_LIMITS_OBJ_NAME, MKFLUID_LIMIT, MKFLUID_OFFSET
from mod.enums import ObjectType

from mod.dataobjects.case import Case
from mod.dataobjects.simulation_object import SimulationObject
from mod.dataobjects.motion.movement import Movement


class CaseSummary(QtGui.QDialog):
    """ Dialog that shows summarized case details in html format. """

    CASE_SUMMARY_TEMPLATE = "/templates/case_summary_template.html"

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.main_layout = QtGui.QVBoxLayout()
        self.info = QtGui.QTextEdit()
        self.close_button = QtGui.QPushButton(__("Close"))
        self.close_button.clicked.connect(self.accept)

        self.info_text = get_template_text(self.CASE_SUMMARY_TEMPLATE).format(**self.get_formatter())

        self.info.setText(self.info_text)
        self.info.setReadOnly(True)

        self.main_layout.addWidget(self.info)
        self.main_layout.addWidget(self.close_button)
        self.setLayout(self.main_layout)
        self.setModal(True)
        self.setMinimumSize(700, 650)
        self.exec_()

    def get_formatter(self) -> dict:
        """ Returns a dictionary to format the summary template. """
        case_dict = obj_to_dict(Case.the())

        # FIXME: Add domainfixed on parameters
        # FIXME: Add periodicity in template
        # FIXME: Add meaningful values to enumerated types

        case_dict.update({
            "_mode3d": "3D" if case_dict["mode3d"] else "2D",
            "_gravity": "({}, {}, {})".format(*case_dict["constants"]["gravity"]),
            "_hswl": "Automatic" if case_dict["constants"]["hswl_auto"] else "{} meters".format(case_dict["constants"]["hswl"]),
            "_speedsystem": "Automatic" if case_dict["constants"]["speedsystem_auto"] else "{} m/s".format(case_dict["constants"]["speedsystem"]),
            "_h": "Automatic" if case_dict["constants"]["h_auto"] else "{} meters".format(case_dict["constants"]["h"]),
            "_b": "Automatic" if case_dict["constants"]["b_auto"] else "{} meters".format(case_dict["constants"]["b"]),
            "_massbound": "Automatic" if case_dict["constants"]["massbound_auto"] else "{} Kg".format(case_dict["constants"]["massbound"]),
            "_massfluid": "Automatic" if case_dict["constants"]["massfluid_auto"] else "{} Kg".format(case_dict["constants"]["massfluid"]),
            "_dtini": "Automatic" if case_dict["execution_parameters"]["dtini_auto"] else "{}".format(case_dict["execution_parameters"]["dtini"]),
            "_dtmin": "Automatic" if case_dict["execution_parameters"]["dtmin_auto"] else "{}".format(case_dict["execution_parameters"]["dtmin"]),
            "_mkfluidused": ", ".join(self.get_used_mkfluids()) if self.get_used_mkfluids() else "None",
            "_mkboundused": ", ".join(self.get_used_mkbounds()) if self.get_used_mkbounds() else "None",
            "_objects_info": self.get_objects_info(),
            "_movement_info": self.get_movements_info(),
        })

        return case_dict

    def get_used_mkfluids(self) -> list:
        "Retrurns a list with all the MKFluid numbers used on the case."
        to_ret = list()
        for obj in Case.the().get_all_fluid_objects():
            if str(obj.obj_mk) not in to_ret:
                to_ret.append(str(obj.obj_mk))
        return to_ret

    def get_used_mkbounds(self) -> list:
        "Retrurns a list with all the MKBound numbers used on the case."
        to_ret = list()
        for obj in Case.the().get_all_bound_objects():
            if str(obj.obj_mk) not in to_ret:
                to_ret.append(str(obj.obj_mk))
        return to_ret

    def get_objects_info(self) -> str:
        """ Returns an HTML string with information about the objects in the case. """
        each_object_info: list = list()

        obj: SimulationObject = None
        for obj in Case.the().objects:
            if obj.name == CASE_LIMITS_OBJ_NAME:
                continue

            is_floating_text: str = "Yes" if Case.the().get_mk_based_properties(obj.type, obj.obj_mk).float_property else "No"
            has_initials_text: str = "Yes" if Case.the().get_mk_based_properties(obj.type, obj.obj_mk).initials else "No"

            to_append = "<li>"
            to_append += "<b>{}</b> ({})<br>".format(get_fc_object(obj.name).Label, obj.name)
            to_append += "Type: {type} (MK{type}: <b>{mk}</b> ; MK: <b>{real_mk}</b>)<br/>".format(type=str(obj.type).capitalize(),
                                                                                                   mk=str(obj.obj_mk),
                                                                                                   real_mk=str(obj.obj_mk + MKFLUID_OFFSET if obj.type == ObjectType.FLUID else obj.obj_mk + MKFLUID_LIMIT))
            to_append += "Fill mode: {}<br/>".format(str(obj.fillmode).capitalize())
            to_append += "Floating: {}<br/>".format(is_floating_text)
            to_append += "Initials: {}</li><br/>".format(has_initials_text)
            to_append += "</li>"

            each_object_info.append(to_append)

        return "<ul>{}</ul>".format("".join(each_object_info) if each_object_info else "No objects were added to the case.")

    def get_movements_info(self) -> str:
        """ Returns an HTML string with information about the movements in the case. """
        each_movement_info: list = list()

        movement: Movement = None
        for movement in Case.the().info.global_movements:
            mklist = list()
            for mkbasedproperties in Case.the().mkbasedproperties.values():
                if movement in mkbasedproperties.movements:
                    mklist.append(str(mkbasedproperties.mk - MKFLUID_LIMIT))

            to_append = "<li>"
            to_append += "{}: <u>{}</u><br>".format(movement.type, movement.name)
            to_append += "Applied to MKBound: {}".format(", ".join(mklist) if mklist else "None")
            to_append += "</li><br>"
            each_movement_info.append(to_append)

        return "<ul>{}</ul>".format("".join(each_movement_info) if each_movement_info else "No movements were defined in the case.")
