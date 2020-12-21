from PyQt5.QtCore import QRect,Qt,QCoreApplication,QThread,pyqtSignal
from PyQt5.QtGui import QIcon,QDoubleValidator,QIntValidator
from PyQt5.QtWidgets import *
import sys
import titleModel
import xlwt
import SendWordModel
import re

# tparms = {'admin_id': '', 'name': '', 'task_id': '', 'username': '', 'password': ''}
class Send(QTabWidget):

    def __init__(self,info, *args, **kwargs):
        super(Send, self).__init__(*args, **kwargs)
        self.tparms = info
        self.SendSetLeft = QWidget(self)
        self.SendSetLeft.setGeometry(QRect(0, 0, 604, 572))
        layout = QGridLayout(self)
        layout.addWidget(SendLeft(info,tabPosition=SendLeft.North))
        layout.setGeometry(QRect(0, 0,841,500))

        self.labelSendText = QLabel(self)
        self.labelSendText.setText('待发列表66 成功列表0 失败列表0')
        self.labelSendText.setGeometry(30, 520, 200, 30)

        self.sendStart = QPushButton(QIcon(""), u"开始", self)
        self.sendStart.setGeometry(380, 530, 55, 25)
        self.sendStart.clicked.connect()

        self.sendEnd = QPushButton(QIcon(""), u"停止", self)
        self.sendEnd.setGeometry(450, 530, 55, 25)

        self.SendSetRight = QWidget(self)
        self.SendSetRight.setGeometry(QRect(542, 0, 350, 687))
        # self.SendSetRight.setStyleSheet('background-color:palevioletred')
        self.textMin = QLabel()
        self.textMin.setText(u'敏感词')
        self.textMin.setParent(self.SendSetRight)
        self.textMin.setGeometry(QRect(20, 10, 200, 50))

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

        sendSet_Frequency_Start = QDoubleValidator(0,100000,0,self.SendSetRight)
        self.sendSet_Frequency_Start_num = QLineEdit(u"60", self.SendSetRight)
        self.sendSet_Frequency_Start_num.setValidator(sendSet_Frequency_Start)
        self.sendSet_Frequency_Start_num.setGeometry(QRect(100, 210, 60, 25))

        self.sendSet_Frequency_fuhao = QLabel()
        self.sendSet_Frequency_fuhao.setText(u'~')
        self.sendSet_Frequency_fuhao.setParent(self.SendSetRight)
        self.sendSet_Frequency_fuhao.setGeometry(QRect(170, 210, 20, 40))

        sendSet_Frequency_End = QDoubleValidator(0,100000,0,self.SendSetRight)
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
        self.sendSet_Frequency_number_one.setText(u'当天最大限额当天最大限额')


        self.sendSet_Frequency_number_zdy = QRadioButton("Button1")  # 实例化一个选择的按钮
        self.sendSet_Frequency_number_zdy.setChecked(True)  # 设置按钮点点击状态
        self.sendSet_Frequency_number_zdy.setGeometry(QRect(100, 300, 100, 20))
        self.sendSet_Frequency_number_zdy.setParent(self.SendSetRight)
        self.sendSet_Frequency_number_zdy.setText(u'自定义数量')

        sendSet_Frequency_zdy = QDoubleValidator(0, 100000, 0, self.SendSetRight)
        self.sendSet_Frequency_number_zdy_label = QLineEdit(u"100", self.SendSetRight)
        self.sendSet_Frequency_number_zdy_label.setValidator(sendSet_Frequency_End)
        self.sendSet_Frequency_number_zdy_label.setGeometry(QRect(220, 300, 60, 25))

        self.sendSet_link = QCheckBox(self.SendSetRight)
        self.sendSet_link.setChecked(True)  # 设置按钮点点击状态
        self.sendSet_link.setGeometry(QRect(100, 330, 120, 25))
        self.sendSet_link.setParent(self.SendSetRight)
        self.sendSet_link.setText(u'链接上一篇信息')

        self.sendTask = QLabel()
        self.sendTask.setText(u'发布任务：')
        self.sendTask.setParent(self.SendSetRight)
        self.sendTask.setGeometry(QRect(20, 360, 200, 50))


        self.sendTask_Gua = QCheckBox(self.SendSetRight)
        self.sendTask_Gua.setChecked(True)  # 设置按钮点点击状态
        self.sendTask_Gua.setGeometry(QRect(100, 390, 120, 25))
        self.sendTask_Gua.setParent(self.SendSetRight)
        self.sendTask_Gua.setText(u'启用挂机模式')

        self.sendTask_time = QLabel()
        self.sendTask_time.setText(u'每日')
        self.sendTask_time.setParent(self.SendSetRight)
        self.sendTask_time.setGeometry(QRect(100, 430, 80, 40))

        # sendTask_Time_Start = QDoubleValidator(0, 23, 0, self.SendSetRight)
        self.sendTask_Time_Start_num = QLineEdit(u"10", self.SendSetRight)
        # self.sendTask_Time_Start_num.setValidator(sendTask_Time_Start)
        self.sendTask_Time_Start_num.setGeometry(QRect(140, 440, 40, 25))
        self.sendTask_Time_Start_num.setValidator(QIntValidator(0, 23))

        self.sendTask_Time_Start_fuhao = QLabel()
        self.sendTask_Time_Start_fuhao.setText(u':')
        self.sendTask_Time_Start_fuhao.setParent(self.SendSetRight)
        self.sendTask_Time_Start_fuhao.setGeometry(QRect(180, 430, 20, 40))

        # sendTask_Time_Start_End = QDoubleValidator(0, 59, 0, self.SendSetRight)
        self.sendTask_Time_Start_End = QLineEdit(u"0", self.SendSetRight)
        # self.sendTask_Time_Start_End.setValidator(sendTask_Time_Start_End)
        self.sendTask_Time_Start_End.setGeometry(QRect(190, 440, 40, 25))
        self.sendTask_Time_Start_End.setValidator(QIntValidator(0, 59))


        self.sendTask_Start = QLabel()
        self.sendTask_Start.setText(u'开始')
        self.sendTask_Start.setParent(self.SendSetRight)
        self.sendTask_Start.setGeometry(QRect(240, 440, 40, 25))

    def start(self):
        sendInfo = {'filter':0,'zdy_filter':0,'start_rate':0,'end_rate':0,'is_sendNumber':0,'max_send':0,'select_last':0,'deposit':0,'start_hour':0,'start_min':0}
        if self.filterRealTime.isChecked():
            sendInfo['filter'] = 1
        if self.filterZdy.isChecked():
            sendInfo['zdy_filter'] = 1
        startRate = self.sendSet_Frequency_Start_num.text()
        sendInfo['start_rate'] = startRate
        endRate = self.sendSet_Frequency_End.text()
        sendInfo['end_rate'] = endRate
        if self.sendSet_Frequency_number_one.isChecked():
            sendInfo['is_sendNumber'] = 1
            sendInfo['max_send'] = self.sendSet_Frequency_number_one.text()
        if self.sendTask_Gua.isChecked():
            sendInfo['deposit'] = 1
            startHour = self.sendTask_Time_Start_num.text()
            startMin = self.sendTask_Time_Start_End.text()

            if startHour > 23:
                msg_box = QMessageBox.information(self,
                                                  "警告",
                                                  "请输入正确的时间，",
                                                  QMessageBox.Yes)
                return
            if startMin > 60:
                msg_box = QMessageBox.information(self,
                                                  "警告",
                                                  "请输入正确的时间，",
                                                  QMessageBox.Yes)
                return
            sendInfo['start_hour'] = startHour
            sendInfo['start_min'] = startMin

        # SendStartNow(self.tparms,sendInfo)

        # self.sendSet_Frequency_number_one.toggled.connect(lambda: self.btnstate(self.btn1))  # 绑定点击事件
    def addMinGan(self):
        self.ui2 = zdyMinKeyword(self.tparms)
        # self.ui2.setupUi(self.form2)
        self.ui2.show()

    def goText(self,msg):
        print(123)
        # view.page().runJavaScript("alert('%s')" % msg)
        self.view.page().runJavaScript("window.say_hello('%s')" % msg)
    def itemActivated_event(self,item):
        print(item.text())

    def WrittingNotOfOther(self, msg):
        print(msg)
        self.view.page().runJavaScript("window.say_hello('%s')" % msg)

