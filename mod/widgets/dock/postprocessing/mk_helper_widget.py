from PySide2 import QtWidgets, QtCore
from mod.dataobjects.case import Case
from mod.enums import ObjectType
from mod.tools.freecad_tools import get_fc_object


class MkHelperWidget(QtWidgets.QWidget):

    def __init__(self):
        super().__init__()
        self.main_layout = QtWidgets.QVBoxLayout()
        self.mk_list_button=QtWidgets.QPushButton("Show Mk List")
        self.mk_list_button.setMaximumWidth(90)
        self.mk_list_button.clicked.connect(self.on_help_list)
        self.scroll_area = QtWidgets.QScrollArea()
        self.mk_list_label = QtWidgets.QLabel()

        self.scroll_area.setWidget(self.mk_list_label)

        self.main_layout.addWidget(self.mk_list_button)
        self.main_layout.addWidget(self.scroll_area)

        self.setLayout(self.main_layout)

        self.scroll_area.setVisible(False)
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.setMinimumWidth(400)
        self.scroll_area.setMaximumHeight(400)
        self.update_mk_info()

    def update_mk_info(self):
        mklist = Case.the().objects
        info = ""
        for obj in mklist:
            if (obj.type != ObjectType.SPECIAL):
                info += f"mk: {obj.real_mk():03d}: (mk{obj.type} {obj.obj_mk:03d}) -{get_fc_object(obj.name).Label} ({obj.name}) \n"
        self.mk_list_label.setText(info)

    def on_help_list(self):
        if self.scroll_area.isVisible():
            self.mk_list_button.setText("Show Mk List")
            self.scroll_area.setVisible(False)
        else:
            self.mk_list_button.setText("Hide Mk List")
            self.update_mk_info()
            self.scroll_area.setVisible(True)



