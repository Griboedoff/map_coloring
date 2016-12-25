import sys

from editor.editor_widget import EditorWidget

try:
    from PyQt5 import QtGui, QtWidgets, QtCore
except Exception as e:
    print('PyQt5 not found: "{}"'.format(e), file=sys.stderr)
    sys.exit(1)


class EditorWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.editor_widget = EditorWidget()
        self.init_ui()

    def init_ui(self):
        bar = QtWidgets.QToolBar()
        bar.addAction("Add county", self.editor_widget.add_country)
        bar.addAction("Add country piece", self.editor_widget.add_piece)
        bar.addAction("Finish piece", self.editor_widget.finish_piece)
        bar.addAction("Save", self.save)
        self.addToolBar(QtCore.Qt.TopToolBarArea, bar)
        self.setCentralWidget(self.editor_widget)
        self.setGeometry(0, 0, 700, 700)
        self.show()

    def save(self):
        self.editor_widget.save()
        self.close()

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    viz = EditorWindow()

    sys.exit(app.exec_())
