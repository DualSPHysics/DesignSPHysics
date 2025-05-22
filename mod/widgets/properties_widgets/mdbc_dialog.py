from PySide2 import QtWidgets
from mod.dataobjects.case import Case
from mod.dataobjects.properties.simulation_object import SimulationObject
from mod.tools.translation_tools import __
from mod.widgets.custom_widgets.value_input import ValueInput
from mod.widgets.custom_widgets.value_input import ValueInput


class MDBCDialog(QtWidgets.QDialog):
    def __init__(self,simobject):
        super().__init__(parent=None)
        self.data:SimulationObject=simobject
        self.mdbc_layout=QtWidgets.QVBoxLayout()

        self.use_mdbc_layout = QtWidgets.QVBoxLayout()
        self.use_mdbc_chck = QtWidgets.QCheckBox(__("Use mDBC geometry normals"))
        self.geo_distance_vdp_label = QtWidgets.QLabel(__("Geometry distance (vdp): "))
        self.geo_distance_vdp_input = ValueInput()
        self.normal_invert_chck = QtWidgets.QCheckBox(__("Invert normals"))
        self.use_mdbc_layout.addWidget(self.use_mdbc_chck)
        self.use_mdbc_layout.addWidget(self.geo_distance_vdp_label)
        self.use_mdbc_layout.addWidget(self.geo_distance_vdp_input)
        self.use_mdbc_layout.addWidget(self.normal_invert_chck)



        self.mdbc_button_layout = QtWidgets.QHBoxLayout()
        self.mdbc_button_ok = QtWidgets.QPushButton(__("Ok"))
        self.mdbc_button_layout.addWidget(self.mdbc_button_ok)
        self.mdbc_button_ok.clicked.connect(self.on_ok)

        # Compose main window layout
        self.mdbc_layout.addLayout(self.use_mdbc_layout)
        self.mdbc_layout.addLayout(self.mdbc_button_layout)

        self.setLayout(self.mdbc_layout)

        self.fill_values()
    def fill_values(self):
        self.use_mdbc_chck.setChecked(self.data.use_mdbc)
        self.geo_distance_vdp_input.setValue(self.data.mdbc_dist_vdp)
        self.normal_invert_chck.setChecked(self.data.mdbc_normal_invert)
    def on_ok(self):
        self.data.use_mdbc=self.use_mdbc_chck.isChecked()
        self.data.mdbc_dist_vdp=self.geo_distance_vdp_input.value()
        self.data.mdbc_normal_invert=self.normal_invert_chck.isChecked()
        self.accept()

    def on_cancel(self):
        self.reject()

