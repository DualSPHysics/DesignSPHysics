from PySide2 import QtWidgets
from mod.dataobjects.case import Case
from mod.tools.dialog_tools import warning_dialog
from mod.tools.stdout_tools import debug
from mod.tools.translation_tools import __
from mod.widgets.custom_widgets.size_input import SizeInput
from mod.widgets.custom_widgets.value_input import ValueInput


class FlowToolXmlBoxDialog(QtWidgets.QDialog):
    """ A widget to show options for the Box zone generator. """

    def __init__(self,box_id,parent):
        super().__init__(parent)
        for box in Case.the().post_processing_settings.flowtool_xml_boxes:
            if box.id == box_id:
                self.box = box
        self.main_layout = QtWidgets.QVBoxLayout()
        self.setLayout(self.main_layout)

        self.box_edit_name_layout = QtWidgets.QHBoxLayout()
        self.box_edit_name_label = QtWidgets.QLabel(__("Box Name"))
        self.box_edit_name_input = QtWidgets.QLineEdit(self.box.name)
        self.box_edit_name_layout.addWidget(self.box_edit_name_label)
        self.box_edit_name_layout.addWidget(self.box_edit_name_input)


        self.point_layout = QtWidgets.QHBoxLayout()

        self.point_label = QtWidgets.QLabel(__("Start [X, Y, Z]"))
        self.point_value_x = SizeInput()
        self.point_value_y = SizeInput()
        self.point_value_z = SizeInput()
        self.point_layout.addWidget(self.point_label)
        self.point_layout.addWidget(self.point_value_x)
        self.point_layout.addWidget(self.point_value_y)
        self.point_layout.addWidget(self.point_value_z)

        self.size_layout = QtWidgets.QHBoxLayout()
        self.size_label = QtWidgets.QLabel(__("Size [X, Y, Z]"))
        self.size_value_x = SizeInput()
        self.size_value_y = SizeInput()
        self.size_value_z = SizeInput()
        self.size_layout.addWidget(self.size_label)
        self.size_layout.addWidget(self.size_value_x)
        self.size_layout.addWidget(self.size_value_y)
        self.size_layout.addWidget(self.size_value_z)

        self.angle_layout = QtWidgets.QHBoxLayout()
        self.angle_label = QtWidgets.QLabel(__("Angle [X, Y, Z]"))
        self.angle_value_x = ValueInput()
        self.angle_value_y = ValueInput()
        self.angle_value_z = ValueInput()
        self.angle_layout.addWidget(self.angle_label)
        self.angle_layout.addWidget(self.angle_value_x)
        self.angle_layout.addWidget(self.angle_value_y)
        self.angle_layout.addWidget(self.angle_value_z)

        self.boxdiv_layout=QtWidgets.QHBoxLayout()
        self.divide_checkbox=QtWidgets.QCheckBox(__("Divide Box"))
        self.divide_axis_label=QtWidgets.QLabel("Divide axis")
        self.divide_axis_combo=QtWidgets.QComboBox()
        self.divide_axis_combo.addItems(["X","Y","Z"])
        self.boxdiv_layout.addWidget(self.divide_checkbox)
        self.boxdiv_layout.addWidget(self.divide_axis_label)
        self.boxdiv_layout.addWidget(self.divide_axis_combo)

        self.buttons_layout=QtWidgets.QHBoxLayout()
        self.save_button = QtWidgets.QPushButton(__("Save"))
        self.cancel_button = QtWidgets.QPushButton(__("Cancel"))
        self.buttons_layout.addWidget(self.save_button)
        self.buttons_layout.addWidget(self.cancel_button)

        self.save_button.clicked.connect(self.save)

        self.main_layout.addLayout(self.box_edit_name_layout)
        self.main_layout.addLayout(self.point_layout)
        self.main_layout.addLayout(self.size_layout)
        self.main_layout.addLayout(self.angle_layout)
        self.main_layout.addLayout(self.boxdiv_layout)
        self.main_layout.addLayout(self.buttons_layout)

        self.fill_values()

    def fill_values(self):

        self.point_value_x.setValue(self.box.point[0])
        self.point_value_y.setValue(self.box.point[1])
        self.point_value_z.setValue(self.box.point[2])
        self.size_value_x.setValue(self.box.size[0])
        self.size_value_y.setValue(self.box.size[1])
        self.size_value_z.setValue(self.box.size[2])
        self.angle_value_x.setValue(self.box.angle[0])
        self.angle_value_y.setValue(self.box.angle[1])
        self.angle_value_z.setValue(self.box.angle[2])
        self.divide_checkbox.setChecked(self.box.divide_axis)
        index=0
        if self.box.axis=="X":
            index=0
        elif self.box.axis=="Y":
            index=1
        elif self.box.axis == "Z":
            index = 2
        self.divide_axis_combo.setCurrentIndex(index)

    def save(self):
        self.box.point[0]=self.point_value_x.value()
        self.box.point[1] = self.point_value_y.value()
        self.box.point[2] = self.point_value_z.value()
        self.box.size[0] = self.size_value_x.value()
        self.box.size[1] = self.size_value_y.value()
        self.box.size[2] = self.size_value_z.value()
        self.box.angle[0] = self.angle_value_x.value()
        self.box.angle[1] = self.angle_value_y.value()
        self.box.angle[2] = self.angle_value_z.value()
        self.box.divide_axis =self.divide_checkbox.isChecked()
        self.box.axis=["X","Y","Z"][self.divide_axis_combo.currentIndex()]

        for box in Case.the().post_processing_settings.flowtool_xml_boxes:
            if box.id != self.box.id and box.name==self.box_edit_name_input.text():
                warning_dialog("There is already a flowbox with this name. Names must be unique")
                return
        self.box.name=self.box_edit_name_input.text()


        self.accept()

