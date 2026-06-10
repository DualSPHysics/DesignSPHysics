import re

import FreeCAD

from mod.constants import DEFAULT_MIN_WIDGET_WIDTH, DEFAULT_MAX_WIDGET_WIDTH,AUTO_UNITS_SELECT,DEFAULT_DECIMALS
from mod.tools.dialog_tools import warning_dialog
from mod.tools.stdout_tools import debug
from mod.widgets.custom_widgets.base_units_input import BaseUnitsInput



class SizeInput(BaseUnitsInput):

    def __init__(self, min_val=-10e12,max_val=10e12,minwidth=DEFAULT_MIN_WIDGET_WIDTH, maxwidth=DEFAULT_MAX_WIDGET_WIDTH,parent=None,value=0,decimals=DEFAULT_DECIMALS):#maxwidth=45
        super().__init__(min_val,max_val,minwidth,maxwidth,parent,decimals)
        # Initialize unit system
        # self.quantity_box.setUnit("m") #<Not needed
        self.setValue(value)
    
    def setValue(self, value):
        super().setValue(value,self.getUnits(),convert=AUTO_UNITS_SELECT) 

    def on_change(self):
        self._value = super().value_from_text()
        self.setValue(self._value)
        self.value_changed.emit()