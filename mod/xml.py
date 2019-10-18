# -*- coding: utf-8 -*-
"""XML Exporter for DesignSPHysics

The utilities on this module creates

"""

import os
import math
from datetime import datetime

import FreeCAD

from mod.constants import APP_NAME, DIVIDER, LINE_END, SUPPORTED_TYPES
from mod.enums import FloatingDensityType, FreeCADObjectType, ObjectType, MLPistonType
from mod.template_tools import obj_to_dict
from mod.stdout_tools import debug


class XMLExporter():
    """ Handles XML generation and data transformation to adapt to DualSPHysics
    preprocessing tools """

    BASE_XML = "/templates/gencase/base.xml"
    DEFINITION_XML = "/templates/gencase/definition.xml"
    OBJECTS_XML = "/templates/gencase/objects/base.xml"
    OBJECTS_MKFLUID_XML = "/templates/gencase/objects/each/mkfluid.xml"
    OBJECTS_MKBOUND_XML = "/templates/gencase/objects/each/mkbound.xml"
    OBJECTS_ROTATION_XML = "/templates/gencase/objects/each/rotation.xml"
    OBJECTS_MATRIXRESET_XML = "/templates/gencase/objects/each/matrixreset.xml"
    OBJECTS_MOVE_XML = "/templates/gencase/objects/each/move.xml"
    OBJECT_BOX_XML = "/templates/gencase/objects/each/cube.xml"
    OBJECT_SPHERE_XML = "/templates/gencase/objects/each/sphere.xml"
    OBJECT_CYLINDER_XML = "/templates/gencase/objects/each/cylinder.xml"
    OBJECT_FILLBOX_XML = "/templates/gencase/objects/each/fillbox.xml"
    OBJECT_COMPLEX_XML = "/templates/gencase/objects/each/complex.xml"
    SIMULATIONDOMAIN_XML = "/templates/gencase/simulationdomain.xml"
    INITIALS_XML = "/templates/gencase/simulationdomain.xml"
    RZONES_XML = "/templates/gencase/rzones/base.xml"
    RZONE_REGULAR_XML = "/templates/gencase/rzones/regular.xml"
    RZONE_IRREGULAR_XML = "/templates/gencase/rzones/irregular.xml"
    RZONE_FILE_XML = "/templates/gencase/rzones/file.xml"
    RZONE_UNIFORM_XML = "/templates/gencase/rzones/uniform.xml"
    RZONE_UNIFORM_VELOCITY_XML = "/templates/gencase/rzones/uniform_velocity.xml"
    RZONE_UNIFORM_VELOCITYTIMES_XML = "/templates/gencase/rzones/uniform_velocitytimes.xml"
    RZONE_UNIFORM_VELOCITYTIMES_EACH_XML = "/templates/gencase/rzones/uniform_velocitytimes_each.xml"
    DAMPING_BASE = "/templates/gencase/damping/base.xml"
    DAMPING_EACH = "/templates/gencase/damping/each.xml"
    MLPISTONS_BASE = "/templates/gencase/mlpistons/base.xml"
    MLPISTONS_EACH_1D = "/templates/gencase/mlpistons/each_1d.xml"
    MLPISTONS_EACH_2D = "/templates/gencase/mlpistons/each_2d.xml"
    MLPISTONS_EACH_2D_VELDATA = "/templates/gencase/mlpistons/each_veldata.xml"
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

    def get_regular_objects_template(self, obj, fc_object) -> str:
        ''' Builds a template for basic object types, like boxes or spheres. '''

        template = {
            FreeCADObjectType.BOX: self.OBJECT_BOX_XML,
            FreeCADObjectType.SPHERE: self.OBJECT_SPHERE_XML,
            FreeCADObjectType.CYLINDER: self.OBJECT_CYLINDER_XML
        }[fc_object.TypeId]

        # Formatting general keys
        obj_formatter = {
            "label": fc_object.Label,
            "obj": obj,
            "pos": [fc_object.Placement.Base.x / DIVIDER, fc_object.Placement.Base.y / DIVIDER, fc_object.Placement.Base.z / DIVIDER] if not fc_object.Placement.Rotation.Angle else [0, 0, 0],
            "mktype_template": (self.get_template_text(self.OBJECTS_MKBOUND_XML) if obj["type"] == ObjectType.BOUND else self.get_template_text(self.OBJECTS_MKFLUID_XML)).format(**obj),
            "move_template": self.get_template_text(self.OBJECTS_MOVE_XML).format(**{
                "vec": [fc_object.Placement.Base.x / DIVIDER, fc_object.Placement.Base.y / DIVIDER, fc_object.Placement.Base.z / DIVIDER]
            }) if fc_object.Placement.Rotation.Angle else "",
            "rotation_template": self.get_template_text(self.OBJECTS_ROTATION_XML).format(**{
                "ang": math.degrees(fc_object.Placement.Rotation.Angle),
                "vec": [-fc_object.Placement.Rotation.Axis.x, -fc_object.Placement.Rotation.Axis.y, -fc_object.Placement.Rotation.Axis.z]
            }) if fc_object.Placement.Rotation.Angle else "",
            "matrixreset_template": self.get_template_text(self.OBJECTS_MATRIXRESET_XML) if fc_object.Placement.Rotation.Angle else ""
        }

        # Formatting specific keys for each type of object
        if fc_object.TypeId == FreeCADObjectType.BOX:
            obj_formatter.update({
                "boxfill": obj["faces_configuration"]["faces_print"] if obj["faces_configuration"] else "solid",
                "size": [fc_object.Length.Value / DIVIDER, fc_object.Width.Value / DIVIDER, fc_object.Height.Value / DIVIDER],
            })
        if fc_object.TypeId == FreeCADObjectType.SPHERE:
            obj_formatter.update({
                "radius": fc_object.Radius.Value / DIVIDER,
            })
        if fc_object.TypeId == FreeCADObjectType.CYLINDER:
            obj_formatter.update({
                "radius": fc_object.Radius.Value / DIVIDER,
                "height": fc_object.Height.Value / DIVIDER
            })

        return self.get_template_text(template).format(**obj_formatter)

    def get_fillbox_object_template(self, obj, fc_object) -> str:
        ''' Builds a template for fillbox objects. '''
        fill_limits, fill_point = None, None
        for element in fc_object.OutList:
            if "FillLimit" in element.Name:
                fill_limits = element
            if "FillPoint" in element.Name:
                fill_point = element
        if not fill_limits or not fill_point:
            raise RuntimeError("Could not find fill limit and fill point inside a fillbox")

        formatter = {
            "label": fc_object.Label,
            "mktype_template": (self.get_template_text(self.OBJECTS_MKBOUND_XML) if obj["type"] == ObjectType.BOUND else self.get_template_text(self.OBJECTS_MKFLUID_XML)).format(**obj),
            "move_template": self.get_template_text(self.OBJECTS_MOVE_XML).format(**{
                "vec": [fill_limits.Placement.Base.x / DIVIDER, fill_limits.Placement.Base.y / DIVIDER, fill_limits.Placement.Base.z / DIVIDER]
            }) if fill_limits.Placement.Base.Length else "",
            "rotation_template": self.get_template_text(self.OBJECTS_ROTATION_XML).format(**{
                "ang": math.degrees(fill_limits.Placement.Rotation.Angle),
                "vec": [-fill_limits.Placement.Rotation.Axis.x, -fill_limits.Placement.Rotation.Axis.y, -fill_limits.Placement.Rotation.Axis.z]
            }) if fill_limits.Placement.Rotation.Angle else "",
            "matrixreset_template": self.get_template_text(self.OBJECTS_MATRIXRESET_XML) if fill_limits.Placement.Rotation.Angle else "",
            "pos": [
                (fill_point.Placement.Base.x - fill_limits.Placement.Base.x) / DIVIDER,
                (fill_point.Placement.Base.y - fill_limits.Placement.Base.y) / DIVIDER,
                (fill_point.Placement.Base.z - fill_limits.Placement.Base.z) / DIVIDER
            ],
            "size": [
                fill_limits.Length.Value / DIVIDER,
                fill_limits.Width.Value / DIVIDER,
                fill_limits.Height.Value / DIVIDER,
            ]
        }

        return self.get_template_text(self.OBJECT_FILLBOX_XML).format(**formatter)

    def get_complex_object_template(self, obj, fc_object) -> str:
        ''' Builds a template for complex objects. '''
        formatter = {
            "label": fc_object.Label,
            "mktype_template": (self.get_template_text(self.OBJECTS_MKBOUND_XML) if obj["type"] == ObjectType.BOUND else self.get_template_text(self.OBJECTS_MKFLUID_XML)).format(**obj),
            "file": "{}.stl".format(fc_object.Name),
            "autofill": "true" if obj["autofill"] else "false"
        }

        return self.get_template_text(self.OBJECT_COMPLEX_XML).format(**formatter)

    def get_objects_template(self, data) -> str:
        """ Renders the <mainlist> part for the GenCase XML. """
        template = self.get_template_text(self.OBJECTS_XML)
        object_xmls = []
        for obj in data["objects"]:
            if obj["type"] == ObjectType.SPECIAL:
                continue
            fc_object = FreeCAD.ActiveDocument.getObject(obj["name"])

            if fc_object.TypeId in SUPPORTED_TYPES:
                object_template: str = self.get_regular_objects_template(obj, fc_object)
            elif "FillBox" in fc_object.Name:
                object_template: str = self.get_fillbox_object_template(obj, fc_object)
            else:
                # Assuming this is a complex object that needs STL exporting.
                object_template: str = self.get_complex_object_template(obj, fc_object)

            object_xmls.append(object_template)

        formatter = {"objects_each": LINE_END.join(object_xmls) if object_xmls else ""}
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

    def get_velocity_times_template(self, times: list) -> str:
        """ Renders the velocity times template for a uniform relaxation zone. """
        timevalues = LINE_END.join(map(lambda tv: self.get_template_text(self.RZONE_UNIFORM_VELOCITYTIMES_EACH_XML).format(tv[0], tv[1]), times))
        return self.get_template_text(self.RZONE_UNIFORM_VELOCITYTIMES_XML).format(each=timevalues)

    def get_rzones_template(self, data, rz_type) -> str:
        """ Renders the <relaxationzones> part for the GenCase XML. """
        template = self.get_template_text(self.RZONES_XML)
        rz_templates = {
            "RelaxationZoneRegular": self.RZONE_REGULAR_XML,
            "RelaxationZoneIrregular": self.RZONE_IRREGULAR_XML,
            "RelaxationZoneFile": self.RZONE_FILE_XML,
            "RelaxationZoneUniform": self.RZONE_UNIFORM_XML
        }
        rzone_formatter = {}

        if rz_type == "RelaxationZoneUniform":
            if data["relaxation_zone"]["use_velocity"] == "true":
                rzone_formatter["rzuniform_velocity"] = self.get_template_text(self.RZONE_UNIFORM_VELOCITY_XML).format(data["relaxation_zone"]["velocity"])
            else:
                rzone_formatter["rzuniform_velocity"] = self.get_velocity_times_template(data["relaxation_zone"]["velocity_times"])

        rzone_formatter.update(data["relaxation_zone"])
        formatter = {
            "rzone": self.get_template_text(rz_templates[rz_type]).format(**rzone_formatter)
        }
        return template.format(**formatter)

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

    def get_damping_template(self, data) -> str:
        """ Renders the <damping> part of the GenCase XML. """
        each_damping_template: list = []

        for obj_name, dzone in data["damping_zones"].items():
            fc_object = FreeCAD.ActiveDocument.getObject(obj_name)
            dzone.update({
                "limitmin": [
                    fc_object.OutList[0].Start[0] / DIVIDER,
                    fc_object.OutList[0].Start[1] / DIVIDER,
                    fc_object.OutList[0].Start[2] / DIVIDER
                ],
                "limitmax": [
                    str(fc_object.OutList[0].End[0] / DIVIDER),
                    str(fc_object.OutList[0].End[1] / DIVIDER),
                    str(fc_object.OutList[0].End[2] / DIVIDER)
                ]
            })
            each_damping_template.append(self.get_template_text(self.DAMPING_EACH).format(**dzone))

        formatter = {
            "each": LINE_END.join(each_damping_template)
        }

        return self.get_template_text(self.DAMPING_BASE).format(**formatter)

    def get_mlpistons_template(self, data) -> str:
        """ Renders the <mlayerpistons> part of the GenCase XML. """
        ml_pistons: dict = dict()
        for mk, mk_prop in data["mkbasedproperties"].items():
            if mk_prop["mlayerpiston"]:
                ml_pistons[mk] = mk_prop["mlayerpiston"]

        if not ml_pistons.values():
            return ""

        each_mlpiston_template: list = list()
        for mk, mlpiston in ml_pistons.items():
            if mlpiston["type"] == MLPistonType.MLPISTON1D:
                mlpiston.update({"mk": mk})
                each_mlpiston_template.append(self.get_template_text(self.MLPISTONS_EACH_1D).format(**mlpiston))
            elif mlpiston["type"] == MLPistonType.MLPISTON2D:
                each_veldata_templates: list = list()
                for veldata in mlpiston["veldata"]:
                    each_veldata_templates.append(self.get_template_text(self.MLPISTONS_EACH_2D_VELDATA).format(**veldata))
                mlpiston.update({
                    "mk": mk,
                    "each_veldata": LINE_END.join(each_veldata_templates)
                })
                each_mlpiston_template.append(self.get_template_text(self.MLPISTONS_EACH_2D).format(**mlpiston))

        formatter = {
            "each": LINE_END.join(each_mlpiston_template)
        }

        return self.get_template_text(self.MLPISTONS_BASE).format(**formatter)

    def get_adapted_case_data(self, case: "Case") -> dict:
        """ Adapts the case data to a dictionary used to format the resulting XML """
        data: dict = obj_to_dict(case)
        data = self.transform_bools_to_strs(data)

        data["definition_template"] = self.get_definition_template(data)
        data["objects_template"] = self.get_objects_template(data)
        data["simulationdomain_template"] = self.get_simulationdomain_template(data)
        data["initials_template"] = self.get_initials_template(data)
        data["floatings_template"] = self.get_floatings_template(data)
        data["rzones_template"] = self.get_rzones_template(data, type(case.relaxation_zone).__name__) if case.relaxation_zone else ""
        data["damping_template"] = self.get_damping_template(data) if case.damping_zones.keys() else ""
        data["mlpistons_template"] = self.get_mlpistons_template(data)
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
