# -*- coding: utf-8 -*-
"""XML Exporter for DesignSPHysics

The utilities on this module creates

"""

import os
from datetime import datetime

import FreeCAD

from mod.constants import APP_NAME, DIVIDER, LINE_END
from mod.enums import FloatingDensityType
from mod.template_tools import obj_to_dict

class XMLExporter():
    """ Handles XML generation and data transformation to adapt to DualSPHysics
    preprocessing tools """

    BASE_XML = "/templates/gencase/base.xml"
    DEFINITION_XML = "/templates/gencase/definition.xml"
    SIMULATIONDOMAIN_XML = "/templates/gencase/simulationdomain.xml"
    INITIALS_XML = "/templates/gencase/simulationdomain.xml"
    FLOATINGS_XML = "/templates/gencase/floatings/base.xml"
    FLOATINGS_EACH_XML = "/templates/gencase/floatings/each/base.xml"
    FLOATINGS_CENTER_XML = "/templates/gencase/floatings/each/center.xml"
    FLOATINGS_INERTIA_XML = "/templates/gencase/floatings/each/inertia.xml"
    FLOATINGS_LINEARVELINI_XML = "/templates/gencase/floatings/each/linearvleini.xml"
    FLOATINGS_ANGULARVELINI_XML = "/templates/gencase/floatings/each/angularvelini.xml"
    FLOATINGS_ROTATION_XML = "/templates/gencase/floatings/each/rotation.xml"
    FLOATINGS_TRANSLATION_XML = "/templates/gencase/floatings/each/translation.xml"
    FLOATINGS_MATERIAL_XML = "/templates/gencase/floatings/each/material.xml"
    GENCASE_XML_SUFFIX = "_Def.xml"

    def __init__(self):
        self.mod_folder = os.path.dirname(os.path.realpath(__file__))

    def get_template_text(self, template_path) -> str:
        """ Returns the text for a given template. """
        template_data = ""
        with open("{}{}".format(self.mod_folder, template_path), "r") as template:
            template_data = template.read()
        return template_data

    def transform_bools_to_strs(self, value):
        """"Transforms a boolean value to a string representing its state, understandable by GenCase. """
        if isinstance(value, bool):
            return "true" if value else "false"
        if isinstance(value, dict):
            return {k: self.transform_bools_to_strs(v) for k, v in value.items()}
        return value

    def get_definition_template(self, data) -> str:
        """ Renders the <definition> part for the GenCase XML. """
        template = self.get_template_text(self.DEFINITION_XML)
        fc_object = FreeCAD.ActiveDocument.getObject("Case_Limits")
        min_point = fc_object.Placement.Base
        formatter = {
            "dp": data["dp"],
            "pointmin": [min_point.x / DIVIDER, min_point.y / DIVIDER, min_point.z / DIVIDER],
            "pointmax": [
                min_point.x / DIVIDER + fc_object.Length.Value / DIVIDER,
                min_point.y / DIVIDER + fc_object.Width.Value / DIVIDER if data["mode3d"] else min_point.y / DIVIDER,
                min_point.z / DIVIDER + fc_object.Height.Value / DIVIDER
            ]
        }
        return template.format(**formatter)

    def get_simulationdomain_template(self, data) -> str:
        """ Renders the <simulationdomain> part for the GenCase XML. """
        if data["domain"]["enabled"].lower() == "false":
            return ""
        template = self.get_template_text(self.SIMULATIONDOMAIN_XML)
        formatter = {}
        for key in ["posmin_x", "posmin_y", "posmin_z", "posmax_x", "posmax_y", "posmax_z"]:
            value = data["domain"][key]["value"]
            symbol = "+" if value >= 0 else "-"
            modes = {
                0: "default",
                1: str(value),
                2: "default{}{}".format(symbol, str(abs(value))),
                3: "default{}{}%".format(symbol, str(abs(value)))
            }
            formatter[key] = modes[data["domain"][key]["type"]]
        return template.format(**formatter)

    def get_initials_template(self, data) -> str:
        """ Renders the <initials> part for the GenCase XML. """
        template = self.get_template_text(self.INITIALS_XML)
        initials = map(lambda y: template.format(**y["mkbasedproperties"]["initials"]), filter(lambda x: x["initials"] is not None, data["mkbasedproperties"].values()))
        return LINE_END.join(initials) if initials else ""

    def get_floatings_template(self, data) -> str:
        """ Renders the <floatings> part of the GenCase XML. """
        float_properties = list(filter(lambda x: x["float_property"] is not None, data["mkbasedproperties"].values()))
        if not float_properties:
            return ""
        float_properties_xmls = []
        for fp in float_properties:
            float_property_attributes = []
            class_attributes = {
                self.FLOATINGS_CENTER_XML: "gravity_center",
                self.FLOATINGS_INERTIA_XML: "inertia",
                self.FLOATINGS_LINEARVELINI_XML: "initial_linear_velocity",
                self.FLOATINGS_ANGULARVELINI_XML: "initial_angular_velocity",
                self.FLOATINGS_TRANSLATION_XML: "translation_restriction",
                self.FLOATINGS_ROTATION_XML: "rotation_restriction",
                self.FLOATINGS_MATERIAL_XML: "material"
            }
            for xml, attr in class_attributes.items():
                if fp[attr] is not None:
                    if isinstance(fp[attr], list):
                        float_property_attributes.append(self.get_template_text(xml).format(*fp[attr]))
                    else:
                        float_property_attributes.append(self.get_template_text(xml).format(**{attr: fp[attr]}))

            formatter = {
                "floating_mk": fp["mk"],
                "floating_density_type": {FloatingDensityType.MASSBODY: "massbody", FloatingDensityType.RHOPBODY: "rhopbody"}[fp["mass_density_type"]],
                "floating_density_value": fp["mass_density_value"],
                "float_property_attributes": float_property_attributes
            }
            float_properties_xmls.append(self.get_template_text(self.FLOATINGS_EACH_XML).format(**formatter))

        formatter = {"floatings_each": LINE_END.join(float_properties_xmls) if float_properties_xmls else ""}
        return self.get_template_text(self.FLOATINGS_XML).format(**formatter)

    def get_adapted_case_data(self, case: "Case") -> dict:
        """ Adapts the case data to a dictionary used to format the resulting XML """
        data: dict = obj_to_dict(case)
        data = self.transform_bools_to_strs(data)

        data["definition_template"] = self.get_definition_template(data)
        data["simulationdomain_template"] = self.get_simulationdomain_template(data)
        data["initials_template"] = self.get_initials_template(data)
        data["floatings_template"] = self.get_floatings_template(data)
        data["application"] = APP_NAME
        data["current_date"] = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
        return data

    def generate(self, case) -> str:
        """ Returns the GenCase-compatible XML resulting from the case """
        return self.get_template_text(self.BASE_XML).format(**self.get_adapted_case_data(case))

    def save_to_disk(self, path, case: "Case") -> None:
        """ Creates a file on disk with the contents of the GenCase generated XML. """
        with open("{}/{}{}".format(path, case.name, self.GENCASE_XML_SUFFIX), "w", encoding="utf-8") as file:
            file.write(self.generate(case))
