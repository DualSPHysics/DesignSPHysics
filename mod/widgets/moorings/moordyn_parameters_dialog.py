#!/usr/bin/env python3.7
# -*- coding: utf-8 -*-
""" DesignSPHysics MoorDyn Parameters Configuration Dialog. """

from uuid import UUID

from PySide import QtGui, QtCore

from mod.translation_tools import __
from mod.enums import ObjectType
from mod.gui_tools import get_icon
from mod.stdout_tools import debug

from mod.dataobjects.moorings.moordyn.moordyn_configuration import MoorDynConfiguration
from mod.dataobjects.moorings.moordyn.moordyn_line import MoorDynLine


class MoorDynBodyWidget(QtGui.QWidget):
    """ Widget to embed in each element of the body list for the MoorDyn configuration dialog. """

    configure_clicked = QtCore.Signal(int)

    def __init__(self, obj_type: ObjectType, mk: int):
        super().__init__()
        self.root_layout: QtGui.QHBoxLayout = QtGui.QHBoxLayout()
        self.mk = mk

        self.mk_label: QtGui.QLabel = QtGui.QLabel("{} - <b>{}</b>".format(obj_type.capitalize(), str(self.mk)))

        self.configure_button: QtGui.QPushButton = QtGui.QPushButton(__("Configure"))

        self.root_layout.addWidget(self.mk_label)
        self.root_layout.addStretch(1)
        self.root_layout.addWidget(self.configure_button)

        self.configure_button.clicked.connect(lambda _=False, mk=self.mk: self.configure_clicked.emit(mk))

        self.setLayout(self.root_layout)


class MoorDynLineWidget(QtGui.QWidget):
    """ Widget to embed in each element of the line list for the MoorDyn configuration dialog. """

    configure_clicked = QtCore.Signal(UUID)
    delete_clicked = QtCore.Signal(UUID)

    def __init__(self, line_id):
        super().__init__()
        self.root_layout: QtGui.QHBoxLayout = QtGui.QHBoxLayout()

        self.line_id = line_id

        self.label: QtGui.QLabel = QtGui.QLabel("Line {}".format(self.line_id))

        self.configure_button: QtGui.QPushButton = QtGui.QPushButton(__("Configure"))
        self.delete_button = QtGui.QPushButton(get_icon("trash.png"), None)

        self.root_layout.addWidget(self.label)
        self.root_layout.addStretch(1)
        self.root_layout.addWidget(self.configure_button)
        self.root_layout.addWidget(self.delete_button)

        self.configure_button.clicked.connect(lambda _=False, line_id=self.line_id: self.configure_clicked.emit(line_id))
        self.delete_button.clicked.connect(lambda _=False, line_id=self.line_id: self.delete_clicked.emit(line_id))

        self.setLayout(self.root_layout)


