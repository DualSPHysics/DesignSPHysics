#!/usr/bin/env python3.7
# -*- coding: utf-8 -*-
'''DesignSPHysics Faces Configuration Dialog'''

from traceback import print_exc

from PySide import QtCore, QtGui

from mod.translation_tools import __

from mod.dataobjects.faces_property import FacesProperty

# FIXME: Change Data references for the new refactored Case

class FacesDialog(QtGui.QDialog):
    ''' Defines a window with faces  '''

    def __init__(self, selection_name):
        super(FacesDialog, self).__init__()

        self.setWindowTitle(__("Faces configuration"))
        self.ok_button = QtGui.QPushButton(__("Ok"))
        self.cancel_button = QtGui.QPushButton(__("Cancel"))
        self.main_faces_layout = QtGui.QVBoxLayout()

        self.target_mk = int(self.data['simobjects'][selection_name][0])
        self.name = selection_name

        self.button_layout = QtGui.QHBoxLayout()
        self.button_layout.addWidget(self.ok_button)
        self.button_layout.addWidget(self.cancel_button)
        self.ok_button.clicked.connect(self.on_ok)
        self.cancel_button.clicked.connect(self.on_cancel)

        self.faces_layout = QtGui.QVBoxLayout()

        self.all_faces = QtGui.QCheckBox(__("All faces"))
        self.all_faces.setCheckState(QtCore.Qt.Checked)
        self.all_faces.toggled.connect(self.on_faces_checkbox)

        self.front_face = QtGui.QCheckBox(__("Front face"))

        self.back_face = QtGui.QCheckBox(__("Back face"))

        self.top_face = QtGui.QCheckBox(__("Top face"))

        self.bottom_face = QtGui.QCheckBox(__("Bottom face"))

        self.left_face = QtGui.QCheckBox(__("Left face"))

        self.right_face = QtGui.QCheckBox(__("Right face"))

        try:
            if (str(self.target_mk), self.name) in self.data['faces'].keys():
                if self.data['faces'][str(self.target_mk), self.name].all_faces:
                    self.all_faces.setCheckState(QtCore.Qt.Checked)
                else:
                    self.all_faces.setCheckState(QtCore.Qt.Unchecked)
                self.all_faces.toggled.connect(self.on_faces_checkbox)

                if self.data['faces'][str(self.target_mk), self.name].front_face:
                    self.front_face.setCheckState(QtCore.Qt.Checked)
                else:
                    self.front_face.setCheckState(QtCore.Qt.Unchecked)

                if self.data['faces'][str(self.target_mk), self.name].back_face:
                    self.back_face.setCheckState(QtCore.Qt.Checked)
                else:
                    self.back_face.setCheckState(QtCore.Qt.Unchecked)

                if self.data['faces'][str(self.target_mk), self.name].top_face:
                    self.top_face.setCheckState(QtCore.Qt.Checked)
                else:
                    self.top_face.setCheckState(QtCore.Qt.Unchecked)

                if self.data['faces'][str(self.target_mk), self.name].bottom_face:
                    self.bottom_face.setCheckState(QtCore.Qt.Checked)
                else:
                    self.bottom_face.setCheckState(QtCore.Qt.Unchecked)

                if self.data['faces'][str(self.target_mk), self.name].left_face:
                    self.left_face.setCheckState(QtCore.Qt.Checked)
                else:
                    self.left_face.setCheckState(QtCore.Qt.Unchecked)

                if self.data['faces'][str(self.target_mk), self.name].right_face:
                    self.right_face.setCheckState(QtCore.Qt.Checked)
                else:
                    self.right_face.setCheckState(QtCore.Qt.Unchecked)
        except:
            print_exc()
            self.all_faces.setCheckState(QtCore.Qt.Checked)

        self.faces_layout.addWidget(self.all_faces)
        self.faces_layout.addWidget(self.front_face)
        self.faces_layout.addWidget(self.back_face)
        self.faces_layout.addWidget(self.top_face)
        self.faces_layout.addWidget(self.bottom_face)
        self.faces_layout.addWidget(self.left_face)
        self.faces_layout.addWidget(self.right_face)

        self.main_faces_layout.addLayout(self.faces_layout)
        self.main_faces_layout.addLayout(self.button_layout)

        self.setLayout(self.main_faces_layout)

        self.on_faces_checkbox()

        self.exec_()

    def on_ok(self):

        fp = FacesProperty()
        fp.mk = self.target_mk

        if self.all_faces.isChecked():
            fp.all_faces = True
            fp.back_face = False
            fp.front_face = False
            fp.top_face = False
            fp.bottom_face = False
            fp.left_face = False
            fp.right_face = False
            fp.face_print = 'all'
        else:
            fp.all_faces = False

            if self.front_face.isChecked():
                fp.front_face = True
                fp.face_print = 'front'
            else:
                fp.front_face = False

            if self.back_face.isChecked():
                fp.back_face = True
                if fp.face_print != '':
                    fp.face_print += ' | back'
                else:
                    fp.face_print = 'back'
            else:
                fp.back_face = False

            if self.top_face.isChecked():
                fp.top_face = True
                if fp.face_print != '':
                    fp.face_print += ' | top'
                else:
                    fp.face_print = 'top'
            else:
                fp.top_face = False

            if self.bottom_face.isChecked():
                fp.bottom_face = True
                if fp.face_print != '':
                    fp.face_print += ' | bottom'
                else:
                    fp.face_print = 'bottom'
            else:
                fp.bottom_face = False

            if self.left_face.isChecked():
                fp.left_face = True
                if fp.face_print != '':
                    fp.face_print += ' | left'
                else:
                    fp.face_print = 'left'
            else:
                fp.left_face = False

            if self.right_face.isChecked():
                fp.right_face = True
                if fp.face_print != '':
                    fp.face_print += ' | right'
                else:
                    fp.face_print = 'right'
            else:
                fp.right_face = False

        self.data['faces'][str(self.target_mk), self.name] = fp

        self.accept()

    def on_cancel(self):
        self.reject()

    def on_faces_checkbox(self):
        ''' Checks the faces state '''
        if self.all_faces.isChecked():
            self.front_face.setEnabled(False)
            self.back_face.setEnabled(False)
            self.top_face.setEnabled(False)
            self.bottom_face.setEnabled(False)
            self.left_face.setEnabled(False)
            self.right_face.setEnabled(False)
        else:
            self.front_face.setEnabled(True)
            self.back_face.setEnabled(True)
            self.top_face.setEnabled(True)
            self.bottom_face.setEnabled(True)
            self.left_face.setEnabled(True)
            self.right_face.setEnabled(True)
