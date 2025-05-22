from PySide2 import QtWidgets
from mod.dataobjects.case import Case
from mod.tools.dialog_tools import ok_cancel_dialog, error_dialog
from mod.tools.freecad_tools import manage_vres_bufferboxes
from mod.tools.translation_tools import __
from mod.tools.stdout_tools import debug

from mod.widgets.custom_widgets.value_input import ValueInput
from mod.widgets.dock.special_widgets.variable_res.bufferbox_edit_dialog import BufferboxEditDialog


class VariableResConfigDialog(QtWidgets.QDialog):

    def __init__(self,parent):
        super().__init__(parent=parent)

        self.setWindowTitle(__("Variable resolution buffer box list"))
        self.main_layout = QtWidgets.QVBoxLayout()

        self.active_layout = QtWidgets.QHBoxLayout()
        self.active_label = QtWidgets.QLabel(__("Active"))
        self.active_checkbox = QtWidgets.QCheckBox()
        self.active_layout.addWidget(self.active_label)
        self.active_layout.addWidget(self.active_checkbox)

        self.buffer_size_layout=QtWidgets.QHBoxLayout()
        self.buffer_size_label = QtWidgets.QLabel(__("Buffer size (h)"))
        self.buffer_size_input = ValueInput()
        self.buffer_size_layout.addWidget(self.buffer_size_label)
        self.buffer_size_layout.addWidget(self.buffer_size_input)

        self.list_layout = QtWidgets.QHBoxLayout()
        self.buffer_boxs_list=QtWidgets.QListWidget()
        self.list_layout.addWidget(self.buffer_boxs_list)

        self.buttons_layout = QtWidgets.QHBoxLayout()
        self.add_buffer_box_button = QtWidgets.QPushButton(__("Add buffer_box"))
        self.add_buffer_box_button.clicked.connect(self.on_add_buffer_box)
        self.edit_buffer_box_button = QtWidgets.QPushButton(__("Edit buffer_box"))
        self.edit_buffer_box_button.clicked.connect(self.on_edit)
        self.delete_buffer_box_button = QtWidgets.QPushButton(__("Delete buffer_box"))
        self.delete_buffer_box_button.clicked.connect(self.on_delete)
        self.ok_button = QtWidgets.QPushButton(text=__("OK"))
        self.ok_button.clicked.connect(self.on_ok)
        self.buttons_layout.addWidget(self.add_buffer_box_button)
        self.buttons_layout.addWidget(self.edit_buffer_box_button)
        self.buttons_layout.addWidget(self.delete_buffer_box_button)
        self.buttons_layout.addWidget(self.ok_button)

        self.main_layout.addLayout(self.active_layout)
        self.main_layout.addLayout(self.buffer_size_layout)
        self.main_layout.addLayout(self.list_layout)
        self.main_layout.addLayout(self.buttons_layout)
        self.setLayout(self.main_layout)

        self.buffer_size_input.setValue(Case.the().vres.vres_buffer_size_h)
        self.active_checkbox.setChecked(Case.the().vres.active)
        self.active_checkbox.stateChanged.connect(self.on_activate)
        self.buffer_boxs_list.itemSelectionChanged.connect(self.on_selection_change)
        self.edit_buffer_box_button.setEnabled(False)
        self.delete_buffer_box_button.setEnabled(False)

        manage_vres_bufferboxes(Case.the().vres.bufferbox_list)
        self.update_buffer_boxs_list()

        self.on_activate(Case.the().vres.active)

    def on_ok(self):
        Case.the().vres.vres_buffer_size_h=self.buffer_size_input.value()
        Case.the().vres.active = self.active_checkbox.isChecked()
        self.accept()

    def on_cancel(self):
        self.reject()

    def on_add_buffer_box(self):
        bufferbox=Case.the().vres.add_bufferbox()
        buff_list=Case.the().vres.bufferbox_list.copy()
        if bufferbox in buff_list:
            buff_list.remove(bufferbox) # Deletes current bufferbox
        wavegen_enabled = sum(1 for buff in buff_list if buff.vreswavegen)
        dialog = BufferboxEditDialog(bufferbox,parent=None,wavegenavail=wavegen_enabled==0)
        ret = dialog.exec_()
        if ret != 1:
            id=bufferbox.id
            Case.the().vres.remove_bufferbox(id)
        self.update_buffer_boxs_list()

    def update_buffer_boxs_list(self):
        self.buffer_boxs_list.clear()
        buff_list=Case.the().vres.bufferbox_list.copy()
        remove_buff=[]
        for buff in buff_list:
            if buff.parent:
                remove_buff.append(buff)
   
        if remove_buff:
            for rem in remove_buff:
                buff_list.remove(rem)

        while buff_list:
            buffer_box= buff_list.pop(0)
            sons = Case.the().vres.get_children(buffer_box.id)
            for son in sons:
                if son in buff_list:
                    buff_list.remove(son)
                buff_list.insert(0,son)
            if buffer_box.parent:
                buffer_box.depth=buffer_box.parent.depth + 1
            self.buffer_boxs_list.addItem(self.spaces(buffer_box.depth) + str(buffer_box.id)) #Add spacings
        self.buffer_boxs_list.setCurrentRow(0)

    def on_edit(self):
        id = int(self.buffer_boxs_list.currentItem().text())
        bufferbox=Case.the().vres.bufferbox_list[id]
        buff_list=Case.the().vres.bufferbox_list.copy()
        if bufferbox in buff_list:
            buff_list.remove(bufferbox) # Deletes current bufferbox
        wavegen_enabled = sum(1 for buff in buff_list if buff.vreswavegen)
        dialog = BufferboxEditDialog(bufferbox,parent=None,wavegenavail=wavegen_enabled==0)
        dialog.exec_()

        self.update_buffer_boxs_list()

    def on_delete(self):
        id = int(self.buffer_boxs_list.currentItem().text())
        if Case.the().vres.get_children(id):
            ret = ok_cancel_dialog("Warning","Children will also be deleted")
            if ret==QtWidgets.QDialog.Accepted: # 1024
                Case.the().vres.remove_with_children(id)
        else:
            Case.the().vres.remove_bufferbox(id)
        self.update_buffer_boxs_list()

    def spaces(self,n:int):
        space=""
        for i in range(n):
            space=space + "  "
        return space

    def on_activate(self,active):
        for x in [self.buffer_size_input,self.buffer_boxs_list,self.add_buffer_box_button,self.edit_buffer_box_button,
                  self.delete_buffer_box_button]:
            x.setEnabled(active)
        if active:
            self.on_selection_change()

    def on_selection_change(self):
        if self.buffer_boxs_list.selectedItems():
            self.edit_buffer_box_button.setEnabled(True)
            self.delete_buffer_box_button.setEnabled(True)
        else :
            self.edit_buffer_box_button.setEnabled(False)
            self.delete_buffer_box_button.setEnabled(False)
