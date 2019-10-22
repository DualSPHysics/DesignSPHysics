#!/usr/bin/env python3.7
# -*- coding: utf-8 -*-
"""DesignSPHysics Movement Dialog """

import FreeCADGui

from PySide import QtCore, QtGui

from mod.translation_tools import __
from mod.gui_tools import get_icon
from mod.dialog_tools import info_dialog
from mod.enums import HelpURL
from mod.freecad_tools import get_fc_main_window

from mod.dataobjects.case import Case
from mod.dataobjects.motion.movement import Movement
from mod.dataobjects.motion.special_movement import SpecialMovement
from mod.dataobjects.motion.regular_piston_wave_gen import RegularPistonWaveGen
from mod.dataobjects.motion.irregular_piston_wave_gen import IrregularPistonWaveGen
from mod.dataobjects.motion.regular_flap_wave_gen import RegularFlapWaveGen
from mod.dataobjects.motion.irregular_flap_wave_gen import IrregularFlapWaveGen
from mod.dataobjects.motion.file_gen import FileGen
from mod.dataobjects.motion.rotation_file_gen import RotationFileGen
from mod.dataobjects.motion.wave_gen import WaveGen
from mod.dataobjects.motion.rect_motion import RectMotion
from mod.dataobjects.motion.wait_motion import WaitMotion
from mod.dataobjects.motion.acc_rect_motion import AccRectMotion
from mod.dataobjects.motion.rot_motion import RotMotion
from mod.dataobjects.motion.acc_rot_motion import AccRotMotion
from mod.dataobjects.motion.acc_cir_motion import AccCirMotion
from mod.dataobjects.motion.rot_sinu_motion import RotSinuMotion
from mod.dataobjects.motion.cir_sinu_motion import CirSinuMotion
from mod.dataobjects.motion.rect_sinu_motion import RectSinuMotion

from mod.widgets.motion.movement_timeline_placeholder import MovementTimelinePlaceholder
from mod.widgets.motion.rectilinear_motion_timeline import RectilinearMotionTimeline
from mod.widgets.motion.wait_motion_timeline import WaitMotionTimeline
from mod.widgets.motion.acc_rectilinear_motion_timeline import AccRectilinearMotionTimeline
from mod.widgets.motion.rotational_motion_timeline import RotationalMotionTimeline
from mod.widgets.motion.acc_rotational_motion_timeline import AccRotationalMotionTimeline
from mod.widgets.motion.acc_circular_motion_timeline import AccCircularMotionTimeline
from mod.widgets.motion.rot_sinu_motion_timeline import RotSinuMotionTimeline
from mod.widgets.motion.cir_sinu_motion_timeline import CirSinuMotionTimeline
from mod.widgets.motion.rect_sinu_motion_timeline import RectSinuMotionTimeline
from mod.widgets.motion.regular_piston_wave_motion_timeline import RegularPistonWaveMotionTimeline
from mod.widgets.motion.irregular_piston_wave_motion_timeline import IrregularPistonWaveMotionTimeline
from mod.widgets.motion.regular_flap_wave_motion_timeline import RegularFlapWaveMotionTimeline
from mod.widgets.motion.irregular_flap_wave_motion_timeline import IrregularFlapWaveMotionTimeline
from mod.widgets.motion.file_motion_timeline import FileMotionTimeline
from mod.widgets.motion.rotation_file_motion_timeline import RotationFileMotionTimeline
from mod.widgets.motion.movement_actions import MovementActions
from mod.widgets.motion.wave_movement_actions import WaveMovementActions


