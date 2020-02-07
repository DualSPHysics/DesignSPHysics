# -*- coding: utf-8 -*-
""" Floatings template renderer.

Renders the <floatings> tag of the GenCase XML.
"""

from mod.template_tools import get_template_text

from mod.enums import FloatingDensityType
from mod.constants import LINE_END


class FloatingsRenderer():
    """ Renders the <floatings> tag of the GenCase XML. """

    FLOATINGS_XML = "/templates/gencase/floatings/base.xml"
    FLOATINGS_EACH_XML = "/templates/gencase/floatings/each/base.xml"
    FLOATINGS_CENTER_XML = "/templates/gencase/floatings/each/center.xml"
    FLOATINGS_INERTIA_XML = "/templates/gencase/floatings/each/inertia.xml"
    FLOATINGS_LINEARVELINI_XML = "/templates/gencase/floatings/each/linearvelini.xml"
    FLOATINGS_ANGULARVELINI_XML = "/templates/gencase/floatings/each/angularvelini.xml"
    FLOATINGS_ROTATION_XML = "/templates/gencase/floatings/each/rotation.xml"
    FLOATINGS_TRANSLATION_XML = "/templates/gencase/floatings/each/translation.xml"
    FLOATINGS_MATERIAL_XML = "/templates/gencase/floatings/each/material.xml"
    FLOATINGS_MASSBODY_XML = "/templates/gencase/floatings/each/massbody_prop.xml"
    FLOATINGS_RHOPBODY_XML = "/templates/gencase/floatings/each/rhopbody_attr.xml"

    @classmethod
    def render(cls, data):
        """ Returns the rendered string. """
        float_properties = list(map(lambda x: x["float_property"], filter(lambda x: x["float_property"] is not None, data["mkbasedproperties"].values())))
        if not float_properties:
            return ""
        float_properties_xmls = []
        for fp in float_properties:
            float_property_attributes = []
            class_attributes = {
                cls.FLOATINGS_CENTER_XML: "gravity_center",
                cls.FLOATINGS_INERTIA_XML: "inertia",
                cls.FLOATINGS_LINEARVELINI_XML: "initial_linear_velocity",
                cls.FLOATINGS_ANGULARVELINI_XML: "initial_angular_velocity",
                cls.FLOATINGS_TRANSLATION_XML: "translation_restriction",
                cls.FLOATINGS_ROTATION_XML: "rotation_restriction",
                cls.FLOATINGS_MATERIAL_XML: "material"
            }
            for xml, attr in class_attributes.items():
                if fp[attr]:
                    if isinstance(fp[attr], list):
                        float_property_attributes.append(get_template_text(xml).format(*fp[attr]))
                    else:
                        float_property_attributes.append(get_template_text(xml).format(**{attr: fp[attr]}))

            formatter = {
                "floating_mk": fp["mk"],
                "rhopbody": "",
                "massbody": "",
                "float_property_attributes": LINE_END.join(float_property_attributes)
            }

            if fp["mass_density_type"] == FloatingDensityType.MASSBODY:
                formatter["massbody"] = get_template_text(cls.FLOATINGS_MASSBODY_XML).format(floating_density_value=fp["mass_density_value"])
            elif fp["mass_density_type"] == FloatingDensityType.RHOPBODY:
                formatter["rhopbody"] = get_template_text(cls.FLOATINGS_RHOPBODY_XML).format(floating_density_value=fp["mass_density_value"])

            float_properties_xmls.append(get_template_text(cls.FLOATINGS_EACH_XML).format(**formatter))

        formatter = {"floatings_each": LINE_END.join(float_properties_xmls) if float_properties_xmls else ""}
        return get_template_text(cls.FLOATINGS_XML).format(**formatter)
