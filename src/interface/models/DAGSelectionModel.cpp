#include "QtGui/qstandarditemmodel.h"
#include "export/PrimWriter.h"
#include "maya/MApiNamespace.h"
#include <maya/MDagPath.h>
#include <maya/MItDag.h>
#include <maya/MString.h>
#include <maya/MStringArray.h>
#include <unordered_map>

#include <QtCore/QList>

#include "interface/models/DAGSelectionModel.h"
#include "interface/models/DagSelectionModelColumns.h"

DAGSelectionModel::DAGSelectionModel()
{
    populateModel();

}

// populates the model from dag paths
void DAGSelectionModel::populateModel()
{
    QStandardItem *rootNode = invisibleRootItem();
    MItDag dagIter;
    std::unordered_map<std::string, QStandardItem*> pathItemMap;

    // iterate dag
    while(!dagIter.isDone())
    {
        QStandardItem *parentItem = rootNode;

        MDagPath dagPath;
        dagIter.getPath(dagPath);
        MString path = dagIter.fullPathName();


        // separate the path into nodes
        MStringArray pathSplit;
        path.split('|', pathSplit);

        // protect against empty paths
        if(pathSplit.length()==0){
            dagIter.next();
            continue;
        }


        // construct parent path
        std::string parentPath;
        for(size_t i = 0; i<pathSplit.length()-1; ++i)
        {
            parentPath+='|';
            parentPath+=pathSplit[i].asChar();
        }

        // get parent item
        if(pathItemMap.count(parentPath)>0)
        {
            parentItem = pathItemMap.at(parentPath);
        }

        MString nodeName = pathSplit[pathSplit.length()-1];

        // add item to model
        QList<QStandardItem*> rowItems;
        QStandardItem *nodeItem = formatModelItem(new QStandardItem(nodeName.asChar()));
        rowItems.insert(static_cast<int>(SelectionCol::MayaPrimName), nodeItem);
        std::string type = MayaUSDExport::PrimWriter::derivePrimType(dagPath);
        rowItems.insert(static_cast<int>(SelectionCol::UsdPrimType), new QStandardItem(type.c_str()));
        parentItem->appendRow(rowItems);


        // add self to pathItemMap
        pathItemMap[std::string(path.asChar())]=nodeItem;

        dagIter.next();
    }
}

QStandardItem* DAGSelectionModel::formatModelItem(QStandardItem* _item)
{
    _item->setCheckable(true);
    _item->setCheckState(Qt::Checked);
    // TODO: add editable functionality
    _item->setEditable(false);

    return _item;
}
