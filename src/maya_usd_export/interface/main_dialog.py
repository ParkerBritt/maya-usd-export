import platform, os, sys
from pathlib import Path

import maya.cmds as cmds
from maya_usd_export.interface.widgets.collapsible_container import CollapsibleContainer

from maya_usd_export.utils import pyside_importer
_, _, qtw, shiboken = pyside_importer.import_all()

from maya_usd_export.interface.options.general_options import GeneralOptions
from maya_usd_export.interface.options.selection_options import SelectionOptions


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


class Interface(qtw.QScrollArea):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setParent(parent)
        self.setWindowFlags(Qt.Window)


        self.setWindowTitle("Maya USD Export")

        self.initUI()

        # set sizing hinting
        self.resize(self.main_widget.minimumSizeHint().width()*1.5, self.main_widget.minimumSizeHint().width()*2)

        # self.setMaximumHeight(self.minimumSizeHint().height()+80)
        # self.setMaximumWidth(800)

    def initUI(self):
        # create layouts
        self.main_layout = qtw.QVBoxLayout()
        self.main_layout.setAlignment(Qt.AlignTop)

        self.main_widget = qtw.QWidget()
        self.main_widget.setLayout(self.main_layout)

        self.scroll = self
        self.scroll.setWidget(self.main_widget)
        self.scroll.setWidgetResizable(True)
        self.scroll.setFrameShape(qtw.QFrame.NoFrame)

        # add form items
        general_options_container = CollapsibleContainer("General Options")
        general_options_container.addWidget(GeneralOptions())
        self.main_layout.addWidget(general_options_container)

        selection_options_container = CollapsibleContainer("Selection Options")
        selection_options_container.addWidget(SelectionOptions())
        self.main_layout.addWidget(selection_options_container)

        # footer buttons
        footer_buttons_layout = qtw.QHBoxLayout()
        self.main_layout.addStretch()
        self.main_layout.addLayout(footer_buttons_layout)

        self.export_button = qtw.QPushButton("export")
        self.cancel_button = qtw.QPushButton("cancel")

        footer_buttons_layout.addStretch()
        footer_buttons_layout.addWidget(self.export_button)
        footer_buttons_layout.addWidget(self.cancel_button)





