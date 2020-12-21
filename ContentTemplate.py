from PyQt5.QtCore import Qt,QRect,QSize,pyqtSlot,QObject,QUrl,QMetaObject
from PyQt5.QtGui import QIcon,QTextCursor
from PyQt5.QtWidgets import *
from qtpy import QtWidgets
from PyQt5.QtWebChannel import QWebChannel
from PyQt5.QtWebEngineWidgets import QWebEngineView
from concurrent.futures import ThreadPoolExecutor
import json
import sys
import contentModel
import sentenceModel
import re
import sip
import requests
from lxml import etree
import optionModel
import time

class CallHandler(QObject):

    def __init__(self):
        super(CallHandler, self).__init__()

    def getInfo(self):
        import socket, platform
        hostname = socket.gethostname()
        ip = socket.gethostbyname(hostname)
        list_info = platform.uname()
        sys_name = list_info[0] + list_info[2]
        cpu_name = list_info[5]
        dic_info = {"hostname": hostname, "ip": ip, "sys_name": sys_name, \
                    "cpu_name": cpu_name}
        return json.dumps(dic_info)

class Content(QTabWidget):

    def __init__(self,tparms, *args, **kwargs):
        super(Content, self).__init__(*args, **kwargs)

        self.tparms = tparms
        self.data = contentModel.getDataList(tparms['admin_id'],tparms['task_id'],tparms['config_id'])
        self.isdeleteLoad = 0


        self.ImgSet = QtWidgets.QWidget(self)


        layout = QtWidgets.QHBoxLayout(self.ImgSet)

        self.listWidgetImg = QtWidgets.QListWidget(self.ImgSet)
        self.listWidgetImg.setStyleSheet('min-width: 142px;max-width: 142px;max-height:570px')

        layout.addWidget(self.listWidgetImg)

        self.stackedWidgetImg = QtWidgets.QStackedWidget(self.ImgSet)

        layout.addWidget(self.stackedWidgetImg)

        self.listWidgetImg.currentRowChanged.connect(
            self.stackedWidgetImg.setCurrentIndex)
        # 去掉边框
        self.listWidgetImg.setFrameShape(QtWidgets.QListWidget.NoFrame)
        # 隐藏滚动条
        self.listWidgetImg.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.listWidgetImg.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        # 这里就用一般的文本配合图标模式了(也可以直接用Icon模式,setViewMode)
        self.nowContent = ''
        self.nowInfo = []
        createVarBt = locals()
        self.number = 0
        self.firstLoad = 0
        self.listall = []
        try:
            self.createVarView = locals()
            self.item = locals()
            self.deleteTemplate = locals()
            self.TemplateLabel_Name = locals()
            self.buttonVarParagraph = locals()
            self.imgListUpload = locals()

            if len(self.data) == 0:
                name = '新建模板'
                contentModel.addOtherContent(name,'',self.tparms['admin_id'],self.tparms['task_id'],self.tparms['config_id'])
                data = contentModel.getDataNameInfo(name, self.tparms['admin_id'], self.tparms['task_id'],self.tparms['config_id'])
                self.data.append({'id': data[0], 'name': data[1], 'status': 0, 'old_name': data[1]})

            for info in self.data:
                self.item['it{}'.format(info['name'])] = QtWidgets.QListWidgetItem(QIcon(), str(info['name']),
                                                 self.listWidgetImg)
                self.item['it{}'.format(info['name'])].setSizeHint(QSize(16777215, 60))
                # 文字居中
                self.item['it{}'.format(info['name'])].setTextAlignment(Qt.AlignCenter)

                self.imgListUpload['nmBox_{}'.format(info['name'])] = QWidget()
                conLayoutGoType_Contect = QGridLayout()
                self.imgListUpload['nmBox_{}'.format(info['name'])].setLayout(conLayoutGoType_Contect)

                self.imgListUploadTop = QLabel()
                self.imgListUploadTop.setFixedHeight(50)
                conLayoutGoType_Top = QGridLayout()
                self.imgListUploadTop.setLayout(conLayoutGoType_Top)

                self.TemplateLabel = QLabel(self.imgListUpload['nmBox_{}'.format(info['name'])])
                self.TemplateLabel.setText('模板名称')
                self.TemplateLabel.setStyleSheet('min-width:88px;')
                self.TemplateLabel.setFixedHeight(32)

                self.TemplateLabel_Name['nm_{}'.format(info['name'])] = QLineEdit(u"", self.ImgSet)
                self.TemplateLabel_Name['nm_{}'.format(info['name'])].setPlaceholderText(str(info['name']))
                self.TemplateLabel_Name['nm_{}'.format(info['name'])].setFocusPolicy(Qt.NoFocus)
                self.TemplateLabel_Name['nm_{}'.format(info['name'])].setStyleSheet(
                    'min-width:134px;min-height:25px')
                self.TemplateLabel_Name['nm_{}'.format(info['name'])].setFixedHeight(25)
                conLayoutGoType_Top.addWidget(self.TemplateLabel, 1, 1)
                conLayoutGoType_Top.addWidget(self.TemplateLabel_Name['nm_{}'.format(info['name'])], 1, 2)

                self.saveTemplate = QtWidgets.QPushButton(QIcon(""), u"保存", self.ImgSet)
                self.saveTemplate.clicked.connect(self.saveTemplateDo)
                self.saveTemplate.setStyleSheet('min-width:75px;')
                self.saveTemplate.setFixedHeight(30)
                conLayoutGoType_Top.addWidget(self.saveTemplate, 1, 3)

                self.saveTemplate_other = QtWidgets.QPushButton(QIcon(""), u"另存为新模板", self.ImgSet)
                self.saveTemplate_other.setStyleSheet('min-width:95px;')
                self.saveTemplate_other.clicked.connect(self.saveOtherTemp)
                self.saveTemplate_other.setFixedHeight(30)
                conLayoutGoType_Top.addWidget(self.saveTemplate_other, 1, 4)

                self.deleteTemplate['{}'.format(info['name'])] = QtWidgets.QPushButton(QIcon(""), u"删除",
                                                                                       self.ImgSet)
                self.deleteTemplate['{}'.format(info['name'])].clicked.connect(
                    lambda: self.deleteTemp(self.item['it{}'.format(info['name'])]))
                self.deleteTemplate['{}'.format(info['name'])].setStyleSheet('min-width:75px;')
                self.deleteTemplate['{}'.format(info['name'])].setFixedHeight(30)

                conLayoutGoType_Top.addWidget(self.deleteTemplate['{}'.format(info['name'])], 1, 5)

                self.newSaveTemplate = QtWidgets.QPushButton(QIcon(""), u"新建", self.ImgSet)
                self.newSaveTemplate.clicked.connect(self.newAddTemplate)
                self.newSaveTemplate.setFixedHeight(30)
                self.newSaveTemplate.setStyleSheet('min-width:75px;')
                conLayoutGoType_Top.addWidget(self.newSaveTemplate, 1, 6)

                self.reNameTemplate = QtWidgets.QPushButton(QIcon(""), u"重命名", self.ImgSet)
                self.reNameTemplate.setStyleSheet('min-width:75px;')
                self.reNameTemplate.clicked.connect(self.reDoNameTemplate)
                self.reNameTemplate.setFixedHeight(30)
                conLayoutGoType_Top.addWidget(self.reNameTemplate, 1, 7)

                conLayoutGoType_Contect.addWidget(self.imgListUploadTop, 1, 1,1,12)
                self.createVarView['{}'.format(info['name'])] = QWebEngineView()
                self.createVarView['{}'.format(info['name'])].setParent(self)
                self.createVarView['{}'.format(info['name'])].setFixedHeight(550)
                channel = QWebChannel()
                handler = CallHandler()  # 实例化QWebChannel的前端处理对象
                channel.registerObject('PyHandler', handler)  # 将前端处理对象在前端页面中注册为名PyHandler对象，此对象在前端访问时名称即为PyHandler'
                self.createVarView['{}'.format(info['name'])].page().setWebChannel(channel)  # 挂载前端处理对象
                self.createVarView['{}'.format(info['name'])].load(QUrl('http://123.133.86.56:8081/xxfb_up/fwb/'))
                conLayoutGoType_Contect.addWidget(self.createVarView['{}'.format(info['name'])], 2, 1,1,12)

                self.btnContect = QLabel()
                conLayoutGoType_Btn = QGridLayout()
                self.btnContect.setLayout(conLayoutGoType_Btn)
                self.btnContect.setFixedHeight(40)
                self.btnContect.setParent(self.imgListUpload['nmBox_{}'.format(info['name'])])
                self.btnContectTitle = QPushButton(QIcon(""), u"标题", self.btnContect)
                self.btnContectTitle.setParent(self.btnContect)
                self.btnContectTitle.setGeometry(QRect(0, 0, 50, 30))
                self.btnContectTitle.setStyleSheet('min-width:50px;min-height:30px')
                self.btnContectTitle.clicked.connect(lambda: self.goText('【标题】'))
                conLayoutGoType_Btn.addWidget(self.btnContectTitle, 1, 1)

                self.buttonZhu = QPushButton(QIcon(""), u"主变量", self.btnContect)
                self.buttonZhu.setParent(self.btnContect)
                self.buttonZhu.setGeometry(QRect(60, 0, 50, 30))
                self.buttonZhu.setStyleSheet('min-width:50px;min-height:30px')
                self.buttonZhu.clicked.connect(lambda: self.goText('【主变量】'))
                conLayoutGoType_Btn.addWidget(self.buttonZhu, 1, 2)

                self.buttonVar1 = QPushButton(QIcon(""), u"变量1", self.btnContect)
                self.buttonVar1.setParent(self.btnContect)
                self.buttonVar1.setGeometry(QRect(120, 0, 50, 30))
                self.buttonVar1.setStyleSheet('min-width:50px;min-height:30px')
                self.buttonVar1.clicked.connect(lambda: self.goText('【变量1】'))
                conLayoutGoType_Btn.addWidget(self.buttonVar1, 1, 3)

                self.buttonVar2 = QPushButton(QIcon(""), u"变量2", self.btnContect)
                self.buttonVar2.setParent(self.btnContect)
                self.buttonVar2.setGeometry(QRect(180, 0, 50, 30))
                self.buttonVar2.setStyleSheet('min-width:50px;min-height:30px')
                self.buttonVar2.clicked.connect(lambda: self.goText('【变量2】'))
                conLayoutGoType_Btn.addWidget(self.buttonVar2, 1, 4)

                self.buttonVar3 = QPushButton(QIcon(""), u"变量3", self.btnContect)
                self.buttonVar3.setParent(self.btnContect)
                self.buttonVar3.setGeometry(QRect(240, 0, 50, 30))
                self.buttonVar3.setStyleSheet('min-width:50px;min-height:30px')
                self.buttonVar3.clicked.connect(lambda: self.goText('【变量3】'))
                conLayoutGoType_Btn.addWidget(self.buttonVar3, 1, 5)

                self.buttonImgVar = QPushButton(QIcon(""), u"图片", self.btnContect)
                self.buttonImgVar.setParent(self.btnContect)
                self.buttonImgVar.setGeometry(QRect(300, 0, 50, 30))
                self.buttonImgVar.setStyleSheet('min-width:50px;min-height:30px')
                self.buttonImgVar.clicked.connect(lambda: self.goText('【图片】'))
                conLayoutGoType_Btn.addWidget(self.buttonImgVar, 1, 6)

                self.buttonVarSen = QPushButton(QIcon(""), u"句子", self.btnContect)
                self.buttonVarSen.setParent(self.btnContect)
                self.buttonVarSen.setGeometry(QRect(360, 0, 50, 30))
                self.buttonVarSen.setStyleSheet('min-width:50px;min-height:30px')
                self.buttonVarSen.clicked.connect(lambda: self.goText('【句子】'))
                conLayoutGoType_Btn.addWidget(self.buttonVarSen, 1, 7)

                self.buttonVarParagraph['pag{}'.format(info['name'])] = QtWidgets.QComboBox(self)
                self.buttonVarParagraph['pag{}'.format(info['name'])].setParent(self.btnContect)
                self.buttonVarParagraph['pag{}'.format(info['name'])].setGeometry(QRect(420, 0, 50, 0))
                self.buttonVarParagraph['pag{}'.format(info['name'])].setStyleSheet(
                    "max-width:80px;width:80px;min-width:80px")
                self.buttonVarParagraph['pag{}'.format(info['name'])].setFixedHeight(30)
                self.buttonVarParagraph['pag{}'.format(info['name'])].setView(QListView())
                self.buttonVarParagraph['pag{}'.format(info['name'])].activated[str].connect(
                    self.WrittingNotOfOther)
                conLayoutGoType_Btn.addWidget(self.buttonVarParagraph['pag{}'.format(info['name'])], 1, 8)

                self.buttonVarSen = QPushButton(QIcon(""), u"设置段落", self.btnContect)
                self.buttonVarSen.setParent(self.btnContect)
                self.buttonVarSen.setGeometry(QRect(520, 0, 70, 30))
                self.buttonVarSen.setStyleSheet('min-width:50px;min-height:30px')
                self.buttonVarSen.clicked.connect(self.setDuan)
                conLayoutGoType_Btn.addWidget(self.buttonVarSen, 1, 9)

                conLayoutGoType_Contect.addWidget(self.btnContect, 3, 1,1,12)

                self.stackedWidgetImg.addWidget(self.imgListUpload['nmBox_{}'.format(info['name'])])

                if self.number == 0:
                    self.itemActivated_event(self.item['it{}'.format(info['name'])])
                self.number+=1

            for info in self.data:
                self.createVarView['{}'.format(info['name'])].setVisible(True)

            self.listWidgetImg.itemClicked.connect(self.itemActivated_event)

        except Exception as e:
            print(e)
        self.loading_album()
        self.setLayout(layout)

    def addTemplate(self,name):
        try:
            self.item['it2{}'.format(name)] = QtWidgets.QListWidgetItem(QIcon(), str(name),
                                             self.listWidgetImg)
            self.item['it2{}'.format(name)].setSizeHint(QSize(16777215, 60))
            # 文字居中
            self.item['it2{}'.format(name)].setTextAlignment(Qt.AlignCenter)

            self.imgListUpload['nmBox_{}'.format(name)] = QWidget()
            conLayoutGoType_Contect = QGridLayout()
            self.imgListUpload['nmBox_{}'.format(name)].setLayout(conLayoutGoType_Contect)

            self.TemplateLabel = QLabel(self.imgListUpload['nmBox_{}'.format(name)])
            self.TemplateLabel.setText('模板名称')
            self.TemplateLabel.setStyleSheet('min-width:88px;min-height:32px')
            self.TemplateLabel_Name['nm_{}'.format(name)] = QLineEdit(u"", self.ImgSet)
            self.TemplateLabel_Name['nm_{}'.format(name)].setFocusPolicy(Qt.NoFocus)
            self.TemplateLabel_Name['nm_{}'.format(name)].setStyleSheet('min-width:134px;min-height:25px')
            conLayoutGoType_Contect.addWidget(self.TemplateLabel, 1, 1)
            conLayoutGoType_Contect.addWidget(self.TemplateLabel_Name['nm_{}'.format(name)], 1, 2)

            self.saveTemplate = QtWidgets.QPushButton(QIcon(""), u"保存", self.ImgSet)
            self.saveTemplate.clicked.connect(self.saveTemplateDo)
            self.saveTemplate.setStyleSheet('min-width:75px;min-height:30px')
            conLayoutGoType_Contect.addWidget(self.saveTemplate, 1, 3)

            self.saveTemplate_other = QtWidgets.QPushButton(QIcon(""), u"另存为新模板", self.ImgSet)
            self.saveTemplate_other.setStyleSheet('min-width:95px;min-height:30px')
            self.saveTemplate_other.clicked.connect(self.saveOtherTemp)
            conLayoutGoType_Contect.addWidget(self.saveTemplate_other, 1, 4)

            self.deleteTemplate['{}'.format(name)] = QtWidgets.QPushButton(QIcon(""), u"删除",
                                                                                   self.ImgSet)

            self.deleteTemplate['{}'.format(name)].clicked.connect(
                lambda: self.deleteTempNew(self.item['it2{}'.format(name)]))
            self.deleteTemplate['{}'.format(name)].setStyleSheet('min-width:75px;min-height:30px')
            conLayoutGoType_Contect.addWidget(self.deleteTemplate['{}'.format(name)], 1, 5)

            self.newSaveTemplate = QtWidgets.QPushButton(QIcon(""), u"新建", self.ImgSet)
            self.newSaveTemplate.clicked.connect(self.newAddTemplate)
            self.newSaveTemplate.setStyleSheet('min-width:75px;min-height:30px')
            conLayoutGoType_Contect.addWidget(self.newSaveTemplate, 1, 6)

            self.reNameTemplate = QtWidgets.QPushButton(QIcon(""), u"重命名", self.ImgSet)
            self.reNameTemplate.setStyleSheet('min-width:75px;min-height:30px')
            self.reNameTemplate.clicked.connect(self.reDoNameTemplateNew)
            conLayoutGoType_Contect.addWidget(self.reNameTemplate, 1, 7)

            self.createVarView['{}'.format(name)] = QWebEngineView()
            self.createVarView['{}'.format(name)].setParent(self)
            self.createVarView['{}'.format(name)].setStyleSheet('min-height:600px;')
            channel = QWebChannel()
            handler = CallHandler()  # 实例化QWebChannel的前端处理对象
            channel.registerObject('PyHandler', handler)
            self.createVarView['{}'.format(name)].page().setWebChannel(channel)  # 挂载前端处理对象
            self.createVarView['{}'.format(name)].load(QUrl('http://123.133.86.56:8081/xxfb_up/fwb/'))
            conLayoutGoType_Contect.addWidget(self.createVarView['{}'.format(name)], 2, 1, 1, 12)

            self.btnContect = QLabel()
            self.btnContect.setStyleSheet('min-height:32px')
            self.btnContect.setParent(self.imgListUpload['nmBox_{}'.format(name)])
            self.btnContectTitle = QPushButton(QIcon(""), u"标题", self.btnContect)
            self.btnContectTitle.setParent(self.btnContect)
            self.btnContectTitle.setGeometry(QRect(0, 0, 50, 30))
            self.btnContectTitle.setStyleSheet('min-width:50px;min-height:30px')
            self.btnContectTitle.clicked.connect(lambda: self.goText('【标题】'))
            self.btnContect.setStyleSheet('min-height:30px')

            self.buttonZhu = QPushButton(QIcon(""), u"主变量", self.btnContect)
            self.buttonZhu.setParent(self.btnContect)
            self.buttonZhu.setGeometry(QRect(60, 0, 50, 30))
            self.buttonZhu.setStyleSheet('min-width:50px;min-height:30px')
            self.buttonZhu.clicked.connect(lambda: self.goText('【主变量】'))

            self.buttonVar1 = QPushButton(QIcon(""), u"变量1", self.btnContect)
            self.buttonVar1.setParent(self.btnContect)
            self.buttonVar1.setGeometry(QRect(120, 0, 50, 30))
            self.buttonVar1.setStyleSheet('min-width:50px;min-height:30px')
            self.buttonVar1.clicked.connect(lambda: self.goText('【变量1】'))

            self.buttonVar2 = QPushButton(QIcon(""), u"变量2", self.btnContect)
            self.buttonVar2.setParent(self.btnContect)
            self.buttonVar2.setGeometry(QRect(180, 0, 50, 30))
            self.buttonVar2.setStyleSheet('min-width:50px;min-height:30px')
            self.buttonVar2.clicked.connect(lambda: self.goText('【变量2】'))

            self.buttonVar3 = QPushButton(QIcon(""), u"变量3", self.btnContect)
            self.buttonVar3.setParent(self.btnContect)
            self.buttonVar3.setGeometry(QRect(240, 0, 50, 30))
            self.buttonVar3.setStyleSheet('min-width:50px;min-height:30px')
            self.buttonVar3.clicked.connect(lambda: self.goText('【变量3】'))

            self.buttonImgVar = QPushButton(QIcon(""), u"图片", self.btnContect)
            self.buttonImgVar.setParent(self.btnContect)
            self.buttonImgVar.setGeometry(QRect(300, 0, 50, 30))
            self.buttonImgVar.setStyleSheet('min-width:50px;min-height:30px')
            self.buttonImgVar.clicked.connect(lambda: self.goText('【图片】'))

            self.buttonVarSen = QPushButton(QIcon(""), u"句子", self.btnContect)
            self.buttonVarSen.setParent(self.btnContect)
            self.buttonVarSen.setGeometry(QRect(360, 0, 50, 30))
            self.buttonVarSen.setStyleSheet('min-width:50px;min-height:30px')
            self.buttonVarSen.clicked.connect(lambda: self.goText('【句子】'))
            self.buttonVarParagraph['pag{}'.format(name)] = QtWidgets.QComboBox(self)
            self.buttonVarParagraph['pag{}'.format(name)].setParent(self.btnContect)
            self.buttonVarParagraph['pag{}'.format(name)].setGeometry(QRect(420, 0, 50, 0))
            self.buttonVarParagraph['pag{}'.format(name)].setStyleSheet(
                "max-width:80px;width:80px;min-width:80px")
            self.buttonVarParagraph['pag{}'.format(name)].setView(QListView())
            self.buttonVarParagraph['pag{}'.format(name)].activated[str].connect(
                self.WrittingNotOfOther)

            self.buttonVarSen = QPushButton(QIcon(""), u"设置段落", self.btnContect)
            self.buttonVarSen.setParent(self.btnContect)
            self.buttonVarSen.setGeometry(QRect(520, 0, 70, 30))
            self.buttonVarSen.setStyleSheet('min-width:50px;min-height:30px')
            self.buttonVarSen.clicked.connect(self.setDuan)

            conLayoutGoType_Contect.addWidget(self.btnContect, 3, 1, 1, 12)

            self.stackedWidgetImg.addWidget(self.imgListUpload['nmBox_{}'.format(name)])
            self.number += 1
        except Exception as e:
            print(e)

    def reDoNameTemplate(self):
        text, ok = QInputDialog.getText(self, '重命名', '输入模板名称：')
        if ok and text:
            result = contentModel.getDataName(str(text), self.tparms['admin_id'], self.tparms['task_id'],self.tparms['config_id'])
            print(result)
            if result is not None:
                msg_box = QMessageBox.information(self,
                                                  "警告",
                                                  "该名称已存在",
                                                  QMessageBox.Yes)

                return
            result = contentModel.updateName(self.nowInfo['id'],str(text),self.tparms['task_id'],self.tparms['config_id'])
            key = 0
            try:
                for info in self.data:
                    if info['name'] == self.nowInfo['old_name']:
                        self.data[key]['name'] = str(text)
                    key+=1

                self.item['it{}'.format(self.nowInfo['old_name'])].setText(str(text))

                self.TemplateLabel_Name['nm_{}'.format(self.nowInfo['old_name'])].setText(str(text))
            except Exception as e:
                print(e)


    def newAddTemplate(self):
        try:
            text, ok = QInputDialog.getText(self, '新建模板', '输入模板名称：')
            if ok and text:
                result = contentModel.getDataName(str(text), self.tparms['admin_id'], self.tparms['task_id'],self.tparms['config_id'])
                if result is not None:
                    msg_box = QMessageBox.information(self,
                                                      "警告",
                                                      "该名称已存在",
                                                      QMessageBox.Yes)

                    return
                result = contentModel.addOtherContent(str(text),'',self.tparms['admin_id'],self.tparms['task_id'],self.tparms['config_id'])
                data = contentModel.getDataNameInfo(str(text),self.tparms['admin_id'], self.tparms['task_id'],self.tparms['config_id'])
                self.data.append({'id': data[0], 'name': data[1], 'status': 0, 'old_name': data[1]})
                self.addTemplate(str(text))
        except Exception as e:
            print(e)

    def deleteTemp(self,item):
        try:
            itemd = self.listWidgetImg.findItems(self.nowInfo['name'], Qt.MatchExactly)[0]
            self.imgListUpload['nmBox_{}'.format(self.nowInfo['old_name'])].deleteLater()
            row = self.listWidgetImg.row(itemd)
            print(itemd)
            print(row)
            self.listWidgetImg.takeItem(row)
            contentModel.deleteInfo(self.tparms['admin_id'],self.nowInfo['name'],self.tparms['task_id'],self.tparms['config_id'])

            olddata = self.data

            self.data = []
            for info in olddata:
                if info['old_name'] != self.nowInfo['old_name']:
                     self.data.append(info)

            selected = self.listWidgetImg.selectedIndexes()
            for sel in selected:
                self.itemActivated_event(self.listWidgetImg.item(sel.row()))
        except Exception as e:
            print(e)

    def saveOtherTemp(self):
        text, ok=QInputDialog.getText(self, '另存为模板', '输入模板名称：')
        if ok and text:
            result = contentModel.getDataName(str(text), self.tparms['admin_id'], self.tparms['task_id'],self.tparms['config_id'])
            if result is not None:
                msg_box = QMessageBox.information(self,
                                            "警告",
                                            "该名称已存在",
                                            QMessageBox.Yes)

                return

            self.newName = str(text)
            try:
                self.createVarView['{}'.format(self.nowInfo['old_name'])].page().runJavaScript("window.saveGetContent()",self.otherContent)
            except Exception as e:
                print(e)
            self.addTemplate(str(text))

    def otherContent(self,result):
        result = contentModel.addOtherContent(self.newName,result,self.tparms['admin_id'],self.tparms['task_id'],self.tparms['config_id'])
        if result == 1:
            result = contentModel.getDataName(self.newName, self.tparms['admin_id'], self.tparms['task_id'],self.tparms['config_id'])
            self.data.append({"id":result[0],"name":self.newName,"status":0,"old_name":self.newName})

    def saveOther(self):
        pass

    def saveTemplateDo(self):
        try:
            self.createVarView['{}'.format(self.nowInfo['old_name'])].page().runJavaScript("window.saveGetContent()", self.getContent)
            QMessageBox.information(self, u'成功', u'保存成功')
        except Exception as e:
            print(e)

    def getContent(self,result):
        contentModel.updateContent(self.nowInfo['id'],result,self.nowInfo['old_name'],self.tparms['task_id'],self.tparms['config_id'])

    def goText(self,msg):
        try:
            self.createVarView['{}'.format(self.nowContent)].page().runJavaScript("window.say_hello('%s')" % msg)
        except Exception as e:
            print(e)

    def itemActivated_event(self,item):
        if self.firstLoad == 0:
            self.listWidgetImg.setVisible(False)

        self.nowContent = item.text()
        self.numberSelect = 0
        for info in self.data:
            if info['name'] == item.text():
                self.nowInfo = info

                try:
                    self.TemplateLabel_Name['nm_{}'.format(info['old_name'])].setText(str(item.text()))

                    if self.data[self.numberSelect]['status'] == 0:
                        self.createVarView['{}'.format(info['old_name'])].setVisible(False)
                        self.createVarView['{}'.format(info['old_name'])].setVisible(True)

                        self.test_loadingEditor(info)
                        self.data[self.numberSelect]['status'] = 1
                except Exception as e:
                    print(e)

            self.numberSelect+=1
        self.loading_album()

    def test_loadingEditor(self,info):
        self.createVarView['{}'.format(info['old_name'])].page().runJavaScript("window.gradeChange()", self.js_callback)

    def js_callback(self,result):

        try:
            self.firstLoad = 1
            # # 删除加载
            if result != 1:
                return self.test_loadingEditor(self.nowInfo)
            else:
                self.listWidgetImg.setVisible(True)
                content = contentModel.getDataContent(self.nowInfo['id'],self.tparms['task_id'],self.tparms['config_id'])
                self.createVarView['{}'.format(self.nowInfo['old_name'])].page().runJavaScript("window.say_hello('%s')" % content.replace('\\"','"'))
                self.firstLoad = 1
        except Exception as e:
            print(e)

    def WrittingNotOfOther(self,msg):
        self.createVarView['{}'.format(self.nowContent)].page().runJavaScript("window.say_hello('%s')" % msg)

    def setDuan(self):
        self.ui2 = DuanWidget(self.tparms)
        self.ui2.show()

    def reDoNameTemplateNew(self):
        text, ok = QInputDialog.getText(self, '重命名', '输入模板名称：')
        if ok and text:
            result = contentModel.getDataName(str(text), self.tparms['admin_id'], self.tparms['task_id'],self.tparms['config_id'])
            if result is not None:
                msg_box = QMessageBox.information(self,
                                                  "警告",
                                                  "该名称已存在",
                                                  QMessageBox.Yes)

                return
            result = contentModel.updateName(self.nowInfo['id'],str(text),self.tparms['task_id'],self.tparms['config_id'])
            key = 0
            try:
                for info in self.data:
                    if info['name'] == self.nowInfo['old_name']:
                        self.data[key]['name'] = str(text)
                    key+=1
                self.item['it2{}'.format(self.nowInfo['old_name'])].setText(str(text))

                self.TemplateLabel_Name['nm_{}'.format(self.nowInfo['old_name'])].setText(str(text))
            except Exception as e:
                print(e)

    def deleteTempNew(self,item):
        try:
            itemd = self.listWidgetImg.findItems(self.nowInfo['name'], Qt.MatchExactly)[0]
            self.imgListUpload['nmBox_{}'.format(self.nowInfo['old_name'])].deleteLater()
            row = self.listWidgetImg.row(itemd)
            print(itemd)
            print(row)
            self.listWidgetImg.takeItem(row)
            print(self.tparms)
            contentModel.deleteInfo(self.tparms['admin_id'],self.nowInfo['name'],self.tparms['task_id'],self.tparms['config_id'])

            olddata = self.data
            self.data = []
            for info in olddata:
                if info['old_name'] != self.nowInfo['old_name']:
                     self.data.append(info)

            selected = self.listWidgetImg.selectedIndexes()
            for sel in selected:
                self.itemActivated_event(self.listWidgetImg.item(sel.row()))
        except Exception as e:
            print(e)

    def loading_album(self):
        try:
            self.buttonVarParagraph['pag{}'.format(self.nowInfo['name'])].clear()
            albumList = sentenceModel.getPagDataList(self.tparms['admin_id'], self.tparms['task_id'],self.tparms['config_id'])
            if len(albumList) > 0:
                for info in albumList:
                    self.buttonVarParagraph['pag{}'.format(self.nowInfo['name'])].addItem(info['name'])
        except Exception as e:
            print(e)

