import os
import sys
import sqlite3
import datetime
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMainWindow, QApplication, QTableWidgetItem, \
    QFileDialog, QInputDialog, QWidget, QLineEdit

TICKETS_SYSTEM_FILE_EXTENSION = '.sqlite3'
CINEMAS_TABLE_HEADERS = ['Название', 'Адрес', 'Кинозалы']
SESSIONS_TABLE_HEADERS = ['Дата', 'Время', 'Название', 'Кинотеатр', 'Кинозал', 'Продано',
                          'Осталось', 'Схема зала', 'Действие', 'Статус']
CINEMAHALLS_TABLE_HEADERS = ['Название / №', 'Кинотеатр', 'Вместимость', 'Планировка']

SCRIPT_FOR_CREATE_TICKETS_SYSTEM_DATABASE = f"""CREATE TABLE cinemas (
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
);"""


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1147, 654)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName("verticalLayout")

        self.tabWidget = QtWidgets.QTabWidget(self.centralwidget)
        self.tabWidget.setWhatsThis("")
        self.tabWidget.setAccessibleName("")
        self.tabWidget.setAccessibleDescription("")
        self.tabWidget.setTabPosition(QtWidgets.QTabWidget.West)
        self.tabWidget.setTabShape(QtWidgets.QTabWidget.Rounded)
        self.tabWidget.setMovable(False)
        self.tabWidget.setTabBarAutoHide(False)
        self.tabWidget.setObjectName("tabWidget")

        self.tab_tickets = QtWidgets.QWidget()
        self.tab_tickets.setObjectName("tab_tickets")

        self.verticalLayout_5 = QtWidgets.QVBoxLayout(self.tab_tickets)
        self.verticalLayout_5.setObjectName("verticalLayout_5")

        self.horizontalLayout_5 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")

        self.label = QtWidgets.QLabel(self.tab_tickets)
        self.label.setObjectName("label")

        self.horizontalLayout_5.addWidget(self.label)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding,
                                           QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_5.addItem(spacerItem)

        self.label_4 = QtWidgets.QLabel(self.tab_tickets)
        self.label_4.setObjectName("label_4")

        self.horizontalLayout_5.addWidget(self.label_4)

        self.tickets_date_start = QtWidgets.QDateEdit(self.tab_tickets)
        self.tickets_date_start.setAutoFillBackground(False)
        self.tickets_date_start.setWrapping(False)
        self.tickets_date_start.setReadOnly(False)
        self.tickets_date_start.setSpecialValueText("")
        self.tickets_date_start.setAccelerated(False)
        self.tickets_date_start.setProperty("showGroupSeparator", False)
        self.tickets_date_start.setCalendarPopup(True)
        self.tickets_date_start.setObjectName("tickets_date_start")

        self.horizontalLayout_5.addWidget(self.tickets_date_start)

        self.tickets_date_end = QtWidgets.QDateEdit(self.tab_tickets)
        self.tickets_date_end.setAutoFillBackground(False)
        self.tickets_date_end.setWrapping(False)
        self.tickets_date_end.setReadOnly(False)
        self.tickets_date_end.setSpecialValueText("")
        self.tickets_date_end.setAccelerated(False)
        self.tickets_date_end.setProperty("showGroupSeparator", False)
        self.tickets_date_end.setCalendarPopup(True)
        self.tickets_date_end.setObjectName("tickets_date_end")

        self.horizontalLayout_5.addWidget(self.tickets_date_end)

        self.line_2 = QtWidgets.QFrame(self.tab_tickets)
        self.line_2.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_2.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_2.setObjectName("line_2")

        self.horizontalLayout_5.addWidget(self.line_2)

        self.tickets_tab_cinema_selector = QtWidgets.QComboBox(self.tab_tickets)
        self.tickets_tab_cinema_selector.setToolTip("")
        self.tickets_tab_cinema_selector.setToolTipDuration(-1)
        self.tickets_tab_cinema_selector.setWhatsThis("")
        self.tickets_tab_cinema_selector.setAccessibleName("")
        self.tickets_tab_cinema_selector.setAccessibleDescription("")
        self.tickets_tab_cinema_selector.setSizeAdjustPolicy(QtWidgets.QComboBox.AdjustToContents)
        self.tickets_tab_cinema_selector.setObjectName("tickets_tab_cinema_selector")
        self.tickets_tab_cinema_selector.addItem("")
        self.tickets_tab_cinema_selector.addItem("")
        self.tickets_tab_cinema_selector.addItem("")
        self.tickets_tab_cinema_selector.addItem("")

        self.horizontalLayout_5.addWidget(self.tickets_tab_cinema_selector)

        self.tickets_enter_search_phrase = QtWidgets.QLineEdit(self.tab_tickets)
        self.tickets_enter_search_phrase.setAlignment(QtCore.Qt.AlignCenter)
        self.tickets_enter_search_phrase.setObjectName("tickets_enter_search_phrase")

        self.horizontalLayout_5.addWidget(self.tickets_enter_search_phrase)

        self.tickets_btn_search = QtWidgets.QPushButton(self.tab_tickets)
        self.tickets_btn_search.setObjectName("tickets_btn_search")

        self.horizontalLayout_5.addWidget(self.tickets_btn_search)

        self.verticalLayout_5.addLayout(self.horizontalLayout_5)

        self.tickets_table = QtWidgets.QTableWidget(self.tab_tickets)
        self.tickets_table.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.tickets_table.setAlternatingRowColors(True)
        self.tickets_table.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        self.tickets_table.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectItems)
        self.tickets_table.setShowGrid(True)
        self.tickets_table.setGridStyle(QtCore.Qt.SolidLine)
        self.tickets_table.setCornerButtonEnabled(True)
        self.tickets_table.setObjectName("tickets_table")
        self.tickets_table.setColumnCount(7)
        self.tickets_table.setRowCount(19)

        item = QtWidgets.QTableWidgetItem()
        self.tickets_table.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tickets_table.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.tickets_table.setHorizontalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        self.tickets_table.setHorizontalHeaderItem(3, item)
        item = QtWidgets.QTableWidgetItem()
        self.tickets_table.setHorizontalHeaderItem(4, item)
        item = QtWidgets.QTableWidgetItem()
        self.tickets_table.setHorizontalHeaderItem(5, item)
        item = QtWidgets.QTableWidgetItem()
        self.tickets_table.setHorizontalHeaderItem(6, item)

        self.tickets_table.horizontalHeader().setVisible(False)
        self.tickets_table.horizontalHeader().setCascadingSectionResizes(False)
        self.tickets_table.horizontalHeader().setHighlightSections(True)
        self.tickets_table.horizontalHeader().setSortIndicatorShown(False)
        self.tickets_table.horizontalHeader().setStretchLastSection(True)
        self.tickets_table.verticalHeader().setVisible(False)

        self.verticalLayout_5.addWidget(self.tickets_table)

        self.tabWidget.addTab(self.tab_tickets, "")
        self.tab_cinemas = QtWidgets.QWidget()
        self.tab_cinemas.setObjectName("tab_cinemas")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.tab_cinemas)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.cinemas_btn_add_cinema = QtWidgets.QPushButton(self.tab_cinemas)
        self.cinemas_btn_add_cinema.setObjectName("cinemas_btn_add_cinema")
        self.horizontalLayout_3.addWidget(self.cinemas_btn_add_cinema)
        self.cinemas_btn_edit_cinema = QtWidgets.QPushButton(self.tab_cinemas)
        self.cinemas_btn_edit_cinema.setObjectName("cinemas_btn_edit_cinema")
        self.horizontalLayout_3.addWidget(self.cinemas_btn_edit_cinema)
        self.cinemas_btn_delete_cinema = QtWidgets.QPushButton(self.tab_cinemas)
        self.cinemas_btn_delete_cinema.setObjectName("cinemas_btn_delete_cinema")
        self.horizontalLayout_3.addWidget(self.cinemas_btn_delete_cinema)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding,
                                            QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem1)
        self.cinemas_enter_search_phrase = QtWidgets.QLineEdit(self.tab_cinemas)
        self.cinemas_enter_search_phrase.setInputMask("")
        self.cinemas_enter_search_phrase.setText("")
        self.cinemas_enter_search_phrase.setAlignment(QtCore.Qt.AlignCenter)
        self.cinemas_enter_search_phrase.setCursorMoveStyle(QtCore.Qt.LogicalMoveStyle)
        self.cinemas_enter_search_phrase.setObjectName("cinemas_enter_search_phrase")
        self.horizontalLayout_3.addWidget(self.cinemas_enter_search_phrase)
        self.cinemas_btn_search_cinema = QtWidgets.QPushButton(self.tab_cinemas)
        self.cinemas_btn_search_cinema.setObjectName("cinemas_btn_search_cinema")
        self.horizontalLayout_3.addWidget(self.cinemas_btn_search_cinema)
        self.verticalLayout_3.addLayout(self.horizontalLayout_3)
        self.cinema_table = QtWidgets.QTableWidget(self.tab_cinemas)
        self.cinema_table.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.cinema_table.setAlternatingRowColors(True)
        self.cinema_table.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        self.cinema_table.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.cinema_table.setShowGrid(True)
        self.cinema_table.setGridStyle(QtCore.Qt.SolidLine)
        self.cinema_table.setCornerButtonEnabled(True)
        self.cinema_table.setObjectName("cinema_table")
        self.cinema_table.setColumnCount(3)
        self.cinema_table.setRowCount(3)
        item = QtWidgets.QTableWidgetItem()
        self.cinema_table.setVerticalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.cinema_table.setVerticalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.cinema_table.setVerticalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        self.cinema_table.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.cinema_table.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.cinema_table.setHorizontalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        self.cinema_table.setItem(0, 0, item)
        item = QtWidgets.QTableWidgetItem()
        self.cinema_table.setItem(0, 1, item)
        item = QtWidgets.QTableWidgetItem()
        self.cinema_table.setItem(0, 2, item)
        item = QtWidgets.QTableWidgetItem()
        self.cinema_table.setItem(1, 0, item)
        item = QtWidgets.QTableWidgetItem()
        self.cinema_table.setItem(1, 1, item)
        item = QtWidgets.QTableWidgetItem()
        self.cinema_table.setItem(2, 0, item)
        item = QtWidgets.QTableWidgetItem()
        self.cinema_table.setItem(2, 1, item)
        self.cinema_table.horizontalHeader().setCascadingSectionResizes(False)
        self.cinema_table.horizontalHeader().setHighlightSections(True)
        self.cinema_table.horizontalHeader().setStretchLastSection(True)
        self.cinema_table.verticalHeader().setVisible(False)
        self.verticalLayout_3.addWidget(self.cinema_table)
        self.tabWidget.addTab(self.tab_cinemas, "")
        self.tab_sessions = QtWidgets.QWidget()
        self.tab_sessions.setObjectName("tab_sessions")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.tab_sessions)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.sessions_btn_add_session = QtWidgets.QPushButton(self.tab_sessions)
        self.sessions_btn_add_session.setObjectName("sessions_btn_add_session")
        self.horizontalLayout_2.addWidget(self.sessions_btn_add_session)
        self.sessions_btn_edit_session = QtWidgets.QPushButton(self.tab_sessions)
        self.sessions_btn_edit_session.setObjectName("sessions_btn_edit_session")
        self.horizontalLayout_2.addWidget(self.sessions_btn_edit_session)
        self.sessions_btn_delete_session = QtWidgets.QPushButton(self.tab_sessions)
        self.sessions_btn_delete_session.setObjectName("sessions_btn_delete_session")
        self.horizontalLayout_2.addWidget(self.sessions_btn_delete_session)
        spacerItem2 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding,
                                            QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem2)
        self.label_3 = QtWidgets.QLabel(self.tab_sessions)
        self.label_3.setObjectName("label_3")
        self.horizontalLayout_2.addWidget(self.label_3)
        self.sessions_date_start = QtWidgets.QDateEdit(self.tab_sessions)
        self.sessions_date_start.setAutoFillBackground(False)
        self.sessions_date_start.setWrapping(False)
        self.sessions_date_start.setReadOnly(False)
        self.sessions_date_start.setSpecialValueText("")
        self.sessions_date_start.setAccelerated(False)
        self.sessions_date_start.setProperty("showGroupSeparator", False)
        self.sessions_date_start.setCalendarPopup(True)
        self.sessions_date_start.setObjectName("sessions_date_start")
        self.horizontalLayout_2.addWidget(self.sessions_date_start)
        self.sessions_date_end = QtWidgets.QDateEdit(self.tab_sessions)
        self.sessions_date_end.setAutoFillBackground(False)
        self.sessions_date_end.setWrapping(False)
        self.sessions_date_end.setReadOnly(False)
        self.sessions_date_end.setSpecialValueText("")
        self.sessions_date_end.setAccelerated(False)
        self.sessions_date_end.setProperty("showGroupSeparator", False)
        self.sessions_date_end.setCalendarPopup(True)
        self.sessions_date_end.setObjectName("sessions_date_end")
        self.horizontalLayout_2.addWidget(self.sessions_date_end)
        self.line = QtWidgets.QFrame(self.tab_sessions)
        self.line.setFrameShape(QtWidgets.QFrame.VLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.horizontalLayout_2.addWidget(self.line)
        self.sessions_enter_search_phrase = QtWidgets.QLineEdit(self.tab_sessions)
        self.sessions_enter_search_phrase.setText("")
        self.sessions_enter_search_phrase.setAlignment(QtCore.Qt.AlignCenter)
        self.sessions_enter_search_phrase.setObjectName("sessions_enter_search_phrase")
        self.horizontalLayout_2.addWidget(self.sessions_enter_search_phrase)
        self.sessions_btn_show_result = QtWidgets.QPushButton(self.tab_sessions)
        self.sessions_btn_show_result.setObjectName("sessions_btn_show_result")
        self.horizontalLayout_2.addWidget(self.sessions_btn_show_result)
        self.verticalLayout_2.addLayout(self.horizontalLayout_2)
        self.sessions_table = QtWidgets.QTableWidget(self.tab_sessions)
        self.sessions_table.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.sessions_table.setAlternatingRowColors(True)
        self.sessions_table.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        self.sessions_table.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.sessions_table.setShowGrid(True)
        self.sessions_table.setGridStyle(QtCore.Qt.SolidLine)
        self.sessions_table.setCornerButtonEnabled(True)
        self.sessions_table.setObjectName("sessions_table")
        self.sessions_table.setColumnCount(10)
        self.sessions_table.setRowCount(9)
        item = QtWidgets.QTableWidgetItem()
        self.sessions_table.setVerticalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.sessions_table.setVerticalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.sessions_table.setVerticalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        self.sessions_table.setVerticalHeaderItem(3, item)
        item = QtWidgets.QTableWidgetItem()
        self.sessions_table.setVerticalHeaderItem(4, item)
        item = QtWidgets.QTableWidgetItem()
        self.sessions_table.setVerticalHeaderItem(5, item)
        item = QtWidgets.QTableWidgetItem()
        self.sessions_table.setVerticalHeaderItem(6, item)
        item = QtWidgets.QTableWidgetItem()
        self.sessions_table.setVerticalHeaderItem(7, item)
        item = QtWidgets.QTableWidgetItem()
        self.sessions_table.setVerticalHeaderItem(8, item)
        item = QtWidgets.QTableWidgetItem()
        self.sessions_table.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.sessions_table.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.sessions_table.setHorizontalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        self.sessions_table.setHorizontalHeaderItem(3, item)
        item = QtWidgets.QTableWidgetItem()
        self.sessions_table.setHorizontalHeaderItem(4, item)
        item = QtWidgets.QTableWidgetItem()
        self.sessions_table.setHorizontalHeaderItem(5, item)
        item = QtWidgets.QTableWidgetItem()
        self.sessions_table.setHorizontalHeaderItem(6, item)
        item = QtWidgets.QTableWidgetItem()
        self.sessions_table.setHorizontalHeaderItem(7, item)
        item = QtWidgets.QTableWidgetItem()
        self.sessions_table.setHorizontalHeaderItem(8, item)
        item = QtWidgets.QTableWidgetItem()
        self.sessions_table.setHorizontalHeaderItem(9, item)
        item = QtWidgets.QTableWidgetItem()
        self.sessions_table.setItem(0, 0, item)
        item = QtWidgets.QTableWidgetItem()
        self.sessions_table.setItem(0, 2, item)
        item = QtWidgets.QTableWidgetItem()
        self.sessions_table.setItem(0, 5, item)
        item = QtWidgets.QTableWidgetItem()
        self.sessions_table.setItem(7, 0, item)
        item = QtWidgets.QTableWidgetItem()
        self.sessions_table.setItem(7, 2, item)
        item = QtWidgets.QTableWidgetItem()
        self.sessions_table.setItem(7, 5, item)
        item = QtWidgets.QTableWidgetItem()
        self.sessions_table.setItem(8, 0, item)
        item = QtWidgets.QTableWidgetItem()
        self.sessions_table.setItem(8, 2, item)
        item = QtWidgets.QTableWidgetItem()
        self.sessions_table.setItem(8, 5, item)
        self.sessions_table.horizontalHeader().setCascadingSectionResizes(False)
        self.sessions_table.horizontalHeader().setHighlightSections(True)
        self.sessions_table.horizontalHeader().setStretchLastSection(True)
        self.sessions_table.verticalHeader().setVisible(False)
        self.verticalLayout_2.addWidget(self.sessions_table)
        self.tabWidget.addTab(self.tab_sessions, "")
        self.tab_cinemahalls = QtWidgets.QWidget()
        self.tab_cinemahalls.setObjectName("tab_cinemahalls")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.tab_cinemahalls)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.cinemahalls_btn_add_hall = QtWidgets.QPushButton(self.tab_cinemahalls)
        self.cinemahalls_btn_add_hall.setObjectName("cinemahalls_btn_add_hall")
        self.horizontalLayout_4.addWidget(self.cinemahalls_btn_add_hall)
        self.cinemahalls_btn_edit_hall = QtWidgets.QPushButton(self.tab_cinemahalls)
        self.cinemahalls_btn_edit_hall.setObjectName("cinemahalls_btn_edit_hall")
        self.horizontalLayout_4.addWidget(self.cinemahalls_btn_edit_hall)
        self.cinemahalls_btn_delete_hall = QtWidgets.QPushButton(self.tab_cinemahalls)
        self.cinemahalls_btn_delete_hall.setObjectName("cinemahalls_btn_delete_hall")
        self.horizontalLayout_4.addWidget(self.cinemahalls_btn_delete_hall)
        spacerItem3 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding,
                                            QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_4.addItem(spacerItem3)
        self.cinemahalls_enter_search_phrase = QtWidgets.QLineEdit(self.tab_cinemahalls)
        self.cinemahalls_enter_search_phrase.setInputMask("")
        self.cinemahalls_enter_search_phrase.setText("")
        self.cinemahalls_enter_search_phrase.setAlignment(QtCore.Qt.AlignCenter)
        self.cinemahalls_enter_search_phrase.setCursorMoveStyle(QtCore.Qt.LogicalMoveStyle)
        self.cinemahalls_enter_search_phrase.setObjectName("cinemahalls_enter_search_phrase")
        self.horizontalLayout_4.addWidget(self.cinemahalls_enter_search_phrase)
        self.cinemahalls_btn_search_hall = QtWidgets.QPushButton(self.tab_cinemahalls)
        self.cinemahalls_btn_search_hall.setObjectName("cinemahalls_btn_search_hall")
        self.horizontalLayout_4.addWidget(self.cinemahalls_btn_search_hall)
        self.verticalLayout_4.addLayout(self.horizontalLayout_4)
        self.cinemahalls_table = QtWidgets.QTableWidget(self.tab_cinemahalls)
        self.cinemahalls_table.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.cinemahalls_table.setAlternatingRowColors(True)
        self.cinemahalls_table.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        self.cinemahalls_table.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.cinemahalls_table.setShowGrid(True)
        self.cinemahalls_table.setGridStyle(QtCore.Qt.SolidLine)
        self.cinemahalls_table.setCornerButtonEnabled(True)
        self.cinemahalls_table.setObjectName("cinemahalls_table")
        self.cinemahalls_table.setColumnCount(4)
        self.cinemahalls_table.setRowCount(3)
        item = QtWidgets.QTableWidgetItem()
        self.cinemahalls_table.setVerticalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.cinemahalls_table.setVerticalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.cinemahalls_table.setVerticalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignLeading | QtCore.Qt.AlignVCenter)
        self.cinemahalls_table.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.cinemahalls_table.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.cinemahalls_table.setHorizontalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        self.cinemahalls_table.setHorizontalHeaderItem(3, item)
        item = QtWidgets.QTableWidgetItem()
        self.cinemahalls_table.setItem(0, 0, item)
        item = QtWidgets.QTableWidgetItem()
        self.cinemahalls_table.setItem(0, 1, item)
        item = QtWidgets.QTableWidgetItem()
        self.cinemahalls_table.setItem(0, 2, item)
        item = QtWidgets.QTableWidgetItem()
        self.cinemahalls_table.setItem(1, 0, item)
        item = QtWidgets.QTableWidgetItem()
        self.cinemahalls_table.setItem(1, 1, item)
        item = QtWidgets.QTableWidgetItem()
        self.cinemahalls_table.setItem(1, 2, item)
        item = QtWidgets.QTableWidgetItem()
        self.cinemahalls_table.setItem(2, 0, item)
        item = QtWidgets.QTableWidgetItem()
        self.cinemahalls_table.setItem(2, 1, item)
        item = QtWidgets.QTableWidgetItem()
        self.cinemahalls_table.setItem(2, 2, item)
        self.cinemahalls_table.horizontalHeader().setCascadingSectionResizes(False)
        self.cinemahalls_table.horizontalHeader().setHighlightSections(True)
        self.cinemahalls_table.horizontalHeader().setStretchLastSection(False)
        self.cinemahalls_table.verticalHeader().setVisible(False)
        self.cinemahalls_table.verticalHeader().setStretchLastSection(False)
        self.verticalLayout_4.addWidget(self.cinemahalls_table)
        self.tabWidget.addTab(self.tab_cinemahalls, "")
        self.tab_plans = QtWidgets.QWidget()
        self.tab_plans.setObjectName("tab_plans")
        self.verticalLayout_6 = QtWidgets.QVBoxLayout(self.tab_plans)
        self.verticalLayout_6.setObjectName("verticalLayout_6")
        self.horizontalLayout_6 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        self.plans_btn_add_plan = QtWidgets.QPushButton(self.tab_plans)
        self.plans_btn_add_plan.setObjectName("plans_btn_add_plan")
        self.horizontalLayout_6.addWidget(self.plans_btn_add_plan)
        self.plans_btn_edit_plan = QtWidgets.QPushButton(self.tab_plans)
        self.plans_btn_edit_plan.setObjectName("plans_btn_edit_plan")
        self.horizontalLayout_6.addWidget(self.plans_btn_edit_plan)
        self.plans_btn_delete_plan = QtWidgets.QPushButton(self.tab_plans)
        self.plans_btn_delete_plan.setObjectName("plans_btn_delete_plan")
        self.horizontalLayout_6.addWidget(self.plans_btn_delete_plan)
        spacerItem4 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding,
                                            QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_6.addItem(spacerItem4)
        self.plans_edit_search_method = QtWidgets.QPushButton(self.tab_plans)
        self.plans_edit_search_method.setObjectName("plans_edit_search_method")
        self.horizontalLayout_6.addWidget(self.plans_edit_search_method)
        self.plans_enter_search_phrase = QtWidgets.QLineEdit(self.tab_plans)
        self.plans_enter_search_phrase.setAlignment(QtCore.Qt.AlignCenter)
        self.plans_enter_search_phrase.setObjectName("plans_enter_search_phrase")
        self.horizontalLayout_6.addWidget(self.plans_enter_search_phrase)
        self.plans_btn_search_plan = QtWidgets.QPushButton(self.tab_plans)
        self.plans_btn_search_plan.setObjectName("plans_btn_search_plan")
        self.horizontalLayout_6.addWidget(self.plans_btn_search_plan)
        self.verticalLayout_6.addLayout(self.horizontalLayout_6)
        self.plans_table = QtWidgets.QTableWidget(self.tab_plans)
        self.plans_table.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.plans_table.setAlternatingRowColors(True)
        self.plans_table.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        self.plans_table.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectItems)
        self.plans_table.setShowGrid(True)
        self.plans_table.setGridStyle(QtCore.Qt.SolidLine)
        self.plans_table.setCornerButtonEnabled(True)
        self.plans_table.setObjectName("plans_table")
        self.plans_table.setColumnCount(7)
        self.plans_table.setRowCount(19)
        item = QtWidgets.QTableWidgetItem()
        self.plans_table.setVerticalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.plans_table.setVerticalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.plans_table.setVerticalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        self.plans_table.setVerticalHeaderItem(3, item)
        item = QtWidgets.QTableWidgetItem()
        self.plans_table.setVerticalHeaderItem(4, item)
        item = QtWidgets.QTableWidgetItem()
        self.plans_table.setVerticalHeaderItem(5, item)
        item = QtWidgets.QTableWidgetItem()
        self.plans_table.setVerticalHeaderItem(6, item)
        item = QtWidgets.QTableWidgetItem()
        self.plans_table.setVerticalHeaderItem(7, item)
        item = QtWidgets.QTableWidgetItem()
        self.plans_table.setVerticalHeaderItem(8, item)
        item = QtWidgets.QTableWidgetItem()
        self.plans_table.setVerticalHeaderItem(9, item)
        item = QtWidgets.QTableWidgetItem()
        self.plans_table.setVerticalHeaderItem(10, item)
        item = QtWidgets.QTableWidgetItem()
        self.plans_table.setVerticalHeaderItem(11, item)
        item = QtWidgets.QTableWidgetItem()
        self.plans_table.setVerticalHeaderItem(12, item)
        item = QtWidgets.QTableWidgetItem()
        self.plans_table.setVerticalHeaderItem(13, item)
        item = QtWidgets.QTableWidgetItem()
        self.plans_table.setVerticalHeaderItem(14, item)
        item = QtWidgets.QTableWidgetItem()
        self.plans_table.setVerticalHeaderItem(15, item)
        item = QtWidgets.QTableWidgetItem()
        self.plans_table.setVerticalHeaderItem(16, item)
        item = QtWidgets.QTableWidgetItem()
        self.plans_table.setVerticalHeaderItem(17, item)
        item = QtWidgets.QTableWidgetItem()
        self.plans_table.setVerticalHeaderItem(18, item)
        item = QtWidgets.QTableWidgetItem()
        self.plans_table.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.plans_table.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.plans_table.setHorizontalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        self.plans_table.setHorizontalHeaderItem(3, item)
        item = QtWidgets.QTableWidgetItem()
        self.plans_table.setHorizontalHeaderItem(4, item)
        item = QtWidgets.QTableWidgetItem()
        self.plans_table.setHorizontalHeaderItem(5, item)
        item = QtWidgets.QTableWidgetItem()
        self.plans_table.setHorizontalHeaderItem(6, item)
        self.plans_table.horizontalHeader().setVisible(False)
        self.plans_table.horizontalHeader().setCascadingSectionResizes(False)
        self.plans_table.horizontalHeader().setHighlightSections(True)
        self.plans_table.horizontalHeader().setSortIndicatorShown(False)
        self.plans_table.horizontalHeader().setStretchLastSection(True)
        self.plans_table.verticalHeader().setVisible(False)
        self.verticalLayout_6.addWidget(self.plans_table)
        self.tabWidget.addTab(self.tab_plans, "")
        self.verticalLayout.addWidget(self.tabWidget)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label_information = QtWidgets.QLabel(self.centralwidget)
        self.label_information.setObjectName("label_information")
        self.horizontalLayout.addWidget(self.label_information)
        spacerItem5 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding,
                                            QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem5)
        self.label_current_date_and_time = QtWidgets.QLabel(self.centralwidget)
        self.label_current_date_and_time.setObjectName("label_current_date_and_time")
        self.horizontalLayout.addWidget(self.label_current_date_and_time)
        self.current_time_edit = QtWidgets.QTimeEdit(self.centralwidget)
        self.current_time_edit.setObjectName("current_time_edit")
        self.horizontalLayout.addWidget(self.current_time_edit)
        self.current_date_edit = QtWidgets.QDateEdit(self.centralwidget)
        self.current_date_edit.setObjectName("current_date_edit")
        self.horizontalLayout.addWidget(self.current_date_edit)
        self.verticalLayout.addLayout(self.horizontalLayout)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1147, 21))
        self.menubar.setObjectName("menubar")
        self.menu = QtWidgets.QMenu(self.menubar)
        self.menu.setObjectName("menu")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.action_new_tickets_system = QtWidgets.QAction(MainWindow)
        self.action_new_tickets_system.setObjectName("action_new_tickets_system")

        self.action_open_tickets_system = QtWidgets.QAction(MainWindow)
        self.action_open_tickets_system.setObjectName("action_open_tickets_system")

        self.action_open_tickets_system = QtWidgets.QAction(MainWindow)
        self.action_open_tickets_system.setObjectName("action_open_tickets_system")

        self.action_rename_tickets_system = QtWidgets.QAction(MainWindow)
        self.action_rename_tickets_system.setObjectName("action_rename_tickets_system")

        self.action_exit = QtWidgets.QAction(MainWindow)
        self.action_exit.setObjectName("action_exit")

        self.menu.addAction(self.action_new_tickets_system)
        self.menu.addAction(self.action_open_tickets_system)
        self.menu.addSeparator()
        self.menu.addAction(self.action_rename_tickets_system)
        self.menu.addAction(self.action_exit)

        self.menubar.addAction(self.menu.menuAction())

        self.retranslateUi(MainWindow)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Билетая система"))
        self.sessions_btn_show_result.setStatusTip(_translate("MainWindow", "Найти сеансы"))
        self.label.setText(_translate("MainWindow", "Купить билеты"))
        self.label_4.setText(_translate("MainWindow", "Временной период"))
        self.tickets_date_start.setStatusTip(_translate("MainWindow", "Дата начала"))
        self.tickets_date_end.setStatusTip(_translate("MainWindow", "Дата конца"))
        self.tickets_tab_cinema_selector.setStatusTip(_translate("MainWindow", "Выбрать кинотеатр"))
        self.tickets_tab_cinema_selector.setItemText(0,
                                                     _translate("MainWindow", "Выбрать кинотеатр"))
        self.tickets_tab_cinema_selector.setItemText(1, _translate("MainWindow", "Минотавр"))
        self.tickets_tab_cinema_selector.setItemText(2, _translate("MainWindow", "Крылья"))
        self.tickets_tab_cinema_selector.setItemText(3, _translate("MainWindow", "Луна"))
        self.tickets_enter_search_phrase.setStatusTip(_translate("MainWindow", "Строка поиска"))
        self.tickets_enter_search_phrase.setPlaceholderText(
            _translate("MainWindow", "поиск по фильмам "))
        self.tickets_btn_search.setStatusTip(_translate("MainWindow", "Найти подходящие сеансы"))
        self.tickets_btn_search.setText(_translate("MainWindow", "Поиск"))
        self.tickets_table.setSortingEnabled(True)
        item = self.tickets_table.horizontalHeaderItem(0)
        item.setText(_translate("MainWindow", "New Column"))
        item = self.tickets_table.horizontalHeaderItem(1)
        item.setText(_translate("MainWindow", "New Column"))
        item = self.tickets_table.horizontalHeaderItem(2)
        item.setText(_translate("MainWindow", "New Column"))
        item = self.tickets_table.horizontalHeaderItem(3)
        item.setText(_translate("MainWindow", "New Column"))
        item = self.tickets_table.horizontalHeaderItem(4)
        item.setText(_translate("MainWindow", "New Column"))
        item = self.tickets_table.horizontalHeaderItem(5)
        item.setText(_translate("MainWindow", "New Column"))
        item = self.tickets_table.horizontalHeaderItem(6)
        item.setText(_translate("MainWindow", "New Column"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_tickets),
                                  _translate("MainWindow", "Касса"))
        self.cinemas_btn_add_cinema.setStatusTip(_translate("MainWindow", "Добавить кинотеатр"))
        self.cinemas_btn_add_cinema.setText(_translate("MainWindow", "Добавить"))
        self.cinemas_btn_edit_cinema.setStatusTip(
            _translate("MainWindow", "Редактировать выделенный кинотеатр"))
        self.cinemas_btn_edit_cinema.setText(_translate("MainWindow", "Редактировать"))
        self.cinemas_btn_delete_cinema.setStatusTip(
            _translate("MainWindow", "Удалить выделенный кинотеатр"))
        self.cinemas_btn_delete_cinema.setText(_translate("MainWindow", "Удалить"))
        self.cinemas_enter_search_phrase.setStatusTip(_translate("MainWindow", "Строка поиска"))
        self.cinemas_enter_search_phrase.setPlaceholderText(
            _translate("MainWindow", "поиск по кинотеатрам"))
        self.cinemas_btn_search_cinema.setStatusTip(_translate("MainWindow", "Найти кинотеатры"))
        self.cinemas_btn_search_cinema.setText(_translate("MainWindow", "Поиск"))
        self.cinema_table.setSortingEnabled(True)
        item = self.cinema_table.verticalHeaderItem(0)
        item.setText(_translate("MainWindow", "1"))
        item = self.cinema_table.verticalHeaderItem(1)
        item.setText(_translate("MainWindow", "2"))
        item = self.cinema_table.verticalHeaderItem(2)
        item.setText(_translate("MainWindow", "3"))
        item = self.cinema_table.horizontalHeaderItem(0)
        item.setText(_translate("MainWindow", "Название"))
        item = self.cinema_table.horizontalHeaderItem(1)
        item.setText(_translate("MainWindow", "Адресс"))
        item = self.cinema_table.horizontalHeaderItem(2)
        item.setText(_translate("MainWindow", "Кинозалы"))
        __sortingEnabled = self.cinema_table.isSortingEnabled()
        self.cinema_table.setSortingEnabled(False)
        item = self.cinema_table.item(0, 0)
        item.setText(_translate("MainWindow", "Минотавр"))
        item = self.cinema_table.item(0, 1)
        item.setText(_translate("MainWindow", "ул. Мира, 10"))
        item = self.cinema_table.item(1, 0)
        item.setText(_translate("MainWindow", "Луна"))
        item = self.cinema_table.item(1, 1)
        item.setText(_translate("MainWindow", "Камышинская, 123"))
        item = self.cinema_table.item(2, 0)
        item.setText(_translate("MainWindow", "Крылья"))
        item = self.cinema_table.item(2, 1)
        item.setText(_translate("MainWindow", "пр. Ленкома, 65"))
        self.cinema_table.setSortingEnabled(__sortingEnabled)
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_cinemas),
                                  _translate("MainWindow", "Кинотеатры"))
        self.sessions_btn_add_session.setStatusTip(_translate("MainWindow", "Добавить сеанс"))
        self.sessions_btn_add_session.setText(_translate("MainWindow", "Добавить"))
        self.sessions_btn_edit_session.setStatusTip(
            _translate("MainWindow", "Редактировать выделенный сеанс"))
        self.sessions_btn_edit_session.setText(_translate("MainWindow", "Редактировать"))
        self.sessions_btn_delete_session.setStatusTip(
            _translate("MainWindow", "Удалить выделенный сеанс"))
        self.sessions_btn_delete_session.setText(_translate("MainWindow", "Удалить"))
        self.label_3.setText(_translate("MainWindow", "Временной период"))
        self.sessions_date_start.setStatusTip(_translate("MainWindow", "Дата начала"))
        self.sessions_date_end.setStatusTip(_translate("MainWindow", "Дата конца"))
        self.sessions_enter_search_phrase.setStatusTip(_translate("MainWindow", "Строка поиска"))
        self.sessions_enter_search_phrase.setPlaceholderText(
            _translate("MainWindow", "поиск по фильмам"))
        self.sessions_btn_show_result.setText(_translate("MainWindow", "Поиск"))
        self.sessions_table.setSortingEnabled(True)
        item = self.sessions_table.verticalHeaderItem(0)
        item.setText(_translate("MainWindow", "New Row"))
        item = self.sessions_table.verticalHeaderItem(1)
        item.setText(_translate("MainWindow", "New Row"))
        item = self.sessions_table.verticalHeaderItem(2)
        item.setText(_translate("MainWindow", "New Row"))
        item = self.sessions_table.verticalHeaderItem(3)
        item.setText(_translate("MainWindow", "New Row"))
        item = self.sessions_table.verticalHeaderItem(4)
        item.setText(_translate("MainWindow", "New Row"))
        item = self.sessions_table.verticalHeaderItem(5)
        item.setText(_translate("MainWindow", "New Row"))
        item = self.sessions_table.verticalHeaderItem(6)
        item.setText(_translate("MainWindow", "New Row"))
        item = self.sessions_table.verticalHeaderItem(7)
        item.setText(_translate("MainWindow", "New Row"))
        item = self.sessions_table.verticalHeaderItem(8)
        item.setText(_translate("MainWindow", "New Row"))
        item = self.sessions_table.horizontalHeaderItem(0)
        item.setText(_translate("MainWindow", "Дата"))
        item = self.sessions_table.horizontalHeaderItem(1)
        item.setText(_translate("MainWindow", "Время"))
        item = self.sessions_table.horizontalHeaderItem(2)
        item.setText(_translate("MainWindow", "Название"))
        item = self.sessions_table.horizontalHeaderItem(3)
        item.setText(_translate("MainWindow", "Кинотеатр"))
        item = self.sessions_table.horizontalHeaderItem(4)
        item.setText(_translate("MainWindow", "Кинозал"))
        item = self.sessions_table.horizontalHeaderItem(5)
        item.setText(_translate("MainWindow", "Продано"))
        item = self.sessions_table.horizontalHeaderItem(6)
        item.setText(_translate("MainWindow", "Осталось"))
        item = self.sessions_table.horizontalHeaderItem(7)
        item.setText(_translate("MainWindow", "Схема зала"))
        item = self.sessions_table.horizontalHeaderItem(8)
        item.setText(_translate("MainWindow", "Действие"))
        item = self.sessions_table.horizontalHeaderItem(9)
        item.setText(_translate("MainWindow", "Статус"))
        __sortingEnabled = self.sessions_table.isSortingEnabled()
        self.sessions_table.setSortingEnabled(False)
        item = self.sessions_table.item(0, 0)
        item.setText(_translate("MainWindow", "3"))
        item = self.sessions_table.item(0, 2)
        item.setText(_translate("MainWindow", "3"))
        item = self.sessions_table.item(0, 5)
        item.setText(_translate("MainWindow", "ы"))
        item = self.sessions_table.item(7, 0)
        item.setText(_translate("MainWindow", "ауы"))
        item = self.sessions_table.item(7, 2)
        item.setText(_translate("MainWindow", "ы"))
        item = self.sessions_table.item(7, 5)
        item.setText(_translate("MainWindow", "ыуа"))
        item = self.sessions_table.item(8, 0)
        item.setText(_translate("MainWindow", "уаы"))
        item = self.sessions_table.item(8, 2)
        item.setText(_translate("MainWindow", "аы"))
        item = self.sessions_table.item(8, 5)
        item.setText(_translate("MainWindow", "ыуа"))
        self.sessions_table.setSortingEnabled(__sortingEnabled)
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_sessions),
                                  _translate("MainWindow", "Сеансы"))
        self.cinemahalls_btn_add_hall.setStatusTip(_translate("MainWindow", "Добавить кинозал"))
        self.cinemahalls_btn_add_hall.setText(_translate("MainWindow", "Добавить"))
        self.cinemahalls_btn_edit_hall.setStatusTip(
            _translate("MainWindow", "Редактировать выделенный кинозал"))
        self.cinemahalls_btn_edit_hall.setText(_translate("MainWindow", "Редактировать"))
        self.cinemahalls_btn_delete_hall.setStatusTip(
            _translate("MainWindow", "Удалить выделенный кинозал"))
        self.cinemahalls_btn_delete_hall.setText(_translate("MainWindow", "Удалить"))
        self.cinemahalls_enter_search_phrase.setStatusTip(_translate("MainWindow", "Строка поиска"))
        self.cinemahalls_enter_search_phrase.setPlaceholderText(
            _translate("MainWindow", "поиск по кинозалам"))
        self.cinemahalls_btn_search_hall.setStatusTip(_translate("MainWindow", "Найти кинозалы"))
        self.cinemahalls_btn_search_hall.setText(_translate("MainWindow", "Поиск"))
        self.cinemahalls_table.setSortingEnabled(True)
        item = self.cinemahalls_table.verticalHeaderItem(0)
        item.setText(_translate("MainWindow", "1"))
        item = self.cinemahalls_table.verticalHeaderItem(1)
        item.setText(_translate("MainWindow", "2"))
        item = self.cinemahalls_table.verticalHeaderItem(2)
        item.setText(_translate("MainWindow", "3"))
        item = self.cinemahalls_table.horizontalHeaderItem(0)
        item.setText(_translate("MainWindow", "Название / №"))
        item = self.cinemahalls_table.horizontalHeaderItem(1)
        item.setText(_translate("MainWindow", "Кинотеатр"))
        item = self.cinemahalls_table.horizontalHeaderItem(2)
        item.setText(_translate("MainWindow", "Вместимость"))
        item = self.cinemahalls_table.horizontalHeaderItem(3)
        item.setText(_translate("MainWindow", "Планировка"))
        __sortingEnabled = self.cinemahalls_table.isSortingEnabled()
        self.cinemahalls_table.setSortingEnabled(False)
        item = self.cinemahalls_table.item(0, 0)
        item.setText(_translate("MainWindow", "1"))
        item = self.cinemahalls_table.item(0, 1)
        item.setText(_translate("MainWindow", "Минотавр"))
        item = self.cinemahalls_table.item(0, 2)
        item.setText(_translate("MainWindow", "40"))
        item = self.cinemahalls_table.item(1, 0)
        item.setText(_translate("MainWindow", "2"))
        item = self.cinemahalls_table.item(1, 1)
        item.setText(_translate("MainWindow", "Луна"))
        item = self.cinemahalls_table.item(1, 2)
        item.setText(_translate("MainWindow", "24"))
        item = self.cinemahalls_table.item(2, 0)
        item.setText(_translate("MainWindow", "3"))
        item = self.cinemahalls_table.item(2, 1)
        item.setText(_translate("MainWindow", "Крылья"))
        item = self.cinemahalls_table.item(2, 2)
        item.setText(_translate("MainWindow", "60"))
        self.cinemahalls_table.setSortingEnabled(__sortingEnabled)
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_cinemahalls),
                                  _translate("MainWindow", "Кинозалы"))
        self.plans_btn_add_plan.setStatusTip(
            _translate("MainWindow", "Добавить планировку кинозала"))
        self.plans_btn_add_plan.setText(_translate("MainWindow", "Добавить"))
        self.plans_btn_edit_plan.setStatusTip(
            _translate("MainWindow", "Редактировать выделенную планировку"))
        self.plans_btn_edit_plan.setText(_translate("MainWindow", "Редактировать"))
        self.plans_btn_delete_plan.setStatusTip(
            _translate("MainWindow", "Удалить выделенную планировку"))
        self.plans_btn_delete_plan.setText(_translate("MainWindow", "Удалить"))
        self.plans_edit_search_method.setStatusTip(
            _translate("MainWindow", "Изменить критерий поиска"))
        self.plans_edit_search_method.setText(_translate("MainWindow", "Название"))
        self.plans_enter_search_phrase.setStatusTip(_translate("MainWindow", "Строка поиска"))
        self.plans_enter_search_phrase.setPlaceholderText(
            _translate("MainWindow", "поиск по названию"))
        self.plans_btn_search_plan.setStatusTip(_translate("MainWindow", "Найти планировки"))
        self.plans_btn_search_plan.setText(_translate("MainWindow", "Поиск"))
        self.plans_table.setSortingEnabled(True)
        item = self.plans_table.verticalHeaderItem(0)
        item.setText(_translate("MainWindow", "New Row"))
        item = self.plans_table.verticalHeaderItem(1)
        item.setText(_translate("MainWindow", "New Row"))
        item = self.plans_table.verticalHeaderItem(2)
        item.setText(_translate("MainWindow", "New Row"))
        item = self.plans_table.verticalHeaderItem(3)
        item.setText(_translate("MainWindow", "New Row"))
        item = self.plans_table.verticalHeaderItem(4)
        item.setText(_translate("MainWindow", "New Row"))
        item = self.plans_table.verticalHeaderItem(5)
        item.setText(_translate("MainWindow", "New Row"))
        item = self.plans_table.verticalHeaderItem(6)
        item.setText(_translate("MainWindow", "New Row"))
        item = self.plans_table.verticalHeaderItem(7)
        item.setText(_translate("MainWindow", "New Row"))
        item = self.plans_table.verticalHeaderItem(8)
        item.setText(_translate("MainWindow", "New Row"))
        item = self.plans_table.verticalHeaderItem(9)
        item.setText(_translate("MainWindow", "New Row"))
        item = self.plans_table.verticalHeaderItem(10)
        item.setText(_translate("MainWindow", "New Row"))
        item = self.plans_table.verticalHeaderItem(11)
        item.setText(_translate("MainWindow", "New Row"))
        item = self.plans_table.verticalHeaderItem(12)
        item.setText(_translate("MainWindow", "New Row"))
        item = self.plans_table.verticalHeaderItem(13)
        item.setText(_translate("MainWindow", "New Row"))
        item = self.plans_table.verticalHeaderItem(14)
        item.setText(_translate("MainWindow", "New Row"))
        item = self.plans_table.verticalHeaderItem(15)
        item.setText(_translate("MainWindow", "New Row"))
        item = self.plans_table.verticalHeaderItem(16)
        item.setText(_translate("MainWindow", "New Row"))
        item = self.plans_table.verticalHeaderItem(17)
        item.setText(_translate("MainWindow", "New Row"))
        item = self.plans_table.verticalHeaderItem(18)
        item.setText(_translate("MainWindow", "New Row"))
        item = self.plans_table.horizontalHeaderItem(0)
        item.setText(_translate("MainWindow", "New Column"))
        item = self.plans_table.horizontalHeaderItem(1)
        item.setText(_translate("MainWindow", "New Column"))
        item = self.plans_table.horizontalHeaderItem(2)
        item.setText(_translate("MainWindow", "New Column"))
        item = self.plans_table.horizontalHeaderItem(3)
        item.setText(_translate("MainWindow", "New Column"))
        item = self.plans_table.horizontalHeaderItem(4)
        item.setText(_translate("MainWindow", "New Column"))
        item = self.plans_table.horizontalHeaderItem(5)
        item.setText(_translate("MainWindow", "New Column"))
        item = self.plans_table.horizontalHeaderItem(6)
        item.setText(_translate("MainWindow", "New Column"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_plans),
                                  _translate("MainWindow", "Планировки"))
        self.label_information.setText(_translate("MainWindow", "TextLabel"))
        self.label_current_date_and_time.setText(_translate("MainWindow", "Текущее время и дата"))
        self.menu.setTitle(_translate("MainWindow", "Файл"))
        self.action_open_tickets_system.setText(_translate("MainWindow", "Открыть систему"))
        self.action_new_tickets_system.setText(_translate("MainWindow", "Создать систему"))
        self.action_exit.setText(_translate("MainWindow", "Выход"))
        self.action_rename_tickets_system.setText(_translate("MainWindow", "Переименовать систему"))


