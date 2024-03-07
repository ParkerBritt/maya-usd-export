import importlib
import os
import sys

import maya.cmds as cmds
import maya.mel as mel
import argparse
from playsound import playsound

# import p4 utils
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

class ExportAnim():
    def __init__(self, output=None, start_frame=None, end_frame=None, do_p4=True, debug=False):
        self.render_geo_whitelist = ["render"]
        self.output = output
        self.debug = debug
        self.do_p4 = do_p4
        self.start_frame = start_frame
        self.end_frame = end_frame
        self.frame_step = 1

        if debug:
            self.do_p4=False
            self.start_frame, self.end_frame = (1001, 1001)

        load_plugins()

        # set start frame to maya scene time range
        if not self.start_frame:
            self.start_frame = cmds.playbackOptions(q=True, animationStartTime=True)
        if not self.end_frame:
            self.end_frame = cmds.playbackOptions(q=True, animationEndTime=True)

        if self.do_p4:
            change_num = p4utils.make_change("animation tool test") 
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

        characters, matching_groups = get_characters()

        for i, character in enumerate(characters):
            group_name = matching_groups[i]
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
            if(not export_file_path):
                shot_num = os.getenv("SHOT_NUM")
                if not project_root or not shot_num:
                    raise Exception("environment variables 'file_root' or 'SHOT_NUM' not set")
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
                    p4utils.edit(export_file_path, change_num=change_num)

            export_dirname = os.path.dirname(export_file_path)

            if not os.path.exists(export_dirname):
                print(f"{export_dirname} does not exist. Making path")
                os.makedirs(export_dirname)

            made_selection = False
            cmds.select(clear=True)
            for child in cmds.listRelatives(group_name, children=True):
                if not child in self.render_geo_whitelist:
                    continue
                cmds.select(f"{group_name}|{child}",add=True)
                made_selection=True
            if not made_selection:
                print(f"ERROR: Could not file element of {self.render_geo_whitelist} in {group_name}")
                continue

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
            )

            if (
                self.do_p4
                and (not export_file_already_exists
                or export_file_p4_info["status"] == "unopened")
            ):
                p4utils.add(export_file_path, change_num=change_num)

            # End the Maya session
            print("finished exporting file:", export_file_path)
        print("exported all characters")
        print("submitting to perforce...")
        if self.do_p4:
            p4utils.submit(change_num)
        print("finished submitting to perforce")

        finished_audio_path = os.path.join(
            project_root, "pipeline/elements/sounds/export_complete.mp3"
        )
        finished_audio_path = os.path.normpath(finished_audio_path)
        if os.path.exists(finished_audio_path):
            playsound(finished_audio_path)
        cmds.confirmDialog(message="Export Finished", title="Export Finished")

        def set_usd_type(self):
            cmds.setAttr('sphere.translateX', lock=True)
