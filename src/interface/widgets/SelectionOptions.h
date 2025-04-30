#pragma once
#include "QtWidgets/qboxlayout.h"
#include <QtWidgets/QWidget>
#include <QtWidgets/QSplitter>
#include <QtWidgets/QTreeView>
#include "interface/models/DAGSelectionModel.h"


class SelectionParameters : public QWidget {
    Q_OBJECT
public:
    SelectionParameters();
};

class SelectionTree : public QTreeView {
    Q_OBJECT
public:
    SelectionTree();
    DAGSelectionModel *m_model;
};

class SelectionOptions : public QWidget {
    Q_OBJECT
public:
    SelectionOptions();

    QVBoxLayout *m_mainLayout;
    QSplitter *m_splitter;
    SelectionTree *m_selectionTree;
    SelectionParameters *m_selectionParameters;
private:
};
