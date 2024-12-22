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

from . import selection, export_usd, export_abc
for module in [selection, export_usd, export_abc]:
    importlib.reload(module)

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

        self.w_anim_type = AnimTypeDropdown()
        self.w_anim_range = AnimRangeWidget()

        # add form items
        self.form_layout.addRow("File Path:", self.file_path_layout)
        self.form_layout.addRow("Animation Type:", self.w_anim_type)
        self.form_layout.addRow("Frame Range:", self.w_anim_range)
        self.form_layout.addRow("Export Type:", self.file_type_widget)
        self.form_layout.addRow(self.export_asset_button)

        # hide anim range when anim type is set to static
        self.w_anim_type.currentTextChanged.connect(lambda text: (
            [self.form_layout.itemAt(i).widget().setVisible(text != AnimTypeDropdown.anim_types["static"]) for i in (4, 5)]
            ))
        # set default dropdown text
        self.w_anim_type.currentTextChanged.emit(AnimTypeDropdown.anim_types["static"])

        self.export_asset_button.clicked.connect(lambda: Export(output=self.file_path_lineedit.text(),
                                                                export_type=self.file_type_widget.currentText(),
                                                                anim_type=self.w_anim_type.currentText(),
                                                                start_frame=self.w_anim_range.return_frames()[0],
                                                                end_frame=self.w_anim_range.return_frames()[1],
                                                                step_frame=self.w_anim_range.return_frames()[2]
                                                                ))

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
    print("start interface ran")
    ui = Interface()
    ui.show()


class AnimRangeWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.w_frame_lower = QSpinBox()
        self.w_frame_upper = QSpinBox()
        self.w_frame_lower.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.w_frame_upper.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.w_frame_lower.setButtonSymbols(QAbstractSpinBox.NoButtons)
        self.w_frame_upper.setButtonSymbols(QAbstractSpinBox.NoButtons)
        self.w_frame_lower.setToolTip("Lower frame range")
        self.w_frame_upper.setToolTip("Upper frame range")
        self.w_frame_lower.setRange(-5000,5000)
        self.w_frame_upper.setRange(-5000,5000)
        self.w_frame_lower.setValue(1001)
        self.w_frame_upper.setValue(1101)

        self.w_frame_step = QSpinBox()
        self.w_frame_step.setButtonSymbols(QAbstractSpinBox.NoButtons)
        self.w_frame_step.setToolTip("Frame Step\nIndicates how many frames to skip for each saved geometry")
        self.w_frame_step.setValue(1)

        self.main_layout = QHBoxLayout()
        self.setLayout(self.main_layout)

        self.main_layout.addWidget(self.w_frame_lower)
        self.main_layout.addWidget(self.w_frame_upper)
        self.main_layout.addWidget(self.w_frame_step)
        self.main_layout.setContentsMargins(0, 0, 0, 0)

    def return_frames(self):
        return (self.w_frame_lower.value(), self.w_frame_upper.value(), self.w_frame_step.value())


class AnimTypeDropdown(QComboBox):
    anim_types = {
        "static":"Static",
        "cache":"Animation Cache",
        "cfx":"CFX"
    }
    def __init__(self):
        super().__init__()
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.addItem(self.anim_types["static"])
        self.addItem(self.anim_types["cache"])
        self.addItem(self.anim_types["cfx"])

class Export():
    def __init__(self, output=None, export_type=None, anim_type=None, start_frame=1001, end_frame=1101, step_frame=1):
        anim_configs = {
            "CFX": {
                "geo_whitelist": ['render', 'muscle', 'bone'],
                "usd_type": "Xform",
                "root_type": "SkelRoot",
                "export_rig": True,
                "include_blendshapes": True,
                "start_frame": start_frame,
                "end_frame": end_frame
            },
            "Animation Cache": {
                "geo_whitelist": ['render'],
                "usd_type": "",
                "root_type": "",
                "export_rig": False,
                "include_blendshapes": False,
                "start_frame": start_frame,
                "end_frame": end_frame
            },
            "Static": {
                "geo_whitelist": ['render'],
                "usd_type": "",
                "root_type": "",
                "export_rig": False,
                "include_blendshapes": True,
                "start_frame": 0,
                "end_frame": 1
            }
        }
        config = anim_configs.get(anim_type, None)
        if not config:
            raise KeyError("Config from anim_type is empty or not within anim_configs")

        selection_instance = selection.Selection(render_geo_whitelist=config.get("geo_whitelist", ['render']),
                                                 export_rig=config.get("export_rig", False))
        selection_data = selection_instance.return_data()
        if not selection_data:
            cmds.warning("selection_data is empty, no selection made aborting export")
            return
        
        if export_type == "USD":
            export_usd.ExportAnim(output=output,
                                  character_dict=selection_data,
                                  start_frame=config.get("start_frame", start_frame),
                                  end_frame=config.get("end_frame", end_frame),
                                  step_frame=step_frame,
                                  usd_type=config.get("usd_type", ""),
                                  root_type=config.get("root_type", ""),
                                  export_rig=config.get("export_rig", False),
                                  include_blendshapes=config.get("include_blendshapes", False)
                                )
        elif export_type == "Alembic":
            export_abc.ExportAlembic(output=output,
                                     character_dict=selection_data,
                                     start_frame=config.get("start_frame", start_frame),
                                     end_frame=config.get("end_frame", end_frame),
                                     step_frame=step_frame
                                )
        else:
            raise TypeError("wrong type for export_type varible passed")