class SendStartNow(QTabWidget):
    finishSignal_pc_up = pyqtSignal(list)

    def __init__(self,tparms,info, *args, **kwargs):
        super(SendStartNow, self).__init__(*args, **kwargs)
        self.tparms = tparms
        self.info = info

    def run(self):
        print(self.info)

class SendLeft(QTabWidget):
    def __init__(self,tparms, *args, **kwargs):
        super(SendLeft, self).__init__(*args, **kwargs)
        self.tparms = tparms
        for i in range(3):
            if i == 0:
                self.daiId = 1
                self.line_dai = []

                self.sendList = QWidget()

                self.sendList_table = QTableWidget(self)
                self.sendList_table.setRowCount(0)
                self.sendList_table.setColumnCount(4)
                self.sendList_table.setParent(self.sendList)
                self.sendList_table.setGeometry(0, 0, 530, 350)
                self.sendList_table.setEditTriggers(QAbstractItemView.DoubleClicked)
                self.sendList_table.setHorizontalHeaderLabels([u"ID",u"选择","待发列表", u"状态"])
                self.sendList_table.setColumnWidth(0, 30)
                self.sendList_table.setColumnWidth(1, 50)
                self.sendList_table.setColumnWidth(2, 310)
                self.sendList_table.setColumnWidth(3, 64)
                self.sendList_table.setEditTriggers(QTableWidget.AnyKeyPressed)
                self.sendList_table.verticalHeader().setVisible(False)

                self.selectAll = QPushButton(QIcon(""), u"全选", self.sendList)
                self.selectAll.setGeometry(30, 400, 55, 25)
                self.selectAll.clicked.connect(self.selectSend)

                self.fanSelectAll = QPushButton(QIcon(""), u"反选", self.sendList)
                self.fanSelectAll.setGeometry(95, 400, 55, 25)
                self.fanSelectAll.clicked.connect(self.selectSendFan)

                self.delSelectedAll = QPushButton(QIcon(""), u"删除勾选", self.sendList)
                self.delSelectedAll.setGeometry(165, 400, 55, 25)
                self.delSelectedAll.clicked.connect(self.selectDel)

                self.delAll = QPushButton(QIcon(""), u"清空列表", self.sendList)
                self.delAll.setGeometry(230, 400, 55, 25)
                self.delAll.clicked.connect(self.clearTitle)

                self.daoTitle = QPushButton(QIcon(""), u"导出标题", self.sendList)
                self.daoTitle.setGeometry(295, 400, 55, 25)
                self.daoTitle.clicked.connect(self.down_title)

                self.daoRuTitle = QPushButton(QIcon(""), u"导入标题", self.sendList)
                self.daoRuTitle.setGeometry(360, 400, 55, 25)
                #
                # self.randTitle = QPushButton(QIcon(""), u"打乱标题", self.sendList)
                # self.randTitle.setGeometry(430, 400, 55, 25)

                self.addTab(self.sendList, str('待发列表'))
            elif i == 1:
                self.startId = 1
                self.line_ok = []

                self.sendListOk = QWidget()

                self.sendList_tableOk = QTableWidget(self)
                self.sendList_tableOk.setRowCount(0)
                self.sendList_tableOk.setColumnCount(4)
                self.sendList_tableOk.setParent(self.sendListOk)
                self.sendList_tableOk.setGeometry(0, 0, 530, 350)
                self.sendList_tableOk.setEditTriggers(QAbstractItemView.DoubleClicked)
                self.sendList_tableOk.setHorizontalHeaderLabels([u"ID",u"选择","待发列表", u"状态"])
                self.sendList_tableOk.setColumnWidth(0, 30)
                self.sendList_tableOk.setColumnWidth(1, 50)
                self.sendList_tableOk.setColumnWidth(2, 310)
                self.sendList_tableOk.setColumnWidth(3, 64)
                self.sendList_tableOk.setEditTriggers(QTableWidget.AnyKeyPressed)
                self.sendList_tableOk.verticalHeader().setVisible(False)

                self.addTab(self.sendListOk, str('发布成功'))
            elif i == 2:
                self.endId = 1
                self.line_error = []

                self.sendListError = QWidget()
                self.sendList_tableError = QTableWidget(self)
                self.sendList_tableError.setRowCount(0)
                self.sendList_tableError.setColumnCount(4)
                self.sendList_tableError.setParent(self.sendListError)
                self.sendList_tableError.setGeometry(0, 0, 530, 350)
                self.sendList_tableError.setEditTriggers(QAbstractItemView.DoubleClicked)
                self.sendList_tableError.setHorizontalHeaderLabels([u"ID",u"选择","待发列表", u"状态"])
                self.sendList_tableError.setColumnWidth(0, 30)
                self.sendList_tableError.setColumnWidth(1, 50)
                self.sendList_tableError.setColumnWidth(2, 310)
                self.sendList_tableError.setColumnWidth(3, 64)
                self.sendList_tableError.setEditTriggers(QTableWidget.AnyKeyPressed)
                self.sendList_tableError.verticalHeader().setVisible(False)

                self.addTab(self.sendListError, str('发布失败'))
        self.loadingInfo()

    def down_title(self):
        result = titleModel.titleData(self.tparms['admin_id'], self.tparms['task_id'],self.tparms['config_id'])
        if len(result) > 0:
            global save_path
            _translate = QCoreApplication.translate
            fileName2, ok2 = QFileDialog.getSaveFileName(None, "文件保存", "H:/")
            if fileName2:
                DownTitle(self.tparms, fileName2,result)
            # DownKeywords(tparms, fileName2)
        else:
            reply = QMessageBox.information(self,
                                            "提示",
                                            "还没有标题可以导出",
                                            QMessageBox.Yes)

    def selectSend(self):
        for line in self.line_dai:
            line[1].setChecked(True)

    def selectDel(self):
        for line in self.line_dai:
            line[1].setChecked(False)

    def selectSendFan(self):
        for line in self.line_dai:
            if line[1].isChecked():
                line[1].setChecked(False)
            else:
                line[1].setChecked(True)

    def loadingInfo(self):
        self.clearTitle()
        try:
            result = titleModel.titleData(self.tparms['admin_id'], self.tparms['task_id'],self.tparms['config_id'])
            for info in result:
                ck = QCheckBox()
                h = QHBoxLayout()
                h.setAlignment(Qt.AlignCenter)
                h.addWidget(ck)
                w = QWidget()
                w.setLayout(h)
                if info['status'] == 0:
                    row = self.sendList_table.rowCount()
                    self.sendList_table.insertRow(row)
                    self.sendList_table.setItem(row, 0, QTableWidgetItem(str(self.daiId)))
                    self.sendList_table.setCellWidget(row, 1, w)
                    self.sendList_table.setItem(row, 2, QTableWidgetItem(info['title']))
                    self.sendList_table.setItem(row, 3, QTableWidgetItem('未发布'))
                    self.line_dai.append([str(self.daiId), ck, info['id']])
                    self.daiId += 1
                elif info['status'] == 1:
                    row = self.sendList_tableOk.rowCount()
                    self.sendList_tableOk.insertRow(row)
                    self.sendList_tableOk.setItem(row, 0, QTableWidgetItem(str(self.startId)))
                    self.sendList_tableOk.setCellWidget(row, 1, w)
                    self.sendList_tableOk.setItem(row, 2, QTableWidgetItem(info['title']))
                    self.sendList_tableOk.setItem(row, 3, QTableWidgetItem('已发布'))
                    self.line_ok.append([str(self.startId), ck, info['id']])
                    self.startId += 1
                elif info['status'] == 2:
                    row = self.sendList_tableError.rowCount()
                    self.sendList_tableError.insertRow(row)
                    self.sendList_tableError.setItem(row, 0, QTableWidgetItem(str(self.endId)))
                    self.sendList_tableError.setCellWidget(row, 1, w)
                    self.sendList_tableError.setItem(row, 2, QTableWidgetItem(info['title']))
                    self.sendList_tableError.setItem(row, 3, QTableWidgetItem('发布失败'))
                    self.line_error.append([str(self.endId), ck, info['id']])
                    self.endId += 1


        except Exception as e:
            print(e)

    def clearTitle(self):
        try:
            row = self.sendList_table.rowCount()
            for x in range(row, 0, -1):
                self.sendList_table.removeRow(x - 1)
            self.daiId = 1
            self.line_dai = []
                # new_list.append(self.title_list_table.item(x - 1, 2).text())
        except Exception as e:
            print(e)

