# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'ui_mainwindow.ui'
##
## Created by: Qt User Interface Compiler version 5.15.1
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(561, 607)
        icon = QIcon()
        icon.addFile(u"icons/terminal.svg", QSize(), QIcon.Normal, QIcon.Off)
        MainWindow.setWindowIcon(icon)
        self.new_server = QAction(MainWindow)
        self.new_server.setObjectName(u"new_server")
        icon1 = QIcon()
        icon1.addFile(u"icons/server.svg", QSize(), QIcon.Normal, QIcon.On)
        self.new_server.setIcon(icon1)
        self.new_server.setShortcutVisibleInContextMenu(True)
        self.close_server = QAction(MainWindow)
        self.close_server.setObjectName(u"close_server")
        self.close_server.setEnabled(False)
        icon4 = QIcon()
        icon4.addFile(u"icons/x-circle.svg", QSize(), QIcon.Normal, QIcon.On)
        self.close_server.setIcon(icon4)
        self.passive = QAction(MainWindow)
        self.passive.setObjectName(u"passive")
        self.passive.setCheckable(True)
        self.passive.setChecked(True)
        self.active = QAction(MainWindow)
        self.active.setObjectName(u"active")
        self.active.setCheckable(True)
        self.new_dir = QAction(MainWindow)
        self.new_dir.setObjectName(u"new_dir")
        self.new_dir.setEnabled(False)
        icon10 = QIcon()
        icon10.addFile(u"icons/folder-plus.svg", QSize(), QIcon.Normal, QIcon.On)
        self.new_dir.setIcon(icon10)
        self.new_file = QAction(MainWindow)
        self.new_file.setObjectName(u"new_file")
        icon11 = QIcon()
        icon11.addFile(u"icons/file-earmark-plus.svg", QSize(), QIcon.Normal, QIcon.On)
        self.new_file.setIcon(icon11)
        self.about = QAction(MainWindow)
        self.about.setObjectName(u"about")
        icon13 = QIcon()
        icon13.addFile(u"icons/question-circle.svg", QSize(), QIcon.Normal, QIcon.On)
        self.about.setIcon(icon13)
        self.upload = QAction(MainWindow)
        self.upload.setObjectName(u"upload")
        self.upload.setEnabled(False)
        icon14 = QIcon()
        icon14.addFile(u"icons/arrow-up-circle.svg", QSize(), QIcon.Normal, QIcon.Off)
        self.upload.setIcon(icon14)
        self.actionSYST = QAction(MainWindow)
        self.actionSYST.setObjectName(u"actionSYST")
        self.actionSYST.setEnabled(False)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.horizontalLayout_2 = QHBoxLayout(self.centralwidget)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.new_conn = QPushButton(self.centralwidget)
        self.new_conn.setObjectName(u"new_conn")
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.new_conn.sizePolicy().hasHeightForWidth())
        self.new_conn.setSizePolicy(sizePolicy)

        self.horizontalLayout_2.addWidget(self.new_conn)

        self.tabWidget = QTabWidget(self.centralwidget)
        self.tabWidget.setObjectName(u"tabWidget")
        self.tab = QWidget()
        self.tab.setObjectName(u"tab")
        self.gridLayout = QGridLayout(self.tab)
        self.gridLayout.setObjectName(u"gridLayout")
        self.file_list = QTableWidget(self.tab)
        if (self.file_list.columnCount() < 3):
            self.file_list.setColumnCount(3)
        self.file_list.setObjectName(u"file_list")
        self.file_list.setShowGrid(False)
        self.file_list.setColumnCount(3)

        self.gridLayout.addWidget(self.file_list, 1, 0, 1, 1)

        self.path = QLabel(self.tab)
        self.path.setObjectName(u"path")

        self.gridLayout.addWidget(self.path, 0, 0, 1, 1)

        self.progressBar = QProgressBar(self.tab)
        self.progressBar.setObjectName(u"progressBar")
        self.progressBar.setValue(0)

        self.gridLayout.addWidget(self.progressBar, 2, 0, 1, 1)

        self.tabWidget.addTab(self.tab, "")

        self.horizontalLayout_2.addWidget(self.tabWidget)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 561, 26))
        self.menubar.setNativeMenuBar(True)
        self.file = QMenu(self.menubar)
        self.file.setObjectName(u"file")
        self.cmd = QMenu(self.menubar)
        self.cmd.setObjectName(u"cmd")
        self.conn_mode = QMenu(self.cmd)
        self.conn_mode.setObjectName(u"conn_mode")
        self.help = QMenu(self.menubar)
        self.help.setObjectName(u"help")
        MainWindow.setMenuBar(self.menubar)

        self.menubar.addAction(self.file.menuAction())
        self.menubar.addAction(self.cmd.menuAction())
        self.menubar.addAction(self.help.menuAction())
        self.file.addAction(self.new_server)
        self.file.addSeparator()
        self.file.addAction(self.close_server)
        self.cmd.addAction(self.conn_mode.menuAction())
        self.cmd.addSeparator()
        self.cmd.addAction(self.new_dir)
        self.cmd.addAction(self.upload)
        self.cmd.addSeparator()
        self.cmd.addAction(self.actionSYST)
        self.conn_mode.addAction(self.passive)
        self.conn_mode.addAction(self.active)
        self.help.addAction(self.about)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"FTP \u5ba2\u6237\u7aef", None))
        self.new_server.setText(QCoreApplication.translate("MainWindow", u"\u65b0\u5efa(&N)\u2026", None))
#if QT_CONFIG(shortcut)
        self.new_server.setShortcut(QCoreApplication.translate("MainWindow", u"Ctrl+N", None))
#endif // QT_CONFIG(shortcut)
        self.close_server.setText(QCoreApplication.translate("MainWindow", u"\u5173\u95ed(&C)", None))
        self.passive.setText(QCoreApplication.translate("MainWindow", u"Passive", None))
        self.active.setText(QCoreApplication.translate("MainWindow", u"Active", None))
        self.new_dir.setText(QCoreApplication.translate("MainWindow", u"\u65b0\u5efa\u6587\u4ef6\u5939(&N)", None))
        self.new_file.setText(QCoreApplication.translate("MainWindow", u"\u65b0\u5efa\u6587\u4ef6(&F)", None))
        self.about.setText(QCoreApplication.translate("MainWindow", u"\u5173\u4e8e(&A)", None))
        self.upload.setText(QCoreApplication.translate("MainWindow", u"\u4e0a\u4f20\u6587\u4ef6", None))
        self.actionSYST.setText(QCoreApplication.translate("MainWindow", u"SYST \u547d\u4ee4", None))
        self.new_conn.setText(QCoreApplication.translate("MainWindow", u"\u65b0\u5efa\u4f1a\u8bdd", None))
        self.path.setText(QCoreApplication.translate("MainWindow", u"\u5f53\u524d\u8def\u5f84\uff1a", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), QCoreApplication.translate("MainWindow", u"Server", None))
        self.file.setTitle(QCoreApplication.translate("MainWindow", u"\u4f1a\u8bdd(&F)", None))
        self.cmd.setTitle(QCoreApplication.translate("MainWindow", u"\u547d\u4ee4(&C)", None))
        self.conn_mode.setTitle(QCoreApplication.translate("MainWindow", u"\u6570\u636e\u8fde\u63a5\u7c7b\u578b", None))
        self.help.setTitle(QCoreApplication.translate("MainWindow", u"\u5e2e\u52a9(&H)", None))
    # retranslateUi

