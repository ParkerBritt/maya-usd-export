#include "export.h"
#include "export/exportItem.h"
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

void MayaUSDExport::PrimWriter::addExportItem(ExportItem _exportItem){
    m_exportItems.push_back(_exportItem);
}


void MayaUSDExport::PrimWriter::writePrims(pxr::UsdStageRefPtr stage){

    for(MayaUSDExport::ExportItem exportItem : m_exportItems){
        cout << "export geo path: " << exportItem.dagPath.fullPathName() << "\n";
        MStringArray pathSplit;
        exportItem.dagPath.fullPathName().split('|', pathSplit);
        std::string geoName = pathSplit[pathSplit.length()-1].asChar();
        cout << "geo name: " << geoName << "\n";
        MFnMesh mesh(exportItem.dagPath);

        MFloatPointArray mayaPointArray;
        mesh.getPoints(mayaPointArray);


        pxr::VtArray<pxr::GfVec3f> usdPointArray;

        for(auto point : mayaPointArray){
            // cout << "point: " << point << '\n';
            usdPointArray.push_back(pxr::GfVec3f(point[0], point[1], point[2]));
        }


        auto newPrim = pxr::UsdGeomPoints::Define(stage, pxr::SdfPath("/"+geoName));

        newPrim.CreatePointsAttr(pxr::VtValue{usdPointArray});
    }


    cout << "End\n";
}