class TicketsSystemMainWindow(Ui_MainWindow, QMainWindow):
    def __init__(self):
        super(TicketsSystemMainWindow, self).__init__()
        self.setupUi(self)

        self.action_open_tickets_system.triggered.connect(self.open_tickets_system)
        self.action_new_tickets_system.triggered.connect(self.create_tickets_system)
        self.action_rename_tickets_system.triggered.connect(self.rename_tickets_system)
        self.action_exit.triggered.connect(self.close_tickets_system)

        self.cinemas_btn_search_cinema.clicked.connect(self.cinemas_btn_search_clicked)
        self.cinemahalls_btn_search_hall.clicked.connect(self.cinemahalls_btn_search_clicked)
        self.plans_btn_search_plan.clicked.connect(self.plans_btn_search_clicked)
        self.plans_edit_search_method.clicked.connect(self.plans_btn_change_search_method_clicked)

        self.label_information.setText('')

        self.database_filename = None
        self.database_connection = None

    def open_tickets_system(self, database_temp_filename):
        if not database_temp_filename:
            database_temp_filename = QFileDialog.getOpenFileName(
                self, 'Выбрать файл билетной системы', '',
                f'Файл билетной системы (*{TICKETS_SYSTEM_FILE_EXTENSION});;Все файлы (*)')[0]

        if database_temp_filename:
            if database_temp_filename != self.database_filename:
                try:
                    self.database_connection = sqlite3.connect(database_temp_filename)
                    self.database_cursor = self.database_connection.cursor()
                    title = self.database_cursor.execute("""SELECT value FROM information
                                                   WHERE name = 'window_title'""").fetchone()
                    if title is None:
                        raise sqlite3.DatabaseError
                    else:
                        title = title[0]

                    self.setWindowTitle(title)

                    self.database_filename = database_temp_filename

                    self.load_all_data_from_database()

                except sqlite3.DatabaseError:
                    self.label_information.setText(
                        f"Файл билетной системы '{database_temp_filename}' поврежден")

    def create_tickets_system(self):
        self.creation_window = CreateTicketsSystemWindow(self)
        self.hide()
        self.creation_window.show()

    def rename_tickets_system(self):
        new_name, ok_pressed = QInputDialog.getText(self, 'Переименовать систему',
                                                    'Введите новое название билетной системы',
                                                    QLineEdit.Normal, '')
        if ok_pressed:
            new_name = new_name.strip()
            if len(new_name):
                try:
                    self.database_cursor.execute(f"""UPDATE information SET value = '{new_name}'
                                                        WHERE name = 'window_title'""")
                    self.database_connection.commit()
                    self.setWindowTitle(new_name)
                except Exception as e:
                    print(e)

    def close_tickets_system(self):
        self.close()

    def load_all_data_from_database(self):
        self.tickets_btn_search.click()
        self.cinemahalls_btn_search_hall.click()
        self.cinemas_btn_search_cinema.click()
        self.plans_btn_search_plan.click()
        self.sessions_btn_show_result.click()

    def tickets_btn_search_clicked(self):
        pass

    def cinemas_btn_search_clicked(self):
        self.label_information.setText('')
        search_phrase = self.cinemas_enter_search_phrase.text().strip()
        query = f"""SELECT * FROM cinemas WHERE name LIKE '%{search_phrase}%'"""
        try:
            result = list(self.database_cursor.execute(query).fetchall())
            self.fill_table_from_db_result(self.cinema_table, result, CINEMAS_TABLE_HEADERS)
        except Exception:
            pass

    def cinemahalls_btn_search_clicked(self):
        self.label_information.setText('')
        search_phrase = self.cinemahalls_enter_search_phrase.text().strip()
        query = f"""SELECT * FROM cinemahalls WHERE name LIKE '%{search_phrase}%'"""
        try:
            result = list(self.database_cursor.execute(query).fetchall())
            self.fill_table_from_db_result(self.cinemahalls_table,
                                           result, CINEMAHALLS_TABLE_HEADERS)
        except Exception:
            pass

    def plans_btn_search_clicked(self):
        self.label_information.setText('')
        search_phrase = self.plans_enter_search_phrase.text().strip()
        query = f"""SELECT * FROM plans """
        if search_phrase:
            if self.plans_edit_search_method.text() == 'Название':
                query += f"WHERE name LIKE '%{search_phrase}%'"
            else:
                if 'вместимость' in search_phrase:
                    query += search_phrase.replace('WHERE вместимость', 'sits_number')
                else:
                    self.label_information.setText("Неверный запрос: слово 'вместимость' не найдено")
        try:
            result = list(self.database_cursor.execute(query).fetchall())
            self.fill_table_from_db_result(self.plans_table, result)
        except Exception:
            pass

    def sessions_btn_search_clicked(self):
        self.label_information.setText('')
        pass

    def plans_btn_change_search_method_clicked(self):
        if self.plans_edit_search_method.text() == 'Название':
            self.plans_enter_search_phrase.setPlaceholderText('поиск по вместимости')
            self.plans_enter_search_phrase.setText('вместимость = 10')
            self.plans_edit_search_method.setText('Вместимость')
        else:
            self.plans_enter_search_phrase.setPlaceholderText('поиск по названию')
            self.plans_enter_search_phrase.setText('')
            self.plans_edit_search_method.setText('Название')

    def fill_table_from_db_result(self, table, result, headers=None):
        if not result:
            self.label_information.setText('Ничего не нашлось')

        table.setRowCount(0)
        table.setColumnCount(len(result[0]))

        if headers is not None:
            table.setHorizontalHeaderLabels(headers)

        for i, row in enumerate(result):
            table.setRowCount(table.rowCount() + 1)
            for j, col in enumerate(row):
                table.setItem(i, j, QTableWidgetItem(col))

    def closeEvent(self, a0: QtGui.QCloseEvent):
        if self.database_connection is not None:
            self.database_connection.close()
        self.close()


