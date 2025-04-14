import sys
import os
import pytest
import tempfile
import shutil

import pytest
import maya.cmds as cmds

import maya.standalone 


@pytest.fixture(scope="session", autouse=True)
def load_maya_usd(init_standalone):
    print("loading mayausdplugin")
    if not cmds.pluginInfo("mayaUsdPlugin", query=True, loaded=True):
        cmds.loadPlugin("mayaUsdPlugin")


@pytest.fixture(scope="session")
def plugin_path():
    plug_path = os.path.normpath(os.path.join(__file__, "../../../build/maya_usd_export.so"))
    plug_exists = os.path.exists(plug_path)

    assert plug_exists, f"Could not find maya_usd_export.so at {plug_path}"
    return plug_path

@pytest.fixture(scope="session")
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

@pytest.fixture(scope="session")
def load_plug(plugin_path, init_standalone):
    print("loading plugin")
    if not cmds.pluginInfo(plugin_path, query=True, loaded=True):
        try:
            cmds.loadPlugin(plugin_path)
        except Exception as e:
            maya.standalone.uninitialize()
            pytest.fail(f"Failed to load plugin: {e}\n")

    assert cmds.pluginInfo(plugin_path, query=True, loaded=True)


@pytest.fixture(scope="function")
def tmp_dir():
    tmp_dir = tempfile.mkdtemp(prefix="maya_usd_export_test")
    print("created tmp dir:", tmp_dir)

    yield tmp_dir

    print("destroying tmp dir:", tmp_dir)
    shutil.rmtree(tmp_dir, ignore_errors=True)


def test_foo(load_plug, new_scene, tmp_dir):
    print("test foo")
    cube1 = cmds.polyCube()
    cube2 = cmds.polyCube()
    torus1 = cmds.polyTorus()
    cmds.select(cube1[0], [torus1[0]])

    export_path = os.path.join(tmp_dir, "export_test.usda")
    cmds.helloWorld(export_path)

def test_parents(load_plug, new_scene, tmp_dir):
    print("test parents")
    cube1 = cmds.polyCube()
    cube2 = cmds.polyCube()
    torus1 = cmds.polyTorus()

    xform = cmds.createNode('transform', name='parentXform')
    print("xform:", xform)

    cmds.parent(cube1, xform)

    cmds.select(cube1[0], torus1[0])

    export_path = os.path.join(tmp_dir, "export_test.usda")
    cmds.helloWorld(export_path)


