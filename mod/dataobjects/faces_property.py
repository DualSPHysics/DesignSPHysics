#!/usr/bin/env python3.7
# -*- coding: utf-8 -*-
""" DesignSPHysics Faces Property data """


class FacesProperty():
    """ Stores the faces selected to generate on GenCase for a given object """

    def __init__(self, all_faces=False, front_face=False,
                 back_face=False, top_face=False, bottom_face=False,
                 left_face=False, right_face=False, face_print=""):
        self.all_faces = all_faces
        self.front_face = front_face
        self.back_face = back_face
        self.top_face = top_face
        self.bottom_face = bottom_face
        self.left_face = left_face
        self.right_face = right_face
        self.face_print = face_print