class MoorDynParametersDialog(QtGui.QDialog):
    """ DesignSPHysics MoorDyn Parameters Configuration Dialog. """

    def __init__(self, moordyn_parameters_data: MoorDynConfiguration):
        super().__init__()
        self.setWindowTitle(__("Moordyn Parameters Configuration"))

        self.stored_configuration: MoorDynConfiguration = moordyn_parameters_data  # Can be None

        self.setMinimumSize(640, 480)
        self.root_layout: QtGui.QVBoxLayout = QtGui.QVBoxLayout()
        self.root_scroll: QtGui.QScrollArea = QtGui.QScrollArea()
        self.root_scroll.setMinimumWidth(400)
        self.root_scroll.setWidgetResizable(True)
        self.scroll_widget: QtGui.QWidget = QtGui.QWidget()
        self.scroll_widget.setMinimumWidth(400)
        self.scroll_widget_layout: QtGui.QVBoxLayout = QtGui.QVBoxLayout()

        # Solver options groupbox
        self.solver_options_groupbox: QtGui.QGroupBox = QtGui.QGroupBox(__("Solver Options"))
        self.solver_options_groupbox_layout: QtGui.QFormLayout = QtGui.QFormLayout()
        self.water_depth_line_edit: QtGui.QLineEdit = QtGui.QLineEdit()
        self.fricdamp_line_edit: QtGui.QLineEdit = QtGui.QLineEdit()
        self.statdynfricscale_line_edit: QtGui.QLineEdit = QtGui.QLineEdit()
        self.dtIC_line_edit: QtGui.QLineEdit = QtGui.QLineEdit()
        self.cdScaleIC_line_edit: QtGui.QLineEdit = QtGui.QLineEdit()
        self.tmaxIC_line_edit: QtGui.QLineEdit = QtGui.QLineEdit()
        self.timeMax_line_edit: QtGui.QLineEdit = QtGui.QLineEdit()

        self.solver_options_groupbox_layout.addRow(__("Water Depth (m):"), self.water_depth_line_edit)
        self.solver_options_groupbox_layout.addRow(__("Damping:"), self.fricdamp_line_edit)
        self.solver_options_groupbox_layout.addRow(__("Static Dynamic Friction ratio:"), self.statdynfricscale_line_edit)
        self.solver_options_groupbox_layout.addRow(__("[ICdt] Convergence analysis time step:"), self.dtIC_line_edit)
        self.solver_options_groupbox_layout.addRow(__("ICDfac:"), self.cdScaleIC_line_edit)
        self.solver_options_groupbox_layout.addRow(__("Max time for IC:"), self.tmaxIC_line_edit)
        self.solver_options_groupbox_layout.addRow(__("Simulation Time (s):"), self.timeMax_line_edit)
        self.solver_options_groupbox.setLayout(self.solver_options_groupbox_layout)

        # Body configuration groupbox
        self.body_configuration_groupbox: QtGui.QGroupBox = QtGui.QGroupBox(__("Body configuration"))
        self.body_configuration_groupbox_layout: QtGui.QVBoxLayout = QtGui.QVBoxLayout()
        self.body_configuration_table: QtGui.QTableWidget = QtGui.QTableWidget()
        self.body_configuration_table.horizontalHeader().setResizeMode(QtGui.QHeaderView.Stretch)
        self.body_configuration_table.horizontalHeader().hide()
        self.body_configuration_table.verticalHeader().hide()
        self.body_configuration_table.setRowCount(0)
        self.body_configuration_table.setColumnCount(1)
        self.body_configuration_groupbox_layout.addWidget(self.body_configuration_table)
        self.body_configuration_groupbox.setLayout(self.body_configuration_groupbox_layout)

        # Line default configuration groupbox
        self.line_default_configuration_groupbox: QtGui.QGroupBox = QtGui.QGroupBox(__("Line default configuration"))
        self.line_default_configuration_groupbox_layout: QtGui.QFormLayout = QtGui.QFormLayout()
        self.ea_line_edit: QtGui.QLineEdit = QtGui.QLineEdit()
        self.diameter_line_edit: QtGui.QLineEdit = QtGui.QLineEdit()
        self.massDenInAir_line_edit: QtGui.QLineEdit = QtGui.QLineEdit()
        self.ba_line_edit: QtGui.QLineEdit = QtGui.QLineEdit()

        self.line_default_configuration_groupbox_layout.addRow(__("Stiffness (N):"), self.ea_line_edit)
        self.line_default_configuration_groupbox_layout.addRow(__("Diameter (m):"), self.diameter_line_edit)
        self.line_default_configuration_groupbox_layout.addRow(__("Mass in Air (kg/m):"), self.massDenInAir_line_edit)
        self.line_default_configuration_groupbox_layout.addRow(__("Line internal damping (Ns):"), self.ba_line_edit)
        self.line_default_configuration_groupbox.setLayout(self.line_default_configuration_groupbox_layout)

        # Lines groupbox
        self.lines_groupbox: QtGui.QGroupBox = QtGui.QGroupBox(__("Lines"))
        self.lines_groupbox_layout: QtGui.QVBoxLayout = QtGui.QVBoxLayout()
        self.lines_table: QtGui.QTableWidget = QtGui.QTableWidget()
        self.lines_table.setRowCount(0)
        self.lines_table.setColumnCount(1)
        self.lines_table.horizontalHeader().setResizeMode(QtGui.QHeaderView.Stretch)
        self.lines_table.horizontalHeader().hide()
        self.lines_table.verticalHeader().hide()
        self.add_line_button: QtGui.QPushButton = QtGui.QPushButton(__("Add a new Line"))
        self.lines_groupbox_layout.addWidget(self.lines_table)
        self.lines_groupbox_layout.addWidget(self.add_line_button)
        self.lines_groupbox.setLayout(self.lines_groupbox_layout)

        # Bottom button row
        self.bottom_button_layout: QtGui.QHBoxLayout = QtGui.QHBoxLayout()
        self.ok_button: QtGui.QPushButton = QtGui.QPushButton(__("OK"))

        self.bottom_button_layout.addStretch(1)
        self.bottom_button_layout.addWidget(self.ok_button)

        # Root layout composition
        self.scroll_widget_layout.addWidget(self.solver_options_groupbox)
        self.scroll_widget_layout.addWidget(self.body_configuration_groupbox)
        self.scroll_widget_layout.addWidget(self.line_default_configuration_groupbox)
        self.scroll_widget_layout.addWidget(self.lines_groupbox)

        self.scroll_widget.setLayout(self.scroll_widget_layout)

        self.root_scroll.setWidget(self.scroll_widget)
        self.root_layout.addWidget(self.root_scroll)
        self.root_layout.addLayout(self.bottom_button_layout)
        self.setLayout(self.root_layout)

        # Bind connections
        self.ok_button.clicked.connect(self._on_ok)
        self.add_line_button.clicked.connect(self._on_add_new_line)

        # Populate data
        self._fill_data()
        self.exec_()

    def _on_ok(self):
        # Solver options
        self.stored_configuration.solver_options.water_depth = float(self.water_depth_line_edit.text())
        self.stored_configuration.solver_options.fricDamp = float(self.fricdamp_line_edit.text())
        self.stored_configuration.solver_options.statDynFricScale = float(self.statdynfricscale_line_edit.text())
        self.stored_configuration.solver_options.dtIC = float(self.dtIC_line_edit.text())
        self.stored_configuration.solver_options.cdScaleIC = float(self.cdScaleIC_line_edit.text())
        self.stored_configuration.solver_options.tmaxIC = float(self.tmaxIC_line_edit.text())
        self.stored_configuration.solver_options.timeMax = float(self.timeMax_line_edit.text())

        # Line default config
        self.stored_configuration.line_default_configuration.ea = self.ea_line_edit.text()
        self.stored_configuration.line_default_configuration.diameter = self.diameter_line_edit.text()
        self.stored_configuration.line_default_configuration.massDenInAir = float(self.massDenInAir_line_edit.text())
        self.stored_configuration.line_default_configuration.ba = float(self.ba_line_edit.text())

        # Bodies and lines are references to lists, so they're already modified in memory :)
        self.accept()

    def _on_add_new_line(self):
        new_line: MoorDynLine = MoorDynLine()
        self.stored_configuration.lines.append(new_line)
        self.lines_table.setRowCount(self.lines_table.rowCount() + 1)
        widget: MoorDynLineWidget = MoorDynLineWidget(new_line.line_id)
        widget.configure_clicked.connect(lambda line_id=None: debug("Opening line configuration for uuid: {}".format(line_id)))
        widget.delete_clicked.connect(lambda line_id=None: debug("Deleting line with uuid: {}".format(line_id)))
        self.lines_table.setCellWidget(self.lines_table.rowCount() - 1, 0, widget)

    def _on_delete_line(self, line_id):
        pass

    def _on_configure_line(self, line_id):
        pass

    def _on_configure_body(self, mkbound):
        pass

    def _fill_data(self):
        # Solver options
        self.water_depth_line_edit.setText(str(self.stored_configuration.solver_options.water_depth))
        self.fricdamp_line_edit.setText(str(self.stored_configuration.solver_options.fricDamp))
        self.statdynfricscale_line_edit.setText(str(self.stored_configuration.solver_options.statDynFricScale))
        self.dtIC_line_edit.setText(str(self.stored_configuration.solver_options.dtIC))
        self.cdScaleIC_line_edit.setText(str(self.stored_configuration.solver_options.cdScaleIC))
        self.tmaxIC_line_edit.setText(str(self.stored_configuration.solver_options.tmaxIC))
        self.timeMax_line_edit.setText(str(self.stored_configuration.solver_options.timeMax))

        # Bodies
        self.body_configuration_table.setRowCount(len(self.stored_configuration.bodies))
        for index, body in enumerate(self.stored_configuration.bodies):
            widget: MoorDynBodyWidget = MoorDynBodyWidget(ObjectType.BOUND, body.ref)
            widget.configure_clicked.connect(lambda mkbound=None: debug("Opening body configuration for mkbound: {}".format(mkbound)))
            self.body_configuration_table.setCellWidget(index, 0, widget)

        # Line default config
        self.ea_line_edit.setText(str(self.stored_configuration.line_default_configuration.ea))
        self.diameter_line_edit.setText(str(self.stored_configuration.line_default_configuration.diameter))
        self.massDenInAir_line_edit.setText(str(self.stored_configuration.line_default_configuration.massDenInAir))
        self.ba_line_edit.setText(str(self.stored_configuration.line_default_configuration.ba))

        # Lines
        self.lines_table.setRowCount(len(self.stored_configuration.lines))
        for index, line in enumerate(self.stored_configuration.lines):
            widget: MoorDynLineWidget = MoorDynLineWidget(line.line_id)
            widget.configure_clicked.connect(lambda line_id=None: debug("Opening line configuration for uuid: {}".format(line_id)))
            widget.delete_clicked.connect(lambda line_id=None: debug("Deleting line with uuid: {}".format(line_id)))
            self.lines_table.setCellWidget(index, 0, widget)
