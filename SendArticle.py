from PyQt5.QtCore import QRect,Qt,QCoreApplication,QThread,pyqtSignal
from PyQt5.QtGui import QIcon,QDoubleValidator,QIntValidator
from PyQt5.QtWidgets import *
import sys
import titleModel
import xlwt
import SendWordModel
import re
import contentModel
import random
import sentenceModel
import titleVarModel
import threading
import configureModel
import albumModel
import apiAll
from math import ceil
import time
import datetime
import optionModel
import taskModel
import math
import sendOptionModel
from concurrent.futures import ThreadPoolExecutor

class Send(QTabWidget):

    def __init__(self,info, *args, **kwargs):
        super(Send, self).__init__(*args, **kwargs)
        self.tparms = info
        self.SendSetLeft = QWidget(self)
        self.SendSetLeft.setGeometry(QRect(0, 0, 604, 572))
        layout = QGridLayout(self)
        layout.addWidget(SendLeft(info,tabPosition=SendLeft.North))
        layout.setGeometry(QRect(0, 0,841,500))


class SendStartNow(QThread):
    finishSignal_pc_up = pyqtSignal(list)

    def __init__(self,tparms,info, *args, **kwargs):
        super(SendStartNow, self).__init__(*args, **kwargs)
        self.tparms = tparms
        self.info = info
        self.lock = threading.RLock()
    def run(self):
        self.lock.acquire()
        try:
            optionModel.setTitleSave(self.tparms['admin_id'],'',self.tparms['task_id'],self.tparms['config_id'])
            configureModel.updateSend(self.tparms['config_id'],1)
            try:
                readyInfo = titleModel.titleDataDai(self.tparms['admin_id'], self.tparms['task_id'],self.tparms['config_id'])
                if len(readyInfo) < 1:
                    self.finishSignal_pc_up.emit(['stop', 'send'])
                    return

                getContent = contentModel.getDataContentList(self.tparms['admin_id'], self.tparms['task_id'],self.tparms['config_id'])
                getZblContent = titleVarModel.getSendTitleVar(self.tparms['admin_id'], self.tparms['task_id'], 1,self.tparms['config_id'])
                getbl1Content = titleVarModel.getSendTitleVar(self.tparms['admin_id'], self.tparms['task_id'], 2,self.tparms['config_id'])
                getbl2Content = titleVarModel.getSendTitleVar(self.tparms['admin_id'], self.tparms['task_id'], 3,self.tparms['config_id'])
                getbl3Content = titleVarModel.getSendTitleVar(self.tparms['admin_id'], self.tparms['task_id'], 4,self.tparms['config_id'])
                getSenContent = sentenceModel.getSendSen(self.tparms['admin_id'], self.tparms['task_id'],self.tparms['config_id'])
                getTitle = titleModel.getSendTitle(self.tparms['admin_id'], self.tparms['task_id'],self.tparms['config_id'])
                minGan = SendWordModel.getDataListSend(self.tparms['admin_id'], self.tparms['task_id'],self.tparms['config_id'])
                pagList = sentenceModel.getPagDataListSend(self.tparms['admin_id'], self.tparms['task_id'],self.tparms['config_id'])
                title_compose = optionModel.titleComposeData(self.tparms['admin_id'], self.tparms['task_id'], 'title_compose',self.tparms['config_id'])
                set_compose = optionModel.titleComposeData(self.tparms['admin_id'], self.tparms['task_id'],'set_compose',self.tparms['config_id'])
                senPagAll = sentenceModel.getSendSenPag(self.tparms['task_id'], self.tparms['config_id'], pagList)
                self.is_ok = 0
                # 关键词过滤
                weigui = ['最','第一','唯一','TOP.1','独一无二','仅此一','首发','首选','首个','首款','独家','一流','顶级','永久','全球级','宇宙级','世界级','国家级','绝佳','免检','极品','极佳','销量冠军','独一无二','绝无仅有','史无前例','领导品牌','领袖品牌','创领品牌','世界领先','领导人推荐','机关推荐','机关专供']
                self.tparms['sendCount'] = len(readyInfo)
                pool = ThreadPoolExecutor(max_workers=1)
                for info in readyInfo:
                    pool.submit(self.sendInfo,info,getContent,pagList,minGan,weigui,getTitle,getZblContent,getbl1Content,getbl2Content,getbl3Content,getSenContent,title_compose,set_compose,senPagAll)

            except Exception as e:
                print(e)
        finally:
            self.lock.release()
    def getShop_id(self):
        getToken = taskModel.getToken(self.tparms['username'],self.tparms['task_id'])
        print(getToken)
        return getToken

    def sendInfo(self,info,getContent,pagList,minGan,weigui,getTitle,getZblContent,getbl1Content,getbl2Content,getbl3Content,getSenContent,title_compose,set_compose,senPagAll):
        if self.tparms['is_open'] == 1:
            try:
                status = titleModel.titleDataStatus(self.tparms['admin_id'], self.tparms['task_id'], info['id'],self.tparms['config_id'])
                if status == 0:
                    content = getContent[random.randint(0, len(getContent) - 1)]

                    titlenum = content.count('【标题】')
                    for i in range(titlenum):
                        namezhu = ''
                        if len(getTitle) > 0:
                            namezhu = getTitle[random.randint(0, len(getTitle) - 1)]
                        content = content.replace('【标题】', namezhu, 1)

                    zhuBlnum = content.count('【主变量】')
                    for i in range(zhuBlnum):
                        namezhu = ''
                        if len(getZblContent) > 0:
                            namezhu = getZblContent[random.randint(0, len(getZblContent) - 1)]
                        content = content.replace('【主变量】', namezhu, 1)

                    Bl1num = content.count('【变量1】')
                    for i in range(Bl1num):
                        name1 = ''
                        if len(getbl1Content) > 0:
                            name1 = getbl1Content[random.randint(0, len(getbl1Content) - 1)]
                        content = content.replace('【变量1】', name1, 1)
                    Bl2num = content.count('【变量2】')
                    for i in range(Bl2num):
                        name2 = ''
                        if len(getbl2Content) > 0:
                            name2 = getbl2Content[random.randint(0, len(getbl2Content) - 1)]
                        content = content.replace('【变量2】', name2, 1)
                    Bl3num = content.count('【变量3】')
                    for i in range(Bl3num):
                        name3 = ''
                        if len(getbl3Content) > 0:
                            name3 = getbl3Content[random.randint(0, len(getbl3Content) - 1)]
                        content = content.replace('【变量3】', name3, 1)
                    titleList = []
                    Imgnum = content.count('【图片】')
                    notWhere = ''
                    for i in range(Imgnum):
                        Img = albumModel.getSendImg(self.tparms['admin_id'], self.tparms['task_id'], 2,self.tparms['config_id'],notWhere)
                        print(Img)
                        if 'error' == str(Img[0]):
                            content = content.replace('【图片】',
                                                      '', 1)
                        elif '【图片】' in content:
                            notWhere = notWhere + '{},'.format(str(Img[0]))
                            print(2222222211)
                            print(Img[1])
                            titleList.append(Img[1])
                            content = content.replace('【图片】',
                                                      '<img src="{}" alt="{}"/>'.format(apiAll.website + '/' + Img[1],
                                                                                        info['title']), 1)
                        else:
                            break

                    sennum = content.count('【句子】')
                    for i in range(sennum):
                        sen = ''
                        if len(getSenContent) > 0:
                            senrand = random.randint(0, len(getSenContent) - 1)
                            sen = getSenContent[senrand]
                            del(getSenContent[senrand])
                        content = content.replace('【句子】', sen, 1)

                    isend = 0
                    for seninfo in senPagAll:
                        senstr = content.count(seninfo['name'])
                        for isen in range(senstr):
                            if seninfo['name'] in content:
                                senrandPag = random.randint(0, len(senPagAll[isend]['data']) - 1)
                                content = content.replace(senPagAll[isend]['name'],
                                                          str(senPagAll[isend]['data'][senrandPag][1]), 1)
                                del (senPagAll[isend]['data'][senrandPag])
                        isend += 1

                    if self.info['filter'] == 1 and self.info['zdy_filter'] == 1:
                        for word in minGan:
                            content = content.replace(word, '')

                    goodsSeoKeywordss = ''
                    for i in range(1, 6):
                        namezhu = ''
                        if len(getZblContent) > 0:
                            namezhu = getZblContent[random.randint(0, len(getZblContent) - 1)]
                        namebl1 = ''
                        if len(getbl1Content) > 0:
                            namebl1 = getbl1Content[random.randint(0, len(getbl1Content) - 1)]
                        namebl2 = ''
                        if len(getbl2Content) > 0:
                            namebl2 = getbl2Content[random.randint(0, len(getbl2Content) - 1)]
                        namebl3 = ''
                        if len(getbl3Content) > 0:
                            namebl3 = getbl3Content[random.randint(0, len(getbl3Content) - 1)]
                        title_compose['keyword_var{}'.format(i)] = title_compose['keyword_var{}'.format(i)].replace(
                            '【主变量】', namezhu)
                        title_compose['keyword_var{}'.format(i)] = title_compose['keyword_var{}'.format(i)].replace(
                            '【变量1】', namebl1)
                        title_compose['keyword_var{}'.format(i)] = title_compose['keyword_var{}'.format(i)].replace(
                            '【变量2】', namebl2)
                        title_compose['keyword_var{}'.format(i)] = title_compose['keyword_var{}'.format(i)].replace(
                            '【变量3】', namebl3)
                        if len(title_compose['keyword_var{}'.format(i)]) > 0:
                            goodsSeoKeywordss = title_compose['keyword_var{}'.format(i)] + ' ' + goodsSeoKeywordss

                    titleList = albumModel.titleImgDataSend(self.tparms['admin_id'], self.tparms['task_id'],set_compose['image_number_max'],self.tparms['config_id'])
                    random.shuffle(titleList)
                    titlegallery = ",".join(str(i) for i in titleList)
                    for weitext in weigui:
                        content = content.replace(weitext, '')
                    if len(goodsSeoKeywordss) == 0:
                        goodsSeoKeywordss = info['title']
                    data = {
                        'token': 'bb601ac9889346400b1b0b6715823cfb',
                        'shopId': self.getShop_id(),
                        'goodsName': info['title'],
                        'goodsSeoKeywords': goodsSeoKeywordss,
                        'goodsResume': info['title'],  # seo描述
                        'goodsDesc': content,  # 内容
                        'gallery': titlegallery,
                        'goodsType': set_compose['goodsType'],  # 一级分类
                        'marketPrice': set_compose['marketPrice'],
                        'shopPrice': set_compose['shopPrice'],
                        'minValue': set_compose['minValue'],
                        'maxValue': set_compose['maxValue'],
                        'goodsStock': set_compose['goodsStock'],
                        'warnStock': set_compose['warnStock'],
                        'goodsUnit': set_compose['goodsUnit'],
                        'goodsTips': set_compose['goodsTips'],
                        'isSale': set_compose['isSale'],
                        'attribute': set_compose['attribute'],
                        'isFreeShipping': set_compose['isFreeShipping'],
                        'shopCatId': set_compose['shopCatId'],  # 二级份额里
                        'goodsCatId': set_compose['goodsCatId'],  # 三级分类ID
                        'specsIds': "-".join(str(i) for i in set_compose['spec_ids']),
                        'defaultSpec': "-".join(str(i) for i in set_compose['spec_ids']),
                    }
                    print(data)
                    for infoA in set_compose['attr']:
                        data['{}'.format(infoA['id'])] = infoA['name']
                    for infoA in set_compose['spec']:
                        data['{}'.format(infoA['spec_name'])] = infoA['value']
                    for infoA in set_compose['field']:
                        data['{}'.format(infoA['name'])] = infoA['value']

                    result = apiAll.Sendinfo(data)
                    if '失败！token验证失败，请检查!' in result['errmsg'] or '请先登录' in result['errmsg'] or 'shopId不能为空' in result['errmsg']:
                        self.finishSignal_pc_up.emit(['continue', 'login'])
                        return
                    if result['errno'] == 0:
                        titleModel.updateStatus(self.tparms['admin_id'], self.tparms['task_id'], 1, info['id'],self.tparms['config_id'], '')
                    elif result['errno'] == 1:
                        titleModel.updateStatus(self.tparms['admin_id'], self.tparms['task_id'], 2, info['id'],self.tparms['config_id'],result['errmsg'])

                    self.is_ok += 1

                    step = math.floor(round(self.is_ok / self.tparms['sendCount'], 4) * 100)
                    taskModel.updateSpeed(self.tparms['task_id'], step)
                    if step == 100:
                        self.finishSignal_pc_up.emit(['success', 'send'])
                    if int(self.info['is_sendNumber']) == 1:
                        if self.is_ok >= int(self.info['max_send']):
                            self.finishSignal_pc_up.emit(['success', 'send'])
                    self.finishSignal_pc_up.emit(['continue', 'send'])
                    time.sleep(random.randint(int(self.info['start_rate']), int(self.info['end_rate'])))
            except Exception as e:
                print(e)

        if self.is_ok >= self.tparms['sendCount']:
            self.finishSignal_pc_up.emit(['success', 'send'])

