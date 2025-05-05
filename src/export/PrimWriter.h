#pragma once

#include <pxr/usd/usd/stage.h>
#include <pxr/usd/usd/prim.h>
#include <pxr/usd/usdGeom/mesh.h>
#include <pxr/usd/usdGeom/primvar.h>
#include "export/exportItem.h"
#include "export/ExportOptions.h"

namespace MayaUSDExport{
class PrimWriter {
public:
    PrimWriter(ExportOptions& _exportOptions);
    void writePrims(pxr::UsdStageRefPtr stage);
    void addExportItem(ExportItem _exportItem);
    std::vector<ExportItem> m_exportItems;
private:
    pxr::VtArray<pxr::GfVec3f> convertMayaPoints(MDagPath _meshPath);
    ExportOptions& m_exportOptions;
    void animatePoints(pxr::UsdAttribute _pointsAttr, ExportItem _exportItem);
    pxr::UsdGeomPrimvar buildUVs(pxr::UsdGeomMesh &_usdMesh, MFnMesh &_mayaMesh);
    void getDagPathType(const MDagPath& dagPath);
    void setPrimType(pxr::UsdPrim& prim, const pxr::TfToken& primTypeName);
};
}
