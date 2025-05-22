
from PySide2 import QtWidgets, QtCore
from mod.tools.dialog_tools import warning_dialog


class MotionTimeline(QtWidgets.QWidget):
    order_up = QtCore.Signal(int)
    order_down = QtCore.Signal(int)

    def __init__(self,  parent=None, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.setFocusPolicy(QtCore.Qt.NoFocus)  #####TEST ####

    def disable_order_up_button(self):
        """ Disables the up button to reorder the widget. """
        self.order_up_button.setEnabled(False)

    def disable_order_down_button(self):
        """ Disables the order down button. """
        self.order_down_button.setEnabled(False)

    def on_order_up(self):
        """ Reacts to the order up button being pressed and moves the element up a position. """
        self.order_up.emit(self.index)

    def on_order_down(self):
        """ Reacts to the order down button being pressed and moves the element down a position. """
        self.order_down.emit(self.index)

    def on_change(self):
        """ Reacts to a change and emits an object construction signal. """
        try:
            self.changed.emit(self.index, self.construct_motion_object())
        except ValueError:
            warning_dialog("Introduced an invalid value for a float number.")

    def construct_motion_object(self):
        pass

    def on_delete(self):
        """ Emits the delete signal on the current motion object specified. """
        self.deleted.emit(self.index, self.construct_motion_object())







