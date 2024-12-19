import os
import maya.cmds as cmds


class ExportAlembic():
    def __init__(
        self,
        output=None,
        start_frame=None,
        end_frame=None,
        step_frame=1,
        character_dict=None
        ):
        self.output = output
        self.start_frame = start_frame
        self.end_frame = end_frame
        self.step_frame = step_frame
        self.character_dict = character_dict

        self.export_alembic()

    def export_alembic(self):
        for character in self.character_dict.values():
            root_prim = character["root_prim"]
            filtered_children = character["filtered_children"]

            cmds.select(clear=True)

            if character["namespace"]:
                root_prim = root_prim.replace(f"{character['namespace']}:","")
            file_name = f"{root_prim}.abc"

            root = " ".join(f"-root {item}" for item in filtered_children)

            self.output = os.path.normpath(self.output)
            if not os.path.exists(self.output):
                print(f"\npath does not exist making directory:\n{self.output}")
                os.makedirs(self.output)
            self.output = f"{self.output}/{file_name}"
            print(self.output)

            print("\n")

            export_args = (
                f"-frameRange {self.start_frame} {self.end_frame} "
                f"-uvWrite -stripNamespaces " # -worldSpace "
                f"-file {self.output} "
                f"-step {self.step_frame} "
                f"{root} "
            )
            print(f"Exporting alembic with args: {export_args}")
            cmds.AbcExport (j=export_args)
        cmds.confirmDialog(message="Export Finished", title="Export Finished")
