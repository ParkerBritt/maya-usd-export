import platform, os, sys
from pathlib import Path

import maya.cmds as cmds
from maya import OpenMayaUI as omui
# from maya_usd_export.widgets.collapsible_container import CollapsibleContainer

from maya_usd_export.utils import pyside_importer
PySide, PySide.QtCore, PySide.QtWidgets, shiboken = pyside_importer.import_all()


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
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setParent(parent)
        self.setWindowFlags(Qt.Window)


        self.setWindowTitle("Maya USD Export")

        # default export path
        self.file_output_path = os.getcwd()
        self.initUI()

        # set sizing hinting
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


    def open_file_dialog(self):
        file_path = QFileDialog.getExistingDirectory(self, "Select Directory", dir=self.file_output_path)
        if file_path:
            self.file_path_lineedit.setText(file_path) 
            self.file_output_path = file_path


def start_interface():
    # parent to maya interface
    mayaMainWindowPtr = omui.MQtUtil.mainWindow()
    mayaMainWindow = shiboken.wrapInstance(int(mayaMainWindowPtr), QWidget)

    ui = Interface(mayaMainWindow)
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
