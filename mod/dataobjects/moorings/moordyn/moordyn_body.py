#!/usr/bin/env python3.7
# -*- coding: utf-8 -*-
""" DesignSPHysics MoorDyn body. """


class MoorDynBody():
    """ MoorDyn Body object representation. """

    def __init__(self, ref, depth=False):
        super().__init__()
        self.ref: int = ref  # This is the mkbound
        self.depth: float = depth  # Only used if is not false. Check for bool!
