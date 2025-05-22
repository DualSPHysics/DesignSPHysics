import re

from PySide2 import QtWidgets, QtCore

import FreeCADGui

from mod.constants import DEFAULT_MIN_WIDGET_WIDTH, DEFAULT_MAX_WIDGET_WIDTH

SIZE_OFFSET=9
class ValueInput(QtWidgets.QWidget):
    focus = QtCore.Signal(str)
    value_changed =QtCore.Signal()
    help_text = ""

    def __init__(self, min_val=-10e12,max_val=10e12,minwidth=DEFAULT_MIN_WIDGET_WIDTH, maxwidth=DEFAULT_MAX_WIDGET_WIDTH,parent=None,value=0,decimals=3):#maxwidth=45
        super().__init__(parent=parent)
        self._value=0
        self.quantity_box = FreeCADGui.UiLoader().createWidget("Gui::DoubleSpinBox")
        if value:
            self._value = value
            self.quantity_box.setProperty("value",value)
        self.quantity_box.setProperty("decimals", decimals)

        self.layout=QtWidgets.QHBoxLayout(parent = None)
        self.setLayout(self.layout)

        self.quantity_box.setMinimum(min_val)
        self.quantity_box.setMaximum(max_val)
        self.quantity_box.setMinimumWidth(minwidth)
        self.quantity_box.setMaximumWidth(maxwidth)
        self.setMinimumWidth(minwidth + SIZE_OFFSET)
        self.setMaximumWidth(maxwidth + SIZE_OFFSET)
        self.quantity_box.setMinimum(min_val)
        self.quantity_box.setMaximum(max_val)
        self.quantity_box.setFixedHeight(20)
        #self.setFixedHeight(26)

        self.quantity_box.editingFinished.connect(self.on_change)
        self.layout.addWidget(self.quantity_box)
        self.layout.setAlignment(QtCore.Qt.AlignLeft)
        self.layout.setContentsMargins(1,1,1,1)


    def set_help_text(self, help_text):
        """ Sets the help text for the line edit. """
        self.help_text = help_text

    def focusInEvent(self, *args, **kwargs):
        """ Reimplements the QLineEdit focusInEvent and fires the focus signal. """
        QtWidgets.QLineEdit.focusInEvent(self, *args, **kwargs)
        self.focus.emit(self.help_text)

    def on_change(self):
        self._value = self.quantity_box.property("value")
        self.value_changed.emit()

    def value(self):
        val = self.quantity_box.property("value")
        return val

    def setValue(self,value:float):
        self._value=value
        self.quantity_box.setProperty("value", value)
