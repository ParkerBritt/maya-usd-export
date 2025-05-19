#pragma once
#include <string>

namespace MayaUSDExport
{

class ExportOptions
{
public:
    int animFrameStart=0;
    int animFrameEnd=0;
    int animFrameInc=1;

    bool createParents=false;
};

}
