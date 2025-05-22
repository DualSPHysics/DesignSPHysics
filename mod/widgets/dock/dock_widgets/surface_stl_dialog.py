import os.path
import shutil
from os import path, walk, chdir
from os.path import dirname

from PySide2 import QtWidgets, QtCore
from mod.dataobjects.case import Case
from mod.tools.dialog_tools import WaitDialog, warning_dialog, ok_cancel_dialog, info_dialog
from mod.tools.executable_tools import refocus_cwd, ensure_process_is_executable_or_fail
from mod.tools.freecad_tools import get_fc_main_window
from mod.tools.stdout_tools import log, debug
from mod.tools.translation_tools import __


def delete_vtm(vtm_file):
    """ Deletes vtm file and folder with vtus/vtps. """
    folder=vtm_file.removesuffix('.vtm')
    if path.isdir(folder):
        shutil.rmtree(str("{}".format(folder)))
        os.remove(vtm_file)


class SurfaceStlDialog(QtWidgets.QDialog):
    def __init__(self,file_name,parent=None):
        super().__init__(parent)
        self.file_name=file_name
        self.setWindowTitle(__("Surface STL Parameters"))
        self.main_layout=QtWidgets.QVBoxLayout()
        self.parameters_layout=QtWidgets.QVBoxLayout()
        self.buttons_layout=QtWidgets.QHBoxLayout()

        self.full_vtk_checkbox = QtWidgets.QCheckBox(__("Full surface vtk"))
        self.sep_vtks_checkbox = QtWidgets.QCheckBox(__("Separated surfaces vtks"))
        self.vtp_checkbox = QtWidgets.QCheckBox(__("Export surfaces as vtp (default vtu)"))
        for x in [self.full_vtk_checkbox,self.sep_vtks_checkbox]:#,self.vtp_checkbox]:
            self.parameters_layout.addWidget(x)

        self.ok_button = QtWidgets.QPushButton(__("OK"))
        self.cancel_button = (QtWidgets.QPushButton(__("Cancel")))
        self.buttons_layout.addWidget(self.ok_button)
        self.buttons_layout.addWidget(self.cancel_button)
        self.ok_button.clicked.connect(self.on_ok)
        self.cancel_button.clicked.connect(self.on_cancel)

        self.main_layout.addLayout(self.parameters_layout)
        self.main_layout.addLayout(self.buttons_layout)

        self.setLayout(self.main_layout)

    def on_ok(self):
        """ Applies the data from the dialog onto the main data structure. """

        wait_dialog = WaitDialog("SurfaceSTL is running.please wait")
        wait_dialog.show()
        if not Case.the().executable_paths.surfacesstl:
            warning_dialog(__("SurfaceSTL executable is not set."))
            return
        refocus_cwd()
        surfacesstl_full_path = path.abspath(Case.the().executable_paths.surfacesstl)
        arguments = [self.file_name,
                     f"-savevtk:{1 if self.full_vtk_checkbox.isChecked() else 0}",
                     f"-savevtks:{1 if self.sep_vtks_checkbox.isChecked() else 0}",
                     "-savesurfs:{ext}".format(ext="vtp" if self.vtp_checkbox.isChecked() else "vtu")
                     ]
        cmd_string = "{} {}".format(surfacesstl_full_path, " ".join(arguments))

        # Check if the case was already generated
        filedir = dirname(self.file_name)
        file_out=os.path.basename(self.file_name).replace("stl","vtm")
        #if Case.the().path:
        #    dir = Case.the().path
        #else:
        dir = filedir
        vtmout=f"{dir}{os.sep}{file_out}"
        if path.exists(vtmout):
            execute_surfacesstl = ok_cancel_dialog(__("Remove previous vtm files"),
                                               __(f"File {vtmout} already exists.This action will remove the data generated before.\n\nPress Ok to remove and run SurfaceSTL.\nPress Cancel to exit and keep the data."))
            # Decision dialog to remove data before running GenCase
            if execute_surfacesstl == QtWidgets.QMessageBox.Cancel:
                return
            else:
                delete_vtm(vtmout)

        refocus_cwd()
        process = QtCore.QProcess(get_fc_main_window())
        process.setWorkingDirectory(dir)
        ensure_process_is_executable_or_fail(surfacesstl_full_path)
        process.start(surfacesstl_full_path, arguments)
        log("Executing -> {}".format(cmd_string))
        # info_dialog("Executing GenCase")
        #process.waitForFinished(msecs=3600000)

        def on_surface_stl_finished(exit_code):
            try:
                output = str(process.readAllStandardOutput().data(), encoding='utf-8')
            except UnicodeDecodeError:
                output = str(process.readAllStandardOutput().data(), encoding='latin1')

            if exit_code == 0:
                info_dialog(f"SurfaceSTl executing successfully finished.{os.linesep}"
                            f"Files saved in {os.path.abspath(process.workingDirectory())}", output)
            else:
                if output.find("Text: Key 'solid' not found at line 0"):
                    warning_dialog(f"SurfaceSTl only works with ASCII .stl files with surfaces")
                else:
                    warning_dialog(f"SurfaceSTl executing failed. with code {exit_code}", output)
                wait_dialog.close_dialog()
                return

            wait_dialog.close_dialog()
            refocus_cwd()
            self.accept()

        process.finished.connect(on_surface_stl_finished)

    def on_cancel(self):
        """ Cancels the dialog rejecting it. """
        self.reject()


