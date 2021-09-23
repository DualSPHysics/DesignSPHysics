#!/usr/bin/env python3.7
# -*- coding: utf-8 -*-
""" DesignSPHysics Faces Property data """


class FacesProperty():
    """ Stores the faces selected to generate on GenCase for a given object """

    def __init__(self, all_faces=False, front_face=False,
                 back_face=False, top_face=False, bottom_face=False,
                 left_face=False, right_face=False, face_print="", layers=""):
        self.all_faces = all_faces
        self.front_face = front_face
        self.back_face = back_face
        self.top_face = top_face
        self.bottom_face = bottom_face
        self.left_face = left_face
        self.right_face = right_face
        self.face_print = face_print
        self.layers = layers

    def build_face_print(self) -> None:
        """ Builds a string to print faces. """
        if self.all_faces:
            self.face_print = "all"
            return

        applied_faces: list = list()
        applied_faces.append("front" if self.front_face else None)
        applied_faces.append("back" if self.back_face else None)
        applied_faces.append("top" if self.top_face else None)
        applied_faces.append("bottom" if self.bottom_face else None)
        applied_faces.append("left" if self.left_face else None)
        applied_faces.append("right" if self.right_face else None)

        self.face_print = " | ".join(filter(lambda x: x is not None, applied_faces))
