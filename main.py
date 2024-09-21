import importlib
import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
print(f"Adding to MAYA_SCRIPT_PATH ENV {os.path.dirname(os.path.abspath(__file__))}")

import export_anim
importlib.reload(export_anim)

import export_cfx
importlib.reload(export_cfx)

def run_export_anim():
    export_anim.export()

def run_export_cfx():
    export_cfx.export()

