# -*- coding: utf-8 -*-
""" Inout template renderer.

Renders the <chrono> tag of the GenCase XML.
"""

from mod.template_tools import get_template_text

from mod.constants import LINE_END


class ChronoRenderer():
    """ Renders the <chrono> tag of the GenCase XML. """

    CHRONO_BASE = "/templates/gencase/chrono/base.xml"
    COLLISIONDP_ACTIVE = "/templates/gencase/chrono/collisiondp_active.xml"
    COLLISIONDP_INACTIVE = "/templates/gencase/chrono/collisiondp_inactive.xml"
    SAVEDATA = "/templates/gencase/chrono/savedata.xml"
    SCHEMESCALE = "/templates/gencase/chrono/schemescale.xml"
    OBJECTS_BASE = "/templates/gencase/chrono/objects/base.xml"
    OBJECTS_MODELNORMAL_FRAGMENT = "/templates/gencase/chrono/objects/modelnormal_template.xml"
    HINGE_BASE = "/templates/gencase/chrono/links/hinge/base.xml"
    LINEARSPRING_BASE = "/templates/gencase/chrono/links/linearspring/base.xml"
    POINTLINE_BASE = "/templates/gencase/chrono/links/pointline/base.xml"
    COULOMBDAMPING_BASE = "/templates/gencase/chrono/links/coulombdamping/base.xml"
    PULLEY_BASE = "/templates/gencase/chrono/links/pulley/base.xml"
    SPHERIC_BASE = "/templates/gencase/chrono/links/spheric/base.xml"
    SPHERIC_IDBODY2 = "/templates/gencase/chrono/links/spheric/idbody2.xml"

    @classmethod
    def render(cls, data):
        """ Returns the rendered string. """
        if not data["chrono"]["objects"]:
            return ""

        formatter: dict = data["chrono"]
        formatter["savedata"] = cls.get_savedata_template(data["chrono"])
        formatter["schemescale"] = cls.get_schemescale_template(data["chrono"])
        formatter["collisiondp"] = cls.get_collisiondp_template(data["chrono"])
        formatter["objects_each"] = cls.get_objects_each_template(data["chrono"])
        formatter["linearspring_each"] = cls.get_linearspring_each_template(data["chrono"])
        formatter["hinge_each"] = cls.get_hinge_each_template(data["chrono"])
        formatter["spheric_each"] = cls.get_spheric_each_template(data["chrono"])
        formatter["pointline_each"] = cls.get_pointline_each_template(data["chrono"])
        formatter["coulombdamping_each"] = cls.get_coulombdamping_each_template(data["chrono"])
        formatter["pulley_each"] = cls.get_pulley_each_template(data["chrono"])

        return get_template_text(cls.CHRONO_BASE).format(**formatter)

    @classmethod
    def get_savedata_template(cls, chrono: dict) -> str:
        """ Renders the savedata part of the chrono template. """
        if chrono["csv_intervals"]["enabled"] == "true":
            return get_template_text(cls.SAVEDATA).format(**chrono["csv_intervals"])
        return ""

    @classmethod
    def get_schemescale_template(cls, chrono: dict) -> str:
        """ Renders the schemescale part of the chrono template. """
        if chrono["scale_scheme"]["enabled"] == "true":
            return get_template_text(cls.SCHEMESCALE).format(**chrono["scale_scheme"])
        return ""

    @classmethod
    def get_collisiondp_template(cls, chrono: dict) -> str:
        """ Renders the collisiondp part of the chrono template. """
        if chrono["collisiondp"]["enabled"] == "true":
            return get_template_text(cls.COLLISIONDP_ACTIVE).format(**chrono["collisiondp"])
        return get_template_text(cls.COLLISIONDP_INACTIVE)

    @classmethod
    def get_objects_each_template(cls, chrono: dict) -> str:
        """ Renders the bodyfixed/floating part of the chrono template. """
        object_each_template_list: list = list()

        for chrono_object in chrono["objects"]:
            formatter: dict = chrono_object
            formatter["modelnormal_template"] = cls.get_modelnormal_fragment(chrono_object)
            object_each_template_list.append(get_template_text(cls.OBJECTS_BASE).format(**formatter))

        return LINE_END.join(object_each_template_list)

    @classmethod
    def get_modelnormal_fragment(cls, chrono_object: dict) -> str:
        """ Returns the fragment for the attributes modelnormal and modelfile for an object """
        if chrono_object["modelnormal_enabled"] == "true":
            return get_template_text(cls.OBJECTS_MODELNORMAL_FRAGMENT).format(**chrono_object)
        return ""

    @classmethod
    def get_linearspring_each_template(cls, chrono: dict) -> str:
        """ Renders the link_linearspring part of the chrono template. """
        link_linearspring_each_templates: list = list()

        for link in chrono["link_linearspring"]:
            link_linearspring_each_templates.append(get_template_text(cls.LINEARSPRING_BASE).format(**link))

        return LINE_END.join(link_linearspring_each_templates)

    @classmethod
    def get_hinge_each_template(cls, chrono: dict) -> str:
        """ Renders the link_hinge part of the chrono template. """
        link_hinge_each_templates: list = list()

        for link in chrono["link_hinge"]:
            link_hinge_each_templates.append(get_template_text(cls.HINGE_BASE).format(**link))

        return LINE_END.join(link_hinge_each_templates)

    @classmethod
    def get_spheric_each_template(cls, chrono: dict) -> str:
        """ Renders the link_spheric part of the chrono template. """
        link_spheric_each_templates: list = list()

        for link in chrono["link_spheric"]:
            formatter: dict = link
            formatter["idbody2_template"] = cls.get_spheric_idbody2_fragment(link)
            link_spheric_each_templates.append(get_template_text(cls.SPHERIC_BASE).format(**link))

        return LINE_END.join(link_spheric_each_templates)

    @classmethod
    def get_spheric_idbody2_fragment(cls, link: dict) -> str:
        """ Renders the idbody2 fragment for the link_spheric tag. """
        if link["idbody2"]:
            return get_template_text(cls.SPHERIC_IDBODY2).format(**link)
        return ""

    @classmethod
    def get_pointline_each_template(cls, chrono: dict) -> str:
        """ Renders the link_pointline part of the chrono template. """
        link_pointline_each_templates: list = list()

        for link in chrono["link_pointline"]:
            link_pointline_each_templates.append(get_template_text(cls.POINTLINE_BASE).format(**link))

        return LINE_END.join(link_pointline_each_templates)

    @classmethod
    def get_coulombdamping_each_template(cls, chrono: dict) -> str:
        """ Renders the link_coulombdamping part of the chrono template. """
        link_coulombdamping_each_templates: list = list()
        
        for link in chrono["link_coulombdamping"]:
            link_coulombdamping_each_templates.append(get_template_text(cls.COULOMBDAMPING_BASE).format(**link))

        return LINE_END.join(link_coulombdamping_each_templates)

    @classmethod
    def get_pulley_each_template(cls, chrono: dict) -> str:
        """ Renders the link_pulley part of the chrono template. """
        link_pulley_each_templates: list = list()

        for link in chrono["link_pulley"]:
            link_pulley_each_templates.append(get_template_text(cls.PULLEY_BASE).format(**link))

        return LINE_END.join(link_pulley_each_templates)
