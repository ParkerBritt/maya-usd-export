import maya.api.OpenMaya as om

from maya_usd_export.utils import pyside_importer
_, qtc, qtw, shiboken = pyside_importer.import_all()
from PySide import QtGui

class SelectionTree(qtw.QTreeView):
    def __init__(self):
        super().__init__()
        self._tree_view = self
        self.model = QtGui.QStandardItemModel(self)
        self._root_node = self.model.invisibleRootItem()

        self.populate_model()
        self._tree_view.setModel(self.model)
        self._tree_view.expandAll()


    def format_model_item(self, item: QtGui.QStandardItem):
        item.setCheckable(True)
        item.setEditable(False)

    def populate_model(self):
        dag_iterator = om.MItDag()
        traversed_items = dict()

        while not dag_iterator.isDone():
            name = dag_iterator.getPath()
            path = dag_iterator.fullPathName()

            split_path = path[1:].split("|")
            print(dag_iterator.fullPathName())
            print(split_path)

            if(len(split_path) == 1):
                model_item = QtGui.QStandardItem(str(name))
                self.format_model_item(model_item)
                self._root_node.appendRow(model_item)
                # reset traversed_items to reduce memory usage
                traversed_items = dict()
            else:
                parent_path = "|"+"|".join(split_path[:-1])

                model_item = QtGui.QStandardItem(str(name))
                self.format_model_item(model_item)
                traversed_items[parent_path].appendRow(model_item)
                print("parent", parent_path)
            traversed_items[path] = model_item



            dag_iterator.next()


class SelectionParameters(qtw.QWidget):
    def __init__(self):
        super().__init__()
        self._main_layout = qtw.QFormLayout()
        self._main_layout.setLabelAlignment(qtc.Qt.AlignLeft | qtc.Qt.AlignVCenter)
        self.setLayout(self._main_layout)

        self._main_layout.addRow("Prim Type", qtw.QComboBox())
        self._main_layout.addRow("Invert Winding Order", qtw.QCheckBox())


class SelectionOptions(qtw.QWidget):
    def __init__(self):
        super().__init__()
        self._main_layout = qtw.QVBoxLayout()
        self.setLayout(self._main_layout)

        self._splitter = qtw.QSplitter()
        self._main_layout.addWidget(self._splitter)

        self._seleciton_tree = SelectionTree()
        self._splitter.addWidget(self._seleciton_tree)

        self._seleciton_parameters = SelectionParameters()
        self._splitter.addWidget(self._seleciton_parameters)
