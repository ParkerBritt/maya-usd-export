#pragma once
#include "QtCore/qobject.h"
#include "QtCore/qobjectdefs.h"
#include "interface/main_export_dialog.h"
#include <QtCore/QPointer>

class SelectionOptionsController
: public QObject
{
    Q_OBJECT
public:
    SelectionOptionsController(QPointer<USDExportInterface> view);
private:
    QPointer<USDExportInterface> view_;
    void primTypeChanged(const QString &text);

public slots:
    void updateParms(const QItemSelection &selected, const QItemSelection &deselected);
};
