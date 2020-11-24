from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtWidgets import QApplication, QWidget, QFileDialog, QPushButton, QMainWindow
import sys
import os
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
            if system_name + '.tsf' in files:
                mb = QtWidgets.QMessageBox
                answer = mb.question(self, '',
                                     f'Файл {system_name + ".tsf"} уже есть. Заменить?',
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
        filename += '.tsf'
        with open(filename, 'w', encoding='utf-8') as file:
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
INSERT INTO information(name, value) VALUES ('window_title', '{filename[:-4]}');""")
            self.connection.close()
            self.new_window = TicketsSystemMainWindow(database_file=filename)
            self.new_window.show()

            self.close()
        except Exception as e:
            print(e)

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


class TicketsSystemMainWindow(QMainWindow):
    def __init__(self, database_file=None):
        super(TicketsSystemMainWindow, self).__init__()
        self.database_file = database_file
        self.setupUi(self)
        if self.database_file is not None:
            self.open_system()

    def closeEvent(self, a0: QtGui.QCloseEvent) -> None:
        try:
            self.database_connection.close()
        except Exception:
            pass
        self.close()

    def open_system(self):
        if self.database_file is None:
            self.database_file = QFileDialog.getOpenFileName(
                self, 'Выбрать файл билетной системы', '',
                'Файл билетной системы (*.tsf);;Все файлы (*)')[0]
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
        except Exception as e:
            self.information_label.setText(f'Файл системы {self.database_file} поврежден')
            print(e)

    def create_system(self):
        self.new_window = CreateTicketsSystemWindow()
        self.new_window.show()
        self.close()

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(739, 503)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.page_title = QtWidgets.QLabel(self.centralwidget)
        self.page_title.setObjectName("page_title")
        self.horizontalLayout.addWidget(self.page_title)
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
        self.listWidget = QtWidgets.QListWidget(self.centralwidget)
        self.listWidget.setObjectName("listWidget")
        self.verticalLayout.addWidget(self.listWidget)
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
        self.page_title.setText(_translate("MainWindow", "TextLabel"))
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


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = TicketsSystemMainWindow()
    ex.show()
    sys.exit(app.exec())
