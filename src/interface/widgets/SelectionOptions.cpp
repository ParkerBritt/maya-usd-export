#include "interface/widgets/SelectionOptions.h"
#include "interface/models/DAGSelectionModel.h"
#include "QtWidgets/qboxlayout.h"
#include <QtWidgets/QSplitter>

SelectionOptions::SelectionOptions(){
    mainLayout = new QVBoxLayout();
    setLayout(mainLayout);

    splitter = new QSplitter();

    mainLayout->addWidget(splitter);


    m_selectionTree = new SelectionTree();
    splitter->addWidget(m_selectionTree);

    m_selectionParameters = new SelectionParameters();
    splitter->addWidget(m_selectionParameters);
}

SelectionTree::SelectionTree(){
    model = new DAGSelectionModel(); 
    setModel(model);
    expandAll();
}

