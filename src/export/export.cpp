#include "export.h"
#include <iostream>

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


MayaUSDExport::PrimWriter::PrimWriter(){
    std::cout << "constructor\n";    
}

void MayaUSDExport::PrimWriter::writePrim(pxr::UsdStageRefPtr stage){


    MSelectionList selectionList;
    MGlobal::getActiveSelectionList(selectionList);

    MDagPath dagPath;
    selectionList.getDagPath(0, dagPath);

    cout << "export geo path: " << dagPath.fullPathName() << "\n";

    MFnMesh mesh(dagPath);

    MFloatPointArray mayaPointArray;
    mesh.getPoints(mayaPointArray);


    pxr::VtArray<pxr::GfVec3f> usdPointArray;

    for(auto point : mayaPointArray){
        cout << "point: " << point << '\n';
        usdPointArray.push_back(pxr::GfVec3f(point[0], point[1], point[2]));
    }


    auto newPrim = pxr::UsdGeomPoints::Define(stage, pxr::SdfPath("/mesh"));

    newPrim.CreatePointsAttr(pxr::VtValue{usdPointArray});


    cout << "End\n";
}

