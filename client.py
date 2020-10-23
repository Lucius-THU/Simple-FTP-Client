import re
import socket
import random
import os
from PySide2.QtWidgets import *
from PySide2.QtCore import QThread, Signal

pattern = re.compile(r'(\d+),(\d+),(\d+),(\d+),(\d+),(\d+)', re.ASCII)


def parse(msg):
    t = re.search(r'[A-Z][a-z]{2}[ \d:]{9}', msg)
    filename = msg[t.end() + 1:]
    edit_time = msg[t.start(): t.end()]
    msg = msg[: t.start() - 1]
    t = msg.rfind(' ')
    size = msg[t + 1:]
    return [filename, edit_time, size, msg[0] == 'd']


class TransferFile(QThread):
    transfer_content = Signal(int)

    def __init__(self, rest, parent=None):
        super().__init__(parent)

    def retr(self):
        print('do something big')
        self.finished_signal.emit('done')

class Client(QWidget):
    MAX_LEN = 8192
    CRLF = '\r\n'

    def __init__(self):
        super(Client, self).__init__()
        self.sock = None
        self.data_sock = None
        self.list = None
        self.root = ''
        self.mode = 'passive'
        self.has_access = False

    def switch_mode(self):
        if self.mode == 'passive':
            self.mode = 'active'
        else:
            self.mode = 'passive'

    @staticmethod
    def get_line(sock):
        msg = sock.recv(Client.MAX_LEN)
        try:
            msg = msg.decode('utf-8')
        except:
            msg = msg.decode('unicode_escape')
        if not msg:
            raise EOFError
        elif msg[-2:] == Client.CRLF:
            return msg[: -2]
        elif msg[-1:] in Client.CRLF:
            return msg[: -1]
        return msg

    def get_response(self):
        msg = self.get_line(self.sock)
        if msg[3: 4] == '-':
            code = msg[: 3]
            while True:
                next_msg = self.get_line(self.sock)
                msg += '\n' + next_msg
                if next_msg[3: 4] == ' ' and next_msg[: 3] == code:
                    break
        return msg

    def data_conn(self):  # pasv/port socket 创建失败的情况有待处理
        self.sock.send('TYPE I\r\n'.encode('utf-8'))
        response = self.get_response()
        if response[: 3] != '200':
            QMessageBox.warning(self, "TYPE 命令错误", response, QMessageBox.Ok, QMessageBox.Ok)
        elif self.mode == 'passive':
            self.sock.send('PASV\r\n'.encode('utf-8'))
            try:
                response = self.get_response()
            except Exception as e:
                print(repr(e))
            if response[: 3] != '227':
                QMessageBox.warning(self, "PASV 命令错误", response, QMessageBox.Ok, QMessageBox.Ok)
            else:
                num = pattern.search(response).groups()
                host = '.'.join(num[: 4])
                port = (int(num[4]) << 8) + int(num[5])
                self.data_sock = socket.create_connection((host, port))
        else:
            host = self.sock.getsockname()[0]
            self.data_sock = socket.create_server((host, 0), family=socket.AF_INET, backlog=1)
            host, port = self.data_sock.getsockname()[: 2]
            nums = host.split('.')
            nums.extend([str(port // 256), str(port % 256)])
            msg = 'PORT ' + ','.join(nums) + '\r\n'
            try:
                self.sock.send(msg.encode('utf-8'))
            except Exception as e:
                print(repr(e))
            response = self.get_response()
            if response[: 3] != '200':
                QMessageBox.warning(self, "PORT 命令错误", response, QMessageBox.Ok, QMessageBox.Ok)

    def get_list(self):
        self.list = [['..', '', '', True]]
        self.data_conn()
        msg = 'LIST\r\n'
        self.sock.send(msg.encode('utf-8'))
        if self.mode == 'active':
            data_sock, _ = self.data_sock.accept()
            self.data_sock.close()
            self.data_sock = data_sock
        while True:
            try:
                response = self.get_line(self.data_sock)
                files = response.split('\r\n')
                for i in files:
                    self.list.append(parse(i))
            except EOFError:
                break
        self.data_sock.close()
        response = self.get_response()
        if response[: 3] == '150':
            if response.find('\r\n') != -1:
                response = response.split('\r\n')[1]
            else:
                response = self.get_response()
        if response[: 3] != '226':
            QMessageBox.warning(self, "LIST 命令错误", response, QMessageBox.Ok, QMessageBox.Ok)

    def get_cwd(self, path):
        msg = 'CWD ' + path + '\r\n'
        self.sock.send(msg.encode('utf-8'))
        response = self.get_response()
        if response[: 3] != '200' and response[: 3] != '250':
            QMessageBox.warning(self, "CWD 命令错误", response, QMessageBox.Ok, QMessageBox.Ok)

    def mkd(self, dir_name):
        msg = 'MKD ' + dir_name + '\r\n'
        self.sock.send(msg.encode('utf-8'))
        response = self.get_response()
        if response[: 3] != '257':
            QMessageBox.warning(self, 'MKD 命令错误', response, QMessageBox.Ok, QMessageBox.Ok)
            raise ValueError
        else:
            self.get_list()

    def get_pwd(self):
        msg = 'PWD\r\n'
        self.sock.send(msg.encode('utf-8'))
        response = self.get_response()
        if response[: 3] != '257':
            QMessageBox.warning(self, 'PWD 命令错误', response, QMessageBox.Ok, QMessageBox.Ok)
        else:
            self.root = ''
            i = 5
            n = len(response)
            while i < n:
                c = response[i]
                i += 1
                if c == '"':
                    if i >= n or response[i] != '"':
                        break
                    i += 1
                self.root += c

    def get_rmd(self, dir):
        msg = 'RMD ' + dir + '\r\n'
        self.sock.send(msg.encode('utf-8'))
        response = self.get_response()
        if response[: 3] != '250':
            QMessageBox.warning(self, 'RMD 命令错误', response, QMessageBox.Ok, QMessageBox.Ok)
        else:
            self.get_list()

    def get_rename(self, old_name, new_name):
        msg = 'RNFR ' + old_name + '\r\n'
        self.sock.send(msg.encode('utf-8'))
        response = self.get_response()
        if response[: 3] != '350':
            QMessageBox.warning(self, 'RNFR 命令错误', response, QMessageBox.Ok, QMessageBox.Ok)
        else:
            msg = 'RNTO ' + new_name + '\r\n'
            self.sock.send(msg.encode('utf-8'))
            response = self.get_response()
            if response[: 3] != '250':
                QMessageBox.warning(self, 'RNTO 命令错误', response, QMessageBox.Ok, QMessageBox.Ok)
                raise ValueError
            else:
                self.get_list()

    def quit(self):
        msg = 'QUIT\r\n'
        self.sock.send(msg.encode('utf-8'))
        response = self.get_response()
        if response[: 3] != '221':
            QMessageBox.warning(self, 'QUIT 命令错误', response, QMessageBox.Ok, QMessageBox.Ok)
        else:
            self.sock.close()
            self.list.clear()
            self.has_access = False

    def get_retr(self, file, path, listWidget, size):
        self.data_conn()
        msg = 'RETR ' + file + '\r\n'
        self.sock.send(msg.encode('utf-8'))
        f = open(path + '/' + file, 'wb')
        listItem = QProgressBar(self)
        listItem.setMinimum(0)
        listItem.setMaximum(int(size))
        listItem.setValue(0)
        listWidget.addWidget(listItem)
        response = self.get_response()
        if self.mode == 'active':
            data_sock, _ = self.data_sock.accept()
            self.data_sock.close()
            self.data_sock = data_sock
        while True:
            response = self.data_sock.recv(Client.MAX_LEN)
            if not response:
                break
            f.write(response)
            listItem.setValue(listItem.value() + len(response))
        self.data_sock.close()
        response = self.get_response()
        if response[: 3] == '150':
            if response.find('\r\n') != -1:
                response = response.split('\r\n')[1]
            else:
                response = self.get_response()
        if response[: 3] != '226':
            QMessageBox.warning(self, "RETR 命令错误", response, QMessageBox.Ok, QMessageBox.Ok)