class MovementDialog(QtGui.QDialog):
    """ Defines a window with motion  """

    def __init__(self, parent=None):
        super(MovementDialog, self).__init__(parent=parent)

        self.setMinimumSize(1400, 650)
        self.setWindowTitle(__("Motion configuration"))
        self.ok_button = QtGui.QPushButton(__("Ok"))
        self.cancel_button = QtGui.QPushButton(__("Cancel"))
        self.notice_label = QtGui.QLabel("")
        self.notice_label.setStyleSheet("QLabel { color : red; }")
        self.target_mk = Case.instance().get_simulation_object(FreeCADGui.Selection.getSelection()[0].Name)
        self.mkbasedproperties = Case.instance().get_mk_based_properties(self.target_mk)
        self.movements_selected = self.mkbasedproperties.movements

        self.ok_button.clicked.connect(self.on_ok)
        self.cancel_button.clicked.connect(self.on_cancel)

        self.has_motion_layout = QtGui.QHBoxLayout()
        self.has_motion_label = QtGui.QLabel(__("Set motion: "))
        self.has_motion_label.setToolTip(__("Enables motion for the selected MKBound"))
        self.has_motion_selector = QtGui.QComboBox()
        self.has_motion_selector.insertItems(0, ["True", "False"])
        self.has_motion_selector.currentIndexChanged.connect(self.on_motion_change)

        ##############################################################################

        self.create_new_movement_button = QtGui.QToolButton()
        self.create_new_movement_button.setPopupMode(QtGui.QToolButton.MenuButtonPopup)
        self.create_new_movement_button.setText(" {}".format(__("Create New")))

        self.create_new_movement_menu = QtGui.QMenu()
        self.create_new_movement_menu.addAction(get_icon("movement.png"), __("Movement"))
        self.create_new_movement_menu.addAction(get_icon("regular_wave.png"), __("Regular wave generator (Piston)"))
        self.create_new_movement_menu.addAction(get_icon("irregular_wave.png"),
                                                __("Irregular wave generator (Piston)"))
        self.create_new_movement_menu.addAction(get_icon("regular_wave.png"), __("Regular wave generator (Flap)"))
        self.create_new_movement_menu.addAction(get_icon("irregular_wave.png"),
                                                __("Irregular wave generator (Flap)"))
        self.create_new_movement_menu.addAction(get_icon("file_mov.png"), __("Linear motion from a file"))
        self.create_new_movement_menu.addAction(get_icon("file_mov.png"), __("Rotation from a file"))
        self.create_new_movement_button.setMenu(self.create_new_movement_menu)

        ##############################################################################

        self.has_motion_helplabel = QtGui.QLabel("<a href='{}'>{}</a>".format(HelpURL.MOTION_HELP, __("Movement Help")))
        self.has_motion_helplabel.setTextFormat(QtCore.Qt.RichText)
        self.has_motion_helplabel.setTextInteractionFlags(
            QtCore.Qt.TextBrowserInteraction)
        self.has_motion_helplabel.setOpenExternalLinks(True)
        self.has_motion_targetlabel = QtGui.QLabel(__("Target MKBound: ") + str(self.target_mk))
        self.has_motion_layout.addWidget(self.has_motion_label)
        self.has_motion_layout.addWidget(self.has_motion_selector)
        self.has_motion_layout.addStretch(1)
        self.has_motion_layout.addWidget(self.has_motion_helplabel)
        self.has_motion_layout.addWidget(self.has_motion_targetlabel)

        self.motion_features_layout = QtGui.QVBoxLayout()
        self.motion_features_splitter = QtGui.QSplitter()

        self.movement_list_groupbox = QtGui.QGroupBox(__("Global Movements"))
        self.movement_list_groupbox_layout = QtGui.QVBoxLayout()

        self.movement_list_table = QtGui.QTableWidget(1, 2)
        self.movement_list_table.setSelectionBehavior(
            QtGui.QAbstractItemView.SelectItems)
        self.movement_list_table.setSelectionMode(QtGui.QAbstractItemView.SingleSelection)
        self.movement_list_table.horizontalHeader().setResizeMode(QtGui.QHeaderView.Stretch)
        self.movement_list_table.horizontalHeader().setResizeMode(0, QtGui.QHeaderView.Stretch)
        self.movement_list_table.horizontalHeader().setResizeMode(1, QtGui.QHeaderView.ResizeToContents)

        self.movement_list_table.verticalHeader().setVisible(False)
        self.movement_list_table.horizontalHeader().setVisible(False)

        self.movement_list_groupbox_layout.addWidget(self.create_new_movement_button)
        self.movement_list_groupbox_layout.addWidget(self.movement_list_table)
        self.movement_list_groupbox.setLayout(self.movement_list_groupbox_layout)

        self.timeline_groupbox = QtGui.QGroupBox(__("Timeline for the selected movement"))
        self.timeline_groupbox_layout = QtGui.QVBoxLayout()

        self.timeline_list_table = QtGui.QTableWidget(0, 1)
        self.timeline_list_table.horizontalHeader().setResizeMode(QtGui.QHeaderView.Stretch)
        self.timeline_list_table.verticalHeader().setResizeMode(QtGui.QHeaderView.ResizeToContents)
        self.timeline_list_table.verticalHeader().setVisible(False)
        self.timeline_list_table.horizontalHeader().setVisible(False)
        self.timeline_list_table.resizeRowsToContents()

        self.timeline_groupbox_layout.addWidget(self.timeline_list_table)
        self.timeline_groupbox.setLayout(self.timeline_groupbox_layout)

        self.actions_groupbox = QtGui.QGroupBox(__("Available actions"))
        self.actions_groupbox_layout = QtGui.QVBoxLayout()

        self.actions_groupbox_table = QtGui.QTableWidget(0, 1)
        self.actions_groupbox_table.horizontalHeader().setResizeMode(QtGui.QHeaderView.Stretch)
        self.actions_groupbox_table.verticalHeader().setVisible(False)
        self.actions_groupbox_table.horizontalHeader().setVisible(False)

        self.actions_groupbox_layout.addWidget(self.actions_groupbox_table)
        self.actions_groupbox.setLayout(self.actions_groupbox_layout)

        self.motion_features_splitter.addWidget(self.movement_list_groupbox)
        self.motion_features_splitter.addWidget(self.timeline_groupbox)
        self.motion_features_splitter.addWidget(self.actions_groupbox)
        self.motion_features_splitter.setSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        self.motion_features_layout.addWidget(self.motion_features_splitter)

        self.buttons_layout = QtGui.QHBoxLayout()
        self.buttons_layout.addWidget(self.notice_label)
        self.buttons_layout.addStretch(1)
        self.buttons_layout.addWidget(self.ok_button)
        self.buttons_layout.addWidget(self.cancel_button)

        self.motion_window_layout = QtGui.QVBoxLayout()
        self.motion_window_layout.addLayout(self.has_motion_layout)
        self.motion_window_layout.addLayout(self.motion_features_layout)
        self.motion_window_layout.addLayout(self.buttons_layout)

        self.setLayout(self.motion_window_layout)

        self.refresh_movements_table()
        self.movement_list_table.cellChanged.connect(self.on_movement_name_change)
        self.movement_list_table.cellClicked.connect(self.on_movement_selected)

        self.actions_groupbox_table.setRowCount(9)
        self.bt_to_add = QtGui.QPushButton(get_icon("left-arrow.png"), __("Add a delay"))
        self.bt_to_add.setStyleSheet("text-align: left")
        self.bt_to_add.clicked.connect(self.on_add_delay)
        self.actions_groupbox_table.setCellWidget(0, 0, self.bt_to_add)
        self.bt_to_add = QtGui.QPushButton(get_icon("left-arrow.png"), __("Add a rectilinear motion"))
        self.bt_to_add.setStyleSheet("text-align: left")
        self.bt_to_add.clicked.connect(self.on_add_rectilinear)
        self.actions_groupbox_table.setCellWidget(1, 0, self.bt_to_add)
        self.bt_to_add = QtGui.QPushButton(get_icon("left-arrow.png"), __("Add an accelerated rectilinear motion"))
        self.bt_to_add.setStyleSheet("text-align: left")
        self.bt_to_add.clicked.connect(self.on_add_accrectilinear)
        self.actions_groupbox_table.setCellWidget(2, 0, self.bt_to_add)
        self.bt_to_add = QtGui.QPushButton(get_icon("left-arrow.png"), __("Add a rotational motion"))
        self.bt_to_add.setStyleSheet("text-align: left")
        self.bt_to_add.clicked.connect(self.on_add_rotational)
        self.actions_groupbox_table.setCellWidget(3, 0, self.bt_to_add)
        self.bt_to_add = QtGui.QPushButton(get_icon("left-arrow.png"), __("Add an accelerated rotational motion"))
        self.bt_to_add.setStyleSheet("text-align: left")
        self.bt_to_add.clicked.connect(self.on_add_acc_rotational)
        self.actions_groupbox_table.setCellWidget(4, 0, self.bt_to_add)
        self.bt_to_add = QtGui.QPushButton(get_icon("left-arrow.png"), __("Add an accelerated circular motion"))
        self.bt_to_add.setStyleSheet("text-align: left")
        self.bt_to_add.clicked.connect(self.on_add_acc_circular)
        self.actions_groupbox_table.setCellWidget(5, 0, self.bt_to_add)
        self.bt_to_add = QtGui.QPushButton(get_icon("left-arrow.png"), __("Add a sinusoidal rotational motion"))
        self.bt_to_add.setStyleSheet("text-align: left")
        self.bt_to_add.clicked.connect(self.on_add_sinu_rot)
        self.actions_groupbox_table.setCellWidget(6, 0, self.bt_to_add)
        self.bt_to_add = QtGui.QPushButton(get_icon("left-arrow.png"), __("Add a sinusoidal circular motion"))
        self.bt_to_add.setStyleSheet("text-align: left")
        self.bt_to_add.clicked.connect(self.on_add_sinu_cir)
        self.actions_groupbox_table.setCellWidget(7, 0, self.bt_to_add)
        self.bt_to_add = QtGui.QPushButton(get_icon("left-arrow.png"), __("Add a sinusoidal rectilinear motion"))
        self.bt_to_add.setStyleSheet("text-align: left")
        self.bt_to_add.clicked.connect(self.on_add_sinu_rect)
        self.actions_groupbox_table.setCellWidget(8, 0, self.bt_to_add)

        # Set motion suscription for this mk
        self.has_motion_selector.setCurrentIndex(1 if self.movements_selected else 0)

        self.exec_()

    def on_ok(self):
        info_dialog(__("This will apply the motion properties to all objects with mkbound = ") + str(self.target_mk))
        if self.has_motion_selector.currentIndex() == 0:
            # True has been selected
            # Reinstance the list and copy every movement selected to avoid referencing problems.
            self.mkbasedproperties.movements = list()
            for movement in self.movements_selected:
                self.mkbasedproperties.movements.append(movement)
        elif self.has_motion_selector.currentIndex() == 1:
            # False has been selected
            self.mkbasedproperties.movements = list()
        self.accept()

    def on_cancel(self):
        self.reject()

    def on_motion_change(self, index):
        """ Set motion action. Enables or disables parts of the window depending
        on what option was selected. """
        if index == 0:
            self.movement_list_groupbox.setEnabled(True)
            self.timeline_groupbox.setEnabled(True)
            self.actions_groupbox.setEnabled(True)
            self.timeline_list_table.setEnabled(False)
            self.actions_groupbox_table.setEnabled(False)

            # Put a placeholder in the table
            self.timeline_list_table.clearContents()
            self.timeline_list_table.setRowCount(1)
            self.timeline_list_table.setCellWidget(0, 0, MovementTimelinePlaceholder())
        else:
            self.movement_list_groupbox.setEnabled(False)
            self.timeline_groupbox.setEnabled(False)
            self.actions_groupbox.setEnabled(False)

    def check_movement_compatibility(self, target_movement):
        # Wave generators are exclusive
        if isinstance(target_movement, SpecialMovement):
            self.notice_label.setText("Notice: Wave generators and file movements are exclusive. All movements are disabled when using one.")
            del self.movements_selected[:]
        elif isinstance(target_movement, Movement):
            for index, ms in enumerate(self.movements_selected):
                if isinstance(ms, SpecialMovement):
                    self.movements_selected.pop(index)
                    self.notice_label.setText(
                        "Notice: Regular movements are not compatible with wave generators and file movements.")

    # Movements table actions
    def on_check_movement(self, index, checked):
        """ Add or delete a movement from the temporal list of selected movements. """
        self.notice_label.setText("")  # Reset the notice label if a valid change is made
        target_movement = Case.instance().info.global_movements[index]
        if checked:
            self.check_movement_compatibility(target_movement)
            self.movements_selected.append(target_movement)
        else:
            self.movements_selected.remove(target_movement)
        self.refresh_movements_table()

    def on_loop_movement(self, index, checked):
        """ Make a movement loop itself """
        self.notice_label.setText("")  # Reset the notice label if a valid change is made
        Case.instance().info.global_movements[index].set_loop(checked)

    def on_delete_movement(self, index):
        """ Remove a movement from the project. """
        try:
            self.movements_selected.remove(Case.instance().info.global_movements[index])
            # Reset the notice label if a valid change is made
            self.notice_label.setText("")
        except ValueError:
            # Movement wasn't selected
            pass
        Case.instance().info.global_movements.pop(index)
        self.refresh_movements_table()
        self.on_movement_selected(self.timeline_list_table.rowCount() - 1, None)

    def on_new_movement(self):
        """ Creates a movement on the project. """
        self.notice_label.setText("")  # Reset the notice label if a valid change is made
        to_add = Movement(name="New Movement")
        Case.instance().info.global_movements.append(to_add)
        self.movements_selected.append(to_add)
        self.check_movement_compatibility(to_add)

        self.refresh_movements_table()

    def on_new_wave_generator(self, action):
        """ Creates a movement on the project. """

        self.notice_label.setText("")  # Reset the notice label if a valid change is made
        if __("Movement") in action.text():
            self.on_new_movement()
            return
        if __("Regular wave generator (Piston)") in action.text():
            to_add = SpecialMovement(name="Regular Wave Generator (Piston)", generator=RegularPistonWaveGen())
        if __("Irregular wave generator (Piston)") in action.text():
            to_add = SpecialMovement(name="Irregular Wave Generator (Piston)", generator=IrregularPistonWaveGen())
        if __("Regular wave generator (Flap)") in action.text():
            to_add = SpecialMovement(name="Regular Wave Generator (Flap)", generator=RegularFlapWaveGen())
        if __("Irregular wave generator (Flap)") in action.text():
            to_add = SpecialMovement(name="Irregular Wave Generator (Flap)", generator=IrregularFlapWaveGen())
        if __("Linear motion from a file") in action.text():
            to_add = SpecialMovement(name="Linear motion from a file", generator=FileGen())
        if __("Rotation from a file") in action.text():
            to_add = SpecialMovement(name="Rotation from a file", generator=RotationFileGen())

        to_add.generator.parent_movement = to_add
        Case.instance().info.global_movements.append(to_add)
        self.check_movement_compatibility(to_add)
        self.movements_selected.append(to_add)

        self.refresh_movements_table()

    def on_movement_name_change(self, row, column):
        """ Changes the name of a movement on the project. """
        target_item = self.movement_list_table.item(row, column)
        if target_item is not None and Case.instance().info.global_movements[row].name != target_item.text():
            # Reset the notice label if a valid change is made
            self.notice_label.setText("")
            Case.instance().info.global_movements[row].name = target_item.text()

    def on_timeline_item_change(self, index, motion_object):
        """ Changes the values of an item on the timeline. """
        self.notice_label.setText("")  # Reset the notice label if a valid change is made
        if isinstance(motion_object, WaveGen):
            motion_object.parent_movement.set_wavegen(motion_object)
        else:
            motion_object.parent_movement.motion_list[index] = motion_object

    def on_timeline_item_delete(self, index, motion_object):
        """ Deletes an item from the timeline. """
        self.notice_label.setText("")  # Reset the notice label if a valid change is made
        motion_object.parent_movement.motion_list.pop(index)
        self.on_movement_selected(self.movement_list_table.selectedIndexes()[0].row(), None)

    def on_timeline_item_order_up(self, index):
        # Reset the notice label if a valid change is made
        self.notice_label.setText("")
        movement = Case.instance().info.global_movements[self.movement_list_table.selectedIndexes()[0].row()]
        movement.motion_list.insert(index - 1, movement.motion_list.pop(index))
        self.on_movement_selected(self.movement_list_table.selectedIndexes()[0].row(), None)

    def on_timeline_item_order_down(self, index):
        # Reset the notice label if a valid change is made
        self.notice_label.setText("")
        movement = Case.instance().info.global_movements[self.movement_list_table.selectedIndexes()[0].row()]
        movement.motion_list.insert(index + 1, movement.motion_list.pop(index))
        self.on_movement_selected(self.movement_list_table.selectedIndexes()[0].row(), None)

    def on_movement_selected(self, row, _):
        """ Shows the timeline for the selected movement. """
        try:
            target_movement = Case.instance().info.global_movements[row]
        except IndexError:
            self.timeline_list_table.clearContents()
            self.timeline_list_table.setEnabled(False)
            self.timeline_list_table.setRowCount(1)
            self.timeline_list_table.setCellWidget(0, 0, MovementTimelinePlaceholder())
            return
        self.timeline_list_table.clearContents()

        # Reset the notice label if a valid change is made
        self.notice_label.setText("")

        if isinstance(target_movement, Movement):
            self.timeline_list_table.setRowCount(len(target_movement.motion_list))
            self.timeline_list_table.setEnabled(True)
            self.actions_groupbox_table.setEnabled(True)

            current_row = 0
            for motion in target_movement.motion_list:
                if isinstance(motion, RectMotion):
                    target_to_put = RectilinearMotionTimeline(current_row, motion, parent=get_fc_main_window())
                elif isinstance(motion, WaitMotion):
                    target_to_put = WaitMotionTimeline(current_row, motion, parent=get_fc_main_window())
                elif isinstance(motion, AccRectMotion):
                    target_to_put = AccRectilinearMotionTimeline(current_row, motion, parent=get_fc_main_window())
                elif isinstance(motion, RotMotion):
                    target_to_put = RotationalMotionTimeline(current_row, motion, parent=get_fc_main_window())
                elif isinstance(motion, AccRotMotion):
                    target_to_put = AccRotationalMotionTimeline(current_row, motion, parent=get_fc_main_window())
                elif isinstance(motion, AccCirMotion):
                    target_to_put = AccCircularMotionTimeline(current_row, motion, parent=get_fc_main_window())
                elif isinstance(motion, RotSinuMotion):
                    target_to_put = RotSinuMotionTimeline(current_row, motion, parent=get_fc_main_window())
                elif isinstance(motion, CirSinuMotion):
                    target_to_put = CirSinuMotionTimeline(current_row, motion, parent=get_fc_main_window())
                elif isinstance(motion, RectSinuMotion):
                    target_to_put = RectSinuMotionTimeline(current_row, motion, parent=get_fc_main_window())
                else:
                    raise NotImplementedError("The type of movement: {} is not implemented.".format(
                        str(motion.__class__.__name__)))

                target_to_put.changed.connect(self.on_timeline_item_change)
                target_to_put.deleted.connect(self.on_timeline_item_delete)
                target_to_put.order_up.connect(self.on_timeline_item_order_up)
                target_to_put.order_down.connect(self.on_timeline_item_order_down)
                self.timeline_list_table.setCellWidget(current_row, 0, target_to_put)

                if current_row is 0:
                    target_to_put.disable_order_up_button()
                elif current_row is len(target_movement.motion_list) - 1:
                    target_to_put.disable_order_down_button()

                current_row += 1
        elif isinstance(target_movement, SpecialMovement):
            self.timeline_list_table.setRowCount(1)
            self.timeline_list_table.setEnabled(True)
            self.actions_groupbox_table.setEnabled(False)

            if isinstance(target_movement.generator, RegularPistonWaveGen):
                target_to_put = RegularPistonWaveMotionTimeline(target_movement.generator, parent=get_fc_main_window())
            elif isinstance(target_movement.generator, IrregularPistonWaveGen):
                target_to_put = IrregularPistonWaveMotionTimeline(target_movement.generator, parent=get_fc_main_window())
            if isinstance(target_movement.generator, RegularFlapWaveGen):
                target_to_put = RegularFlapWaveMotionTimeline(target_movement.generator, parent=get_fc_main_window())
            elif isinstance(target_movement.generator, IrregularFlapWaveGen):
                target_to_put = IrregularFlapWaveMotionTimeline(target_movement.generator, parent=get_fc_main_window())
            elif isinstance(target_movement.generator, FileGen):
                target_to_put = FileMotionTimeline(target_movement.generator, Case.instance().path, parent=get_fc_main_window())
            elif isinstance(target_movement.generator, RotationFileGen):
                target_to_put = RotationFileMotionTimeline(target_movement.generator, Case.instance().path, parent=get_fc_main_window())

            target_to_put.changed.connect(self.on_timeline_item_change)
            self.timeline_list_table.setCellWidget(0, 0, target_to_put)

    def refresh_movements_table(self):
        """ Refreshes the movement table. """
        self.movement_list_table.clearContents()
        self.movement_list_table.setRowCount(len(Case.instance().info.global_movements) + 1)
        current_row = 0
        for movement in Case.instance().info.global_movements:
            self.movement_list_table.setItem(current_row, 0, QtGui.QTableWidgetItem(movement.name))
            try:
                has_loop = movement.loop
            except AttributeError:
                has_loop = False
            if isinstance(movement, Movement):
                movement_actions = MovementActions(current_row, movement in self.movements_selected, has_loop, parent=get_fc_main_window())
                movement_actions.loop.connect(self.on_loop_movement)
            elif isinstance(movement, SpecialMovement):
                movement_actions = WaveMovementActions(current_row, movement in self.movements_selected, parent=get_fc_main_window())

            movement_actions.delete.connect(self.on_delete_movement)
            movement_actions.use.connect(self.on_check_movement)
            self.movement_list_table.setCellWidget(current_row, 1, movement_actions)

            current_row += 1

        self.create_new_movement_button.clicked.connect(self.on_new_movement)
        self.create_new_movement_menu.triggered.connect(self.on_new_wave_generator)

        self.movement_list_table.setCellWidget(current_row, 0, QtGui.QWidget())

    def on_add_delay(self):
        """ Adds a WaitMotion to the timeline of the selected movement. """
        self.notice_label.setText("")  # Reset the notice label if a valid change is made
        if self.movement_list_table.selectedIndexes():
            if self.movement_list_table.selectedIndexes()[0].row() is not len(Case.instance().info.global_movements):
                Case.instance().info.global_movements[self.movement_list_table.selectedIndexes()[0].row()].add_motion(WaitMotion())
                self.on_movement_selected(self.movement_list_table.selectedIndexes()[0].row(), None)

    def on_add_rectilinear(self):
        """ Adds a RectMotion to the timeline of the selected movement. """
        self.notice_label.setText("")  # Reset the notice label if a valid change is made
        if self.movement_list_table.selectedIndexes():
            if self.movement_list_table.selectedIndexes()[0].row() is not len(Case.instance().info.global_movements):
                Case.instance().info.global_movements[self.movement_list_table.selectedIndexes()[0].row()].add_motion(RectMotion())
                self.on_movement_selected(self.movement_list_table.selectedIndexes()[0].row(), None)

    def on_add_accrectilinear(self):
        """ Adds a AccRectMotion to the timeline of the selected movement. """
        self.notice_label.setText("")  # Reset the notice label if a valid change is made
        if self.movement_list_table.selectedIndexes():
            if self.movement_list_table.selectedIndexes()[0].row() is not len(Case.instance().info.global_movements):
                Case.instance().info.global_movements[self.movement_list_table.selectedIndexes()[0].row()].add_motion(AccRectMotion())
                self.on_movement_selected(
                    self.movement_list_table.selectedIndexes()[0].row(), None)

    def on_add_rotational(self):
        """ Adds a RotMotion to the timeline of the selected movement. """
        self.notice_label.setText(
            "")  # Reset the notice label if a valid change is made
        if self.movement_list_table.selectedIndexes():
            if self.movement_list_table.selectedIndexes()[0].row() is not len(Case.instance().info.global_movements):
                Case.instance().info.global_movements[self.movement_list_table.selectedIndexes()[0].row()].add_motion(RotMotion())
                self.on_movement_selected(
                    self.movement_list_table.selectedIndexes()[0].row(), None)

    def on_add_acc_rotational(self):
        """ Adds a AccRotMotion to the timeline of the selected movement. """
        self.notice_label.setText("")  # Reset the notice label if a valid change is made
        if self.movement_list_table.selectedIndexes():
            if self.movement_list_table.selectedIndexes()[0].row() is not len(Case.instance().info.global_movements):
                Case.instance().info.global_movements[self.movement_list_table.selectedIndexes()[0].row()].add_motion(AccRotMotion())
                self.on_movement_selected(
                    self.movement_list_table.selectedIndexes()[0].row(), None)

    def on_add_acc_circular(self):
        """ Adds a AccCirMotion to the timeline of the selected movement. """
        self.notice_label.setText("")  # Reset the notice label if a valid change is made
        if self.movement_list_table.selectedIndexes():
            if self.movement_list_table.selectedIndexes()[0].row() is not len(Case.instance().info.global_movements):
                Case.instance().info.global_movements[self.movement_list_table.selectedIndexes()[0].row()].add_motion(AccCirMotion())
                self.on_movement_selected(
                    self.movement_list_table.selectedIndexes()[0].row(), None)

    def on_add_sinu_rot(self):
        """ Adds a RotSinuMotion to the timeline of the selected movement. """
        self.notice_label.setText("")  # Reset the notice label if a valid change is made
        if self.movement_list_table.selectedIndexes():
            if self.movement_list_table.selectedIndexes()[0].row() is not len(Case.instance().info.global_movements):
                Case.instance().info.global_movements[self.movement_list_table.selectedIndexes()[0].row()].add_motion(RotSinuMotion())
                self.on_movement_selected(
                    self.movement_list_table.selectedIndexes()[0].row(), None)

    def on_add_sinu_cir(self):
        """ Adds a CirSinuMotion to the timeline of the selected movement. """
        self.notice_label.setText("")  # Reset the notice label if a valid change is made
        if self.movement_list_table.selectedIndexes():
            if self.movement_list_table.selectedIndexes()[0].row() is not len(Case.instance().info.global_movements):
                Case.instance().info.global_movements[self.movement_list_table.selectedIndexes()[0].row()].add_motion(CirSinuMotion())
                self.on_movement_selected(
                    self.movement_list_table.selectedIndexes()[0].row(), None)

    def on_add_sinu_rect(self):
        """ Adds a RectSinuMotion to the timeline of the selected movement. """
        self.notice_label.setText("")  # Reset the notice label if a valid change is made
        if self.movement_list_table.selectedIndexes():
            if self.movement_list_table.selectedIndexes()[0].row() is not len(Case.instance().info.global_movements):
                Case.instance().info.global_movements[self.movement_list_table.selectedIndexes()[0].row()].add_motion(RectSinuMotion())
                self.on_movement_selected(self.movement_list_table.selectedIndexes()[0].row(), None)
