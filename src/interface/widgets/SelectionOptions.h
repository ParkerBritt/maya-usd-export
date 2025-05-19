#pragma once
#include "QtWidgets/qboxlayout.h"
#include <QtWidgets/QWidget>
#include <QtWidgets/QSplitter>
#include <QtWidgets/QTreeView>
#include "interface/models/DAGSelectionModel.h"
#include "interface/widgets/SelectionParameters.h"


class SelectionTree : public QTreeView {
    Q_OBJECT
public:
    SelectionTree();
    DAGSelectionModel* model;
};

class SelectionOptions : public QWidget {
    Q_OBJECT
public:
    SelectionOptions();

    QVBoxLayout *mainLayout;
    QSplitter *splitter;
    SelectionTree *m_selectionTree;
    SelectionParameters *m_selectionParameters;
private:
};
