# -*- coding: utf-8 -*-
""" Initials template renderer.

Renders the <initials> tag of the GenCase XML.
"""

from mod.template_tools import get_template_text

from mod.enums import InitialsType
from mod.enums import BoundInitialsType
from mod.constants import LINE_END


class InitialsRenderer():
    """ Renders the <initials> tag of the GenCase XML. """

    BASE_XML = "/templates/gencase/initials/base.xml"
    UNIFORM_XML = "/templates/gencase/initials/uniform.xml"
    LINEAR_XML = "/templates/gencase/initials/linear.xml"
    PARABOLIC_XML = "/templates/gencase/initials/parabolic.xml"

    SET_XML = "/templates/gencase/initials/boundnormal_set.xml"
    PLANE_XML = "/templates/gencase/initials/boundnormal_plane.xml"
    PLANE_POINT_XML = "/templates/gencase/initials/boundnormal_plane_point.xml"
    PLANE_POINT_AUTO_XML = "/templates/gencase/initials/boundnormal_plane_point_auto.xml"
    SPHERE_XML = "/templates/gencase/initials/boundnormal_sphere.xml"
    CYLINDER_XML = "/templates/gencase/initials/boundnormal_cylinder.xml"
    PARTS_XML = "/templates/gencase/initials/boundnormal_parts.xml"

    @classmethod
    def render(cls, data):
        """ Returns the rendered string. """

        for x in data["mkbasedproperties"].values():
            if not "bound_initials" in x:
                x["bound_initials"] = None

        suitable_mkbasedproperties = filter(lambda x: x["initials"] is not None or x["bound_initials"] is not None, data["mkbasedproperties"].values())

        if not suitable_mkbasedproperties:
            return ""

        initials_templates = list()
        for mkbasedproperty in suitable_mkbasedproperties:
            initials = mkbasedproperty["initials"]
            if initials is not None:
                if initials["initials_type"] == InitialsType.UNIFORM:
                    initials_templates.append(get_template_text(cls.UNIFORM_XML).format(**initials))
                elif initials["initials_type"] == InitialsType.LINEAR:
                    initials_templates.append(get_template_text(cls.LINEAR_XML).format(**initials))
                elif initials["initials_type"] == InitialsType.PARABOLIC:
                    initials_templates.append(get_template_text(cls.PARABOLIC_XML).format(**initials))

            bound_initials = mkbasedproperty["bound_initials"]
            if bound_initials is not None:
                if bound_initials["initials_type"] == BoundInitialsType.SET:
                    initials_templates.append(get_template_text(cls.SET_XML).format(**bound_initials))
                elif bound_initials["initials_type"] == BoundInitialsType.PLANE:
                    bound_plane_key="bound_normal_point_template"
                    if  bound_initials["point_auto"] == "true":
                        bound_initials[bound_plane_key] = get_template_text(cls.PLANE_POINT_AUTO_XML).format(**bound_initials)
                        #initials_templates.append(get_template_text(cls.PLANE_XML).format(**formatter))
                        #plane_point_auto_tmp = get_template_text(cls.PLANE_POINT_AUTO_XML)
                        #plane_xml_tmp=plane_xml_tmp.format(bound_normal_point_template=plane_point_auto_tmp)
                    else:
                        bound_initials[bound_plane_key] = get_template_text(cls.PLANE_POINT_XML).format(**bound_initials)
                        #initials_templates.append(get_template_text(cls.PLANE_XML).format(**formatter))
                        #plane_point_auto_tmp = get_template_text(cls.PLANE_POINT_AUTO_XML)
                        #plane_xml_tmp=plane_xml_tmp.format(bound_normal_point_template=plane_point_auto_tmp)
                    #initials_templates.append(plane_xml_tmp.format(**bound_initials))
                    initials_templates.append(get_template_text(cls.PLANE_XML).format(**bound_initials))
                elif bound_initials["initials_type"] == BoundInitialsType.SPHERE:
                    initials_templates.append(get_template_text(cls.SPHERE_XML).format(**bound_initials))
                elif bound_initials["initials_type"] == BoundInitialsType.CYLINDER:
                    initials_templates.append(get_template_text(cls.CYLINDER_XML).format(**bound_initials))
                elif bound_initials["initials_type"] == BoundInitialsType.PARTS:
                    initials_templates.append(get_template_text(cls.PARTS_XML).format(**bound_initials))

        return get_template_text(cls.BASE_XML).format(initials_each=LINE_END.join(initials_templates))
