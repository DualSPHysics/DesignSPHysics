# -*- coding: utf-8 -*-
""" Definition template renderer.

Renders the <mainlist> tag of the GenCase XML.
"""
import math

import FreeCAD

from mod.enums import FreeCADObjectType, ObjectType
from mod.constants import DIVIDER, SUPPORTED_TYPES, LINE_END

from mod.template_tools import get_template_text


class ObjectsRenderer():
    """ Renders the <mainlist> tag of the GenCase XML. """

    OBJECTS_XML = "/templates/gencase/objects/base.xml"
    OBJECTS_MKFLUID_XML = "/templates/gencase/objects/each/mkfluid.xml"
    OBJECTS_MKBOUND_XML = "/templates/gencase/objects/each/mkbound.xml"
    OBJECTS_ROTATION_XML = "/templates/gencase/objects/each/rotation.xml"
    OBJECT_FRDRAWMODE_ENABLE = "/templates/gencase/objects/each/frdrawmode_enable.xml"
    OBJECT_FRDRAWMODE_DISABLE = "/templates/gencase/objects/each/frdrawmode_disable.xml"
    OBJECTS_MATRIXRESET_XML = "/templates/gencase/objects/each/matrixreset.xml"
    OBJECTS_MOVE_XML = "/templates/gencase/objects/each/move.xml"
    OBJECT_BOX_XML = "/templates/gencase/objects/each/cube.xml"
    OBJECT_SPHERE_XML = "/templates/gencase/objects/each/sphere.xml"
    OBJECT_CYLINDER_XML = "/templates/gencase/objects/each/cylinder.xml"
    OBJECT_FILLBOX_XML = "/templates/gencase/objects/each/fillbox.xml"
    OBJECT_COMPLEX_XML = "/templates/gencase/objects/each/complex.xml"

    @classmethod
    def get_regular_objects_template(cls, obj, fc_object) -> str:
        ''' Builds a template for basic object types, like boxes or spheres. '''

        template = {
            FreeCADObjectType.BOX: cls.OBJECT_BOX_XML,
            FreeCADObjectType.SPHERE: cls.OBJECT_SPHERE_XML,
            FreeCADObjectType.CYLINDER: cls.OBJECT_CYLINDER_XML
        }[fc_object.TypeId]

        # Formatting general keys
        obj_formatter = {
            "label": fc_object.Label,
            "obj": obj,
            "pos": [fc_object.Placement.Base.x / DIVIDER, fc_object.Placement.Base.y / DIVIDER, fc_object.Placement.Base.z / DIVIDER] if not fc_object.Placement.Rotation.Angle else [0, 0, 0],
            "mktype_template": (get_template_text(cls.OBJECTS_MKBOUND_XML) if obj["type"] == ObjectType.BOUND else get_template_text(cls.OBJECTS_MKFLUID_XML)).format(**obj),
            "move_template": get_template_text(cls.OBJECTS_MOVE_XML).format(**{
                "vec": [fc_object.Placement.Base.x / DIVIDER, fc_object.Placement.Base.y / DIVIDER, fc_object.Placement.Base.z / DIVIDER]
            }) if fc_object.Placement.Rotation.Angle else "",
            "rotation_template": get_template_text(cls.OBJECTS_ROTATION_XML).format(**{
                "ang": math.degrees(fc_object.Placement.Rotation.Angle),
                "vec": [-fc_object.Placement.Rotation.Axis.x, -fc_object.Placement.Rotation.Axis.y, -fc_object.Placement.Rotation.Axis.z]
            }) if fc_object.Placement.Rotation.Angle else "",
            "frdrawmode_template_enable": get_template_text(cls.OBJECT_FRDRAWMODE_ENABLE) if fc_object.TypeId in (FreeCADObjectType.BOX, FreeCADObjectType.CYLINDER, FreeCADObjectType.SPHERE) and "frdrawmode" in obj.keys() and obj["frdrawmode"] == "true" else "",
            "frdrawmode_template_disable": get_template_text(cls.OBJECT_FRDRAWMODE_DISABLE) if fc_object.TypeId in (FreeCADObjectType.BOX, FreeCADObjectType.CYLINDER, FreeCADObjectType.SPHERE) and "frdrawmode" in obj.keys() and obj["frdrawmode"] == "true" else "",
        }

        # Decide if reset matrix or not
        obj_formatter.update({
            "matrixreset_template": get_template_text(cls.OBJECTS_MATRIXRESET_XML) if obj_formatter["move_template"] or obj_formatter["rotation_template"] else ""
        })

        # Formatting specific keys for each type of object
        if fc_object.TypeId == FreeCADObjectType.BOX:
            obj_formatter.update({
                "boxfill": obj["faces_configuration"]["face_print"] if obj["faces_configuration"] else "solid",
                "layers": '\t\t\t\t\t<layers vdp="{}" />'.format(obj["faces_configuration"]["layers"]) if obj["faces_configuration"] and obj["faces_configuration"]["layers"] != "" else "",
                "size": [fc_object.Length.Value / DIVIDER, fc_object.Width.Value / DIVIDER, fc_object.Height.Value / DIVIDER],
            })
        if fc_object.TypeId == FreeCADObjectType.SPHERE:
            obj_formatter.update({
                "radius": fc_object.Radius.Value / DIVIDER,
            })
        if fc_object.TypeId == FreeCADObjectType.CYLINDER:
            obj_formatter.update({
                "radius": fc_object.Radius.Value / DIVIDER,
                "z2": (fc_object.Height.Value / DIVIDER) + (fc_object.Placement.Base.z / DIVIDER)
            })

        return get_template_text(template).format(**obj_formatter)

    @classmethod
    def get_fillbox_object_template(cls, obj, fc_object) -> str:
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
            "mktype_template": (get_template_text(cls.OBJECTS_MKBOUND_XML) if obj["type"] == ObjectType.BOUND else get_template_text(cls.OBJECTS_MKFLUID_XML)).format(**obj),
            "move_template": get_template_text(cls.OBJECTS_MOVE_XML).format(**{
                "vec": [fill_limits.Placement.Base.x / DIVIDER, fill_limits.Placement.Base.y / DIVIDER, fill_limits.Placement.Base.z / DIVIDER]
            }) if fill_limits.Placement.Base.Length else "",
            "rotation_template": get_template_text(cls.OBJECTS_ROTATION_XML).format(**{
                "ang": math.degrees(fill_limits.Placement.Rotation.Angle),
                "vec": [-fill_limits.Placement.Rotation.Axis.x, -fill_limits.Placement.Rotation.Axis.y, -fill_limits.Placement.Rotation.Axis.z]
            }) if fill_limits.Placement.Rotation.Angle else "",
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

        # Decide if reset matrix or not
        formatter.update({
            "matrixreset_template": get_template_text(cls.OBJECTS_MATRIXRESET_XML) if formatter["move_template"] or formatter["rotation_template"] else ""
        })

        return get_template_text(cls.OBJECT_FILLBOX_XML).format(**formatter)

    @classmethod
    def get_complex_object_template(cls, obj, fc_object) -> str:
        ''' Builds a template for complex objects. '''
        formatter = {
            "label": fc_object.Label,
            "mktype_template": (get_template_text(cls.OBJECTS_MKBOUND_XML) if obj["type"] == ObjectType.BOUND else get_template_text(cls.OBJECTS_MKFLUID_XML)).format(**obj),
            "file": "{}.stl".format(fc_object.Name),
            "autofill": "true" if obj["autofill"] == "true" else "false"
        }

        return get_template_text(cls.OBJECT_COMPLEX_XML).format(**formatter)

    @classmethod
    def render(cls, data):
        """ Returns the rendered string. """
        template = get_template_text(cls.OBJECTS_XML)
        object_xmls = []
        for obj in data["objects"]:
            if obj["type"] == ObjectType.SPECIAL:
                continue
            fc_object = FreeCAD.ActiveDocument.getObject(obj["name"])

            if fc_object.TypeId in SUPPORTED_TYPES:
                object_template: str = cls.get_regular_objects_template(obj, fc_object)
            elif "FillBox" in fc_object.Name:
                object_template: str = cls.get_fillbox_object_template(obj, fc_object)
            else:
                # Assuming this is a complex object that needs STL exporting.
                object_template: str = cls.get_complex_object_template(obj, fc_object)

            object_xmls.append(object_template)

        formatter = {"objects_each": LINE_END.join(object_xmls) if object_xmls else ""}
        return template.format(**formatter)
