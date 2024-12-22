import pytest
# from maya_usd_export import interface
import maya_usd_export
import maya.cmds as cmd

import maya.standalone 
maya.standalone.initialize(name="python")



def test_foo():
    cmd.file(new=True, force=True)
    cube = cmd.polyCube(name="cube")[0]

    render_grp = cmd.group(empty=True, name="render")
    geo_grp = cmd.group(empty=True, name="geo")
    foo_grp = cmd.group(empty=True, name="foo_grp")

    cmd.parent(cube, render_grp)
    cmd.parent(render_grp, geo_grp)
    cmd.parent(geo_grp, foo_grp)

    assert True == True

    cmd.file(rename="/home/parker/Downloads/new_scene.ma")
    cmd.file(save=True, type="mayaAscii")

def pytest_sessionfinish(session, exitstatus):
    maya.standalone.uninitialize()
