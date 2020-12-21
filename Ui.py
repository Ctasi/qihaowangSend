#!/usr/bin/env python
# -*- coding: utf-8 -*-

from math import floor, pi, cos, sin,ceil
from random import random, randint
from time import time
from PyQt5.QtCore import QTimer, Qt,QRect,QSize,QBasicTimer,QThread,pyqtSignal
from PyQt5.QtGui import QColor, QPainter, QPainterPath, QPen,QPixmap,QIcon,QFont,QDoubleValidator,QBrush,QPalette
from PyQt5.QtWidgets import *
from graphTest import graph_Form
import datetime
import sys
import subprocess
import platform
import config
from TitleCombination import TabWidgetTitle
from ContentTemplate import Content
from SendArticle import Send
import taskModel
import usernameModel
import sip
import requests
import json
import configureModel
import apiAll
import PIL
import re
from ImageSet import TabWidgetImages
import optionModel
import time as time2
import os 
import sentenceModel

tparms_f = {'username':'','admin_id':0,'version':2.3}

__Author__ = 'Tasi'
__Copyright__ = 'Copyright (c) 2020'

#动态背景参数设置
# 最小和最大半径、 半径阈值和填充圆的百分比
radMin = 10
radMax = 80
filledCircle = 30  # 填充圆的百分比
concentricCircle = 60  # 同心圆百分比
radThreshold = 25  # IFF special, over this radius concentric, otherwise filled
# 最小和最大移动速度
speedMin = 0.3
speedMax = 0.6
# 每个圆和模糊效果的最大透明度
maxOpacity = 0.6

colors = [
    QColor(52, 168, 83),
    QColor(117, 95, 147),
    QColor(199, 108, 23),
    QColor(194, 62, 55),
    QColor(0, 172, 212),
    QColor(120, 120, 120)
]
circleBorder = 10
backgroundLine = colors[0]
backgroundColor = QColor(0, 160, 233)
backgroundMlt = 0.85

lineBorder = 2.5

# 整个圆和数组的数目
maxCircles = 8
points = []

# 实验变量
circleExp = 1
circleExpMax = 1.003
circleExpMin = 0.997
circleExpSp = 0.00004
circlePulse = False

# 生成随机整数 a<=x<=b
def randint(a, b):
    return floor(random() * (b - a + 1) + a)
# 生成随机小数
def randRange(a, b):
    return random() * (b - a) + a
# 生成接近a的随机小数
def hyperRange(a, b):
    return random() * random() * random() * (b - a) + a


class Circle:

    def __init__(self, background, width, height):
        self.background = background
        self.x = randRange(-width / 2, width / 2)
        self.y = randRange(-height / 2, height / 2)
        self.radius = hyperRange(radMin, radMax)
        self.filled = (False if randint(
            0, 100) > concentricCircle else 'full') if self.radius < radThreshold else (
                False if randint(0, 100) > concentricCircle else 'concentric')
        self.color = colors[randint(0, len(colors) - 1)]
        self.borderColor = colors[randint(0, len(colors) - 1)]
        self.opacity = 0.05
        self.speed = randRange(speedMin, speedMax)  # * (radMin / self.radius)
        self.speedAngle = random() * 2 * pi
        self.speedx = cos(self.speedAngle) * self.speed
        self.speedy = sin(self.speedAngle) * self.speed
        spacex = abs((self.x - (-1 if self.speedx < 0 else 1) *
                      (width / 2 + self.radius)) / self.speedx)
        spacey = abs((self.y - (-1 if self.speedy < 0 else 1) *
                      (height / 2 + self.radius)) / self.speedy)
        self.ttl = min(spacex, spacey)
        #背景参数调用

class testStart(QThread):
    finishSignal_pc_up = pyqtSignal(list)
    def __init__(self,*args, **kwargs):
        super(testStart, self).__init__(*args, **kwargs)
    def run(self):
        while True:
            self.finishSignal_pc_up.emit(['continue', 'send'])
            time2.sleep(20)

#软件登录模块
class Login(QDialog):

    def __init__(self, parent=None):
        QDialog.__init__(self, parent)
        # 设置背景颜色
        palette = self.palette()
        palette.setColor(palette.Background, backgroundColor)
        self.setWindowIcon(QIcon(self.resource_path('logo-min.png')))
        self.setAutoFillBackground(True)
        self.setPalette(palette)

        self.setWindowTitle(u"智享云·闪投系统 {}".format(tparms_f['version']))
        self.resize(313, 434)
        self.setFixedSize(313, 408)

        label_logo = QLabel("", self)
        label_logo.setGeometry(QRect(122, 40, 68, 68))
        logo_img = QPixmap()
        label_logo.setPixmap(logo_img)

        label_title = QLabel("", self)
        label_title.setText('智享云·闪投系统')
        label_title.setStyleSheet("font-size:15px;color:white")
        label_title.setGeometry(QRect(100, 111, 137, 17))

        login_font = QFont()
        login_font.setPointSize(13)

        self.filename = datetime.datetime.now().strftime("%Y%m%d%H%M")
        type = self.version_test()
        if str(tparms_f['version']) not in str(type):
            #如果发现新版本 提示更新
            tparms_f['version'] = type
            label_title_version = QLabel("", self)
            label_title_version.setText('发现新版本')
            label_title_version.setStyleSheet("font-size:17px;color:white")
            label_title_version.setGeometry(QRect(115, 171, 107, 17))
            self.pushButton_update = QPushButton(QIcon(""), u"更新", self)
            self.pushButton_update.setGeometry(QRect(55, 252, 202, 36))
            self.pushButton_update.setStyleSheet("border:0px groove gray;border-radius:10px;padding:2px 4px;background-color:#ffffff;color:#1c91ce;")
            self.pushButton_update.clicked.connect(self.start_update)
        else:
            self.lineEdit_user = QLineEdit(u"", self)
            self.lineEdit_user.setPlaceholderText(u"请输入您的账号")
            self.lineEdit_user.setGeometry(QRect(55, 170, 202, 36))
            self.lineEdit_user.setStyleSheet("border:0px solid;border-radius:5px;padding:2px 4px;")
            self.lineEdit_user.setFont(login_font)

            self.lineEdit_passwd = QLineEdit(u'', self)
            self.lineEdit_passwd.setPlaceholderText(u"请输入您的密码")
            self.lineEdit_passwd.setGeometry(QRect(55, 218, 202, 36))
            self.lineEdit_passwd.setStyleSheet("border:0;border-radius:5px;padding:2px 4px;")
            self.lineEdit_passwd.setFont(login_font)
            self.lineEdit_passwd.setEchoMode(QLineEdit.Password)

            self.pushButton_login = QPushButton(QIcon(""), u"登录", self)
            self.pushButton_login.setGeometry(QRect(55, 292, 202, 36))
            self.pushButton_login.setStyleSheet(
                "border:0px groove gray;border-radius:10px;padding:2px 4px;background-color:#ffffff;color:#262b2e;")
            self.pushButton_login.clicked.connect(self.log_in)

        label_version = QLabel("", self)
        label_version.setText('版本2.3')
        label_version.setStyleSheet("font-size:12px;color:white")
        label_version.setGeometry(QRect(127, 366, 55, 15))

    def version_test(self):
        #版本检测
        try:
            sql = "SELECT `version` FROM fb_version WHERE id = 1"
            cursor = config.config_online()
            data = []
            cursor.execute(sql)
            for info in cursor:
                return info[0]
        except:
            QMessageBox.critical(self, u'错误', u'网络连接异常')

    def start_update(self):
        QMessageBox.information(self, u'等待', u'正在下载')
        self.pushButton_update.setDisabled(True)
        self.pushButton_update.setText('正在下载')
        self.pushButton_update.setStyleSheet("background-color: #d44e4d;color:#FFFFFF;border-radius:5px;")
        self.updateThread = download_update()
        self.updateThread.finishSignal_up.connect(self.start_update_end)
        self.updateThread.start()

    def start_update_end(self, reres):
        if reres[0] == 1:
            QMessageBox.information(self, u"提示", u"更新完成，同级目录下“信息发布软件-企好网-{}.exe”为最新版本".format(tparms_f['version']))
            self.pushButton_update.setStyleSheet(
                "border:0px groove gray;border-radius:10px;padding:2px 4px;background-color:#ffffff;color:#f8565e;")
            self.pushButton_update.setDisabled(True)
            self.pushButton_update.setText('更新完成')
            if os.path.isfile("upgrade.bat"):
                os.remove("upgrade.bat")
            self.WriteRestartCmd("信息发布软件-企好网-{}.exe".format(tparms_f['version']))
        elif reres[0] == 0:
            QMessageBox.information(self, u"提示", u"更新失败请检查网络")
            self.pushButton_update.setStyleSheet(
                "border:0px groove gray;border-radius:10px;padding:2px 4px;background-color:#ffffff;color:#f8565e;")
            self.pushButton_update.setDisabled(False)
            self.pushButton_update.setText('更新')

    def WriteRestartCmd(self,exe_name):
        b = open("upgrade.bat", 'w')
        TempList = "@echo off\n";  # 关闭bat脚本的输出
        TempList += "if not exist " + exe_name + " exit \n";  # 新文件不存在,退出脚本执行
        TempList += "sleep 3\n"  # 3秒后删除旧程序（3秒后程序已运行结束，不延时的话，会提示被占用，无法删除）
        TempList += "del " + os.path.realpath(sys.argv[0]) + "\n"  # 删除当前文件
        TempList += "start " + exe_name  # 启动新程序
        b.write(TempList)
        b.close()
        subprocess.Popen("upgrade.bat")
        sys.exit()  # 进行升级，退出此程序

    def resource_path(self, relative):
        if hasattr(sys, "_MEIPASS"):
            return os.path.join(sys._MEIPASS, relative)
        return os.path.join(relative)

    def log_in(self):
        username = str(self.lineEdit_user.text())
        password = str(self.lineEdit_passwd.text())

        try:
            info = usernameModel.login(username,password)
            if len(info) > 0:
                tparms_f['username'] = info[0]
                tparms_f['admin_id'] = info[1]
                QMessageBox.information(self, u"提示", u"登录成功")
                self.accept()
            else:
                QMessageBox.critical(self, u'错误', u'用户名或密码错误')
        except:
            QMessageBox.critical(self, u'错误', u'用户名或密码错误')
            return


class download_update(QThread):
    finishSignal_up = pyqtSignal(list)
    def __init__(self):
        super(download_update, self).__init__()
    def run(self):
        try:
            Edition = self.os_bits(self.machine())
            url = 'http://123.133.86.56:8080/xxfb_up/%E4%BF%A1%E6%81%AF%E5%8F%91%E5%B8%83%E8%BD%AF%E4%BB%B6-%E4%BC%81%E5%A5%BD%E7%BD%91.exe'
            self.r = requests.get(url, stream=True)
            with open('信息发布软件-企好网-{}.exe'.format(tparms_f['version']), "wb") as code:
                for chunk in self.r.iter_content(chunk_size=1024):  # 边下载边存硬盘
                    if chunk:
                        code.write(chunk)
            self.finishSignal_up.emit([1])
        except:
            self.finishSignal_up.emit([0])

    def machine(self):
        """Return type of machine."""
        if os.name == 'nt' and sys.version_info[:2] < (2, 7):
            return os.environ.get("PROCESSOR_ARCHITEW6432",
                                  os.environ.get('PROCESSOR_ARCHITECTURE', ''))
        else:
            return platform.machine()

    def os_bits(self, machine):
        """Return bitness of operating system, or None if unknown."""
        machine2bits = {'AMD64': 64, 'x86_64': 64, 'i386': 32, 'x86': 32}
        return machine2bits.get(machine, None)


