#!/usr/bin/env python3.7
# -*- coding: utf-8 -*-
"""DesignSPHysics Inlet/Oulet Configuration Dialog """

from PySide2.QtWidgets import QDialog

from PySide2 import QtCore, QtWidgets
from mod.dataobjects.case import Case
from mod.dataobjects.inletoutlet.inlet_outlet_config import InletOutletConfig
from mod.dataobjects.inletoutlet.inlet_outlet_zone import InletOutletZone
from mod.enums import InletOutletDetermLimit, InletOutletZoneGeneratorType, ObjectType
from mod.tools.freecad_tools import delete_group, create_inout_zone_box, create_inout_zone_circle, \
    create_inout_zone_line, create_inout_zone_3d_mk_object, update_inout_zone_3d_mk_object, \
    update_inout_zone_2d_mk_object
from mod.tools.freecad_tools import manage_inlet_outlet_zones
from mod.tools.stdout_tools import log
from mod.tools.translation_tools import __
from mod.widgets.dock.special_widgets.inout.inlet_zone_edit import InletZoneEdit
from mod.widgets.custom_widgets.value_input import ValueInput


class InletZoneWidget(QtWidgets.QWidget):
    """ A widget representing a zone to embed in the zones table. """

    on_edit = QtCore.Signal(InletOutletZone)
    on_delete = QtCore.Signal(InletOutletZone)

    def __init__(self, index, io_object:InletOutletZone):
        super().__init__()
        self.layout = QtWidgets.QHBoxLayout()
        zone_type_string=""
        if io_object.zone_info.zone_generator_type==InletOutletZoneGeneratorType.LINE : zone_type_string = "2d Line"
        if io_object.zone_info.zone_generator_type == InletOutletZoneGeneratorType.MK_2D: zone_type_string = "2d MK"
        if io_object.zone_info.zone_generator_type == InletOutletZoneGeneratorType.BOX: zone_type_string = "3d Box"
        if io_object.zone_info.zone_generator_type == InletOutletZoneGeneratorType.CIRCLE: zone_type_string = "3d Circle"
        if io_object.zone_info.zone_generator_type == InletOutletZoneGeneratorType.MK_3D: zone_type_string = "3d Mk"
        self.label = QtWidgets.QLabel(__(f"Inlet/Outlet {str(index + 1)} ({zone_type_string} Zone)"))
        self.edit_button = QtWidgets.QPushButton(__("Edit"))
        self.delete_button = QtWidgets.QPushButton(__("Delete"))

        self.edit_button.clicked.connect(lambda _=False, obj=io_object: self.on_edit.emit(obj))
        self.delete_button.clicked.connect(lambda _=False, obj=io_object: self.on_delete.emit(obj))

        self.layout.addWidget(self.label)
        self.layout.addStretch(1)
        self.layout.addWidget(self.edit_button)
        self.layout.addWidget(self.delete_button)
        self.setLayout(self.layout)


