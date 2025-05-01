#ifndef PRIM_WRITER_H
#define PRIM_WRITER_H

#include <algorithm>
#include <memory>
#include <pxr/usd/usd/stage.h>
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
};
}

#endif