class zdyMinKeyword(QMainWindow):

    def __init__(self,tparms, parent=None):
        super(zdyMinKeyword,self).__init__()
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
        needText = self.leftQWidgetTextNeed.toPlainText()
        need_list = re.split('\n', needText)
        noNeedText = self.rightQWidgetTextNeed.toPlainText()
        noNeed_list = re.split('\n', noNeedText)

        SendWordModel.deleteAll(self.tparms['admin_id'],self.tparms['task_id'],self.tparms['config_id'])
        SendWordModel.add_Data(need_list,self.tparms['admin_id'],self.tparms['task_id'],1,self.tparms['config_id'])
        SendWordModel.add_Data(noNeed_list,self.tparms['admin_id'],self.tparms['task_id'],2,self.tparms['config_id'])

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
            print(result)
            count = 0
            sheet = wbk.add_sheet('Sheet1', cell_overwrite_ok=True)
            for info in result  :
                print(info)
                sheet.write(count, 0, info['title'])
                count += 1
                # print(self.filedir + self.filename + '.xls')
            wbk.save(self.filedir + self.filename + '.xls')
        except Exception as e:
            print(e)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    # login = Login()
    # login.show()
    # if login.exec_():
    # w = CityLead()
    w = zdyMinKeyword()
    w.resize(350,430)
    w.show()
    sys.exit(app.exec_())
