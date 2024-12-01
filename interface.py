import os
import platform
from pathlib import Path
import sys

import maya.cmds as cmds
from maya import OpenMayaUI as omui

try:
    from PySide6.QtCore import Qt, QObject, SIGNAL
    from PySide6.QtWidgets import (QWidget,
                                   QHBoxLayout,
                                   QFormLayout,
                                   QPushButton,
                                   QLabel,
                                   QLineEdit,
                                   QFileDialog)
    from shiboken6 import wrapInstance
except ModuleNotFoundError:
    from PySide2.QtCore import Qt, QObject, SIGNAL
    from PySide2.QtWidgets import (QWidget,
                                   QHBoxLayout,
                                   QFormLayout,
                                   QPushButton,
                                   QLabel,
                                   QLineEdit,
                                   QFileDialog)
    from shiboken2 import wrapInstance

mayaMainWindowPtr = omui.MQtUtil.mainWindow()
mayaMainWindow = wrapInstance(int(mayaMainWindowPtr), QWidget)

class Interface(QWidget):
    def __init__(self, *args, **kwargs):
        super(Interface,self).__init__(*args, **kwargs)
        self.setParent(mayaMainWindow)
        self.setWindowFlags(Qt.Window)
        self.setFixedWidth(290)
        self.setFixedHeight(140)
        self.setWindowTitle("Maya_USD_Export")

        # default export path
        self.file_output_path = os.getcwd()
        self.initUI()

    def initUI(self):
        self.main_layout_widget = QWidget(self)
        self.main_layout_widget.setMaximumWidth(500)
        self.main_layout = QFormLayout(self.main_layout_widget)
        self.main_layout.setLabelAlignment(Qt.AlignLeft | Qt.AlignVCenter)

        self.file_path_label = QLabel("File Path:")
        self.file_path_layout = QHBoxLayout()
        self.file_path_lineedit = QLineEdit(self.file_output_path)
        self.file_path_lineedit.setObjectName("file_path_lineedit")
        self.file_path_button =  QPushButton("Change")
        self.file_path_button.setObjectName("file_path_button")
        self.file_path_button.clicked.connect(self.open_file_dialog)
        self.file_path_layout.addWidget(self.file_path_lineedit)
        self.file_path_layout.addWidget(self.file_path_button)

        self.shot_num_label = QLabel("Shot Num:")
        self.shot_num_lineedit = QLineEdit("1")
        self.shot_num_lineedit.setObjectName("shot_number")

        self.asset_ver_label = QLabel("Asset Version:")
        self.asset_ver_lineedit = QLineEdit("1")
        self.asset_ver_lineedit.setObjectName("asset_version")

        self.export_asset_button = QPushButton("Export USD")
        self.export_asset_button.setObjectName("export_usd")

        self.main_layout.addRow(self.file_path_label, self.file_path_layout)
        self.main_layout.addRow(self.shot_num_label, self.shot_num_lineedit)
        self.main_layout.addRow(self.asset_ver_label, self.asset_ver_lineedit)
        self.main_layout.addRow(self.export_asset_button)

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

