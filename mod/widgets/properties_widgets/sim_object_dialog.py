from PySide2 import QtWidgets
from mod.dataobjects.properties.simulation_object import SimulationObject
from mod.tools.freecad_tools import get_fc_object
from mod.tools.translation_tools import __
from mod.widgets.custom_widgets.value_input import ValueInput
import FreeCAD

from mod.widgets.custom_widgets.value_input import ValueInput


class SimObjectDialog(QtWidgets.QDialog):
    def __init__(self,simobject):
        super().__init__(parent=None)
        self.data:SimulationObject=simobject
        self.sim_object_layout=QtWidgets.QVBoxLayout()
        # Autofill
        self.geo_autofil_layout = QtWidgets.QHBoxLayout()
        self.geo_autofill_chck = QtWidgets.QCheckBox(__("Autofill"))
        self.geo_autofil_layout.addWidget(self.geo_autofill_chck)

        # Scaling factor
        self.geo_scaling_widget = QtWidgets.QWidget()
        self.geo_scaling_layout = QtWidgets.QHBoxLayout()
        self.geo_scaling_label = QtWidgets.QLabel(__("Scaling factor: (X,Y,Z)"))
        self.geo_scaling_x_e = ValueInput(value=1.0)
        self.geo_scaling_y_e = ValueInput(value=1.0)
        self.geo_scaling_z_e = ValueInput(value=1.0)

        for x in [self.geo_scaling_label,
                  self.geo_scaling_x_e,
                  self.geo_scaling_y_e,
                  self.geo_scaling_z_e, ]:
            self.geo_scaling_layout.addWidget(x)
        self.geo_scaling_layout.setContentsMargins(0, 0, 0, 0)
        #self.geo_scaling_widget.setLayout(self.geo_scaling_layout)

        # Advanced Draw
        self.adv_draw_layout = QtWidgets.QHBoxLayout()
        self.adv_draw_label = QtWidgets.QLabel("Advanced Draw Mode")
        self.adv_draw_enabled_checkbox = QtWidgets.QCheckBox(__("Enabled"))
        self.adv_draw_reverse_checkbox = QtWidgets.QCheckBox(__("Reverse"))
        self.adv_draw_mindepth_checkbox = QtWidgets.QCheckBox(__("MinDepth(Dp)"))
        self.adv_draw_mindepth_input = ValueInput(value=0.1)
        self.adv_draw_maxdepth_checkbox = QtWidgets.QCheckBox(__("MaxDepth(Dp)"))
        self.adv_draw_maxdepth_input = ValueInput(value=3.0)
        for x in [self.adv_draw_label, self.adv_draw_enabled_checkbox, self.adv_draw_reverse_checkbox,
                  self.adv_draw_mindepth_checkbox, self.adv_draw_mindepth_input, self.adv_draw_maxdepth_checkbox,
                  self.adv_draw_maxdepth_input]:
            self.adv_draw_layout.addWidget(x)

        self.sim_object_layout.addLayout(self.geo_scaling_layout)
        self.sim_object_layout.addLayout(self.adv_draw_layout)
        self.sim_object_layout.addLayout(self.geo_autofil_layout)

        # Create button layout
        self.obj_button_layout = QtWidgets.QHBoxLayout()
        self.obj_button_ok = QtWidgets.QPushButton(__("Ok"))
        self.obj_button_cancel = QtWidgets.QPushButton(__("Cancel"))
        self.obj_button_layout.addStretch(1)
        self.obj_button_layout.addWidget(self.obj_button_cancel)
        self.obj_button_layout.addWidget(self.obj_button_ok)

        # Compose main window layout
        self.sim_object_layout.addLayout(self.obj_button_layout)

        self.setLayout(self.sim_object_layout)

        self.obj_button_cancel.clicked.connect(self.on_cancel)
        self.obj_button_ok.clicked.connect(self.on_ok)
        self.adv_draw_enabled_checkbox.stateChanged.connect(self.on_adv_draw_enable)
        self.adv_draw_mindepth_checkbox.stateChanged.connect(self.on_adv_draw_mindepth)
        self.adv_draw_maxdepth_checkbox.stateChanged.connect(self.on_adv_draw_maxdepth)


        self.fill_values()
    def fill_values(self):
        self.geo_autofill_chck.setChecked(self.data.autofill)
        self.geo_scaling_x_e.setValue(self.data.scale_factor[0])
        self.geo_scaling_y_e.setValue(self.data.scale_factor[1])
        self.geo_scaling_z_e.setValue(self.data.scale_factor[2])
        self.adv_draw_enabled_checkbox.setChecked(self.data.advdraw_enabled)
        self.adv_draw_reverse_checkbox.setChecked(self.data.advdraw_reverse)
        self.adv_draw_mindepth_checkbox.setChecked(self.data.advdraw_mindepth_enabled)
        self.adv_draw_maxdepth_checkbox.setChecked(self.data.advdraw_maxdepth_enabled)
        self.adv_draw_mindepth_input.setValue(self.data.advdraw_mindepth)
        self.adv_draw_maxdepth_input.setValue(self.data.advdraw_maxdepth)

        if not self.data.is_loaded_geometry:
            self.geo_scaling_x_e.setEnabled(False)
            self.geo_scaling_y_e.setEnabled(False)
            self.geo_scaling_z_e.setEnabled(False)



    def on_ok(self):
        self.data.autofill = self.geo_autofill_chck.isChecked()
        old_scale_factor=self.data.scale_factor
        self.data.scale_factor = [self.geo_scaling_x_e.value(),self.geo_scaling_y_e.value(),
                                  self.geo_scaling_z_e.value()]
        self.data.advdraw_enabled = self.adv_draw_enabled_checkbox.isChecked()
        self.data.advdraw_reverse = self.adv_draw_reverse_checkbox.isChecked()
        self.data.advdraw_mindepth_enabled = self.adv_draw_mindepth_checkbox.isChecked()
        self.data.advdraw_maxdepth_enabled = self.adv_draw_maxdepth_checkbox.isChecked()
        self.data.advdraw_mindepth = self.adv_draw_mindepth_input.value()
        self.data.advdraw_maxdepth = self.adv_draw_maxdepth_input.value()

        scale_matrix = FreeCAD.Matrix()
        scale_matrix.scale(self.data.scale_factor[0]/old_scale_factor[0], self.data.scale_factor[1]/old_scale_factor[1]
                           , self.data.scale_factor[2]/old_scale_factor[2])
        fcobj=get_fc_object(self.data.name)


        if self.data.file_type == ".vtk" or self.data.file_type == ".vtu" or self.data.file_type == ".vtp":
            new_msh = fcobj.FemMesh.copy()
            new_msh.transformGeometry(scale_matrix)
            fcobj.FemMesh = new_msh
        else:
            if self.data.is_loaded_geometry:
                new_msh = fcobj.Mesh.copy()
                new_msh.transformGeometry(scale_matrix)
                fcobj.Mesh = new_msh


        self.accept()




    def on_cancel(self):
        self.reject()


    def on_adv_draw_enable(self,state):
        for x in [self.adv_draw_reverse_checkbox,self.adv_draw_maxdepth_checkbox,self.adv_draw_mindepth_checkbox,
                  self.adv_draw_maxdepth_input,self.adv_draw_mindepth_input]:
            x.setEnabled(state)
        if state:
            self.on_adv_draw_mindepth(self.adv_draw_mindepth_checkbox.isChecked())
            self.on_adv_draw_maxdepth(self.adv_draw_maxdepth_checkbox.isChecked())
        self.geo_autofill_chck.setEnabled(not state)

    def on_adv_draw_mindepth(self,state):
        self.adv_draw_mindepth_input.setEnabled(state)

    def on_adv_draw_maxdepth(self,state):
        self.adv_draw_maxdepth_input.setEnabled(state)
