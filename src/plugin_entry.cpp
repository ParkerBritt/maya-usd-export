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
#include <maya/MSyntax.h>
#include <maya/MArgDatabase.h>
#include <pxr/usd/usd/stage.h>
#include <sys/select.h>
#include "export.h"
#include "export/exportItem.h"
#include "export/ExportOptions.h"

// interface
#include <QtCore/QPointer>
#include "interface/main_export_dialog.h"
#include "maya/MApiNamespace.h"



// ---- cli command ----
class USDExport : public MPxCommand
{
    public:
        USDExport();
        virtual ~USDExport();
        MStatus doIt( const MArgList& );
        bool isUndoable() const;
        static void* creator();

        static MSyntax newSyntax();
};

MSyntax USDExport::newSyntax()
{
        MSyntax syntax;
        syntax.addFlag("", "-AnimStart", MSyntax::kString);

        return syntax;
}

USDExport::USDExport() {
    cout << "In USDExport::USDExport()\n";
}
USDExport::~USDExport() {
    cout << "In USDExport::~USDExport()\n";
}


MStatus USDExport::doIt( const MArgList& args) {
    cout << "Entry\n";
    MStatus status;
    MArgDatabase argData(syntax(), args, &status);
    cout << "got args\n";
    if(!status) return status;

    cout << "checking args\n";
    if (argData.isFlagSet("-AnimStart")) {
        MString value;
        argData.getFlagArgument("-AnimStart", 0, value);
        MGlobal::displayInfo("Got flag value: " + value);
    }
    else{
        MGlobal::displayInfo("invalid flag");
    }

    return MS::kSuccess;
    std::string exportPath(args.asString(0).asChar());
    pxr::UsdStageRefPtr stage = pxr::UsdStage::CreateNew(exportPath);

    // get items in scene
    MSelectionList selectionList;
    MGlobal::getActiveSelectionList(selectionList);

    // set options
    MayaUSDExport::ExportOptions exportOptions;
    exportOptions.animate = true;
    exportOptions.animRangeStart = 0;
    exportOptions.animRangeCount = 6;

    MayaUSDExport::PrimWriter primWriter(exportOptions);

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
bool USDExport::isUndoable() const {
    return false;
}
void* USDExport::creator() {
    cout << "In USDExport::creator()\n";
    return new USDExport();
}

// ---- gui command ----
class USDExportGUI : public MPxCommand
{
    public:
        USDExportGUI();
        MStatus doIt( const MArgList& );
        bool isUndoable() const;
        static void* creator();
};
MStatus USDExportGUI::doIt( const MArgList& args) {
    static QPointer<USDExportInterface> interface;

    if (interface.isNull()) {
        interface = new USDExportInterface();
        interface->show();
    } else {
        interface->showNormal();
        interface->raise();
    }
    return MS::kSuccess;
}

USDExportGUI::USDExportGUI() {
    cout << "In USDExportGUI::USDExportGUI()\n";
}
bool USDExportGUI::isUndoable() const {
    return false;
}
void* USDExportGUI::creator() {
    cout << "In USDExportGUI::creator()\n";
    return new USDExportGUI();
}



MStatus initializePlugin( MObject obj )
{
    MFnPlugin plugin( obj, "Parker Britt", "0.1", "Any" );
    plugin.registerCommand( "USDExport", USDExport::creator , USDExport::newSyntax);
    plugin.registerCommand( "USDExportGUI", USDExportGUI::creator );
    cout << "In initializePlugin()\n";
    return MS::kSuccess;
}

MStatus uninitializePlugin( MObject obj )
{
    MFnPlugin plugin( obj );
    plugin.deregisterCommand( "USDExport" );
    plugin.deregisterCommand( "USDExportGUI" );
    cout << "In uninitializePlugin()\n";
    return MS::kSuccess;
}





