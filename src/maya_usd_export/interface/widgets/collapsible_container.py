from maya_usd_export.utils import pyside_importer
_, qtc, qtw, shiboken = pyside_importer.import_all()

class CollapsibleContainerHeader(qtw.QPushButton):
    def __init__(self, title):
        super().__init__(title)
        main_layout = qtw.QVBoxLayout()
        self.setLayout(main_layout)

class CollapsibleContainer(qtw.QWidget):
    def __init__(self, title):
        super().__init__()
        self._main_layout = qtw.QVBoxLayout()
        self._main_layout.setAlignment(qtc.Qt.AlignTop)
        self.setLayout(self._main_layout)

        self._head_bttn = CollapsibleContainerHeader(title)
        self._head_bttn.clicked.connect(self.header_clicked_slot)
        self._head_bttn.setIcon(self.style().standardIcon(qtw.QStyle.SP_ArrowDown))

        self._main_layout.addWidget(self._head_bttn)

        self._contents_w = qtw.QWidget()
        self._main_layout.addWidget(self._contents_w)
        self._contents_l = qtw.QVBoxLayout(self._contents_w)
        self._contents_l.setContentsMargins(0,0,0,0)

    def header_clicked_slot(self):
        self._contents_w.setVisible(not self._contents_w.isVisible())
        if(self._contents_w.isVisible()):
            self._head_bttn.setIcon(self.style().standardIcon(qtw.QStyle.SP_ArrowDown))
        else:
            self._head_bttn.setIcon(self.style().standardIcon(qtw.QStyle.SP_ArrowRight))

    def addWidget(self, _widget):
       self._contents_l.addWidget(_widget) 

    def addLayout(self, _layout):
       self._contents_l.addLayout(_layout) 
        

