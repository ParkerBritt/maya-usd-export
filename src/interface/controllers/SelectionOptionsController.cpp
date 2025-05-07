#include "interface/controllers/SelectionOptionsController.h"
#include <iostream>
#include "interface/models/DagSelectionModelColumns.h"

SelectionOptionsController::SelectionOptionsController(QPointer<USDExportInterface> view)
: view_(view)
{
    connect(view_->selectionOptions->m_selectionTree->selectionModel(), &QItemSelectionModel::selectionChanged, this, &SelectionOptionsController::updateParms);
    connect(view_->selectionOptions->m_selectionParameters->primTypeParm, &QComboBox::currentTextChanged, this, &SelectionOptionsController::primTypeChanged);
}

void SelectionOptionsController::primTypeChanged(const QString &text)
{
    QStandardItemModel* model = view_->selectionOptions->m_selectionTree->model;
    SelectionParameters* parms = view_->selectionOptions->m_selectionParameters;

    QModelIndex index = view_->selectionOptions->m_selectionTree->currentIndex().siblingAtColumn(static_cast<int>(SelectionCol::UsdPrimType));
    QStandardItem* usdTypeItem = model->itemFromIndex(index);
    usdTypeItem->setText(parms->primTypeParm->currentText());
}

void SelectionOptionsController::updateParms(const QItemSelection &selected, const QItemSelection &deselected)
{
    QStandardItemModel* model = view_->selectionOptions->m_selectionTree->model;
    SelectionParameters* parms = view_->selectionOptions->m_selectionParameters;

    // ----
    // handle previous selection
    // ----
    // if(!deselected.indexes().isEmpty())
    // {
    //     QModelIndex prevIndex = deselected.indexes().first();
    //     QStandardItem* usdTypeItem = model->item(prevIndex.row(), static_cast<int>(SelectionCol::UsdPrimType));
    //     parms->primTypeParm->currentText();
    // }

    // ----
    // handle current selection
    // ----
    if(!selected.indexes().isEmpty())
    {
        QModelIndex curIndex = selected.indexes().first();
        // get correct column
        curIndex = curIndex.siblingAtColumn(static_cast<int>(SelectionCol::UsdPrimType));
        QStandardItem* usdTypeItem = model->item(curIndex.row(), static_cast<int>(SelectionCol::UsdPrimType));
        // set combobox to model value
        parms->primTypeParm->blockSignals(true);
        parms->primTypeParm->setCurrentText(usdTypeItem->text());
        parms->primTypeParm->blockSignals(false);
        std::cout << "item selected" << usdTypeItem->text().toStdString() << "\n";
    }
}

