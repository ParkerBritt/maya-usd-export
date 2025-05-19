#ifndef EXPORT_ITEM_H
#define EXPORT_ITEM_H

#include <maya/MDagPath.h>
#include <pxr/base/tf/token.h>

namespace MayaUSDExport{
class ExportItem{
public:
    ExportItem(MDagPath dagPath);
    MDagPath dagPath;
    // add exportArgs

    void setPrimType(pxr::TfToken usdTypeName) { usdTypeName_ = usdTypeName; }
    pxr::TfToken getPrimType() { return usdTypeName_; }
private:
    pxr::TfToken usdTypeName_;
};
}

#endif
