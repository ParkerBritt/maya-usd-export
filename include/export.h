#ifndef PRIM_WRITER_H
#define PRIM_WRITER_H

#include <pxr/usd/usd/stage.h>
#include "export/exportItem.h"

namespace MayaUSDExport{
class PrimWriter {
public:
    PrimWriter();
    void writePrims(pxr::UsdStageRefPtr stage);
    void addExportItem(ExportItem _exportItem);
    pxr::VtArray<pxr::GfVec3f> convertMayaPoints(MDagPath _meshPath);
    std::vector<ExportItem> m_exportItems;
};
}

#endif
