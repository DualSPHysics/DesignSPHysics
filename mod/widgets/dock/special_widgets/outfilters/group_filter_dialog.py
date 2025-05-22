from PySide2.QtWidgets import QHBoxLayout

from PySide2 import QtWidgets
from mod.dataobjects.outparts_filter.filters import FilterGroup, FilterPos, FilterPlane, FilterSphere, FilterCylinder, \
    TypeFilter, FilterMK
from mod.tools.dialog_tools import warning_dialog, info_dialog, ok_cancel_dialog
from mod.tools.freecad_tools import delete_object
from mod.tools.translation_tools import __
from mod.widgets.dock.special_widgets.outfilters.base_dialog import BaseFilterDialog
from mod.widgets.dock.special_widgets.outfilters.cylinder_filter_dialog import CylinderFilterDialog
from mod.widgets.dock.special_widgets.outfilters.mk_filter_dialog import MKFilterDialog
from mod.widgets.dock.special_widgets.outfilters.plane_filter_dialog import PlaneFilterDialog
from mod.widgets.dock.special_widgets.outfilters.pos_filter_dialog import PosFilterDialog
from mod.widgets.dock.special_widgets.outfilters.sphere_filter_dialog import SphereFilterDialog
from mod.widgets.dock.special_widgets.outfilters.type_filter_dialog import TypeFilterDialog


class GroupFilterDialog(BaseFilterDialog):

    def __init__(self,group_filter,parent=None):
        super().__init__(base_filter=group_filter,parent=parent)
        self.data:FilterGroup=group_filter
        self.group_layout = QHBoxLayout()

        self.preselect_all_layout = QtWidgets.QHBoxLayout()
        self.preselect_all_checkbox = QtWidgets.QCheckBox(__("Preselect all"))
        self.preselect_all_layout.addWidget(self.preselect_all_checkbox)

        self.list_layout = QtWidgets.QHBoxLayout()
        self.filter_list = QtWidgets.QListWidget()
        self.list_layout.addWidget(self.filter_list)

        self.add_filter_button = QtWidgets.QPushButton(__("Add filter"))
        self.add_filter_menu = QtWidgets.QMenu()
        self.add_filter_menu.addAction(__("Add position filter"))
        self.add_filter_menu.addAction(__("Add plane filter"))
        self.add_filter_menu.addAction(__("Add sphere filter"))
        self.add_filter_menu.addAction(__("Add cylinder filter"))
        self.add_filter_menu.addAction(__("Add type filter"))
        self.add_filter_menu.addAction(__("Add mk filter"))
        self.add_filter_menu.addAction(__("Add group filter"))
        self.add_filter_button.setMenu(self.add_filter_menu)
        self.add_filter_menu.triggered.connect(self.on_add_filter_menu)
        self.edit_filter_button = QtWidgets.QPushButton(__("Edit filter"))
        self.edit_filter_button.clicked.connect(self.on_edit)
        self.delete_filter_button = QtWidgets.QPushButton(__("Delete filter"))
        self.delete_filter_button.clicked.connect(self.on_delete)
        #self.ok_button = QtWidgets.QPushButton(text=__("OK"))
        #self.ok_button.clicked.connect(self.save_data)
        self.buttons_layout.insertWidget(0,self.add_filter_button)
        self.buttons_layout.insertWidget(1,self.edit_filter_button)
        self.buttons_layout.insertWidget(2,self.delete_filter_button)
        #self.buttons_layout.insertWidget(3,self.ok_button)

        self.main_layout.insertLayout(2,self.preselect_all_layout)
        self.main_layout.insertLayout(3,self.list_layout)
        self.fill_values()

    def fill_values(self):
        super().fill_values()
        self.preselect_all_checkbox.setChecked(self.data.preselection_all)
        self.update_filter_list()

    def update_filter_list(self):
        self.filter_list.clear()
        for name in self.data.filts.keys():
            self.filter_list.addItem(name)
        self.filter_list.setCurrentRow(0)
    def save_data(self):
        super().save_data()
        self.data.preselection_all = self.preselect_all_checkbox.isChecked()
        if self.data.name:
            self.accept()
        else:
            warning_dialog("Please name your Filter")

    def on_add_filter_menu(self,action):
        """ Defines damping menu behaviour"""
        if __("Add position filter") in action.text():
            new_filter = FilterPos()
            dialog = PosFilterDialog(pos_filter=new_filter, parent=None)
            dialog.exec_()
        elif __("Add plane filter") in action.text():
            new_filter = FilterPlane()
            dialog = PlaneFilterDialog(plane_filter=new_filter, parent=None)
            dialog.exec_()
        elif __("Add sphere filter") in action.text():
            new_filter = FilterSphere()
            dialog = SphereFilterDialog(sphere_filter=new_filter, parent=None)
            dialog.exec_()
        elif __("Add cylinder filter") in action.text():
            new_filter = FilterCylinder()
            dialog = CylinderFilterDialog(cylinder_filter=new_filter, parent=None)
            dialog.exec_()
        elif __("Add type filter") in action.text():
            new_filter = TypeFilter()
            dialog = TypeFilterDialog(type_filter=new_filter, parent=None)
            dialog.exec_()
        elif __("Add mk filter") in action.text():
            new_filter = FilterMK()
            dialog = MKFilterDialog(mk_filter=new_filter, parent=None)
            dialog.exec_()
        else: #if __("Add group filter") in action.text():
            new_filter = FilterGroup()
            dialog = GroupFilterDialog(group_filter=new_filter, parent=None)
            dialog.exec_()
        if new_filter.name in self.data.filts.keys():
            info_dialog(f"Filter named {new_filter.name} already exists")
        else:
            self.data.add_filter(new_filter)
        new_filter.process_strings()
        self.update_filter_list()

    def on_edit(self):
        name = self.filter_list.currentItem().text()
        filter =self.data.filts[name]  # get_by_name
        if filter.__class__ == FilterPos:
            dialog = PosFilterDialog(pos_filter=filter, parent=None)
            dialog.exec_()
        elif filter.__class__ == FilterPlane:
            dialog = PlaneFilterDialog(plane_filter=filter, parent=None)
            dialog.exec_()
        elif filter.__class__ == FilterSphere:
            dialog = SphereFilterDialog(sphere_filter=filter, parent=None)
            dialog.exec_()
        elif filter.__class__ == FilterCylinder:
            dialog = CylinderFilterDialog(cylinder_filter=filter, parent=None)
            dialog.exec_()
        elif filter.__class__ == TypeFilter:
            dialog = TypeFilterDialog(type_filter=filter, parent=None)
            dialog.exec_()
        elif filter.__class__ == FilterMK:
            dialog = MKFilterDialog(mk_filter=filter, parent=None)
            dialog.exec_()
        elif filter.__class__ == FilterGroup:
            dialog = GroupFilterDialog(group_filter=filter, parent=None)
            dialog.exec_()
        filter.process_strings()
        self.update_filter_list()

    def on_delete(self):
        name = self.filter_list.currentItem().text()
        filt=self.data.filts[name]
        if filt.__class__ == FilterGroup:
            ret = ok_cancel_dialog("Warning", "Children will also be deleted")
            if ret == 1024:  # WHY 1024???
                self.data.remove_filter(name)
                self.delete_children(filt)
        else:
            delete_object(filt.fc_object_name)
            self.data.remove_filter(name)
        self.update_filter_list()

    def delete_children(self, parent):
        filts: dict = parent.filts
        for name, filt in filts.items():
            if filt.__class__ == FilterGroup:
                self.delete_children(filt)
            else:
                delete_object(filt.fc_object_name)

