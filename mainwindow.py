from PySide2.QtWidgets import *
from PySide2.QtCore import *
from PySide2.QtGui import QCursor
from ui_mainwindow import Ui_MainWindow
from connection import Connection
from client import Client
from dialog import Dialog
import os


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setupUi(self)
        self.temp = None
        self.mode_group = QActionGroup(self)
        self.mode_group.addAction(self.passive)
        self.mode_group.addAction(self.active)
        with open("style.qss", "r") as qs:
            self.setStyleSheet(qs.read())
        self.client = Client()
        self.client.refresh.connect(self.fill_table)
        self.client.bar = self.progressBar
        self.actionSYST.triggered.connect(self.send_SYST)
        self.progressBar.setVisible(False)
        self.passive.triggered.connect(self.client.switch_mode)
        self.active.triggered.connect(self.client.switch_mode)
        self.new_server.triggered.connect(self.start_conn)
        self.close_server.triggered.connect(self.close_conn)
        self.new_conn.clicked.connect(self.start_conn)
        self.tabWidget.setVisible(False)
        self.new_dir.triggered.connect(self.on_mkd_triggered)
        self.upload.triggered.connect(self.upload_file)
        self.file_list.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.file_list.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.file_list.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeToContents)
        self.file_list.horizontalHeader().setSectionResizeMode(QHeaderView.Interactive)
        self.file_list.horizontalHeader().setDefaultAlignment(Qt.AlignLeft)
        self.file_list.itemDoubleClicked.connect(self.double_click)
        self.file_list.setContextMenuPolicy(Qt.CustomContextMenu)
        self.file_list.customContextMenuRequested.connect(self.menu_show)
        self.table_menu = QMenu(self.file_list)
        self.open = QAction(u'打开', self.table_menu)
        self.open.triggered.connect(self.right_click_open)
        self.mkd = QAction(u'新建文件夹', self)
        self.mkd.triggered.connect(self.on_mkd_triggered)
        self.rmd = QAction(u'删除', self)
        self.rmd.triggered.connect(self.on_rmd_triggered)
        self.rename = QAction(u'重命名', self)
        self.rename.triggered.connect(self.on_rename_triggered)
        self.table_menu.addAction(self.open)
        self.table_menu.addAction(self.rmd)
        self.table_menu.addAction(self.rename)
        self.table_menu.addAction(self.mkd)
        self.about.triggered.connect(self.get_about)

    def get_about(self):
        QMessageBox.information(self, u"关于", 'FTP Client\r\nVer 1.0.0\r\nAuthor: Luo Cheng - 2018013013', QMessageBox.Ok, QMessageBox.Ok)

    def menu_show(self, _):
        flag = self.client.list[self.file_list.currentRow()][3]
        if flag:
            self.open.setText(u'打开')
        else:
            self.open.setText(u'下载')
        self.rmd.setVisible(flag and self.file_list.currentRow())
        self.table_menu.exec_(QCursor.pos())

    def right_click_open(self):
        self.double_click(self.file_list.currentItem())

    def on_rmd_triggered(self):
        item = self.file_list.item(self.file_list.currentItem().row(), 0)
        if self.client.list[item.row()][3]:
            self.client.get_rmd(item.text())
            self.fill_table()

    def on_rename_triggered(self):
        item = self.file_list.item(self.file_list.currentItem().row(), 0)
        dlg = Dialog(self.client, self.client.list[item.row()][3], self.progressBar, item.text())
        dlg.exec_()
        self.fill_table()

    def on_mkd_triggered(self):
        dlg = Dialog(self.client, True, self.progressBar)
        dlg.exec_()
        self.fill_table()

    def fill_table(self):
        self.file_list.clear()
        self.file_list.setHorizontalHeaderItem(0, QTableWidgetItem(u'名称'))
        self.file_list.setHorizontalHeaderItem(1, QTableWidgetItem(u'修改时间'))
        self.file_list.setHorizontalHeaderItem(2, QTableWidgetItem(u'大小(Bytes)'))
        self.file_list.setRowCount(len(self.client.list))
        icon_provider = QFileIconProvider()
        for i, item in enumerate(self.client.list):
            name = QTableWidgetItem(item[0])
            if item[3]:
                name.setIcon(icon_provider.icon(QFileIconProvider.Folder))
            else:
                name.setIcon(icon_provider.icon(QFileInfo(item[0])))
            self.file_list.setItem(i, 0, name)
            self.file_list.setItem(i, 1, QTableWidgetItem(item[1]))
            if not item[3]:
                self.file_list.setItem(i, 2, QTableWidgetItem(item[2]))

    def start_conn(self):
        dialog = Connection(self.client)
        dialog.exec_()
        if self.client.has_access:
            self.tabWidget.setVisible(True)
            self.new_conn.setVisible(False)
            self.new_server.setDisabled(True)
            self.close_server.setEnabled(True)
            self.fill_table()
            self.client.get_pwd()
            self.actionSYST.setEnabled(True)
            self.new_dir.setEnabled(True)
            self.upload.setEnabled(True)
            self.path.setText(u'当前路径：' + self.client.root)

    def close_conn(self):
        try:
            self.client.quit()
            self.new_server.setEnabled(True)
            self.new_conn.setVisible(True)
            self.tabWidget.setVisible(False)
            self.close_server.setEnabled(False)
            self.actionSYST.setEnabled(False)
            self.new_dir.setEnabled(False)
            self.upload.setEnabled(False)
        except Exception:
            pass

    def double_click(self, item):
        row = item.row()
        item = self.file_list.item(row, 0)
        if self.client.list[item.row()][3]:
            self.client.get_cwd(item.text())
            self.client.get_list()
            self.fill_table()
            self.client.get_pwd()
            self.path.setText(u'当前路径：' + self.client.root)
        else:
            path = self.temp
            if not path:
                path = QDir.homePath()
            dir_name = QFileDialog.getExistingDirectory(self, u'选择保存路径', path, QFileDialog.ShowDirsOnly | QFileDialog.DontResolveSymlinks)
            if dir_name:
                self.temp = dir_name
                self.progressBar.setMaximum(int(self.client.list[row][2]))
                self.progressBar.setValue(0)
                dlg = Dialog(self.client, False, self.progressBar, item.text(), 'download', self.temp)
                dlg.exec_()

    def upload_file(self):
        path = self.temp
        if not path:
            path = QDir.homePath()
        file_name = QFileDialog.getOpenFileName(self, u"选择上传文件", path, "All Files(*.*)")
        if file_name:
            self.temp = QDir(file_name[0]).path()
            self.progressBar.setMaximum(int(os.path.getsize(file_name[0])))
            self.progressBar.setValue(0)
            dlg = Dialog(self.client, False, self.progressBar, file_name[0], 'upload')
            dlg.exec_()

    def send_SYST(self):
        self.client.get_syst()

