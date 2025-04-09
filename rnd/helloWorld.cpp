#include <maya/MSimple.h>
#include <maya/MIOStream.h>
#include <maya/MGlobal.h>
#include <maya/MSelectionList.h>
#include <maya/MDagPath.h>
#include <maya/MFnMesh.h>
#include <maya/MFloatPointArray.h>

#include <pxr/usd/usd/stage.h>
#include <pxr/usd/usdGeom/xform.h>
#include <pxr/usd/usdGeom/cube.h>
#include <pxr/usd/usdGeom/mesh.h>
#include <pxr/usd/usdGeom/points.h>

DeclareSimpleCommand( helloWorld, "Autodesk", "2021" );

using namespace pxr;

MStatus helloWorld::doIt( const MArgList& )
{
    cout << "Start\n";

    MSelectionList selectionList;
    MGlobal::getActiveSelectionList(selectionList);

    MDagPath dagPath;
    selectionList.getDagPath(0, dagPath);

    cout << "hello2 path: " << dagPath.fullPathName() << "\n";

    MFnMesh mesh(dagPath);

    MFloatPointArray mayaPointArray;
    mesh.getPoints(mayaPointArray);


    pxr::VtArray<pxr::GfVec3f> usdPointArray;

    for(auto point : mayaPointArray){
        cout << "point: " << point << '\n';
        usdPointArray.push_back(pxr::GfVec3f(point[0], point[1], point[2]));
    }

    UsdStageRefPtr stage = UsdStage::CreateNew("/home/s5709975/Downloads/usd_cpp_export_test.usda");

    // UsdGeomXform xform = UsdGeomXform::Define(stage, SdfPath("/CubeGroup"));
    // UsdGeomCube cube = UsdGeomCube::Define(stage, SdfPath("/CubeGroup/Cube"));

    // UsdGeomMesh billboard = UsdGeomMesh::Define(stage, pxr::SdfPath("/mesh"));
    auto billboard = UsdGeomPoints::Define(stage, pxr::SdfPath("/mesh"));

    billboard.CreatePointsAttr(VtValue{usdPointArray});

    // billboard.CreatePointsAttr(pxr::VtValue{pxr::VtArray<pxr::GfVec3f> {
    //     {-1, -1, 0},
    //     {1, -1, 0},
    //     {1, 1, 0},
    //     {-1, 1, 0},
    //     // {-1, 0, 0},
    //     // {1, 0, 0},
    //     {1, 2, 1},
    //     {-1, 2, 1},
    // }});

    // billboard.CreateFaceVertexCountsAttr(pxr::VtValue{pxr::VtArray<int> {4, 4}});
    // billboard.CreateFaceVertexIndicesAttr(pxr::VtValue{pxr::VtArray<int> {0, 1, 2, 3, 3, 2, 4, 5}});
    // billboard.CreateExtentAttr(pxr::VtValue{pxr::VtArray<pxr::GfVec3f> {
    //     {
    //         {-1, -1, 0},
    //         {1, 1, 0},
    //     }
    // }});

    stage->GetRootLayer()->Save();

    cout << "End\n";
    return MS::kSuccess;
}
