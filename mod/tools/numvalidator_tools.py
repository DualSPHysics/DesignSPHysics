#!/usr/bin/env python3.7
# -*- coding: utf-8 -*-
""" General number validators to be used in DesingSPHysics."""

from PySide2 import QtCore,QtGui

class FloatValidator(QtGui.QValidator):
    """ Validates float numbers """

    def __init__(self, min_val=-10e12, max_val=10e12):
        super().__init__()
        if min_val>max_val :
            min_val=max_val-1
        self.min_val = min_val
        self.max_val = max_val

    def validate(self, arg_1, arg_2):
        #validrx = QtCore.QRegularExpression("^-?\d+(\.\d+)?$")
        validrx = QtCore.QRegularExpression("^-?[1-9][0-9]*(\.\d+)?$|^-?0\.\d+$|^0$")
        #intermediaterx = QtCore.QRegularExpression("^-?\d+\.?\d*$|^$") #"^-?\d+\.?\d*$"
        intermediaterx = QtCore.QRegularExpression("^-?[0-9]*(\.\d*)?$|^-?0\.\d*$|^-?0?$")  # "^-?\d+\.?\d*$"
        if validrx.match(arg_1).hasMatch():
            val=float(arg_1)
            if self.min_val>=0:
                if 0 < val < self.min_val:
                    valid_exp = QtGui.QValidator.State.Intermediate
                elif self.min_val <= val <= self.max_val:
                    valid_exp = QtGui.QValidator.State.Acceptable
                else:
                    valid_exp = QtGui.QValidator.State.Invalid
            elif self.min_val < 0 <= self.max_val:
                if self.min_val<=val<=self.max_val:
                    valid_exp = QtGui.QValidator.State.Acceptable
                else:
                    valid_exp = QtGui.QValidator.State.Invalid
            else:
                if 0 > val > self.max_val:
                    valid_exp = QtGui.QValidator.State.Intermediate
                elif self.max_val >= val >= self.min_val:
                    valid_exp = QtGui.QValidator.State.Acceptable
                else:
                    valid_exp = QtGui.QValidator.State.Invalid
        elif intermediaterx.match(arg_1).hasMatch():
            valid_exp = QtGui.QValidator.State.Intermediate
        else:
            valid_exp = QtGui.QValidator.State.Invalid
        return valid_exp


class IntValidator(QtGui.QValidator):
    """ Validates integer numbers """

    def __init__(self, min_val=0, max_val=999999999):
        super().__init__()
        if min_val>max_val :
            min_val=max_val-1
        self.min_val = min_val
        self.max_val = max_val

    def validate(self, arg_1, arg_2):
        if self.min_val<0 :
            validrx = QtCore.QRegularExpression("^-?[1-9][0-9]*$|^0$")
            intermediaterx = QtCore.QRegularExpression("^-$")
        elif self.min_val>0:
            validrx = QtCore.QRegularExpression("^[1-9][0-9]*$")
            intermediaterx = QtCore.QRegularExpression("^$")
        else:
            validrx = QtCore.QRegularExpression("^[1-9][0-9]*$|^0$")
            intermediaterx = QtCore.QRegularExpression("^$")
        if validrx.match(arg_1).hasMatch():
            val=int(arg_1)
            if self.min_val>=0:
                if 0 < val < self.min_val:
                    valid_exp = QtGui.QValidator.State.Intermediate
                elif self.min_val <= val <= self.max_val:
                    valid_exp = QtGui.QValidator.State.Acceptable
                else:
                    valid_exp = QtGui.QValidator.State.Invalid
            elif self.min_val<0 and self.max_val>=0:
                if self.min_val<=val<=self.max_val:
                    valid_exp = QtGui.QValidator.State.Acceptable
                else:
                    valid_exp = QtGui.QValidator.State.Invalid
            else:
                if 0 > val > self.max_val:
                    valid_exp = QtGui.QValidator.State.Intermediate
                elif self.max_val >= val >= self.min_val:
                    valid_exp = QtGui.QValidator.State.Acceptable
                else:
                    valid_exp = QtGui.QValidator.State.Invalid
        elif intermediaterx.match(arg_1).hasMatch():
            valid_exp = QtGui.QValidator.State.Intermediate
        else:
            valid_exp = QtGui.QValidator.State.Invalid
        return valid_exp

class FloatOpValidator(QtGui.QValidator):

    def __init__(self):
        super().__init__()

    def validate(self, arg_1, arg_2):
        #validrx = QtCore.QRegularExpression("^-?\d+(\.\d+)?$")
        validrx = QtCore.QRegularExpression("^-?[1-9][0-9]*(\.\d+)?$|^-?0\.\d+$|^0|#.*$")
        #intermediaterx = QtCore.QRegularExpression("^-?\d+\.?\d*$|^$") #"^-?\d+\.?\d*$"
        intermediaterx = QtCore.QRegularExpression("^-?[0-9]*(\.\d*)?$|^-?0\.\d*$|^-?0?|#.*$")  # "^-?\d+\.?\d*$"
        if arg_1[0] != '#':
            if validrx.match(arg_1).hasMatch():
                valid_exp = QtGui.QValidator.State.Acceptable
            elif intermediaterx.match(arg_1).hasMatch():
                valid_exp = QtGui.QValidator.State.Intermediate
            else:
                valid_exp = QtGui.QValidator.State.Invalid
        else:
            if validrx.match(arg_1).hasMatch():
                valid_exp = QtGui.QValidator.State.Acceptable
            elif intermediaterx.match(arg_1).hasMatch():
                valid_exp = QtGui.QValidator.State.Intermediate
            else:
                valid_exp = QtGui.QValidator.State.Invalid
        return valid_exp

class VarNameValidator(QtGui.QValidator):
    def __init__(self):
        super().__init__()

    def validate(self, arg_1, arg_2):
        validrx = QtCore.QRegularExpression("^[a-zA-Z]\w*$")
        intermediaterx = QtCore.QRegularExpression("^[a-zA-Z]\w*$")  # "^-?\d+\.?\d*$"
        if validrx.match(arg_1).hasMatch():
            valid_exp = QtGui.QValidator.State.Acceptable
        elif intermediaterx.match(arg_1).hasMatch():
            valid_exp = QtGui.QValidator.State.Intermediate
        else:
            valid_exp = QtGui.QValidator.State.Invalid
        return valid_exp