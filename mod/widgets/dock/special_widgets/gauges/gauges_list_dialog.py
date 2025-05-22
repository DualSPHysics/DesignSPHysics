from PySide2 import QtWidgets
from mod.constants import GAUGES_GROUP_NAME, GAUGES_COLOR
from mod.dataobjects.case import Case
from mod.dataobjects.gauges.force_gauge import ForceGauge
from mod.dataobjects.gauges.gauge_base import Gauge
from mod.dataobjects.gauges.max_z_gauge import MaxZGauge
from mod.dataobjects.gauges.mesh_gauge import MeshGauge
from mod.dataobjects.gauges.swl_gauge import SWLGauge
from mod.dataobjects.gauges.velocity_gauge import VelocityGauge
from mod.tools.dialog_tools import info_dialog
from mod.tools.freecad_tools import delete_object, draw_line, get_fc_object, draw_sphere, \
    create_mesh_gauge_box, delete_group, create_flow_gauge_box
from mod.tools.freecad_tools import manage_gauges
from mod.tools.translation_tools import __
from mod.widgets.dock.special_widgets.gauges.defaults_gauge_dialog import GaugeDefaultsDialog
from mod.widgets.dock.special_widgets.gauges.flow_gauge_dialog import FlowGaugeDialog
from mod.widgets.dock.special_widgets.gauges.force_gauge_dialog import ForceGaugeDialog
from mod.widgets.dock.special_widgets.gauges.max_z_gauge_dialog import MaxZGaugeDialog
from mod.widgets.dock.special_widgets.gauges.mesh_gauge_dialog import MeshGaugeDialog
from mod.widgets.dock.special_widgets.gauges.swl_gauge_dialog import SWLGaugeDialog
from mod.widgets.dock.special_widgets.gauges.velocity_gauge_dialog import VelocityGaugeDialog