class DuanWidget(QTabWidget):
    def __init__(self,tparms, *args, **kwargs):
        super(DuanWidget, self).__init__(*args, **kwargs)
        self.setWindowTitle(u"设置段落/句子")
        self.resize(841,500)
        self.tparms = tparms
        for i in range(2):
            if i == 0:
                self.Juzi = QtWidgets.QWidget()
                self.Labeltext = QLabel(self.Juzi)
                self.Labeltext.setText('共 0 行')
                self.Labeltext.setGeometry(QRect(5, 15,90,30))

                self.titleText = QtWidgets.QTextEdit(self.Juzi)
                self.titleText.setGeometry(QRect(0, 40, 830, 400))
                self.titleText.setObjectName("edit")

                self.clearBtn = QPushButton(QIcon(""), u"清空", self.Juzi)
                self.clearBtn.move(0, 440)
                self.clearBtn.clicked.connect(self.clearTitle)

                self.setListLast = ''
                self.setList = QtWidgets.QComboBox(self.Juzi)
                self.setList.move(100, 443)
                self.sentype = optionModel.titleComposeData(self.tparms['admin_id'],self.tparms['task_id'],'senType',self.tparms['config_id'])
                self.setList.addItem("以行分割")
                self.setList.addItem("符号分割 <*>")
                if self.sentype is not None and self.sentype == 1:
                    self.setList.setCurrentIndex(0)
                elif self.sentype is not None and self.sentype == 2:
                    self.setList.setCurrentIndex(1)
                self.setList.activated[str].connect(self.changeJuzi)

                self.saveBtn_Jzi = QPushButton(QIcon(""), u"保存", self.Juzi)
                self.saveBtn_Jzi.move(223, 440)
                self.saveBtn_Jzi.clicked.connect(self.saveJuzi)
                self.addTab(self.Juzi, str('句子'))
                QMetaObject.connectSlotsByName(self)
                pool = ThreadPoolExecutor(max_workers=1)
                pool.submit(self.getInfoJuzi)

            elif i == 1:
                self.Duanluo = QtWidgets.QWidget()

                self.Labeltext_Duan = QLabel(self.Duanluo)
                self.Labeltext_Duan.setText('共 0 行')
                self.Labeltext_Duan.setGeometry(QRect(5, 15, 90, 30))

                self.duanCombo_Duan = QtWidgets.QComboBox(self.Duanluo)
                self.duanCombo_Duan.setGeometry(QRect(120, 10, 50, 30))
                self.duanCombo_Duan.setStyleSheet('min-width:170px;max-width:170px;')
                self.duanCombo_Duan.currentIndexChanged.connect(self.getInfoDuan)
                self.duanOption = {'【段落1】':1,'【段落2】':1,'【段落3】':1,'【段落4】':1,'【段落5】':1,'【段落6】':1}

                self.titleText_Duan = QTextEdit(u"", self.Duanluo)
                self.titleText_Duan.setGeometry(QRect(0, 40, 830, 400))

                self.clearBtn_Duan = QPushButton(QIcon(""), u"清空", self.Duanluo)
                self.clearBtn_Duan.move(0, 440)
                self.clearBtn_Duan.clicked.connect(self.clearTitleDuan)

                self.setListDuanLast = ''
                self.setList_Duan = QtWidgets.QComboBox(self.Duanluo)
                self.setList_Duan.move(100, 443)
                duantype = optionModel.titleComposeData(self.tparms['admin_id'], self.tparms['task_id'], 'duanType',
                                                       self.tparms['config_id'])
                self.setList_Duan.addItem("以行分割")
                self.setList_Duan.addItem("符号分割 <*>")
                if duantype is not None and len(duantype) > 0:
                    if duantype['【段落1】'] is not None and duantype['【段落1】'] == 1:
                        self.duanOption = duantype
                        self.setList_Duan.setCurrentIndex(0)
                    elif duantype['【段落1】'] is not None and duantype['【段落1】'] == 2:
                        self.duanOption = duantype
                        self.setList_Duan.setCurrentIndex(1)

                self.setList_Duan.activated[str].connect(self.changeDuan)

                self.clearBtn_Cloud = QPushButton(QIcon(""), u"云段落", self.Duanluo)
                self.clearBtn_Cloud.move(313, 440)
                self.clearBtn_Cloud.clicked.connect(self.startSpider)

                self.clearBtn_save = QPushButton(QIcon(""), u"保存", self.Duanluo)
                self.clearBtn_save.move(223, 440)
                self.clearBtn_save.clicked.connect(self.saveDuan)

                self.addTab(self.Duanluo, str('段落'))
                self.loading_album()
                self.getInfoDuan()

    @pyqtSlot()
    def on_edit_textChanged(self):
        text = self.titleText.toPlainText()
        count = len(re.split('\n', text))
        self.Labeltext.setText('共 '+str(count)+' 行')

        text2 = self.titleText_Duan.toPlainText()
        count2 = len(re.split('\n', text2))
        self.Labeltext_Duan.setText('共 '+str(count2)+' 行')

    def changeJuzi(self,s):
        if '以行分割' in s and self.setListLast not in '以行分割':
            configName = self.setList.currentText()
            self.setListLast = configName
            titleText = self.titleText.toPlainText()
            self.titleText.clear()
            titleText = titleText.replace('<*>','\n')
            titleText = titleText.replace('\n\n','\n')
            self.titleText.setText(titleText)

        if '符号分割 <*>' in s and self.setListLast not in '符号分割 <*>':
            configName = self.setList.currentText()
            self.setListLast = configName
            titleText = self.titleText.toPlainText()
            self.titleText.clear()
            titleText = titleText.replace('\n', '<*>\n')
            titleText = titleText.replace('<*><*>\n', '<*>\n')
            self.titleText.setText(titleText)

    def changeDuan(self,s):
        duan = self.duanCombo_Duan.currentText()
        if '以行分割' in s:
            self.duanOption['{}'.format(duan)] = 1
            print(self.duanOption)
            configName = self.setList_Duan.currentText()
            self.setListDuanLast = configName
            titleText = self.titleText_Duan.toPlainText()
            self.titleText_Duan.clear()
            titleText = titleText.replace('<*>','\n')
            titleText = titleText.replace('\n\n','\n')
            self.titleText_Duan.setText(titleText)

        if '符号分割 <*>' in s:
            self.duanOption['{}'.format(duan)] = 2
            print(self.duanOption)
            configName = self.setList_Duan.currentText()
            self.setListDuanLast = configName
            titleText = self.titleText_Duan.toPlainText()
            self.titleText_Duan.clear()
            titleText = titleText.replace('\n', '<*>\n')
            titleText = titleText.replace('<*><*>\n', '<*>\n')
            self.titleText_Duan.setText(titleText)

    def add_Duan(self):
        text, ok = QInputDialog.getText(self, '新建模板', '输入段落名称：')
        if ok and text:

            result = sentenceModel.getDataOne(self.tparms['admin_id'],self.tparms['task_id'],'【'+str(text)+'】',self.tparms['config_id'])
            if int(result['id']) > 0:
                msg_box = QMessageBox.information(self,
                                                  "警告",
                                                  "该名称已存在",
                                                  QMessageBox.Yes)
                return
            else:
                try:
                    sentenceModel.addPageInfo(self.tparms['admin_id'],'【'+str(text)+'】',self.tparms['task_id'],self.tparms['config_id'])
                except Exception as e:
                    print(e)
    def loading_album(self):
        try:
            self.duanCombo_Duan.clear()
            albumList = sentenceModel.getPagDataList1(self.tparms['admin_id'],self.tparms['task_id'],self.tparms['config_id'])
            if len(albumList) > 0:
                for info in albumList:
                    self.duanCombo_Duan.addItem(info['name'])
        except Exception as e:
            print(e)

    def getInfoDuan(self):
        configName = self.setList_Duan.currentText()

        self.setListDuanLast = configName
        self.titleText_Duan.clear()
        sel = self.duanCombo_Duan.currentText()

        try:
            if self.duanOption['{}'.format(sel)] is not None and self.duanOption['{}'.format(sel)] == 1:
                self.setList_Duan.setCurrentIndex(0)
            elif self.duanOption['{}'.format(sel)] is not None and self.duanOption['{}'.format(sel)] == 2:
                self.setList_Duan.setCurrentIndex(1)
        except Exception as e:
            print(e)

        info = sentenceModel.getDataOne(self.tparms['admin_id'],self.tparms['task_id'],sel,self.tparms['config_id'])
        if info['id'] > 0:
            data = sentenceModel.getDataListDuan(self.tparms['admin_id'],self.tparms['task_id'],info['id'],self.tparms['config_id'])
            self.titleText_Duan.moveCursor(QTextCursor.End)
            for info in data:
                try:
                    if self.duanOption['{}'.format(sel)] is not None and self.duanOption['{}'.format(sel)] == 1:
                        self.titleText_Duan.insertPlainText(str(info['content'])+'\n')
                    elif self.duanOption['{}'.format(sel)] is not None and self.duanOption['{}'.format(sel)] == 2:
                        self.titleText_Duan.insertPlainText(str(info['content'])+'<*>')
                except Exception as e:
                    self.titleText_Duan.insertPlainText(str(info['content']) + '\n')

            self.Labeltext_Duan.setText('共 '+str(len(data))+' 行')

    def getInfoJuzi(self):
        try:
            configName = self.setList.currentText()
            self.setListLast = configName
            data = sentenceModel.getDataList(self.tparms['admin_id'],self.tparms['task_id'],self.tparms['config_id'])

            self.titleText.moveCursor(QTextCursor.End)
            for info in data:
                if self.sentype == 1:
                    self.titleText.insertPlainText(str(info['content'])+'\n')
                elif self.sentype == 2:
                    self.titleText.insertPlainText(str(info['content'])+'<*>')
                elif len(self.sentype) == 0:
                    self.titleText.insertPlainText(str(info['content'])+'\n')

            self.Labeltext.setText('共 '+str(len(data))+' 行')
        except Exception as e:
            print(e)
        # pass

    def clearTitle(self):
        self.titleText.setText('')
        self.Labeltext.setText('共 0 行')

    def clearTitleDuan(self):
        self.titleText_Duan.setText('')
        self.Labeltext_Duan.setText('共 0 行')

    def saveJuzi(self):

        configName = self.setList.currentText()
        titleText = self.titleText.toPlainText()
        if '符号分割 <*>' in configName:
            optionModel.setSenTypeSave(self.tparms['admin_id'],2,self.tparms['task_id'],self.tparms['config_id'])
            list = titleText.split('<*>')
            sentenceModel.deleteAll(self.tparms['admin_id'], self.tparms['task_id'], self.tparms['config_id'])
            sentenceModel.add_Data(list, self.tparms['admin_id'], self.tparms['task_id'], self.tparms['config_id'])
        elif '以行分割' in configName:
            optionModel.setSenTypeSave(self.tparms['admin_id'],1,self.tparms['task_id'],self.tparms['config_id'])
            zhu_list = re.split('\n', titleText)
            sentenceModel.deleteAll(self.tparms['admin_id'],self.tparms['task_id'],self.tparms['config_id'])
            sentenceModel.add_Data(zhu_list,self.tparms['admin_id'],self.tparms['task_id'],self.tparms['config_id'])

    def saveDuan(self):
        try:
            configName = self.setList_Duan.currentText()
            titleText = self.titleText_Duan.toPlainText()
            if '符号分割 <*>' in configName:
                zhu_list = titleText.split('<*>')
            elif '以行分割' in configName:
                zhu_list = re.split('\n', titleText)
            print(self.duanOption)
            optionModel.setDuanTypeSave(self.tparms['admin_id'], self.duanOption, self.tparms['task_id'], self.tparms['config_id'])

            sel = self.duanCombo_Duan.currentText()
            info = sentenceModel.getDataOne(self.tparms['admin_id'], self.tparms['task_id'], sel,self.tparms['config_id'])