class InletConfigDialog(QtWidgets.QDialog):
    """ Defines the Inlet/Outlet dialog window.
       Modifies data dictionary passed as parameter. """

    MINIMUM_WIDTH = 570
    MINIMUM_HEIGHT = 630
    MINIMUM_TABLE_SECTION_HEIGHT = 64

    def __init__(self, parent=None):
        super().__init__(parent=parent)

        # Reference to the inlet outlet configuration on the case data
        self.inlet_outlet: InletOutletConfig = Case.the().inlet_outlet

        # Creates a dialog
        self.setWindowTitle("Inlet/Outlet configuration")
        self.setModal(False)
        self.setMinimumWidth(self.MINIMUM_WIDTH)
        self.setMinimumHeight(self.MINIMUM_HEIGHT)
        self.main_layout = QtWidgets.QVBoxLayout()

        # Creates layout for content first options
        self.advanced_options_widget=QtWidgets.QWidget()
        self.io_options_layout = QtWidgets.QVBoxLayout()

        # Creates memory_resize option
        self.memory_resize_layout = QtWidgets.QHBoxLayout()
        self.memory_resize_size0_option = QtWidgets.QLabel(__("Initial Memory Resize: "))
        self.memory_resize_size0_line_edit = ValueInput()
        self.memory_resize_size0_line_edit.setValue(self.inlet_outlet.memoryresize_size0)

        self.memory_resize_size_option = QtWidgets.QLabel(__("Following Memory Resizes: "))
        self.memory_resize_size_line_edit = ValueInput()
        self.memory_resize_size_line_edit.setValue(self.inlet_outlet.memoryresize_size)

        self.memory_resize_layout.addWidget(self.memory_resize_size0_option)
        self.memory_resize_layout.addWidget(self.memory_resize_size0_line_edit)
        self.memory_resize_layout.addWidget(self.memory_resize_size_option)
        self.memory_resize_layout.addWidget(self.memory_resize_size_line_edit)


        # Creates extrapolate mode selector
        self.extrapolatemode_layout = QtWidgets.QHBoxLayout()
        self.extrapolatemode_option = QtWidgets.QLabel(__("Extrapolate mode: "))
        self.extrapolatemode_combobox = QtWidgets.QComboBox()
        self.extrapolatemode_combobox.insertItems(0, [__("Fast-Single"), __("Single"), __("Double")])
        self.extrapolatemode_combobox.setCurrentIndex(self.inlet_outlet.extrapolatemode - 1)

        self.extrapolatemode_layout.addWidget(self.extrapolatemode_option)
        self.extrapolatemode_layout.addWidget(self.extrapolatemode_combobox)
        self.extrapolatemode_layout.addStretch(1)

        # Creates use determlimit option
        self.determlimit_layout = QtWidgets.QHBoxLayout()
        self.determlimit_option = QtWidgets.QLabel(__("Determlimit: "))
        self.determlimit_combobox = QtWidgets.QComboBox()
        self.determlimit_combobox.insertItems(0, [__("1e+3"), __("1e-3")])
        self.determlimit_combobox.setCurrentIndex(0 if self.inlet_outlet.determlimit == InletOutletDetermLimit.ZEROTH_ORDER else 1)

        self.determlimit_layout.addWidget(self.determlimit_option)
        self.determlimit_layout.addWidget(self.determlimit_combobox)
        self.determlimit_layout.addStretch(1)

        self.refilling_rate_layout = QtWidgets.QHBoxLayout()
        self.refilling_rate_label = QtWidgets.QLabel(__("Refilling rate: "))
        self.refilling_rate_input = ValueInput()
        self.refilling_rate_input.setValue(self.inlet_outlet.refillingrate)

        self.refilling_rate_layout.addWidget(self.refilling_rate_label)
        self.refilling_rate_layout.addWidget(self.refilling_rate_input)

        self.useboxlimit_layout = QtWidgets.QHBoxLayout()
        self.useboxlimit_label = QtWidgets.QLabel(__("Use BoxLimit: "))
        self.useboxlimit_check = QtWidgets.QCheckBox()
        self.useboxlimit_check.setChecked(self.inlet_outlet.useboxlimit_enabled)
        self.useboxlimit_check.stateChanged.connect(self.on_useboxlimit_checked)

        self.useboxlimit_layout.addWidget(self.useboxlimit_label)
        self.useboxlimit_layout.addWidget(self.useboxlimit_check)
        self.useboxlimit_layout.addStretch(1)

        #NOT IN USE
        self.useboxlimit_freecentre_layout = QtWidgets.QHBoxLayout()
        self.useboxlimit_freecentre_label = QtWidgets.QLabel(__("Use BoxLimit Freecentre: "))
        self.useboxlimit_freecentre_check = QtWidgets.QCheckBox()
        self.useboxlimit_freecentre_check.setChecked(self.inlet_outlet.useboxlimit_freecentre_enabled)
        self.useboxlimit_freecentre_check.stateChanged.connect(self.on_useboxlimit_freecentre_checked)

        self.useboxlimit_freecentre_layout.addWidget(self.useboxlimit_freecentre_label)
        self.useboxlimit_freecentre_layout.addWidget(self.useboxlimit_freecentre_check)
        self.useboxlimit_freecentre_layout.addStretch(1)

        self.useboxlimit_freecentre_values_layout = QtWidgets.QHBoxLayout()
        self.useboxlimit_freecentre_values_label = QtWidgets.QLabel(__("Boxlimit Freecentre: "))
        self.useboxlimit_freecentre_values_x_input = ValueInput(value=self.inlet_outlet.useboxlimit_freecentre_values[0])

        self.useboxlimit_freecentre_values_y_input = ValueInput(value=self.inlet_outlet.useboxlimit_freecentre_values[1])
        self.useboxlimit_freecentre_values_z_input = ValueInput(value=self.inlet_outlet.useboxlimit_freecentre_values[2])

        self.useboxlimit_freecentre_values_layout.addWidget(self.useboxlimit_freecentre_values_label)
        self.useboxlimit_freecentre_values_layout.addWidget(self.useboxlimit_freecentre_values_x_input)
        self.useboxlimit_freecentre_values_layout.addWidget(self.useboxlimit_freecentre_values_y_input)
        self.useboxlimit_freecentre_values_layout.addWidget(self.useboxlimit_freecentre_values_z_input)
        self.useboxlimit_freecentre_layout.addStretch(1)

        self.first_row_layout: QtWidgets.QHBoxLayout = QtWidgets.QHBoxLayout()
        self.first_row_layout.addLayout(self.extrapolatemode_layout)
        self.first_row_layout.addLayout(self.determlimit_layout)
        self.first_row_layout.addLayout(self.refilling_rate_layout)

        self.second_row_layout: QtWidgets.QHBoxLayout = QtWidgets.QHBoxLayout()
        self.second_row_layout.addLayout(self.useboxlimit_layout)
        self.second_row_layout.addLayout(self.useboxlimit_freecentre_layout)
        self.second_row_layout.addLayout(self.useboxlimit_freecentre_values_layout)

        self.on_useboxlimit_checked(self.useboxlimit_check.isChecked())


        # Creates 2 main buttons
        self.finish_button = QtWidgets.QPushButton(__("Close"))
        self.button_layout = QtWidgets.QHBoxLayout()

        self.finish_button.clicked.connect(self.on_ok)

        self.button_layout.addStretch(1)
        self.button_layout.addWidget(self.finish_button)

        # Create the list for zones
        self.zones_groupbox = QtWidgets.QGroupBox(__("Inlet/Outlet zones"))
        self.zones_groupbox_layout = QtWidgets.QVBoxLayout()
        self.io_zones_table = QtWidgets.QTableWidget()
        self.io_zones_table.setColumnCount(1)
        self.io_zones_table.horizontalHeader().setResizeMode(QtWidgets.QHeaderView.Stretch)
        self.io_zones_table.verticalHeader().setDefaultSectionSize(self.MINIMUM_TABLE_SECTION_HEIGHT)
        self.io_zones_table.horizontalHeader().setVisible(False)
        self.io_zones_table.verticalHeader().setVisible(False)

        # Add buttons
        self.add_button_layout = QtWidgets.QHBoxLayout()
        self.add_line_zone_button = QtWidgets.QPushButton(__("Add 2D Line Zone"))
        self.add_2d_mk_zone_button = QtWidgets.QPushButton(__("Add 2D Mk Zone"))
        self.add_box_zone_button = QtWidgets.QPushButton(__("Add 3D Box Zone"))
        self.add_circle_zone_button = QtWidgets.QPushButton(__("Add 3D Circle Zone"))
        self.add_3d_mk_zone_button = QtWidgets.QPushButton(__("Add 3D Mk Zone"))

        #self.add_button_layout.addStretch(1)
        for x in(self.add_line_zone_button,self.add_2d_mk_zone_button,self.add_box_zone_button,self.add_circle_zone_button,self.add_3d_mk_zone_button):
            self.add_button_layout.addWidget(x)
        self.add_line_zone_button.clicked.connect(self.on_add_line_zone)
        self.add_2d_mk_zone_button.clicked.connect(self.on_add_2d_mk_zone)
        self.add_box_zone_button.clicked.connect(self.on_add_box_zone)
        self.add_circle_zone_button.clicked.connect(self.on_add_circle_zone)
        self.add_3d_mk_zone_button.clicked.connect(self.on_add_3d_mk_zone)

        self.zones_groupbox_layout.addLayout(self.add_button_layout)
        self.zones_groupbox_layout.addWidget(self.io_zones_table)

        self.zones_groupbox.setLayout(self.zones_groupbox_layout)

        # Adds options to option layout
        self.io_options_layout.addLayout(self.memory_resize_layout)
        self.io_options_layout.addLayout(self.first_row_layout)
        self.io_options_layout.addLayout(self.second_row_layout)

        self.advanced_options_widget.setLayout(self.io_options_layout)
        self.advanced_options_layout=QtWidgets.QVBoxLayout()
        self.advanced_options_layout.addWidget(self.advanced_options_widget)
        self.advanced_options_groupbox = QtWidgets.QGroupBox(__("Advanced options"))
        self.advanced_options_groupbox.setLayout(self.advanced_options_layout)
        self.advanced_options_groupbox.setCheckable(True)
        self.advanced_options_groupbox.setChecked(False)
        self.advanced_options_widget.hide()
        self.advanced_options_groupbox.clicked.connect(self.on_advanced_options_clicked)

        # Adds options to main
        self.main_layout.addWidget(self.zones_groupbox)
        self.main_layout.addWidget(self.advanced_options_groupbox)
        self.main_layout.addLayout(self.button_layout)

        self.setLayout(self.main_layout)
        self.refresh_zones()
        self.finish_button.setFocus()

        manage_inlet_outlet_zones(Case.the().inlet_outlet.zones)


    def on_add_line_zone(self):
        """ Adds Inlet/Outlet zone """
        new_io_zone = InletOutletZone(InletOutletZoneGeneratorType.LINE)
        info=new_io_zone.zone_info
        new_io_zone.fc_object_name = create_inout_zone_line(info.zone_line_generator, info.zone_direction_2d,
                                                           info.zone_rotation_2d)
        self.inlet_outlet.zones.append(new_io_zone)
        self.refresh_zones()
        self.zone_edit(io = new_io_zone,new=True)

    def on_add_2d_mk_zone(self):
        """ Adds Inlet/Outlet zone """
        new_io_zone = InletOutletZone(InletOutletZoneGeneratorType.MK_2D)
        self.inlet_outlet.zones.append(new_io_zone)
        self.refresh_zones()
        if self.zone_edit(io=new_io_zone, new=True):
            info = new_io_zone.zone_info
            obj_name = Case.the().get_first_fc_object_from_mk(ObjectType.FLUID, info.zone_mk_generator.mkfluid)
            new_io_zone.fc_object_name =create_inout_zone_3d_mk_object(obj_name)
            update_inout_zone_2d_mk_object(new_io_zone.fc_object_name, info.zone_mk_generator,
                                           info.zone_direction_2d,
                                           info.zone_rotation_2d,obj_name)

    def on_add_box_zone(self):
        """ Adds Inlet/Outlet zone """
        new_io_zone = InletOutletZone(InletOutletZoneGeneratorType.BOX)
        info = new_io_zone.zone_info
        new_io_zone.fc_object_name = create_inout_zone_box(info.zone_box_generator, info.zone_direction_3d,
                                                                   info.zone_rotation_3d)
        self.inlet_outlet.zones.append(new_io_zone)
        self.refresh_zones()
        self.zone_edit(io = new_io_zone,new=True)

    def on_add_circle_zone(self):
        """ Adds Inlet/Outlet zone """
        new_io_zone = InletOutletZone(InletOutletZoneGeneratorType.CIRCLE)
        info=new_io_zone.zone_info
        new_io_zone.fc_object_name = create_inout_zone_circle(info.zone_circle_generator, info.zone_direction_3d,
                                                           info.zone_rotation_3d)
        self.inlet_outlet.zones.append(new_io_zone)
        self.refresh_zones()
        self.zone_edit(io = new_io_zone,new=True)
    def on_add_3d_mk_zone(self):
        """ Adds Inlet/Outlet zone """
        new_io_zone = InletOutletZone(InletOutletZoneGeneratorType.MK_3D)

        self.inlet_outlet.zones.append(new_io_zone)
        self.refresh_zones()
        if self.zone_edit(io=new_io_zone, new=True):
            info = new_io_zone.zone_info
            obj_name = Case.the().get_first_fc_object_from_mk(ObjectType.FLUID, info.zone_mk_generator.mkfluid)
            new_io_zone.fc_object_name = create_inout_zone_3d_mk_object(obj_name)
            update_inout_zone_3d_mk_object(new_io_zone.fc_object_name,info.zone_mk_generator,
                                                                    info.zone_direction_3d,
                                                                    info.zone_rotation_3d,obj_name)

    def refresh_zones(self):
        """ Refreshes the zones list """
        self.io_zones_table.clear()
        self.io_zones_table.setRowCount(len(self.inlet_outlet.zones))

        count = 0
        for io_object in self.inlet_outlet.zones:
            io_zone_widget = InletZoneWidget(count, io_object)
            io_zone_widget.on_edit.connect(self.zone_edit)
            io_zone_widget.on_delete.connect(self.zone_delete)
            self.io_zones_table.setCellWidget(count, 0, io_zone_widget)
            count += 1

    def zone_delete(self, io):
        """ Delete one zone from the list """
        io_zone_obj_name=io.fc_object_name
        delete_group(io_zone_obj_name)
        self.inlet_outlet.zones.remove(io)
        self.refresh_zones()

    def zone_edit(self, io:InletOutletZone, new =False):
        """ Calls a window for edit zones """
        io_id=io.id
        log("Trying to open a zone edit for zone UUID {}".format(io_id))
        dialog = InletZoneEdit(io_id, parent=None)
        ret = dialog.exec()
        if ret==QDialog.Rejected and new:
            self.zone_delete(io)
            return False
        self.refresh_zones()
        return True

    def on_cancel(self):
        """ Cancels the dialog not saving anything. """
        self.reject()

    def on_ok(self):
        """ Save data """

        if not self.inlet_outlet:
            self.inlet_outlet = InletOutletConfig()

        self.inlet_outlet.memoryresize_size0 = self.memory_resize_size0_line_edit.value()
        self.inlet_outlet.memoryresize_size = self.memory_resize_size_line_edit.value()
        self.inlet_outlet.determlimit = self.determlimit_combobox.currentText()
        self.inlet_outlet.extrapolatemode = self.extrapolatemode_combobox.currentIndex() + 1
        self.inlet_outlet.refillingrate=self.refilling_rate_input.value()
        self.inlet_outlet.useboxlimit_enabled = self.useboxlimit_check.isChecked()
        InletConfigDialog.accept(self)

    def on_useboxlimit_checked(self,check):
        self.useboxlimit_freecentre_check.setEnabled(check)
        self.on_useboxlimit_freecentre_checked(self.useboxlimit_freecentre_check.isChecked())

    def on_useboxlimit_freecentre_checked(self,check):
        for x in [self.useboxlimit_freecentre_values_x_input,
                   self.useboxlimit_freecentre_values_y_input,self.useboxlimit_freecentre_values_z_input]:
            x.setEnabled(check)

    def on_advanced_options_clicked(self,checked):
        if self.advanced_options_widget.isHidden():
            self.advanced_options_widget.show()
        else:
            self.advanced_options_widget.hide()