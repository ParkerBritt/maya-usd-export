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

@pytest.fixture(scope="function")
def write_maya_file(request):
    yield
    tmp_dir = tempfile.mkdtemp(prefix=f"maya_file_{request.node.name}_")

    output_path = os.path.join(tmp_dir, "scene.ma")
    print(f"writing maya scene to {output_path}")
    cmds.file(rename=output_path)
    cmds.file(save=True, type="mayaAscii")

@pytest.fixture(scope="module", autouse=True)
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
def tmp_dir_parent(request):
    tmp_dir = tempfile.mkdtemp(prefix="maya_usd_export_tests_")
    print("created tmp dir:", tmp_dir)

    yield tmp_dir

    keep_tmp_dirs = request.config.getoption("--keep-tmp-dirs")
    if(not keep_tmp_dirs):
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


# def test_foo(load_plug, new_scene, tmp_dir):
#     print("test foo")
#     cube1 = cmds.polyCube()
#     cube2 = cmds.polyCube()
#     torus1 = cmds.polyTorus()
#     cmds.select(cube1[0], [torus1[0]])

#     export_path = os.path.join(tmp_dir, "export_test.usda")
#     cmds.USDExport(export_path)

def test_parenting(new_scene, tmp_dir):
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
    cmds.USDExport(f=export_path)

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

# def test_xform_animation(new_scene, tmp_dir):
#     from pxr import Usd, UsdGeom

#     cube1 = cmds.polyCube()

#     xform_parent = cmds.createNode('transform', name='parentXform')

#     cmds.parent(cube1, xform_parent)
#     print("cube:", cube1)

#     # animate translation Y from 0 at frame 0 to 0.5 at frame 5
#     cmds.setKeyframe("pCubeShape1", attribute="translateY", value=0, time=0)
#     cmds.setKeyframe("pCubeShape1", attribute="translateY", value=0.5, time=5)

#     # select for export
#     cmds.select(cube1[0])

#     export_path = os.path.join(tmp_dir, "export_test.usda")
#     cmds.USDExport(export_path)

#     stage = Usd.Stage.Open(export_path)
#     prim = stage.GetPrimAtPath("/parentXform/pCube1/pCube1")
#     assert prim.IsValid(), "Invalid prim"
#     points = UsdGeom.Points(prim)
#     positions_attr = points.GetPointsAttr()

#     time_code = 0
#     positions = positions_attr.Get(time_code)
#     assert positions == [(-0.5, -0.5, 0.5), (0.5, -0.5, 0.5), (-0.5, 0.5, 0.5), (0.5, 0.5, 0.5), (-0.5, 0.5, -0.5), (0.5, 0.5, -0.5), (-0.5, -0.5, -0.5), (0.5, -0.5, -0.5)], f"points not in expected position: {positions}"

#     time_code = 5
#     positions = positions_attr.Get(time_code)
#     assert positions == [(-0.5, 0, 0.5), (0.5, 0, 0.5), (-0.5, 1, 0.5), (0.5, 1, 0.5), (-0.5, 1, -0.5), (0.5, 1, -0.5), (-0.5, 0, -0.5), (0.5, 0, -0.5)], f"points not in expected position: {positions}"



def test_rig_animation(new_scene, tmp_dir):
    from pxr import Usd, UsdGeom

    # ----
    # setup scene
    # ----
    cube = cmds.polyCube(w=10,h=10,d=10,n="skinned_geo")
    cmds.select(clear=True)
    joint = cmds.joint(n="root")
    
    cmds.skinCluster(joint, "skinned_geo", toSelectedBones=True)
    
    cmds.group([joint, "skinned_geo"],n="rig",w=1)
    
    cmds.currentTime(1)
    cmds.setKeyframe(joint)
    
    cmds.currentTime(5)
    cmds.move(10, 0, 0, joint, relative=True)
    cmds.setKeyframe(joint)

    cmds.select(cube[0])

    export_path = os.path.join(tmp_dir, "export_test.usda")
    cmds.USDExport(f=export_path, fr=(1,5))

    # ----
    # test check usd
    # ----
    stage = Usd.Stage.Open(export_path)
    prim = stage.GetPrimAtPath("/rig/skinned_geo/skinned_geo")
    assert prim.IsValid(), "Invalid prim"
    assert prim.GetTypeName() == "Mesh"
    points = UsdGeom.Points(prim)
    positions_attr = points.GetPointsAttr()

    time_code = 0
    positions = positions_attr.Get(time_code)
    expected_positions  = [
        (-5, -5, 5),
        (5, -5, 5),
        (-5, 5, 5),
        (5, 5, 5),
        (-5, 5, -5),
        (5, 5, -5),
        (-5, -5, -5),
        (5, -5, -5),
    ]
    assert positions == expected_positions, f"points not in expected start position: {positions}"

    time_code = 5
    positions = positions_attr.Get(time_code)
    expected_positions  = [
        (5, -5, 5),
        (15, -5, 5),
        (5, 5, 5),
        (15, 5, 5),
        (5, 5, -5),
        (15, 5, -5),
        (5, -5, -5),
        (15, -5, -5),
    ]
    assert positions == expected_positions, f"points not in expected end position: {positions}"


def test_uvs(new_scene, tmp_dir):
    from pxr import Usd, UsdGeom
    import os
    import maya.cmds as cmds

    cube = cmds.polyCube(n="cube_geo")
    cmds.select(cube[0])

    # export the mesh to USD
    export_path = os.path.join(tmp_dir, "export_uv_test.usda")
    cmds.USDExport(f=export_path)

    # open the stage and locate the mesh prim
    stage = Usd.Stage.Open(export_path)
    prim = stage.GetPrimAtPath("/cube_geo/cube_geo")
    assert prim.IsValid(), "Invalid prim at /cube_geo/cube_geo"
    assert prim.GetTypeName() == "Mesh"

    # get the UV primvar
    api = UsdGeom.PrimvarsAPI(prim)
    st_primvar = api.GetPrimvar("st")
    assert st_primvar.GetInterpolation() == UsdGeom.Tokens.faceVarying

    # retrieve and compare UVs
    uvs = st_primvar.Get()
    expected_uvs = [
        (0.33, 0),
        (0.66333336, 0),
        (0.66333336, 0.25),
        (0.33, 0.25),
        (0.33, 0.25),
        (0.66333336, 0.25),
        (0.66333336, 0.5),
        (0.33, 0.5),
        (0.33, 0.5),
        (0.66333336, 0.5),
        (0.66333336, 0.75),
        (0.33, 0.75),
        (0.33, 0.75),
        (0.66333336, 0.75),
        (0.66333336, 1),
        (0.33, 1),
        (0.66333336, 0),
        (1, 0),
        (1, 0.25),
        (0.66333336, 0.25),
        (0, 0),
        (0.33, 0),
        (0.33, 0.25),
        (0, 0.25),
    ]
    assert uvs == expected_uvs, f"UVs not as expected:\nGot: {uvs}\n  Expected: {expected_uvs}"
