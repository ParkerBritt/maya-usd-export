#include <maya/MSimple.h>
#include <maya/MIOStream.h>
#include <maya/MGlobal.h>
#include <maya/MSelectionList.h>
#include <maya/MDagPath.h>
#include <maya/MFnMesh.h>
#include <maya/MFloatPointArray.h>

// #include <pxr/usd/usd/stage.h>
// #include <pxr/usd/usdGeom/xform.h>
// #include <pxr/usd/usdGeom/cube.h>
// #include <pxr/usd/usdGeom/mesh.h>
// #include <pxr/usd/usdGeom/points.h>

#include "export.h"

DeclareSimpleCommand( helloWorld, "Autodesk", "2021" );

// using namespace pxr;

MStatus helloWorld::doIt( const MArgList& args )
{
    cout << "Entry\n";
    foo();
    return MS::kSuccess;

    // std::string exportPath(args.asString(0).asChar());
    // cout << "exporting file to: " << exportPath << '\n';
    // 

    // MSelectionList selectionList;
    // MGlobal::getActiveSelectionList(selectionList);

    // MDagPath dagPath;
    // selectionList.getDagPath(0, dagPath);

    // cout << "hello2 path: " << dagPath.fullPathName() << "\n";

    // MFnMesh mesh(dagPath);

    // MFloatPointArray mayaPointArray;
    // mesh.getPoints(mayaPointArray);


    // pxr::VtArray<pxr::GfVec3f> usdPointArray;

    // for(auto point : mayaPointArray){
    //     cout << "point: " << point << '\n';
    //     usdPointArray.push_back(pxr::GfVec3f(point[0], point[1], point[2]));
    // }

    // UsdStageRefPtr stage = UsdStage::CreateNew(exportPath);

    // auto billboard = UsdGeomPoints::Define(stage, pxr::SdfPath("/mesh"));

    // billboard.CreatePointsAttr(VtValue{usdPointArray});

    // stage->GetRootLayer()->Save();

    // cout << "End\n";
    // return MS::kSuccess;
}
