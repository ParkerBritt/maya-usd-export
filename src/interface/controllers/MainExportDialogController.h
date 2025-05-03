#pragma once
#include "interface/main_export_dialog.h"
#include <QtCore/QPointer>

class MainExportDialogController
{
public:
    MainExportDialogController(QPointer<USDExportInterface> _view);

private:
    QPointer<USDExportInterface> m_view;
};