class CircleLineWindow(QWidget,graph_Form):

    def __init__(self, *args, **kwargs):
        super(CircleLineWindow, self).__init__(*args, **kwargs)
        # 设置背景颜色
        palette = self.palette()
        palette.setColor(palette.Background, backgroundColor)
        self.setAutoFillBackground(True)
        self.setPalette(palette)
        # 获取屏幕大小
        geometry = QApplication.instance().desktop().availableGeometry()
        self.screenWidth = geometry.width()
        self.screenHeight = geometry.height()
        self._canDraw = True
        self._firstDraw = True
        self._timer = QTimer(self, timeout=self.update)
        self.init()
        self.main()

    def closeEvent(self, event):
        print(1)
        ret = 1

        if ret == 0:
            print(u'目标进程存在，杀死该进程')
            os.system('TASKKILL /F /IM {}"'.format(sys.argv[0]))
            ret = 1
        else:
            print(u'目标进程不存在')
        ret = os.system('tasklist | find "{}"'.format(sys.argv[0]))
        sys.exit(0)
        
    def main(self):
        # self.pushButton_7.clicked.connect(self.test)
        self.setupUi(self)
        self.tabWidget.clear()
        self.rjList()
        self.tabWidget.setTabsClosable(True)  # 显示关闭按钮
        self.tabWidget.tabCloseRequested.connect(self.closeTab)
        self.setWindowTitle(u"智享云·闪投系统 v{}".format(tparms_f['version']))


    def rjList(self):
        self.tab1 = QWidget()
        self.topFiller = QLabel()
        self.topFiller.setMinimumSize(900, 600)  #######设置滚动条的尺寸

        self.taskTips = QLabel(self)
        self.taskdata = taskModel.getListTask(tparms_f['admin_id'])
        self.taskdataCount = taskModel.getListTaskCount(tparms_f['admin_id'])
        self.taskTips.setText(u'共{}任务'.format(self.taskdataCount))
        self.taskTips.setStyleSheet("border:0px solid;max-height:30px;color:black")
        # self.taskTips.setGeometry(QRect(10, 10, 197, 17)

        self.addTask = QPushButton(QIcon(""), u"添加", self.topFiller)
        self.addTask.setGeometry(QRect(900, 10, 100, 30))
        self.addTask.clicked.connect(self.addTaskNow)

        self.search = QLineEdit(self)

        self.searchButton = QPushButton(QIcon(""), u"搜索", self.topFiller)
        self.searchButton.setGeometry(QRect(900, 10, 100, 30))
        self.searchButton.clicked.connect(lambda:self.searchTask(1))

        self.conLayout = QGridLayout(self.topFiller)
        self.conLayout.setGeometry(QRect(10, 50, 0, 0))

        self.conLayout.addWidget(self.taskTips, 0, 1)
        self.conLayout.addWidget(self.search, 0, 3)
        self.conLayout.addWidget(self.searchButton, 0, 5)
        self.conLayout.addWidget(self.addTask, 0, 6)

        self.page_num = 0
        self.limit = 6
        self.page_now = 1
        self.page_count = ceil(self.taskdataCount / 6)

        self.MapButton = locals()
        self.phone = locals()

        self.pbar = locals()
        self.timer = locals()
        self.step = locals()

        self.status = locals()

        self.start = locals()

        # 中控列表
        self.tabCentralControl = locals()
        self.layoutCentralControl = locals()

        userList = []
        self.key = 2
        for info in self.taskdata:
            self.tparms = locals()
            self.tparms['tparms{}'.format(info['id'])] = {'admin_id': info['admin_id'],'name':'{}'.format(info['name']),'task_id':'{}'.format(info['id']),'username':'{}'.format(info['username']),'password':'{}'.format(info['password']),'token':'{}'.format(info['token']),'config_id':'{}'.format(info['config_id']),'shop_id':'{}'.format(info['shop_id'])}
            self.MapButton['MapButton{}'.format(info['id'])] = QLabel(self)
            self.MapButton['MapButton{}'.format(info['id'])].setText(u'{}'.format(info['name']))
            self.MapButton['MapButton{}'.format(info['id'])].setStyleSheet("border:0px solid;max-height:30px;color:black")

            self.pbar['pbar{}'.format(info['id'])] = QProgressBar(self)
            self.timer['timer{}'.format(info['id'])] = QBasicTimer()
            self.timer['timer{}'.format(info['id'])].start(0, self)
            self.step['step{}'.format(info['id'])] = int(info['speed'])
            self.pbar['pbar{}'.format(info['id'])].setStyleSheet('border-radius:15px;font-size:12px;color:white')
            self.pbar['pbar{}'.format(info['id'])].setAlignment(Qt.AlignRight)
            self.pbar['pbar{}'.format(info['id'])].setValue(self.step['step{}'.format(info['id'])])

            self.setUp = locals()
            self.setUp['setUp{}'.format(info['id'])] = QPushButton(QIcon(""), u"设置", self)
            self.setUp['setUp{}'.format(info['id'])].setObjectName('{}'.format(info['id']))
            self.setUp['setUp{}'.format(info['id'])].clicked.connect(lambda:self.addNewControl(self.sender().objectName()))

            self.delUp = locals()
            self.delUp['delUp{}'.format(info['id'])] = QPushButton(QIcon(""), u"删除", self)
            self.delUp['delUp{}'.format(info['id'])].setObjectName('{}'.format(info['id']))
            self.delUp['delUp{}'.format(info['id'])].clicked.connect(lambda: self.delOldControl(self.sender().objectName()))

            self.conLayout.addWidget(self.MapButton['MapButton{}'.format(info['id'])], self.key, 1)
            self.conLayout.addWidget(self.pbar['pbar{}'.format(info['id'])], self.key, 3)
            self.conLayout.addWidget(self.setUp['setUp{}'.format(info['id'])], self.key, 5)
            self.conLayout.addWidget(self.delUp['delUp{}'.format(info['id'])], self.key, 6)

            self.key+=1

        self.pageContent = QLabel(self.topFiller)
        self.pageContent.setStyleSheet('max-height:50px;')
        self.conLayout.addWidget(self.pageContent, 8, 3,1,4)

        self.conLayout_page = QGridLayout(self.pageContent)
        self.indexBtn = QPushButton(QIcon(""), u"首页", self.pageContent)
        self.indexBtn.clicked.connect(self.homePage)

        self.conLayout_page.addWidget(self.indexBtn, 1, 1)

        self.lastPageBtn = QPushButton(QIcon(""), u"< 上一页", self.pageContent)
        self.lastPageBtn.clicked.connect(self.lastPage)
        self.conLayout_page.addWidget(self.lastPageBtn, 1, 2)
        self.page = QLabel(self.topFiller)
        self.page.setText('{}'.format(self.page_now))
        self.conLayout_page.addWidget(self.page, 1, 3)
        self.nextPageBtn = QPushButton(QIcon(""), u"下一页 >", self.pageContent)
        self.nextPageBtn.clicked.connect(self.nextPage)
        self.conLayout_page.addWidget(self.nextPageBtn, 1, 4)
        self.endPageBtn = QPushButton(QIcon(""), u"尾页", self.pageContent)
        self.endPageBtn.clicked.connect(self.endPage)
        self.conLayout_page.addWidget(self.endPageBtn, 1, 5)
        self.formto = QLabel(self.topFiller)
        self.formto.setText('共 {} 页，跳到'.format(self.page_count))
        self.conLayout_page.addWidget(self.formto, 1, 6)

        pageValidator = QDoubleValidator(0, 100000, 0, self.pageContent)
        self.pageInput = QLineEdit()
        self.pageInput.setValidator(pageValidator)

        self.conLayout_page.addWidget(self.pageInput, 1, 7)
        self.yetext = QLabel(self.topFiller)
        self.yetext.setText('页')
        self.conLayout_page.addWidget(self.yetext, 1, 8)
        self.pageAlright = QPushButton(QIcon(""), u"确定", self.pageContent)
        self.pageAlright.clicked.connect(self.pageturn)
        self.conLayout_page.addWidget(self.pageAlright, 1, 9)

        self.conLayout.setParent(self.topFiller)

        ##创建一个滚动条
        self.scroll = QScrollArea()
        self.scroll.setWidget(self.topFiller)

        self.vbox = QVBoxLayout()
        self.vbox.addWidget(self.scroll)
        self.tab1.setLayout(self.vbox)

        str = "QTabBar::tab:select{color:white;background-color:#00a0e9;min-height:36px;border: 0px solid;min-width:136px;padding-left:5px}"+\
              "QTabBar::tab:selected{color:#00a0e9;background-color:white;min-height:36px;border: 0px solid;min-width:136px;padding-left:5px}"
        self.tabWidget.setStyleSheet(str)
        self.tabWidget.addTab(self.tab1, QIcon(self.resource_path("list-icon.png")),'软件列表')

        self.tabWidget.setGeometry(QRect(122, 40, 68, 68))

        #设置信号每隔20s刷新进度条
        self.sendTest = testStart()
        self.sendTest.finishSignal_pc_up.connect(self.is_start)
        self.sendTest.start()

    def pageturn(self):
        if len(self.pageInput.text()) > 0:
            page = int(self.pageInput.text())
            if page >= self.page_count:
                self.endPage()
                return
            else:
                self.page_num = (page-1)*6

            self.searchTask(2)

    def homePage(self):
        self.page_num = 0
        self.page_now = 1
        self.page.setText('{}'.format(self.page_now))
        self.searchTask(2)


    def endPage(self):
        try:
            if self.taskdataCount % 6 == 0:
                self.page_num = self.taskdataCount - 6
            else:
                self.page_num = self.taskdataCount - self.taskdataCount % 6
                if self.page_num == 0:
                    return
            self.page_now = self.page_count
            self.page.setText('{}'.format(self.page_now))
            self.searchTask(2)
        except Exception as e:
            print(e)

    def lastPage(self):
        if self.page_num <= 0:
            self.page_num = 0
            self.page_now = 1
            self.page.setText('{}'.format(self.page_now))
            return
        self.page_num = self.page_num-6
        self.page_now -= 1
        self.page.setText('{}'.format(self.page_now))
        self.searchTask(2)

    def nextPage(self):
        if self.page_now >= self.page_count:
            QMessageBox.information(self, u"提示", u"这是最后一页了")
            return
        self.page_num = self.page_num+6
        self.page_now += 1
        self.page.setText('{}'.format(self.page_now))
        self.searchTask(2)

    def searchTask(self,type):
        #搜索任务并重载任务列表
        try:
            search = self.search.text()
            self.clearTaskALl()
            if type == 2:
                self.taskdata = taskModel.getListTask(tparms_f['admin_id'],self.page_num,self.limit,search)
            else:
                self.taskdata = taskModel.getListTask(tparms_f['admin_id'],search=search)
            self.taskdataCount = taskModel.getListTaskCount(tparms_f['admin_id'],search)
            self.key = 2
            for info in self.taskdata:

                self.tparms = locals()
                self.tparms['tparms{}'.format(info['id'])] = {'admin_id': info['admin_id'],'name':'{}'.format(info['name']),'task_id':'{}'.format(info['id']),'username':'{}'.format(info['username']),'password':'{}'.format(info['password']),'token':'{}'.format(info['token']),'config_id':'{}'.format(info['config_id'])}

                self.MapButton['MapButton{}'.format(info['id'])] = QLabel(self)
                self.MapButton['MapButton{}'.format(info['id'])].setText(u'{}'.format(info['name']))
                self.MapButton['MapButton{}'.format(info['id'])].setStyleSheet("border:0px solid;max-height:30px;color:black")

                self.pbar['pbar{}'.format(info['id'])] = QProgressBar(self)
                self.timer['timer{}'.format(info['id'])] = QBasicTimer()
                self.timer['timer{}'.format(info['id'])].start(0, self)
                self.step['step{}'.format(info['id'])] = int(info['speed'])
                self.pbar['pbar{}'.format(info['id'])].setStyleSheet('border-radius:15px;font-size:12px;color:white')
                self.pbar['pbar{}'.format(info['id'])].setAlignment(Qt.AlignRight)
                self.pbar['pbar{}'.format(info['id'])].setValue(self.step['step{}'.format(info['id'])])

                self.setUp = locals()
                self.setUp['setUp{}'.format(info['id'])] = QPushButton(QIcon(""), u"设置", self)
                self.setUp['setUp{}'.format(info['id'])].setObjectName('{}'.format(info['id']))
                self.setUp['setUp{}'.format(info['id'])].clicked.connect(lambda:self.addNewControl(self.sender().objectName()))

                self.delUp = locals()
                self.delUp['delUp{}'.format(info['id'])] = QPushButton(QIcon(""), u"删除", self)
                self.delUp['delUp{}'.format(info['id'])].setObjectName('{}'.format(info['id']))
                self.delUp['delUp{}'.format(info['id'])].clicked.connect(lambda: self.delOldControl(self.sender().objectName()))

                self.conLayout.addWidget(self.MapButton['MapButton{}'.format(info['id'])], self.key, 1)
                self.conLayout.addWidget(self.pbar['pbar{}'.format(info['id'])], self.key, 3)
                self.conLayout.addWidget(self.setUp['setUp{}'.format(info['id'])], self.key, 5)
                self.conLayout.addWidget(self.delUp['delUp{}'.format(info['id'])], self.key, 6)

                self.key+=1

        except Exception as e:
            print(e)

    def clearTaskALl(self):
        #清除任务列表
        for info in self.taskdata:
            try:
                self.conLayout.removeWidget(self.MapButton['MapButton{}'.format(info['id'])])
                sip.delete(self.MapButton['MapButton{}'.format(info['id'])])
                self.conLayout.removeWidget(self.pbar['pbar{}'.format(info['id'])])
                sip.delete(self.pbar['pbar{}'.format(info['id'])])
                self.conLayout.removeWidget(self.setUp['setUp{}'.format(info['id'])])
                sip.delete(self.setUp['setUp{}'.format(info['id'])])
                self.conLayout.removeWidget(self.delUp['delUp{}'.format(info['id'])])
                sip.delete(self.delUp['delUp{}'.format(info['id'])])
            except Exception as e:
                print(e)

    def addTaskNow(self):
        try:
            text, ok = QInputDialog.getText(self, '新建任务', '输入任务名称：')

            if ok and text:
                result = taskModel.getTask(tparms_f['admin_id'],str(text))
                if len(result) > 0:
                    msg_box = QMessageBox.information(self,
                                                      "警告",
                                                      "该名称已存在",
                                                      QMessageBox.Yes)
                result = taskModel.addTask(str(text),1,tparms_f['admin_id'])
                self.addTaskNowList(str(text))
                self.searchTask(2)
        except Exception as e:
            print(e)

    def addTaskNowList(self,text):
        #新建任务，添加必要信息，并重载任务列表
        info = taskModel.getTaskInfo(tparms_f['admin_id'],text)

        configureModel.addConfig('默认配置',info['id'])
        configid = configureModel.getInfo(info['id'])
        taskModel.updateConfig(info['id'],configid[0]['id'])
        info['config_id'] = configid[0]['id']

        sentenceModel.addPageInfo(tparms_f['admin_id'],'【段落1】',info['id'],info['config_id'])
        sentenceModel.addPageInfo(tparms_f['admin_id'],'【段落2】',info['id'],info['config_id'])
        sentenceModel.addPageInfo(tparms_f['admin_id'],'【段落3】',info['id'],info['config_id'])
        sentenceModel.addPageInfo(tparms_f['admin_id'],'【段落4】',info['id'],info['config_id'])
        sentenceModel.addPageInfo(tparms_f['admin_id'],'【段落5】',info['id'],info['config_id'])
        sentenceModel.addPageInfo(tparms_f['admin_id'],'【段落6】',info['id'],info['config_id'])

        self.taskdataCount = taskModel.getListTaskCount(tparms_f['admin_id'])
        self.page_count = ceil(self.taskdataCount / 6)
        if self.page_count == self.page_now:
            self.tparms = locals()
            self.tparms['tparms{}'.format(info['id'])] = {'admin_id': info['admin_id'], 'name': '{}'.format(info['name']),
                                                          'task_id': '{}'.format(info['id']),
                                                          'username': '{}'.format(info['username']),
                                                          'password': '{}'.format(info['password']),
                                                          'token':'{}'.format(info['token']),
                                                          'config_id':'{}'.format(info['config_id'])}
            self.taskdata.append(info)

            self.MapButton['MapButton{}'.format(info['id'])] = QLabel(self)
            self.MapButton['MapButton{}'.format(info['id'])].setText(u'{}'.format(info['name']))
            self.MapButton['MapButton{}'.format(info['id'])].setStyleSheet("border:0px solid;max-height:30px;color:black")

            self.pbar['pbar{}'.format(info['id'])] = QProgressBar(self)
            self.timer['timer{}'.format(info['id'])] = QBasicTimer()
            self.timer['timer{}'.format(info['id'])].start(0, self)
            self.step['step{}'.format(info['id'])] = int(info['speed'])
            self.pbar['pbar{}'.format(info['id'])].setStyleSheet('border-radius:15px;font-size:12px;color:white')
            self.pbar['pbar{}'.format(info['id'])].setAlignment(Qt.AlignRight)
            self.pbar['pbar{}'.format(info['id'])].setValue(self.step['step{}'.format(info['id'])])

            self.setUp = locals()
            self.setUp['setUp{}'.format(info['id'])] = QPushButton(QIcon(""), u"设置", self)
            self.setUp['setUp{}'.format(info['id'])].setObjectName('{}'.format(info['id']))
            self.setUp['setUp{}'.format(info['id'])].clicked.connect(lambda: self.addNewControl(self.sender().objectName()))

            self.delUp = locals()
            self.delUp['delUp{}'.format(info['id'])] = QPushButton(QIcon(""), u"删除", self)
            self.delUp['delUp{}'.format(info['id'])].setObjectName('{}'.format(info['id']))
            self.delUp['delUp{}'.format(info['id'])].clicked.connect(lambda: self.delOldControl(self.sender().objectName()))

            self.conLayout.addWidget(self.MapButton['MapButton{}'.format(info['id'])], self.key, 1)
            self.conLayout.addWidget(self.pbar['pbar{}'.format(info['id'])], self.key, 3)
            self.conLayout.addWidget(self.setUp['setUp{}'.format(info['id'])], self.key, 5)
            self.conLayout.addWidget(self.delUp['delUp{}'.format(info['id'])], self.key, 6)

        self.key+=1

    def is_start(self):
        try:
            data = taskModel.getListTask(tparms_f['admin_id'])
            for info in data:
                self.pbar['pbar{}'.format(info['id'])].setValue(int(info['speed']))
        except Exception as e:
            print(e)

    def delOldControl(self, number):
        reply = QMessageBox.question(self, '注意', '确认要删除吗? （删除后需重启软件）',
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

        if reply == QMessageBox.Yes:
            tparms = self.tparms['tparms{}'.format(number)]

            taskModel.delUserInfo(tparms['task_id'])
            self.close()
        else:
            pass

    def addNewControl(self,number):
        #打开任务（设置）
        try:
            self.resize(1100,740)

            self.tparms['tparms{}'.format(number)] = taskModel.getTaskOne(self.tparms['tparms{}'.format(number)]['task_id'])
            tparms = self.tparms['tparms{}'.format(number)]
            config = configureModel.getInfoIdForId(tparms['config_id'])
            tparms['config_name'] = config['name']

            self.tabCentralControl[tparms['admin_id']] = QWidget()

            self.layoutCentralControl = QHBoxLayout(self.tabCentralControl[tparms['admin_id']], spacing=0)
            self.layoutCentralControl.setContentsMargins(0, 0, 0, 0)
            # 左侧列表
            self.listWidget = QListWidget(self.tabCentralControl[tparms['admin_id']])
            self.listWidget.setFixedHeight(500)

            self.listWidget.setStyleSheet('min-width: 142px;max-width: 142px;')
            self.layoutCentralControl.addWidget(self.listWidget)
            # 右侧层叠窗口

            self.stackedWidget = QStackedWidget(self.tabCentralControl[tparms['admin_id']])
            self.layoutCentralControl.addWidget(self.stackedWidget)

            self.sendList = []

            self.clearBtn_Cloud1 = QComboBox(self.tabCentralControl[tparms['admin_id']])
            self.addConfigBtn = QPushButton(QIcon(""), u"添加配置", self.tabCentralControl[tparms['admin_id']])
            self.addConfigBtn.setFixedWidth(100)
            self.addConfigBtn.setGeometry(QRect(40, 30, 140, 30))
            self.addConfigBtn.clicked.connect(lambda: self.addConfig(tparms))
            self.deleteConfigBtn = QPushButton(QIcon(""), u"删除", self.tabCentralControl[tparms['admin_id']])
            self.deleteConfigBtn.setGeometry(QRect(0, 30, 140, 30))
            self.deleteConfigBtn.setFixedWidth(40)
            self.deleteConfigBtn.clicked.connect(lambda: self.deleteConfig(tparms, number))
            self.testConfig(tparms)
            self.clearBtn_Cloud1.setGeometry(QRect(0, 0, 140, 30))
            self.clearBtn_Cloud1.activated[str].connect(lambda: self.changeOption(number))

            self.initUi(tparms,number)
            self.tabWidget.addTab(self.tabCentralControl[tparms['admin_id']],QIcon(self.resource_path("user.png")),tparms['name'])

        except Exception as e:
            print(e)

    def initUi(self,tparms,number):
        # 初始化界面
        # 通过QListWidget的当前item变化来切换QStackedWidget中的序号
        if len(self.tparms['tparms{}'.format(number)]['username']) > 0:
            result = apiAll.Login_in(self.tparms['tparms{}'.format(number)]['username'],
                                     self.tparms['tparms{}'.format(number)]['password'],
                                     self.tparms['tparms{}'.format(number)]['task_id'])
            if result['errno'] == 0:
                taskModel.updateToken(self.tparms['tparms{}'.format(number)]['task_id'], result['token'])
                tparms['token'] = result['token']
        self.setWindowTitle(u"智享云·闪投系统 {}".format(tparms_f['version']))
        self.tparms_info = tparms
        self.listWidget.currentRowChanged.connect(
            self.stackedWidget.setCurrentIndex)
        # 去掉边框
        self.listWidget.setFrameShape(QListWidget.NoFrame)
        # 隐藏滚动条
        self.listWidget.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.listWidget.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        for i in range(6):
            if i == 0:
                item = QListWidgetItem(QIcon(self.resource_path('userSet.png')), str('账号登录'),
                                                 self.listWidget)
                # 设置item的默认宽高
                item.setSizeHint(QSize(16777215, 60))
                # 文字居中
                item.setTextAlignment(Qt.AlignCenter)
            elif i == 1:
                self.item = QListWidgetItem(QIcon(self.resource_path('set.png')), str('通用设置'),
                                                 self.listWidget)
                self.item.setSizeHint(QSize(16777215, 60))
                self.item.setTextAlignment(Qt.AlignCenter)
            elif i == 2:
                item = QListWidgetItem(QIcon(self.resource_path('images.png')), str('图片管理'),
                                                 self.listWidget)
                item.setSizeHint(QSize(16777215, 60))
                item.setTextAlignment(Qt.AlignCenter)
            elif i == 3:
                item = QListWidgetItem(QIcon(self.resource_path('title.png')), str('标题组合'),
                                                 self.listWidget)
                item.setSizeHint(QSize(16777215, 60))
                item.setTextAlignment(Qt.AlignCenter)
            elif i == 4:
                item = QListWidgetItem(QIcon(self.resource_path('content.png')), str('内容模板'),
                                                 self.listWidget)
                item.setSizeHint(QSize(16777215, 60))
                item.setTextAlignment(Qt.AlignCenter)
            elif i == 5:
                is_run = 0
                if '发布控制({})'.format(tparms['config_name']) in self.sendList:
                    is_run = 1

                if is_run == 0:
                    item = QListWidgetItem(QIcon(self.resource_path('go.png')), str('发布控制({})'.format(tparms['config_name'])),
                                                     self.listWidget)
                    item.setSizeHint(QSize(16777215, 60))
                    item.setTextAlignment(Qt.AlignCenter)

        for i in range(6):
            #登录模块
            if i == 0:
                login_font = QFont()
                login_font.setPointSize(13)
                self.loginTab = QWidget()
                self.loginTab.setStyleSheet("background-color:#1c91ce")

                conLayoutBody = QGridLayout()
                self.loginTab.setLayout(conLayoutBody)

                self.topBox = QLabel("", self.loginTab)
                conLayoutBody.addWidget(self.topBox, 1, 1)

                self.loginTabBox = QWidget(self.loginTab)
                self.loginTabBox.setFixedHeight(500)
                conLayoutBody.addWidget(self.loginTabBox, 2, 1)
                label_title = QLabel("", self.loginTabBox)
                label_title.setText('信息发布平台')
                label_title.setStyleSheet("font-size:15px;color:#ffffff")
                label_title.setGeometry(QRect(445, 111, 150, 17))

                self.lineEdit_user = QLineEdit(u"", self.loginTabBox)
                self.lineEdit_user.setPlaceholderText(u"请输入您的账号")
                if str(self.tparms_info['username']) != 'None':
                    self.lineEdit_user.setText(str(self.tparms_info['username']))

                self.lineEdit_user.setGeometry(QRect(393, 170, 202, 36))
                self.lineEdit_user.setStyleSheet(
                    "border-bottom:1px solid;border-radius:5px;padding:2px 4px;color:#ffffff")
                self.lineEdit_user.setFont(login_font)

                self.lineEdit_passwd = QLineEdit(u'', self.loginTabBox)
                self.lineEdit_passwd.setPlaceholderText(u"请输入您的密码")
                self.lineEdit_passwd.setGeometry(QRect(393, 218, 202, 36))
                if str(self.tparms_info['password']) != 'None':
                    self.lineEdit_passwd.setText(str(self.tparms_info['password']))
                self.lineEdit_passwd.setStyleSheet(
                    "border-bottom:1px solid;border-radius:5px;padding:2px 4px;color:#ffffff")
                self.lineEdit_passwd.setFont(login_font)
                self.lineEdit_passwd.setEchoMode(QLineEdit.Password)

                self.pushButton_login = QPushButton(QIcon(""), u"登录", self.loginTabBox)
                self.pushButton_login.setGeometry(QRect(393, 292, 202, 36))
                self.pushButton_login.setStyleSheet(
                    "border:0px groove gray;border-radius:10px;padding:2px 4px;background-color:#262b2e;color:#ffffff;")
                self.pushButton_login.clicked.connect(self.log_in)

                self.topBox2 = QLabel("", self.loginTab)
                conLayoutBody.addWidget(self.topBox2, 3, 1)

                self.stackedWidget.addWidget(self.loginTab)


            #通用设置模块
            elif i == 1:
                self.allSet = QWidget()
                conLayoutGoType = QGridLayout(self.allSet)
                ##创建一个滚动条
                self.boxLeftallSet = QWidget(self.allSet)
                self.conLayoutGoTypeLeft = QGridLayout(self.boxLeftallSet)
                self.boxLeftallSetTitle_text = QLabel(self.boxLeftallSet)
                self.boxLeftallSetTitle_text.setText(u'参数设置')
                self.boxLeftallSetTitle_Refresh = QPushButton(QIcon(""), u"刷新", self.boxLeftallSet)
                self.boxLeftallSetTitle_Refresh.clicked.connect(self.optionSetUi)
                self.conLayoutGoTypeLeft.addWidget(self.boxLeftallSetTitle_text, 1, 1)
                self.conLayoutGoTypeLeft.addWidget(self.boxLeftallSetTitle_Refresh, 1, 2)
                self.optionSetUi(1)

                self.boxRightallSet= QLabel(self.allSet) #right
                self.conLayoutGoTypeRight = QGridLayout(self.boxRightallSet)
                self.boxRightallSetTitle_text = QLabel(self.boxRightallSet)
                self.boxRightallSetTitle_text.setText(u'产品参数')
                self.boxRightallSetTitle_Refresh = QPushButton(QIcon(""), u"刷新", self.boxRightallSet)
                self.boxRightallSetTitle_Refresh.clicked.connect(self.loadingProduct)
                self.conLayoutGoTypeRight.addWidget(self.boxRightallSetTitle_text, 1, 1)
                self.conLayoutGoTypeRight.addWidget(self.boxRightallSetTitle_Refresh, 1, 2)

                conLayoutGoType.addWidget(self.boxLeftallSet, 1, 1)
                conLayoutGoType.addWidget(self.boxRightallSet, 1, 2)

                self.stackedWidget.addWidget(self.allSet)

            #图片管理模块
            elif i == 2:
                self.ImgSet = QWidget()
                layout = QGridLayout(self.ImgSet)
                layout.addWidget(TabWidgetImages(tparms, tabPosition=TabWidgetImages.North), 0, 1)
                self.stackedWidget.addWidget(self.ImgSet)
            #标题组合模块
            elif i == 3:
                self.TitleSet = QWidget()
                layout = QGridLayout(self.TitleSet)
                layout.addWidget(TabWidgetTitle(tparms,tabPosition=TabWidgetTitle.North), 0, 1)
                self.stackedWidget.addWidget(self.TitleSet)
            #内容模板模块
            elif i == 4:
                self.contentSet = Content(tparms)
                self.stackedWidget.addWidget(self.contentSet)
            elif i == 5:
                if is_run == 0:
                    self.sendSet = Send(tparms)
                    self.stackedWidget.addWidget(self.sendSet)


    def testConfig(self,tparms):
        #设置默认选中配置列表
        self.clearBtn_Cloud1.clear()
        configList = configureModel.getInfo(tparms['task_id'])
        num = 0
        run = 0
        for info in configList:
            if info['id'] == int(tparms['config_id']):
                num = run
                taskModel.updateConfig(tparms['task_id'], info['id'])
            run+=1
            self.clearBtn_Cloud1.addItem('{}'.format(info['name']))
        self.clearBtn_Cloud1.setCurrentIndex(num)

    def deleteConfig(self,tparms,number):
        #删除配置
        reply = QMessageBox.question(self, '注意', '确认要删除吗? ',
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            list = configureModel.getInfo(tparms['task_id'])
            if len(list) <= 1:
                msg_box = QMessageBox.information(self,
                                                  "警告",
                                                  "至少留一个配置",
                                                  QMessageBox.Yes)
                return
            configureModel.updateStatus(self.tparms['tparms{}'.format(number)]['config_id'])
            self.testConfig(tparms)
            self.changeOption(number)

    def addConfig(self,tparms):
        #添加配置
        try:
            text, ok = QInputDialog.getText(self, '新建配置', '输入配置名称：')
            if ok and text:
                result = configureModel.getDataName(str(text), tparms['task_id'])
                if result is not None:
                    msg_box = QMessageBox.information(self,
                                                      "警告",
                                                      "该名称已存在",
                                                      QMessageBox.Yes)

                    return
                result = configureModel.addConfig(str(text),tparms['task_id'])
                result = configureModel.getDataName(str(text), tparms['task_id'])
                #新配置添加新段落
                sentenceModel.addPageInfo(tparms_f['admin_id'], '【段落1】', tparms['task_id'], result[0])
                sentenceModel.addPageInfo(tparms_f['admin_id'], '【段落2】', tparms['task_id'], result[0])
                sentenceModel.addPageInfo(tparms_f['admin_id'], '【段落3】', tparms['task_id'], result[0])
                sentenceModel.addPageInfo(tparms_f['admin_id'], '【段落4】', tparms['task_id'], result[0])
                sentenceModel.addPageInfo(tparms_f['admin_id'], '【段落5】', tparms['task_id'], result[0])
                sentenceModel.addPageInfo(tparms_f['admin_id'], '【段落6】', tparms['task_id'], result[0])
                self.testConfig(tparms)
        except Exception as e:
            print(e)

    def resource_path(self, relative):
        if hasattr(sys, "_MEIPASS"):
            return os.path.join(sys._MEIPASS, relative)
        return os.path.join(relative)

    def changeOption(self,number):
        #切换配置
        configName = self.clearBtn_Cloud1.currentText()
        config = configureModel.getInfoIdForName(configName,self.tparms['tparms{}'.format(number)]['task_id'])

        #获取当前配置下 任务是否正在发送
        config_send = configureModel.getInfoIdForId(self.tparms['tparms{}'.format(number)]['config_id'])

        self.stackedWidget.removeWidget(self.loginTab)
        self.stackedWidget.removeWidget(self.allSet)
        self.stackedWidget.removeWidget(self.ImgSet)
        self.stackedWidget.removeWidget(self.TitleSet)
        self.stackedWidget.removeWidget(self.contentSet)

        count = self.listWidget.count()
        # 遍历listwidget中的内容
        is_run = 0
        try:
            if config_send['is_send'] == 1:
                #如发送则添加至正在发送列表
                if '发布控制({})'.format(config_send['name']) not in self.sendList:
                    self.sendList.append('发布控制({})'.format(config_send['name']))

            for i in range(count):
                #循环所有左侧列表
                if config_send['is_send'] == 1:
                    if '发布控制({})'.format(config_send['name']) in self.listWidget.item(is_run).text():
                        is_run+=1
                        continue
                for name in self.sendList:
                    if self.listWidget.item(is_run).text() in name:
                        is_run += 1
                        continue
                self.listWidget.takeItem(is_run)
        except Exception as e:
            print(e)
        try:
            if config_send['is_send'] == 0:
                self.stackedWidget.removeWidget(self.sendSet)
        except Exception as e:
            print(e)
        self.tparms['tparms{}'.format(number)] = taskModel.getTaskOne(self.tparms['tparms{}'.format(number)]['task_id'])
        self.tparms['tparms{}'.format(number)]['config_id'] = config['id']
        self.tparms['tparms{}'.format(number)]['config_name'] = config['name']
        taskModel.updateConfig(self.tparms['tparms{}'.format(number)]['task_id'], self.tparms['tparms{}'.format(number)]['config_id'])
        self.initUi(self.tparms['tparms{}'.format(number)],number)

    def optionSetUi(self,type=None):
        num = 2
        start = 1
        self.inputBasics = locals()
        self.inputLabel = locals()
        self.textEdit = locals()
        select1 = 1
        select2 = 1
        select3 = 1
        input = 1
        radio = 1
        checkbox = 1
        textarea = 1

        self.goods_id = 0
        self.select1 = ''
        self.select2 = ''
        self.select3 = ''
        self.tparms_info = taskModel.getTaskOne(self.tparms_info['task_id'])
        if self.tparms_info['token'] != 'None':
            self.infoList = apiAll.getOption(self.tparms_info['token'])
            infotest = optionModel.titleComposeData(self.tparms_info['admin_id'],self.tparms_info['task_id'],'set_compose',self.tparms_info['config_id'])
            if self.infoList['errno'] == 0:
                num = 2
                start = 1
                self.inputBasics = locals()
                self.inputLabel = locals()
                self.textEditBox = locals()
                self.inputBasicsBox = locals()
                self.textEdit = locals()
                select1 = 1
                select2 = 1
                select3 = 1
                input = 1
                radio = 1
                checkbox = 1
                textarea = 1

                self.goods_id = 0
                self.select1 = ''
                self.select2 = ''
                self.select3 = ''
                for info in self.infoList['data']:
                    if info['type'] == 'select':
                        self.inputLabel['label-{}'.format(start)] = QLabel(self.boxLeftallSet)
                        self.inputLabel['label-{}'.format(start)].setText(u'* {}'.format(info['title']))
                        self.inputLabel['label-{}'.format(start)].setFixedWidth(110)
                        self.inputLabel['label-{}'.format(start)].setStyleSheet('max-height:40px;min-height40px')

                        self.inputBasics['select-{}'.format(select1)] = QComboBox(self)
                        self.inputBasics['select-{}'.format(select1)].setStyleSheet('min-height:30px')
                        is_select1_ok = 0
                        is_select1_num = 0
                        for det in info['data']:
                            self.inputBasics['select-{}'.format(select1)].addItem(det['val'])
                            if len(infotest) > 0 and det['key'] == infotest['goodsType']:
                                is_select1_num = is_select1_ok
                            is_select1_ok+=1
                        self.inputBasics['select-{}'.format(select1)].setCurrentIndex(is_select1_num)
                        self.conLayoutGoTypeLeft.addWidget(self.inputLabel['label-{}'.format(select1)], num, 1)
                        self.conLayoutGoTypeLeft.addWidget(self.inputBasics['select-{}'.format(select1)], num, 2)
                        select1+=1

                    elif info['type'] == 'select2':
                        self.inputLabel['label-{}'.format(start)] = QLabel(self.boxLeftallSet)
                        self.inputLabel['label-{}'.format(start)].setText(u'{}'.format(info['title']))
                        self.inputLabel['label-{}'.format(start)].setStyleSheet('max-height:40px;min-height40px')

                        self.inputBasics['select2-{}'.format(select2)] = QComboBox(self)
                        self.inputBasics['select2-{}'.format(select2)].setStyleSheet('min-height:30px')
                        self.inputBasics['select2-{}'.format(select2)].addItem('未选择')

                        is_select2_ok = 1
                        is_select2_num = 0
                        for det in info['data']:
                            self.inputBasics['select2-{}'.format(select2)].addItem(det['catName'])
                            if len(infotest) > 0 and det['catId'] == infotest['shopCatId']:
                                is_select2_num = is_select2_ok
                            is_select2_ok+=1
                        self.inputBasics['select2-{}'.format(select2)].setCurrentIndex(is_select2_num)
                        self.conLayoutGoTypeLeft.addWidget(self.inputLabel['label-{}'.format(start)], num, 1)
                        self.conLayoutGoTypeLeft.addWidget(self.inputBasics['select2-{}'.format(select2)], num, 2)
                        select2 += 1

                    elif info['type'] == 'select3':
                        self.inputLabel['label-{}'.format(start)] = QLabel(self.boxLeftallSet)
                        self.inputLabel['label-{}'.format(start)].setText(u'* {}'.format(info['title']))
                        self.inputLabel['label-{}'.format(start)].setStyleSheet('max-height:40px;min-height40px')

                        self.classData = info
                        self.select3Qlabel = QLabel(self)
                        self.select3Qlabel.setStyleSheet('min-height:50px;')
                        self.conLayoutGoTypeLeft_select3Qlabel = QGridLayout(self.select3Qlabel)

                        self.inputBasics['select3-1'] = QComboBox(self)
                        self.inputBasics['select3-1'].setStyleSheet('min-height:30px')
                        self.inputBasics['select3-1'].activated[str].connect(self.myClass)
                        self.inputBasics['select3-2'] = QComboBox(self)
                        self.inputBasics['select3-2'].setStyleSheet('min-height:30px')
                        self.inputBasics['select3-2'].activated[str].connect(self.myClassTwo)

                        self.inputBasics['select3-3'] = QComboBox(self)
                        self.inputBasics['select3-3'].setStyleSheet('min-height:30px')

                        self.conLayoutGoTypeLeft_select3Qlabel.addWidget(self.inputBasics['select3-1'], num, 1)
                        self.conLayoutGoTypeLeft_select3Qlabel.addWidget(self.inputBasics['select3-2'], num, 2)
                        self.conLayoutGoTypeLeft_select3Qlabel.addWidget(self.inputBasics['select3-3'], num, 3)

                        select3_1_index = 0
                        select3_1_ok = 0
                        is_one_class = 0
                        for det1 in info['data']:
                            try:
                                if len(infotest) > 0 and det1['catId'] == infotest['goodsCatId_1']:
                                    select3_1_ok = select3_1_index
                                    self.myClass(det1['catName'])
                                    is_one_class+=1
                            except Exception as e:
                                select3_1_ok = 0
                            self.inputBasics['select3-1'].addItem(det1['catName'])
                            select3_1_index+=1
                        self.inputBasics['select3-1'].setCurrentIndex(select3_1_ok)

                        select3_2_index = 0
                        select3_2_ok = 0
                        is_two_class = 0
                        if is_one_class == 1:
                            for det1 in info['data']:
                                try:
                                    if len(infotest) > 0 and det1['catId'] == infotest['goodsCatId_1']:
                                        for det2 in det1['children']:
                                            try:
                                                if len(infotest) > 0 and det2['catId'] == infotest['goodsCatId_2']:
                                                    select3_2_ok = select3_2_index
                                                    self.myClassTwo(det2['catName'])
                                                    is_two_class+=1
                                            except Exception as e:
                                                select3_2_ok = 0
                                                self.inputBasics['select3-2'].addItem(det2['catName'])
                                            select3_2_index+=1
                                        self.inputBasics['select3-2'].setCurrentIndex(select3_2_ok)
                                except Exception as e:
                                    print(e)
                        else:
                            for det2 in info['data'][0]['children']:
                                try:
                                    if len(infotest) > 0 and det2['catId'] == infotest['goodsCatId_2']:
                                        select3_2_ok = select3_2_index
                                        self.myClassTwo(det2['catName'])
                                except Exception as e:
                                    select3_2_ok = 0
                                    self.inputBasics['select3-2'].addItem(det2['catName'])
                                select3_2_index += 1
                            self.inputBasics['select3-2'].setCurrentIndex(select3_2_ok)

                        select3_3_index = 0
                        select3_3_ok = 0
                        threeClass = self.inputBasics['select3-3'].currentText()
                        if len(threeClass) > 0:
                            if is_two_class == 1:
                                for det1 in info['data']:
                                    try:
                                        if len(infotest) > 0 and det1['catId'] == infotest['goodsCatId_1']:
                                            for det2 in det1['children']:
                                                try:
                                                    if len(infotest) > 0 and det2['catId'] == infotest['goodsCatId_2']:
                                                        self.inputBasics['select3-3'].clear()
                                                        for det3 in det2['children']:
                                                            try:
                                                                if len(infotest) > 0 and det3['catId'] == infotest['goodsCatId']:
                                                                    select3_3_ok = select3_3_index
                                                            except Exception as e:
                                                                select3_3_ok = 0
                                                            select3_3_index += 1
                                                            self.inputBasics['select3-3'].addItem(det3['catName'])
                                                        self.inputBasics['select3-3'].setCurrentIndex(select3_3_ok)
                                                except Exception as e:
                                                    for det3 in info['data'][0]['children'][0]['children']:
                                                        self.inputBasics['select3-3'].addItem(det3['catName'])
                                                    print(e)
                                    except Exception as e:
                                        print(e)
                            else:
                                for det3 in info['data'][0]['children'][0]['children']:
                                    self.inputBasics['select3-3'].addItem(det3['catName'])
                            self.inputBasics['select3-3'].setCurrentIndex(select3_3_ok)

                        self.conLayoutGoTypeLeft.addWidget(self.inputLabel['label-{}'.format(start)], num, 1)
                        self.conLayoutGoTypeLeft.addWidget(self.select3Qlabel, num, 2)

                    elif info['type'] == 'input':
                        self.inputLabel['input-attr-{}'.format(input)] = QLabel(self.boxLeftallSet)
                        if info['title'] in '市场价格' or  info['title'] in '店铺价格' or  info['title'] in '商品库存' or  info['title'] in '预警库存' or  info['title'] in '商品单位':
                            self.inputLabel['input-attr-{}'.format(input)].setText(u'* {}'.format(info['title']))
                        else:
                            self.inputLabel['input-attr-{}'.format(input)].setText(u'{}'.format(info['title']))

                        self.inputLabel['input-attr-{}'.format(input)].setStyleSheet('max-height:35px;min-height35px')

                        self.inputBasicsBox['inputbox-{}'.format(input)] = QLabel(self.boxLeftallSet)
                        self.inputBasics['input-{}'.format(input)] = QLineEdit(u"", self.inputBasicsBox['inputbox-{}'.format(input)])
                        self.inputBasics['input-{}'.format(input)].setFixedWidth(300)
                        if len(infotest) > 0 and info['title'] in '市场价格' :
                            self.inputBasics['input-{}'.format(input)].setText(str(infotest['marketPrice']))
                        if len(infotest) > 0 and  info['title'] in '店铺价格':
                            self.inputBasics['input-{}'.format(input)].setText(str(infotest['shopPrice']))
                        if len(infotest) > 0 and  info['title'] in '起批量':
                            self.inputBasics['input-{}'.format(input)].setText(str(infotest['minValue']))
                        if len(infotest) > 0 and  info['title'] in '最大批量':
                            self.inputBasics['input-{}'.format(input)].setText(str(infotest['maxValue']))
                        if len(infotest) > 0 and  info['title'] in '商品库存':
                            self.inputBasics['input-{}'.format(input)].setText(str(infotest['goodsStock']))
                        if len(infotest) > 0 and  info['title'] in '预警库存':
                            self.inputBasics['input-{}'.format(input)].setText(str(infotest['warnStock']))
                        if len(infotest) > 0 and  info['title'] in '商品单位':
                            self.inputBasics['input-{}'.format(input)].setText(str(infotest['goodsUnit']))

                        self.conLayoutGoTypeLeft.addWidget(self.inputLabel['input-attr-{}'.format(input)], num, 1)
                        self.conLayoutGoTypeLeft.addWidget(self.inputBasicsBox['inputbox-{}'.format(input)], num, 2)
                        input += 1

                    elif info['type'] == 'radio':
                        self.inputLabel['radio-attr-{}'.format(radio)] = QLabel(self.boxLeftallSet)
                        self.inputLabel['radio-attr-{}'.format(radio)].setText(u'* {}'.format(info['title']))
                        self.inputLabel['radio-attr-{}'.format(radio)].setStyleSheet('max-height:40px;min-height40px')

                        td = 1
                        self.radioQlabel = QLabel(self)
                        self.radioQlabel.setStyleSheet('min-height:30px;max-height:30px')
                        self.conLayoutGoTypeLeft_radio = QGridLayout(self.radioQlabel)

                        for det in info['data']:
                            self.inputBasics['radio-{}-{}'.format(td,radio)] = QRadioButton()  # 实例化一个选择的按钮
                            if td == 1 and len(infotest) == 0:
                                self.inputBasics['radio-{}-{}'.format(td,radio)].setChecked(True)  # 设置按钮点点击状态
                            if len(infotest) > 0:
                                if info['title'] == '商品状态' and det['key'] == infotest['isSale']:
                                    self.inputBasics['radio-{}-{}'.format(td,radio)].setChecked(True)
                            if len(infotest) > 0:
                                if info['title'] == '是否包邮' and det['key'] == infotest['isFreeShipping']:
                                    self.inputBasics['radio-{}-{}'.format(td,radio)].setChecked(True)

                            # self.inputBasics['radio-{}-{}'.format(td,radio)].setGeometry(QRect(100, 300, 100, 20))
                            self.inputBasics['radio-{}-{}'.format(td,radio)].setText(det['val'])
                            self.inputBasics['radio-{}-{}'.format(td,radio)].setStyleSheet('max-height:20px;min-height:20px')

                            self.conLayoutGoTypeLeft_radio.addWidget(self.inputBasics['radio-{}-{}'.format(td,radio)], num, td)
                            self.conLayoutGoTypeLeft.addWidget(self.inputLabel['radio-attr-{}'.format(radio)], num, 1)
                            self.conLayoutGoTypeLeft.addWidget(self.radioQlabel, num, 2)
                            td+=1
                        radio+=1
                    elif info['type'] == 'checkbox':
                        self.inputLabel['checkbox-attr-{}'.format(checkbox)] = QLabel(self.boxLeftallSet)
                        self.inputLabel['checkbox-attr-{}'.format(checkbox)].setText(u'* {}'.format(info['title']))
                        self.inputLabel['checkbox-attr-{}'.format(checkbox)].setStyleSheet('max-height:40px;min-height40px')

                        td = 1
                        self.checkQlabel = QLabel(self)
                        self.checkQlabel.setStyleSheet('min-height:30px;max-height:30px')
                        self.conLayoutGoTypeLeft_check = QGridLayout(self.checkQlabel)

                        for det in info['data']:
                            self.inputBasics['checkbox-{}-{}'.format(checkbox,td)] = QCheckBox(self)

                            if len(infotest) > 0:
                                attribute = re.split('[,]', infotest['attribute'])
                                if str(det['key']) in attribute:
                                    self.inputBasics['checkbox-{}-{}'.format(checkbox,td)].setChecked(True)  # 设置按钮点点击状态

                            self.inputBasics['checkbox-{}-{}'.format(checkbox,td)].setText(det['val'])
                            self.inputBasics['checkbox-{}-{}'.format(checkbox,td)].setStyleSheet('max-height:20px;min-height:20px')

                            self.conLayoutGoTypeLeft_check.addWidget(self.inputBasics['checkbox-{}-{}'.format(checkbox,td)], num, td)
                            self.conLayoutGoTypeLeft.addWidget(self.inputLabel['checkbox-attr-{}'.format(checkbox)], num, 1)
                            self.conLayoutGoTypeLeft.addWidget(self.checkQlabel, num, 2)
                            td+=1
                        checkbox += 1

                    elif info['type'] == 'textarea':
                        self.inputLabel['textarea-attr-{}'.format(textarea)] = QLabel(self.boxLeftallSet)
                        self.inputLabel['textarea-attr-{}'.format(textarea)].setText(u'{}'.format(info['title']))
                        self.inputLabel['textarea-attr-{}'.format(textarea)].setStyleSheet('max-height:80px;min-height80px')
                        self.textEditBox['textareabox-{}'.format(textarea)] = QLabel(self.boxLeftallSet)
                        self.textEditBox['textareabox-{}'.format(textarea)].setStyleSheet('min-height:80px')
                        self.textEdit['textarea-{}'.format(textarea)] = QTextEdit(self.textEditBox['textareabox-{}'.format(textarea)])
                        self.textEdit['textarea-{}'.format(textarea)].setFixedWidth(300)
                        self.textEdit['textarea-{}'.format(textarea)].setGeometry(0, 0, 300, 80)
                        if '商品促销信息' == info['title'] and len(infotest) > 0:
                            self.textEdit['textarea-{}'.format(textarea)].setText(infotest['goodsTips'])
                        self.conLayoutGoTypeLeft.addWidget(self.inputLabel['textarea-attr-{}'.format(textarea)], num, 1)
                        self.conLayoutGoTypeLeft.addWidget(self.textEditBox['textareabox-{}'.format(textarea)], num,2)
                        textarea+=1
                    start+=1
                    num+=1
                start+=1

                self.inputLabel['max_img'] = QLabel(self.boxLeftallSet)
                self.inputLabel['max_img'].setText('图片数量')
                self.inputLabel['max_img'].setStyleSheet('max-height:40px;min-height:40px')
                image_numberValidator = QDoubleValidator(0, 100000, 0, self.boxLeftallSet)
                self.inputBasicsBoxInfo = QLabel(self)
                if len(infotest) > 0:
                    self.inputBasics['input-images'] = QLineEdit(u"{}".format(infotest['image_number_max']), self.inputBasicsBoxInfo)
                else:
                    self.inputBasics['input-images'] = QLineEdit(u"5", self.inputBasicsBoxInfo)

                self.inputBasics['input-images'].setValidator(image_numberValidator)
                self.inputBasics['input-images'].setStyleSheet('max-height:30px;min-height:30px')

                self.conLayoutGoTypeLeft.addWidget(self.inputLabel['max_img'], start, 1)
                self.conLayoutGoTypeLeft.addWidget(self.inputBasicsBoxInfo, start, 2)
                start += 1
                self.saveSetting = QPushButton(QIcon(""), u"保存", self.boxLeftallSet)
                self.saveSetting.clicked.connect(lambda:self.saveInfo(start,select1,select2,input,radio,textarea,checkbox))

                self.conLayoutGoTypeLeft.addWidget(self.saveSetting, start, 2)
                self.attrData = {'data':{'attrs':[] , 'spec':[]}}
            else:
                if type != 1:
                    msg_box = QMessageBox.information(self,
                                                      "警告",
                                                      "{}".format(self.infoList['errmsg']),
                                                      QMessageBox.Yes)
        else:
            if type != 1:
                msg_box = QMessageBox.information(self,
                                                      "警告",
                                                      "请先登录",
                                                      QMessageBox.Yes)

    def handleActivated1(self, index):
        self.select1 = self.inputBasics['select3-1'].itemText(index)

    def handleActivated2(self, index):
        self.select2 = self.inputBasics['select3-2'].itemText(index)

    def handleActivated3(self, index):
        self.select3 = self.inputBasics['select3-3'].itemText(index)

    def myClass(self,s):
        # pass
        self.inputBasics['select3-2'].clear()
        self.inputBasics['select3-3'].clear()
        try:
            for det in self.classData['data']:
                if s in det['catName']:
                    for det2 in det['children']:
                        self.inputBasics['select3-2'].addItem(det2['catName'])
        except Exception as e:
            print(e)

    def myClassTwo(self, s):
        # pass
        self.inputBasics['select3-3'].clear()
        first = self.inputBasics['select3-1'].currentText()
        try:
            for det in self.classData['data']:
                if first in det['catName']:
                    for det2 in det['children']:
                        if s in det2['catName']:
                            for det3 in det2['children']:
                                self.inputBasics['select3-3'].addItem(det3['catName'])
        except Exception as e:
            print(e)

    def loadingProduct(self):
        self.tparms_info = taskModel.getTaskOne(self.tparms_info['task_id'])

        oneClass = self.inputBasics['select3-1'].currentText()
        twoClass = self.inputBasics['select3-2'].currentText()
        threeClass = self.inputBasics['select3-3'].currentText()
        goodsId = 0
        if len(oneClass) > 0:
            for det in self.classData['data']:
                if oneClass in det['catName']:
                    goodsId = det['catId']
                    if len(twoClass) > 0:
                        for det2 in det['children']:
                            if twoClass in det2['catName']:
                                goodsId = det2['catId']
                                if len(threeClass) > 0:
                                    for det3 in det2['children']:
                                        if threeClass in det3['catName']:
                                            goodsId = det3['catId']
                                            break
                                break
        self.attrData = apiAll.getProductAttr(self.tparms_info['token'],goodsId)
        data = self.attrData

        if data['errno'] == 1:
            QMessageBox.critical(self, u'注意', u'{}'.format(data['errmsg']))
            return
        self.attr_number_check = 2

        self.attr_number_text = 2

        self.attr_number_select = 2

        self.number_all = 2

        for i in range(self.conLayoutGoTypeRight.count()):
            self.conLayoutGoTypeRight.itemAt(i).widget().deleteLater()

        self.boxRightallSetTitle_text = QLabel(self.boxRightallSet)
        self.boxRightallSetTitle_text.setText(u'产品参数')
        self.boxRightallSetTitle_Refresh = QPushButton(QIcon(""), u"刷新", self.boxRightallSet)
        self.boxRightallSetTitle_Refresh.clicked.connect(self.loadingProduct)
        self.conLayoutGoTypeRight.addWidget(self.boxRightallSetTitle_text, 1, 1)
        self.conLayoutGoTypeRight.addWidget(self.boxRightallSetTitle_Refresh, 1, 2)
        self.spec_number = 2
        self.optionAttr = locals()
        self.optionAttrBox = locals()
        self.optionAttrInput = locals()

        try:
            if len(data['data']['attrs']) > 0:
                for info in data['data']['attrs']:
                    if info['attrType'] == 1:
                        self.optionAttr['label-check-{}'.format(self.attr_number_check)] = QLabel(self.boxRightallSet)
                        self.optionAttr['label-check-{}'.format(self.attr_number_check)].setText(u'{}'.format(info['attrName']))
                        self.optionAttr['label-check-{}'.format(self.attr_number_check)].setStyleSheet('max-height:40px;min-height40px')
                        self.optionAttr['label-check-{}'.format(self.attr_number_check)].setFixedWidth(80)
                        td = 1
                        checkQlabel = QLabel(self)
                        checkQlabel.setStyleSheet('min-height:30px;max-height:30px;min-width:360px')
                        conLayoutGoType_check = QGridLayout(checkQlabel)
                        check = re.split(',', info['attrVal'])
                        for det in check:
                            self.optionAttr['checkbox-{}-{}'.format(self.attr_number_check,td)] = QCheckBox(self)
                            self.optionAttr['checkbox-{}-{}'.format(self.attr_number_check,td)].setChecked(False)  # 设置按钮点点击状态
                            self.optionAttr['checkbox-{}-{}'.format(self.attr_number_check,td)].setGeometry(QRect(100, 330, 120, 25))
                            self.optionAttr['checkbox-{}-{}'.format(self.attr_number_check,td)].setText(det)
                            self.optionAttr['checkbox-{}-{}'.format(self.attr_number_check,td)].setStyleSheet('max-height:20px;min-height:20px')

                            conLayoutGoType_check.addWidget(self.optionAttr['checkbox-{}-{}'.format(self.attr_number_check,td)], self.number_all, td)

                            td += 1
                        self.conLayoutGoTypeRight.addWidget(self.optionAttr['label-check-{}'.format(self.attr_number_check)], self.number_all, 1)
                        self.conLayoutGoTypeRight.addWidget(checkQlabel, self.number_all, 2)
                        self.attr_number_check += 1
                    elif info['attrType'] == 2:
                        self.optionAttr['label-select-{}'.format(self.attr_number_select)] = QLabel(self.boxRightallSet)
                        self.optionAttr['label-select-{}'.format(self.attr_number_select)].setText(info['title'])
                        self.optionAttr['label-select-{}'.format(self.attr_number_select)].setFixedWidth(80)

                        self.optionAttr['select-{}'.format(self.attr_number_select)] = QComboBox(self)
                        self.optionAttr['select-{}'.format(self.attr_number_select)].setStyleSheet('min-height:30px')
                        option = re.split(',', info['attrVal'])
                        for det in option:
                            self.optionAttr['select-{}'.format(self.attr_number_select)].addItem(det)

                        self.conLayoutGoTypeRight.addWidget(self.optionAttr['label-select-{}'.format(self.attr_number_select)], self.number_all, 1)
                        self.conLayoutGoTypeRight.addWidget(self.optionAttr['select-{}'.format(self.attr_number_select)], self.number_all, 2)
                        self.attr_number_select+=1
                    elif info['attrType'] == 0:
                        self.optionAttr['label-input-{}'.format(self.attr_number_text)] = QLabel(self.boxRightallSet)
                        self.optionAttr['label-input-{}'.format(self.attr_number_text)].setText(u'{}'.format(info['attrName']))
                        self.optionAttr['label-input-{}'.format(self.attr_number_text)].setStyleSheet('max-height:40px;min-height40px')
                        self.optionAttr['label-input-{}'.format(self.attr_number_text)].setFixedWidth(80)

                        self.optionAttrInput['input-box-{}'.format(self.attr_number_text)] = QLabel(self)
                        self.optionAttr['input-{}'.format(self.attr_number_text)] = QLineEdit(u"", self.optionAttrInput['input-box-{}'.format(self.attr_number_text)])
                        self.optionAttr['input-{}'.format(self.attr_number_text)].setStyleSheet('max-height:40px;min-height40px')
                        self.optionAttr['input-{}'.format(self.attr_number_text)].setFixedWidth(300)

                        self.conLayoutGoTypeRight.addWidget(self.optionAttr['label-input-{}'.format(self.attr_number_text)], self.number_all, 1)
                        self.conLayoutGoTypeRight.addWidget(self.optionAttrInput['input-box-{}'.format(self.attr_number_text)], self.number_all , 2)
                        self.attr_number_text += 1
                    self.number_all += 1

            if len(data['data']['field']) > 0:

                self.startF = 1
                self.inputBasics_F = locals()
                self.inputLabel_F = locals()
                self.textEdit_F = locals()
                self.inputBasics_Box = locals()
                self.select_F1 = 1
                self.select_F2 = 1
                select3 = 1
                self.input_F = 1
                self.radio_F = 1
                self.checkbox_F = 1
                self.textarea_F = 1

                self.goods_id = 0
                self.select1 = ''
                self.select2 = ''
                self.select3 = ''

                for info in data['data']['field']:
                    if info['type'] == 'select':
                        self.inputLabel_F['label-{}'.format(self.startF)] = QLabel(self.boxRightallSet)
                        self.inputLabel_F['label-{}'.format(self.startF)].setFixedWidth(80)

                        if info['required'] == 1:
                            self.inputLabel_F['label-{}'.format(self.startF)].setText(u'* {}'.format(info['title']))
                        else:
                            self.inputLabel_F['label-{}'.format(self.startF)].setText(u'{}'.format(info['title']))
                        self.inputLabel_F['label-{}'.format(self.startF)].setStyleSheet('max-height:40px;min-height40px')

                        self.inputBasics_F['select-{}'.format(self.select_F1)] = QComboBox(self)
                        self.inputBasics_F['select-{}'.format(self.select_F1)].addItem('未选择')
                        self.inputBasics_F['select-{}'.format(self.select_F1)].setStyleSheet('min-height:30px')
                        is_select1_ok = 0
                        for det in info['data']:
                            self.inputBasics_F['select-{}'.format(self.select_F1)].addItem(det['brandName'])
                        self.conLayoutGoTypeRight.addWidget(self.inputLabel_F['label-{}'.format(self.select_F1)], self.number_all, 1)
                        self.conLayoutGoTypeRight.addWidget(self.inputBasics_F['select-{}'.format(self.select_F1)], self.number_all, 2)
                        self.select_F1 += 1
                        self.number_all+=1
                    elif info['type'] == 'select2':
                        self.inputLabel_F['label-{}'.format(self.startF)] = QLabel(self.boxRightallSet)
                        self.inputLabel_F['label-{}'.format(self.startF)].setFixedWidth(80)

                        if info['required'] == 1:
                            self.inputLabel_F['label-{}'.format(self.startF)].setText(u'* {}'.format(info['title']))
                        else:
                            self.inputLabel_F['label-{}'.format(self.startF)].setText(u'{}'.format(info['title']))
                        self.inputLabel_F['label-{}'.format(self.startF)].setStyleSheet('max-height:40px;min-height40px')

                        self.inputBasics_F['select2-{}'.format(self.select_F2)] = QComboBox(self)
                        self.inputBasics_F['select2-{}'.format(self.select_F2)].setStyleSheet('min-height:30px')
                        is_select2_ok = 0
                        is_select2_num = 0
                        for det in info['data']:
                            self.inputBasics_F['select2-{}'.format(self.select_F2)].addItem(det['catName'])
                        self.inputBasics_F['select2-{}'.format(self.select_F2)].setCurrentIndex(is_select2_num)
                        self.conLayoutGoTypeRight.addWidget(self.inputLabel_F['label-{}'.format(self.startF)], self.number_all, 1)
                        self.conLayoutGoTypeRight.addWidget(self.inputBasics_F['select2-{}'.format(self.select_F2)], self.number_all, 2)
                        self.select_F2 += 1
                        self.number_all+=1
                    elif info['type'] == 'select3':
                        self.inputLabel_F['label-{}'.format(self.startF)] = QLabel(self.boxRightallSet)
                        self.inputLabel_F['label-{}'.format(self.startF)].setFixedWidth(80)

                        if info['required'] == 1:
                            self.inputLabel_F['label-{}'.format(self.startF)].setText(u'* {}'.format(info['title']))
                        else:
                            self.inputLabel_F['label-{}'.format(self.startF)].setText(u'{}'.format(info['title']))
                        self.inputLabel_F['label-{}'.format(self.startF)].setStyleSheet('max-height:40px;min-height40px')

                        self.classData = info
                        self.select3Qlabel = QLabel(self)
                        self.select3Qlabel.setStyleSheet('min-height:50px;')
                        self.conLayoutGoTypeLeft_select3Qlabel = QGridLayout(self.select3Qlabel)

                        self.inputBasics_F['select3-1'] = QComboBox(self)
                        self.inputBasics_F['select3-1'].setStyleSheet('min-height:30px')
                        self.inputBasics_F['select3-1'].activated[str].connect(self.myClass)
                        self.inputBasics_F['select3-2'] = QComboBox(self)
                        self.inputBasics_F['select3-2'].setStyleSheet('min-height:30px')
                        self.inputBasics_F['select3-2'].activated[str].connect(self.myClassTwo)

                        self.inputBasics_F['select3-3'] = QComboBox(self)
                        self.inputBasics_F['select3-3'].setStyleSheet('min-height:30px')

                        self.conLayoutGoTypeLeft_select3Qlabel.addWidget(self.inputBasics_F['select3-1'], self.number_all, 1)
                        self.conLayoutGoTypeLeft_select3Qlabel.addWidget(self.inputBasics_F['select3-2'], self.number_all, 2)
                        self.conLayoutGoTypeLeft_select3Qlabel.addWidget(self.inputBasics_F['select3-3'], self.number_all, 3)

                        for det1 in info['data']:
                            self.inputBasics_F['select3-1'].addItem(det1['catName'])
                        for det2 in info['data'][0]['children']:
                            self.inputBasics_F['select3-2'].addItem(det2['catName'])
                        for det3 in info['data'][0]['children'][0]['children']:
                            self.inputBasics_F['select3-3'].addItem(det3['catName'])

                        self.conLayoutGoTypeRight.addWidget(self.inputLabel_F['label-{}'.format(self.startF)], self.number_all, 1)
                        self.conLayoutGoTypeRight.addWidget(self.select3Qlabel, self.number_all, 2)
                        self.number_all+=1
                    elif info['type'] == 'input':
                        self.inputLabel_F['input-attr-{}'.format(self.input_F)] = QLabel(self.boxRightallSet)
                        self.inputLabel_F['input-attr-{}'.format(self.input_F)].setFixedWidth(80)

                        if info['required'] == 1:
                            self.inputLabel_F['input-attr-{}'.format(self.input_F)].setText(u'* {}'.format(info['title']))
                        else:
                            self.inputLabel_F['input-attr-{}'.format(self.input_F)].setText(u'{}'.format(info['title']))

                        self.inputLabel_F['input-attr-{}'.format(self.input_F)].setStyleSheet(
                            'max-height:40px;min-height40px')

                        self.inputBasics_Box['input-box-{}'.format(self.input_F)] = QLabel(self)
                        self.inputBasics_F['input-{}'.format(self.input_F)] = QLineEdit(u"", self.inputBasics_Box['input-box-{}'.format(self.input_F)])
                        self.inputBasics_F['input-{}'.format(self.input_F)].setFixedWidth(300)

                        self.conLayoutGoTypeRight.addWidget(self.inputLabel_F['input-attr-{}'.format(self.input_F)], self.number_all, 1)
                        self.conLayoutGoTypeRight.addWidget(self.inputBasics_Box['input-box-{}'.format(self.input_F)], self.number_all, 2)
                        self.input_F += 1
                        self.number_all+=1
                    elif info['type'] == 'radio':
                        self.inputLabel_F['radio-attr-{}'.format(self.radio_F)] = QLabel(self.boxRightallSet)
                        self.inputLabel_F['radio-attr-{}'.format(self.radio_F)].setFixedWidth(80)

                        if info['required'] == 1:
                            self.inputLabel_F['radio-attr-{}'.format(self.radio_F)].setText(u'* {}'.format(info['title']))
                        else:
                            self.inputLabel_F['radio-attr-{}'.format(self.radio_F)].setText(u'{}'.format(info['title']))

                        self.inputLabel_F['radio-attr-{}'.format(self.radio_F)].setStyleSheet(
                            'max-height:40px;min-height40px')

                        td = 1
                        self.radioQlabel = QLabel(self)
                        self.radioQlabel.setStyleSheet('min-height:30px;max-height:30px')
                        self.conLayoutGoTypeLeft_radio = QGridLayout(self.radioQlabel)

                        for det in info['data']:
                            try:
                                self.inputBasics_F['radio-{}-{}'.format(td, self.radio_F)] = QRadioButton()  # 实例化一个选择的按钮
                                if td == 1:
                                    self.inputBasics_F['radio-{}-{}'.format(td, self.radio_F)].setChecked(True)  # 设置按钮点点击状态
                                elif info['title'] == '商品状态':
                                    self.inputBasics_F['radio-{}-{}'.format(td, self.radio_F)].setChecked(True)
                                elif info['title'] == '是否包邮':
                                    self.inputBasics_F['radio-{}-{}'.format(td, self.radio_F)].setChecked(True)

                                self.inputBasics_F['radio-{}-{}'.format(td, self.radio_F)].setGeometry(QRect(100, 300, 100, 20))
                                self.inputBasics_F['radio-{}-{}'.format(td, self.radio_F)].setText(det['val'])
                                self.inputBasics_F['radio-{}-{}'.format(td, self.radio_F)].setStyleSheet(
                                    'max-height:20px;min-height:20px')

                                self.conLayoutGoTypeLeft_radio.addWidget(
                                    self.inputBasics['radio-{}-{}'.format(td, self.radio_F)], self.number_all, td)
                                self.conLayoutGoTypeRight.addWidget(self.inputLabel_F['radio-attr-{}'.format(self.radio_F)], self.number_all,
                                                                   1)
                                self.conLayoutGoTypeRight.addWidget(self.radioQlabel, self.number_all, 2)
                            except Exception as e:
                                print(e)
                            td += 1
                        self.radio_F += 1
                        self.number_all+=1
                    elif info['type'] == 'checkbox':
                        self.inputLabel_F['checkbox-attr-{}'.format(self.checkbox_F)] = QLabel(self.boxRightallSet)
                        self.inputLabel_F['checkbox-attr-{}'.format(self.checkbox_F)].setFixedWidth(80)

                        if info['required'] == 1:
                            self.inputLabel_F['checkbox-attr-{}'.format(self.checkbox_F)].setText(u'* {}'.format(info['title']))
                        else:
                            self.inputLabel_F['checkbox-attr-{}'.format(self.checkbox_F)].setText(u'{}'.format(info['title']))

                        self.inputLabel_F['checkbox-attr-{}'.format(self.checkbox_F)].setStyleSheet(
                            'max-height:40px;min-height40px')

                        td = 1
                        self.checkQlabel = QLabel(self)
                        self.checkQlabel.setStyleSheet('min-height:30px;max-height:30px')
                        self.conLayoutGoTypeLeft_check = QGridLayout(self.checkQlabel)

                        for det in info['data']:
                            self.inputBasics_F['checkbox-{}-{}'.format(self.checkbox_F, td)] = QCheckBox(self)
                            self.inputBasics_F['checkbox-{}-{}'.format(self.checkbox_F, td)].setGeometry(
                                QRect(100, 330, 120, 25))
                            self.inputBasics_F['checkbox-{}-{}'.format(self.checkbox_F, td)].setText(det['val'])
                            self.inputBasics_F['checkbox-{}-{}'.format(self.checkbox_F, td)].setStyleSheet(
                                'max-height:20px;min-height:20px')

                            self.conLayoutGoTypeLeft_check.addWidget(
                                self.inputBasics_F['checkbox-{}-{}'.format(self.checkbox_F, td)], self.number_all, td)
                            self.conLayoutGoTypeRight.addWidget(self.inputLabel_F['checkbox-attr-{}'.format(self.checkbox_F)],
                                                               self.number_all, 1)
                            self.conLayoutGoTypeRight.addWidget(self.checkQlabel, self.number_all, 2)
                            td += 1
                        self.checkbox_F += 1
                        self.number_all+=1
                    elif info['type'] == 'textarea':
                        self.inputLabel_F['textarea-attr-{}'.format(self.textarea_F)] = QLabel(self.boxRightallSet)
                        self.inputLabel_F['textarea-attr-{}'.format(self.textarea_F)].setFixedWidth(80)

                        if info['required'] == 1:
                            self.inputLabel_F['textarea-attr-{}'.format(self.textarea_F)].setText(u'* {}'.format(info['title']))
                        else:
                            self.inputLabel_F['textarea-attr-{}'.format(self.textarea_F)].setText(u'{}'.format(info['title']))
                        self.inputLabel_F['textarea-attr-{}'.format(self.textarea_F)].setStyleSheet(
                            'max-height:40px;min-height40px')

                        self.textEdit_Box['textarea-box-{}'.format(self.textarea_F)] = QLabel(self)
                        self.textEdit_F['textarea-{}'.format(self.textarea_F)] = QTextEdit(self.textEdit_Box['textarea-box-{}'.format(self.textarea_F)])
                        self.textEdit_F['textarea-{}'.format(self.textarea_F)].setStyleSheet('margin-top:0')

                        self.conLayoutGoTypeRight.addWidget(self.inputLabel_F['textarea-attr-{}'.format(self.textarea_F)],
                                                           self.number_all, 1)
                        self.conLayoutGoTypeRight.addWidget(self.textEdit_Box['textarea-box-{}'.format(self.textarea_F)], self.number_all, 2)
                        self.number_all+=1
                        self.self.textarea_F+=1

        except Exception as e:
            print(e)
        try:
            for info in data['data']['spec']:
                self.optionAttr['label-spec-{}'.format(self.spec_number)] = QLabel(self.boxRightallSet)
                self.optionAttr['label-spec-{}'.format(self.spec_number)].setFixedWidth(80)
                self.optionAttr['label-spec-{}'.format(self.spec_number)].setText(u'{}'.format(info['catName']))
                self.optionAttr['label-spec-{}'.format(self.spec_number)].setStyleSheet('max-height:40px;min-height40px')

                self.optionAttrBox['input-box-{}'.format(self.spec_number)] = QLabel(self)
                self.optionAttr['input-spec-{}'.format(self.spec_number)] = QLineEdit(u"", self.optionAttrBox['input-box-{}'.format(self.spec_number)])
                self.optionAttr['input-spec-{}'.format(self.spec_number)].setStyleSheet('max-height:40px;min-height40px')

                self.conLayoutGoTypeRight.addWidget(self.optionAttr['label-spec-{}'.format(self.spec_number)], self.attr_number, 1)
                self.conLayoutGoTypeRight.addWidget(self.optionAttrBox['input-box-{}'.format(self.spec_number)], self.attr_number, 2)
                self.spec_number += 1
                self.attr_number += 1
        except Exception as e:
            print('没有spec')

    def saveInfo(self,key,select1,select2,input,radio,textarea,checkbox):

        image_number = self.inputBasics['input-images'].text()
        if int(image_number) < 1:
            msg_box = QMessageBox.information(self,
                                              "警告",
                                              "图片数量最少为1",
                                              QMessageBox.Yes)
            return
        if int(image_number) > 9:
            msg_box = QMessageBox.information(self,
                                              "警告",
                                              "图片数量最多10张",
                                              QMessageBox.Yes)
            return

        is_all_option = {'goodsType':'','shopCatId':'','goodsCatId':0,'marketPrice':'','shopPrice':'','minValue':'','maxValue':'','goodsStock':'','warnStock':'','goodsUnit':'','goodsTips':'','isSale':'','isFreeShipping':'','attribute':'','spec_ids':[],'spec':[],'attr':[],'field':[],'image_number_max':image_number,'goodsCatId_1':0,'goodsCatId_2':0,'shopClassId':0}
        for info in self.infoList['data']:
            if info['type'] == 'select':
                for i1 in range(1,select1):
                    str = self.inputBasics['select-{}'.format(i1)].currentText()
                    if len(info) > 0:
                        for cont in info['data']:
                            if str == cont['val']:
                                    is_all_option['goodsType'] = cont['key']

            elif info['type'] == 'select2':
                for i2 in range(1, select2):
                    str2 = self.inputBasics['select2-{}'.format(i2)].currentText()
                    if len(info) > 0:
                        for cont in info['data']:
                            print(222222211)
                            print(str2)
                            print(cont)
                            if str2 == cont['catName']:
                                is_all_option['shopCatId'] = cont['catId']

            elif info['type'] == 'select3':
                goodsCatId = 0
                goodsCatId_1 = self.inputBasics['select3-1'].currentText()
                goodsCatId_2 = self.inputBasics['select3-2'].currentText()
                goodsCatId_3 = self.inputBasics['select3-3'].currentText()
                for goodsCatIds_1 in info['data']:
                    if goodsCatIds_1['catName'] == goodsCatId_1:
                        goodsCatId = goodsCatIds_1['catId']
                        is_all_option['goodsCatId_1'] = goodsCatId
#                         # print(is_all_option)
                        for goodsCatIds_2 in goodsCatIds_1['children']:
                            if goodsCatIds_2['catName'] == goodsCatId_2:
#                                 # print(goodsCatIds_2)
                                goodsCatId = goodsCatIds_2['catId']
                                is_all_option['goodsCatId_2'] = goodsCatId
                                if len(goodsCatId_3) > 0:
                                    for goodsCatIds_3 in goodsCatIds_2['children']:
                                        if goodsCatId_3 == goodsCatIds_3['catName']:
                                            goodsCatId = goodsCatIds_3['catId']
                is_all_option['goodsCatId'] = goodsCatId
            elif info['type'] == 'input':
                for i3 in range(1, input):
                    attrList = self.inputLabel['input-attr-{}'.format(i3)].text()
                    inputext = self.inputBasics['input-{}'.format(i3)].text()

                    if attrList in info['title'] or attrList in '* '+info['title']:
                        is_all_option['{}'.format(info['name'])] = inputext
            elif info['type'] == 'textarea':
                for i4 in range(1, textarea):
                    attrList = self.inputLabel['textarea-attr-{}'.format(i4)].text()
                    Tips= self.textEdit['textarea-{}'.format(i4)].toPlainText()
                    if attrList in info['title'] or attrList in '* '+info['title']:
                        is_all_option['{}'.format(info['name'])] = Tips
            elif info['type'] == 'select2':
                for i2 in range(1, select2):
                    str2 = self.inputBasics['select2-{}'.format(i2)].currentText()
                    if len(info) > 0:
                        for cont in info['data']:
                            if cont['catName'] == str2:
                                is_all_option['shopCatId'] = cont['catId']
            elif info['type'] == 'radio':
                for i5 in range(1,radio):
                    attr = self.inputLabel['radio-attr-{}'.format(i5)].text()
                    radioId = ''
                    for i5_1 in range(1,5):
                        try:
                            if self.inputBasics['radio-{}-{}'.format(i5_1, i5)].isChecked():
                                radioext = self.inputBasics['radio-{}-{}'.format(i5_1, i5)].text()
                                for det in info['data']:
                                    if det['val'] == radioext:
                                        radioId = det['key']
                        except Exception as e:
                            continue
                    if attr in info['title'] or attr in '* '+info['title']:
                        is_all_option['{}'.format(info['name'])] = radioId
            elif info['type'] == 'checkbox':
                for i5 in range(1, checkbox):
                    attr = self.inputLabel['checkbox-attr-{}'.format(i5)].text()
                    radioId = []
                    for i5_1 in range(1, 5):
                        try:
                            if self.inputBasics['checkbox-{}-{}'.format(i5,i5_1)].isChecked():
                                radioext = self.inputBasics['checkbox-{}-{}'.format(i5,i5_1)].text()
                                for det in info['data']:
                                    if det['val'] == radioext:
                                        radioId.append(det['key'])
                        except Exception as e:
                            continue
                    try:
                        radioStr = ''
                        if len(radioId) > 0:
                            radioStr = ",".join('%s' %id for id in radioId)
                        if attr in info['title'] or attr in '* '+info['title']:
                            is_all_option['{}'.format(info['name'])] = radioStr
                    except Exception as e:
                        print(e)

        is_all_option['attr'] = []
        if len(self.attrData['data']['attrs']) > 0:
            anum = 0
            for info in self.attrData['data']['attrs']:
                for i2 in range(2, self.attr_number_check):
                    attrList = self.optionAttr['label-check-{}'.format(i2)].text()

                    infoList = []
                    for i5_1 in range(1, 5):
                        try:
                            if self.optionAttr['checkbox-{}-{}'.format(i2,i5_1)].isChecked():
                                text = self.optionAttr['checkbox-{}-{}'.format(i2,i5_1)].text()
                                if len(text) > 0:
                                    infoList.append(text)
                        except Exception as e:
                            continue
                    try:
                        if len(infoList) > 0:
                            if info['attrName'] in attrList:
                                if len(infoList) > 0:
                                    infotext222 = ",".join(id11 for id11 in infoList)
                                    infocheck = {'id':'attr_{}'.format(info['attrId']),'name':'{}'.format(infotext222)}
                                    is_all_option['attr'].append(infocheck)
                    except Exception as e:
                        print(e)
                for i3 in range(2, self.attr_number_text):
                    attrList = self.optionAttr['label-input-{}'.format(i3)].text()
                    inputext = self.optionAttr['input-{}'.format(i3)].text()
                    attrname = ''
                    if len(info['attrName']) > 0:
                        if info['attrName'] == attrList:
                            info = {'id':'attr_{}'.format(info['attrId']),'name':inputext}
                            is_all_option['attr'].append(info)
                            break
        if len(self.attrData['data']['spec']) > 0:
            anum = 0
            for info in self.attrData['data']['spec']:
                for i3 in range(2, self.spec_number):
                    attrList = self.optionAttr['label-spec-{}'.format(i3)].text()
                    inputext = self.optionAttr['input-spec-{}'.format(i3)].text()
                    attrname = ''
                    try:
                        if len(info['catName']) > 0:
                            if info['catName'] == attrList:
                                is_all_option['spec_ids'].append('{}_{}'.format(info['catId'],anum))
                                info = {'spec_name': 'specName_{}_{}'.format(info['catId'],anum), 'value': inputext}
                                is_all_option['spec'].append(info)
                                anum+=1
                                break
                    except Exception as e:
                        print(e)

        try:
            if len(self.attrData['data']['field']) > 0:
                anum = 0
                for info in self.attrData['data']['field']:
                    if info['type'] == 'input':
                        for i3_f in range(1, self.input_F):
                            attrList = self.inputLabel_F['input-attr-{}'.format(i3_f)].text()
                            inputext = self.inputBasics_F['input-{}'.format(i3_f)].text()

                            if attrList in info['title'] or attrList in '* '+info['title']:
                                infofn = {'name':'{}'.format(info['name']),'value':inputext}
                                is_all_option['field'].append(infofn)

                    if info['type'] == 'select':
                        for i1_f in range(1,self.select_F1):
                            str = self.inputBasics_F['select-{}'.format(i1_f)].currentText()
                            if len(info) > 0:
                                for cont in info['data']:
                                    if str == cont['brandName']:
                                        infofs = {'name': '{}'.format(info['name']), 'value': cont['brandId']}
                                        is_all_option['field'].append(infofs)

                    if info['type'] == 'select2':
                        for i2_f in range(1, self.select_F2):
                            str2 = self.inputBasics_F['select2-{}'.format(i2_f)].currentText()
                            if len(info) > 0:
                                for cont in info['data']:
                                    if str2 == cont['catName']:
                                        infofs2 = {'name': '{}'.format(info['name']), 'value': cont['catId']}
                                        is_all_option['field'].append(infofs2)

                    if info['type'] == 'select3':
                        goodsCatId = 0
                        goodsCatId_1 = self.inputBasics_F['select3-1'].currentText()
                        goodsCatId_2 = self.inputBasics_F['select3-2'].currentText()
                        goodsCatId_3 = self.inputBasics_F['select3-3'].currentText()
                        for goodsCatIds_1 in info['data']:
                            if goodsCatId_1 == goodsCatIds_1['catName']:
                                for goodsCatIds_2 in goodsCatIds_1['children']:
                                    if goodsCatId_2 == goodsCatIds_2['catName']:
                                        goodsCatId = goodsCatIds_2['catId']
                                        if len(goodsCatId_3) > 0:
                                            for goodsCatIds_3 in goodsCatIds_2['children']:
                                                if goodsCatId_3 == goodsCatIds_3['catName']:
                                                    goodsCatId = goodsCatIds_3['catId']
                        infofs3 = {'name': '{}'.format(info['name']), 'value': goodsCatId}
                        is_all_option['field'].append(infofs3)

                    if info['type'] == 'textarea':
                        for i4 in range(1, self.textarea_F):
                            attrList = self.inputLabel_F['textarea-attr-{}'.format(i4)].text()
                            Tips= self.textEdit_F['textarea-{}'.format(i4)].toPlainText()
                            if attrList in info['title'] or attrList in '* '+info['title']:
                                infofst = {'name': '{}'.format(info['name']), 'value': Tips}
                                is_all_option['field'].append(infofst)

                    if info['type'] == 'radio':
                        for i5 in range(1,self.radio_F):
                            attr = self.inputLabel_F['radio-attr-{}'.format(i5)].text()
                            radioId = ''
                            for i5_1 in range(1,5):
                                try:
                                    if self.inputBasics_F['radio-{}-{}'.format(i5_1, i5)].isChecked():
                                        radioext = self.inputBasics_F['radio-{}-{}'.format(i5_1, i5)].text()
                                        for det in info['data']:
                                            if det['val'] == radioext:
                                                radioId = det['key']
                                except Exception as e:
                                    continue
                            if attr in info['title'] or attr in '* '+info['title']:
                                infofst = {'name': '{}'.format(info['name']), 'value': radioId}
                                is_all_option['field'].append(infofst)

                    if info['type'] == 'checkbox':
                        for i5 in range(1, self.checkbox_F):
                            attr = self.inputLabel_F['checkbox-attr-{}'.format(i5)].text()
                            radioId = []
                            for i5_1 in range(1, 5):
                                try:
                                    if self.inputBasics_F['checkbox-{}-{}'.format(i5,i5_1)].isChecked():
                                        radioext = self.inputBasics_F['checkbox-{}-{}'.format(i5,i5_1)].text()
                                        for det in info['data']:
                                            if det['val'] == radioext:
                                                radioId.append(det['key'])
                                except Exception as e:
                                    continue
                            try:
                                radioStr = ''
                                if len(radioId) > 0:
                                    radioStr = ",".join('%s' %id for id in radioId)
                                if attr in info['title'] or attr in '* '+info['title']:
                                    infofst = {'name': '{}'.format(info['name']), 'value': radioStr}
                                    is_all_option['field'].append(infofst)
                            except Exception as e:
                                print(e)
        except Exception as e:
            print(e)

        try:
            optionModel.setComposeSave(self.tparms_info['admin_id'],is_all_option,self.tparms_info['task_id'],self.tparms_info['config_id'])
            QMessageBox.information(self, u'成功', u'保存成功')
        except Exception as e:
            print(e)

    def myClass2(self,s):
        try:
            for det in self.classData['data']:
                if s in det['catName']:
                    self.optionAttr['select3-2'].clear()
                    self.optionAttr['select3-3'].clear()
                    for det2 in det['children']:
                        self.optionAttr['select3-2'].addItem(det2['catName'])
        except Exception as e:
            print(e)

    def myClassTwo2(self, s):
        self.optionAttr['select3-3'].clear()
        first = self.optionAttr['select3-1'].itemText(0)
        try:
            for det in self.classData['data']:
                if first in det['catName']:
                    for det2 in det['children']:
                        if s in det2['catName']:
                            for det3 in det2['children']:
                                self.optionAttr['select3-3'].addItem(det3['catName'])
        except Exception as e:
            print(e)

    def log_in(self):
        try:
            username = str(self.lineEdit_user.text())
            password = str(self.lineEdit_passwd.text())
            if username != ''.join(username.split()):
                QMessageBox.critical(self, u'错误', u'账号不可输入空格')
                return
            if password != ''.join(password.split()):
                QMessageBox.critical(self, u'错误', u'密码不可输入空格')
                return
            result = apiAll.Login_in(username,password,self.tparms_info['task_id'])
            print(result)
            if result['errno'] == 0:
                taskModel.updateUserInfo(username,password,self.tparms_info['task_id'],result['data']['shopId'],result['token'])

                QMessageBox.information(self, u'成功', u'登录成功')
                # self.accept()
            else:
                QMessageBox.critical(self, u'错误', u'用户名或密码错误')
        except:
            QMessageBox.critical(self, u'错误', u'用户名或密码错误')
            return


    #背景
    def init(self):
        points.clear()
        # 链接的最小距离
        self.linkDist = min(self.screenWidth, self.screenHeight) / 2.4
        # 初始化点
        for _ in range(maxCircles * 3):
            points.append(Circle('', self.screenWidth, self.screenHeight))
        self.update()

    def closeTab(self, index):
        if index >= 1:
            self.tabWidget.removeTab(index)

    def showEvent(self, event):
        super(CircleLineWindow, self).showEvent(event)
        self._canDraw = True

    def hideEvent(self, event):
        super(CircleLineWindow, self).hideEvent(event)
        # 窗口最小化要停止绘制, 减少cpu占用
        self._canDraw = False

    def paintEvent(self, event):
        super(CircleLineWindow, self).paintEvent(event)
        if not self._canDraw:
            return
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setRenderHint(QPainter.SmoothPixmapTransform)
        self.draw(painter)

    def draw(self, painter):
        if circlePulse:
            global circleExp
            global circleExpSp
            if circleExp < circleExpMin or circleExp > circleExpMax:
                circleExpSp *= -1
            circleExp += circleExpSp

        painter.translate(self.screenWidth / 2, self.screenHeight / 2)

        if self._firstDraw:
            t = time()
        self.renderPoints(painter, points)
        if self._firstDraw:
            self._firstDraw = False
            # 此处有个比例关系用于设置timer的时间，如果初始窗口很小，没有比例会导致动画很快
            t = (time() - t) * 1000 * 2
            # 比例最大不能超过1920/800
            t = int(min(2.4, self.screenHeight / self.height()) * t) - 1
            t = t if t > 15 else 15  # 不能小于15s
#             # print('start timer(%d msec)' % t)
            # 开启定时器
            self._timer.start(t)

    def drawCircle(self, painter, circle):
        #         circle.radius *= circleExp
        if circle.background:
            circle.radius *= circleExp
        else:
            circle.radius /= circleExp
        radius = circle.radius

        r = radius * circleExp
        # 边框颜色设置透明度
        c = QColor(circle.borderColor)
        c.setAlphaF(circle.opacity)

        painter.save()
        if circle.filled == 'full':
            # 设置背景刷
            painter.setBrush(c)
            painter.setPen(Qt.NoPen)
        else:
            # 设置画笔
            painter.setPen(
                QPen(c, max(1, circleBorder * (radMin - circle.radius) / (radMin - radMax))))

        # 画实心圆或者圆圈
        painter.drawEllipse(circle.x - r, circle.y - r, 2 * r, 2 * r)
        painter.restore()

        if circle.filled == 'concentric':
            r = radius / 2
            # 画圆圈
            painter.save()
            painter.setBrush(Qt.NoBrush)
            painter.setPen(
                QPen(c, max(1, circleBorder * (radMin - circle.radius) / (radMin - radMax))))
            painter.drawEllipse(circle.x - r, circle.y - r, 2 * r, 2 * r)
            painter.restore()

        circle.x += circle.speedx
        circle.y += circle.speedy
        if (circle.opacity < maxOpacity):
            circle.opacity += 0.01
        circle.ttl -= 1

    def renderPoints(self, painter, circles):
        for i, circle in enumerate(circles):
            if circle.ttl < -20:
                # 重新初始化一个
                circle = Circle('', self.screenWidth, self.screenHeight)
                circles[i] = circle
            self.drawCircle(painter, circle)

        circles_len = len(circles)
        for i in range(circles_len - 1):
            for j in range(i + 1, circles_len):
                deltax = circles[i].x - circles[j].x
                deltay = circles[i].y - circles[j].y
                dist = pow(pow(deltax, 2) + pow(deltay, 2), 0.5)
                # if the circles are overlapping, no laser connecting them
                if dist <= circles[i].radius + circles[j].radius:
                    continue
                # otherwise we connect them only if the dist is < linkDist
                if dist < self.linkDist:
                    xi = (1 if circles[i].x < circles[j].x else -
                          1) * abs(circles[i].radius * deltax / dist)
                    yi = (1 if circles[i].y < circles[j].y else -
                          1) * abs(circles[i].radius * deltay / dist)
                    xj = (-1 if circles[i].x < circles[j].x else 1) * \
                        abs(circles[j].radius * deltax / dist)
                    yj = (-1 if circles[i].y < circles[j].y else 1) * \
                        abs(circles[j].radius * deltay / dist)
                    path = QPainterPath()
                    path.moveTo(circles[i].x + xi, circles[i].y + yi)
                    path.lineTo(circles[j].x + xj, circles[j].y + yj)
#                     samecolor = circles[i].color == circles[j].color
                    c = QColor(circles[i].borderColor)
                    c.setAlphaF(min(circles[i].opacity, circles[j].opacity)
                                * ((self.linkDist - dist) / self.linkDist))
                    painter.setPen(QPen(c, (
                        lineBorder * backgroundMlt if circles[i].background else lineBorder) * (
                        (self.linkDist - dist) / self.linkDist)))
                    painter.drawPath(path)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    login = Login()
    login.show()
    if login.exec_():
        # w = CityLead()
        w = CircleLineWindow()
        w.resize(1100,740)
        w.show()
    sys.exit(app.exec_())
