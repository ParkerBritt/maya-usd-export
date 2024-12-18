import os
import platform
from pathlib import Path

import maya.cmds as cmds
from maya import OpenMayaUI as omui

class ExportAnim():
    def __init__(
        self,
        usd_type="",
        output=None,
        root_type="",
        start_frame=None,
        end_frame=None,
        step_frame=1,
        export_rig=False,
        include_blendshapes=True,
        character_dict=None
    ):  
        self.output = output
        self.root_type = root_type
        self.start_frame = start_frame
        self.end_frame = end_frame
        self.usd_type = usd_type
        self.export_rig = export_rig
        self.frame_step = step_frame
        self.include_blendshapes = include_blendshapes
        self.character_dict = character_dict
        self.MESSAGE = "Export Finished"

        self.load_plugins()
        self.export_anim()

    def load_plugins(self):
        if not cmds.pluginInfo("mayaUsdPlugin", query=True, loaded=True):
            cmds.loadPlugin("mayaUsdPlugin")

    def export_anim(self):
        for character in self.character_dict.values():
            group_name = character["group_name"]
            root_prim = character["root_prim"]

            cmds.select(clear=True)
            if self.export_rig:
                for joint_grp in character["joint_grp_path"]:
                    cmds.select(joint_grp, add=True)

            self.set_usd_type(group_name, self.usd_type)
            self.set_usd_type(root_prim, self.root_type)

            for child in character["filtered_children"]:
                child = f"{group_name}|{child}"
                cmds.select(child, add=True)
                self.set_usd_type(child, self.usd_type)

            if character["namespace"]:
                root_prim = root_prim.replace(f"{character['namespace']}:", "")
            
            self.output = os.path.normpath(self.output)
            if not os.path.exists(self.output):
                print(f"\npath does not exists making directory:\n{self.output}")
                os.makedirs(self.output)
            export_file_path = f"{self.output}/{root_prim}"

            # export file
            export_args = {
                    "file":export_file_path,
                    "selection":True,
                    "defaultMeshScheme":"none",
                    "exportVisibility":False,
                    "exportUVs":True,
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

            print(f"\nEXPORTING USD...\nUSD export args: {export_args}\n")
            cmds.mayaUSDExport(**export_args)

        self.MESSAGE = f"{self.MESSAGE}\nExported to: {export_file_path}.usd"
        cmds.confirmDialog(message=self.MESSAGE, title="Export Finished")

    def set_usd_type(self, item, usd_type):
        attr_path = f"{item}.USD_typeName"
        if(cmds.objExists(attr_path)):
            cmds.setAttr(attr_path, usd_type, type="string")
        else: 
            print(f"cant find {attr_path} not setting attr value: {usd_type}")
