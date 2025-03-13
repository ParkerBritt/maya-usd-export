from maya_usd_export.utils import pyside_importer
_, qtc, qtw, shiboken = pyside_importer.import_all()
from PySide import QtGui

class SelectionTree(qtw.QTreeView):
    def __init__(self):
        super().__init__()
        self._tree_view = self
        self.model = QtGui.QStandardItemModel(self)
        self._root_node = self.model.invisibleRootItem()

        self._tree_view.setModel(self.model)
        self._tree_view.expandAll()

    def populate_model(self):
        pass

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
