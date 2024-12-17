import os
import platform
from pathlib import Path

import maya.cmds as cmds
from maya import OpenMayaUI as omui

class ExportAnim():
    def __init__(
        self,
        geo_whitelist,
        usd_type="",
        output=None,
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

        print("\nSTART FRAME", self.start_frame)
        print('END FRAME', self.end_frame, "\n")

    def load_plugins(self):
        if not cmds.pluginInfo("mayaUsdPlugin", query=True, loaded=True):
            cmds.loadPlugin("mayaUsdPlugin")

    def export_anim(self, export_file_path):
        for character in character_dict:
            # make selection
            made_selection = False
            cmds.select(clear=True)
            if self.export_rig:
                for joint_grp in JOINTGRPHERE:
                    cmds.select(joint_grp, add=True)

            self.set_usd_type(group_name, self.usd_type)
            self.set_usd_type(root_prim, self.root_type)

            for child in cmds.listRelatives(group_name, children=True): # Ask parker what this was for
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
            
            # need to add a way to click true to export blendshapes
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
        cmds.confirmDialog(message=self.MESSAGE, title="Export Finished")

    def set_usd_type(self, item, usd_type):
        attr_path = f"{item}.USD_typeName"
        if(cmds.objExists(attr_path)):
            cmds.setAttr(attr_path, usd_type, type="string")
        else: 
            print(f"cant find {attr_path} not setting attr value: {usd_type}")