class SendLeft(QTabWidget):
    changeValue = pyqtSignal()

    def __init__(self,tparms, *args, **kwargs):
        super(SendLeft, self).__init__(*args, **kwargs)
        self.tparms = tparms
        self.ready = 0
        self.is_run = 0
        self.is_false = 0

        conLayoutBody = QGridLayout()
        self.setLayout(conLayoutBody)
        self.BodyQtWidgetsTopLeft = QTabWidget(self)
        self.BodyQtWidgetsTopLeft.setFixedHeight(500)
        for i in range(3):
            if i == 0:
                self.titledataCountWei = titleModel.titleDataCount(self.tparms['admin_id'], self.tparms['task_id'], 0,self.tparms['config_id'])

                self.page_num = 0
                self.limit = 10
                self.page_now = 1
                self.page_count = ceil(self.titledataCountWei / 10)
                self.daiId = 1
                self.line_dai = []

                self.sendList = QWidget()
                self.sendList.setFixedHeight(423)
                conLayoutBody_tab1 = QGridLayout()
                self.sendList.setLayout(conLayoutBody_tab1)

                self.sendList_table = QTableWidget(self)
                self.sendList_table.setRowCount(0)
                self.sendList_table.setColumnCount(4)
                self.sendList_table.setParent(self.sendList)
                self.sendList_table.setEditTriggers(QAbstractItemView.DoubleClicked)
                self.sendList_table.setHorizontalHeaderLabels([u"ID", u"选择", "待发列表", u"状态"])
                self.sendList_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

                self.sendList_table.horizontalHeader().setDefaultSectionSize(50)
                self.sendList_table.horizontalHeader().setSectionResizeMode(0, QHeaderView.Fixed)
                self.sendList_table.horizontalHeader().setSectionResizeMode(1, QHeaderView.Fixed)
                self.sendList_table.horizontalHeader().setSectionResizeMode(3, QHeaderView.Fixed)
                self.sendList_table.setEditTriggers(QTableWidget.AnyKeyPressed)
                self.sendList_table.verticalHeader().setVisible(False)
                conLayoutBody_tab1.addWidget(self.sendList_table, 1, 1,1,9)

                self.indexBtn = QPushButton(QIcon(""), u"首页", self.sendList)
                self.indexBtn.clicked.connect(self.homePageSend)
                conLayoutBody_tab1.addWidget(self.indexBtn, 2, 1)

                self.lastPageBtn = QPushButton(QIcon(""), u"< 上一页", self.sendList)
                self.lastPageBtn.clicked.connect(self.lastPageSend)
                conLayoutBody_tab1.addWidget(self.lastPageBtn, 2, 2)

                self.page = QLabel(self.sendList)
                self.page.setText('{}'.format(10))
                self.page.setAlignment(Qt.AlignHCenter|Qt.AlignVCenter)
                conLayoutBody_tab1.addWidget(self.page, 2, 3)

                self.nextPageBtn = QPushButton(QIcon(""), u"下一页 >", self.sendList)
                self.nextPageBtn.clicked.connect(self.nextPageSend)
                conLayoutBody_tab1.addWidget(self.nextPageBtn, 2, 4)

                self.endPageBtn = QPushButton(QIcon(""), u"尾页", self.sendList)
                self.endPageBtn.clicked.connect(self.endPageSend)
                conLayoutBody_tab1.addWidget(self.endPageBtn, 2, 5)

                self.formto = QLabel(self.sendList)
                self.formto.setText('共{}页 到'.format(self.page_count))
                conLayoutBody_tab1.addWidget(self.formto, 2, 6)

                pageValidator = QDoubleValidator(0, 100000, 0, self.sendList)
                self.pageInput = QLineEdit(self.sendList)
                self.pageInput.setValidator(pageValidator)
                conLayoutBody_tab1.addWidget(self.pageInput, 2, 7)

                self.yetext = QLabel(self.sendList)
                self.yetext.setText('页')
                conLayoutBody_tab1.addWidget(self.yetext, 2, 8)

                self.pageAlright = QPushButton(QIcon(""), u"确定", self.sendList)
                self.pageAlright.clicked.connect(self.pageturn)
                conLayoutBody_tab1.addWidget(self.pageAlright, 2, 9)

                self.selectAll = QPushButton(QIcon(""), u"全选", self.sendList)
                self.selectAll.clicked.connect(self.selectSend)
                conLayoutBody_tab1.addWidget(self.selectAll, 3, 1)

                self.fanSelectAll = QPushButton(QIcon(""), u"反选", self.sendList)
                self.fanSelectAll.clicked.connect(self.selectSendFan)
                conLayoutBody_tab1.addWidget(self.fanSelectAll, 3, 2)

                self.delSelectedAll = QPushButton(QIcon(""), u"删除勾选", self.sendList)
                self.delSelectedAll.clicked.connect(self.selectDel)
                conLayoutBody_tab1.addWidget(self.delSelectedAll, 3, 3)

                self.delAll = QPushButton(QIcon(""), u"清空列表", self.sendList)
                self.delAll.clicked.connect(lambda: self.clearTitleDelete(0))
                conLayoutBody_tab1.addWidget(self.delAll, 3, 4)

                self.daoTitle = QPushButton(QIcon(""), u"导出标题", self.sendList)
                self.daoTitle.clicked.connect(self.down_title)
                conLayoutBody_tab1.addWidget(self.daoTitle, 3, 5)

                self.randTitle = QPushButton(QIcon(""), u"刷新", self.sendList)
                self.randTitle.setGeometry(360, 400, 55, 25)
                self.randTitle.clicked.connect(self.loadingInfoLeft)
                conLayoutBody_tab1.addWidget(self.randTitle, 3, 6)

                self.BodyQtWidgetsTopLeft.addTab(self.sendList, str('待发列表'))
            elif i == 1:
                self.titledataCountOk = titleModel.titleDataCount(self.tparms['admin_id'], self.tparms['task_id'], 1,self.tparms['config_id'])

                self.page_num_ok = 0
                self.limit_ok = 10
                self.page_now_ok = 1
                self.page_count_ok = ceil(self.titledataCountOk / 10)

                self.startId = 1
                self.line_ok = []

                self.sendListOk = QWidget()
                self.sendListOk.setFixedHeight(423)
                conLayoutBody_tab2 = QGridLayout()
                self.sendListOk.setLayout(conLayoutBody_tab2)

                self.sendList_tableOk = QTableWidget(self)
                self.sendList_tableOk.setRowCount(0)
                self.sendList_tableOk.setColumnCount(4)
                self.sendList_tableOk.setParent(self.sendListOk)
                self.sendList_tableOk.setEditTriggers(QAbstractItemView.DoubleClicked)
                self.sendList_tableOk.setHorizontalHeaderLabels([u"ID", u"选择", "发布列表", u"时间"])
                self.sendList_tableOk.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
                self.sendList_tableOk.horizontalHeader().setDefaultSectionSize(50)
                self.sendList_tableOk.horizontalHeader().setSectionResizeMode(0, QHeaderView.Fixed)
                self.sendList_tableOk.horizontalHeader().setSectionResizeMode(1, QHeaderView.Fixed)
                self.sendList_tableOk.setEditTriggers(QTableWidget.AnyKeyPressed)
                self.sendList_tableOk.verticalHeader().setVisible(False)
                conLayoutBody_tab2.addWidget(self.sendList_tableOk, 1, 1, 1, 9)



                self.indexBtn_ok = QPushButton(QIcon(""), u"首页", self.sendListOk)
                self.indexBtn_ok.clicked.connect(self.homePageSendOk)
                conLayoutBody_tab2.addWidget(self.indexBtn_ok, 2, 1)

                self.lastPageBtn_ok = QPushButton(QIcon(""), u"< 上一页", self.sendListOk)
                self.lastPageBtn_ok.clicked.connect(self.lastPageSendOk)
                conLayoutBody_tab2.addWidget(self.lastPageBtn_ok, 2, 2)

                self.page_ok = QLabel(self.sendListOk)
                self.page_ok.setText('{}'.format(10))
                self.page_ok.setFixedWidth(25)
                self.page_ok.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
                conLayoutBody_tab2.addWidget(self.page_ok, 2, 3)


                self.nextPageBtn_ok = QPushButton(QIcon(""), u"下一页 >", self.sendListOk)
                self.nextPageBtn_ok.clicked.connect(self.nextPageSendOk)
                conLayoutBody_tab2.addWidget(self.nextPageBtn_ok, 2, 4)

                self.endPageBtn_ok = QPushButton(QIcon(""), u"尾页", self.sendListOk)
                self.endPageBtn_ok.clicked.connect(self.endPageSendOk)
                conLayoutBody_tab2.addWidget(self.endPageBtn_ok, 2, 5)

                self.formto_ok = QLabel(self.sendListOk)
                self.formto_ok.setText('共{}页 到'.format(self.page_count_ok))
                conLayoutBody_tab2.addWidget(self.formto_ok, 2, 6)

                pageValidator = QDoubleValidator(0, 100000, 0, self.sendListOk)
                self.pageInput_ok = QLineEdit(self.sendListOk)
                self.pageInput_ok.setValidator(pageValidator)
                conLayoutBody_tab2.addWidget(self.pageInput_ok, 2, 7)

                self.yetext_ok = QLabel(self.sendListOk)
                self.yetext_ok.setText('页')
                conLayoutBody_tab2.addWidget(self.yetext_ok, 2, 8)

                self.pageAlright_ok = QPushButton(QIcon(""), u"确定", self.sendListOk)
                self.pageAlright_ok.clicked.connect(self.pageturnOk)
                conLayoutBody_tab2.addWidget(self.pageAlright_ok, 2, 9)

                self.delAll = QPushButton(QIcon(""), u"清空列表", self.sendListOk)
                self.delAll.clicked.connect(lambda: self.clearTitleDelete(1))
                conLayoutBody_tab2.addWidget(self.delAll, 3, 1)

                self.delSelectedAllOk = QPushButton(QIcon(""), u"删除勾选", self.sendListOk)
                self.delSelectedAllOk.clicked.connect(self.selectDelOk)
                conLayoutBody_tab2.addWidget(self.delSelectedAllOk, 3, 2)

                self.BodyQtWidgetsTopLeft.addTab(self.sendListOk, str('发布成功'))
            elif i == 2:
                self.titledataCountError = titleModel.titleDataCount(self.tparms['admin_id'], self.tparms['task_id'], 2,self.tparms['config_id'])

                self.page_num_Error = 0
                self.limit_Error = 10
                self.page_now_Error = 1
                self.page_count_Error = ceil(self.titledataCountError / 10)

                self.endId = 1
                self.line_error = []

                self.sendListError = QWidget()
                self.sendListError = QWidget()
                self.sendListError.setFixedHeight(423)
                conLayoutBody_tab3 = QGridLayout()
                self.sendListError.setLayout(conLayoutBody_tab3)

                self.sendList_tableError = QTableWidget(self)
                self.sendList_tableError.setRowCount(0)
                self.sendList_tableError.setColumnCount(5)
                self.sendList_tableError.setParent(self.sendListError)
                self.sendList_tableError.setGeometry(0, 0, 530, 350)
                self.sendList_tableError.setEditTriggers(QAbstractItemView.DoubleClicked)
                self.sendList_tableError.setHorizontalHeaderLabels([u"ID", u"选择", "失败列表", u"状态", u"时间"])
                self.sendList_tableError.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
                self.sendList_tableError.horizontalHeader().setDefaultSectionSize(50)
                self.sendList_tableError.horizontalHeader().setSectionResizeMode(0, QHeaderView.Fixed)
                self.sendList_tableError.horizontalHeader().setSectionResizeMode(1, QHeaderView.Fixed)
                self.sendList_tableError.setEditTriggers(QTableWidget.AnyKeyPressed)
                self.sendList_tableError.verticalHeader().setVisible(False)
                conLayoutBody_tab3.addWidget(self.sendList_tableError, 1, 1, 1, 9)


                try:
                    self.indexBtn_Error = QPushButton(QIcon(""), u"首页", self.sendListError)
                    self.indexBtn_Error.clicked.connect(self.homePageSendError)
                    conLayoutBody_tab3.addWidget(self.indexBtn_Error, 2,1)

                    self.lastPageBtn_Error = QPushButton(QIcon(""), u"< 上一页", self.sendListError)
                    self.lastPageBtn_Error.clicked.connect(self.lastPageSendError)
                    conLayoutBody_tab3.addWidget(self.lastPageBtn_Error, 2,2)

                    self.page_Error = QLabel(self.sendListError)
                    self.page_Error.setText('{}'.format(10))
                    self.page_Error.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
                    conLayoutBody_tab3.addWidget(self.page_Error, 2,3)

                    self.nextPageBtn_Error = QPushButton(QIcon(""), u"下一页 >", self.sendListError)
                    self.nextPageBtn_Error.clicked.connect(self.nextPageSendError)
                    conLayoutBody_tab3.addWidget(self.nextPageBtn_Error, 2,4)

                    self.endPageBtn_Error = QPushButton(QIcon(""), u"尾页", self.sendListError)
                    self.endPageBtn_Error.clicked.connect(self.endPageSendError)
                    conLayoutBody_tab3.addWidget(self.endPageBtn_Error, 2,5)

                    self.formto_Error = QLabel(self.sendListError)
                    self.formto_Error.setText('共{}页 到'.format(self.page_count_Error))
                    conLayoutBody_tab3.addWidget(self.formto_Error, 2,6)

                    pageValidator = QDoubleValidator(0, 100000, 0, self.sendListError)
                    self.pageInput_Error = QLineEdit(self.sendListError)
                    self.pageInput_Error.setValidator(pageValidator)
                    conLayoutBody_tab3.addWidget(self.pageInput_Error, 2,7)

                    self.yetext_Error = QLabel(self.sendListError)
                    self.yetext_Error.setText('页')
                    self.yetext_Error.setGeometry(450, 360, 50, 25)
                    conLayoutBody_tab3.addWidget(self.yetext_Error, 2,8)

                    self.pageAlright_Error = QPushButton(QIcon(""), u"确定", self.sendListError)
                    self.pageAlright_Error.setGeometry(475, 360, 55, 25)
                    self.pageAlright_Error.clicked.connect(self.pageturnError)
                    conLayoutBody_tab3.addWidget(self.pageAlright_Error, 2,9)

                    self.delAll = QPushButton(QIcon(""), u"清空列表", self.sendListError)
                    self.delAll.setGeometry(30, 400, 55, 25)
                    self.delAll.clicked.connect(lambda: self.clearTitleDelete(2))
                    conLayoutBody_tab3.addWidget(self.delAll, 3,1)

                    self.delSelectedAllError = QPushButton(QIcon(""), u"删除勾选", self.sendListError)
                    self.delSelectedAllError.setGeometry(95, 400, 55, 25)
                    self.delSelectedAllError.clicked.connect(self.selectDelError)
                    conLayoutBody_tab3.addWidget(self.delSelectedAllError, 3,2)

                except Exception as e:
                    print(e)

                self.BodyQtWidgetsTopLeft.addTab(self.sendListError, str('发布失败'))

        conLayoutBody.addWidget(self.BodyQtWidgetsTopLeft, 1, 1)

        self.SendSetRight = QWidget(self)
        self.SendSetRight.setFixedWidth(300)

        self.textMin = QLabel()
        self.textMin.setText(u'敏感词')
        self.textMin.setParent(self.SendSetRight)
        self.textMin.setGeometry(QRect(20, 0, 200, 50))

        self.filterRealTime = QCheckBox(self.SendSetRight)
        self.filterRealTime.setGeometry(QRect(100, 56, 80, 30))
        self.filterRealTime.setText(u'实时过滤')

        self.filterZdy = QCheckBox(self.SendSetRight)
        self.filterZdy.setGeometry(QRect(100, 100, 110, 30))
        self.filterZdy.setText(u'自定义敏感词')

        self.filterAdd_text = QPushButton(QIcon(""), u"敏感词添加", self.SendSetRight)
        self.filterAdd_text.setGeometry(100, 130, 100, 30)
        self.filterAdd_text.clicked.connect(self.addMinGan)

        self.sendSet = QLabel()
        self.sendSet.setText(u'发布控制')
        self.sendSet.setParent(self.SendSetRight)
        self.sendSet.setGeometry(QRect(20, 160, 200, 50))

        self.sendSet_Frequency = QLabel()
        self.sendSet_Frequency.setText(u'发布频率：')
        self.sendSet_Frequency.setParent(self.SendSetRight)
        self.sendSet_Frequency.setGeometry(QRect(20, 200, 80, 40))

        sendSet_Frequency_Start = QDoubleValidator(0, 100000, 0, self.SendSetRight)
        self.sendSet_Frequency_Start_num = QLineEdit(u"60", self.SendSetRight)
        self.sendSet_Frequency_Start_num.setValidator(sendSet_Frequency_Start)
        self.sendSet_Frequency_Start_num.setGeometry(QRect(100, 210, 60, 25))

        self.sendSet_Frequency_fuhao = QLabel()
        self.sendSet_Frequency_fuhao.setText(u'~')
        self.sendSet_Frequency_fuhao.setParent(self.SendSetRight)
        self.sendSet_Frequency_fuhao.setGeometry(QRect(170, 210, 20, 40))

        sendSet_Frequency_End = QDoubleValidator(0, 100000, 0, self.SendSetRight)
        self.sendSet_Frequency_End = QLineEdit(u"150", self.SendSetRight)
        self.sendSet_Frequency_End.setValidator(sendSet_Frequency_End)
        self.sendSet_Frequency_End.setGeometry(QRect(200, 210, 60, 25))

        self.sendSet_Frequency_miao = QLabel()
        self.sendSet_Frequency_miao.setText(u'秒')
        self.sendSet_Frequency_miao.setParent(self.SendSetRight)
        self.sendSet_Frequency_miao.setGeometry(QRect(280, 200, 20, 40))

        self.sendSet_Frequency_number_text = QLabel()
        self.sendSet_Frequency_number_text.setText(u'发布条数：')
        self.sendSet_Frequency_number_text.setParent(self.SendSetRight)
        self.sendSet_Frequency_number_text.setGeometry(QRect(20, 240, 80, 40))

        self.sendSet_Frequency_number_one = QRadioButton()  # 实例化一个选择的按钮
        self.sendSet_Frequency_number_one.setChecked(True)  # 设置按钮点点击状态
        self.sendSet_Frequency_number_one.setGeometry(QRect(100, 260, 200, 20))
        self.sendSet_Frequency_number_one.setParent(self.SendSetRight)
        self.sendSet_Frequency_number_one.setText(u'当天最大限额')

        self.sendSet_Frequency_number_zdy = QRadioButton("Button1")  # 实例化一个选择的按钮
        self.sendSet_Frequency_number_zdy.setChecked(False)  # 设置按钮点点击状态
        self.sendSet_Frequency_number_zdy.setGeometry(QRect(100, 300, 100, 20))
        self.sendSet_Frequency_number_zdy.setParent(self.SendSetRight)
        self.sendSet_Frequency_number_zdy.setText(u'自定义数量')

        sendSet_Frequency_zdy = QDoubleValidator(0, 100000, 0, self.SendSetRight)
        self.sendSet_Frequency_number_zdy_label = QLineEdit(u"100", self.SendSetRight)
        self.sendSet_Frequency_number_zdy_label.setValidator(sendSet_Frequency_End)
        self.sendSet_Frequency_number_zdy_label.setGeometry(QRect(220, 300, 60, 25))

        self.sendTask = QLabel()
        self.sendTask.setText(u'离线发布：')
        self.sendTask.setParent(self.SendSetRight)
        self.sendTask.setGeometry(QRect(20, 340, 200, 50))

        self.sendTask_time = QLabel()
        self.sendTask_time.setText(u'每日')
        self.sendTask_time.setParent(self.SendSetRight)
        self.sendTask_time.setGeometry(QRect(100, 365, 80, 40))
        sendOption = sendOptionModel.getOption(self.tparms['admin_id'],self.tparms['task_id'],self.tparms['config_id'])
        self.sendTask_Time_Start_num = QLineEdit(u"10", self.SendSetRight)
        if sendOption is not None:
            if sendOption[3] is not None:
                self.sendTask_Time_Start_num.setText('{}'.format(sendOption[3]))
        self.sendTask_Time_Start_num.setGeometry(QRect(140, 375, 40, 25))
        self.sendTask_Time_Start_num.setValidator(QIntValidator(0, 23))

        self.sendTask_Time_Start_fuhao = QLabel()
        self.sendTask_Time_Start_fuhao.setText(u':')
        self.sendTask_Time_Start_fuhao.setParent(self.SendSetRight)
        self.sendTask_Time_Start_fuhao.setGeometry(QRect(180, 365, 20, 40))

        self.sendTask_Time_Start_End = QLineEdit(u"0", self.SendSetRight)
        if sendOption is not None:
            if sendOption[4] is not None:
                self.sendTask_Time_Start_End.setText('{}'.format(sendOption[4]))
        self.sendTask_Time_Start_End.setGeometry(QRect(190, 375, 40, 25))
        self.sendTask_Time_Start_End.setValidator(QIntValidator(0, 59))

        conLayoutBody.addWidget(self.SendSetRight, 1, 2)

        self.sendTask_timefor = QLabel()
        self.sendTask_timefor.setText(u'间隔')
        self.sendTask_timefor.setParent(self.SendSetRight)
        self.sendTask_timefor.setGeometry(QRect(100, 395, 80, 40))

        self.sendTask_TimeFor_Start_num = QLineEdit(u"0", self.SendSetRight)
        if sendOption is not None:
            if sendOption[6] is not None:
                self.sendTask_TimeFor_Start_num.setText('{}'.format(sendOption[6]))
        self.sendTask_TimeFor_Start_num.setGeometry(QRect(140, 405, 40, 25))
        self.sendTask_TimeFor_Start_num.setValidator(QIntValidator(0, 23))

        self.sendTask_TimeFor_Start_fuhao = QLabel()
        self.sendTask_TimeFor_Start_fuhao.setText(u'时')
        self.sendTask_TimeFor_Start_fuhao.setParent(self.SendSetRight)
        self.sendTask_TimeFor_Start_fuhao.setGeometry(QRect(185, 395, 20, 40))

        self.sendTask_TimeFor_Start_End = QLineEdit(u"0", self.SendSetRight)
        if sendOption is not None:
            if sendOption[7] is not None:
                self.sendTask_TimeFor_Start_End.setText('{}'.format(sendOption[7]))
        self.sendTask_TimeFor_Start_End.setGeometry(QRect(200, 405, 40, 25))
        self.sendTask_TimeFor_Start_End.setValidator(QIntValidator(0, 59))

        self.sendTask_timefor_Start = QLabel()
        self.sendTask_timefor_Start.setText(u'分')
        self.sendTask_timefor_Start.setParent(self.SendSetRight)
        self.sendTask_timefor_Start.setGeometry(QRect(245, 405, 40, 25))

        self.sendTask_Dan = QLabel()
        self.sendTask_Dan.setText(u'单次发送')
        self.sendTask_Dan.setParent(self.SendSetRight)
        self.sendTask_Dan.setGeometry(QRect(70, 425, 80, 40))

        self.sendTask_TimeFor_Start_dan = QLineEdit(u"0", self.SendSetRight)
        if sendOption is not None:
            if sendOption[9] is not None:
                self.sendTask_TimeFor_Start_dan.setText('{}'.format(sendOption[9]))
        self.sendTask_TimeFor_Start_dan.setGeometry(QRect(140, 435, 40, 25))
        self.sendTask_TimeFor_Start_dan.setValidator(QIntValidator(0, 23))

        self.sendTask_TimeFor_dan_fuhao = QLabel()
        self.sendTask_TimeFor_dan_fuhao.setText(u'个')
        self.sendTask_TimeFor_dan_fuhao.setParent(self.SendSetRight)
        self.sendTask_TimeFor_dan_fuhao.setGeometry(QRect(185, 425, 20, 40))

        self.offLineBtn = QPushButton(QIcon(""), u"开始", self.SendSetRight)
        self.offLineBtn.setGeometry(QRect(100, 470, 80, 20))
        self.offLineBtn.clicked.connect(self.startOffLine)
        if sendOption is not None:
            if sendOption[5] is not None:
                if sendOption[5] == 1:
                    self.offLineBtn.setDisabled(True)
        self.offLineBtn.clicked.connect(self.startOffLine)

        self.offLineBtnEnd = QPushButton(QIcon(""), u"停止", self.SendSetRight)
        self.offLineBtnEnd.setGeometry(QRect(190, 470, 80, 20))
        self.offLineBtnEnd.setDisabled(True)
        if sendOption is not None:
            if sendOption[5] is not None:
                if sendOption[5] == 1:
                    self.offLineBtnEnd.setDisabled(False)


        self.sendButton = QWidget()
        conLayoutBodyButton = QGridLayout()
        self.sendButton.setLayout(conLayoutBodyButton)
        self.labelSendText = QLabel(self.sendButton)
        self.labelSendText.setText('待发列表0 成功列表0 失败列表0')
        conLayoutBodyButton.addWidget(self.labelSendText, 1, 1)

        self.sendStart = QPushButton(QIcon(""), u"开始", self.sendButton)
        self.sendStart.clicked.connect(self.start)
        conLayoutBodyButton.addWidget(self.sendStart, 1, 2)


        self.sendEnd = QPushButton(QIcon(""), u"停止", self.sendButton)
        self.sendEnd.clicked.connect(self.stop)
        self.sendEnd.setDisabled(True)

        conLayoutBodyButton.addWidget(self.sendEnd, 1, 3)

        conLayoutBody.addWidget(self.sendButton, 2, 1)



        self.loadingInfoLeft()
        self.loadingInfoLeftOk()
        self.loadingInfoLeftError()

    def getShop_id(self):
        getToken = taskModel.getToken(self.tparms['username'],self.tparms['task_id'])
        return getToken

    def startOffLine(self):
        try:
            shop_id = self.getShop_id()
            if shop_id is None:
                QMessageBox.information(self, u"提示", u"请重新登录")
                return
            sendInfo = {'minute': 0,'hour':0, 'send_hour': 0, 'send_min': 0, 'count_num': 0,'status':1}
            startHour = int(self.sendTask_Time_Start_num.text())
            startMin = int(self.sendTask_Time_Start_End.text())
            danNum = int(self.sendTask_TimeFor_Start_dan.text())
            interval_hour = int(self.sendTask_TimeFor_Start_num.text())
            interval_min = int(self.sendTask_TimeFor_Start_End.text())
            if interval_hour < 1 and interval_min < 1:
                msg_box = QMessageBox.information(self,
                                                  "警告",
                                                  "间隔时间不可为空",
                                                  QMessageBox.Yes)
                return
            if startHour > 23:
                msg_box = QMessageBox.information(self,
                                                  "警告",
                                                  "请输入正确的时间",
                                                  QMessageBox.Yes)
                return
            if startMin >= 60 and interval_hour >= 60:
                msg_box = QMessageBox.information(self,
                                                  "警告",
                                                  "请输入正确的时间",
                                                  QMessageBox.Yes)
                return
            if danNum < 1:
                msg_box = QMessageBox.information(self,
                                                  "警告",
                                                  "单次发送不可为0",
                                                  QMessageBox.Yes)
                return
        except Exception as e:
            msg_box = QMessageBox.information(self,
                                              "警告",
                                              "请填写正确的信息",
                                              QMessageBox.Yes)
        sendInfo['hour'] = startHour
        sendInfo['minute'] = startMin
        sendInfo['count_num'] = danNum
        sendInfo['send_hour'] = interval_hour
        sendInfo['send_min'] = interval_min

        self.sendTask_Time_Start_num.setDisabled(True)
        self.sendTask_Time_Start_End.setDisabled(True)
        self.sendTask_TimeFor_Start_num.setDisabled(True)
        self.sendTask_TimeFor_Start_End.setDisabled(True)
        self.sendTask_TimeFor_Start_dan.setDisabled(True)
        self.offLineBtn.setDisabled(True)
        self.offLineBtnEnd.setDisabled(False)
        sendOptionModel.setOption(self.tparms['admin_id'], self.tparms['task_id'],self.tparms['config_id'],sendInfo)

    def endOffLine(self):
        self.sendTask_Time_Start_num.setDisabled(False)
        self.sendTask_Time_Start_End.setDisabled(False)
        self.sendTask_TimeFor_Start_num.setDisabled(False)
        self.sendTask_TimeFor_Start_End.setDisabled(False)
        self.sendTask_TimeFor_Start_dan.setDisabled(False)
        self.offLineBtn.setDisabled(False)
        self.offLineBtnEnd.setDisabled(True)
        sendOptionModel.setOptionStatus(self.tparms['task_id'], self.tparms['config_id'], 0)

    def pageturnError(self):
        if len(self.pageInput_Error.text()) > 0:
            page = int(self.pageInput_Error.text())
            if page > 0:
                if page >= self.page_count_Error:
                    self.endPageSendError()
                    return
                else:
                    self.page_num_Error = (page - 1) * 10
                self.page_now_Error = page
                self.loadingInfoLeftError()

    def endPageSendError(self):
        try:
            if self.titledataCountError % 10 == 0:
                self.page_num_Error = self.titledataCountError - 10
            else:
                self.page_num_Error = self.titledataCountError - self.titledataCountError % 10
                if self.page_num_Error == 0:
                    return
            self.page_now_Error = self.page_count_Error
            if self.page_num_Error <= 0:
                self.page_num_Error = 0
            self.loadingInfoLeftError()
        except Exception as e:
            print(e)

    def homePageSendError(self):
        self.page_num_Error = 0
        self.page_now_Error = 1
        self.page_Error.setText('{}'.format(self.page_now_Error))
        self.loadingInfoLeftError()

    def lastPageSendError(self):
        if self.page_num_Error <= 0:
            self.page_num_Error = 0
            self.page_now_Error = 1
            self.page_Error.setText('{}'.format(self.page_now_Error))
            return
        self.page_num_Error = self.page_num_Error-10
        self.page_now_Error -= 1
        self.page_Error.setText('{}'.format(self.page_now_Error))
        self.loadingInfoLeftError()

    def nextPageSendError(self):
        if self.page_now_Error >= self.page_count_Error:
            QMessageBox.information(self, u"提示", u"这是最后一页了")
            return
        self.page_num_Error = self.page_num_Error+10
        self.page_now_Error += 1
        self.page_Error.setText('{}'.format(self.page_now_Error))
        self.loadingInfoLeftError()
    #发布失败
    def pageturnOk(self):
        if len(self.pageInput_ok.text()) > 0:
            page = int(self.pageInput_ok.text())
            if page > 0:
                if page >= self.page_count_ok:
                    self.endPageSendOk()
                    return
                else:
                    self.page_num_ok = (page - 1) * 10
                self.page_now_ok = page
                self.loadingInfoLeftOk()

    def endPageSendOk(self):
        try:
            if self.titledataCountOk % 10 == 0:
                self.page_num_ok = self.titledataCountOk - 10
            else:
                self.page_num_ok = self.titledataCountOk - self.titledataCountOk % 10
                if self.page_num_ok == 0:
                    return
            self.page_now_ok = self.page_count_ok
            if self.page_num_ok <= 0:
                self.page_num_ok = 0
            self.loadingInfoLeftOk()
        except Exception as e:
            print(e)

    def homePageSendOk(self):
        self.page_num_ok = 0
        self.page_now_ok = 1
        self.page_ok.setText('{}'.format(self.page_now_ok))
        self.loadingInfoLeftOk()

    def lastPageSendOk(self):
        if self.page_num_ok <= 0:
            self.page_num_ok = 0
            self.page_now_ok = 1
            self.page_ok.setText('{}'.format(self.page_now_ok))
            return
        self.page_num_ok = self.page_num_ok-10
        self.page_now_ok -= 1
        self.page_ok.setText('{}'.format(self.page_now_ok))
        self.loadingInfoLeftOk()

    def nextPageSendOk(self):
        if self.page_now_ok >= self.page_count_ok:
            QMessageBox.information(self, u"提示", u"这是最后一页了")
            return
        self.page_num_ok = self.page_num_ok+10
        self.page_now_ok += 1
        self.page_ok.setText('{}'.format(self.page_now_ok))
        self.loadingInfoLeftOk()
    #已发布列表
    def pageturn(self):
        if len(self.pageInput.text()) > 0:
            page = int(self.pageInput.text())
            if page > 0:
                if page >= self.page_count:
                    self.endPageSend()
                    return
                else:
                    self.page_num = (page - 1) * 10
                self.page_now = page
                self.loadingInfoLeft()

    def endPageSend(self):
        try:
            if self.titledataCountWei % 10 == 0:
                self.page_num = self.titledataCountWei - 10
            else:
                self.page_num = self.titledataCountWei - self.titledataCountWei % 10
                if self.page_num == 0:
                    return
            self.page_now = self.page_count
            if self.page_num <= 0:
                self.page_num = 0
            self.loadingInfoLeft()
        except Exception as e:
            print(e)

    def homePageSend(self):
        self.page_num = 0
        self.page_now = 1
        self.page.setText('{}'.format(self.page_now))
        self.loadingInfoLeft()

    def lastPageSend(self):
        if self.page_num <= 0:
            self.page_num = 0
            self.page_now = 1
            self.page.setText('{}'.format(self.page_now))
            return
        self.page_num = self.page_num-10
        self.page_now -= 1
        self.page.setText('{}'.format(self.page_now))
        self.loadingInfoLeft()

    def nextPageSend(self):
        if self.page_now >= self.page_count:
            QMessageBox.information(self, u"提示", u"这是最后一页了")
            return
        self.page_num = self.page_num+10
        self.page_now += 1
        self.page.setText('{}'.format(self.page_now))
        self.loadingInfoLeft()

    def stop(self):
        time.sleep(2)
        self.sendStart.setDisabled(False)
        self.sendEnd.setDisabled(True)
        self.tparms['is_open'] = 0
        self.sendStart.setText(u"发送")
        configureModel.updateSend(self.tparms['config_id'],0)

    def start(self):
        try:

            self.is_All_status = 0

            sendInfo = {'filter': 0, 'zdy_filter': 0, 'start_rate': 0, 'end_rate': 0, 'is_sendNumber': 0,
                        'max_send': 0, 'select_last': 0, 'deposit': 0, 'start_hour': 0, 'start_min': 0}
            if self.filterRealTime.isChecked():
                sendInfo['filter'] = 1
            if self.filterZdy.isChecked():
                sendInfo['zdy_filter'] = 1
            startRate = self.sendSet_Frequency_Start_num.text()
            sendInfo['start_rate'] = startRate
            endRate = self.sendSet_Frequency_End.text()
            sendInfo['end_rate'] = endRate
            if self.sendSet_Frequency_number_zdy.isChecked():
                sendInfo['is_sendNumber'] = 1
                sendInfo['max_send'] = self.sendSet_Frequency_number_zdy_label.text()

            self.sendStart.setDisabled(True)
            self.sendStart.setText(u"发送中")

            self.tparms['is_open'] = 1
            self.sendEnd.setDisabled(False)
            self.send_parms = SendStartNow(self.tparms, sendInfo)
            self.send_parms.finishSignal_pc_up.connect(self.is_ok)
            self.send_parms.start()

        except Exception as e:
            print(e)

    def is_ok(self,reres):
        if reres[1] == 'login':
            self.tparms['is_open'] = 0
            configureModel.updateSend(self.tparms['config_id'], 0)
            QMessageBox.information(self, u'注意', u'请重新登录')
            self.sendStart.setDisabled(False)
            self.sendStart.setText(u"开始")

        if reres[0] == 'continue':
            taskModel.updateStart(self.tparms['admin_id'], self.tparms['username'], 1)
            self.loadingInfoLeft()
            self.loadingInfoLeftOk()
            self.loadingInfoLeftError()
        elif reres[0] == 'success':
            self.tparms['is_open'] = 0
            configureModel.updateSend(self.tparms['config_id'], 0)
            QMessageBox.information(self, u'完成', u'发送完成')
            self.sendStart.setDisabled(False)
            self.sendStart.setText(u"开始")
        elif reres[0] == 'stop':
            configureModel.updateSend(self.tparms['config_id'], 0)
            QMessageBox.information(self, u'完成', u'发送完成')
            self.sendStart.setDisabled(False)
            self.sendStart.setText(u"开始")

    def addMinGan(self):
        self.ui2 = zdyMinKeyword(self.tparms)
        self.ui2.show()

    def goText(self, msg):
        self.view.page().runJavaScript("window.say_hello('%s')" % msg)

    def WrittingNotOfOther(self, msg):
        self.view.page().runJavaScript("window.say_hello('%s')" % msg)

    def down_title(self):
        try:
            result = titleModel.titleDataAll(self.tparms['admin_id'], self.tparms['task_id'],0,self.tparms['config_id'])
            if len(result) > 0:
                global save_path
                _translate = QCoreApplication.translate
                fileName2, ok2 = QFileDialog.getSaveFileName(None, "文件保存", "H:/")
                if fileName2:
                    DownTitle(self.tparms, fileName2,result)
            else:
                reply = QMessageBox.information(self,
                                                "提示",
                                                "还没有标题可以导出",
                                                QMessageBox.Yes)
        except Exception as e:
            print(e)
    def selectSend(self):
        for line in self.line_dai:
            line[1].setChecked(True)

    def selectDel(self):
        self.delSelectedAll.setDisabled(True)
        removeline = []
        for line in self.line_dai:
            if line[1].isChecked():
                titleModel.deleteOne(self.tparms['admin_id'],self.tparms['task_id'],line[2],self.tparms['config_id'])
                row = self.sendList_table.rowCount()
                for x in range(row, 0, -1):
                    if line[0] == self.sendList_table.item(x - 1, 0).text():
                        self.sendList_table.removeRow(x - 1)
                        removeline.append(line)
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
            self.line_dai.remove(line)
        self.loadingInfoLeft()
        self.delSelectedAll.setDisabled(False)

    def selectDelError(self):
        self.delSelectedAllError.setDisabled(True)
        removeline = []
        for line in self.line_error:
            if line[1].isChecked():
                titleModel.deleteOne(self.tparms['admin_id'],self.tparms['task_id'],line[2],self.tparms['config_id'])
                row = self.sendList_tableError.rowCount()
                for x in range(row, 0, -1):
                    if line[0] == self.sendList_tableError.item(x - 1, 0).text():
                        self.sendList_tableError.removeRow(x - 1)
                        removeline.append(line)
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
            self.line_error.remove(line)
        self.loadingInfoLeftError()
        self.delSelectedAllError.setDisabled(False)

    def selectDelOk(self):
        self.delSelectedAllOk.setDisabled(True)
        removeline = []
        for line in self.line_ok:
            if line[1].isChecked():
                titleModel.deleteOne(self.tparms['admin_id'],self.tparms['task_id'],line[2],self.tparms['config_id'])
                row = self.sendList_tableOk.rowCount()
                for x in range(row, 0, -1):
                    if line[0] == self.sendList_tableOk.item(x - 1, 0).text():
                        self.sendList_tableOk.removeRow(x - 1)
                        removeline.append(line)
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
            self.line_ok.remove(line)
        self.loadingInfoLeftOk()
        self.delSelectedAllOk.setDisabled(False)

    def selectSendFan(self):
        for line in self.line_dai:
            if line[1].isChecked():
                line[1].setChecked(False)
            else:
                line[1].setChecked(True)

    def loadingInfoLeft(self):
        self.indexBtn.setDisabled(True)
        self.lastPageBtn.setDisabled(True)
        self.nextPageBtn.setDisabled(True)
        self.endPageBtn.setDisabled(True)
        self.pageAlright.setDisabled(True)

        row = self.sendList_table.rowCount()
        for x in range(row, 0, -1):
            self.sendList_table.removeRow(x - 1)
        self.daiId = 1
        self.line_dai = []
        try:
            if self.page_now == 0:
                self.page.setText('1')
            else:
                self.page.setText('{}'.format(self.page_now))
            result = titleModel.titleData(self.tparms['admin_id'], self.tparms['task_id'],0,self.tparms['config_id'],self.page_num,10)
            self.ready = titleModel.titleDataCount(self.tparms['admin_id'], self.tparms['task_id'],0,self.tparms['config_id'])
            self.page_count = ceil(self.ready / 10)
            self.formto.setText('共{}页 到'.format(self.page_count))
            self.titledataCountWei = self.ready
            for info in result:
                ck = QCheckBox()
                h = QHBoxLayout()
                h.setAlignment(Qt.AlignCenter)
                h.addWidget(ck)
                w = QWidget()
                w.setLayout(h)
                row = self.sendList_table.rowCount()
                self.sendList_table.insertRow(row)
                self.sendList_table.setItem(row, 0, QTableWidgetItem(str(self.daiId)))
                self.sendList_table.setCellWidget(row, 1, w)
                self.sendList_table.setRowHeight(row, 32)

                self.sendList_table.setItem(row, 2, QTableWidgetItem(info['title']))
                self.sendList_table.setItem(row, 3, QTableWidgetItem('未发布'))
                self.line_dai.append([str(self.daiId), ck, info['id'], info['title']])
                self.daiId += 1

            self.labelSendText.setText('待发列表{},成功列表{},失败{}'.format(self.ready, self.is_run, self.is_false))
        except Exception as e:
            print(e)
        self.indexBtn.setDisabled(False)
        self.lastPageBtn.setDisabled(False)
        self.nextPageBtn.setDisabled(False)
        self.endPageBtn.setDisabled(False)
        self.pageAlright.setDisabled(False)

    def loadingInfoLeftOk(self):
        self.indexBtn.setDisabled(True)
        self.lastPageBtn.setDisabled(True)
        self.nextPageBtn.setDisabled(True)
        self.endPageBtn.setDisabled(True)
        self.pageAlright.setDisabled(True)
        row2 = self.sendList_tableOk.rowCount()
        for x in range(row2, 0, -1):
            self.sendList_tableOk.removeRow(x - 1)
        self.startId = 1
        self.line_ok = []
        try:
            if self.page_now_ok == 0:
                self.page_ok.setText('1')
            else:
                self.page_ok.setText('{}'.format(self.page_now_ok))
            result = titleModel.titleData(self.tparms['admin_id'], self.tparms['task_id'], 1,self.tparms['config_id'], self.page_num_ok,10)
            self.is_run = titleModel.titleDataCount(self.tparms['admin_id'], self.tparms['task_id'], 1,self.tparms['config_id'])
            self.titledataCountOk = self.is_run
            self.page_count_ok = ceil(self.is_run / 10)
            self.formto_ok.setText('共{}页 到'.format(self.page_count_ok))
            for info in result:
                ck = QCheckBox()
                h = QHBoxLayout()
                h.setAlignment(Qt.AlignCenter)
                h.addWidget(ck)
                w = QWidget()
                w.setLayout(h)
                row = self.sendList_tableOk.rowCount()
                self.sendList_tableOk.insertRow(row)
                self.sendList_tableOk.setItem(row, 0, QTableWidgetItem(str(self.startId)))
                self.sendList_tableOk.setCellWidget(row, 1, w)
                self.sendList_tableOk.setRowHeight(row, 32)
                self.sendList_tableOk.setItem(row, 2, QTableWidgetItem(info['title']))
                if info['send_time'] is None:
                    self.sendList_tableOk.setItem(row, 3, QTableWidgetItem(''))
                else:
                    self.sendList_tableOk.setItem(row, 3, QTableWidgetItem(
                        time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(int(info['send_time'])))))

                self.line_ok.append([str(self.startId), ck, info['id']])
                self.startId += 1
            self.labelSendText.setText('待发列表{},成功列表{},失败{}'.format(self.ready, self.is_run, self.is_false))
        except Exception as e:
            print(e)
        self.indexBtn.setDisabled(False)
        self.lastPageBtn.setDisabled(False)
        self.nextPageBtn.setDisabled(False)
        self.endPageBtn.setDisabled(False)
        self.pageAlright.setDisabled(False)

    def loadingInfoLeftError(self):
        self.indexBtn.setDisabled(True)
        self.lastPageBtn.setDisabled(True)
        self.nextPageBtn.setDisabled(True)
        self.endPageBtn.setDisabled(True)
        self.pageAlright.setDisabled(True)
        row3 = self.sendList_tableError.rowCount()
        for x in range(row3, 0, -1):
            self.sendList_tableError.removeRow(x - 1)
        self.endId = 1
        self.line_error = []
        try:
            if self.page_now_Error == 0:
                self.page_Error.setText('1')
            else:
                self.page_Error.setText('{}'.format(self.page_now_Error))
            result = titleModel.titleData(self.tparms['admin_id'], self.tparms['task_id'], 2,self.tparms['config_id'], self.page_num_Error,10)

            self.is_false = titleModel.titleDataCount(self.tparms['admin_id'], self.tparms['task_id'], 2,self.tparms['config_id'])
            self.titledataCountError = self.is_false
            self.page_count_Error = ceil(self.is_false / 10)
            self.formto_Error.setText('共{}页 到'.format(self.page_count_Error))
            for info in result:
                ck = QCheckBox()
                h = QHBoxLayout()
                h.setAlignment(Qt.AlignCenter)
                h.addWidget(ck)
                w = QWidget()
                w.setLayout(h)
                row = self.sendList_tableError.rowCount()
                self.sendList_tableError.insertRow(row)
                self.sendList_tableError.setItem(row, 0, QTableWidgetItem(str(self.endId)))
                self.sendList_tableError.setCellWidget(row, 1, w)
                self.sendList_tableError.setRowHeight(row, 32)

                self.sendList_tableError.setItem(row, 2, QTableWidgetItem(info['title']))
                if len(info['desc']) > 0:
                    self.sendList_tableError.setItem(row, 3, QTableWidgetItem(info['desc']))
                else:
                    self.sendList_tableError.setItem(row, 3, QTableWidgetItem('发布失败'))
                if info['send_time'] is None:
                    self.sendList_tableError.setItem(row, 4, QTableWidgetItem(''))
                else:
                    self.sendList_tableError.setItem(row, 4, QTableWidgetItem(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(int(info['send_time'])))))
                self.line_error.append([str(self.endId), ck, info['id']])
                self.endId += 1
                self.is_false+=1
            self.labelSendText.setText('待发列表{},成功列表{},失败{}'.format(self.ready, self.is_run, self.is_false))
        except Exception as e:
            print(e)
        self.indexBtn.setDisabled(False)
        self.lastPageBtn.setDisabled(False)
        self.nextPageBtn.setDisabled(False)
        self.endPageBtn.setDisabled(False)
        self.pageAlright.setDisabled(False)

    def clearTitleDelete(self,status):
        try:
            if status == 0:
                self.page_num = 0
                self.limit = 10
                self.page_now = 1
                self.page_count = 0
                row = self.sendList_table.rowCount()
                for x in range(row, 0, -1):
                    self.sendList_table.removeRow(x - 1)
                self.daiId = 1
                self.line_dai = []

            if status == 1:
                self.page_num_ok = 0
                self.limit_ok = 10
                self.page_now_ok = 1
                self.page_count_ok = 0
                row2 = self.sendList_tableOk.rowCount()
                for x in range(row2, 0, -1):
                    self.sendList_tableOk.removeRow(x - 1)
                self.startId = 1
                self.line_ok = []

            if status == 2:
                self.page_num_Error = 0
                self.limit_Error = 10
                self.page_now_Error = 1
                self.page_count_Error = 0
                row3 = self.sendList_tableError.rowCount()
                for x in range(row3, 0, -1):
                    self.sendList_tableError.removeRow(x - 1)
                self.endId = 1
                self.line_error = []
            titleModel.deleteList(self.tparms['admin_id'],self.tparms['task_id'],status,self.tparms['config_id'])
            reply = QMessageBox.information(self,
                                            "提示",
                                            "清空成功",
                                            QMessageBox.Yes)
        except Exception as e:
            print(e)


