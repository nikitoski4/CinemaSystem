from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtWidgets import QApplication, QWidget, QFileDialog
import sys
import sqlite3


class TicketsSystemStartWindow(QWidget):
    def __init__(self):
        super(TicketsSystemStartWindow, self).__init__()
        self.setupUi(self)
        self.exit.clicked.connect(self.exit_clicked)
        self.open_system.clicked.connect(self.open_system_clicked)
        self.create_system.clicked.connect(self.create_system_clicked)

    def exit_clicked(self):
        self.close()

    def create_system_clicked(self):
        pass

    def open_system_clicked(self):
        database_file = QFileDialog.getOpenFileName(
            self, 'Выбрать файл билетной системы', '',
            'Файл билетной системы (*.tsf);;Все файлы (*)')[0]
        if database_file:
            self.hide()
            self.tabwindow = TicketsSystemTabsWindow()
            self.tabwindow.show()

    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(260, 200)
        Form.setMinimumSize(QtCore.QSize(260, 120))
        Form.setMaximumSize(QtCore.QSize(400, 200))
        self.verticalLayout = QtWidgets.QVBoxLayout(Form)
        self.verticalLayout.setObjectName("verticalLayout")
        self.open_system = QtWidgets.QPushButton(Form)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum,
                                           QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.open_system.sizePolicy().hasHeightForWidth())
        self.open_system.setSizePolicy(sizePolicy)
        self.open_system.setMinimumSize(QtCore.QSize(0, 0))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.open_system.setFont(font)
        self.open_system.setObjectName("open_system")
        self.verticalLayout.addWidget(self.open_system)
        self.create_system = QtWidgets.QPushButton(Form)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum,
                                           QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.create_system.sizePolicy().hasHeightForWidth())
        self.create_system.setSizePolicy(sizePolicy)
        self.create_system.setMinimumSize(QtCore.QSize(0, 0))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.create_system.setFont(font)
        self.create_system.setObjectName("create_system")
        self.verticalLayout.addWidget(self.create_system)
        self.exit = QtWidgets.QPushButton(Form)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum,
                                           QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.exit.sizePolicy().hasHeightForWidth())
        self.exit.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(14)
        self.exit.setFont(font)
        self.exit.setFocusPolicy(QtCore.Qt.ClickFocus)
        self.exit.setObjectName("exit")
        self.verticalLayout.addWidget(self.exit)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Билетная система"))
        self.open_system.setText(_translate("Form", "Открыть файл системы..."))
        self.create_system.setText(_translate("Form", "Создать новую систему..."))
        self.exit.setText(_translate("Form", "Выход"))


class TicketsSystemTabsWindow(QWidget):
    def __init__(self):
        super(TicketsSystemTabsWindow, self).__init__()
        self.setupUi(self)

    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(389, 238)
        self.verticalLayout = QtWidgets.QVBoxLayout(Form)
        self.verticalLayout.setObjectName("verticalLayout")
        self.tabWidget = QtWidgets.QTabWidget(Form)
        self.tabWidget.setObjectName("tabWidget")
        self.tab = QtWidgets.QWidget()
        self.tab.setObjectName("tab")
        self.tabWidget.addTab(self.tab, "")
        self.tab_2 = QtWidgets.QWidget()
        self.tab_2.setObjectName("tab_2")
        self.tabWidget.addTab(self.tab_2, "")
        self.verticalLayout.addWidget(self.tabWidget)

        self.retranslateUi(Form)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Билетная система"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), _translate("Form", "Tab 1"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), _translate("Form", "Tab 2"))


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = TicketsSystemStartWindow()
    ex.show()
    sys.exit(app.exec())
