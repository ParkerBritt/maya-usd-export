import sys
import os

# check scripts
scripts_dir = os.path.join(os.getenv("HOME"), "maya", "scripts")
if not os.path.exists(scripts_dir):
    raise Exception (f"Scripts directory does not exist {scripts_dir}")
sys.path.append(scripts_dir)

# from maya_usd_export import interface
import pytest
import maya_usd_export
from maya_usd_export import selection
import maya.cmds as cmd

import maya.standalone 
maya.standalone.initialize(name="python")



def test_export():

def pytest_sessionfinish(session, exitstatus):
    maya.standalone.uninitialize()
