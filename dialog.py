from PySide2.QtWidgets import *
from ui_dialog import Ui_Dialog
import os


class Dialog(QDialog, Ui_Dialog):
    def __init__(self, client, category, progress, old_name=None, direction=None, path=None):
        self.client = client
        self.category = category # category == True 表示待操作的是文件夹而非文件
        self.old_name = old_name # 重命名时先显示旧名
        self.direction = direction # 上传或下载，说明方向
        self.progress = progress # 文件传输需要让进度条可见
        self.path = path
        super(Dialog, self).__init__()
        self.setupUi(self)
        if not self.direction:
            self.lineEdit.setText(old_name)
        else:
            self.lineEdit.setText(os.path.basename(old_name))
        with open("style.qss", "r") as qs:
            self.setStyleSheet(qs.read())
        if not old_name: # 处理新建文件夹的情形
            self.setWindowTitle(u'请输入新建文件夹名')
        elif self.category: # 处理重命名文件夹的情形
            self.setWindowTitle(u'请输入新的文件夹名')
        elif not direction: # 处理重命名文件的情形
            self.setWindowTitle(u'请输入新的文件名')
        elif self.direction == 'upload': # 处理上传文件明命名的情形
            self.setWindowTitle(u'请输入服务端保存的文件名')
        else: # 处理下载文件命名的情形
            self.setWindowTitle(u'请输入本机保存的文件名')

    def accept(self):
        if self.lineEdit.text() == '' or self.lineEdit.text().find('/') != -1:
            if self.category:
                QMessageBox.warning(self, "文件夹名错误", u"文件夹名不得为空或含有 '/'", QMessageBox.Ok, QMessageBox.Ok)
            else:
                QMessageBox.warning(self, "文件名错误", u"文件名不得为空或含有 '/'", QMessageBox.Ok, QMessageBox.Ok)
        else:
            try:
                if not self.old_name: # 新建文件夹
                    self.client.get_mkd(self.lineEdit.text())
                elif not self.direction: # 重命名
                    self.client.get_rename(self.old_name, self.lineEdit.text())
                elif self.direction == 'download': # 下载
                    self.progress.setVisible(True)
                    self.client.get_retr(self.old_name, self.path, self.lineEdit.text())
                else: # 上传
                    self.progress.setVisible(True)
                    self.client.get_stor(self.old_name, self.lineEdit.text())
                self.reject()
            except ValueError:
                pass