class GaugesListDialog(QtWidgets.QDialog):

    def __init__(self, parent):
        super().__init__(parent=parent)

        self.setWindowTitle(__("Gauges list"))
        self.main_layout = QtWidgets.QVBoxLayout()

        self.list_layout = QtWidgets.QHBoxLayout()
        self.gauges_list = QtWidgets.QListWidget()
        self.list_layout.addWidget(self.gauges_list)

        self.buttons_layout = QtWidgets.QHBoxLayout()
        self.add_gauge_button = QtWidgets.QPushButton(__("Add gauge"))
        self.add_gauge_menu = QtWidgets.QMenu()
        self.add_gauge_menu.addAction(__("Add velocity gauge"))
        self.add_gauge_menu.addAction(__("Add zmax gauge"))
        self.add_gauge_menu.addAction(__("Add swl gauge"))
        self.add_gauge_menu.addAction(__("Add force gauge"))
        self.add_gauge_menu.addAction(__("Add mesh gauge"))
        self.add_gauge_button.setMenu(self.add_gauge_menu)
        self.add_gauge_menu.triggered.connect(self.on_add_gauge_menu)
        self.edit_gauge_button = QtWidgets.QPushButton(__("Edit gauge"))
        self.edit_gauge_button.clicked.connect(self.on_edit)
        self.delete_gauge_button = QtWidgets.QPushButton(__("Delete gauge"))
        self.delete_gauge_button.clicked.connect(self.on_delete)
        self.ok_button = QtWidgets.QPushButton(text=__("OK"))
        self.ok_button.clicked.connect(self.on_ok)
        self.buttons_layout.addWidget(self.add_gauge_button)
        self.buttons_layout.addWidget(self.edit_gauge_button)
        self.buttons_layout.addWidget(self.delete_gauge_button)
        self.buttons_layout.addWidget(self.ok_button)

        self.gauges_list.itemSelectionChanged.connect(self.on_selection_change)
        self.edit_gauge_button.setEnabled(False)
        self.delete_gauge_button.setEnabled(False)

        self.main_layout.addLayout(self.list_layout)
        self.main_layout.addLayout(self.buttons_layout)
        self.setLayout(self.main_layout)

        manage_gauges(Case.the().gauges.gauges_dict)
        self.update_gauges_list()

    def on_ok(self):
        self.accept()


    def on_add_gauge_menu(self, action):
        """ Defines damping menu behaviour"""
        new_object_name=""
        if __("Add velocity gauge") in action.text():
            new_gauge = VelocityGauge()
            new_gauge.load_defaults(Case.the().gauges.gauges_dict["Defaults"])
            new_gauge.fc_object_name = draw_sphere(center=new_gauge.point0, radius=0.01, name="Helper_VelocityGauge",color=GAUGES_COLOR)
            get_fc_object(GAUGES_GROUP_NAME).addObject(get_fc_object(new_gauge.fc_object_name))
            get_fc_object(new_gauge.fc_object_name).addProperty("App::PropertyVector", "lastposition")
            dialog = VelocityGaugeDialog(velocity_gauge=new_gauge, parent=None)
            ret=dialog.exec_()
        elif __("Add zmax gauge") in action.text():
            new_gauge = MaxZGauge()
            new_gauge.load_defaults(Case.the().gauges.gauges_dict["Defaults"])
            new_gauge.fc_object_name = draw_line(point1=new_gauge.point0, point2=new_gauge.point0,name="Helper_MaxZGauge",color=GAUGES_COLOR)
            get_fc_object(GAUGES_GROUP_NAME).addObject(get_fc_object(new_gauge.fc_object_name))
            get_fc_object(new_gauge.fc_object_name).addProperty("App::PropertyVector", "lastposition")
            dialog = MaxZGaugeDialog(max_z_gauge=new_gauge, parent=None)
            ret=dialog.exec_()
        elif __("Add swl gauge") in action.text():
            new_gauge = SWLGauge()
            new_gauge.load_defaults(Case.the().gauges.gauges_dict["Defaults"])
            new_gauge.fc_object_name = draw_line(point1=new_gauge.point0, point2=new_gauge.point1, name="Helper_SWLGauge",color=GAUGES_COLOR)
            get_fc_object(GAUGES_GROUP_NAME).addObject(get_fc_object(new_gauge.fc_object_name))
            get_fc_object(new_gauge.fc_object_name).addProperty("App::PropertyVector", "lastposition")
            dialog = SWLGaugeDialog(swl_gauge=new_gauge, parent=None)
            ret=dialog.exec_()
        elif __("Add force gauge") in action.text():
            new_gauge = ForceGauge()
            new_gauge.load_defaults(Case.the().gauges.gauges_dict["Defaults"])
            dialog = ForceGaugeDialog(force_gauge=new_gauge, parent=None)
            ret=dialog.exec_()
        elif __("Add mesh gauge") in action.text():
            new_gauge = MeshGauge()
            new_gauge.load_defaults(Case.the().gauges.gauges_dict["Defaults"])
            new_gauge.fc_object_name=create_mesh_gauge_box(new_gauge)
            get_fc_object(GAUGES_GROUP_NAME).addObject(get_fc_object(new_gauge.fc_object_name))
            get_fc_object(new_gauge.fc_object_name).addProperty("App::PropertyVector", "lastposition")
            dialog = MeshGaugeDialog(mesh_gauge=new_gauge, parent=None)
            ret=dialog.exec_()
        if ret== QtWidgets.QDialog.Accepted:
            if new_gauge.name == "Defaults":
                info_dialog("New gauge cannot be named 'Defaults'")
            else:
                Case.the().gauges.add_gauge(new_gauge)
        else:
            if new_gauge.type=="mesh" or new_gauge.type=="flow":
                delete_group(new_gauge.fc_object_name)
            else:
                delete_object(new_gauge.fc_object_name)
        self.update_gauges_list()

    def update_gauges_list(self):
        self.gauges_list.clear()
        for name, gauge in Case.the().gauges.gauges_dict.items():
            self.gauges_list.addItem(name)
        self.gauges_list.setCurrentRow(0)

    def on_edit(self):
        key = self.gauges_list.currentItem().text()
        gauge = Case.the().gauges.gauges_dict[key]
        if gauge.__class__ == VelocityGauge:
            dialog = VelocityGaugeDialog(velocity_gauge=gauge, parent=None)
            dialog.exec_()
        elif gauge.__class__ == MaxZGauge:
            dialog = MaxZGaugeDialog(max_z_gauge=gauge, parent=None)
            dialog.exec_()
        elif gauge.__class__ == SWLGauge:
            dialog = SWLGaugeDialog(swl_gauge=gauge, parent=None)
            dialog.exec_()
        elif gauge.__class__ == ForceGauge:
            dialog = ForceGaugeDialog(force_gauge=gauge, parent=None)
            dialog.exec_()
        elif gauge.__class__ == MeshGauge:
            dialog = MeshGaugeDialog(mesh_gauge=gauge, parent=None)
            dialog.exec_()
        elif gauge.__class__ == Gauge:
            dialog = GaugeDefaultsDialog(base_gauge=gauge, parent=None)
            dialog.exec_()
        self.update_gauges_list()

    def on_delete(self):
        key = self.gauges_list.currentItem().text()
        if key == "Defaults":
            info_dialog("Gauge defaults cannot be deleted.")
        else:
            if Case.the().gauges.gauges_dict[key].type=="mesh" or Case.the().gauges.gauges_dict[key].type=="flow":
                delete_group(Case.the().gauges.gauges_dict[key].fc_object_name)
            else:
                delete_object(Case.the().gauges.gauges_dict[key].fc_object_name)
            Case.the().gauges.remove_gauge(key)
        self.update_gauges_list()

    def on_selection_change(self):
        if self.gauges_list.selectedItems():
            self.edit_gauge_button.setEnabled(True)
            self.delete_gauge_button.setEnabled(True)
        else:
            self.edit_gauge_button.setEnabled(False)
            self.delete_gauge_button.setEnabled(False)
