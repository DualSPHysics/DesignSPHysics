#!/usr/bin/env python3.7
# -*- coding: utf-8 -*-
""" DesignsSPHysics Case Summary Dialog """

from PySide import QtGui

from mod.enums import Template
from mod.template_tools import get_template, obj_to_dict

from mod.dataobjects.case import Case

# FIXME: Finish this when data is more consistent
class CaseSummary(QtGui.QDialog):
    """ Dialog that shows summarized case details in html format. """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.main_layout = QtGui.QVBoxLayout()
        self.info = QtGui.QTextEdit()

        self.summary_template = get_template(Template.CASE_SUMMARY)

        self.info_text = self.summary_template.format(obj_to_dict(Case.instance()))

        self.info.setText(self.info_text)
        self.info.setReadOnly(True)

        self.main_layout.addWidget(self.info)
        self.setLayout(self.main_layout)
        self.setModal(True)
        self.setMinimumSize(500, 650)
        self.exec_()


# def case_summary(orig_data):
#     """ Displays a dialog with a summary of the current opened case. """
#     if not mod.file_tools.valid_document_environment():
#         return

#     # Data copy to avoid referencing issues
#     data = dict(orig_data)

#     # Preprocess data to show in data copy
#     data["gravity"] = "({}, {}, {})".format(*data["gravity"])
#     if data["project_name"] == "":
#         data["project_name"] = "<i>{}</i>".format(mod.file_tools.__("Not yet saved"))

#     if data["project_path"] == "":
#         data["project_path"] = "<i>{}</i>".format(mod.file_tools.__("Not yet saved"))

#     for k in ["gencase_path", "dsphysics_path", "partvtk4_path"]:
#         if data[k] == "":
#             data[k] = "<i>{}</i>".format(
#                 mod.file_tools.__("Executable not correctly set"))

#     data["stepalgorithm"] = {
#         "1": "Verlet",
#         "2": "Symplectic"
#     }[str(data["stepalgorithm"])]
#     data["project_mode"] = "3D" if data["3dmode"] else "2D"

#     #data["incz"] = float(data["incz"]) * 100
#     data["partsoutmax"] = float(data["partsoutmax"]) * 100

#     # Setting certain values to automatic
#     for x in ["hswl", "speedsystem", "speedsound", "h", "b", "massfluid", "massbound"]:
#         data[x] = "<u>Automatic</u>" if data[x + "_auto"] else data[x]

#     # region Formatting objects info
#     data["objects_info"] = ""
#     if len(data["simobjects"]) > 1:
#         data["objects_info"] += "<ul>"
#         # data["simobjects"] is a dict with format
#         # {"key": ["mk", "type", "fill"]} where key is an internal name.
#         for key, value in data["simobjects"].items():
#             if key.lower() == "case_limits":
#                 continue
#             fc_object = mod.file_tools.get_fc_object(key)
#             is_floating = mod.file_tools.__("Yes") if str(
#                 value[0]) in data["floating_mks"].keys() else mod.file_tools.__("No")
#             is_floating = mod.file_tools.__("No") if value[
#                 1].lower() == "fluid" else is_floating
#             has_initials = mod.file_tools.__("Yes") if str(
#                 value[0]) in data["initials_mks"].keys() else mod.file_tools.__("No")
#             has_initials = mod.file_tools.__("No") if value[
#                 1].lower() == "bound" else has_initials
#             real_mk = value[0] + 11 if value[
#                 1].lower() == "bound" else value[0] + 1
#             data["objects_info"] += "<li><b>{label}</b> (<i>{iname}</i>): <br/>" \
#                                     "Type: {type} (MK{type}: <b>{mk}</b> ; MK: <b>{real_mk}</b>)<br/>" \
#                                     "Fill mode: {fillmode}<br/>" \
#                                     "Floating: {floats}<br/>" \
#                                     "Initials: {initials}</li><br/>".format(label=fc_object.Label, iname=key,
#                                                                             type=value[1].title(), mk=value[0],
#                                                                             real_mk=str(
#                                                                                 real_mk),
#                                                                             fillmode=value[2].title(
#                                                                             ),
#                                                                             floats=is_floating,
#                                                                             initials=has_initials)
#         data["objects_info"] += "</ul>"
#     else:
#         data["objects_info"] += mod.file_tools.__(
#             "No objects were added to the simulation yet.")
#     # endregion Formatting objects info

#     # region Formatting movement info
#     data["movement_info"] = ""
#     if len(data["simobjects"]) > 1:
#         data["movement_info"] += "<ul>"
#         for mov in data["global_movements"]:
#             try:
#                 movtype = mov.type
#             except AttributeError:
#                 movtype = mov.__class__.__name__

#             mklist = list()
#             for key, value in data["motion_mks"].items():
#                 if mov in value:
#                     mklist.append(str(key))

#             data["movement_info"] += "<li>{movtype} <u>{movname}</u><br/>" \
#                                      "Applied to MKBound: {mklist}</li><br/>".format(movtype=movtype, movname=mov.name, mklist=", ".join(mklist))

#         data["movement_info"] += "</ul>"
#     else:
#         data["movement_info"] += "No movements were defined in this case."

#     # Create a string with MK used (of each type)
#     data["mkboundused"] = list()
#     data["mkfluidused"] = list()
#     for element in data["simobjects"].values():
#         if element[1].lower() == "bound":
#             data["mkboundused"].append(str(element[0]))
#         elif element[1].lower() == "fluid":
#             data["mkfluidused"].append(str(element[0]))

#     data["mkboundused"] = ", ".join(
#         data["mkboundused"]) if data["mkboundused"] else "None"
#     data["mkfluidused"] = ", ".join(
#         data["mkfluidused"]) if data["mkfluidused"] else "None"

#     data["last_number_particles"] = data["last_number_particles"] if data["last_number_particles"] >= 0 else "GenCase wasn't executed"

#     # endregion Formatting movement info
#     # Dialog creation and template filling
#     main_window = QtGui.QDialog()
#     main_layout = QtGui.QVBoxLayout()
#     info = QtGui.QTextEdit()

#     lib_folder = os.path.dirname(os.path.realpath(__file__))

#     try:
#         with open("{}/templates/case_summary_template.html".format(lib_folder),
#                   "r") as input_template:
#             info_text = input_template.read().format(**data)
#     except:
#         error_dialog("An error occurred trying to load the template file and format it.")
#         return

#     info.setText(info_text)
#     info.setReadOnly(True)

#     main_layout.addWidget(info)
#     main_window.setLayout(main_layout)
#     main_window.setModal(True)
#     main_window.setMinimumSize(500, 650)
#     main_window.exec_()
