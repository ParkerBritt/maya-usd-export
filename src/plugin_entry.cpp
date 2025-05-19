// plugin
#include <memory>
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
#include "export/PrimWriter.h"
#include "export/ExportItem.h"
#include "export/ExportOptions.h"

// interface
#include <QtCore/QPointer>
#include "interface/main_export_dialog.h"
#include "interface/controllers/MainExportDialogController.h"
#include "maya/MApiNamespace.h"

// flags
#define kFlagFile    "-f"
#define kFlagLongFile    "-file"
#define kFlagFrameRange    "-fr"
#define kFlagLongFrameRange     "-frameRange"
#define kFlagFrameInc      "-fi"
#define kFlagLongFrameInc       "-frameInc"




// ---- cli command ----
class USDExport : public MPxCommand
{
    public:
        USDExport();
        virtual ~USDExport();
        MStatus doIt( const MArgList& );
        MStatus parseArgs( const MArgList& args );
        bool isUndoable() const;
        static void* creator();

        static MSyntax newSyntax();
private:
    MString m_exportPath;
    double m_frameStart = 0;
    double m_frameEnd = 1;
    double m_frameInc = 1;
    MayaUSDExport::ExportOptions m_exportOptions;
};

MSyntax USDExport::newSyntax()
{
        MSyntax syntax;
        syntax.addFlag(kFlagFile, kFlagLongFile, MSyntax::kString);
        syntax.addFlag(kFlagFrameRange, kFlagLongFrameRange, MSyntax::kDouble, MSyntax::kDouble);
        syntax.addFlag(kFlagFrameInc, kFlagLongFrameInc, MSyntax::kDouble);

        return syntax;
}

USDExport::USDExport() {
    cout << "In USDExport::USDExport()\n";
}
USDExport::~USDExport() {
    cout << "In USDExport::~USDExport()\n";
}

MStatus USDExport::parseArgs( const MArgList& args )
{
    MStatus status = MS::kSuccess;

    MArgDatabase argData(syntax(), args, &status);
    cout << "got args\n";
    if(!status) return status;

    cout << "checking args\n";
    if (argData.isFlagSet(kFlagFile)) {
        argData.getFlagArgument(kFlagFile, 0, m_exportPath);
    }
    else {
        MGlobal::displayError("The -f/--file option is required.");
        return MS::kFailure;
    }
    if (argData.isFlagSet(kFlagFrameRange)) {
        argData.getFlagArgument(kFlagFrameRange, 0, m_exportOptions.animFrameStart);
        argData.getFlagArgument(kFlagFrameRange, 1, m_exportOptions.animFrameEnd);
        if(m_exportOptions.animFrameStart>m_exportOptions.animFrameEnd){
            MGlobal::displayError("Start frame cannot be greater than end frame");
            return MS::kFailure;
        }
    }
    if (argData.isFlagSet(kFlagFrameInc)) {
        argData.getFlagArgument(kFlagFrameInc, 0, m_exportOptions.animFrameInc);
    }

    cout << "-----\nexport args\n-----\n";
    cout << "file: " << m_exportOptions.animFrameStart << "\n";
    cout << "frame start: " << m_exportOptions.animFrameStart << "\n";
    cout << "frame count: " << m_exportOptions.animFrameEnd << "\n";
    cout << "frame inc: " << m_exportOptions.animFrameInc << "\n";

    return status;
}

MStatus USDExport::doIt( const MArgList& args) {
    cout << "Entry\n";
    MStatus status;
    status = parseArgs(args);
    if(!status){
        MGlobal::displayError("failed to parse args");
        return status;
    }

    std::string exportPath(m_exportPath.asChar());
    pxr::UsdStageRefPtr stage = pxr::UsdStage::CreateNew(exportPath);

    // get items in scene
    MSelectionList selectionList;
    MGlobal::getActiveSelectionList(selectionList);


    MayaUSDExport::PrimWriter primWriter(m_exportOptions);

    std::vector<MayaUSDExport::ExportItem> exportItems;
    MDagPath dagPath;
    for(size_t i=0; i<selectionList.length(); ++i){
        selectionList.getDagPath(i, dagPath);
        cout << "adding geo path: " << dagPath.fullPathName() << "\n";

        MayaUSDExport::ExportItem exportItem(dagPath);
        exportItem.setPrimType(pxr::TfToken(MayaUSDExport::PrimWriter::derivePrimType(dagPath)));
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
    static std::unique_ptr<MainExportDialogController> mainController;


    if (interface.isNull()) {
        interface = new USDExportInterface();
        mainController = std::make_unique<MainExportDialogController>(interface);
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





