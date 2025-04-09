#include <maya/MSimple.h>
#include <maya/MIOStream.h>
#include <maya/MGlobal.h>
#include <maya/MSelectionList.h>
#include <maya/MDagPath.h>

#include <pxr/usd/usd/stage.h>
#include <pxr/usd/usdGeom/xform.h>
#include <pxr/usd/usdGeom/cube.h>

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

    UsdStageRefPtr stage = UsdStage::CreateNew("/home/s5709975/Downloads/usd_cpp_export_test.usda");

    UsdGeomXform xform = UsdGeomXform::Define(stage, SdfPath("/CubeGroup"));

    // // Add a cube under it
    UsdGeomCube cube = UsdGeomCube::Define(stage, SdfPath("/CubeGroup/Cube"));

    cube.GetSizeAttr().Set(1.0);  // Optional: set size

    stage->GetRootLayer()->Save();

    cout << "End\n";
    return MS::kSuccess;
}
