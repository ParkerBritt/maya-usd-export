#include "QtCore/qnamespace.h"
#include "QtGui/qstandarditemmodel.h"
#include "export/PrimWriter.h"
#include "maya/MApiNamespace.h"
#include <maya/MDagPath.h>
#include <maya/MItDag.h>
#include <maya/MString.h>
#include <maya/MStringArray.h>
#include <maya/MSelectionList.h>
#include <maya/MGlobal.h>
#include <unordered_map>

#include <QtCore/QList>

#include "interface/models/DAGSelectionModel.h"
#include "interface/models/DagSelectionModelColumns.h"
#include "maya/MStatus.h"

DAGSelectionModel::DAGSelectionModel()
{
    // set header names
    this->setColumnCount(2);
    this->setHeaderData(0, Qt::Horizontal, "Name");
    this->setHeaderData(1, Qt::Horizontal, "Type");

    // pupulate the model from dag paths
    populateModel();

}

// populates the model from dag paths
void DAGSelectionModel::populateModel()
{
    QStandardItem *rootNode = invisibleRootItem();
    MItDag dagIter;
    std::unordered_map<std::string, QStandardItem*> pathItemMap;

    MSelectionList selectedObjects;
    MGlobal::getActiveSelectionList(selectedObjects);

    // iterate dag
    while(!dagIter.isDone())
    {
        QStandardItem *parentItem = rootNode;

        MDagPath dagPath;
        dagIter.getPath(dagPath);
        MString path = dagIter.fullPathName();
        
        // don't include shapes
        if(dagPath.hasFn(MFn::Type::kShape) && dagPath.childCount()==0)
        {
            std::cout << "is shape, not including: " << path << "\n";
            dagIter.next();
            continue;
        }



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
        
        // set selection
        {
            MDagPath checkPath = dagPath;
            Qt::CheckState state = Qt::CheckState::Unchecked;
            while (true)
            {
                if(selectedObjects.hasItem(checkPath))
                {
                    state = Qt::CheckState::Checked;
                    break;
                }

                if(!checkPath.length())
                {
                    break;
                }

                // move up a level
                MStatus status = checkPath.pop();
                if(status != MStatus::kSuccess)
                {
                    break;
                }
            }
            nodeItem->setCheckState(state); 
        }

        // add prim to model
        rowItems.insert(static_cast<int>(SelectionCol::MayaPrimName), nodeItem);
        std::string type = MayaUSDExport::PrimWriter::derivePrimType(dagPath);

        //  add type to model
        QStandardItem* typeItem = new QStandardItem(type.c_str());
        rowItems.insert(static_cast<int>(SelectionCol::UsdPrimType), typeItem);
        typeItem->setEditable(false);

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
