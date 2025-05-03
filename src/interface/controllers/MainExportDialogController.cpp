#include <QtCore/QPointer>

#include <pxr/usd/usd/stage.h>

#include <maya/MGlobal.h>
#include <maya/MSelectionList.h>

#include "interface/controllers/MainExportDialogController.h"
#include "interface/main_export_dialog.h"

#include "export/PrimWriter.h"
#include "export/ExportOptions.h"
#include "export/exportItem.h"

MainExportDialogController::MainExportDialogController(QPointer<USDExportInterface> _view)
: m_view(_view)
{
    connect(m_view->m_exportButton, &QPushButton::clicked, this, &MainExportDialogController::doExport);
}

void MainExportDialogController::doExport()
{
    std::string exportPath = m_view->generalOptions->m_filePathLine->text().toStdString();

    pxr::UsdStageRefPtr stage = pxr::UsdStage::CreateNew(exportPath);

    // get items in scene
    MSelectionList selectionList;
    MGlobal::getActiveSelectionList(selectionList);

    MayaUSDExport::ExportOptions exportOptions;

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



}
