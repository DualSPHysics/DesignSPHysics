#!/usr/bin/env python3.7
# -*- coding: utf-8 -*-
""" DesignSPHysics MoorDynPlus body. """


class MoorDynPlusBody():
    """ MoorDynPlus Body object representation. """

    def __init__(self, ref, depth=False):
        self.ref: int = ref  # This is the mkbound
        self.depth: float = depth  # Only used if is not false. Check for bool!

