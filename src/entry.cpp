// plugin
#include <stdio.h>
#include <maya/MString.h>
#include <maya/MArgList.h>
#include <maya/MFnPlugin.h>
#include <maya/MPxCommand.h>
#include <maya/MIOStream.h>

// doit
#include <maya/MGlobal.h>
#include <maya/MSelectionList.h>
#include <maya/MDagPath.h>
#include <maya/MFnMesh.h>
#include <maya/MFloatPointArray.h>
#include <pxr/usd/usd/stage.h>
#include <sys/select.h>
#include "export.h"
#include "export/exportItem.h"

class USDExport : public MPxCommand
{
    public:
        USDExport();
        virtual ~USDExport();
        MStatus doIt( const MArgList& );
        MStatus redoIt();
        MStatus undoIt();
        bool isUndoable() const;
        static void* creator();
};
USDExport::USDExport() {
    cout << "In USDExport::USDExport()\n";
}
USDExport::~USDExport() {
    cout << "In USDExport::~USDExport()\n";
}
MStatus USDExport::doIt( const MArgList& args) {
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
MStatus USDExport::redoIt() {
    cout << "In USDExport::redoIt()\n";
    return MS::kSuccess;
}
MStatus USDExport::undoIt() {
    cout << "In USDExport::undoIt()\n";
    return MS::kSuccess;
}
bool USDExport::isUndoable() const {
    cout << "In USDExport::isUndoable()\n";
    return true;
}
void* USDExport::creator() {
    cout << "In USDExport::creator()\n";
    return new USDExport();
}
MStatus initializePlugin( MObject obj )
{
    MFnPlugin plugin( obj, "Parker Britt", "0.1", "Any" );
    plugin.registerCommand( "USDExport", USDExport::creator );
    cout << "In initializePlugin()\n";
    return MS::kSuccess;
}
MStatus uninitializePlugin( MObject obj )
{
    MFnPlugin plugin( obj );
    plugin.deregisterCommand( "USDExport" );
    cout << "In uninitializePlugin()\n";
    return MS::kSuccess;
}
