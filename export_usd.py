import importlib
import os
import sys

import maya.cmds as cmds
from playsound import playsound

project_root = os.getenv("film_root")
if not project_root:
    raise Exception("environment variable: film_root not found")
python_utils_path = os.path.join(project_root, "pipeline/packages/2AM/python_utils")
p4_utils_path = os.path.join(python_utils_path, "p4utils.py")
if not os.path.exists(p4_utils_path):
    raise Exception(f"can't find p4utils.py file in: {p4_utils_path}")
sys.path.append(python_utils_path)

import p4utils
importlib.reload(p4utils)


# self.render_geo_whitelist = ["Render", "Muscles", "Fat"]


class ExportAnim:
    def __init__(
        self,
        geo_whitelist=["render"],
        usd_type="",
        output=None,
        root_type="",
        start_frame=None,
        end_frame=None,
        do_p4=True,
        debug=False,
        export_rig=False,
    ):
        self.render_geo_whitelist = geo_whitelist
        self.output = output
        self.root_type=root_type
        self.debug = debug
        self.do_p4 = do_p4
        self.start_frame = start_frame
        self.end_frame = end_frame
        self.usd_type = usd_type
        self.joint_grp_path = "rig|Trans_Grp|Control_Grp|Global_Ctrl_Offset|Global_Ctrl|Joint_Grp"
        self.export_rig = export_rig
        self.frame_step = 1

        if debug:
            self.do_p4 = False

        self.load_plugins()

        print("START FRAME", self.start_frame)
        print('END FRAME', self.end_frame)
        # set start frame to maya scene time range
        if not self.start_frame:
            self.start_frame = cmds.playbackOptions(q=True, animationStartTime=True)
        if not self.end_frame:
            self.end_frame = cmds.playbackOptions(q=True, animationEndTime=True)

        if self.do_p4:
            self.change_num = p4utils.make_change("animation tool test")
        self.export_anim(self.output)

    def get_characters(self):
        groups = cmds.ls("geo", long=True)
        print("found groups", groups)

        matching_groups = []
        characters = []

        for grp in groups:
            print("grp:", grp)
            parent = cmds.listRelatives(grp, parent=True, fullPath=True)

            if parent:
                parent_name = parent[0]

                if parent_name.endswith("_anim"):
                    characters.append(parent_name[1:-5])
                    matching_groups.append(grp)
        print("matching groups", matching_groups)
        print("characters:", characters)

        return (characters, matching_groups)

    def load_plugins(self):
        if not cmds.pluginInfo("mayaUsdPlugin", query=True, loaded=True):
            cmds.loadPlugin("mayaUsdPlugin")

    def export_anim(self, export_file_path):
        # start_frame = frame_range[0]
        # end_frame = frame_range[1]
        # frame_step = frame_range[2]

        #    if not cmds.pluginInfo("AbcExport", query=True, loaded=True):
        #        cmds.loadPlugin("AbcExport")

        characters, matching_groups = self.get_characters()

        for i, character in enumerate(characters):
            group_name = matching_groups[i]
            root_prim = cmds.listRelatives(group_name, parent=True)[0]
            children = cmds.listRelatives(group_name, children=True)

            filtered_children = [
                child for child in children if child in self.render_geo_whitelist
            ]
            if len(filtered_children) == 0:
                print(f"no groups match the whitelist: {self.render_geo_whitelist}")
                return

            print("filtered_children", filtered_children)
            print("children:", children)
            print(character, group_name)

            project_root = os.getenv("film_root")
            if not export_file_path:
                print("export file path:", export_file_path)
                shot_num = os.getenv("SHOT_NUM")
                if not project_root or not shot_num:
                    raise Exception(
                        "environment variables 'file_root' or 'SHOT_NUM' not set"
                    )
                export_file_path = f"{project_root}/usd/shots/SH{shot_num.zfill(4)}/scene_layers/anims/{character}.usd"
            print("EXPORT FILE PATH", export_file_path)
            export_file_already_exists = os.path.exists(export_file_path)
            export_file_p4_info = None
            if export_file_already_exists:
                print("FILE ALREADY EXISTS")
                file_info = p4utils.get_file_info(export_file_path)[0]
                print("FILE INFO", file_info)
                export_file_p4_info = file_info
                if file_info["status"] != "unopened":
                    p4utils.edit(export_file_path, change_num=self.change_num)

            export_dirname = os.path.dirname(export_file_path)

            if not os.path.exists(export_dirname):
                print(f"{export_dirname} does not exist. Making path")
                os.makedirs(export_dirname)

            # make selection
            made_selection = False
            cmds.select(clear=True)
            if self.export_rig:
                cmds.select(root_prim+"|"+self.joint_grp_path, add=True)
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
                print(
                    f"ERROR: Could not file element of {self.render_geo_whitelist} in {group_name}"
                )
                continue

            # export file
            frame_range = (self.start_frame, self.end_frame)
            cmds.mayaUSDExport(
                file=export_file_path,
                selection=True,
                defaultMeshScheme="none",
                exportVisibility=False,
                exportUVs=False,
                exportMaterialCollections=False,
                shadingMode="none",
                frameRange=frame_range,
                frameStride=self.frame_step,
                exportSkels="auto",
                exportSkin="auto",
            )

            # add file to changelist
            if self.do_p4 and (
                not export_file_already_exists
                or export_file_p4_info["status"] == "unopened"
            ):
                p4utils.add(export_file_path, change_num=self.change_num)

            # End the Maya session
            print("finished exporting file:", export_file_path)
        print("exported all characters")
        if self.do_p4:
            print("submitting to perforce...")
            p4utils.submit(self.change_num)
            print("finished submitting to perforce")

        finished_audio_path = os.path.join(
            project_root, "pipeline/elements/sounds/export_complete.mp3"
        )
        finished_audio_path = os.path.normpath(finished_audio_path)
        if os.path.exists(finished_audio_path):
            playsound(finished_audio_path)
        cmds.confirmDialog(message="Export Finished", title="Export Finished")

    def set_usd_type(self, item, usd_type):
        attr_path=f"{item}.USD_typeName"
        if(cmds.objExists(attr_path)):
            cmds.setAttr(attr_path, usd_type, type="string")
