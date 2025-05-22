import re

from PySide2 import QtWidgets, QtCore

import FreeCADGui
import FreeCAD

from mod.constants import DEFAULT_MAX_WIDGET_WIDTH, DEFAULT_MIN_WIDGET_WIDTH
from mod.tools.dialog_tools import warning_dialog
from mod.tools.stdout_tools import debug
from mod.widgets.custom_widgets.base_units_input import BaseUnitsInput



class AccelerationInput(BaseUnitsInput):

    def __init__(self, min_val=-10e12,max_val=10e12,minwidth=DEFAULT_MIN_WIDGET_WIDTH, maxwidth=DEFAULT_MAX_WIDGET_WIDTH,parent=None,value=0):#maxwidth=45
        super().__init__(min_val,max_val,minwidth,maxwidth,parent)
        # Initialize unit system
        self.auto_update = False
        self.quantity_box.setMagnitude(pre_unit="",pos_unit="/s^2")
        self.setValue(value)
    
    def setValue(self, value):
        super().setValue(value,self.getUnits(),convert=False)

    def on_change(self):
        self._value = super().value_from_text()
        self.setValue(self._value)
        self.value_changed.emit()