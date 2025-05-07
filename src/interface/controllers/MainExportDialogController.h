#pragma once
#include "QtCore/qobject.h"
#include "QtCore/qobjectdefs.h"
#include "QtWidgets/qwidget.h"
#include "interface/main_export_dialog.h"
#include <QtCore/QPointer>
#include "interface/controllers/SelectionOptionsController.h"
#include "export/exportItem.h"

class MainExportDialogController
: public QObject
{
    Q_OBJECT
public:
    MainExportDialogController(QPointer<USDExportInterface> _view);

private:
    QPointer<USDExportInterface> m_view;
    SelectionOptionsController selectionOptionsController;
    void getExportItems(std::vector<MayaUSDExport::ExportItem>& exportItems, QStandardItem* item, std::string parentPath);

public slots:
    void doExport();

};
