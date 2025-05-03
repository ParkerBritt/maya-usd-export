#include <QtCore/QPointer>
#include "interface/controllers/MainExportDialogController.h"
#include "interface/main_export_dialog.h"

MainExportDialogController::MainExportDialogController(QPointer<USDExportInterface> _view)
: m_view(_view)
{
    m_view->animationOptions->m_animRangeStart->setValue(5);
}
