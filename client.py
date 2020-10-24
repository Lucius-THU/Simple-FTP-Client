import re
import socket
import time
import ftplib
from PySide2.QtWidgets import *
from PySide2.QtCore import QThread, Signal

pattern = re.compile(r'(\d+),(\d+),(\d+),(\d+),(\d+),(\d+)', re.ASCII)


def parse(msg):
    if msg.find('\t') == -1:
        t = re.search(r'[A-Z][a-z]{2}[ \d:]{9}', msg)
        filename = msg[t.end() + 1:]
        edit_time = msg[t.start(): t.end()]
        msg = msg[: t.start() - 1]
        t = msg.rfind(' ')
        size = msg[t + 1:]
        return [filename, edit_time, size, msg[0] == 'd']
    else:
        t = msg.find('\t')
        filename = msg[t + 1:]
        msg = msg[: t]
        time_msg = msg[msg.find('m') + 1:]
        edit_time = time.localtime(int(time_msg[: time_msg.find(',')]))
        size_msg = msg[msg.find('s') + 1:]
        size = size_msg[: size_msg.find(',')]
        return [filename, time.strftime("%Y-%m-%d %H:%M:%S", edit_time), size, msg.find('/,') != -1]

class TransferFile(QThread):
    transfer_finished = Signal(str)
    transfer_happened = Signal(int)
    MAX_SIZE = 8192

    def __init__(self, sock, path, flag):
        super().__init__()
        self.sock = sock
        self.path = path
        self.flag = flag
        self.f = None

    def run(self):
        if self.flag == 'retr':
            self.retr()
        else:
            self.stor()
        self.sock.close()
        self.f.close()
        self.transfer_finished.emit(self.flag)

    def retr(self):
        self.f = open(self.path, 'wb')
        while True:
            response = self.sock.recv(Client.MAX_LEN)
            if not response:
                break
            self.f.write(response)
            self.transfer_happened.emit(len(response))

    def stor(self):
        self.f = open(self.path, 'rb')
        while True:
            data = self.f.read(TransferFile.MAX_SIZE)
            if not data:
                break
            self.sock.sendall(data)
            self.transfer_happened.emit(len(data))


