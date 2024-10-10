import os
import maya.cmds as cmds
from maya import OpenMayaUI as omui
try:
    from PySide6.QtCore import *
    from PySide6.QtGui import *
    from PySide6.QtWidgets import QWidget
    from PySide6.QtWidgets import *
    from PySide6.QtUiTools import *
    from shiboken6 import wrapInstance
except ModuleNotFoundError:
    from PySide2.QtCore import *
    from PySide2.QtGui import *
    from PySide2.QtWidgets import QWidget
    from PySide2.QtWidgets import *
    from PySide2.QtUiTools import *
    from shiboken2 import wrapInstance

mayaMainWindowPtr = omui.MQtUtil.mainWindow()
mayaMainWindow = wrapInstance(int(mayaMainWindowPtr), QWidget)

class Interface(QWidget):
    def __init__(self, *args, **kwargs):
        super(Interface,self).__init__(*args, **kwargs)
        self.setParent(mayaMainWindow)
        self.setWindowFlags(Qt.Window)
        self.initUI()
        self.setFixedWidth(200)
        self.setFixedHeight(110)
        self.setWindowTitle("Maya_USD_Export")

    def initUI(self):
        self.main_layout_widget = QWidget(self)
        self.main_layout_widget.setMaximumWidth(200)
        self.main_layout = QFormLayout(self.main_layout_widget)
        self.main_layout.setLabelAlignment(Qt.AlignLeft | Qt.AlignVCenter)

        shot_num_label = QLabel("Shot Num:")
        shot_num_lineedit = QLineEdit("1")
        shot_num_lineedit.setObjectName("shot_number")

        asset_ver_label = QLabel("Asset Version:")
        asset_ver_lineedit = QLineEdit("1")
        asset_ver_lineedit.setObjectName("asset_version")

        export_asset_button = QPushButton("Export ABC")
        export_asset_button.setObjectName("export_abc")

        self.main_layout.addRow(shot_num_label, shot_num_lineedit)
        self.main_layout.addRow(asset_ver_label, asset_ver_lineedit)
        self.main_layout.addRow(export_asset_button)

        stylesheet_path = os.path.join(os.path.dirname(os.path.abspath(__file__)),"style.css")
        with open(stylesheet_path, "r") as file:
            stylesheet = file.read()
        self.setStyleSheet(stylesheet)

class ExportAlembic():
    def __init__(self):
        self.output = "D:/University_Projects/test_usd_export/"
        self.render_geo_whitelist = ["render"]

        self.start_frame = cmds.playbackOptions(q=True, minTime=True)
        self.start_frame = str(self.start_frame)
        self.end_frame = cmds.playbackOptions(q=True, maxTime=True)
        self.end_frame = str(self.end_frame)
        print("\nSTART FRAME", self.start_frame)
        print('END FRAME', self.end_frame, "\n")

        self.ui = Interface()
        self.ui.show()
        pushButton = self.ui.findChild(QPushButton, "export_abc")
        QObject.connect(pushButton, SIGNAL("clicked()"), lambda: self.export_alembic())

    def get_characters(self):
        groups = cmds.ls("*geo*", long=True)
        print("found groups", groups, "\n")

        matching_groups = []
        characters = []

        for grp in groups:
            parent = cmds.listRelatives(grp, parent=True, fullPath=True)

            if parent:
                parent_name = parent[0]

                if parent_name.endswith("_rig"):
                    characters.append(parent_name[1:-4])
                    matching_groups.append(grp)

        if not characters and not matching_groups:
            print("ERROR: No parent group to geo found, make sure parent group of geo has _rig suffix \n")
        else:
            print("matching groups", matching_groups)
            print("characters:", characters, "\n")

        return (characters, matching_groups)

    def export_alembic(self):
        characters, matching_groups = self.get_characters()
        project_root = self.output

        project_root = os.path.normpath(project_root)

        for i, character in enumerate(characters):
            group_name = matching_groups[i]
            root_prim = cmds.listRelatives(group_name, parent=True)[0]
            children = cmds.listRelatives(group_name, children=True)
            print(group_name)

            filtered_children = [
                child for child in children if child in self.render_geo_whitelist
            ]
            if len(filtered_children) == 0:
                print(f"no groups match the whitelist: {self.render_geo_whitelist} \n")
                return

            print("filtered_children from whitelist", filtered_children)
            print("children groups:", children, "\n")

            shot_num = self.ui.findChild(QLineEdit, "shot_number")
            shot_num = shot_num.text()
            shot_num = f"SH{shot_num.zfill(4)}"
            export_ver = self.ui.findChild(QLineEdit, "asset_version")
            export_ver = export_ver.text()
            export_ver = f"v{export_ver.zfill(4)}"
            character_name = character.split("|")[-1]
            file_name = f"{character_name}_{export_ver}.abc"

            root = f"-root {group_name}"
            export_file_path = f"{project_root}/{shot_num}/{character_name}/{file_name}"
            export_file_path = os.path.normpath(export_file_path)

            export_file_already_exists = os.path.exists(f"{project_root}/{shot_num}/{character}/")
            if export_file_already_exists:
                print("FILE ALREADY EXISTS, going to OVERWITE")

            export_dirname = os.path.dirname(export_file_path)

            if not os.path.exists(export_dirname):
                print(f"{export_dirname} does not exist. Making path")
                os.makedirs(export_dirname)

            print("\n")

            command = "-frameRange " + self.start_frame + " " + self.end_frame +" -uvWrite -worldSpace " + root + " -file " + export_file_path
            cmds.AbcExport ( j = command )
        print("exported all characters(meshes)")
        self.ui.close()
        cmds.confirmDialog(message="Export Finished", title="Export Finished")