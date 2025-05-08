#include "export/PrimWriter.h"
#include "export/exportItem.h"
#include "maya/MApiNamespace.h"
#include "maya/MFn.h"
#include "maya/MTypes.h"
#include "pxr/usd/sdf/path.h"
#include "pxr/usd/usd/attribute.h"
#include <iostream>

#include <maya/MGlobal.h>
#include <maya/MDagPath.h>
#include <maya/MFnMesh.h>
#include <maya/MFnCamera.h>
#include <maya/MFnTransform.h>
#include <maya/MFloatPointArray.h>
#include <maya/MFloatArray.h>
#include <maya/MMatrix.h>

#include <pxr/usd/usd/stage.h>
#include <pxr/usd/usdGeom/xform.h>
#include <pxr/usd/usdGeom/cube.h>
#include <pxr/usd/usdGeom/mesh.h>
#include <pxr/usd/usdGeom/points.h>
#include <pxr/usd/sdf/valueTypeName.h>
#include <pxr/usd/sdf/types.h>
#include <pxr/usd/usdGeom/tokens.h>
#include <pxr/usd/usdGeom/primvarsAPI.h>
#include <tuple>
#include <unordered_map>


MayaUSDExport::PrimWriter::PrimWriter(ExportOptions& _exportOptions)
: m_exportOptions(_exportOptions)
{
    std::cout << "constructor\n";    
}

void MayaUSDExport::PrimWriter::addExportItem(ExportItem _exportItem){
    m_exportItems.push_back(_exportItem);
}

void MayaUSDExport::PrimWriter::getDagPathType(const MDagPath& dagPath)
{
    MStatus status;

    if (dagPath.hasFn(MFn::kCamera)) {
        MFnCamera cameraFn(dagPath, &status);
        if (status) {
            MGlobal::displayInfo("It's a camera.");
            return;
        }
    }
    if (dagPath.hasFn(MFn::kMesh)) {
        MFnMesh meshFn(dagPath, &status);
        if (status) {
            MGlobal::displayInfo("It's a mesh.");
            return;
        }
    }
    if (dagPath.hasFn(MFn::kTransform)) {
        MFnTransform transformFn(dagPath, &status);
        if (status) {
            MGlobal::displayInfo("It's a transform.");
            return;
        }
    }

    // fallback
    MGlobal::displayInfo("Unknown or unhandled node type.");
}

void MayaUSDExport::PrimWriter::writePrims(pxr::UsdStageRefPtr stage){

    bool CREATE_PARENTS = true;
    bool TIME_VARYING = true;

    for(MayaUSDExport::ExportItem exportItem : m_exportItems){
        cout << "export geo path: " << exportItem.dagPath.fullPathName() << "\n";
        MGlobal::displayInfo(exportItem.dagPath.fullPathName());
        MGlobal::displayInfo(exportItem.dagPath.node().apiTypeStr());
        MStringArray pathSplit;
        exportItem.dagPath.fullPathName().split('|', pathSplit);
        std::string geoName = pathSplit[pathSplit.length()-1].asChar();
        cout << "geo name: " << geoName << "\n";
        MFnMesh mayaMesh(exportItem.dagPath);

        cout << "DAG PATH: " << exportItem.dagPath.transform().apiTypeStr() << "\n";

        pxr::VtArray<int> usdVertexCount;
        pxr::VtArray<int> usdVertexIndices;


        // create and connect points
        // set vertexCount and mayaVertexIndices
        MIntArray mayaVertexCount;
        MIntArray mayaVertexIndices;
        mayaMesh.getVertices(mayaVertexCount, mayaVertexIndices);
        for(size_t i=0; i<mayaVertexCount.length();++i){
            usdVertexCount.push_back(mayaVertexCount[i]);
        }
        for(size_t i=0; i<mayaVertexIndices.length();++i){
            usdVertexIndices.push_back(mayaVertexIndices[i]);
        }


        // get parent path
        std::string primPathStr;
        for(auto parent : pathSplit){
            primPathStr += '/';
            primPathStr += parent.asChar();

            // create parents
            if(CREATE_PARENTS){
                pxr::UsdGeomXform::Define(stage, pxr::SdfPath(primPathStr));
            }
        }

        pxr::UsdPrim usdPrim;
        pxr::TfToken usdPrimType = exportItem.getPrimType();
        pxr::SdfPath primPath(primPathStr);

        // create prim
        if(usdPrimType==pxr::TfToken("Mesh"))
        {
            cout << "parent: " << primPathStr << "\n";
            pxr::UsdGeomMesh usdMesh = pxr::UsdGeomMesh::Define(stage, primPath);
            usdPrim = usdMesh.GetPrim();

            // assign points and vertices
            pxr::UsdAttribute pointsAttr = usdMesh.CreatePointsAttr(pxr::VtValue{convertMayaPoints(exportItem.dagPath)});
            usdMesh.CreateFaceVertexCountsAttr(pxr::VtValue{usdVertexCount});
            usdMesh.CreateFaceVertexIndicesAttr(pxr::VtValue{usdVertexIndices});

            buildUVs(usdMesh, mayaMesh);

            animatePoints(pointsAttr, exportItem);
            setPrimType(usdPrim, usdPrimType);
            setTransform(usdPrim, exportItem.dagPath);
        }
        else if (usdPrimType == pxr::TfToken("Xform"))
        {
            usdPrim = stage->DefinePrim(primPath, usdPrimType);
        }
        else if (usdPrimType == pxr::TfToken("Scope"))
        {
            usdPrim = stage->DefinePrim(primPath, usdPrimType);
        }
        else
        {
            usdPrim = stage->DefinePrim(primPath, usdPrimType);
            std::string errMsg = "Invalid prim type: " + usdPrimType.GetString();
            MGlobal::displayError(MString(errMsg.c_str()));
            continue;
        }

    }


    cout << "End\n";
}

