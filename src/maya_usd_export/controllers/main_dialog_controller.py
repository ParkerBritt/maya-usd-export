
class MainDialogController():
    def __init__(self, _view):
        self.view = _view

        self.view.cancel_button.clicked.connect(self.view.close)
        # self.view.export_button.clicked.connect(self.)

