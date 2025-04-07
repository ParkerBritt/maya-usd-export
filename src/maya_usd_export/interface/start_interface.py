from .main_dialog import Interface
from maya_usd_export.controllers.main_dialog_controller import MainDialogController

from maya_usd_export.utils import pyside_importer
from maya import OpenMayaUI as omui
_, _, qtw, shiboken = pyside_importer.import_all()

def start_interface():
    # parent to maya interface
    mayaMainWindowPtr = omui.MQtUtil.mainWindow()
    mayaMainWindow = shiboken.wrapInstance(int(mayaMainWindowPtr), qtw.QWidget)

    ui = Interface(mayaMainWindow)
    main_dialog_controller = MainDialogController(ui)
    ui.show()