std::string MayaUSDExport::PrimWriter::derivePrimType(MDagPath dagPath, bool promoteShapes)
{
    std::cout << "deriving path for: " << dagPath.fullPathName() << "\n";
    std::string primTypeName;
    std::string defaultType = "None";

    MFn::Type apiType = dagPath.node().apiType();

    std::unordered_map<MFn::Type, std::string> typeMap =
        {
            {MFn::Type::kMesh, "Mesh"},
            {MFn::Type::kTransform, "Xform"},
        };

    // promotes the type of the shape to the parent
    // so if foo/fooShape is a mesh foo instead becomes a mesh
    if(promoteShapes)
    {
        // check if path has a shape child
        bool hasShape = false;
        MObject shapeObj;
        for(unsigned int i=0; i<dagPath.childCount(); ++i)
        {
            MObject child = dagPath.child(i);
            if(child.hasFn(MFn::Type::kShape))
            {
                hasShape = true;
                shapeObj = child;
                break;
            }
        }

        // get shape type
        if(hasShape)
        {
            apiType = shapeObj.apiType(); 
            std::cout << "child has api type: " << shapeObj.apiTypeStr() << '\n';
        }

    }

    // not in type map
    if(typeMap.find(apiType)==typeMap.end())
    {
        std::cout << "default\n";
        return defaultType;
    }

    primTypeName = typeMap[apiType];

    std::cout << "type: " << primTypeName << "\n";
    
    return primTypeName;
}



void MayaUSDExport::PrimWriter::setTransform(pxr::UsdPrim usdPrim, MDagPath dagPath)
{
    if(!dagPath.hasFn(MFn::kTransform))
    {
        MGlobal::displayError(MString("Cannot set transform on type:") + dagPath.node().apiTypeStr() + " " + dagPath.fullPathName());
        return;
    }
    MFnTransform transformFn(dagPath);
    MTransformationMatrix mayaTransformApi = transformFn.transformation();
    MMatrix mayaTransformMatrix = mayaTransformApi.asMatrix();
    double mDouble[4][4];
    mayaTransformMatrix.get(mDouble);

    pxr::UsdGeomXformable geom(usdPrim);
    pxr::UsdGeomXformOp XformOp = geom.AddTransformOp();
    XformOp.Set(pxr::GfMatrix4d(mDouble));
}


void MayaUSDExport::PrimWriter::setPrimType(pxr::UsdPrim& prim, const pxr::TfToken& primTypeName)
{
    if(primTypeName==pxr::TfToken())
    {
        std::cout << "prim writer empty type\n";
        return;
    }
    prim.SetTypeName(primTypeName); 
}


pxr::UsdGeomPrimvar MayaUSDExport::PrimWriter::buildUVs(pxr::UsdGeomMesh &_usdMesh, MFnMesh &_mayaMesh)
{
    pxr::UsdPrim prim = _usdMesh.GetPrim();
    pxr::UsdGeomPrimvar texCoords = pxr::UsdGeomPrimvarsAPI(prim).CreatePrimvar(
        pxr::TfToken("st"),
        pxr::SdfValueTypeNames->TexCoord2fArray,
        pxr::UsdGeomTokens->faceVarying
    );

    // all unique uvs on the mesh
    MFloatArray uArray;
    MFloatArray vArray;
    _mayaMesh.getUVs(uArray, vArray);

    // non unique uv indices as they are assigned in mapping
    MIntArray uvCounts;
    MIntArray uvIds;
    _mayaMesh.getAssignedUVs(uvCounts, uvIds);

    if(uArray.length()!=vArray.length()){
        MGlobal::displayError("U and V arrays incorrect length");
    }

    pxr::VtArray<pxr::GfVec2f> stArray;
    for(size_t i=0; i<uvIds.length(); ++i)
    {
        int uvId = uvIds[i];
        std::cout << "u: " << uArray[uvId] << " v: " << vArray[uvId] << "\n";
        stArray.push_back(pxr::GfVec2f(uArray[uvId], vArray[uvId]));
    }

    texCoords.Set(pxr::VtValue{stArray});
    return texCoords;
}

void MayaUSDExport::PrimWriter::animatePoints(pxr::UsdAttribute _pointsAttr, ExportItem _exportItem)
{
    for(int i=m_exportOptions.animFrameStart; i<=m_exportOptions.animFrameEnd; i++)
    {
        cout << "frame: " << i << "\n";
        MGlobal::viewFrame(i);
        _pointsAttr.Set(pxr::VtValue{convertMayaPoints(_exportItem.dagPath)}, i);
    }
}

pxr::VtArray<pxr::GfVec3f> MayaUSDExport::PrimWriter::convertMayaPoints(MDagPath _meshPath){
    MFnMesh mesh;
    // MGlobal::viewFrame(i);
    mesh.setObject(_meshPath);

    MFloatPointArray mayaPointArray;
    mesh.getPoints(mayaPointArray);

    pxr::VtArray<pxr::GfVec3f> usdPointArray;
    for(size_t i=0; i<mayaPointArray.length(); ++i){
        auto point = mayaPointArray[i]; 
        cout << point[0] << ' ' << point[1] << ' ' << point[2] << "\n";
        usdPointArray.push_back(pxr::GfVec3f(point[0], point[1], point[2]));
    }
    return usdPointArray;
}

