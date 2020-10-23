from PySide2.QtWidgets import *
from ui_dialog import Ui_Dialog


class Dialog(QDialog, Ui_Dialog):
    def __init__(self, client, category, old_name=None):
        self.client = client
        self.category = category
        self.old_name = old_name
        super(Dialog, self).__init__()
        self.setupUi(self)
        self.lineEdit.setText(old_name)
        with open("style.qss", "r") as qs:
            self.setStyleSheet(qs.read())
        if not old_name:
            self.setWindowTitle(u'请输入新建文件夹名')
        elif self.category:
            self.setWindowTitle(u'请输入新的文件夹名')
        else:
            self.setWindowTitle(u'请输入新的文件名')

    def accept(self):
        if self.lineEdit.text() == '' or self.lineEdit.text().find('/') != -1:
            if self.category:
                QMessageBox.warning(self, "文件夹名错误", u"文件夹名不得为空或含有 '/'", QMessageBox.Ok, QMessageBox.Ok)
            else:
                QMessageBox.warning(self, "文件名错误", u"文件名不得为空或含有 '/'", QMessageBox.Ok, QMessageBox.Ok)
        else:
            try:
                if self.category:
                    self.client.mkd(self.lineEdit.text())
                else:
                    self.client.get_rename(self.old_name, self.lineEdit.text())
                self.reject()
            except ValueError:
                pass
