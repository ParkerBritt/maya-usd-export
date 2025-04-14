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

    assert cmds.pluginInfo(plugin_path, query=True, loaded=True), "maya_usd_export failed to load"


@pytest.fixture(scope="session")
def tmp_dir_parent():
    DESTROY_TMP_DIRS = True
    tmp_dir = tempfile.mkdtemp(prefix="maya_usd_export_tests_")
    print("created tmp dir:", tmp_dir)

    yield tmp_dir

    if(DESTROY_TMP_DIRS):
        print("destroying tmp dir:", tmp_dir)
        shutil.rmtree(tmp_dir, ignore_errors=True)

@pytest.fixture(scope="function")
def tmp_dir(tmp_dir_parent, request):
    tmp_dir = tempfile.mkdtemp(prefix=f"{request.node.name}_", dir=tmp_dir_parent)
    print("created tmp dir:", tmp_dir)

    return tmp_dir
    # yield tmp_dir

    # print("destroying tmp dir:", tmp_dir)
    # shutil.rmtree(tmp_dir, ignore_errors=True)


def test_foo(load_plug, new_scene, tmp_dir):
    print("test foo")
    cube1 = cmds.polyCube()
    cube2 = cmds.polyCube()
    torus1 = cmds.polyTorus()
    cmds.select(cube1[0], [torus1[0]])

    export_path = os.path.join(tmp_dir, "export_test.usda")
    cmds.USDExport(export_path)

def test_parenting(load_plug, new_scene, tmp_dir):
    from pxr import Usd, UsdGeom
    cube1 = cmds.polyCube()
    cube2 = cmds.polyCube()
    torus1 = cmds.polyTorus()

    xform_parent = cmds.createNode('transform', name='parentXform')
    xform_child = cmds.createNode('transform', name='childXform')

    cmds.parent(cube1, xform_parent)
    cmds.parent(xform_child, xform_parent)
    cmds.parent(cube2, xform_child)

    cmds.select(cube1[0], cube2[0],torus1[0])

    export_path = os.path.join(tmp_dir, "export_test.usda")
    cmds.USDExport(export_path)

    stage = Usd.Stage.Open(export_path)

    def prim_exists(parent_path):
        prim = stage.GetPrimAtPath(parent_path)
        assert prim.IsValid(), f"Expected prim {parent_path} not found in USD stage"

    # check expected parents exist
    prim_exists("/pTorus1")
    prim_exists("/parentXform/pCube1")
    prim_exists("/parentXform/childXform/pCube2")

    # inverse test
    prim = stage.GetPrimAtPath("/fakeparent")
    assert not prim.IsValid()


