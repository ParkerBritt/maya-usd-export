#include "interface/widgets/SelectionOptions.h"
#include "interface/models/DAGSelectionModel.h"
#include "QtWidgets/qboxlayout.h"
#include <QtWidgets/QSplitter>

SelectionOptions::SelectionOptions(){
    m_mainLayout = new QVBoxLayout();
    setLayout(m_mainLayout);

    m_splitter = new QSplitter();

    m_mainLayout->addWidget(m_splitter);


    m_selectionTree = new SelectionTree();
    m_splitter->addWidget(m_selectionTree);

    m_selectionParameters = new SelectionParameters();
    m_splitter->addWidget(m_selectionParameters);
}

SelectionTree::SelectionTree(){
    model = new DAGSelectionModel(); 
    setModel(model);
    expandAll();
}

