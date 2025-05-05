#ifndef EXPORT_ITEM_H
#define EXPORT_ITEM_H

#include <maya/MDagPath.h>
#include <pxr/base/tf/token.h>

namespace MayaUSDExport{
class ExportItem{
public:
    ExportItem(MDagPath dagPath);
    MDagPath dagPath;
    pxr::TfToken usdTypeName;
    // add exportArgs

};
}

#endif
