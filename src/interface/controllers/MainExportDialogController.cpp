#include <QtCore/QPointer>

#include <pxr/usd/usd/stage.h>

#include <maya/MGlobal.h>
#include <maya/MSelectionList.h>

#include "interface/controllers/MainExportDialogController.h"
#include "QtGui/qstandarditemmodel.h"
#include "interface/main_export_dialog.h"

#include "export/PrimWriter.h"
#include "export/ExportOptions.h"
#include "export/exportItem.h"
#include "maya/MApiNamespace.h"

MainExportDialogController::MainExportDialogController(QPointer<USDExportInterface> _view)
: m_view(_view)
{
    connect(m_view->m_exportButton, &QPushButton::clicked, this, &MainExportDialogController::doExport);
}

void getModelDagPaths(MSelectionList& selectionPaths, QStandardItem* item, std::string parentPath)
{
    for(int row=0; row<item->rowCount(); ++row)
    {
        QStandardItem* child = item->child(row, 0);
        // skip if no children exist
        if(!child) continue;
        // only include checked items
        if(child->checkState() != Qt::Checked) continue;
        cout << "ITERATING ITEM: " << child->text().toStdString() << "\n";
        std::string constructedPath = parentPath+"|"+child->text().toStdString();
        getModelDagPaths(selectionPaths, child, constructedPath);

        MString dagPathStr = constructedPath.c_str();
        MDagPath dagPath;

        if(!selectionPaths.add(dagPathStr))
        {
            cout << "failed to add " << dagPathStr << "\n";
        }
    }

}

void MainExportDialogController::doExport()
{
    std::string exportPath = m_view->generalOptions->m_filePathLine->text().toStdString();

    QStandardItemModel* model = m_view -> selectionOptions -> m_selectionTree -> model;

    MSelectionList selectionList;

    pxr::UsdStageRefPtr stage = pxr::UsdStage::CreateNew(exportPath);

    // get items in scene
    // MGlobal::getActiveSelectionList(selectionList);
    getModelDagPaths(selectionList, model->invisibleRootItem(), std::string());

    MayaUSDExport::ExportOptions exportOptions;

    MayaUSDExport::PrimWriter primWriter(exportOptions);

    std::vector<MayaUSDExport::ExportItem> exportItems; MDagPath dagPath;
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
