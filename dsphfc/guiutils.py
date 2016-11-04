# -*- coding: utf-8 -*-

'''
Copyright (C) 2016 - Andrés Vieira (anvieiravazquez@gmail.com)
EPHYSLAB Environmental Physics Laboratory, Universidade de Vigo

This file is part of DualSPHysics for FreeCAD.

DualSPHysics for FreeCAD is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

DualSPHysics for FreeCAD is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with DualSPHysics for FreeCAD.  If not, see <http://www.gnu.org/licenses/>.
'''

from PySide import QtGui, QtCore

def warning_dialog(warn_text):
	exec_not_correct_dialog = QtGui.QMessageBox()
	exec_not_correct_dialog.setText(warn_text)
	exec_not_correct_dialog.setIcon(QtGui.QMessageBox.Warning)
	exec_not_correct_dialog.exec_()

def ok_cancel_dialog(title, text):
	openConfirmDialog = QtGui.QMessageBox()
	openConfirmDialog.setText(title)
	openConfirmDialog.setInformativeText(text)
	openConfirmDialog.setStandardButtons(QtGui.QMessageBox.Ok | QtGui.QMessageBox.Cancel)
	openConfirmDialog.setDefaultButton(QtGui.QMessageBox.Ok)
	return openConfirmDialog.exec_()