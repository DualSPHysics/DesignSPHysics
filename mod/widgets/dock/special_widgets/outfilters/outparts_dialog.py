from PySide2 import QtWidgets
from mod.constants import OUTFILTERS_GROUP_NAME
from mod.dataobjects.case import Case

from mod.dataobjects.outparts_filter.filters import FilterPos, FilterPlane, FilterSphere, FilterCylinder, TypeFilter, \
    FilterMK, FilterGroup
from mod.tools.dialog_tools import ok_cancel_dialog, info_dialog
from mod.tools.freecad_tools import delete_object, create_parts_out_sphere, create_parts_out_box, \
    get_fc_object, create_parts_out_cylinder
from mod.tools.freecad_tools import manage_partfilters

from mod.tools.translation_tools import __
from mod.widgets.custom_widgets.int_value_input import IntValueInput

from mod.widgets.dock.special_widgets.outfilters.cylinder_filter_dialog import CylinderFilterDialog
from mod.widgets.dock.special_widgets.outfilters.group_filter_dialog import GroupFilterDialog
from mod.widgets.dock.special_widgets.outfilters.mk_filter_dialog import MKFilterDialog
from mod.widgets.dock.special_widgets.outfilters.plane_filter_dialog import PlaneFilterDialog
from mod.widgets.dock.special_widgets.outfilters.pos_filter_dialog import PosFilterDialog
from mod.widgets.dock.special_widgets.outfilters.sphere_filter_dialog import SphereFilterDialog
from mod.widgets.dock.special_widgets.outfilters.type_filter_dialog import TypeFilterDialog