class Client(QWidget):
    refresh = Signal()
    MAX_LEN = 8192
    CRLF = '\r\n'

    def __init__(self):
        super(Client, self).__init__()
        self.sock = None
        self.data_sock = None
        self.list = None
        self.root = ''
        self.mode = 'passive'
        self.bar = None
        self.has_access = False
        self.transfer_file = None

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

    def get_type(self):
        self.sock.send('TYPE I\r\n'.encode('utf-8'))
        response = self.get_response()
        if response[: 3] != '200':
            QMessageBox.warning(self, "TYPE 命令错误", response, QMessageBox.Ok, QMessageBox.Ok)

    def get_pasv(self):
        self.sock.send('PASV\r\n'.encode('utf-8'))
        response = self.get_response()
        if response[: 3] != '227':
            QMessageBox.warning(self, "PASV 命令错误", response, QMessageBox.Ok, QMessageBox.Ok)
        else:
            num = pattern.search(response).groups()
            host = '.'.join(num[: 4])
            port = (int(num[4]) << 8) + int(num[5])
            try:
                self.data_sock = socket.create_connection((host, port))
            except:
                pass

    def get_port(self):
        host = self.sock.getsockname()[0]
        self.data_sock = socket.create_server((host, 0), family=socket.AF_INET, backlog=1)
        host, port = self.data_sock.getsockname()[: 2]
        nums = host.split('.')
        nums.extend([str(port // 256), str(port % 256)])
        msg = 'PORT ' + ','.join(nums) + '\r\n'
        self.sock.send(msg.encode('utf-8'))
        response = self.get_response()
        if response[: 3] != '200':
            QMessageBox.warning(self, "PORT 命令错误", response, QMessageBox.Ok, QMessageBox.Ok)

    def data_conn(self):
        self.get_type()
        if self.mode == 'passive':
            self.get_pasv()
        else:
            self.get_port()

    def get_list(self):
        self.list = [['..', '', '', True]]
        try:
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
        except:
            pass

    def get_cwd(self, path):
        msg = 'CWD ' + path + '\r\n'
        try:
            self.sock.send(msg.encode('utf-8'))
            response = self.get_response()
            if response[: 3] != '200' and response[: 3] != '250':
                QMessageBox.warning(self, "CWD 命令错误", response, QMessageBox.Ok, QMessageBox.Ok)
        except:
            pass

    def get_mkd(self, dir_name):
        msg = 'MKD ' + dir_name + '\r\n'
        try:
            self.sock.send(msg.encode('utf-8'))
            response = self.get_response()
            if response[: 3] != '257':
                QMessageBox.warning(self, 'MKD 命令错误', response, QMessageBox.Ok, QMessageBox.Ok)
                raise ValueError
            else:
                self.get_list()
        except:
            pass

    def get_pwd(self):
        msg = 'PWD\r\n'
        try:
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
        except:
            pass

    def get_rmd(self, dir):
        msg = 'RMD ' + dir + '\r\n'
        try:
            self.sock.send(msg.encode('utf-8'))
            response = self.get_response()
            if response[: 3] != '250':
                QMessageBox.warning(self, 'RMD 命令错误', response, QMessageBox.Ok, QMessageBox.Ok)
            else:
                self.get_list()
        except:
            pass

    def get_rename(self, old_name, new_name):
        try:
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
        except:
            pass

    def quit(self):
        msg = 'QUIT\r\n'
        self.sock.send(msg.encode('utf-8'))
        response = self.get_response()
        if response[: 3] != '221':
            QMessageBox.warning(self, 'QUIT 命令错误', response, QMessageBox.Ok, QMessageBox.Ok)
            raise Exception
        else:
            self.sock.close()
            self.list.clear()
            self.has_access = False

    def get_retr(self, file, path, new_name):
        try:
            self.data_conn()
            msg = 'RETR ' + file + '\r\n'
            self.sock.send(msg.encode('utf-8'))
            if self.mode == 'active':
                data_sock, _ = self.data_sock.accept()
                self.data_sock.close()
                self.data_sock = data_sock
            self.transfer_file = TransferFile(self.data_sock, path + '/' + new_name, 'retr')
            self.transfer_file.transfer_finished.connect(self.finish_response)
            self.transfer_file.transfer_happened.connect(self.change_bar)
            self.transfer_file.start()
        except:
            pass

    def get_stor(self, file_name, new_name):
        try:
            self.data_conn()
            msg = 'STOR ' + new_name + '\r\n'
            self.sock.send(msg.encode('utf-8'))
            if self.mode == 'active':
                data_sock, _ = self.data_sock.accept()
                self.data_sock.close()
                self.data_sock = data_sock
            self.transfer_file = TransferFile(self.data_sock, file_name, 'stor')
            self.transfer_file.transfer_finished.connect(self.finish_response)
            self.transfer_file.transfer_happened.connect(self.change_bar)
            self.transfer_file.start()
        except:
            pass

    def change_bar(self, val):
        self.bar.setValue(self.bar.value() + val)

    def finish_response(self, flag):
        response = self.get_response()
        if response[: 3] == '150':
            if response.find('\r\n') != -1:
                response = response.split('\r\n')[1]
            else:
                response = self.get_response()
        if response[: 3] != '226':
            QMessageBox.warning(self, u"错误", response, QMessageBox.Ok, QMessageBox.Ok)
        else:
            if flag == 'stor':
                self.get_list()
                self.refresh.emit()
        self.bar.setVisible(False)

    def get_syst(self):
        msg = 'SYST\r\n'
        self.sock.send(msg.encode('utf-8'))
        response = self.get_response()
        if response[: 3] != '215':
            QMessageBox.warning(self, u"SYST 错误", response, QMessageBox.Ok, QMessageBox.Ok)
        else:
            QMessageBox.information(self, u"SYST", response, QMessageBox.Ok, QMessageBox.Ok)
