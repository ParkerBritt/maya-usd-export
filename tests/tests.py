import pytest
# from maya_usd_export import interface
import maya_usd_export
from maya_usd_export import selection
import maya.cmds as cmd

import maya.standalone 
maya.standalone.initialize(name="python")



def test_selection():
    # create new file
    cmd.file(new=True, force=True)
    cube = cmd.polyCube(name="cube")[0]

    # create rig groups
    render_grp = cmd.group(empty=True, name="render")
    geo_grp = cmd.group(empty=True, name="geo")
    foo_grp = cmd.group(empty=True, name="foo_rig")

    # parent rig heirarcy
    cmd.parent(cube, render_grp)
    cmd.parent(render_grp, geo_grp)
    cmd.parent(geo_grp, foo_grp)

    selection_instance = selection.Selection(render_geo_whitelist=['render'], export_rig=False)
    assert selection_instance
    assert selection_instance.return_data() == {'|foo_rig': {'root_prim': 'foo_rig', 'filtered_children': ['render'], 'joint_grp_path': None, 'group_name': '|foo_rig|geo', 'namespace': None}}

    # cmd.file(rename="/home/parker/Downloads/new_scene.ma")
    # cmd.file(save=True, type="mayaAscii")

def pytest_sessionfinish(session, exitstatus):
    maya.standalone.uninitialize()
