#include <maya/MSimple.h>
#include <maya/MGlobal.h>
#include <maya/MSelectionList.h>
#include <maya/MDagPath.h>
#include <maya/MFnMesh.h>
#include <maya/MFloatPointArray.h>

#include <pxr/usd/usd/stage.h>
#include <sys/select.h>

#include "export.h"
#include "export/exportItem.h"

DeclareSimpleCommand( USDExport, "Autodesk", "2021" );


MStatus USDExport::doIt( const MArgList& args )
{
    cout << "Entry\n";
    std::string exportPath(args.asString(0).asChar());
    pxr::UsdStageRefPtr stage = pxr::UsdStage::CreateNew(exportPath);

    // get items in scene
    MSelectionList selectionList;
    MGlobal::getActiveSelectionList(selectionList);

    MayaUSDExport::PrimWriter primWriter;

    std::vector<MayaUSDExport::ExportItem> exportItems;
    MDagPath dagPath;
    for(size_t i=0; i<selectionList.length(); ++i){
        selectionList.getDagPath(i, dagPath);
        cout << "adding geo path: " << dagPath.fullPathName() << "\n";

        MayaUSDExport::ExportItem exportItem(dagPath);
        primWriter.addExportItem(exportItem);
    }


    primWriter.writePrims(stage);

    cout << "exporting file to: " << exportPath << '\n';
    stage->GetRootLayer()->Save();


    return MS::kSuccess;

}
