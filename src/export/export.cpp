#include "export.h"
#include "export/exportItem.h"
#include "pxr/usd/sdf/path.h"
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

    bool CREATE_PARENTS = true;

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
        pxr::VtArray<int> usdVertexCount;
        pxr::VtArray<int> usdVertexIndices;


        // create points
        for(size_t i=0; i<mayaPointArray.length(); ++i){
            // cout << "point: " << point << '\n';
            auto point = mayaPointArray[i]; 
            usdPointArray.push_back(pxr::GfVec3f(point[0], point[1], point[2]));
        }


        // connect points
        MIntArray mayaVertexCount;
        MIntArray mayaVertexIndices;
        mesh.getVertices(mayaVertexCount, mayaVertexIndices);
        for(size_t i=0; i<mayaVertexCount.length();++i){
            usdVertexCount.push_back(mayaVertexCount[i]);
        }
        for(size_t i=0; i<mayaVertexIndices.length();++i){
            usdVertexIndices.push_back(mayaVertexIndices[i]);
        }


        // create parents
        std::string primPathStr;
        for(auto parent : pathSplit){
            primPathStr += '/';
            primPathStr += parent.asChar();

            if(CREATE_PARENTS){
                pxr::UsdGeomXform::Define(stage, pxr::SdfPath(primPathStr));
            }
        }
        cout << "parent: " << primPathStr << "\n";
        auto newPrim = pxr::UsdGeomMesh::Define(stage, pxr::SdfPath(primPathStr+'/'+geoName));

        newPrim.CreatePointsAttr(pxr::VtValue{usdPointArray});
        newPrim.CreateFaceVertexCountsAttr(pxr::VtValue{usdVertexCount});
        newPrim.CreateFaceVertexIndicesAttr(pxr::VtValue{usdVertexIndices});
    }


    cout << "End\n";
}

