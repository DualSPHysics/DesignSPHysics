from PySide2.QtWidgets import QHBoxLayout

from PySide2 import QtWidgets, QtCore
from mod.dataobjects.case import Case
from mod.dataobjects.configuration.simulation_domain import SimulationDomain
from mod.dataobjects.variable_res.bufferbox import BufferBox
from mod.enums import ObjectType
from mod.tools.dialog_tools import warning_dialog
from mod.tools.freecad_tools import create_vres_buffer_box, delete_object, update_vres_buffer_box
from mod.tools.stdout_tools import debug
from mod.tools.translation_tools import __
from mod.tools.dialog_tools import error_dialog, warning_dialog
from mod.widgets.dock.dock_widgets.simulation_domain_widget import SimulationDomainWidget
from mod.widgets.custom_widgets.value_input import ValueInput

from mod.widgets.custom_widgets.int_value_input import IntValueInput
from mod.widgets.custom_widgets.mk_select_input_with_names import MkSelectInputWithNames
from mod.widgets.custom_widgets.size_input import SizeInput
from mod.widgets.custom_widgets.value_input import ValueInput


class BufferboxEditDialog(QtWidgets.QDialog):

    WIDTH=800
    def __init__(self, bufferbox: BufferBox, parent,wavegenavail=True):
        super().__init__(parent=parent)
        self.data = bufferbox
        self.wavegenavail = wavegenavail
        self.bufferbox_scroll = QtWidgets.QScrollArea()
        self.bufferbox_scroll.setMinimumWidth(self.WIDTH)
        self.bufferbox_scroll.setWidgetResizable(True)
        self.bufferbox_scroll_widget = QtWidgets.QWidget()
        #self.bufferbox_scroll_widget.setMinimumWidth(self.WIDTH)

        self.bufferbox_scroll.setWidget(self.bufferbox_scroll_widget)
        self.bufferbox_scroll.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)


        self.bufferbox_layout = QtWidgets.QVBoxLayout()
        self.bufferbox_scroll_widget.setLayout(self.bufferbox_layout)

        self.setWindowTitle(__("Variable resolution bufferbox edit"))
        self.main_layout = QtWidgets.QVBoxLayout()

        self.id_layout = QtWidgets.QHBoxLayout()
        self.id_label = QtWidgets.QLabel(f"Id : {self.data.id}")
        self.active_checkbox = QtWidgets.QCheckBox(__("Active"))
        self.active_checkbox.stateChanged.connect(self.on_active_changed)
        self.id_layout.addWidget(self.id_label)
        self.id_layout.addWidget(self.active_checkbox)

        self.vreswavegen_layout = QtWidgets.QHBoxLayout()
        self.vreswavegen_label = QtWidgets.QLabel(f"Wave Generation active: {self.data.vreswavegen}")
        self.vreswavegen_checkbox = QtWidgets.QCheckBox(__("Active"))
        self.vreswavegen_checkbox.stateChanged.connect(self.on_active_changed)
        self.vreswavegen_layout.addWidget(self.vreswavegen_label)
        self.vreswavegen_layout.addWidget(self.vreswavegen_checkbox)

        self.manual_placement_layout=QtWidgets.QHBoxLayout()
        self.manual_placement_label=QtWidgets.QLabel(__("Placement: "))
        self.manual_placement_combo = QtWidgets.QComboBox()
        self.manual_placement_combo.addItems(["Parametric","Manual"])
        self.manual_placement_layout.addWidget(self.manual_placement_label)
        self.manual_placement_layout.addWidget(self.manual_placement_combo)
        self.manual_placement_combo.currentIndexChanged.connect(self.on_change_manual)


        self.place_layout = QHBoxLayout()
        self.point_label = QtWidgets.QLabel(__("Point (X,Y,Z)"))
        self.point_x_input = SizeInput()
        self.point_y_input = SizeInput()
        self.point_z_input = SizeInput()
        for x in [self.point_label, self.point_x_input, self.point_y_input, self.point_z_input, ]:
            self.place_layout.addWidget(x)

        self.size_layout = QHBoxLayout()
        self.size_label = QtWidgets.QLabel(__("Size (X,Y,Z)"))
        self.size_x_input = SizeInput()
        self.size_y_input = SizeInput()
        self.size_z_input = SizeInput()
        for x in [self.size_label, self.size_x_input, self.size_y_input, self.size_z_input]:
            self.size_layout.addWidget(x)

        self.transform_layout = QtWidgets.QVBoxLayout()

        self.transform_move_layout = QHBoxLayout()
        self.transform_move_label = QtWidgets.QLabel(__("Move (X,Y,Z)"))
        self.transform_move_x_input = SizeInput()
        self.transform_move_y_input = SizeInput()
        self.transform_move_z_input = SizeInput()
        for x in [self.transform_move_label, self.transform_move_x_input, self.transform_move_y_input,
                  self.transform_move_z_input, ]:
            self.transform_move_layout.addWidget(x)

        self.transform_rotate_layout = QHBoxLayout()
        self.transform_rotate_label = QtWidgets.QLabel(__("Rotate (X,Y,Z)"))
        self.transform_rotate_x_input = ValueInput()
        self.transform_rotate_y_input = ValueInput()
        self.transform_rotate_z_input = ValueInput()
        self.transform_rotate_angunits_combo = QtWidgets.QComboBox()
        self.transform_rotate_angunits_combo.addItems(["degrees", "radians"])
        for x in [self.transform_rotate_label, self.transform_rotate_angunits_combo, self.transform_rotate_x_input,
                  self.transform_rotate_y_input, self.transform_rotate_z_input]:
            self.transform_rotate_layout.addWidget(x)

        self.transform_center_layout = QHBoxLayout()
        self.transform_center_label = QtWidgets.QLabel(__("Center (X,Y,Z)"))
        self.transform_center_x_input = SizeInput()
        self.transform_center_y_input = SizeInput()
        self.transform_center_z_input = SizeInput()
        for x in [self.transform_center_label, self.transform_center_x_input,
                  self.transform_center_y_input, self.transform_center_z_input, ]:
            self.transform_center_layout.addWidget(x)

        self.transform_layout.addLayout(self.transform_move_layout)
        self.transform_layout.addLayout(self.transform_rotate_layout)
        self.transform_layout.addLayout(self.transform_center_layout)

        self.transform_groupbox = QtWidgets.QGroupBox("Transform")
        self.transform_groupbox.setCheckable(True)
        self.transform_groupbox.setLayout(self.transform_layout)

        self.conf_layout = QHBoxLayout()
        self.dp_ratio_label = QtWidgets.QLabel(__("Dp_ratio"))
        self.dp_ratio_input = ValueInput()
        self.buffer_size_label = QtWidgets.QLabel(__("Buffer size (h)"))
        self.buffer_size_input = IntValueInput()
        self.overlapping_h_label = QtWidgets.QLabel(__("Overlapping h"))
        self.overlapping_h_input = ValueInput()
        for x in [self.dp_ratio_label, self.dp_ratio_input, self.buffer_size_label, self.buffer_size_input,
                  self.overlapping_h_label, self.overlapping_h_input, ]:
            self.conf_layout.addWidget(x)
        self.tracking_layout = QHBoxLayout()
        self.tracking_active_checkbox = QtWidgets.QCheckBox(__("Tracking Active"))
        self.tracking_label = QtWidgets.QLabel(__("Tracking MkBound"))
        self.tracking_mk_input = MkSelectInputWithNames(ObjectType.BOUND)
        for x in [self.tracking_active_checkbox, self.tracking_label, self.tracking_mk_input]:
            self.tracking_layout.addWidget(x)
        self.parent_layout = QHBoxLayout()
        self.parent_label = QtWidgets.QLabel(__("Parent:"))
        self.parent_combo = QtWidgets.QComboBox()
        self.parent_combo.addItem("None")

        descendance = Case.the().vres.get_descendance(self.data.id)
        descendance.append(self.data)
        descendance_ids = []

        for buff in descendance:
            descendance_ids.append(buff.id)
        for bf in Case.the().vres.bufferbox_list:
            if bf.id not in descendance_ids:
                self.parent_combo.addItem(str(bf.id))

        for x in [self.parent_label, self.parent_combo]:
            self.parent_layout.addWidget(x)

        if hasattr(self.data,'domain'): #Compatibility with previous version
            self.simdomain_widget=SimulationDomainWidget(self.data.domain,True)
        else:
            warning_dialog("Case from a previous version .You will need to setup your domain")
            self.data.domain=SimulationDomain()
            self.simdomain_widget = SimulationDomainWidget(self.data.domain, True)


        self.buttons_layout = QHBoxLayout()
        self.ok_button = QtWidgets.QPushButton(text=__("OK"))
        self.ok_button.clicked.connect(self.save_data)
        self.buttons_layout.addWidget(self.ok_button)

        self.bufferbox_layout.addLayout(self.id_layout)
        self.bufferbox_layout.addLayout(self.vreswavegen_layout)
        self.bufferbox_layout.addLayout(self.manual_placement_layout)

        self.bufferbox_layout.addLayout(self.place_layout)
        self.bufferbox_layout.addLayout(self.size_layout)
        self.bufferbox_layout.addWidget(self.transform_groupbox)
        self.bufferbox_layout.addLayout(self.conf_layout)
        self.bufferbox_layout.addLayout(self.tracking_layout)
        self.bufferbox_layout.addLayout(self.parent_layout)
        self.bufferbox_layout.addWidget(self.simdomain_widget)

        self.main_layout.addWidget(self.bufferbox_scroll)
        self.main_layout.addLayout(self.buttons_layout)
        self.setLayout(self.main_layout)

        self.fill_values()

    def fill_values(self):

        self.active_checkbox.setChecked(self.data.active)

        self.vreswavegen_checkbox.setChecked(self.data.vreswavegen)

        self.manual_placement_combo.setCurrentIndex(1 if self.data.manual_placement else 0)

        self.point_x_input.setValue(self.data.point[0])
        self.point_y_input.setValue(self.data.point[1])
        self.point_z_input.setValue(self.data.point[2])
        self.size_x_input.setValue(self.data.size[0])
        self.size_y_input.setValue(self.data.size[1])
        self.size_z_input.setValue(self.data.size[2])

        self.transform_groupbox.setChecked(self.data.transform_enabled)
        self.transform_move_x_input.setValue(self.data.transform_move[0])
        self.transform_move_y_input.setValue(self.data.transform_move[1])
        self.transform_move_z_input.setValue(self.data.transform_move[2])

        self.transform_rotate_angunits_combo.setCurrentIndex(1 if self.data.transform_rotate_radians else 0)
        self.transform_rotate_x_input.setValue(self.data.transform_rotate[0])
        self.transform_rotate_y_input.setValue(self.data.transform_rotate[1])
        self.transform_rotate_z_input.setValue(self.data.transform_rotate[2])

        self.transform_center_x_input.setValue(self.data.transform_center[0])
        self.transform_center_y_input.setValue(self.data.transform_center[1])
        self.transform_center_z_input.setValue(self.data.transform_center[2])

        self.dp_ratio_input.setValue(self.data.dp_ratio)
        self.buffer_size_input.setValue(self.data.buffer_size_h)
        self.overlapping_h_input.setValue(self.data.overlapping_h)
        self.tracking_active_checkbox.setChecked(self.data.tracking_active)
        self.tracking_mk_input.set_mk_index(self.data.tracking_mkbound)
        if self.data.parent is not None:
            id = self.parent_combo.findText(str(self.data.parent.id))
            self.parent_combo.setCurrentIndex(id)
        else:
            self.parent_combo.setCurrentIndex(0)

    def save_data(self):
        self.data.active = self.active_checkbox.isChecked()

        self.data.vreswavegen = self.vreswavegen_checkbox.isChecked()

        self.data.manual_placement = (self.manual_placement_combo.currentIndex()==1)
        self.data.point[0] = self.point_x_input.value()
        self.data.point[1] = self.point_y_input.value()
        self.data.point[2] = self.point_z_input.value()
        self.data.size[0] = self.size_x_input.value()
        self.data.size[1] = self.size_y_input.value()
        self.data.size[2] = self.size_z_input.value()
        self.data.dp_ratio = self.dp_ratio_input.value()
        self.data.buffer_size_h = self.buffer_size_input.value()
        self.data.overlapping_h = self.overlapping_h_input.value()
        self.data.tracking_active = self.tracking_active_checkbox.isChecked()
        self.data.tracking_mkbound = self.tracking_mk_input.get_mk_value()
        parent = self.parent_combo.currentText()
        if parent != "None":
            self.data.parent = Case.the().vres.bufferbox_list[int(self.parent_combo.currentText())]
            self.data.depth = self.data.parent.depth + 1
        else:
            self.data.parent = None
            self.data.depth = 0
        self.data.transform_enabled = self.transform_groupbox.isChecked()
        mult=1 if self.data.transform_enabled else 0
        self.data.transform_move[0] = self.transform_move_x_input.value()*mult
        self.data.transform_move[1] = self.transform_move_y_input.value()*mult
        self.data.transform_move[2] = self.transform_move_z_input.value()*mult
        self.data.transform_rotate_radians = self.transform_rotate_angunits_combo.currentIndex() == 1
        self.data.transform_rotate[0] = self.transform_rotate_x_input.value()*mult
        self.data.transform_rotate[1] = self.transform_rotate_y_input.value()*mult
        self.data.transform_rotate[2] = self.transform_rotate_z_input.value()*mult
        self.data.transform_center[0] = self.transform_center_x_input.value()*mult
        self.data.transform_center[1] = self.transform_center_y_input.value()*mult
        self.data.transform_center[2] = self.transform_center_z_input.value()*mult
        self.data.domain=self.simdomain_widget.save()
        update_vres_buffer_box(self.data)
        
        if not self.is_valid():
            error_dialog(__("Wave generation is not allowed for multiple domains yet. Disable other buffer boxes with wave generation enabled."))
            return -1
        
        self.accept()

    def on_change_manual(self):
        enable=self.manual_placement_combo.currentIndex()==0
        self.transform_groupbox.setEnabled(enable)
        for x in [self.point_x_input,self.point_y_input,self.point_z_input,
                  self.size_x_input,self.size_y_input,self.size_z_input,]:
            x.setEnabled(enable)

    def on_active_changed(self,active:bool):
        for x in [self.point_x_input,self.point_y_input,self.point_z_input,self.size_x_input,self.size_y_input,self.size_z_input,
                  self.dp_ratio_input,self.buffer_size_input,self.overlapping_h_input,self.tracking_mk_input,self.tracking_active_checkbox,
                    self.manual_placement_combo,self.parent_combo,   self.transform_groupbox]:
            x.setEnabled(active)
        if active:
            self.on_change_manual()

    def is_valid(self):
        if not self.wavegenavail and self.data.vreswavegen:
            return False
        return True