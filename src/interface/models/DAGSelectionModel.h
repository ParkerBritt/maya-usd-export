#pragma once

#include "QtCore/qobjectdefs.h"
#include <QtGui/QStandardItemModel>
#include <QtGui/QStandardItem>

class DAGSelectionModel : public QStandardItemModel
{
    Q_OBJECT
public:
    DAGSelectionModel();
    void populateModel();
private:
    QStandardItem* formatModelItem(QStandardItem* _item);
};
