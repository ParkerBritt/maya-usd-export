#include "interface/models/DAGSelectionModel.h"
#include "maya/MApiNamespace.h"
#include <maya/MDagPath.h>
#include <maya/MItDag.h>
#include <maya/MString.h>
#include <maya/MStringArray.h>
#include <unordered_map>

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

        // add item to model
        MString nodeName = pathSplit[pathSplit.length()-1];
        QStandardItem *nodeItem = new QStandardItem(nodeName.asChar());
        formatModelItem(nodeItem);
        parentItem->appendRow(nodeItem);

        // add self to pathItemMap
        pathItemMap[std::string(path.asChar())]=nodeItem;

        dagIter.next();
    }
}

void DAGSelectionModel::formatModelItem(QStandardItem* _item)
{
    _item->setCheckable(true);
    // TODO: add editable functionality
    _item->setEditable(false);
}
