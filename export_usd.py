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


class ExportAnim():
    def __init__(
        self,
        geo_whitelist,
        usd_type="",
        output="/home/will/Downloads/", # directory file is saved too
        root_type="",
        start_frame=None,
        end_frame=None,
        debug=False,
        export_rig=False,
        include_blendshapes=True,
        changelist_description=None,
    ):  
        self.render_geo_whitelist = geo_whitelist
        self.output = output
        self.root_type = root_type
        self.debug = debug
        self.start_frame = start_frame
        self.end_frame = end_frame
        self.usd_type = usd_type
        self.export_rig = export_rig
        self.frame_step = 1
        self.include_blendshapes = include_blendshapes
        self.changelist_description = changelist_description if changelist_description else "Animation Export"
        self.MESSAGE = "Export Finished"

        self.load_plugins()

        if not self.start_frame:
            self.start_frame = cmds.playbackOptions(q=True, minTime=True)
        if not self.end_frame:
            self.end_frame = cmds.playbackOptions(q=True, maxTime=True)
        print("\nSTART FRAME", self.start_frame)
        print('END FRAME', self.end_frame, "\n")

        self.ui = Interface()
        self.ui.show()

        pushButton = self.ui.findChild(QPushButton, "export_usd")
        QObject.connect(pushButton, SIGNAL("clicked()"), lambda: self.export_anim(self.output))

        self.file_path_lineedit = self.ui.findChild(QLineEdit, "file_path_lineedit")
        file_path_button = self.ui.findChild(QPushButton, "file_path_button")
        QObject.connect(file_path_button, SIGNAL("clicked()"), lambda: self.open_file_dialog())

        if os.path.exists(self.output):
            self.file_path_lineedit.setText(self.output)
        else:
            if platform.system() == "Windows":
                if os.environ["TWELVEFOLD_ROOT"]:
                    export_path = os.path.join(os.environ,"__ANIM__","export")
                    if not os.path.exists(export_path):
                        export_path = os.mkdir(export_path)
                elif os.environ["MAYA_APP_DIR"]:
                    export_path = os.environ["MAYA_APP_DIR"]
                else:
                    export_path = Path.home() / "Documents"
            elif platform.system() == "Linux":
                if os.environ["MAYA_APP_DIR"]:
                    export_path = os.environ["MAYA_APP_DIR"]
                else:
                    export_path = Path.home() / "Documents"

            self.file_path_lineedit.setText(str(export_path))
            self.output = str(export_path)

    def open_file_dialog(self):
        file_path = QFileDialog.getExistingDirectory(self.ui, "Select Directory", dir=self.output)
        if file_path:
            self.file_path_lineedit.setText(file_path) 
            self.output = file_path

    def get_joint_grps(self, character):
        def traverse(parent_path):
            attr_name = "joints_grp"
            found_items = []
            try:
                children = cmds.listRelatives(parent_path, children=True, fullPath=True)
            except ValueError:
                print("Warning: grp_joints does not exist under character")
                return found_items

            if not children:
                return found_items
        
            for child in children:
                attr_path = child+"."+attr_name
                # appends joint grp if they have attr_path on the joints grp (allows you only to export skin joints)
                try:
                    if cmds.objExists(child) == True and cmds.getAttr(attr_path, asString=True) == "True":
                        print(f"FOUND ITEM {child}")
                        found_items.append(child)
                except ValueError: 
                    pass
                child_found_items = traverse(child)
                found_items.extend(child_found_items)

            return found_items

        if self.namespace:
            joints_path = f"{character}|{self.namespace}:grp_joints"  # parent group to joints grp
        else:
            joints_path = f"{character}|grp_joints"
        character_paths = traverse(joints_path)
        print(f"joint: {character_paths}")
        return character_paths

    def get_characters(self):
        namespaces = cmds.namespaceInfo(lon=True, r=True)
        if "UI" and "shared" in namespaces:
            namespaces.remove("UI")
            namespaces.remove("shared")

        if namespaces:
            self.namespace = namespaces[0]
            groups = cmds.ls(f"{self.namespace}:geo*", long=True)
        else:
            self.namespace = None
            groups = cmds.ls("*geo*", long=True)
        print("found groups", groups, "\n")

        matching_groups = []
        characters = []

        for grp in groups:
            parent = cmds.listRelatives(grp, parent=True, fullPath=True)
            print(parent)
            if parent:
                parent_name = parent[0]
                print(parent_name)

                if parent_name.endswith("_rig"):
                    characters.append(parent_name[1:-4])
                    matching_groups.append(grp)

        if not characters and not matching_groups:
            print("ERROR: No parent group to geo found, make sure parent group of geo has _rig suffix \n")
            self.MESSAGE = f"No parent group to geo found, make sure parent group of geo has _rig suffix \n{self.MESSAGE}"
        else:
            print("matching groups", matching_groups)
            print("characters:", characters, "\n")

        return (characters, matching_groups)

    def load_plugins(self):
        if not cmds.pluginInfo("mayaUsdPlugin", query=True, loaded=True):
            cmds.loadPlugin("mayaUsdPlugin")

    def export_anim(self, export_file_path):
        characters, matching_groups = self.get_characters()
        self.output = self.file_path_lineedit.text()
        project_root = os.path.normpath(self.output)

        for i, character in enumerate(characters):
            group_name = matching_groups[i]
            print(f"grpname: {group_name}")
            root_prim = cmds.listRelatives(group_name, parent=True)[0]
            children = cmds.listRelatives(group_name, children=True)

            if self.namespace:
                for geo in self.render_geo_whitelist:
                    new_geo = f"{self.namespace}:{geo}"
                    index = self.render_geo_whitelist.index(geo)
                    self.render_geo_whitelist[index] = new_geo
            print(f"geo_whitelist: {self.render_geo_whitelist}")

            filtered_children = [
                child for child in children if child in self.render_geo_whitelist
            ]
            if len(filtered_children) == 0:
                print(f"no groups match the whitelist: {self.render_geo_whitelist} \n")
                self.MESSAGE = f"no groups match the whitelist: {self.render_geo_whitelist} \n{self.MESSAGE}"
                return

            print("filtered_children from whitelist", filtered_children)
            print("children groups:", children, "\n")

            # string handling for export
            shot_num = self.ui.findChild(QLineEdit, "shot_number")
            shot_num = shot_num.text()
            shot_num = f"SH{shot_num.zfill(4)}"
            export_ver = self.ui.findChild(QLineEdit, "asset_version")
            export_ver = export_ver.text()
            export_ver = f"v{export_ver.zfill(4)}"
            character_name = character.split('|')[0]
            if self.namespace:
                character_name = character_name.replace(f"{self.namespace}:","")
            file_name = f"{character_name}_{export_ver}"

            export_file_path = f"{project_root}/{shot_num}/{character_name}/{file_name}"
            export_file_path = os.path.normpath(export_file_path)
            print("EXPORT FILE PATH", export_file_path)

            export_file_already_exists = os.path.exists(f"{project_root}/{shot_num}/{character}/")
            if export_file_already_exists:
                print("FILE ALREADY EXISTS, going to OVERWITE")

            export_dirname = os.path.dirname(export_file_path)

            if not os.path.exists(export_dirname):
                print(f"{export_dirname} does not exist. Making path")
                os.makedirs(export_dirname)

            print("\n")

            # make selection
            made_selection = False
            cmds.select(clear=True)
            if self.export_rig:
                for joint_grp in self.get_joint_grps(character+"_rig"):
                    cmds.select(joint_grp, add=True)
            self.set_usd_type(group_name, self.usd_type)

            self.set_usd_type(root_prim, self.root_type)
            for child in cmds.listRelatives(group_name, children=True):
                if not child in self.render_geo_whitelist:
                    continue

                child = f"{group_name}|{child}"
                cmds.select(child, add=True)
                self.set_usd_type(child, self.usd_type)
                made_selection = True
            if not made_selection:
                print(f"ERROR: Could not file element of {self.render_geo_whitelist} in {group_name} \n")
                self.MESSAGE = f"ERROR: Could not file element of {self.render_geo_whitelist} in {group_name} \n{self.MESSAGE}"
                continue

            # export file
            export_args = {
                    "file":export_file_path,
                    "selection":True,
                    "defaultMeshScheme":"none",
                    "exportVisibility":False,
                    "exportUVs":False,
                    "exportMaterialCollections":False,
                    "shadingMode":"none",
                    "frameRange":(self.start_frame, self.end_frame),
                    "frameStride":self.frame_step,
                    "staticSingleSample":True,
                    "stripNamespaces":True,
            }

            if self.include_blendshapes:
                export_args.update({"exportBlendShapes":True})
            else:
                export_args.update({"exportBlendShapes":False})

            if self.export_rig:
                export_args.update({
                    "exportSkels":"auto",
                    "exportSkin":"auto",
                })

            print("EXPORTING USD...")
            print("USD export args:\n",export_args)

            cmds.mayaUSDExport(**export_args)

            # End the Maya session
            print("finished exporting file:", export_file_path)
        print("exported all characters(meshes)")
        self.ui.close()
        cmds.confirmDialog(message=self.MESSAGE, title="Export Finished")

    def set_usd_type(self, item, usd_type):
        attr_path = f"{item}.USD_typeName"
        if(cmds.objExists(attr_path)):
            cmds.setAttr(attr_path, usd_type, type="string")
        else: 
            print(f"cant find {attr_path} not setting attr value: {usd_type}")
