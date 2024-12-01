import os
import platform
from pathlib import Path
import sys

import maya.cmds as cmds
from maya import OpenMayaUI as omui

import importlib

pyside_versions = ["PySide6", "PySide2"]

for version in pyside_versions:
    print("Trying pyside version:", version)
    try:
        sys.modules["PySide"] = importlib.import_module(version)
        sys.modules["PySide.QtCore"] = importlib.import_module(f"{version}.QtCore")
        sys.modules["PySide.QtWidgets"] = importlib.import_module(f"{version}.QtWidgets")
        shiboken = importlib.import_module(f"shiboken{version[-1]}")
        wrapInstance = shiboken.wrapInstance

        print("Successful import of", version)
        break
    except ModuleNotFoundError:
        continue
else:
    raise ModuleNotFoundError("No PySide module found.")

from PySide.QtCore import Qt, QObject, SIGNAL
from PySide.QtWidgets import (
    QWidget,
    QHBoxLayout,
    QFormLayout,
    QPushButton,
    QLabel,
    QVBoxLayout,
    QLineEdit,
    QFileDialog,
    QSpacerItem,
    QSizePolicy,
)


class Interface(QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # parent to maya interface
        mayaMainWindowPtr = omui.MQtUtil.mainWindow()
        mayaMainWindow = wrapInstance(int(mayaMainWindowPtr), QWidget)
        self.setParent(mayaMainWindow)
        self.setWindowFlags(Qt.Window)

        # set size hinting
        self.resize(290, 140)
        self.setMaximumWidth(600)
        self.setMaximumHeight(140)

        self.setWindowTitle("Maya_USD_Export")

        # default export path
        self.file_output_path = os.getcwd()
        self.initUI()

    def initUI(self):
        # create layouts
        self.main_layout = QVBoxLayout(self)
        self.form_layout = QFormLayout()
        # place form layout in main layout
        self.main_layout.addLayout(self.form_layout)
        self.form_layout.setLabelAlignment(Qt.AlignLeft | Qt.AlignVCenter)

        self.file_path_layout = QHBoxLayout()
        self.file_path_lineedit = QLineEdit(self.file_output_path)
        self.file_path_lineedit.setObjectName("file_path_lineedit")
        self.file_path_button =  QPushButton("Change")
        self.file_path_button.setObjectName("file_path_button")
        self.file_path_button.clicked.connect(self.open_file_dialog)
        self.file_path_layout.addWidget(self.file_path_lineedit)
        self.file_path_layout.addWidget(self.file_path_button)

        self.shot_num_lineedit = QLineEdit("0001")
        self.shot_num_lineedit.setObjectName("shot_number")

        self.asset_ver_lineedit = QLineEdit("1")
        self.asset_ver_lineedit.setObjectName("asset_version")

        self.export_asset_button = QPushButton("Export USD")
        self.export_asset_button.setObjectName("export_usd")

        # add form items
        self.form_layout.addRow("File Path:", self.file_path_layout)
        self.form_layout.addRow("Shot Num:", self.shot_num_lineedit)
        self.form_layout.addRow("Asset Version:", self.asset_ver_lineedit)
        self.form_layout.addRow(self.export_asset_button)

        stylesheet_path = os.path.join(os.path.dirname(os.path.abspath(__file__)),"style.css")
        with open(stylesheet_path, "r") as file:
            stylesheet = file.read()
        self.setStyleSheet(stylesheet)

    def open_file_dialog(self):
        file_path = QFileDialog.getExistingDirectory(self, "Select Directory", dir=self.file_output_path)
        if file_path:
            self.file_path_lineedit.setText(file_path) 
            self.file_output_path = file_path

def start_interface():
    ui = Interface()
    ui.show()

