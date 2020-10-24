from PySide2.QtWidgets import *
from ui_dialog import Ui_Dialog
import os


class Dialog(QDialog, Ui_Dialog):
    def __init__(self, client, category, progress, old_name=None, direction=None, path=None):
        self.client = client
        self.category = category
        self.old_name = old_name
        self.direction = direction
        self.progress = progress
        self.path = path
        super(Dialog, self).__init__()
        self.setupUi(self)
        if not self.direction:
            self.lineEdit.setText(old_name)
        else:
            self.lineEdit.setText(os.path.basename(old_name))
        with open("style.qss", "r") as qs:
            self.setStyleSheet(qs.read())
        if not old_name:
            self.setWindowTitle(u'请输入新建文件夹名')
        elif self.category:
            self.setWindowTitle(u'请输入新的文件夹名')
        elif not direction:
            self.setWindowTitle(u'请输入新的文件名')
        elif self.direction == 'upload':
            self.setWindowTitle(u'请输入服务端保存的文件名')
        else:
            self.setWindowTitle(u'请输入本机保存的文件名')

    def accept(self):
        if self.lineEdit.text() == '' or self.lineEdit.text().find('/') != -1:
            if self.category:
                QMessageBox.warning(self, "文件夹名错误", u"文件夹名不得为空或含有 '/'", QMessageBox.Ok, QMessageBox.Ok)
            else:
                QMessageBox.warning(self, "文件名错误", u"文件名不得为空或含有 '/'", QMessageBox.Ok, QMessageBox.Ok)
        else:
            try:
                if not self.old_name:
                    self.client.get_mkd(self.lineEdit.text())
                elif not self.direction:
                    self.client.get_rename(self.old_name, self.lineEdit.text())
                elif self.direction == 'download':
                    self.progress.setVisible(True)
                    self.client.get_retr(self.old_name, self.path, self.lineEdit.text())
                else:
                    self.progress.setVisible(True)
                    self.client.get_stor(self.old_name, self.lineEdit.text())
                self.reject()
            except ValueError:
                pass
