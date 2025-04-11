#ifndef PRIM_WRITER_H
#define PRIM_WRITER_H

#include <pxr/usd/usd/stage.h>

namespace MayaUSDExport{
class PrimWriter {
public:
    PrimWriter();
    void writePrim(pxr::UsdStageRefPtr stage);
};
}

#endif
