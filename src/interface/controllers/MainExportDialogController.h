#pragma once
#include "QtCore/qobject.h"
#include "QtCore/qobjectdefs.h"
#include "QtWidgets/qwidget.h"
#include "interface/main_export_dialog.h"
#include <QtCore/QPointer>

class MainExportDialogController
: public QObject
{
    Q_OBJECT
public:
    MainExportDialogController(QPointer<USDExportInterface> _view);

private:
    QPointer<USDExportInterface> m_view;

public slots:
    void doExport();

};
