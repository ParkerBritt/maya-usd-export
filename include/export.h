#include <pxr/usd/usd/stage.h>

namespace maya_usd_export{
class PrimWriter {
public:
    PrimWriter();
    void writePrim(pxr::UsdStageRefPtr stage);
};
}

