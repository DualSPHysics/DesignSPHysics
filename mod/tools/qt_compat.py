"""Qt compatibility helpers for FreeCAD environments.

This module prefers PySide6 (used by newer FreeCAD versions) and
falls back to PySide2 for older releases.
"""

try:
    from PySide6 import QtCore, QtGui, QtWidgets  # type: ignore
    from PySide6.QtCore import QObject, Signal, Slot  # type: ignore
    from PySide6.QtGui import QAction, QValidator  # type: ignore
    from PySide6.QtWidgets import QDialog, QDoubleSpinBox, QHBoxLayout, QWidget  # type: ignore
except ImportError:
    from mod.tools.qt_compat import QtCore, QtGui, QtWidgets  # type: ignore
    from PySide2.QtCore import QObject, Signal, Slot  # type: ignore
    from mod.tools.qt_compat import QValidator  # type: ignore
    from mod.tools.qt_compat import QAction, QDialog, QDoubleSpinBox, QHBoxLayout, QWidget  # type: ignore


# Qt6 removed several Qt5 aliases commonly used by legacy plugins.
if not hasattr(QtWidgets.QHeaderView, "setResizeMode") and hasattr(QtWidgets.QHeaderView, "setSectionResizeMode"):
    def _set_resize_mode(self, *args):
        return self.setSectionResizeMode(*args)

    try:
        QtWidgets.QHeaderView.setResizeMode = _set_resize_mode  # type: ignore[attr-defined]
    except (AttributeError, TypeError):
        pass


if not hasattr(QtWidgets.QDialog, "exec_") and hasattr(QtWidgets.QDialog, "exec"):
    try:
        QtWidgets.QDialog.exec_ = QtWidgets.QDialog.exec  # type: ignore[attr-defined]
    except (AttributeError, TypeError):
        pass


if hasattr(QtWidgets, "QApplication") and not hasattr(QtWidgets.QApplication, "exec_") and hasattr(QtWidgets.QApplication, "exec"):
    try:
        QtWidgets.QApplication.exec_ = QtWidgets.QApplication.exec  # type: ignore[attr-defined]
    except (AttributeError, TypeError):
        pass


__all__ = [
    "QtCore",
    "QtGui",
    "QtWidgets",
    "Signal",
    "Slot",
    "QObject",
    "QAction",
    "QDialog",
    "QDoubleSpinBox",
    "QHBoxLayout",
    "QValidator",
    "QWidget",
]
