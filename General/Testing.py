import sys
from PyQt5 import QtWidgets


class TempWidget(QtWidgets.QGroupBox):

    def __init__(self, **kwargs):

        super().__init__()

        self.setTitle(str(kwargs.get("title")))

        self.layout = QtWidgets.QHBoxLayout()
        self.text_box = QtWidgets.QTextEdit()

        self.layout.addWidget(self.text_box)
        self.setLayout(self.layout)


class WidgetScroll:

    def __init__(self, **kwargs):

        self.layout = QtWidgets.QVBoxLayout()
        self.parent_widget = QtWidgets.QWidget()
        self.parent_widget.setLayout(self.layout)

        self.scroll = QtWidgets.QScrollArea()
        self.scroll.setWidgetResizable(True)  # Set to make the inner widget resize with scroll area
        self.scroll.setWidget(self.parent_widget)

        for i in range(8):
            self.layout.addWidget(TempWidget(title=i))


class MyDialog(QtWidgets.QDialog):

    def __init__(self):

        super().__init__()

        # widget_scroll = WidgetScroll()
        #
        # layout = QtWidgets.QHBoxLayout()
        # layout.addWidget(widget_scroll.scroll)
        # self.setLayout(layout)

        self.Stack = QtWidgets.QStackedWidget(self)
        self.Stack.addWidget(self.stack1UI())

        hbox_layout = QtWidgets.QHBoxLayout(self)
        self.setLayout(hbox_layout)

    def stack1UI(self):
        layout = QtWidgets.QFormLayout()
        layout.addRow("Name", QtWidgets.QLineEdit())
        layout.addRow("Address", QtWidgets.QLineEdit())
        # self.setTabText(0,"Contact Details")


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    dialog = MyDialog()
    dialog.show()
    sys.exit(app.exec_())
