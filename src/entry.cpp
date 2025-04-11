#include <maya/MSimple.h>

#include <pxr/usd/usd/stage.h>

#include "export.h"

DeclareSimpleCommand( helloWorld, "Autodesk", "2021" );


MStatus helloWorld::doIt( const MArgList& args )
{
    cout << "Entry\n";
    std::string exportPath(args.asString(0).asChar());
    pxr::UsdStageRefPtr stage = pxr::UsdStage::CreateNew(exportPath);

    MayaUSDExport::PrimWriter primWriter;
    primWriter.writePrim(stage);

    cout << "exporting file to: " << exportPath << '\n';
    stage->GetRootLayer()->Save();


    return MS::kSuccess;

}
