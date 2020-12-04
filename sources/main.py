from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtWidgets import QApplication, QWidget, QFileDialog, QPushButton, QMainWindow, \
    QTableWidgetItem
import sys
import os
import sqlite3
import datetime as dt

EXTENSION = '.sqlite3'

print()

class TicketsSystemMainWindow(QMainWindow):
    def __init__(self, database_file=None):
        super(TicketsSystemMainWindow, self).__init__()
        self.database_file = database_file
        self.setupUi(self)

        self.mode_box.currentIndexChanged.connect(self.mode_change)

        self.modes = ['Cinemas', 'Cinemahalls',
                      'Sessions', 'Tickets']

        if self.database_file is not None:
            self.open_system()

    def mode_change(self):
        if self.database_file:
            current_mode = self.mode_box.currentText()

            queries = {'Кинотетары': ('name, address', ['Название', 'Адресс']),
                       'Кинозалы': ('name, number', ['Название', 'Номер кинозала']),
                       'Сеансы': ('name, number', ['Название', 'Номер кинозала']),
                       'Касса': ('name, number', ['Название', 'Номер кинозала'])}
            query = f'SELECT {queries[current_mode[0]]} FROM {current_mode}'
            result = list(self.cursor.execute(query))
            if result:
                self.table.setRowCount(0)
                self.table.setColumnCount(len(result[0]))
                # self.table.setHorizontalHeaderLabels(queries[current_mode[1]])
                for i, row in enumerate(result):
                    self.table.setRowCount(self.table.rowCount() + 1)
                    for j, col in enumerate(row):
                        self.table.setItem(i, j, QTableWidgetItem(col))

    def open_system(self):
        self.database_file = QFileDialog.getOpenFileName(
            self, 'Выбрать файл билетной системы', '',
            f'Файл билетной системы (*{EXTENSION});;Все файлы (*)')[0]
        try:
            self.database_connection = sqlite3.connect(self.database_file)
            self.cursor = self.database_connection.cursor()
            title = self.cursor.execute("""SELECT value FROM information
                                                    WHERE name = 'window_title'""").fetchone()

            if title is not None:
                title = title[0]
            else:
                title = 'Билетная система'
            self.setWindowTitle(str(title))

            self.mode_change()

        except Exception as e:
            self.information_label.setText(f'Файл системы {self.database_file} поврежден')
            print(e)

    def create_system(self):
        self.new_window = CreateTicketsSystemWindow()
        self.new_window.show()
        self.close()

    def closeEvent(self, a0: QtGui.QCloseEvent):
        try:
            self.database_connection.close()
        except Exception:
            pass
        self.close()

    def close_program(self):
        self.close()

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(740, 500)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")

        self.add_btn = QPushButton('Добавить...')
        self.add_btn.setObjectName("add_btn")
        self.horizontalLayout.addWidget(self.add_btn)

        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding,
                                           QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.mode_box = QtWidgets.QComboBox(self.centralwidget)
        self.mode_box.setObjectName("mode_box")
        self.mode_box.addItem("")
        self.mode_box.addItem("")
        self.mode_box.addItem("")
        self.mode_box.addItem("")
        self.horizontalLayout.addWidget(self.mode_box)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.table = QtWidgets.QTableWidget(self.centralwidget)
        self.table.setObjectName("listWidget")
        self.verticalLayout.addWidget(self.table)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.information_label = QtWidgets.QLabel(self.centralwidget)
        self.information_label.setObjectName("information_label")
        self.horizontalLayout_2.addWidget(self.information_label)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding,
                                            QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem1)
        self.time_label = QtWidgets.QLabel(self.centralwidget)
        self.time_label.setObjectName("time_label")
        self.horizontalLayout_2.addWidget(self.time_label)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 739, 21))
        self.menubar.setObjectName("menubar")
        self.menu = QtWidgets.QMenu(self.menubar)
        self.menu.setObjectName("menu")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.rename_system = QtWidgets.QAction(MainWindow)
        self.rename_system.setObjectName("rename_system")

        self.exit_btn = QtWidgets.QAction(MainWindow)
        self.exit_btn.setObjectName("exit_btn")
        self.exit_btn.triggered.connect(self.close_program)

        self.action = QtWidgets.QAction(MainWindow)
        self.action.setObjectName("action")

        self.save_as_btn = QtWidgets.QAction(MainWindow)
        self.save_as_btn.setObjectName("save_as_btn")

        self.open_system_btn = QtWidgets.QAction(MainWindow)
        self.open_system_btn.setObjectName("open_system_btn")
        self.open_system_btn.triggered.connect(self.open_system)

        self.create_new_system_btn = QtWidgets.QAction(MainWindow)
        self.create_new_system_btn.setObjectName("create_new_system_btn")
        self.create_new_system_btn.triggered.connect(self.create_system)

        self.menu.addAction(self.open_system_btn)
        self.menu.addAction(self.save_as_btn)
        self.menu.addSeparator()
        self.menu.addAction(self.create_new_system_btn)
        self.menu.addSeparator()
        self.menu.addAction(self.rename_system)
        self.menu.addAction(self.action)
        self.menu.addSeparator()
        self.menu.addAction(self.exit_btn)
        self.menubar.addAction(self.menu.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Билетная система"))

        self.mode_box.setItemText(0, _translate("MainWindow", "Кинотеатры"))
        self.mode_box.setItemText(1, _translate("MainWindow", "Кинозалы"))
        self.mode_box.setItemText(2, _translate("MainWindow", "Сеансы"))
        self.mode_box.setItemText(3, _translate("MainWindow", "Касса"))
        self.information_label.setText(_translate("MainWindow", "TextLabel"))
        self.time_label.setText(_translate("MainWindow", "TextLabel"))
        self.menu.setTitle(_translate("MainWindow", "Файл"))
        self.rename_system.setText(_translate("MainWindow", "Переименовать систему"))
        self.exit_btn.setText(_translate("MainWindow", "Выйти из системы"))
        self.action.setText(_translate("MainWindow", "Удалить систему"))
        self.save_as_btn.setText(_translate("MainWindow", "Сохранить как..."))
        self.open_system_btn.setText(_translate("MainWindow", "Открыть систему"))
        self.create_new_system_btn.setText(_translate("MainWindow", "Создать систему"))


class CreateTicketsSystemWindow(QWidget):
    def __init__(self):
        super(CreateTicketsSystemWindow, self).__init__()
        self.setupUi(self)
        self.btn.clicked.connect(self.button_clicked)

    def button_clicked(self):
        system_name = self.title_input.text().strip()
        check_result = self._check_system_name(system_name)
        if check_result != '':
            self.error_label.setText(check_result)
        else:
            files = list(os.walk(os.getcwd()))[0][2]
            if system_name + EXTENSION in files:
                mb = QtWidgets.QMessageBox
                answer = mb.question(self, '',
                                     f'Файл {system_name + EXTENSION} уже есть. Заменить?',
                                     mb.No | mb.Yes, mb.No)
                if answer == mb.No:
                    return

            self.create_new_system_file(system_name)

    def _check_system_name(self, name: str) -> str:
        if len(name) == 0:
            return 'Название не может быть пустым'
        if set('/\\?:*"\'<>|.') & set(name):
            return 'Название системы не может содержать /\\?:*"\'<>.|'
        return ''

    def create_new_system_file(self, filename: str) -> None:
        filename += EXTENSION
        with open(filename, 'w', encoding='utf-8'):
            pass
        try:
            self.connection = sqlite3.connect(filename)
            self.cursor = self.connection.cursor()
            self.cursor.executescript(f"""CREATE TABLE cinemas (
    id      INTEGER      PRIMARY KEY AUTOINCREMENT
                         UNIQUE
                         NOT NULL,
    name    STRING (255) UNIQUE
                         NOT NULL,
    address STRING (255) 
);
CREATE TABLE information (
    name  STRING (255) PRIMARY KEY
                       UNIQUE
                       NOT NULL,
    value TEXT (4096)  NOT NULL
);
CREATE TABLE sessions (
    id             INTEGER      PRIMARY KEY AUTOINCREMENT
                                UNIQUE
                                NOT NULL,
    name           STRING (255) NOT NULL,
    date           DATE         NOT NULL,
    time           TIME         NOT NULL,
    duration       INTEGER      NOT NULL,
    cinema_hall_id INTEGER      REFERENCES cinemahalls (id) 
                                NOT NULL
);
CREATE TABLE plans (
    id   INTEGER      PRIMARY KEY AUTOINCREMENT
                      UNIQUE
                      NOT NULL,
    name STRING (255) UNIQUE
                      NOT NULL,
    data TEXT (4096)  NOT NULL
);
CREATE TABLE cinemahalls (
    id        INTEGER      PRIMARY KEY AUTOINCREMENT
                           UNIQUE
                           NOT NULL,
    name      STRING (255) NOT NULL,
    plan_id   INTEGER      REFERENCES plans (id) 
                           NOT NULL,
    cinema_id INTEGER      REFERENCES cinemas (id) 
                           NOT NULL
);
CREATE TABLE tickets (
    id        INTEGER      PRIMARY KEY AUTOINCREMENT
                           UNIQUE
                           NOT NULL,
    date      DATE         NOT NULL,
    time      TIME         NOT NULL,
    cost      INTEGER      NOT NULL,
    session_id   INTEGER   REFERENCES sessions (id) 
                           NOT NULL,
    cinema_id INTEGER      REFERENCES cinemas (id) 
                           NOT NULL,
    sit_id      INTEGER    NOT NULL
);
INSERT INTO information(name, value) VALUES ('window_title', '{filename[:filename.rfind('.')]}');""")
            self.connection.close()
            self.new_window = TicketsSystemMainWindow(database_file=filename)
            self.new_window.show()

            self.close()
        except Exception as e:
            print(e)

    def closeEvent(self, a0: QtGui.QCloseEvent) -> None:
        self.new_window = TicketsSystemMainWindow()
        self.new_window.show()

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


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = TicketsSystemMainWindow()
    ex.show()
    sys.exit(app.exec())
