import os
import platform
from pathlib import Path

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
        self.initUI()
        self.setFixedWidth(290)
        self.setFixedHeight(140)
        self.setWindowTitle("Maya_USD_Export")

    def initUI(self):
        self.main_layout_widget = QWidget(self)
        self.main_layout_widget.setMaximumWidth(500)
        self.main_layout = QFormLayout(self.main_layout_widget)
        self.main_layout.setLabelAlignment(Qt.AlignLeft | Qt.AlignVCenter)

        file_path_label = QLabel("File Path:")
        file_path_layout = QHBoxLayout()
        file_path_lineedit = QLineEdit("tmp_file_path")
        file_path_lineedit.setObjectName("file_path_lineedit")
        file_path_button =  QPushButton("Change")
        file_path_button.setObjectName("file_path_button")
        file_path_layout.addWidget(file_path_lineedit)
        file_path_layout.addWidget(file_path_button)

        shot_num_label = QLabel("Shot Num:")
        shot_num_lineedit = QLineEdit("1")
        shot_num_lineedit.setObjectName("shot_number")

        asset_ver_label = QLabel("Asset Version:")
        asset_ver_lineedit = QLineEdit("1")
        asset_ver_lineedit.setObjectName("asset_version")

        export_asset_button = QPushButton("Export USD")
        export_asset_button.setObjectName("export_usd")

        self.main_layout.addRow(file_path_label, file_path_layout)
        self.main_layout.addRow(shot_num_label, shot_num_lineedit)
        self.main_layout.addRow(asset_ver_label, asset_ver_lineedit)
        self.main_layout.addRow(export_asset_button)

        stylesheet_path = os.path.join(os.path.dirname(os.path.abspath(__file__)),"style.css")
        with open(stylesheet_path, "r") as file:
            stylesheet = file.read()
        self.setStyleSheet(stylesheet)

def start_interface():
    ui = Interface()
    ui.show()

