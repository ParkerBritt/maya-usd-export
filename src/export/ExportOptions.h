#pragma once

namespace MayaUSDExport
{

class ExportOptions
{
public:
    bool animate=false;
    int animRangeStart=0;
    int animRangeCount=0;
    int animRangeStep=1;

    bool createParents=false;
};

}
