# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'ui_connection.ui'
##
## Created by: Qt User Interface Compiler version 5.15.1
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *


class Ui_Connection(object):
    def setupUi(self, Connection):
        if not Connection.objectName():
            Connection.setObjectName(u"Connection")
        Connection.resize(325, 305)
        icon = QIcon()
        icon.addFile(u"bootstrap-icons-1.0.0/server.svg", QSize(), QIcon.Normal, QIcon.Off)
        Connection.setWindowIcon(icon)
        self.gridLayout = QGridLayout(Connection)
        self.gridLayout.setObjectName(u"gridLayout")
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        self.ip = QLineEdit(Connection)
        self.ip.setObjectName(u"ip")

        self.port = QSpinBox(Connection)
        self.port.setObjectName(u"port")
        sizePolicy.setHeightForWidth(self.port.sizePolicy().hasHeightForWidth())
        self.port.setSizePolicy(sizePolicy)
        self.port.setMaximum(65535)
        self.port.setValue(21)

        self.username = QLineEdit(Connection)
        self.username.setObjectName(u"username")

        self.passwd = QLineEdit(Connection)
        self.passwd.setObjectName(u"passwd")
        self.passwd.setEchoMode(QLineEdit.Password)

        self.gridLayout.addWidget(self.passwd, 3, 1, 1, 1)

        self.login = QPushButton(Connection)
        self.login.setObjectName(u"login")

        self.login.setSizePolicy(sizePolicy)
        self.login.setLayoutDirection(Qt.RightToLeft)
        sizePolicy.setHeightForWidth(self.login.sizePolicy().hasHeightForWidth())

        self.gridLayout.addWidget(self.login, 4, 1, 1, 1)

        self.gridLayout.addWidget(self.username, 2, 1, 1, 1)

        self.port_label = QLabel(Connection)
        self.port_label.setObjectName(u"port_label")

        self.gridLayout.addWidget(self.port_label, 1, 0, 1, 1)

        self.gridLayout.addWidget(self.port, 1, 1, 1, 1)

        self.ip_label = QLabel(Connection)
        self.ip_label.setObjectName(u"ip_label")

        self.gridLayout.addWidget(self.ip_label, 0, 0, 1, 1)

        self.username_label = QLabel(Connection)
        self.username_label.setObjectName(u"username_label")

        self.gridLayout.addWidget(self.username_label, 2, 0, 1, 1)

        self.gridLayout.addWidget(self.ip, 0, 1, 1, 1)

        self.passwd_label = QLabel(Connection)
        self.passwd_label.setObjectName(u"passwd_label")

        self.gridLayout.addWidget(self.passwd_label, 3, 0, 1, 1)


        self.retranslateUi(Connection)

        QMetaObject.connectSlotsByName(Connection)
    # setupUi

    def retranslateUi(self, Connection):
        Connection.setWindowTitle(QCoreApplication.translate("Connection", u"\u65b0\u5efa\u4f1a\u8bdd", None))
        self.passwd.setInputMask("")
        self.login.setText(QCoreApplication.translate("Connection", u"\u8fde\u63a5", None))
        self.port_label.setText(QCoreApplication.translate("Connection", u"\u7aef\u53e3\u53f7\uff1a", None))
        self.ip_label.setText(QCoreApplication.translate("Connection", u"\u4e3b\u673a\uff1a", None))
        self.username_label.setText(QCoreApplication.translate("Connection", u"\u7528\u6237\u540d\uff1a", None))
        self.passwd_label.setText(QCoreApplication.translate("Connection", u"\u5bc6\u7801\uff1a", None))
    # retranslateUi

