# -*- coding: utf-8 -*-
"""XML Exporter for DesignSPHysics

The utilities on this module creates

"""

import os
from datetime import datetime

from mod.stdout_tools import debug

from mod.constants import APP_NAME, LINE_END
from mod.template_tools import obj_to_dict, get_template_text

from mod.xml.renderers.definition_renderer import DefinitionRenderer
from mod.xml.renderers.objects_renderer import ObjectsRenderer
from mod.xml.renderers.simulationdomain_renderer import SimulationDomainRenderer
from mod.xml.renderers.initials_renderer import InitialsRenderer
from mod.xml.renderers.floatings_renderer import FloatingsRenderer
from mod.xml.renderers.rzones_renderer import RZonesRenderer
from mod.xml.renderers.accinput_renderer import AccinputRenderer
from mod.xml.renderers.damping_renderer import DampingRenderer
from mod.xml.renderers.mlpistons_renderer import MLPistonsRenderer
from mod.xml.renderers.motion_renderer import MotionRenderer
from mod.xml.renderers.wavepaddles_renderer import WavePaddlesRenderer
from mod.xml.renderers.inout_renderer import InoutRenderer
from mod.xml.renderers.chrono_renderer import ChronoRenderer
from mod.xml.renderers.periodicity_renderer import PeriodicityRenderer
from mod.xml.renderers.moorings_renderer import MooringsRenderer
from mod.xml.renderers.properties_renderer import PropertiesRenderer


class XMLExporter():
    """ Handles XML generation and data transformation to adapt to DualSPHysics
    preprocessing tools """

    BASE_XML = "/templates/gencase/base.xml"
    BASE_MATERIALS_XML = "/templates/gencase/materials/base.xml"
    PROPERTY_MATERIALS_XML = "/templates/gencase/materials/property.xml"
    GENCASE_XML_SUFFIX = "_Def.xml"
    MATERIAL_FILE_NAME = "materials.xml"

    def __init__(self):
        self.mod_folder = "{}/..".format(os.path.dirname(os.path.realpath(__file__)))

    def transform_bools_to_strs(self, value):
        """ Transforms a boolean value to a string representing its state, understandable by GenCase. """
        if isinstance(value, bool):
            return "true" if value else "false"
        if isinstance(value, list):
            return [self.transform_bools_to_strs(v) for v in value]
        if isinstance(value, dict):
            return {k: self.transform_bools_to_strs(v) for k, v in value.items()}
        return value

    def get_adapted_case_data(self, case: "Case") -> dict:
        """ Adapts the case data to a dictionary used to format the resulting XML """
        data: dict = obj_to_dict(case)
        data = self.transform_bools_to_strs(data)

        data["definition_template"] = DefinitionRenderer.render(data)
        data["objects_template"] = ObjectsRenderer.render(data)
        data["simulationdomain_template"] = SimulationDomainRenderer.render(data)
        data["periodicity_template"] = PeriodicityRenderer.render(data)
        data["initials_template"] = InitialsRenderer.render(data)
        data["floatings_template"] = FloatingsRenderer.render(data)
        data["rzones_template"] = RZonesRenderer.render(data, type(case.relaxation_zone).__name__) if case.relaxation_zone else ""
        data["accinput_template"] = AccinputRenderer.render(data)
        data["damping_template"] = DampingRenderer.render(data) if case.damping_zones.keys() else ""
        data["mlpistons_template"] = MLPistonsRenderer.render(data)
        data["motion_template"] = MotionRenderer.render(data)
        data["wavepaddles_template"] = WavePaddlesRenderer.render(data)
        data["inout_template"] = InoutRenderer.render(data)
        data["chrono_template"] = ChronoRenderer.render(data)
        data["moorings_template"] = MooringsRenderer.render(data)
        data["properties_template"] = PropertiesRenderer.render(data)
        data["application"] = APP_NAME
        data["current_date"] = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
        return data

    def generate(self, case) -> str:
        """ Returns the GenCase-compatible XML resulting from the case """
        final_xml: str = get_template_text(self.BASE_XML).format(**self.get_adapted_case_data(case))

        # Strip empty lines from the final XML to clean it up.
        while "\n\n" in final_xml:
            final_xml = final_xml.replace("\n\n", "\n")

        return final_xml

    def generate_material(self, case) -> str:
        """ Returns a material XML definition for DualSPHysics from the data available on the given case. """

        properties_list: list = list()
        for mkbasedproperty in case.mkbasedproperties.values():
            if mkbasedproperty.property:
                if not any(mkbasedproperty.property.name in prop for prop in properties_list):
                    properties_list.append(get_template_text(self.PROPERTY_MATERIALS_XML).format(**mkbasedproperty.property.__dict__))

        formatter: dict = {
            "each_property": LINE_END.join(properties_list)
        }

        return get_template_text(self.BASE_MATERIALS_XML).format(**formatter)

    def save_to_disk(self, path, case: "Case") -> None:
        """ Creates a file on disk with the contents of the GenCase generated XML. """
        with open("{}/{}".format(path, self.MATERIAL_FILE_NAME), "w", encoding="utf-8") as file:
            file.write(self.generate_material(case))
        with open("{}/{}{}".format(path, case.name, self.GENCASE_XML_SUFFIX), "w", encoding="utf-8") as file:
            file.write(self.generate(case))
