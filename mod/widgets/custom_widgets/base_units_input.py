import re

from PySide2 import QtWidgets, QtCore

import FreeCADGui
import FreeCAD

from mod.widgets.custom_widgets.unit_spin_box import UnitSpinBox
from mod.constants import DEFAULT_MIN_WIDGET_WIDTH, DEFAULT_MAX_WIDGET_WIDTH,AUTO_UNITS_SELECT,DEFAULT_UNITS_CONFIG,DEFAULT_DECIMALS
from mod.tools.dialog_tools import warning_dialog,error_dialog
from mod.tools.stdout_tools import debug


SIZE_OFFSET = 9

class BaseUnitsInput(QtWidgets.QWidget):
    focus = QtCore.Signal(str)
    value_changed = QtCore.Signal()
    help_text = ""
    auto_update = AUTO_UNITS_SELECT
    unit_map = {
        0: "mm"  # Standard (mm)
       ,1: "m"   # MKS (m)
    #    ,2: "cm"  # Imperial decimal (inches)
    #    ,3: "in"  # Imperial fractional
    #    ,4: "ft"  # US building
    #    ,5: "thou" # Custom
    }
    def __init__(self, min_val=-10e12,max_val=10e12,minwidth=DEFAULT_MIN_WIDGET_WIDTH, maxwidth=DEFAULT_MAX_WIDGET_WIDTH,parent=None,decimals=DEFAULT_DECIMALS):#maxwidth=45
        super().__init__(parent=parent)
        
        self._value = 0
        # Select default units str
        self.unit_system = DEFAULT_UNITS_CONFIG
        self.default_unit = self.unit_map.get(self.unit_system, "m")  # Default to m
        # Select the units system used (auto or manual)
        if self.auto_update:
            self.unit_system = FreeCAD.ParamGet("User parameter:BaseApp/Preferences/Units").GetInt("UserSchema")
            # If the user-selected system is not allowed
            if self.unit_system not in self.unit_map:
                warning_dialog(f"Unit system with id={self.unit_system} is not allowed. Size units are set to '{self.default_unit}' by default.")

        self.layout=QtWidgets.QHBoxLayout(parent = None)
        self.setLayout(self.layout)
        self.quantity_box = UnitSpinBox(unit=self.get_user_unit_symbol())
        self.quantity_box.setProperty("minimum",min_val)
        self.quantity_box.setProperty("maximum",max_val)
        self.quantity_box.setMinimumWidth(minwidth)
        self.quantity_box.setMaximumWidth(maxwidth)
        self.quantity_box.setDecimals(decimals)
        self.setMinimumWidth(minwidth+SIZE_OFFSET)
        self.setMaximumWidth(maxwidth+SIZE_OFFSET)
        self.quantity_box.valueChanged.connect(self.on_change)
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

    def get_user_unit_symbol(self):
        """Get the symbol for user's preferred length unit"""
        if self.auto_update:
            new_sys = FreeCAD.ParamGet("User parameter:BaseApp/Preferences/Units").GetInt("UserSchema")
        else:
            new_sys = self.unit_system
        units = self.unit_map.get(new_sys, self.default_unit)  # Default to m
       
        # Dynamic units change
        # if new_sys != self.unit_system:
        #     self.unit_system = new_sys
        #     self.quantity_box.setUnit(units)
       
        return units
   
    def getValue(self):
        """Get the value as a FreeCAD Quantity object"""
        value_str = self.quantity_box.property("rawValue")
        value = FreeCAD.Units.Quantity(value_str)
        # value = self.quantity_box.property("value")
        return float(value)
    
    def value(self):
        """Qt-compatible value getter (returns in meters)"""
        return self.getValue()
    
    def on_change(self):
        pass

    def setValue(self, value, unit="m",convert=AUTO_UNITS_SELECT):
        """
        Set the value with optional unit specification
        Args:
            value: Numeric value or string with unit (e.g. "10 mm")
            unit: Required if value is numeric, ignored if value is string with unit
            convert: Performs the conversion when activated
        """
        try:
            if isinstance(value, str):
                value = value.strip()
                if value == "":
                    error_dialog(f"Empty string passed as value\n")
                    return
                self.quantity = FreeCAD.Units.Quantity(f"{float(value)}")
        except Exception as e:
            error_dialog(f"Invalid input '{value}' ({unit}): {e}\n")
            return

        display_value = value
        # Convert to display unit and set
        # if convert:
        #     display_unit = self.get_user_unit_symbol()
        #     display_value = self.quantity.getValueAs(display_unit)
        self._value = float(display_value)
        self.quantity_box.setValue(self._value)
        self.quantity_box.setProperty("rawValue",self._value)

    def getUnits(self):
        return "" if not self.quantity_box else self.quantity_box.getUnit() 
    
    def value_from_text(self):
        text = self.quantity_box.text()
        # self.quantity = FreeCAD.Units.parseQuantity(text)
        res = re.findall("([\.0-9-]*)", text)
        return res[0]