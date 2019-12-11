# -*- coding: utf-8 -*-
""" WavePaddles template renderer.

Renders the <wavepaddles> tag of the GenCase XML.
"""

from mod.template_tools import get_template_text

from mod.enums import MotionType
from mod.constants import LINE_END, MKFLUID_LIMIT


class WavePaddlesRenderer():
    """ Renders the <wavepaddles> tag of the GenCase XML. """

    WAVEPADDLES_TEMPLATE_BASE = "/templates/gencase/wavepaddles/base.xml"
    WAVEPADDLES_REGULAR_PISTON = "/templates/gencase/wavepaddles/piston/regular.xml"
    WAVEPADDLES_IRREGULAR_PISTON = "/templates/gencase/wavepaddles/piston/irregular.xml"
    WAVEPADDLES_PISTON_AWAS = "/templates/gencase/wavepaddles/awas.xml"
    WAVEPADDLES_PISTON_AWAS_CORRECTION = "/templates/gencase/wavepaddles/awas_correction.xml"
    WAVEPADDLES_REGULAR_FLAP = "/templates/gencase/wavepaddles/flap/regular.xml"
    WAVEPADDLES_IRREGULAR_FLAP = "/templates/gencase/wavepaddles/flap/irregular.xml"

    @classmethod
    def render(cls, data):
        """ Returns the rendered string. """
        target_types: list = [MotionType.REGULAR_PISTON_WAVE_GENERATOR, MotionType.IRREGULAR_PISTON_WAVE_GENERATOR, MotionType.REGULAR_FLAP_WAVE_GENERATOR, MotionType.IRREGULAR_FLAP_WAVE_GENERATOR]
        filtered_mkprops: list = list(filter(lambda mkprop: len(mkprop["movements"]) == 1 and "generator" in mkprop["movements"][0] and mkprop["movements"][0]["generator"] and mkprop["movements"][0]["generator"]["type"] in target_types, data["mkbasedproperties"].values()))

        if not filtered_mkprops:
            return ""

        formatter: dict = {
            "each": cls.get_each_wavepaddle(filtered_mkprops)
        }

        return get_template_text(cls.WAVEPADDLES_TEMPLATE_BASE).format(**formatter)

    @classmethod
    def get_awas_template(cls, awas: dict) -> str:
        """ Renders the <awas_zsurf> tag for a piston generator. """

        awas["correction"]["correction_enabled"] = "" if awas["correction"]["enabled"] == "true" else "_"

        awas["correction_template"] = get_template_text(cls.WAVEPADDLES_PISTON_AWAS_CORRECTION).format(**awas["correction"])

        return get_template_text(cls.WAVEPADDLES_PISTON_AWAS).format(**awas)

    @classmethod
    def get_regular_piston_wave_template(cls, mk: int, generator: dict) -> str:
        """ Renders a <piston> tag from a regular piston wave generator. """
        generator["mk"] = mk

        generator["awas_template"] = cls.get_awas_template(generator["awas"]) if generator["awas"]["enabled"] == "true" else ""

        return get_template_text(cls.WAVEPADDLES_REGULAR_PISTON).format(**generator)

    @classmethod
    def get_irregular_piston_wave_template(cls, mk: int, generator: dict) -> str:
        """ Renders a <piston_spectrum> tag from an irregular piston wave generator. """
        generator["mk"] = mk

        generator["awas_template"] = cls.get_awas_template(generator["awas"]) if generator["awas"]["enabled"] == "true" else ""

        return get_template_text(cls.WAVEPADDLES_IRREGULAR_PISTON).format(**generator)

    @classmethod
    def get_regular_flap_wave_template(cls, mk: int, generator: dict) -> str:
        """ Renders a <flap> tag from a regular flap wave generator. """
        generator["mk"] = mk

        return get_template_text(cls.WAVEPADDLES_REGULAR_FLAP).format(**generator)

    @classmethod
    def get_irregular_flap_wave_template(cls, mk: int, generator: dict) -> str:
        """ Renders a <flap_spectrum> tag from a regular flap wave generator. """
        generator["mk"] = mk

        return get_template_text(cls.WAVEPADDLES_IRREGULAR_FLAP).format(**generator)

    @classmethod
    def get_each_wavepaddle(cls, mkprops: list) -> str:
        """ Returns a string with a list of wavepaddles (wave generators) from the received mkbasedproperties list. """
        each_template: list = []
        for prop in mkprops:
            movement = prop["movements"][0]
            mk_bound = prop["mk"] - MKFLUID_LIMIT
            if movement["generator"]["type"] == MotionType.REGULAR_PISTON_WAVE_GENERATOR:
                each_template.append(cls.get_regular_piston_wave_template(mk_bound, movement["generator"]))
            elif movement["generator"]["type"] == MotionType.IRREGULAR_PISTON_WAVE_GENERATOR:
                each_template.append(cls.get_irregular_piston_wave_template(mk_bound, movement["generator"]))
            elif movement["generator"]["type"] == MotionType.REGULAR_FLAP_WAVE_GENERATOR:
                each_template.append(cls.get_regular_flap_wave_template(mk_bound, movement["generator"]))
            elif movement["generator"]["type"] == MotionType.IRREGULAR_FLAP_WAVE_GENERATOR:
                each_template.append(cls.get_irregular_flap_wave_template(mk_bound, movement["generator"]))

        return LINE_END.join(each_template)
