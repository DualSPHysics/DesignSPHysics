from PySide2.QtWidgets import QDoubleSpinBox
from PySide2.QtGui import QValidator

from mod.tools.stdout_tools import debug

class UnitSpinBox(QDoubleSpinBox):
    def __init__(self, pre_unit="", unit="",pos_unit="", parent=None):
        super().__init__(parent)
        self.pre_unit = pre_unit
        self.pos_unit = pos_unit
        self.unit = unit
        self.setUnit(self.unit)

    def textFromValue(self, value):
        return f"{value}"

    def valueFromText(self, text):
        return float(text.strip().replace(f" {self.unit}", ""))

    def validate(self, text, pos):
        stripped = text.strip().replace(f" {self.unit}", "")
        try:
            float(stripped)
            return (QValidator.State.Acceptable, text, pos)
        except ValueError:
            return (QValidator.State.Intermediate, text, pos)

    def focusInEvent(self, event):
        # Remove suffix during editing
        # self.setSuffix("")
        super().focusInEvent(event)

    def focusOutEvent(self, event):
        # Restore suffix after editing
        super().focusOutEvent(event)
        # self.setSuffix(f" {self.unit}")

    def textFromValue(self, value):
        # return f"{value:.2f} {self.unit}"
        return f"{value}"

    def valueFromText(self, text):
        try:
            return float(text.strip().replace(str(self.unit), "").strip())
        except ValueError:
            return 0.0
    
    def getUnit(self):
        return f"{self.unit}"

    def setUnit(self, unit):
        self.unit = self.pre_unit+unit+self.pos_unit
        self.setSuffix("")
        self.setSuffix(f" {self.unit}")
        self.update()
    
    def setMagnitude(self, pre_unit, pos_unit):
        self.pre_unit = pre_unit
        self.pos_unit = pos_unit
        self.setUnit(self.unit)