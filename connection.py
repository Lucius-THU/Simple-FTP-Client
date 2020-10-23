from PySide2.QtWidgets import *
from ui_connection import Ui_Connection
import socket


class Connection(QDialog, Ui_Connection):
    def __init__(self, client=None):
        self.client = client
        super(Connection, self).__init__()
        self.setupUi(self)
        with open("style.qss", "r") as qs:
            self.setStyleSheet(qs.read())
        self.login.clicked.connect(self.conn_request)

    def conn_request(self):
        self.login.setEnabled(False)
        try:
            self.client.sock = socket.create_connection((self.ip.text(), self.port.value()))
            response = self.client.get_response()
            while response[0] == '1':
                response = self.client.get_response()
            if response[: 3] != '220':
                QMessageBox.warning(self, "无法连接", response, QMessageBox.Ok, QMessageBox.Ok)
            else:
                msg = 'USER ' + self.username.text() + '\r\n'
                self.client.sock.send(msg.encode('utf-8'))
                response = self.client.get_response()
                if response[: 2] == '33':
                    msg = 'PASS ' + self.passwd.text() + '\r\n'
                    self.client.sock.send(msg.encode('utf-8'))
                    response = self.client.get_response()
                if response[: 3] != '230':
                    QMessageBox.warning(self, "无法登录", response, QMessageBox.Ok, QMessageBox.Ok)
                else:
                    self.client.has_access = True
                    self.client.get_list()
                    self.close()
                    return
        except ConnectionRefusedError:
            QMessageBox.warning(self, "无法连接", "无法连接到给定主机端口", QMessageBox.Ok, QMessageBox.Ok)
        self.login.setEnabled(True)
