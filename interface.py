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
    QComboBox,
    QSizePolicy,
    QCheckBox,
    QSpinBox,
    QAbstractSpinBox,
)


class Interface(QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # parent to maya interface
        mayaMainWindowPtr = omui.MQtUtil.mainWindow()
        mayaMainWindow = wrapInstance(int(mayaMainWindowPtr), QWidget)
        self.setParent(mayaMainWindow)
        self.setWindowFlags(Qt.Window)


        self.setWindowTitle("Maya_USD_Export")

        # default export path
        self.file_output_path = os.getcwd()
        self.initUI()

        # set sizing hinting
        print("MINIMUM HEIGHT:", self.minimumSizeHint().height())
        print("MINIMUM HEIGHT:", self.sizeHint().height())
        self.resize(self.minimumSizeHint().height()*2.5, self.minimumSizeHint().height())

        self.setMaximumHeight(self.minimumSizeHint().height()+80)
        self.setMaximumWidth(800)

    def initUI(self):
        # create layouts
        self.main_layout = QVBoxLayout(self)
        self.form_layout = QFormLayout()
        # place form layout in main layout
        self.main_layout.addStretch()
        self.main_layout.addLayout(self.form_layout)
        self.main_layout.addStretch()
        self.form_layout.setLabelAlignment(Qt.AlignLeft | Qt.AlignVCenter)

        self.file_path_layout = QHBoxLayout()
        self.file_path_lineedit = QLineEdit(self.file_output_path)
        self.file_path_lineedit.setObjectName("file_path_lineedit")
        self.file_path_button =  QPushButton("Change")
        self.file_path_button.setObjectName("file_path_button")
        self.file_path_button.clicked.connect(self.open_file_dialog)
        self.file_path_layout.addWidget(self.file_path_lineedit)
        self.file_path_layout.addWidget(self.file_path_button)

        self.export_asset_button = QPushButton("Export USD")
        self.export_asset_button.setObjectName("export_usd")

        self.file_type_widget = QComboBox()
        self.file_type_widget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.file_type_widget.currentTextChanged.connect(lambda text: self.export_asset_button.setText("Export "+text))
        self.file_type_widget.addItem("USD")
        self.file_type_widget.addItem("Alembic")

        self.animation_type_widget = QComboBox()
        self.animation_type_widget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.animation_type_widget.addItem("Static")
        self.animation_type_widget.addItem("Animation Cache")
        self.animation_type_widget.addItem("CFX")

        self.w_frame_lower = QSpinBox()
        self.w_frame_upper = QSpinBox()
        self.w_frame_lower.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.w_frame_upper.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.w_frame_lower.setButtonSymbols(QAbstractSpinBox.NoButtons)
        self.w_frame_upper.setButtonSymbols(QAbstractSpinBox.NoButtons)
        self.w_frame_lower.setToolTip("Lower frame range")
        self.w_frame_upper.setToolTip("Upper frame range")
        self.w_frame_lower

        self.w_frame_step = QSpinBox()
        self.w_frame_step.setButtonSymbols(QAbstractSpinBox.NoButtons)
        self.w_frame_step.setToolTip("Frame Step\nIndicates how many frames to skip for each saved geometry")

        self.anim_range_layout = QHBoxLayout()
        self.anim_range_layout.addWidget(self.w_frame_lower)
        self.anim_range_layout.addWidget(self.w_frame_upper)
        self.anim_range_layout.addWidget(self.w_frame_step)


        # add form items
        self.form_layout.addRow("File Path:", self.file_path_layout)
        self.form_layout.addRow("Frame Range:", self.anim_range_layout)
        self.form_layout.addRow("Animation Type:", self.animation_type_widget)
        self.form_layout.addRow("Export Type:", self.file_type_widget)
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