class OutpartsDialog(QtWidgets.QDialog):

    def __init__(self, parent):
        super().__init__(parent=parent)

        self.setWindowTitle(__("Output parts filters list"))
        self.main_layout = QtWidgets.QVBoxLayout()

        self.active_layout = QtWidgets.QHBoxLayout()
        self.active_checkbox = QtWidgets.QCheckBox(__("Active"))
        self.active_layout.addWidget(self.active_checkbox)

        self.preselect_all_layout = QtWidgets.QHBoxLayout()
        self.preselect_all_checkbox = QtWidgets.QCheckBox(__("Preselect all"))
        self.preselect_all_layout.addWidget(self.preselect_all_checkbox)

        self.ignore_nparts_layout = QtWidgets.QHBoxLayout()
        self.ignore_nparts_label = QtWidgets.QLabel(__("Ignore each n files"))
        self.ignore_nparts_input = IntValueInput()
        self.ignore_nparts_layout.addWidget(self.ignore_nparts_label)
        self.ignore_nparts_layout.addWidget(self.ignore_nparts_input)

        self.list_layout = QtWidgets.QHBoxLayout()
        self.filter_list = QtWidgets.QListWidget()

        self.list_layout.addWidget(self.filter_list)

        self.buttons_layout = QtWidgets.QHBoxLayout()
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


        self.ok_button = QtWidgets.QPushButton(text=__("OK"))
        self.ok_button.clicked.connect(self.on_ok)
        self.buttons_layout.addWidget(self.add_filter_button)
        self.buttons_layout.addWidget(self.edit_filter_button)
        self.buttons_layout.addWidget(self.delete_filter_button)
        self.buttons_layout.addWidget(self.ok_button)

        self.main_layout.addLayout(self.active_layout)
        self.main_layout.addLayout(self.preselect_all_layout)
        self.main_layout.addLayout(self.ignore_nparts_layout)
        self.main_layout.addLayout(self.list_layout)
        self.main_layout.addLayout(self.buttons_layout)
        self.setLayout(self.main_layout)

        self.preselect_all_checkbox.setChecked(Case.the().outparts.preselection_all)
        self.active_checkbox.setChecked(Case.the().outparts.active)
        self.ignore_nparts_input.setValue(Case.the().outparts.ignore_nparts)
        self.active_checkbox.stateChanged.connect(self.on_activate)
        self.filter_list.itemSelectionChanged.connect(self.on_selection_change)
        self.edit_filter_button.setEnabled(False)
        self.delete_filter_button.setEnabled(False)

        self.on_activate(Case.the().outparts.active)
        manage_partfilters(Case.the().outparts.filts)
        self.update_filter_list()

    def on_ok(self):
        Case.the().outparts.preselection_all = self.preselect_all_checkbox.isChecked()
        Case.the().outparts.active = self.active_checkbox.isChecked()
        Case.the().outparts.ignore_nparts = self.ignore_nparts_input.value()
        self.accept()

    def on_cancel(self):
        self.reject()

    def on_add_filter_menu(self, action):
        """ Defines damping menu behaviour"""
        if __("Add position filter") in action.text():
            new_filter = FilterPos()
            new_filter.fc_object_name = create_parts_out_box(new_filter)
            get_fc_object(OUTFILTERS_GROUP_NAME).addObject(get_fc_object(new_filter.fc_object_name))
            get_fc_object(new_filter.fc_object_name).addProperty("App::PropertyVector", "lastposition")
            dialog = PosFilterDialog(pos_filter=new_filter, parent=None)
        elif __("Add plane filter") in action.text():
            new_filter = FilterPlane()
            dialog = PlaneFilterDialog(plane_filter=new_filter, parent=None)
        elif __("Add sphere filter") in action.text():
            new_filter = FilterSphere()
            new_filter.fc_object_name = create_parts_out_sphere(new_filter)
            get_fc_object(OUTFILTERS_GROUP_NAME).addObject(get_fc_object(new_filter.fc_object_name))
            get_fc_object(new_filter.fc_object_name).addProperty("App::PropertyVector", "lastposition")
            dialog = SphereFilterDialog(sphere_filter=new_filter, parent=None)
        elif __("Add cylinder filter") in action.text():
            new_filter = FilterCylinder()
            new_filter.fc_object_name = create_parts_out_cylinder(new_filter)
            get_fc_object(OUTFILTERS_GROUP_NAME).addObject(get_fc_object(new_filter.fc_object_name))
            get_fc_object(new_filter.fc_object_name).addProperty("App::PropertyVector", "lastposition")
            dialog = CylinderFilterDialog(cylinder_filter=new_filter, parent=None)
        elif __("Add type filter") in action.text():
            new_filter = TypeFilter()
            dialog = TypeFilterDialog(type_filter=new_filter, parent=None)
        elif __("Add mk filter") in action.text():
            new_filter = FilterMK()
            dialog = MKFilterDialog(mk_filter=new_filter, parent=None)
        else:  # if __("Add group filter") in action.text():
            new_filter = FilterGroup()
            dialog = GroupFilterDialog(group_filter=new_filter, parent=None)
        ret=dialog.exec_()
        if ret==QtWidgets.QDialog.Accepted:
            if new_filter.name in Case.the().outparts.filts.keys():
                info_dialog(f"Filter named {new_filter.name} already exists")
            else:
                Case.the().outparts.add_filter(new_filter)
            new_filter.process_strings()
        else:
            delete_object(new_filter.fc_object_name)
        self.update_filter_list()

    def update_filter_list(self):
        self.filter_list.clear()
        for name in Case.the().outparts.filts.keys():
            self.filter_list.addItem(name)
        self.filter_list.setCurrentRow(0)

    def on_edit(self):
        name = self.filter_list.currentItem().text()
        filter = Case.the().outparts.filts[name]  # get_by_name
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
        filt=Case.the().outparts.filts[name]
        if filt.__class__ == FilterGroup:
            ret = ok_cancel_dialog("Warning", "Children will also be deleted")
            if ret == 1024:  # WHY 1024???
                self.delete_children(filt)
                Case.the().outparts.remove_filter(name)
        else:
            delete_object(Case.the().outparts.filts[name].fc_object_name)
            Case.the().outparts.remove_filter(name)

        self.update_filter_list()

    def on_activate(self, active):
        for x in [self.preselect_all_checkbox, self.filter_list, self.add_filter_button,self.edit_filter_button,
                  self.delete_filter_button]:
            x.setEnabled(active)
        if active:
            self.on_selection_change()

    def on_selection_change(self):
        if self.filter_list.selectedItems():
            self.edit_filter_button.setEnabled(True)
            self.delete_filter_button.setEnabled(True)
        else :
            self.edit_filter_button.setEnabled(False)
            self.delete_filter_button.setEnabled(False)

    def delete_children(self,parent):
        filts:dict=parent.filts
        for name,filt in filts.items():
            if filt.__class__ == FilterGroup:
                self.delete_children(filt)
            else:
                delete_object(filt.fc_object_name)
