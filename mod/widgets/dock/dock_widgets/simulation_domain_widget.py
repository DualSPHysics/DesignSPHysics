from PySide2 import QtWidgets
from mod.dataobjects.case import Case
from mod.dataobjects.configuration.sd_position_property import SDPositionProperty
from mod.dataobjects.configuration.simulation_domain import SimulationDomain
from mod.tools.stdout_tools import debug
from mod.tools.translation_tools import __
from mod.widgets.custom_widgets.size_input import SizeInput
from mod.widgets.custom_widgets.value_input import ValueInput


class SimulationDomainWidget(QtWidgets.QWidget):

    def __init__(self,domain:SimulationDomain,show_useparent:bool=False):

        super().__init__()

        # Simulation domain
        self.simdomain_layout = QtWidgets.QVBoxLayout()
        self.domain:SimulationDomain = domain
        self.show_useparent=show_useparent

        self.simdomain_chk = QtWidgets.QCheckBox(__("Simulation Domain"))
        self.simdomain_useparent_chk = QtWidgets.QCheckBox(__("Use Parent Domain"))

        self.simdomain_posmin_layout = QtWidgets.QHBoxLayout()
        self.simdomain_posminx_layout = QtWidgets.QVBoxLayout()
        self.simdomain_posminy_layout = QtWidgets.QVBoxLayout()
        self.simdomain_posminz_layout = QtWidgets.QVBoxLayout()
        self.simdomain_posmax_layout = QtWidgets.QHBoxLayout()
        self.simdomain_posmaxx_layout = QtWidgets.QVBoxLayout()
        self.simdomain_posmaxy_layout = QtWidgets.QVBoxLayout()
        self.simdomain_posmaxz_layout = QtWidgets.QVBoxLayout()
        texts_min=[__("Default"), __("Value"), __("Default - value"), __("Default - %")]
        self.simdomain_posmin_label = QtWidgets.QLabel(__("Minimum position(x, y, z):"))
        self.simdomain_posminx_combobox = QtWidgets.QComboBox()
        self.simdomain_posminx_combobox.insertItems(0,texts_min)
        self.simdomain_posminx_line_edit = ValueInput()

        self.simdomain_posminy_combobox = QtWidgets.QComboBox()
        self.simdomain_posminy_combobox.insertItems(0,
                                                    texts_min)
        self.simdomain_posminy_line_edit = ValueInput()

        self.simdomain_posminz_combobox = QtWidgets.QComboBox()
        self.simdomain_posminz_combobox.insertItems(0,
                                                    texts_min)
        self.simdomain_posminz_line_edit = ValueInput()

        self.simdomain_posminx_layout.addWidget(self.simdomain_posminx_combobox)
        self.simdomain_posminx_layout.addWidget(self.simdomain_posminx_line_edit)
        self.simdomain_posminy_layout.addWidget(self.simdomain_posminy_combobox)
        self.simdomain_posminy_layout.addWidget(self.simdomain_posminy_line_edit)
        self.simdomain_posminz_layout.addWidget(self.simdomain_posminz_combobox)
        self.simdomain_posminz_layout.addWidget(self.simdomain_posminz_line_edit)
        self.simdomain_posmin_layout.addWidget(self.simdomain_posmin_label)
        self.simdomain_posmin_layout.addLayout(self.simdomain_posminx_layout)
        self.simdomain_posmin_layout.addLayout(self.simdomain_posminy_layout)
        self.simdomain_posmin_layout.addLayout(self.simdomain_posminz_layout)

        texts_max=[__("Default"), __("Value"), __("Default + value"), __("Default + %")]
        self.simdomain_posmax_label = QtWidgets.QLabel(__("Maximum position(x, y, z):"))
        self.simdomain_posmaxx_combobox = QtWidgets.QComboBox()
        self.simdomain_posmaxx_combobox.insertItems(0,
                                                    texts_max)
        self.simdomain_posmaxx_line_edit = ValueInput()


        self.simdomain_posmaxy_combobox = QtWidgets.QComboBox()
        self.simdomain_posmaxy_combobox.insertItems(0,
                                                    texts_max)
        self.simdomain_posmaxy_line_edit = ValueInput()

        self.simdomain_posmaxz_combobox = QtWidgets.QComboBox()
        self.simdomain_posmaxz_combobox.insertItems(0,
                                                    texts_max)
        self.simdomain_posmaxz_line_edit = ValueInput()

        self.simdomain_posmaxx_layout.addWidget(self.simdomain_posmaxx_combobox)
        self.simdomain_posmaxx_layout.addWidget(self.simdomain_posmaxx_line_edit)
        self.simdomain_posmaxy_layout.addWidget(self.simdomain_posmaxy_combobox)
        self.simdomain_posmaxy_layout.addWidget(self.simdomain_posmaxy_line_edit)
        self.simdomain_posmaxz_layout.addWidget(self.simdomain_posmaxz_combobox)
        self.simdomain_posmaxz_layout.addWidget(self.simdomain_posmaxz_line_edit)
        self.simdomain_posmax_layout.addWidget(self.simdomain_posmax_label)
        self.simdomain_posmax_layout.addLayout(self.simdomain_posmaxx_layout)
        self.simdomain_posmax_layout.addLayout(self.simdomain_posmaxy_layout)
        self.simdomain_posmax_layout.addLayout(self.simdomain_posmaxz_layout)


        self.simdomain_layout.addWidget(self.simdomain_chk)
        if self.show_useparent:
            self.simdomain_layout.addWidget(self.simdomain_useparent_chk)
        self.simdomain_layout.addLayout(self.simdomain_posmin_layout)
        self.simdomain_layout.addLayout(self.simdomain_posmax_layout)
        self.simdomain_chk.stateChanged.connect(self.on_simdomain_change)
        self.simdomain_useparent_chk.stateChanged.connect(self.on_simdomain_change)
        self.simdomain_posmaxx_combobox.currentIndexChanged.connect(self.on_posmaxx_changed)
        self.simdomain_posmaxy_combobox.currentIndexChanged.connect(self.on_posmaxy_changed)
        self.simdomain_posmaxz_combobox.currentIndexChanged.connect(self.on_posmaxz_changed)
        self.simdomain_posminx_combobox.currentIndexChanged.connect(self.on_posminx_changed)
        self.simdomain_posminy_combobox.currentIndexChanged.connect(self.on_posminy_changed)
        self.simdomain_posminz_combobox.currentIndexChanged.connect(self.on_posminz_changed)

        self.setLayout(self.simdomain_layout)

        self.fill_values()

    def fill_values(self):
        self.simdomain_chk.setChecked(self.domain.enabled)
        self.simdomain_useparent_chk.setChecked(self.domain.useparent)
        self.on_simdomain_change()

        self.simdomain_posminx_combobox.setCurrentIndex(self.domain.posmin_x.type)
        self.simdomain_posminy_combobox.setCurrentIndex(self.domain.posmin_y.type)
        self.simdomain_posminz_combobox.setCurrentIndex(self.domain.posmin_z.type)
        self.simdomain_posmaxx_combobox.setCurrentIndex(self.domain.posmax_x.type)
        self.simdomain_posmaxy_combobox.setCurrentIndex(self.domain.posmax_y.type)
        self.simdomain_posmaxz_combobox.setCurrentIndex(self.domain.posmax_z.type)


        self.simdomain_posminx_line_edit.setValue(self.domain.posmin_x.value)
        self.simdomain_posminy_line_edit.setValue(self.domain.posmin_y.value)
        self.simdomain_posminz_line_edit.setValue(self.domain.posmin_z.value)
        self.simdomain_posmaxx_line_edit.setValue(self.domain.posmax_x.value)
        self.simdomain_posmaxy_line_edit.setValue(self.domain.posmax_y.value)
        self.simdomain_posmaxz_line_edit.setValue(self.domain.posmax_z.value)





    def on_simdomain_change(self):
        """ Reacts to the simdomain checkbox being pressed enabling/disabling its inputs. """
        if not self.simdomain_chk.isChecked():
            self.simdomain_useparent_chk.setEnabled(False)
        else:
            self.simdomain_useparent_chk.setEnabled(True)
        if self.simdomain_chk.isChecked() and (not self.simdomain_useparent_chk.isChecked() or not self.show_useparent):
            self.simdomain_posminx_combobox.setEnabled(True)
            self.simdomain_posminy_combobox.setEnabled(True)
            self.simdomain_posminz_combobox.setEnabled(True)
            self.simdomain_posmaxx_combobox.setEnabled(True)
            self.simdomain_posmaxy_combobox.setEnabled(True)
            self.simdomain_posmaxz_combobox.setEnabled(True)
            self.on_posminx_changed()
            self.on_posminy_changed()
            self.on_posminz_changed()
            self.on_posmaxx_changed()
            self.on_posmaxy_changed()
            self.on_posmaxz_changed()

        else:
            self.simdomain_posminx_combobox.setEnabled(False)
            self.simdomain_posminy_combobox.setEnabled(False)
            self.simdomain_posminz_combobox.setEnabled(False)
            self.simdomain_posmaxx_combobox.setEnabled(False)
            self.simdomain_posmaxy_combobox.setEnabled(False)
            self.simdomain_posmaxz_combobox.setEnabled(False)
            self.simdomain_posminx_line_edit.setEnabled(False)
            self.simdomain_posminy_line_edit.setEnabled(False)
            self.simdomain_posminz_line_edit.setEnabled(False)
            self.simdomain_posmaxx_line_edit.setEnabled(False)
            self.simdomain_posmaxy_line_edit.setEnabled(False)
            self.simdomain_posmaxz_line_edit.setEnabled(False)

    def on_posminx_changed(self):
        """ Reacts to the posminx combobox being changed enabling/disabling its input. """
        if self.simdomain_posminx_combobox.currentIndex() == 0:
            self.simdomain_posminx_line_edit.setEnabled(False)
        else:
            self.simdomain_posminx_line_edit.setEnabled(True)
            if self.simdomain_posminx_combobox.currentIndex() == 1:
                self.simdomain_posminx_line_edit.setParent(None)
                self.simdomain_posminx_line_edit=SizeInput()
                self.simdomain_posminx_layout.insertWidget(1,self.simdomain_posminx_line_edit)
            if self.simdomain_posminx_combobox.currentIndex() == 2:
                self.simdomain_posminx_line_edit.setParent(None)
                self.simdomain_posminx_line_edit = SizeInput()
                self.simdomain_posminx_layout.insertWidget(1, self.simdomain_posminx_line_edit)
            if self.simdomain_posminx_combobox.currentIndex() == 3:
                self.simdomain_posminx_line_edit.setParent(None)
                self.simdomain_posminx_line_edit = ValueInput()
                self.simdomain_posminx_layout.insertWidget(1, self.simdomain_posminx_line_edit)

    def on_posminy_changed(self):
        """ Reacts to the posminx combobox being changed enabling/disabling its input. """
        if self.simdomain_posminy_combobox.currentIndex() == 0:
            self.simdomain_posminy_line_edit.setEnabled(False)
        else:
            self.simdomain_posminy_line_edit.setEnabled(True)
            if self.simdomain_posminy_combobox.currentIndex() == 1:
                self.simdomain_posminy_line_edit.setParent(None)
                self.simdomain_posminy_line_edit=SizeInput()
                self.simdomain_posminy_layout.insertWidget(1,self.simdomain_posminy_line_edit)
            if self.simdomain_posminy_combobox.currentIndex() == 2:
                self.simdomain_posminy_line_edit.setParent(None)
                self.simdomain_posminy_line_edit = SizeInput()
                self.simdomain_posminy_layout.insertWidget(1, self.simdomain_posminy_line_edit)
            if self.simdomain_posminy_combobox.currentIndex() == 3:
                self.simdomain_posminy_line_edit.setParent(None)
                self.simdomain_posminy_line_edit = ValueInput()
                self.simdomain_posminy_layout.insertWidget(1, self.simdomain_posminy_line_edit)

    def on_posminz_changed(self):
        """ Reacts to the posminz combobox being changed enabling/disabling its input. """
        if self.simdomain_posminz_combobox.currentIndex() == 0:
            self.simdomain_posminz_line_edit.setEnabled(False)
        else:
            self.simdomain_posminz_line_edit.setEnabled(True)
            if self.simdomain_posminz_combobox.currentIndex() == 1:
                self.simdomain_posminz_line_edit.setParent(None)
                self.simdomain_posminz_line_edit=SizeInput()
                self.simdomain_posminz_layout.insertWidget(1,self.simdomain_posminz_line_edit)
            if self.simdomain_posminz_combobox.currentIndex() == 2:
                self.simdomain_posminz_line_edit.setParent(None)
                self.simdomain_posminz_line_edit = SizeInput()
                self.simdomain_posminz_layout.insertWidget(1, self.simdomain_posminz_line_edit)
            if self.simdomain_posminz_combobox.currentIndex() == 3:
                self.simdomain_posminz_line_edit.setParent(None)
                self.simdomain_posminz_line_edit = ValueInput()
                self.simdomain_posminz_layout.insertWidget(1, self.simdomain_posminz_line_edit)

    def on_posmaxx_changed(self):
        """ Reacts to the posmaxx combobox being changed enabling/disabling its input. """
        if self.simdomain_posmaxx_combobox.currentIndex() == 0:
            self.simdomain_posmaxx_line_edit.setEnabled(False)
        else:
            self.simdomain_posmaxx_line_edit.setEnabled(True)
            if self.simdomain_posmaxx_combobox.currentIndex() == 1:
                self.simdomain_posmaxx_line_edit.setParent(None)
                self.simdomain_posmaxx_line_edit = SizeInput()
                self.simdomain_posmaxx_layout.insertWidget(1, self.simdomain_posmaxx_line_edit)
            if self.simdomain_posmaxx_combobox.currentIndex() == 2:
                self.simdomain_posmaxx_line_edit.setParent(None)
                self.simdomain_posmaxx_line_edit = SizeInput()
                self.simdomain_posmaxx_layout.insertWidget(1, self.simdomain_posmaxx_line_edit)
            if self.simdomain_posmaxx_combobox.currentIndex() == 3:
                self.simdomain_posmaxx_line_edit.setParent(None)
                self.simdomain_posmaxx_line_edit = ValueInput()
                self.simdomain_posmaxx_layout.insertWidget(1, self.simdomain_posmaxx_line_edit)

    def on_posmaxy_changed(self):
        """ Reacts to the posmaxx combobox being changed enabling/disabling its input. """
        if self.simdomain_posmaxy_combobox.currentIndex() == 0:
            self.simdomain_posmaxy_line_edit.setEnabled(False)
        else:
            self.simdomain_posmaxy_line_edit.setEnabled(True)
            if self.simdomain_posmaxy_combobox.currentIndex() == 1:
                self.simdomain_posmaxy_line_edit.setParent(None)
                self.simdomain_posmaxy_line_edit = SizeInput()
                self.simdomain_posmaxy_layout.insertWidget(1, self.simdomain_posmaxy_line_edit)
            if self.simdomain_posmaxy_combobox.currentIndex() == 2:
                self.simdomain_posmaxy_line_edit.setParent(None)
                self.simdomain_posmaxy_line_edit = SizeInput()
                self.simdomain_posmaxy_layout.insertWidget(1, self.simdomain_posmaxy_line_edit)
            if self.simdomain_posmaxy_combobox.currentIndex() == 3:
                self.simdomain_posmaxy_line_edit.setParent(None)
                self.simdomain_posmaxy_line_edit = ValueInput()
                self.simdomain_posmaxy_layout.insertWidget(1, self.simdomain_posmaxy_line_edit)

    def on_posmaxz_changed(self):
        """ Reacts to the posmaxz combobox being changed enabling/disabling its input. """
        if self.simdomain_posmaxz_combobox.currentIndex() == 0:
            self.simdomain_posmaxz_line_edit.setEnabled(False)
        else:
            self.simdomain_posmaxz_line_edit.setEnabled(True)
            if self.simdomain_posmaxz_combobox.currentIndex() == 1:
                self.simdomain_posmaxz_line_edit.setParent(None)
                self.simdomain_posmaxz_line_edit = SizeInput()
                self.simdomain_posmaxz_layout.insertWidget(1, self.simdomain_posmaxz_line_edit)
            if self.simdomain_posmaxz_combobox.currentIndex() == 2:
                self.simdomain_posmaxz_line_edit.setParent(None)
                self.simdomain_posmaxz_line_edit = SizeInput()
                self.simdomain_posmaxz_layout.insertWidget(1, self.simdomain_posmaxz_line_edit)
            if self.simdomain_posmaxz_combobox.currentIndex() == 3:
                self.simdomain_posmaxz_line_edit.setParent(None)
                self.simdomain_posmaxz_line_edit = ValueInput()
                self.simdomain_posmaxz_layout.insertWidget(1, self.simdomain_posmaxz_line_edit)

    def save(self):
        if self.simdomain_chk.isChecked():
            self.domain.enabled = True
            # IncZ must be 0 in simulations with specified domain

            self.domain.useparent=self.simdomain_useparent_chk.isChecked()
            self.domain.posmin_x = SDPositionProperty(self.simdomain_posminx_combobox.currentIndex(),
                                                            self.simdomain_posminx_line_edit.value())
            self.domain.posmin_y = SDPositionProperty(self.simdomain_posminy_combobox.currentIndex(),
                                                            self.simdomain_posminy_line_edit.value())
            self.domain.posmin_z = SDPositionProperty(self.simdomain_posminz_combobox.currentIndex(),
                                                            self.simdomain_posminz_line_edit.value())

            self.domain.posmax_x = SDPositionProperty(self.simdomain_posmaxx_combobox.currentIndex(),
                                                            self.simdomain_posmaxx_line_edit.value())
            self.domain.posmax_y = SDPositionProperty(self.simdomain_posmaxy_combobox.currentIndex(),
                                                            self.simdomain_posmaxy_line_edit.value())
            self.domain.posmax_z = SDPositionProperty(self.simdomain_posmaxz_combobox.currentIndex(),
                                                            self.simdomain_posmaxz_line_edit.value())
        else:
            self.domain.enabled = False
            self.domain = SimulationDomain()
        return self.domain
