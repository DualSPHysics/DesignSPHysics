from PySide2.QtWidgets import QHBoxLayout

from PySide2 import QtWidgets
from mod.tools.freecad_tools import delete_object
from mod.tools.translation_tools import __
from mod.widgets.custom_widgets.value_input import ValueInput
from mod.widgets.custom_widgets.time_input import TimeInput


class BaseGaugeDialog(QtWidgets.QDialog):

    def __init__(self, base_gauge, parent):
        super().__init__(parent=parent)
        self.data = base_gauge


        self.main_layout = QtWidgets.QVBoxLayout()

        self.name_layout = QHBoxLayout()
        self.name_label = QtWidgets.QLabel(__("Gauge name"))
        self.name_input = QtWidgets.QLineEdit()
        self.name_layout.addWidget(self.name_label)
        self.name_layout.addWidget(self.name_input)

        self.compute_layout = QHBoxLayout()
        self.compute_dt_label = QtWidgets.QLabel(__("Compute dt"))
        self.compute_dt_input = TimeInput()
        self.compute_time_label = QtWidgets.QLabel(__("Compute time (start, end)"))
        self.compute_time_start_input = TimeInput()
        self.compute_time_end_input = TimeInput()
        for x in [ self.compute_dt_label,
                  self.compute_dt_input, self.compute_time_label, self.compute_time_start_input,
                  self.compute_time_end_input]:
            self.compute_layout.addWidget(x)

        self.output_layout = QHBoxLayout()
        self.output_dt_label = QtWidgets.QLabel(__("Output dt"))
        self.output_dt_input = TimeInput()
        self.output_time_label = QtWidgets.QLabel(__("Output time (start, end)"))
        self.output_time_start_input = TimeInput()
        self.output_time_end_input = TimeInput()
        for x in [ self.output_dt_label,
                  self.output_dt_input, self.output_time_label, self.output_time_start_input,
                  self.output_time_end_input]:
            self.output_layout.addWidget(x)

        self.save_layout =QHBoxLayout()
        self.save_vtk_part_label = QtWidgets.QLabel(__("Save vtk"))
        self.save_vtk_part_checkbox = QtWidgets.QCheckBox()
        self.save_csv_label = QtWidgets.QLabel(__("Save csv"))
        self.save_csv_checkbox = QtWidgets.QCheckBox()
        for x in [self.save_vtk_part_label, self.save_vtk_part_checkbox,self.save_csv_label,
                  self.save_csv_checkbox]:
            self.save_layout.addWidget(x)
        self.buttons_layout = QHBoxLayout()
        self.ok_button = QtWidgets.QPushButton(text=__("OK"))
        self.ok_button.clicked.connect(self.save_data)
        self.buttons_layout.addWidget(self.ok_button)

        self.main_layout.addLayout(self.name_layout)
        self.main_layout.addLayout(self.compute_layout)
        self.main_layout.addLayout(self.output_layout)
        self.main_layout.addLayout(self.save_layout)

        self.main_layout.addLayout(self.buttons_layout)
        self.setLayout(self.main_layout)

    def fill_values(self):
        if self.data.name != "":
            self.name_input.setText(self.data.name)
            self.name_input.setEnabled(False)
        self.save_vtk_part_checkbox.setChecked(self.data.save_vtk_part)
        self.compute_dt_input.setValue(self.data.compute_dt)
        self.compute_time_start_input.setValue(self.data.compute_time_start)
        self.compute_time_end_input.setValue(self.data.compute_time_end)
        self.save_csv_checkbox.setChecked(self.data.output)
        self.output_dt_input.setValue(self.data.output_dt)
        self.output_time_start_input.setValue(self.data.output_time_start)
        self.output_time_end_input.setValue(self.data.output_time_end)

    def save_data(self):
        self.data.save_vtk_part = self.save_vtk_part_checkbox.isChecked()
        self.data.compute_dt = self.compute_dt_input.value()
        self.data.compute_time_start = self.compute_time_start_input.value()
        self.data.compute_time_end = self.compute_time_end_input.value()
        self.data.output = self.save_csv_checkbox.isChecked()
        self.data.output_dt = self.output_dt_input.value()
        self.data.output_time_start = self.output_time_start_input.value()
        self.data.output_time_end = self.output_time_end_input.value()
        self.data.name = self.name_input.text()
#        delete_object(self.data.fc_object_name)

    def closeEvent(self, evnt):
        #evnt.ignore()
        pass

