import sys
import os
import pytest

import pytest
import maya.cmds as cmds

import maya.standalone 



@pytest.fixture(scope="module")
def plugin_path():
    plug_path = os.path.normpath(os.path.join(__file__, "../../../build/maya_usd_export.so"))
    plug_exists = os.path.exists(plug_path)

    assert plug_exists, f"Could not find maya_usd_export.so at {plug_path}"
    return plug_path

@pytest.fixture(scope="module")
def init_standalone():
    print("starting standalone")
    maya.standalone.initialize(name="python")
    yield
    print("ending standalone")
    maya.standalone.uninitialize()

@pytest.fixture(scope="function")
def new_scene():
    print("creating new scene")
    cmds.file(new=True, force=True)

@pytest.fixture(scope="module")
def load_plug(plugin_path, init_standalone):
    print("loading plugin")
    if not cmds.pluginInfo(plugin_path, query=True, loaded=True):
        try:
            cmds.loadPlugin(plugin_path)
        except Exception as e:
            maya.standalone.uninitialize()
            pytest.fail(f"Failed to load plugin: {e}\n")

    assert cmds.pluginInfo(plugin_path, query=True, loaded=True)



def test_foo(load_plug, new_scene):
    print("test foo")
    cube1 = cmds.polyCube()
    cube2 = cmds.polyCube()
    torus1 = cmds.polyTorus()
    cmds.select(cube1[0], [torus1[0]])

    cmds.helloWorld(f"{os.getenv('HOME')}/Downloads/cpp_export_test.usda")