class CreateTicketsSystemWindow(QWidget):
    def __init__(self, mainwindow):
        super(CreateTicketsSystemWindow, self).__init__()
        self.setupUi(self)
        self.mainwindow = mainwindow
        self.btn.clicked.connect(self.button_clicked)

    def button_clicked(self):
        system_name = self.title_input.text().strip()
        check_result = self._check_system_name(system_name)
        if check_result != '':
            self.error_label.setText(check_result)
        else:
            files = list(os.walk(os.getcwd()))[0][2]
            if system_name + TICKETS_SYSTEM_FILE_EXTENSION in files:
                mb = QtWidgets.QMessageBox
                answer = mb.question(self, '',
                                     f'Файл {system_name + TICKETS_SYSTEM_FILE_EXTENSION}'
                                     f' уже есть. Заменить?',
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
        filename += TICKETS_SYSTEM_FILE_EXTENSION
        with open(filename, 'w', encoding='utf-8'):
            pass
        try:
            self.connection = sqlite3.connect(filename)
            self.cursor = self.connection.cursor()
            self.cursor.executescript(SCRIPT_FOR_CREATE_TICKETS_SYSTEM_DATABASE +
                                      f"""INSERT INTO information(name, value) VALUES
                                       ('window_title',
                    '{filename[:filename.rfind('.')]}');""")
            self.connection.close()

            self.mainwindow.open_tickets_system(filename)
            self.mainwindow.show()

            self.close()
        except Exception as e:
            print(e)

    def closeEvent(self, a0: QtGui.QCloseEvent) -> None:
        self.mainwindow.show()
        self.close()

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
    application = QApplication(sys.argv)
    main_program_window = TicketsSystemMainWindow()
    main_program_window.show()
    sys.exit(application.exec())
