#!/usr/bin/env python3.7
# -*- coding: utf-8 -*-
"""DesignSPHysics MK selector widget"""
from PySide2 import QtWidgets
from mod.constants import DEFAULT_MIN_WIDGET_WIDTH, DEFAULT_MAX_WIDGET_WIDTH
from mod.dataobjects.case import Case
from mod.enums import ObjectType
from mod.tools.freecad_tools import get_fc_object
from mod.tools.stdout_tools import debug


class MkSelectInputWithNames(QtWidgets.QComboBox):

    def __init__(self, obj_type: ObjectType,min_width=DEFAULT_MIN_WIDGET_WIDTH,max_width=DEFAULT_MAX_WIDGET_WIDTH):
        super().__init__()
        self.obj_type=obj_type
        self.mk_list = []
        self.mk_name_dict={}
        self.setMinimumWidth(min_width)
        self.setMaximumWidth(max_width)
        self.update_mk_list()


    def update_mk_list(self):
        self.mk_list = []
        self.clear()
        obj_list = self.get_all_objects()
        if obj_list:
            for obj in obj_list:
                self.mk_list.append(obj.obj_mk)
                self.mk_name_dict[obj.obj_mk] = get_fc_object(obj.name).Label
                self.addItem(f"{obj.obj_mk}: {self.mk_name_dict[obj.obj_mk]}")

    def get_all_objects(self):
        return list(filter(lambda obj: obj.type == self.obj_type, Case.the().objects))

    def text(self):
        return self.itemText(self.currentIndex())

    def get_mk_value(self) -> int:
        if self.mk_list:
            return self.mk_list[self.currentIndex()]
        else:
            return -1

    def set_mk_index(self, mk: int):
        index = self.get_index(mk)
        if index:
            self.setCurrentIndex(index)
        else:
            self.setCurrentIndex(0)

    def get_index(self, mk_value: int):
        self.update_mk_list()
        try :
            index=self.mk_list.index(mk_value)
        except ValueError:
            index=None
        return index

    def set_object_type(self,object_type:ObjectType):
        self.obj_type=object_type
        self.update_mk_list()


