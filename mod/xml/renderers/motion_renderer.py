# -*- coding: utf-8 -*-
""" Motion template renderer.

Renders the <motion> tag of the GenCase XML.
"""

from mod.template_tools import get_template_text

from mod.enums import MotionType
from mod.constants import LINE_END, MKFLUID_LIMIT


class MotionRenderer():
    """ Renders the <motion> tag of the GenCase XML. """

    MOTION_BASE_XML = "/templates/gencase/motion/base.xml"
    MOTION_EACH_BASE_XML = "/templates/gencase/motion/each/base.xml"
    MOTION_EACH_MOVEMENT_LIST_XML = "/templates/gencase/motion/each/movements_list.xml"
    MOTION_TEMPLATES = {
        MotionType.RECTILINEAR: "/templates/gencase/motion/each/normal/rectilinear.xml",
        MotionType.WAIT: "/templates/gencase/motion/each/normal/wait.xml",
        MotionType.ACCELERATED_RECTILINEAR: "/templates/gencase/motion/each/normal/acc_rectilinear.xml",
        MotionType.ROTATIONAL: "/templates/gencase/motion/each/normal/rotational.xml",
        MotionType.ACCELERATED_ROTATIONAL: "/templates/gencase/motion/each/normal/acc_rotational.xml",
        MotionType.CIRCULAR: "/templates/gencase/motion/each/normal/circular.xml",
        MotionType.SINUSOIDAL_ROTATIONAL: "/templates/gencase/motion/each/normal/sinu_rotational.xml",
        MotionType.SINUSOIDAL_CIRCULAR: "/templates/gencase/motion/each/normal/sinu_circular.xml",
        MotionType.SINUSOIDAL_RECTILINEAR: "/templates/gencase/motion/each/normal/sinu_rectilinear.xml"
    }
    MOTION_NEXT_ATTR = "/templates/gencase/motion/each/next_attr.txt"
    MOTION_GENERATORS_TEMPLATES = {
        MotionType.FILE_GENERATOR: "/templates/gencase/motion/each/special/file_gen.xml",
        MotionType.FILE_ROTATIONAL_GENERATOR: "/templates/gencase/motion/each/special/file_rotational_gen.xml"
    }
    MOTION_NULL_TEMPLATE = "/templates/gencase/motion/each/null.xml"

    @classmethod
    def render(cls, data):
        """ Returns the rendered string. """
        each_objreal_template: list = list()
        for prop in data["mkbasedproperties"].values():
            if not prop["movements"] and not prop["mlayerpiston"]:
                continue

            formatter: dict = {
                "ref": prop["mk"] - MKFLUID_LIMIT,
                "movements_list": cls.get_movement_template_list(prop)
            }

            each_objreal_template.append(get_template_text(cls.MOTION_EACH_BASE_XML).format(**formatter))

        if not each_objreal_template:
            # There are no movements in the case. Do not bother rendering the <motion> tag.
            return ""

        formatter: dict = {
            "each_objreal": LINE_END.join(each_objreal_template)
        }

        return get_template_text(cls.MOTION_BASE_XML).format(**formatter)

    @classmethod
    def get_specific_motion_template(cls, motion, first_index: int, index: int, is_last: bool, loops: bool):
        """ Renders an individual motion based on its type. """
        if motion["type"] not in cls.MOTION_TEMPLATES.keys():
            return get_template_text(cls.MOTION_NULL_TEMPLATE)

        motion.update({
            "index": index,
            "next_attr": get_template_text(cls.MOTION_NEXT_ATTR).format(next_index=index + 1)
        })

        if is_last:
            motion["next_attr"] = "" if not loops else get_template_text(cls.MOTION_NEXT_ATTR).format(next_index=first_index)

        return get_template_text(cls.MOTION_TEMPLATES[motion["type"]]).format(**motion)

    @classmethod
    def get_special_motion_template(cls, motion_generator: dict) -> str:
        """ Renders an SpecialMovement motion inside a movement. """
        if not motion_generator:
            raise ValueError("Generator for an SpecialMovement should always have a value")

        if motion_generator["type"] not in cls.MOTION_GENERATORS_TEMPLATES.keys():
            return get_template_text(cls.MOTION_NULL_TEMPLATE)

        return get_template_text(cls.MOTION_GENERATORS_TEMPLATES[motion_generator["type"]]).format(**motion_generator)

    @classmethod
    def get_each_motion_template(cls, movement: dict, counter: int) -> str:
        """ Renders the list of motions inside a movement. """
        if "generator" in movement.keys():
            # Is a SpecialMovement
            return cls.get_special_motion_template(movement["generator"])

        # If this code path is followed, is a regular movement
        if not movement["motion_list"]:
            return ""

        motion_templates: list = list()
        first_index = counter
        index = counter

        for it_index, motion in enumerate(movement["motion_list"]):
            is_last = it_index == len(movement["motion_list"]) - 1
            loops = is_last and movement["loop"]
            motion_templates.append(cls.get_specific_motion_template(motion, first_index, index, is_last, loops))
            index += 1

        return LINE_END.join(motion_templates)

    @classmethod
    def get_movement_template_list(cls, mk_based_prop: dict) -> str:
        """ Returns a rendered list of movements. """
        counter: int = 1
        each_movement_template: list = list()
        if mk_based_prop["mlayerpiston"]:
            formatter: dict = {
                "count": counter,
                "motions_list": get_template_text(cls.MOTION_NULL_TEMPLATE)
            }
            each_movement_template.append(get_template_text(cls.MOTION_EACH_MOVEMENT_LIST_XML).format(**formatter))
        else:
            for mov in mk_based_prop["movements"]:
                formatter: dict = {
                    "count": counter,
                    "motions_list": cls.get_each_motion_template(mov, counter),
                }
                each_movement_template.append(get_template_text(cls.MOTION_EACH_MOVEMENT_LIST_XML).format(**formatter))
                counter += len(mov["motion_list"]) if "motion_list" in mov.keys() else 1

        return LINE_END.join(each_movement_template)
