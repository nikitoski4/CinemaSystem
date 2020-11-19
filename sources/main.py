from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtWidgets import QApplication, QWidget, QFileDialog, QInputDialog, QDialogButtonBox
import sys
import sqlite3


class CinemaTicketsSystemException(Exception):
    pass


class CinemaTicketsSystemFileBroken(CinemaTicketsSystemException):
    pass


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
        self.new_window = CreateTicketsSystemWindow()
        self.new_window.show()
        self.close()

    def open_system_clicked(self):
        database_file = QFileDialog.getOpenFileName(
            self, 'Выбрать файл билетной системы', '',
            'Файл билетной системы (*.tsf);;Все файлы (*)')[0]
        if database_file:
            try:
                self.new_window = TicketsSystemTabsWindow(database_file)
                self.new_window.show()
                self.close()
            except CinemaTicketsSystemFileBroken:
                print('Файл системы поврежден или неопознан')
                self.show()

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
        self.open_system.setText(_translate("Form", "Открыть файл системы"))
        self.create_system.setText(_translate("Form", "Создать новую систему"))
        self.exit.setText(_translate("Form", "Выход"))


class TicketsSystemTabsWindow(QWidget):
    def __init__(self, database_file):
        super(TicketsSystemTabsWindow, self).__init__()

        self.database_file = database_file
        try:
            self.database_connection = sqlite3.connect(self.database_file)
            self.cursor = self.database_connection.cursor()
            title = self.cursor.execute("""SELECT value FROM information
                                            WHERE name = 'window_title'""").fetchone()[0]
        except Exception:
            raise CinemaTicketsSystemFileBroken

        self.setupUi(self)
        self.setWindowTitle(str(title))

    def closeEvent(self, a0: QtGui.QCloseEvent) -> None:
        self.database_connection.close()
        self.new_window = TicketsSystemStartWindow()
        self.new_window.show()
        self.close()

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


class CreateTicketsSystemWindow(QWidget):
    def __init__(self):
        super(CreateTicketsSystemWindow, self).__init__()
        self.setupUi(self)
        self.btn.clicked.connect(self.button_clicked)

    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(375, 150)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred,
                                           QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Form.sizePolicy().hasHeightForWidth())
        Form.setSizePolicy(sizePolicy)
        Form.setMaximumSize(QtCore.QSize(375, 150))
        self.verticalLayout = QtWidgets.QVBoxLayout(Form)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label = QtWidgets.QLabel(Form)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred,
                                           QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy)
        self.label.setObjectName("label")
        self.horizontalLayout.addWidget(self.label)
        self.error_label = QtWidgets.QLabel(Form)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred,
                                           QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.error_label.sizePolicy().hasHeightForWidth())
        self.error_label.setSizePolicy(sizePolicy)
        self.error_label.setText("")
        self.error_label.setObjectName("error_label")
        self.horizontalLayout.addWidget(self.error_label)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.title_input = QtWidgets.QLineEdit(Form)
        self.title_input.setMaxLength(255)
        self.title_input.setObjectName("title_input")
        self.verticalLayout.addWidget(self.title_input)
        self.btn = QtWidgets.QPushButton(Form)
        self.btn.setObjectName("btn")
        self.verticalLayout.addWidget(self.btn)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Новая билетная система"))
        self.label.setText(_translate("Form", "Введите название новой системы:"))
        self.btn.setText(_translate("Form", "Далее"))

    def button_clicked(self):
        system_name = self.title_input.text().strip()
        check_result = self._check_system_name(system_name)
        if check_result != '':
            self.error_label.setText(check_result)
        else:
            self._create_new_system_file(system_name)

    def _check_system_name(self, name: str) -> str:
        if len(name) == 0:
            return 'Название не может быть пустым'
        if set('/\\?:*"\'<>|.') & set(name):
            return 'Название системы не может содержать /\\?:*"\'<>.|'
        return ''

    def _create_new_system_file(self, filename: str) -> None:
        pass


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = TicketsSystemStartWindow()
    ex.show()
    sys.exit(app.exec())