#             # print(info)
            sentenceModel.deleteAllDuan(self.tparms['admin_id'],self.tparms['task_id'],info['id'],self.tparms['config_id'])
            sentenceModel.add_DataDuan(zhu_list,self.tparms['admin_id'],self.tparms['task_id'],info['id'],self.tparms['config_id'])
        except Exception as e:
            print(e)

    def startSpider(self):
        text, ok = QInputDialog.getText(self, '云段落', '请输入关键词：')
        if ok and text:
            if len(str(text)) == 0:
                msg_box = QMessageBox.information(self,
                                                  "警告",
                                                  "请输入关键词，",
                                                  QMessageBox.Yes)
            else:
                self.link_request(str(text))
                self.add_request()

    def link_request(self, keyword):
        self.sess = requests.session()
        self.keyword = keyword
        self.baidu_host = 'http://www.baidu.com'
        self.baidu_search = 'http://www.baidu.com/s?wd={}&ie=utf-8&rqlang=cn&tn=baiduhome_pg'
        self.enter_zhihu = ''
        self.zhihu_search = 'https://www.zhihu.com/search?type=content&q={}'
        self.zhihu_add = 'https://api.zhihu.com/search_v3?t=general&q={}&correction=1&offset={}&limit=20&lc_idx={}&show_all_topics=0&vertical_info=0%2C0%2C0%2C0%2C0%2C0%2C0%2C0%2C0%2C1'
        self.zhihu_addhash = 'https://api.zhihu.com/search_v3?t=general&q={}&correction=1&offset={}&limit=20&lc_idx={}&show_all_topics=0&search_hash_id={}&vertical_info=0%2C0%2C0%2C0%2C0%2C0%2C0%2C0%2C0%2C1'
        self.header = {
            'user-agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.70 Safari/537.36"}
        self.result = []
        self.hash_id = None
        self.error_code = 0
        self.title_all = []
        self.content_all = []
        self.article_id_all = []

        headers = {
            "Accept": "application/json, text/javascript, */*; q=0.01",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8,fr;q=0.7",
            "Connection": "keep-alive",
            # "Cookie": cookieValue,
            # "Host": "www.baidu.com",
            # "Referer": "https://www.baidu.com/s?ie=UTF-8&wd={}headers&oq=%25E6%2596%25B0%25E5%259E%258Buv%25E7%258E%25AF%25E4%25BF%259D%25E8%25BF%2590%25E6%25B0%25B4%25E7%2583%259F%25E7%25BD%25A9%25E6%2589%25B9%25E5%258F%2591&rsv_pq=e98236ca00014635&rsv_t=c102CoCiB95P83cJtVpRmucNu%2BMFIzwOaHCF85uaz3tKMfSqHS7dw6eZAHY&rqlang=cn&rsv_enter=1&rsv_dl=tb&inputT=1721716&rsv_sug3=35&rsv_sug1=3&rsv_sug7=000&rsv_sug2=0&rsv_sug4=1721797&rsv_sug=1".format(keyword),
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "same-origin",
            "User-Agent": 'Mozilla/5.0 (iPhone; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1',
        }
        self.sess.headers.update(self.header)
        try:
            self.sess.get(self.baidu_host, headers=headers, timeout=3)
            url = self.baidu_search.format(u'知乎' + self.keyword)
            resp_bsearch = self.sess.get(url, headers=headers, timeout=3)
            if 'ç½ç»ä¸ç»åï¼è¯·ç¨åéè¯' in resp_bsearch.text:
                return self.link_request(self.keyword)
            self.enter_zhihu = self.search_parse(resp_bsearch.content)
            if self.enter_zhihu:
#                 # print(self.enter_zhihu)
                self.sess.get(self.enter_zhihu)
                resp_index = self.sess.get(self.zhihu_search.format(self.keyword))
                self.resp_parse(resp_index.content)
            else:
                self.error_code = 5
        except Exception as e:
            print(e)
            self.error_code = 4
            return

    def add_request(self):
        offset = 20
        lc_idx = 21
        while len(self.result) < 20:
            try:
                if not self.hash_id:
                    url = self.zhihu_add.format(self.keyword, offset, lc_idx)
                    resp_add = self.sess.get(url, timeout=3)
                else:
                    url = self.zhihu_addhash.format(self.keyword, offset, lc_idx, self.hash_id)
                    resp_add = self.sess.get(url, timeout=3)
                offset += 20
                lc_idx += 20
                if lc_idx > 220:
                    break
                self.add_parse(resp_add.content)
                # time.sleep(3)
            except Exception as e:
                break

    def search_parse(self, resp):
        dment = etree.HTML(resp)
        res_list = dment.xpath(
            "//div[@class='f13 c-gap-top-xsmall se_st_footer user-avatar']/a[@class='c-showurl c-color-gray']")
        inter_zhihu = ''
        for i in res_list:
            if i.text and 'zhihu' in i.text:
                inter_zhihu = i.attrib['href']
                break
            elif u'知乎' in i.xpath("string(.)"):
                inter_zhihu = i.attrib['href']
                break
        # if not inter_zhihu:
        #    with open('{}.html'.format(int(time.time())), 'a+') as f:
        #        f.write(resp)
        return inter_zhihu

    def resp_parse(self, resp):
        hment = etree.HTML(resp)
        json_text = hment.xpath("//script[@id='js-initialData']")
        resa = json.loads(json_text[0].text)
        str_replace = re.compile(r'<.+?>')

        article_list = resa['initialState']['entities']['articles']

        for k1, v1 in article_list.items():
            if v1.get('content'):
                v1['content'] = v1['content'].replace('<p>', '').replace('</p>', '\n')
                news = str_replace.sub('', v1['content'])
#                 # print(news)
                try:
                    if len(news) > 200:
                        if v1.get('title'):
                            title = str_replace.sub('', v1['title'])
                        else:
                            title = str_replace.sub('', v1['question']['name'])
                        self.result.append({'title': title, 'article_id': 'zh_' + str(v1['id']), 'content': news})
                except Exception as e:
                    print(e)
        answer_list = resa['initialState']['entities']['answers']
        for k2, v2 in answer_list.items():
            if v2.get('content'):
                v2['content'] = v2['content'].replace('<p>', '').replace('</p>', '\n')
                news = str_replace.sub('', v2['content'])
                try:
                    if len(news) > 200:
                        if v2.get('title'):
                            title = str_replace.sub('', v2['title'])
                        else:
                            title = str_replace.sub('', v2['question']['name'])
#                         # print(news)
                        self.result.append({'title': title, 'article_id': 'zh_' + str(v2['id']), 'content': news})
                except Exception as e:
                    print(e)

    def add_parse(self, data):
        atext = json.loads(data)

        self.hash_id = atext['search_action_info']['search_hash_id']
        str_replace = re.compile(r'<.+?>')
        for i in atext['data']:
            if i['object'].get('content'):
                i['object']['content'] = i['object']['content'].replace('<p>', '').replace('</p>', '\n')
                news = str_replace.sub('', i['object']['content'])
                if len(news) > 200:
                    if i['object'].get('title'):
                        title = str_replace.sub('', i['object']['title'])
                    else:
                        title = str_replace.sub('', i['object']['question']['name'])

                    text = self.titleText_Duan.toPlainText()
                    count = len(re.split('\n', text))
                    if count < 200:
                        self.titleText_Duan.insertPlainText(news + '\n')
                        self.Labeltext_Duan.setText('共 ' + str(count) + ' 行')
                        break
                    # news


if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = DuanWidget({'admin_id': 1, 'username': 'test2','task_id':16})
    w.resize(841,500)
    w.show()
    sys.exit(app.exec_())
