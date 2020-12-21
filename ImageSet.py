from PyQt5.QtCore import QTimer, Qt,QRect,QSize,QRegExp,QBasicTimer,pyqtSignal,QDir
from PyQt5.QtGui import QColor, QPainter, QPainterPath, QPen,QPixmap,QIcon,QFont,QDoubleValidator
from PyQt5.QtWidgets import *
import requests
import os
import albumModel
import apiAll
import taskModel

class TabWidgetImages(QTabWidget):

    def __init__(self,tparms, *args, **kwargs):
        super(TabWidgetImages, self).__init__(*args, **kwargs)
        self.cwd = os.getcwd()  # 获取当前程序文件位置
        self.id = 1
        self.lines = []
        self.lines_album = []
        self.isStop = 0
        for i in range(4):
            if i == 0:
                self.imgListUpload = QWidget()
                conLayoutImgUpload = QGridLayout(self.imgListUpload)
                self.img_table = QTableWidget(self)
                self.img_table.setRowCount(0)
                self.img_table.setColumnCount(5)
                self.img_table.setParent(self.imgListUpload)
                self.img_table.setGeometry(0, 0, 530, 687)
                self.img_table.setEditTriggers(QAbstractItemView.DoubleClicked)
                self.img_table.verticalHeader().setVisible(False)
                self.img_table.setHorizontalHeaderLabels([u"ID",u"选择",u"图片路径", u"上传结果", u"图片url"])
                self.img_table.setColumnWidth(0, 25)
                self.img_table.setColumnWidth(1, 64)
                self.img_table.setColumnWidth(2, 309)
                self.img_table.setColumnWidth(3, 100)
                self.img_table.setColumnWidth(4, 350)

                self.img_table.setEditTriggers(QTableWidget.AnyKeyPressed)
                self.img_table.setEditTriggers(QAbstractItemView.NoEditTriggers)
                self.img_Option = QWidget()
                conLayoutImgOption = QGridLayout(self.img_Option)
                self.img_File = QPushButton(QIcon(""), u"选择文件", self.img_Option)
                self.img_File_Dir = QPushButton(QIcon(""), u"选择文件夹", self.img_Option)
                self.img_Clear_List = QPushButton(QIcon(""), u"清空列表", self.img_Option)
                self.img_Clear_List.clicked.connect(self.clearUpd)
                self.img_Delete_checked = QPushButton(QIcon(""), u"删除选中", self.img_Option)
                self.img_Delete_Fanchecked = QPushButton(QIcon(""), u"反选", self.img_Option)
                self.img_Delete_Allchecked = QPushButton(QIcon(""), u"全选", self.img_Option)

                self.img_File.clicked.connect(self.local_img)
                self.img_File_Dir.clicked.connect(self.local_imgDir)
                self.img_Delete_checked.clicked.connect(self.del_line)
                self.img_Delete_Allchecked.clicked.connect(self.Allchecked)
                self.img_Delete_Fanchecked.clicked.connect(self.Fanchecked)

                conLayoutImgOption.addWidget(self.img_File, 1, 1)
                conLayoutImgOption.addWidget(self.img_File_Dir, 1, 2)
                conLayoutImgOption.addWidget(self.img_Clear_List, 2, 1)
                conLayoutImgOption.addWidget(self.img_Delete_checked, 2, 2)
                conLayoutImgOption.addWidget(self.img_Delete_Fanchecked, 3, 1)
                conLayoutImgOption.addWidget(self.img_Delete_Allchecked, 3, 2)

                self.Album_Select = QWidget()
                self.WebAlbum = QLabel(self.Album_Select)
                self.WebAlbum.setText(u'网站相册')
                self.WebAlbum.setStyleSheet('max-width:60px;max-height:30px')
                conLayoutAlbumOption = QGridLayout(self.Album_Select)
                self.Album_Select_list = QComboBox(self.Album_Select)
                self.loading_album(tparms)
                self.Album_Select_Btn = QPushButton(QIcon(""), u"刷新", self.Album_Select)
                self.Album_Select_Btn.clicked.connect(lambda:self.loading_album(tparms))

                self.Album_add_Btn = QPushButton(QIcon(""), u"添加相册", self.Album_Select)
                self.Album_add_Btn.clicked.connect(lambda:self.add_album(tparms))

                conLayoutAlbumOption.addWidget(self.WebAlbum, 1, 1)
                conLayoutAlbumOption.addWidget(self.Album_Select_list, 1, 2)
                conLayoutAlbumOption.addWidget(self.Album_Select_Btn, 1, 3)
                conLayoutAlbumOption.addWidget(self.Album_add_Btn, 1, 4)

                self.Album_Select_Submit = QWidget()
                conLayoutAlbumSubmit = QGridLayout(self.Album_Select_Submit)
                self.Album_Submit_title = QPushButton(QIcon(""), u"将选中添加到“标题图片”",
                                                                self.Album_Select_Submit)
                self.Album_Submit_title.clicked.connect(lambda:self.addAlbum(tparms,1))

                self.Album_Submit_Random = QPushButton(QIcon(""), u"将选中添加到“随机图片”",
                                                                 self.Album_Select_Submit)
                self.Album_Submit_Random.clicked.connect(lambda:self.addAlbum(tparms,2))

                conLayoutAlbumSubmit.addWidget(self.Album_Submit_title, 1, 1)
                conLayoutAlbumSubmit.addWidget(self.Album_Submit_Random, 1, 2)

                self.Album_Select_Submit_Btn = QWidget()
                conLayoutAlbumSubmitBtn = QGridLayout(self.Album_Select_Submit_Btn)
                self.Album_Submit_Start = QPushButton(QIcon(""), u"开始上传",
                                                                self.Album_Select_Submit_Btn)
                self.Album_Submit_Start.clicked.connect(lambda:self.uploadImg(tparms))

                self.Album_Submit_Stop = QPushButton(QIcon(""), u"停止上传",
                                                               self.Album_Select_Submit_Btn)
                self.Album_Submit_Stop.clicked.connect(self.uploadStop)

                conLayoutAlbumSubmitBtn.addWidget(self.Album_Submit_Start, 1, 1)
                conLayoutAlbumSubmitBtn.addWidget(self.Album_Submit_Stop, 1, 2)

                conLayoutImgUpload.addWidget(self.img_table, 1, 1)
                conLayoutImgUpload.addWidget(self.img_Option, 2, 1)
                conLayoutImgUpload.addWidget(self.Album_Select, 3, 1)
                conLayoutImgUpload.addWidget(self.Album_Select_Submit, 4, 1)
                conLayoutImgUpload.addWidget(self.Album_Select_Submit_Btn, 5, 1)

                self.addTab(self.imgListUpload, str('上传图片'))

            elif i == 1:
                self.titleId = 1
                self.line_title = []
                self.imgListTitle = QWidget()
                conLayoutTitleList = QGridLayout(self.imgListTitle)
                self.imgListTitle_Left = QWidget(self.imgListTitle)
                self.imgListTitle_Left.setStyleSheet('max-height:50px;')
                self.imgListTitle_Info = QWidget(self.imgListTitle_Left)

                conLayoutImgTitleInfo = QGridLayout(self.imgListTitle_Info)
                self.imgListTitle_InfoCount = QLabel(self.imgListTitle_Info)
                self.imgListTitle_InfoCount.setText(u'共 0 张图片')
                self.imgListTitle_InfoClear = QPushButton(QIcon(""), u"清空",
                                                                    self.imgListTitle_Info)
                self.imgListTitle_InfoDelete = QPushButton(QIcon(""), u"删除选中",
                                                                     self.imgListTitle_Info)
                self.loading_title = QPushButton(QIcon(""), u"刷新",
                                                           self.imgListTitle_Info)

                self.imgListTitle_InfoClear.clicked.connect(self.clearTitleImgDel)
                self.imgListTitle_InfoDelete.clicked.connect(self.del_line_title)
                self.loading_title.clicked.connect(lambda:self.loadTitleImg(tparms))

                conLayoutImgTitleInfo.addWidget(self.imgListTitle_InfoCount, 1, 1)
                conLayoutImgTitleInfo.addWidget(self.imgListTitle_InfoClear, 1, 2)
                conLayoutImgTitleInfo.addWidget(self.imgListTitle_InfoDelete, 1, 3)
                conLayoutImgTitleInfo.addWidget(self.loading_title, 1, 4)

                self.title_list_table = QTableWidget()
                self.title_list_table.setRowCount(0)
                self.title_list_table.setColumnCount(3)
                self.title_list_table.setEditTriggers(QAbstractItemView.DoubleClicked)
                self.title_list_table.setHorizontalHeaderLabels([u"ID",u'选择',u"图片链接"])
                self.title_list_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
                self.title_list_table.horizontalHeader().setDefaultSectionSize(50)
                self.title_list_table.horizontalHeader().setSectionResizeMode(0, QHeaderView.Fixed)
                self.title_list_table.horizontalHeader().setSectionResizeMode(1, QHeaderView.Fixed)
                self.title_list_table.setEditTriggers(QTableWidget.AnyKeyPressed)
                self.title_list_table.clicked.connect(self.show_img_det_title)
                self.title_list_table.setEditTriggers(QAbstractItemView.NoEditTriggers)
                self.title_list_table.verticalHeader().setVisible(False)

                self.imgListTitle_Preview = QLabel(self)
                self.imgListTitle_Preview.setStyleSheet('max-width:500px;max-height:500px')

                self.imgListTitle_Preview_top = QWidget(self.imgListTitle)
                self.imgListTitle_Preview_top.setStyleSheet('max-height:50px')

                conLayoutTitleList.addWidget(self.imgListTitle_Info, 1, 1)
                conLayoutTitleList.addWidget(self.title_list_table, 2, 1)
                conLayoutTitleList.addWidget(self.imgListTitle_Preview, 2, 2)
                conLayoutTitleList.addWidget(self.imgListTitle_Preview_top, 1, 2)
                self.loadTitleImg(tparms)
                self.addTab(self.imgListTitle, str('标题图片'))

            elif i == 2:
                self.randomId = 1
                self.line_random = []

                self.imgListRandom = QWidget()
                conLayoutRandomList = QGridLayout(self.imgListRandom)
                self.imgListRandom_Left = QWidget(self.imgListRandom)
                self.imgListRandom_Left.setStyleSheet('max-height:50px;')
                self.imgListRandom_Info = QWidget(self.imgListRandom_Left)

                conLayoutImgRandomInfo = QGridLayout(self.imgListRandom_Info)
                self.imgListRandom_InfoCount = QLabel(self.imgListRandom_Info)
                self.imgListRandom_InfoCount.setText(u'共 0 张图片')
                self.imgListRandom_InfoClear = QPushButton(QIcon(""), u"清空",
                                                                     self.imgListRandom_Info)
                self.imgListRandom_InfoDelete = QPushButton(QIcon(""), u"删除选中",
                                                                      self.imgListRandom_Info)

                self.loading_random = QPushButton(QIcon(""), u"刷新",
                                                           self.imgListRandom_Info)

                self.imgListRandom_InfoClear.clicked.connect(self.clearRandomImgDel)
                self.imgListRandom_InfoDelete.clicked.connect(self.del_line_random)
                self.loading_random.clicked.connect(lambda:self.loadRandomImg(tparms))

                conLayoutImgRandomInfo.addWidget(self.imgListRandom_InfoCount, 1, 1)
                conLayoutImgRandomInfo.addWidget(self.imgListRandom_InfoClear, 1, 2)
                conLayoutImgRandomInfo.addWidget(self.imgListRandom_InfoDelete, 1,3)
                conLayoutImgRandomInfo.addWidget(self.loading_random, 1, 4)

                self.Random_list_table = QTableWidget(self)
                self.Random_list_table.setRowCount(0)
                self.Random_list_table.setColumnCount(3)
                self.Random_list_table.setEditTriggers(QAbstractItemView.DoubleClicked)
                self.Random_list_table.setHorizontalHeaderLabels([u"ID", u'选择', u"图片链接"])
                self.Random_list_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
                self.Random_list_table.horizontalHeader().setDefaultSectionSize(50)
                self.Random_list_table.horizontalHeader().setSectionResizeMode(0, QHeaderView.Fixed)
                self.Random_list_table.horizontalHeader().setSectionResizeMode(1, QHeaderView.Fixed)
                self.Random_list_table.setEditTriggers(QTableWidget.AnyKeyPressed)
                self.Random_list_table.clicked.connect(self.show_img_det_Random)
                self.Random_list_table.setEditTriggers(QAbstractItemView.NoEditTriggers)
                self.Random_list_table.verticalHeader().setVisible(False)

                self.imgListRandom_Preview = QLabel(self)
                self.imgListRandom_Preview.setStyleSheet('max-width:500px;max-height:500px')

                self.imgListRandom_Preview_top = QWidget(self.imgListRandom)
                self.imgListRandom_Preview_top.setStyleSheet('max-height:50px;')

                conLayoutRandomList.addWidget(self.imgListRandom_Info, 1, 1)
                conLayoutRandomList.addWidget(self.Random_list_table, 2, 1)
                conLayoutRandomList.addWidget(self.imgListRandom_Preview, 2, 2)
                conLayoutRandomList.addWidget(self.imgListRandom_Preview_top, 1, 2)
                self.loadRandomImg(tparms)
                self.addTab(self.imgListRandom, str('随机图片'))

            elif i == 3:
                self.albumId = 1
                self.albumImgId = 1

                self.line_album = []
                self.select_album = ''

                self.imgListAlbum = QWidget()
                conLayoutAlbumList = QGridLayout(self.imgListAlbum)
                self.imgListAlbum_Left = QWidget(self.imgListAlbum)
                self.imgListAlbum_Left.setStyleSheet('max-height:50px;')
                self.imgListAlbum_Info = QWidget(self.imgListAlbum_Left)

                self.tparms = tparms
                conLayoutImgAlbumInfo = QGridLayout(self.imgListAlbum_Info)
                self.imgListAlbum_InfoCount = QComboBox(self)
                self.imgListAlbum_InfoCount.activated[str].connect(self.loadAlbum)

                self.album_Delete_checked = QPushButton(QIcon(""), u"删除选中", self.imgListAlbum_Info)
                self.album_Delete_checked.clicked.connect(self.del_line_album)

                self.imgListAlbum_InfoClear = QPushButton(QIcon(""), u"刷新",
                                                                    self.imgListAlbum_Info)

                self.imgListAlbum_InfoClear.clicked.connect(lambda:self.loading_album2(tparms))
                self.imgListAlbum_InfoDelete = QLabel(self.imgListAlbum_Info)
                self.imgListAlbum_InfoDelete.setText(u'共 0 张图片')
                conLayoutImgAlbumInfo.addWidget(self.album_Delete_checked, 1, 1)
                conLayoutImgAlbumInfo.addWidget(self.imgListAlbum_InfoCount, 1, 2)
                conLayoutImgAlbumInfo.addWidget(self.imgListAlbum_InfoClear, 1, 3)
                conLayoutImgAlbumInfo.addWidget(self.imgListAlbum_InfoDelete, 1, 4)

                self.Album_list_table = QTableWidget(self)
                self.Album_list_table.setGeometry(0, 0, 400, 400)
                self.Album_list_table.setRowCount(0)
                self.Album_list_table.setColumnCount(3)
                self.Album_list_table.setEditTriggers(QAbstractItemView.DoubleClicked)
                self.Album_list_table.setHorizontalHeaderLabels([u"ID", u'选择', u"图片链接"])
                self.Album_list_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
                self.Album_list_table.horizontalHeader().setDefaultSectionSize(50)
                self.Album_list_table.horizontalHeader().setSectionResizeMode(0, QHeaderView.Fixed)
                self.Album_list_table.horizontalHeader().setSectionResizeMode(1, QHeaderView.Fixed)
                self.Album_list_table.setEditTriggers(QTableWidget.AnyKeyPressed)
                self.Album_list_table.clicked.connect(self.show_img_det_Album)
                self.Album_list_table.setEditTriggers(QAbstractItemView.NoEditTriggers)
                self.Album_list_table.verticalHeader().setVisible(False)

                self.imgListAlbum_Preview = QLabel(self)
                self.imgListAlbum_Preview_top = QWidget(self.imgListAlbum)
                self.imgListAlbum_Preview_top.setStyleSheet('max-height:50px;')
                self.imgListAlbum_Preview.setStyleSheet('max-width:500px;max-height:500px')

                self.img_Album_left = QWidget()
                self.img_Album_left.setStyleSheet('max-height:50px')
                conLayoutImgAlbum_left = QGridLayout(self.img_Album_left)
                self.img_File_Album = QPushButton(QIcon(""), u"保存", self.img_Album_left)

                self.img_File_Album.clicked.connect(lambda: self.saveAlbumImg(tparms))

                self.img_Clear_List_Album = QPushButton(QIcon(""), u"清空", self.img_Album_left)
                self.img_Clear_List_Album.clicked.connect(self.clearAlbumImg)
                self.img_allClicked_Album = QPushButton(QIcon(""), u"全选", self.img_Album_left)
                self.img_allClicked_Album.clicked.connect(self.AllcheckedAlbum)
                self.img_fanClicked_Album = QPushButton(QIcon(""), u"反选", self.img_Album_left)
                self.img_fanClicked_Album.clicked.connect(self.FancheckedAlbum)

                conLayoutImgAlbum_left.addWidget(self.img_File_Album, 1, 1)
                conLayoutImgAlbum_left.addWidget(self.img_Clear_List_Album, 1, 2)
                conLayoutImgAlbum_left.addWidget(self.img_allClicked_Album, 1, 3)
                conLayoutImgAlbum_left.addWidget(self.img_fanClicked_Album, 1, 4)

                self.img_Album_right = QWidget()
                conLayoutImgAlbum_right = QGridLayout(self.img_Album_right)
                self.Album_Submit_title = QPushButton(QIcon(""), u"将图片添加到 “标题图片”",
                                                                self.img_Album_right)
                self.Album_Submit_title.clicked.connect(lambda: self.addToAlbum(tparms,1))

                self.Album_Submit_Random = QPushButton(QIcon(""), u"将图片添加到 “随机图片”",
                                                                 self.img_Album_right)
                self.Album_Submit_Random.clicked.connect(lambda: self.addToAlbum(tparms,2))


                conLayoutImgAlbum_right.addWidget(self.Album_Submit_title, 1, 1)
                conLayoutImgAlbum_right.addWidget(self.Album_Submit_Random, 1, 2)

                conLayoutAlbumList.addWidget(self.imgListAlbum_Info, 1, 1)
                conLayoutAlbumList.addWidget(self.Album_list_table, 2, 1)
                conLayoutAlbumList.addWidget(self.imgListAlbum_Preview, 2, 2)
                conLayoutAlbumList.addWidget(self.imgListAlbum_Preview_top, 1, 2)

                conLayoutAlbumList.addWidget(self.img_Album_left, 3, 1)
                conLayoutAlbumList.addWidget(self.img_Album_right, 3, 2)

                self.loading_album2(tparms)

                self.addTab(self.imgListAlbum, str('相册图片'))

    def loadAlbum(self,s):
        self.clearAlbumImg()
        self.select_album = s
        self.lines_album = []
        try:
            albumInfo = albumModel.getDataOne(self.tparms['admin_id'], self.tparms['task_id'], str(s),self.tparms['config_id'])
            data = albumModel.albumImgData(self.tparms['admin_id'], self.tparms['task_id'], albumInfo['id'],self.tparms['config_id'])
            for info in data:
                ck = QCheckBox()
                h = QHBoxLayout()
                h.setAlignment(Qt.AlignCenter)
                h.addWidget(ck)
                w = QWidget()
                w.setLayout(h)

                row = self.Album_list_table.rowCount()
                self.Album_list_table.insertRow(row)
                self.Album_list_table.setItem(row, 0, QTableWidgetItem(str(self.albumId)))
                self.Album_list_table.setCellWidget(row, 1, w)
                self.Album_list_table.setItem(row, 2, QTableWidgetItem(apiAll.website+'/'+info['url']))
                self.lines_album.append([str(self.albumId), ck, apiAll.website+'/'+info['url']])

                self.albumId += 1

            self.imgListAlbum_InfoDelete.setText('共 '+str(len(data))+' 张图片')
        except Exception as e:
            print(e)
    def uploadStop(self):
        self.isStop = 1

    def clearUpd(self):
        try:
            row = self.img_table.rowCount()
            for x in range(row, 0, -1):
                self.img_table.removeRow(x - 1)
            self.lines = []
            reply = QMessageBox.information(self,
                                            "提示",
                                            "已清空",
                                            QMessageBox.Yes)
        except Exception as e:
            print(e)

    def uploadImg(self,tparms):
        try:
            tparms = taskModel.getTaskOne(tparms['task_id'])
            self.Album_Submit_Start.setDisabled(True)
            str2 = self.Album_Select_list.currentText()
            if len(str2) > 0:
                row = self.img_table.rowCount()
                if row > 0:
                    QMessageBox.information(self,
                                            "提示",
                                            "开始上传",
                                            QMessageBox.Yes)
                    albumInfo = albumModel.getDataOne(tparms['admin_id'], tparms['task_id'], str(str2),tparms['config_id'])
                    for x in range(row, 0, -1):
                        imgList = self.img_table.item(x - 1, 2).text()
                        status = self.img_table.item(x - 1, 3).text()
                        if self.isStop == 0:
                            if len(imgList)> 0 and status == '待上传':
                                try:
                                    if len(tparms['token']) == 0:
                                         msg_box = QMessageBox.information(self,
                                                      "警告",
                                                      "您还没登录",
                                                      QMessageBox.Yes)

                                    result = apiAll.uploadImg(tparms['token'],imgList)
                                    if result['errno'] == 0:
                                        url =result['data']['savePath']+result['data']['thumb']
                                        albumModel.addAlbumImg(tparms['admin_id'],url,tparms['task_id'],albumInfo['id'],tparms['config_id'])
                                        self.img_table.item(x - 1, 4).setText(url)
                                        self.img_table.item(x - 1, 3).setText('上传成功')
                                    else:
                                        msg_box = QMessageBox.information(self,
                                                                          "警告",
                                                                          "上传失败，请重新登录",
                                                                          QMessageBox.Yes)
                                except Exception as e:
                                    print(e)
                                    msg_box = QMessageBox.information(self,
                                                                        "警告",
                                                                        "您还没登录",
                                                                        QMessageBox.Yes)
                else:
                    msg_box = QMessageBox.information(self,
                                                  "警告",
                                                  "暂无图片可上传",
                                                  QMessageBox.Yes)
            else:
                msg_box = QMessageBox.information(self,
                                                  "警告",
                                                  "请选择相册",
                                                  QMessageBox.Yes)
        except Exception as e:
            print(e)
            msg_box = QMessageBox.information(self,
                                                "警告",
                                                "您还没登录",
                                                QMessageBox.Yes)
        self.Album_Submit_Start.setDisabled(False)

    def loadTitleImg(self,tparms):
        self.clearTitleImg()
        data = albumModel.titleImgData(tparms['admin_id'],tparms['task_id'],tparms['config_id'])
        for info in data:
            ck = QCheckBox()
            h = QHBoxLayout()
            h.setAlignment(Qt.AlignCenter)
            h.addWidget(ck)
            w = QWidget()
            w.setLayout(h)

            row = self.title_list_table.rowCount()
            self.title_list_table.insertRow(row)
            self.title_list_table.setItem(row, 0, QTableWidgetItem(str(self.titleId)))
            self.title_list_table.setCellWidget(row, 1, w)
            self.title_list_table.setItem(row, 2, QTableWidgetItem(apiAll.website+'/'+info['url']))

            self.line_title.append([str(self.titleId), ck, apiAll.website+'/'+info['url'],info['id']])
            self.titleId+=1

        self.imgListTitle_InfoCount.setText('共 '+str(len(data))+' 张图片')

    def loadRandomImg(self,tparms):
        self.clearRandomImg()
        data = albumModel.randomImgData(tparms['admin_id'],tparms['task_id'],tparms['config_id'])
        for info in data:
            # print(info)
            ck = QCheckBox()
            h = QHBoxLayout()
            h.setAlignment(Qt.AlignCenter)
            h.addWidget(ck)
            w = QWidget()
            w.setLayout(h)

            row = self.Random_list_table.rowCount()
            self.Random_list_table.insertRow(row)
            self.Random_list_table.setItem(row, 0, QTableWidgetItem(str(self.randomId)))
            self.Random_list_table.setCellWidget(row, 1, w)
            self.Random_list_table.setItem(row, 2, QTableWidgetItem(apiAll.website+'/'+info['url']))

            self.line_random.append([str(self.randomId), ck, apiAll.website+'/'+info['url'],info['id']])
            self.randomId+=1

        self.imgListRandom_InfoCount.setText('共 '+str(len(data))+' 张图片')

    def loadAlbumImg(self,tparms,str2):
        self.albumId = 1
        self.albumImgId = 1
        self.clearAlbumImg()
        self.lines_album = []
        if len(str2) == 0:
            str2 = self.Album_Select_list.currentText()
        albumInfo = albumModel.getDataOne(tparms['admin_id'], tparms['task_id'], str(str2),tparms['config_id'])

        data = albumModel.albumImgData(tparms['admin_id'],tparms['task_id'],albumInfo['id'],tparms['config_id'])
        for info in data:
            ck = QCheckBox()
            h = QHBoxLayout()
            h.setAlignment(Qt.AlignCenter)
            h.addWidget(ck)
            w = QWidget()
            w.setLayout(h)

            row = self.Album_list_table.rowCount()
            self.Album_list_table.insertRow(row)
            self.Album_list_table.setItem(row, 0, QTableWidgetItem(str(self.albumImgId)))
            self.Album_list_table.setCellWidget(row, 1, w)

            if apiAll.website+'/' not in info['url']:
                self.Album_list_table.setItem(row, 2, QTableWidgetItem(apiAll.website + '/' + info['url']))
                self.lines_album.append([str(self.albumImgId), ck, apiAll.website + '/' + info['url']])
            else:
                self.Album_list_table.setItem(row, 2, QTableWidgetItem(info['url']))
                self.lines_album.append([str(self.albumImgId), ck, info['url']])


            self.albumId+=1
            self.albumImgId+=1
        self.imgListAlbum_InfoDelete.setText('共 '+str(len(data))+' 张图片')

    def clearTitleImg(self):
        try:
            row = self.title_list_table.rowCount()
            for x in range(row, 0, -1):
                self.title_list_table.removeRow(x - 1)
            self.titleId = 1
            self.line_title = []
        except Exception as e:
            print(e)
    def clearTitleImgDel(self):
        try:
            row = self.title_list_table.rowCount()
            for x in range(row, 0, -1):
                self.title_list_table.removeRow(x - 1)
            self.titleId = 1
            self.line_title = []
            albumModel.delAlbumImgClear(1, self.tparms['admin_id'], self.tparms['task_id'], 0,self.tparms['config_id'])
            reply = QMessageBox.information(self,
                                            "提示",
                                            "已清空",
                                            QMessageBox.Yes)
        except Exception as e:
            print(e)
    def clearRandomImg(self):
        try:
            row = self.Random_list_table.rowCount()
            for x in range(row, 0, -1):
                self.Random_list_table.removeRow(x - 1)
            self.randomId = 1
            self.line_random = []
        except Exception as e:
            print(e)

    def clearRandomImgDel(self):
        try:
            row = self.Random_list_table.rowCount()
            for x in range(row, 0, -1):
                self.Random_list_table.removeRow(x - 1)
            self.randomId = 1
            self.line_random = []
            albumModel.delAlbumImgClear(2, self.tparms['admin_id'], self.tparms['task_id'], 0,self.tparms['config_id'])
            reply = QMessageBox.information(self,
                                            "提示",
                                            "已清空",
                                            QMessageBox.Yes)
        except Exception as e:
            print(e)
    def clearAlbumImg(self):
        try:
            row = self.Album_list_table.rowCount()
            for x in range(row, 0, -1):
                self.Album_list_table.removeRow(x - 1)
            self.albumId = 1
            self.line_album = []
        except Exception as e:
            print(e)

    def saveTitleImg(self,tparms,type):
        try:
            row = self.title_list_table.rowCount()
            new_list = []
            for x in range(row, 0, -1):
                new_list.append(self.title_list_table.item(x - 1, 2).text().replace(apiAll.website+'/',''))
            new_list.reverse()
            albumModel.addAlbumAll(tparms['admin_id'], new_list,0,tparms['task_id'],type,tparms['config_id'])
            reply = QMessageBox.information(self,
                                            "提示",
                                            "添加成功",
                                            QMessageBox.Yes)
        except Exception as e:
            print(e)

    def saveAlbumImg(self,tparms):
        try:
            self.select_album = self.imgListAlbum_InfoCount.currentText()
            albumInfo = albumModel.getDataOne(tparms['admin_id'], tparms['task_id'], str(self.select_album),tparms['config_id'])

            row = self.Album_list_table.rowCount()
            new_list = []
            for x in range(row, 0, -1):
                new_list.append(self.Album_list_table.item(x - 1, 2).text())
            albumModel.addAlbumAll(tparms['admin_id'], new_list,albumInfo['id'],tparms['task_id'],3,tparms['config_id'])
        except Exception as e:
            print(e)

    def saverRandomImg(self,tparms,type):
        try:
            row = self.Random_list_table.rowCount()
            new_list = []
            for x in range(row, 0, -1):
                new_list.append(self.Random_list_table.item(x - 1, 2).text().replace(apiAll.website+'/',''))
            new_list.reverse()
            albumModel.addAlbumAll(tparms['admin_id'], new_list,0,tparms['task_id'],type,tparms['config_id'])
        except Exception as e:
            print(e)

    def addAlbum(self,tparms,type):
        row = self.img_table.rowCount()
        new_list = []
        for x in range(row, 0, -1):
            if self.lines[x - 1][1].isChecked():
                new_list.append(self.img_table.item(x - 1, 4).text())

                if str(self.img_table.item(x - 1, 3).text()) in '待上传':
                    reply = QMessageBox.information(self,
                                                    "提示",
                                                    "请先上传图片",
                                                    QMessageBox.Yes)
                    return
        if len(new_list) == 0:
            reply = QMessageBox.information(self,
                                            "提示",
                                            "至少选择一项",
                                            QMessageBox.Yes)
            return
        albumModel.addAlbum(tparms['admin_id'], new_list,type,tparms['task_id'],tparms['config_id'])

        reply = QMessageBox.information(self,
                                            "提示",
                                            "添加成功",
                                            QMessageBox.Yes)
    def addToAlbum(self,tparms,type):
        try:
            row = self.Album_list_table.rowCount()
            new_list = []
            for x in range(row, 0, -1):
                if self.lines_album[x - 1][1].isChecked():
                    new_list.append(self.Album_list_table.item(x - 1, 2).text().replace(apiAll.website+'/',''))

            if len(new_list) == 0:
                reply = QMessageBox.information(self,
                                                "提示",
                                                "至少选择一项",
                                                QMessageBox.Yes)
                return
            albumModel.addAlbum(tparms['admin_id'], new_list, type, tparms['task_id'],tparms['config_id'])
            reply = QMessageBox.information(self,
                                            "提示",
                                            "添加成功",
                                            QMessageBox.Yes)
        except Exception as e:
            print(e)


    def loading_album(self,tparms):
        try:
            self.Album_Select_list.clear()
            albumList = albumModel.getDataList(tparms['admin_id'],tparms['task_id'],tparms['config_id'])
            if len(albumList) > 0:
                for info in albumList:
                    self.Album_Select_list.addItem(info['name'])
        except Exception as e:
            print(e)

    def loading_album2(self, tparms):
        try:
            text = self.imgListAlbum_InfoCount.currentText()
            self.imgListAlbum_InfoCount.clear()
            albumList = albumModel.getDataList(tparms['admin_id'], tparms['task_id'],tparms['config_id'])
            Num = 0
            for info in albumList:
                self.imgListAlbum_InfoCount.addItem(info['name'])
                if text in info['name']:
                    self.imgListAlbum_InfoCount.setCurrentIndex(Num)  # 设置默认值
                else:
                    Num += 1
                    continue

            self.loadAlbumImg(tparms,text)
        except Exception as e:
            print(e)

    def add_album(self,tparms):
        text, ok = QInputDialog.getText(self, '新建模板', '输入相册名称：')
        if ok and text:
            result = albumModel.getDataOne(tparms['admin_id'],tparms['task_id'],str(text),tparms['config_id'])
            if int(result['id']) > 0:
                msg_box = QMessageBox.information(self,
                                                  "警告",
                                                  "该名称已存在",
                                                  QMessageBox.Yes)
                return
            else:
                albumModel.addAlbumInfo(tparms['admin_id'],str(text),tparms['task_id'],tparms['config_id'])
                self.loading_album(tparms)
                pass


    def Allchecked(self):
        for line in self.lines:
            line[1].setChecked(True)

    def AllcheckedAlbum(self):
        for line in self.lines_album:
            line[1].setChecked(True)

    def FancheckedAlbum(self):
        for line in self.lines_album:
            if line[1].isChecked():
                line[1].setChecked(False)
            else:
                line[1].setChecked(True)

    def Fanchecked(self):
        for line in self.lines:
            if line[1].isChecked():
                line[1].setChecked(False)
            else:
                line[1].setChecked(True)

    def show_img_det_title(self,index):
        try:
            row_index = self.title_list_table.currentIndex().row()  # 获取当前行Index
            self.imgListTitle_img = QPixmap()
            imgListTitle_imgurl = self.title_list_table.item(row_index, 2).text()
            re_img = requests.get(imgListTitle_imgurl)
            self.imgListTitle_img.loadFromData(re_img.content)
            self.imgListTitle_Preview.setPixmap(self.imgListTitle_img)
            self.imgListTitle_Preview.setScaledContents(True)
        except Exception as e:
            print(e)

    def show_img_det_Random(self,index):
        try:
            row_index = self.Random_list_table.currentIndex().row()  # 获取当前行Index
            self.imgListRandom_img = QPixmap()
            imgListTitle_imgurl = self.Random_list_table.item(row_index, 2).text()
            re_img = requests.get(imgListTitle_imgurl)
            self.imgListRandom_img.loadFromData(re_img.content)
            self.imgListRandom_Preview.setPixmap(self.imgListRandom_img)
            self.imgListRandom_Preview.setScaledContents(True)
        except Exception as e:
            print(e)
    def show_img_det_Album(self, index):
        row_index = self.Album_list_table.currentIndex().row()  # 获取当前行Index
        self.imgListAlbum_img = QPixmap()
        imgListAlbum_imgurl = self.Album_list_table.item(row_index, 2).text()
        # print(imgListAlbum_imgurl)
        re_img = requests.get(imgListAlbum_imgurl)
        self.imgListAlbum_img.loadFromData(re_img.content)
        self.imgListAlbum_Preview.setPixmap(self.imgListAlbum_img)
        self.imgListAlbum_Preview.setScaledContents(True)

    def local_imgDir(self):
        dir_choose = QFileDialog.getExistingDirectory(self,
                                                      "选取文件夹",
                                                      self.cwd)  # 起始路径

        if dir_choose == "":
            return

        pathDir = os.listdir(dir_choose)
        for allDir in pathDir:
            url = dir_choose+'/'+allDir
            typejpg = url.endswith('.jpg')
            typepng = url.endswith('.png')
            typejpeg = url.endswith('.jpeg')

            if typejpg or typepng or typejpeg:
                fsize = os.path.getsize(url)
                f_kb = fsize / float(1024)
                if f_kb < 5120:
                    # 此处上传接口
                    ck = QCheckBox()
                    h = QHBoxLayout()
                    h.setAlignment(Qt.AlignCenter)
                    h.addWidget(ck)
                    w = QWidget()
                    w.setLayout(h)

                    row = self.img_table.rowCount()
                    self.img_table.insertRow(row)
                    self.img_table.setItem(row, 0, QTableWidgetItem(str(self.id)))
                    self.img_table.setCellWidget(row, 1, w)
                    self.img_table.setItem(row, 2, QTableWidgetItem(url))
                    self.img_table.setItem(row, 3, QTableWidgetItem('待上传'))
                    self.img_table.setItem(row, 4, QTableWidgetItem(url))
                    self.lines.append([str(self.id),ck, url])
                    self.id += 1
                else:
                    reply = QMessageBox.information(self,
                                                    "提示",
                                                    "文件大小不得大于5M",
                                                    QMessageBox.Yes)
    def del_line(self):
        try:
            removeline = []
            for line in self.lines:
                if line[1].isChecked():
                    row = self.img_table.rowCount()
                    for x in range(row,0,-1):
                        if line[0] == self.img_table.item(x - 1,0).text():
                            self.img_table.removeRow(x - 1)
                            removeline.append(line)
            if len(removeline) == 0:
                reply = QMessageBox.information(self,
                                                "提示",
                                                "至少选择一项",
                                                QMessageBox.Yes)
            else:
                for line in removeline:
                    self.lines.remove(line)
                reply = QMessageBox.information(self,
                                                "提示",
                                                "删除成功",
                                                QMessageBox.Yes)
        except Exception as e:
            print(e)


    def del_line_title(self):
        try:
            removeline = []
            removeId = []
            for line in self.line_title:
                if line[1].isChecked():
                    row = self.title_list_table.rowCount()
                    for x in range(row,0,-1):
                        if line[0] == self.title_list_table.item(x - 1,0).text():
                            self.title_list_table.removeRow(x - 1)
                            removeline.append(line)
                            removeId.append(line[3])
            if len(removeline) == 0:
                reply = QMessageBox.information(self,
                                                "提示",
                                                "至少选择一项",
                                                QMessageBox.Yes)
            else:
                for line in removeline:
                    self.line_title.remove(line)

                albumModel.delAlbumImg(removeId)
                reply = QMessageBox.information(self,
                                                "提示",
                                                "删除成功",
                                                QMessageBox.Yes)
        except Exception as e:
            print(e)

    def del_line_album(self):
        try:
            removeline = []
            # print(self.lines_album)
            for line in self.lines_album:
                if line[1].isChecked():
                    row = self.Album_list_table.rowCount()
                    for x in range(row,0,-1):
                        if line[0] == self.Album_list_table.item(x - 1,0).text():
                            self.Album_list_table.removeRow(x - 1)
                            removeline.append(line)
            if len(removeline) == 0:
                reply = QMessageBox.information(self,
                                                "提示",
                                                "请选择一项",
                                                QMessageBox.Yes)
            else:
                reply = QMessageBox.information(self,
                                                "提示",
                                                "删除成功",
                                                QMessageBox.Yes)
                for line in removeline:
                    self.lines_album.remove(line)
        except Exception as e:
            print(e)

    def del_line_random(self):
        try:
            removeline = []
            removeId = []
            for line in self.line_random:
                if line[1].isChecked():
                    row = self.Random_list_table.rowCount()
                    for x in range(row,0,-1):
                        if line[0] == self.Random_list_table.item(x - 1,0).text():
                            self.Random_list_table.removeRow(x - 1)
                            removeline.append(line)
                            removeId.append(line[3])
            if len(removeline) == 0:
                reply = QMessageBox.information(self,
                                                "提示",
                                                "至少选择一项",
                                                QMessageBox.Yes)
            else:
                reply = QMessageBox.information(self,
                                                "提示",
                                                "删除成功",
                                                QMessageBox.Yes)
                for line in removeline:
                    self.line_random.remove(line)
                albumModel.delAlbumImg(removeId)
        except Exception as e:
            print(e)

    def local_img(self):
        files, ok1 =QFileDialog.getOpenFileNames(self, "打开图片", "", "*.jpg;*.png;*.gif;;All Files(*)")

        for url in files:
            typejpg = url.endswith('.jpg')
            typepng = url.endswith('.png')
            typejpeg = url.endswith('.jpeg')
            typegif = url.endswith('.gif')

            if typejpg or typepng or typejpeg or typegif:
                fsize = os.path.getsize(url)
                f_kb = fsize / float(1024)
                if f_kb < 5120:
                    # 此处上传接口
                    ck = QCheckBox()
                    h = QHBoxLayout()
                    h.setAlignment(Qt.AlignCenter)
                    h.addWidget(ck)
                    w = QWidget()
                    w.setLayout(h)

                    row = self.img_table.rowCount()
                    self.img_table.insertRow(row)
                    self.img_table.setItem(row, 0, QTableWidgetItem(str(self.id)))
                    self.img_table.setCellWidget(row, 1, w)
                    self.img_table.setItem(row, 2, QTableWidgetItem(url))
                    self.img_table.setItem(row, 3, QTableWidgetItem('待上传'))
                    self.img_table.setItem(row, 4, QTableWidgetItem(url))
                    self.lines.append([str(self.id),ck, url])
                    self.id += 1
                else:
                    reply = QMessageBox.information(self,
                                                    "提示",
                                                    "文件大小不得大于5M",
                                                    QMessageBox.Yes)