class zdyMinKeyword(QMainWindow):

    def __init__(self,tparms, parent=None):
        super(zdyMinKeyword,self).__init__()
        self.setWindowTitle('敏感词管理')
        self.tparms = tparms
        self.resize(350,430)
        self.leftQWidget = QWidget(self)
        self.leftQWidget.setGeometry(0, 0, 175, 430)

        self.leftQWidgetText = QLabel(self.leftQWidget)
        self.leftQWidgetText.setText(u'需要过滤的敏感词')
        self.leftQWidgetText.setGeometry(10, 10, 170, 20)

        self.leftQWidgetTextNeed = QTextEdit(self.leftQWidget)
        self.leftQWidgetTextNeed.setGeometry(QRect(7, 40, 350,165))
        self.leftQWidgetTextNeed.setStyleSheet('min-width:165;min-height:350')

        self.leftQWidgetTextTips = QLabel(self.leftQWidget)
        self.leftQWidgetTextTips.setGeometry(QRect(7, 400, 170, 20))
        self.leftQWidgetTextTips.setText(u'填写敏感词，一行一个')

        self.rightQWidget = QWidget(self)
        self.rightQWidget.setGeometry(185, 0, 175, 430)

        self.rightQWidgetText = QLabel(self.rightQWidget)
        self.rightQWidgetText.setText(u'不需要过滤的敏感词')
        self.rightQWidgetText.setGeometry(10, 10, 170, 20)

        self.rightQWidgetTextNeed = QTextEdit(self.rightQWidget)
        self.rightQWidgetTextNeed.setGeometry(QRect(7, 40, 350,165))
        self.rightQWidgetTextNeed.setStyleSheet('min-width:165;min-height:350')

        self.saveAll = QPushButton(QIcon(""), u"保存", self)
        self.saveAll.setGeometry(QRect(150, 400, 40,20))
        self.saveAll.clicked.connect(self.saveAllClick)

        self.loadWord()

    def loadWord(self):
        data = SendWordModel.getDataList(self.tparms['admin_id'],self.tparms['task_id'],self.tparms['config_id'])
        for info in data:
            if info['type'] == 1:
                self.leftQWidgetTextNeed.insertPlainText(info['word']+'\n')
            elif info['type'] == 2:
                self.rightQWidgetTextNeed.insertPlainText(info['word'] + '\n')

    def saveAllClick(self):
        try:
            needText = self.leftQWidgetTextNeed.toPlainText()
            need_list = re.split('\n', needText)
            noNeedText = self.rightQWidgetTextNeed.toPlainText()
            noNeed_list = re.split('\n', noNeedText)

            SendWordModel.deleteAll(self.tparms['admin_id'],self.tparms['task_id'],self.tparms['config_id'])
            SendWordModel.add_Data(need_list,self.tparms['admin_id'],self.tparms['task_id'],1,self.tparms['config_id'])
            SendWordModel.add_Data(noNeed_list,self.tparms['admin_id'],self.tparms['task_id'],2,self.tparms['config_id'])
            QMessageBox.information(self, u'提示', u'保存成功')
        except Exception as e:
            print(e)
class DownTitle(QThread):
    finishSignal_keyword = pyqtSignal(list)

    def __init__(self, tparms, filedir,result, parent=None):
        super(DownTitle, self).__init__(parent)
        self.filename = '标题'
        self.file_dir = tparms['username']
        self.filedir = filedir
        self.download(result)
    def download(self,result):
        wbk = xlwt.Workbook()
        try:
            count = 0
            sheet = wbk.add_sheet('Sheet1', cell_overwrite_ok=True)
            for info in result:
                sheet.write(count, 0, info['title'])
                count += 1
            wbk.save(self.filedir + self.filename + '.xls')
        except Exception as e:
            print(e)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = zdyMinKeyword()
    w.resize(350,430)
    w.show()
    sys.exit(app.exec_())

