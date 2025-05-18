#include <QtCore/QPointer>
#include <QtWidgets/QTreeView>

#include <pxr/usd/usd/stage.h>

#include <maya/MGlobal.h>
#include <maya/MSelectionList.h>

#include "interface/controllers/MainExportDialogController.h"
#include "QtCore/qnamespace.h"
#include "QtGui/qstandarditemmodel.h"
#include "interface/main_export_dialog.h"
#include "interface/widgets/SelectionParameters.h"
#include "interface/models/DagSelectionModelColumns.h"

#include "export/PrimWriter.h"
#include "export/ExportOptions.h"
#include "export/exportItem.h"
#include "maya/MApiNamespace.h"

MainExportDialogController::MainExportDialogController(QPointer<USDExportInterface> _view)
: m_view(_view), selectionOptionsController(_view)
{
    QStandardItemModel* model = m_view->selectionOptions->m_selectionTree->model;
    SelectionParameters* parms = m_view->selectionOptions->m_selectionParameters;

    connect(m_view->m_exportButton, &QPushButton::clicked, this, &MainExportDialogController::doExport);

}


void MainExportDialogController::getExportItems(std::vector<MayaUSDExport::ExportItem>& exportItems, QStandardItem* item, std::string parentPath)
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
        getExportItems(exportItems, child, constructedPath);

        // get name
        MString dagPathStr = constructedPath.c_str();
        MDagPath dagPath;

        MSelectionList selectionList;
        if(!selectionList.add(dagPathStr))
        {
            cout << "failed to add " << dagPathStr << "\n";
        }
        selectionList.getDagPath(0, dagPath);

        // for model lookup
        QStandardItemModel* model = child->model();
        QModelIndex childIndex = child->index();

        // get type
        QModelIndex usdTypeIndex = childIndex.siblingAtColumn(static_cast<int>(SelectionCol::UsdPrimType));
        QString usdTypeName = model->itemFromIndex(usdTypeIndex)->text();

        // debug
        // cout << "creating export item for: " << dagPath.fullPathName() << "\n";
        // cout << "type: " << usdTypeName.toStdString() << "\n";

        MayaUSDExport::ExportItem exportItem(dagPath);
        exportItem.setPrimType(pxr::TfToken(usdTypeName.toStdString()));
        exportItems.push_back(exportItem);
    }

}

void MainExportDialogController::doExport()
{
    std::string exportPath = m_view->generalOptions->m_filePathLine->text().toStdString();
    if(
        !(
            (exportPath.size()>=4 && exportPath.substr(exportPath.size()-4, 4) == ".usd") ||
            (exportPath.size()>=5 && exportPath.substr(exportPath.size()-5, 5) == ".usda") ||
            (exportPath.size()>=5 && exportPath.substr(exportPath.size()-5, 5) == ".usdc")
        )
    )
    {
        MGlobal::displayError("Invalid export path, must end with .usd, .usda, or .usdc");
        return;
    }

    QStandardItemModel* model = m_view -> selectionOptions -> m_selectionTree -> model;

    MSelectionList selectionList;

    pxr::UsdStageRefPtr stage = pxr::UsdStage::CreateNew(exportPath);

    // get items in scene
    std::vector<MayaUSDExport::ExportItem> exportItems;
    getExportItems(exportItems, model->invisibleRootItem(), std::string());

    MayaUSDExport::ExportOptions exportOptions;

    if(m_view->animationOptions->m_doAnimationToggle->checkState() == Qt::CheckState::Checked)
    {
        exportOptions.animFrameStart = m_view->animationOptions->m_animRangeStart->value();
        exportOptions.animFrameEnd = m_view->animationOptions->m_animRangeEnd->value();
        exportOptions.animFrameInc = m_view->animationOptions->m_animRangeStep->value();
    }

    MayaUSDExport::PrimWriter primWriter(exportOptions);

    MDagPath dagPath;
    for(size_t i=0; i<exportItems.size(); ++i){
        MayaUSDExport::ExportItem exportItem = exportItems[i];

        primWriter.addExportItem(exportItem);
    }


    primWriter.writePrims(stage);

    cout << "exporting file to: " << exportPath << '\n';
    stage->GetRootLayer()->Save();



}
