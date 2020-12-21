from PyQt5.QtCore import QRect,pyqtSlot,QMetaObject,QThread,pyqtSignal
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import *
import sys
import threading
import re
import random
import titleVarModel
import optionModel
import cityModel
import titleModel
from SendArticle import SendLeft
import itertools
import apiAll
import sip

class TabWidgetTitle(QTabWidget):

    def __init__(self,tparms, *args, **kwargs):
        super(TabWidgetTitle, self).__init__(*args, **kwargs)
        conLayoutBody= QGridLayout()
        self.setLayout(conLayoutBody)
        self.BodyQtWidgetsTop = QTabWidget(self)
        self.BodyQtWidgetsTop.setFixedHeight(150)

        for i in range(6):
            if i == 0:
                self.AllQtWidgets = QWidget()
                self.titleQtWidgets = QWidget()
                self.titleQtWidgets.setStyleSheet('max-height:180px;')
                self.titleLabel = QLabel(self.titleQtWidgets)
                self.titleLabel.setText('标题组合')
                self.titleLabel.setGeometry(QRect(20, 10, 50, 40))

                self.titleText = QLineEdit(u"", self.titleQtWidgets)
                self.titleText.setGeometry(QRect(90, 10, 300, 30))

                self.firstVariable = QPushButton(QIcon(""), u"主变量", self.titleQtWidgets)
                self.firstVariable.setGeometry(QRect(90, 50, 70, 30))
                self.firstVariable.clicked.connect(lambda: self.titleQLineEdit("【主变量】"))

                self.twoVariable = QPushButton(QIcon(""), u"变量1", self.titleQtWidgets)
                self.twoVariable.setGeometry(QRect(170, 50, 70, 30))
                self.twoVariable.clicked.connect(lambda: self.titleQLineEdit("【变量1】"))

                self.threeVariable = QPushButton(QIcon(""), u"变量2", self.titleQtWidgets)
                self.threeVariable.setGeometry(QRect(250, 50, 70, 30))
                self.threeVariable.clicked.connect(lambda: self.titleQLineEdit("【变量2】"))

                self.fourVariable = QPushButton(QIcon(""), u"变量3", self.titleQtWidgets)
                self.fourVariable.setGeometry(QRect(320, 50, 70, 30))
                self.fourVariable.clicked.connect(lambda: self.titleQLineEdit("【变量3】"))

                self.takeUpSet = QCheckBox(self.titleQtWidgets)
                self.takeUpSet.setGeometry(QRect(430, 50, 90, 40))
                self.takeUpSet.setText('打乱顺序')

                self.produceTitle = QPushButton(QIcon(""), u"生成标题", self.titleQtWidgets)
                self.produceTitle.setGeometry(QRect(550, 50, 70, 30))
                self.produceTitle.clicked.connect(lambda: self.produceTitleData(tparms))

                self.deleteNull = QCheckBox(self.titleQtWidgets)
                self.deleteNull.setGeometry(QRect(90, 80, 80, 30))
                self.deleteNull.setText('去除空格')

                self.deleteRepeat = QCheckBox(self.titleQtWidgets)
                self.deleteRepeat.setGeometry(QRect(200, 80, 80, 30))
                self.deleteRepeat.setText('去除重复项')

                self.BodyQtWidgetsTop.addTab(self.titleQtWidgets, str('标题'))

            elif i == 1:

                self.oneQtWidgets = QWidget()
                self.oneQtWidgets.setStyleSheet('max-height:110px;')
                self.oneLabel = QLabel(self.oneQtWidgets)
                self.oneLabel.setText('关键词1')
                self.oneLabel.setGeometry(QRect(20, 10, 50, 30))

                self.oneText = QLineEdit(u"", self.oneQtWidgets)
                self.oneText.setGeometry(QRect(90, 10, 300, 30))

                self.firstVariableOne = QPushButton(QIcon(""), u"主变量", self.oneQtWidgets)
                self.firstVariableOne.setGeometry(QRect(90, 50, 70, 30))
                self.firstVariableOne.clicked.connect(lambda:self.var1QLineEdit("【主变量】"))

                self.twoVariableOne = QPushButton(QIcon(""), u"变量1", self.oneQtWidgets)
                self.twoVariableOne.setGeometry(QRect(170, 50, 70, 30))
                self.twoVariableOne.clicked.connect(lambda:self.var1QLineEdit("【变量1】"))

                self.threeVariableOne = QPushButton(QIcon(""), u"变量2", self.oneQtWidgets)
                self.threeVariableOne.setGeometry(QRect(250, 50, 70, 30))
                self.threeVariableOne.clicked.connect(lambda:self.var1QLineEdit("【变量2】"))

                self.fourVariableOne = QPushButton(QIcon(""), u"变量3", self.oneQtWidgets)
                self.fourVariableOne.setGeometry(QRect(320, 50, 70, 30))
                self.fourVariableOne.clicked.connect(lambda:self.var1QLineEdit("【变量3】"))

                self.BodyQtWidgetsTop.addTab(self.oneQtWidgets, '关键词' + str(i))
            elif i == 2:

                self.twoQtWidgets = QWidget()
                self.twoQtWidgets.setStyleSheet('max-height:110px;')
                self.twoLabel = QLabel(self.twoQtWidgets)
                self.twoLabel.setText('关键词2')
                self.twoLabel.setGeometry(QRect(20, 10, 50, 30))

                self.twoText = QLineEdit(u"", self.twoQtWidgets)
                self.twoText.setGeometry(QRect(90, 10, 300, 30))

                self.firstVariabletwo = QPushButton(QIcon(""), u"主变量", self.twoQtWidgets)
                self.firstVariabletwo.setGeometry(QRect(90, 50, 70, 30))
                self.firstVariabletwo.clicked.connect(lambda:self.var2QLineEdit("【主变量】"))

                self.twoVariabletwo = QPushButton(QIcon(""), u"变量1", self.twoQtWidgets)
                self.twoVariabletwo.setGeometry(QRect(170, 50, 70, 30))
                self.twoVariabletwo.clicked.connect(lambda:self.var2QLineEdit("【变量1】"))

                self.threeVariabletwo = QPushButton(QIcon(""), u"变量2", self.twoQtWidgets)
                self.threeVariabletwo.setGeometry(QRect(250, 50, 70, 30))
                self.threeVariabletwo.clicked.connect(lambda:self.var2QLineEdit("【变量2】"))

                self.fourVariabletwo = QPushButton(QIcon(""), u"变量3", self.twoQtWidgets)
                self.fourVariabletwo.setGeometry(QRect(320, 50, 70, 30))
                self.fourVariabletwo.clicked.connect(lambda:self.var2QLineEdit("【变量3】"))

                self.BodyQtWidgetsTop.addTab(self.twoQtWidgets, '关键词' + str(i))

            elif i == 3:

                self.three2QtWidgets = QWidget()
                self.three2QtWidgets.setStyleSheet('max-height:110px;')
                self.three2Label = QLabel(self.three2QtWidgets)
                self.three2Label.setText('关键词3')
                self.three2Label.setGeometry(QRect(20, 10, 50, 30))

                self.three2Text = QLineEdit(u"", self.three2QtWidgets)
                self.three2Text.setGeometry(QRect(90, 10, 300, 30))

                self.firstVariablethree2 = QPushButton(QIcon(""), u"主变量", self.three2QtWidgets)
                self.firstVariablethree2.setGeometry(QRect(90, 50, 70, 30))
                self.firstVariablethree2.clicked.connect(lambda:self.var3QLineEdit("【主变量】"))

                self.three2Variablethree2 = QPushButton(QIcon(""), u"变量1", self.three2QtWidgets)
                self.three2Variablethree2.setGeometry(QRect(170, 50, 70, 30))
                self.three2Variablethree2.clicked.connect(lambda:self.var3QLineEdit("【变量1】"))

                self.threeVariablethree2 = QPushButton(QIcon(""), u"变量2", self.three2QtWidgets)
                self.threeVariablethree2.setGeometry(QRect(250, 50, 70, 30))
                self.threeVariablethree2.clicked.connect(lambda:self.var3QLineEdit("【变量2】"))

                self.fourVariablethree2 = QPushButton(QIcon(""), u"变量3", self.three2QtWidgets)
                self.fourVariablethree2.setGeometry(QRect(320, 50, 70, 30))
                self.fourVariablethree2.clicked.connect(lambda:self.var3QLineEdit("【变量3】"))

                self.BodyQtWidgetsTop.addTab(self.three2QtWidgets, '关键词' + str(i))

            elif i == 4:
                self.four2QtWidgets = QWidget()
                self.four2QtWidgets.setStyleSheet('max-height:110px;')
                self.four2Label = QLabel(self.four2QtWidgets)
                self.four2Label.setText('关键词4')
                self.four2Label.setGeometry(QRect(20, 10, 50, 30))

                self.four2Text = QLineEdit(u"", self.four2QtWidgets)
                self.four2Text.setGeometry(QRect(90, 10, 300, 30))

                self.firstVariablefour2 = QPushButton(QIcon(""), u"主变量", self.four2QtWidgets)
                self.firstVariablefour2.setGeometry(QRect(90, 50, 70, 30))
                self.firstVariablefour2.clicked.connect(lambda:self.var4QLineEdit("【主变量】"))

                self.four2Variablefour2 = QPushButton(QIcon(""), u"变量1", self.four2QtWidgets)
                self.four2Variablefour2.setGeometry(QRect(170, 50, 70, 30))
                self.four2Variablefour2.clicked.connect(lambda:self.var4QLineEdit("【变量1】"))

                self.threeVariablefour2 = QPushButton(QIcon(""), u"变量2", self.four2QtWidgets)
                self.threeVariablefour2.setGeometry(QRect(250, 50, 70, 30))
                self.threeVariablefour2.clicked.connect(lambda:self.var4QLineEdit("【变量2】"))

                self.fourVariablefour2 = QPushButton(QIcon(""), u"变量3", self.four2QtWidgets)
                self.fourVariablefour2.setGeometry(QRect(320, 50, 70, 30))
                self.fourVariablefour2.clicked.connect(lambda:self.var4QLineEdit("【变量3】"))

                self.BodyQtWidgetsTop.addTab(self.four2QtWidgets, '关键词' + str(i))

            elif i == 5:
                self.five2QtWidgets = QWidget()
                self.five2QtWidgets.setStyleSheet('max-height:110px;')
                self.five2Label = QLabel(self.five2QtWidgets)
                self.five2Label.setText('关键词5')
                self.five2Label.setGeometry(QRect(20, 10, 50, 30))

                self.five2Text = QLineEdit(u"", self.five2QtWidgets)
                self.five2Text.setGeometry(QRect(90, 10, 300, 30))

                self.firstVariablefive2 = QPushButton(QIcon(""), u"主变量", self.five2QtWidgets)
                self.firstVariablefive2.setGeometry(QRect(90, 50, 70, 30))
                self.firstVariablefive2.clicked.connect(lambda:self.var5QLineEdit("【主变量】"))

                self.five2Variablefive2 = QPushButton(QIcon(""), u"变量1", self.five2QtWidgets)
                self.five2Variablefive2.setGeometry(QRect(170, 50, 70, 30))
                self.five2Variablefive2.clicked.connect(lambda:self.var5QLineEdit("【变量1】"))

                self.threeVariablefive2 = QPushButton(QIcon(""), u"变量2", self.five2QtWidgets)
                self.threeVariablefive2.setGeometry(QRect(250, 50, 70, 30))
                self.threeVariablefive2.clicked.connect(lambda:self.var5QLineEdit("【变量2】"))

                self.fourVariablefive2 = QPushButton(QIcon(""), u"变量3", self.five2QtWidgets)
                self.fourVariablefive2.setGeometry(QRect(320, 50, 70, 30))
                self.fourVariablefive2.clicked.connect(lambda:self.var5QLineEdit("【变量3】"))

                self.BodyQtWidgetsTop.addTab(self.five2QtWidgets, '关键词' + str(i))
            else:
                self.BodyQtWidgetsTop.addTab(QLabel('Tab' + str(i)), '关键词'+str(i))


        conLayoutBody.addWidget(self.BodyQtWidgetsTop, 1, 1)

        self.BodyQtWidgets = QWidget(self)
        conLayoutBody.addWidget(self.BodyQtWidgets, 2, 1)
        conLayoutBodyOption = QGridLayout()
        self.BodyQtWidgets.setLayout(conLayoutBodyOption)

        self.BodyTitle_first = QWidget(self.BodyQtWidgets)
        self.BodyTitle_first.setStyleSheet('border:1px solid #dddddd')
        conLayoutBodyOption_first = QGridLayout()
        self.BodyTitle_first.setLayout(conLayoutBodyOption_first)

        self.BodyTitle_first_title = QLabel(self.BodyTitle_first)
        self.BodyTitle_first_title.setText('主变量，共0行')
        conLayoutBodyOption_first.addWidget(self.BodyTitle_first_title, 1, 1)

        self.BodyTitle_first_content = QTextEdit(self.BodyTitle_first)
        self.BodyTitle_first_content.setObjectName("zhu")
        conLayoutBodyOption_first.addWidget(self.BodyTitle_first_content, 2, 1,1,2)

        self.randomClick = QCheckBox(self.BodyTitle_first)
        self.randomClick.setText('随机')
        conLayoutBodyOption_first.addWidget(self.randomClick, 3, 1)

        self.city_lead = QPushButton(QIcon(""), u"地名生成器", self.BodyTitle_first)
        self.city_lead.clicked.connect(self.cityLeadDef)
        conLayoutBodyOption_first.addWidget(self.city_lead, 3, 2)

        self.clear_keyword = QPushButton(QIcon(""), u"清空", self.BodyTitle_first)
        self.clear_keyword.clicked.connect(self.clearZhu)
        conLayoutBodyOption_first.addWidget(self.clear_keyword, 4, 1)

        self.keyword_take = QPushButton(QIcon(""), u"打乱", self.BodyTitle_first)
        self.keyword_take.clicked.connect(self.random_Zhu)
        conLayoutBodyOption_first.addWidget(self.keyword_take, 4, 2)


        ##关键词1

        self.BodyTitle_two = QWidget(self.BodyQtWidgets)
        self.BodyTitle_two.setStyleSheet('border:1px solid #dddddd')
        conLayoutBodyOption_two = QGridLayout()
        self.BodyTitle_two.setLayout(conLayoutBodyOption_two)
        self.BodyTitle_two_title = QLabel(self.BodyTitle_two)
        self.BodyTitle_two_title.setText('变量1，共0行')
        conLayoutBodyOption_two.addWidget(self.BodyTitle_two_title, 1, 1)

        self.BodyTitle_two_content = QTextEdit(self.BodyTitle_two)
        self.BodyTitle_two_content.setStyleSheet('margin-top:0')
        self.BodyTitle_two_content.setObjectName("bl1")
        conLayoutBodyOption_two.addWidget(self.BodyTitle_two_content, 2, 1,1,2)

        self.randomClick_two = QCheckBox(self.BodyTitle_two)
        self.randomClick_two.setText('随机')
        conLayoutBodyOption_two.addWidget(self.randomClick_two, 3, 1)

        self.city_lead_two = QPushButton(QIcon(""), u"长尾词挖掘", self.BodyTitle_two)
        self.city_lead_two.clicked.connect(self.excavate)
        conLayoutBodyOption_two.addWidget(self.city_lead_two, 3, 2)

        self.clear_keyword_two = QPushButton(QIcon(""), u"清空", self.BodyTitle_two)
        self.clear_keyword_two.clicked.connect(self.clearVar1)
        conLayoutBodyOption_two.addWidget(self.clear_keyword_two, 4, 1)

        self.keyword_take_two = QPushButton(QIcon(""), u"打乱", self.BodyTitle_two)
        self.keyword_take_two.clicked.connect(self.random_Var1)
        conLayoutBodyOption_two.addWidget(self.keyword_take_two, 4, 2)

        ##关键词2

        self.BodyTitle_three = QWidget(self.BodyQtWidgets)
        self.BodyTitle_three.setStyleSheet('border:1px solid #dddddd')
        conLayoutBodyOption_three = QGridLayout()
        self.BodyTitle_three.setLayout(conLayoutBodyOption_three)

        self.BodyTitle_three_title = QLabel(self.BodyTitle_three)
        self.BodyTitle_three_title.setText('变量2，共0行')
        conLayoutBodyOption_three.addWidget(self.BodyTitle_three_title, 1, 1)

        self.BodyTitle_three_content = QTextEdit(self.BodyTitle_three)
        self.BodyTitle_three_content.setObjectName("bl2")
        conLayoutBodyOption_three.addWidget(self.BodyTitle_three_content,2, 1,1,2)

        self.randomClick_three = QCheckBox(self.BodyTitle_three)
        self.randomClick_three.setText('随机')
        conLayoutBodyOption_three.addWidget(self.randomClick_three,3, 1)

        self.clear_keyword_three = QPushButton(QIcon(""), u"清空", self.BodyTitle_three)
        self.clear_keyword_three.clicked.connect(self.clearVar2)
        conLayoutBodyOption_three.addWidget(self.clear_keyword_three,3, 2)

        self.keyword_take_three = QPushButton(QIcon(""), u"打乱", self.BodyTitle_three)
        self.keyword_take_three.clicked.connect(self.random_Var2)
        conLayoutBodyOption_three.addWidget(self.keyword_take_three,4, 1)


        ##关键词3
        self.BodyTitle_four = QWidget(self.BodyQtWidgets)
        self.BodyTitle_four.setStyleSheet('border:1px solid #dddddd')
        conLayoutBodyOption_four = QGridLayout()
        self.BodyTitle_four.setLayout(conLayoutBodyOption_four)

        self.BodyTitle_four_title = QLabel(self.BodyTitle_four)
        self.BodyTitle_four_title.setText('变量3，共0行')
        conLayoutBodyOption_four.addWidget(self.BodyTitle_four_title,1, 1)

        self.BodyTitle_four_content = QTextEdit(self.BodyTitle_four)
        self.BodyTitle_four_content.setObjectName("bl3")
        conLayoutBodyOption_four.addWidget(self.BodyTitle_four_content,2, 1,1,2)

        self.randomClick_four = QCheckBox(self.BodyTitle_four)
        self.randomClick_four.setText('随机')
        conLayoutBodyOption_four.addWidget(self.randomClick_four,3, 1)

        self.clear_keyword_four = QPushButton(QIcon(""), u"清空", self.BodyTitle_four)
        self.clear_keyword_four.clicked.connect(self.clearVar3)
        conLayoutBodyOption_four.addWidget(self.clear_keyword_four,3, 2)

        self.keyword_take_four = QPushButton(QIcon(""), u"打乱", self.BodyTitle_four)
        self.keyword_take_four.clicked.connect(self.random_Var3)
        conLayoutBodyOption_four.addWidget(self.keyword_take_four,4, 1)

        conLayoutBodyOption.addWidget(self.BodyTitle_first, 1, 1)
        conLayoutBodyOption.addWidget(self.BodyTitle_two, 1, 2)
        conLayoutBodyOption.addWidget(self.BodyTitle_three, 1, 3)
        conLayoutBodyOption.addWidget(self.BodyTitle_four, 1, 4)

        self.produceTitleSave = QPushButton(QIcon(""), u"保存", self.BodyQtWidgets)
        self.produceTitleSave.clicked.connect(lambda: self.saveTitle(tparms))
        conLayoutBody.addWidget(self.produceTitleSave, 3, 1)

        self.VarFirstOnline(tparms)
        self.titleQLineEditLoading(tparms)

        QMetaObject.connectSlotsByName(self)
        self.on_zhu_textChanged()

    @pyqtSlot()
    def on_zhu_textChanged(self):
        textZhu = self.BodyTitle_first_content.toPlainText()
        countZhu = len(re.split('\n', textZhu))
        self.BodyTitle_first_title.setText('主变量，共'+str(countZhu)+'行')

        Bl1text = self.BodyTitle_two_content.toPlainText()
        countBl1 = len(re.split('\n', Bl1text))
        self.BodyTitle_two_title.setText('变量1，共' + str(countBl1) + '行')

        Bl2text = self.BodyTitle_three_content.toPlainText()
        countBl2 = len(re.split('\n', Bl2text))
        self.BodyTitle_three_title.setText('变量2，共' + str(countBl2) + '行')

        Bl3text = self.BodyTitle_four_content.toPlainText()
        countBl3 = len(re.split('\n', Bl3text))
        self.BodyTitle_four_title.setText('变量3，共' + str(countBl3) + '行')
    @pyqtSlot()
    def on_bl1_textChanged(self):
        textZhu = self.BodyTitle_first_content.toPlainText()
        countZhu = len(re.split('\n', textZhu))
        self.BodyTitle_first_title.setText('主变量，共' + str(countZhu) + '行')

        Bl1text = self.BodyTitle_two_content.toPlainText()
        countBl1 = len(re.split('\n', Bl1text))
        self.BodyTitle_two_title.setText('变量1，共' + str(countBl1) + '行')

        Bl2text = self.BodyTitle_three_content.toPlainText()
        countBl2 = len(re.split('\n', Bl2text))
        self.BodyTitle_three_title.setText('变量2，共' + str(countBl2) + '行')

        Bl3text = self.BodyTitle_four_content.toPlainText()
        countBl3 = len(re.split('\n', Bl3text))
        self.BodyTitle_four_title.setText('变量3，共' + str(countBl3) + '行')

    @pyqtSlot()
    def on_bl2_textChanged(self):
        textZhu = self.BodyTitle_first_content.toPlainText()
        countZhu = len(re.split('\n', textZhu))
        self.BodyTitle_first_title.setText('主变量，共' + str(countZhu) + '行')

        Bl1text = self.BodyTitle_two_content.toPlainText()
        countBl1 = len(re.split('\n', Bl1text))
        self.BodyTitle_two_title.setText('变量1，共' + str(countBl1) + '行')

        Bl2text = self.BodyTitle_three_content.toPlainText()
        countBl2 = len(re.split('\n', Bl2text))
        self.BodyTitle_three_title.setText('变量2，共' + str(countBl2) + '行')

        Bl3text = self.BodyTitle_four_content.toPlainText()
        countBl3 = len(re.split('\n', Bl3text))
        self.BodyTitle_four_title.setText('变量3，共' + str(countBl3) + '行')

    @pyqtSlot()
    def on_bl3_textChanged(self):
        textZhu = self.BodyTitle_first_content.toPlainText()
        countZhu = len(re.split('\n', textZhu))
        self.BodyTitle_first_title.setText('主变量，共' + str(countZhu) + '行')

        Bl1text = self.BodyTitle_two_content.toPlainText()
        countBl1 = len(re.split('\n', Bl1text))
        self.BodyTitle_two_title.setText('变量1，共' + str(countBl1) + '行')

        Bl2text = self.BodyTitle_three_content.toPlainText()
        countBl2 = len(re.split('\n', Bl2text))
        self.BodyTitle_three_title.setText('变量2，共' + str(countBl2) + '行')

        Bl3text = self.BodyTitle_four_content.toPlainText()
        countBl3 = len(re.split('\n', Bl3text))
        self.BodyTitle_four_title.setText('变量3，共' + str(countBl3) + '行')

    def excavate(self):
        try:
            text, ok = QInputDialog.getText(self, '挖掘长尾词', '关键词：')
            if ok and text:
                Content = apiAll.getKeywordsList(text)
                lastContent = self.BodyTitle_two_content.toPlainText()
                Details = ('\n').join(Content)
                self.BodyTitle_two_content.setText(lastContent + Details)
        except Exception as e:
            print(e)

    def titleQLineEdit(self,text):
        old = self.titleText.text()
        self.titleText.setText(old+text)

    def var1QLineEdit(self,text):
        old = self.oneText.text()
        self.oneText.setText(old+text)

    def var2QLineEdit(self, text):
        old = self.twoText.text()
        self.twoText.setText(old + text)

    def var3QLineEdit(self, text):
        old = self.three2Text.text()
        self.three2Text.setText(old + text)

    def var4QLineEdit(self, text):
        old = self.four2Text.text()
        self.four2Text.setText(old + text)

    def var5QLineEdit(self, text):
        old = self.five2Text.text()
        self.five2Text.setText(old + text)

    def saveTitle(self,tparms,theme=None):
        Title_first_content = self.BodyTitle_first_content.toPlainText()
        zhu_list = re.split('\n', Title_first_content)

        Title_two_content = self.BodyTitle_two_content.toPlainText()
        var1_list = re.split('\n', Title_two_content)

        Title_three_content = self.BodyTitle_three_content.toPlainText()
        var2_list = re.split('\n', Title_three_content)

        Title_four_content = self.BodyTitle_four_content.toPlainText()
        var3_list = re.split('\n', Title_four_content)

        titleVarModel.deleteAll(tparms['admin_id'],tparms['task_id'],tparms['config_id'])
        titleVarModel.add_Data(zhu_list,tparms['admin_id'],titleVarModel.config_Zhu,tparms['task_id'],tparms['config_id'])
        titleVarModel.add_Data(var1_list,tparms['admin_id'],titleVarModel.config_Var1,tparms['task_id'],tparms['config_id'])
        titleVarModel.add_Data(var2_list,tparms['admin_id'],titleVarModel.config_Var2,tparms['task_id'],tparms['config_id'])
        titleVarModel.add_Data(var3_list,tparms['admin_id'],titleVarModel.config_Var3,tparms['task_id'],tparms['config_id'])

        titleText = self.titleText.text()
        oneText = self.oneText.text()
        twoText = self.twoText.text()
        three2Text = self.three2Text.text()
        four2Text = self.four2Text.text()
        five2Text = self.five2Text.text()
        optionModel.titleComposeSave(tparms['admin_id'],titleText,oneText,twoText,three2Text,four2Text,five2Text,tparms['task_id'],tparms['config_id'])
        try:
            QMessageBox.information(self, u'成功', u'保存成功')
        except Exception as e:
            print(e)
    def VarFirstOnline(self,tparms):
        list_all = titleVarModel.titleData(tparms['admin_id'],tparms['task_id'],tparms['config_id'])

        keyword_res_zhu = ''
        keyword_res_var1 = ''
        keyword_res_var2 = ''
        keyword_res_var3 = ''
        for info in list_all:
            if info[0] == titleVarModel.config_Zhu:
                keyword_res_zhu += info[1]+'\n'
            elif info[0] == titleVarModel.config_Var1:
                keyword_res_var1 += info[1]+'\n'
            elif info[0] == titleVarModel.config_Var2:
                keyword_res_var2 += info[1]+'\n'
            elif info[0] == titleVarModel.config_Var3:
                keyword_res_var3 += info[1]+'\n'

        self.BodyTitle_first_content.setText(keyword_res_zhu[:-1])
        self.BodyTitle_two_content.setText(keyword_res_var1[:-1])
        self.BodyTitle_three_content.setText(keyword_res_var2[:-1])
        self.BodyTitle_four_content.setText(keyword_res_var3[:-1])

    def produceTitleData(self,tparms):
        titleAll = []
        info = self.titleText.text()

        try:
            self.produceTitle.setDisabled(True)
            key = 0
            keywordList = {}
            blArr = ['【主变量】','【变量1】','【变量2】','【变量3】']
            for bl in blArr:
                if bl in info:
                    nbl = bl.replace('】','')
                    nbl = nbl.replace('【', '')
                    info = info.replace(bl,'#,#{}#,#'.format(nbl))
            arrlist = re.split('#,#', info)
            # print(arrlist)
            arr = []
            for a in arrlist:
                if len(a) > 0:
                    arr.append(a)
            for str in arr:
                strAll = ''
                keywordList['{}'.format(key)] = self.testKeywordAll(str)
                key += 1
            self.str = ''
            isnum = 0
            regex_All = ''
            for info in keywordList:
                regex = ''
                if len(keywordList[info]) <= 1:
                    regex = keywordList[info][0].replace(',','*1*').replace('\'',"*2*").replace('(',"*3*").replace(')',"*4*").replace(' ',"*5*")+'|'
                    regex = regex[:-1]
                else:
                    regex = "|".join('%s' %id.replace(',','*1*').replace('\'',"*2*").replace('(',"*3*").replace(')',"*4*").replace(' ',"*5*") for id in keywordList[info])
#                 # print(regex)
                regex_All = regex_All+'+'+'('+regex+')'
            rl = Regex2List(regex_path=regex_All[1:], regex_list=["\(", "\)", "\+", "\（", "\）"])


            if self.deleteNull.isChecked():
                for res in rl.run():
                    if self.deleteRepeat.isChecked():
                        if re.sub(r"\s+", "", res) not in titleAll:
                            titleAll.append(re.sub(r"\s+", "", res))
                    else:
                        titleAll.append(re.sub(r"\s+", "", res))
            else:
                for res in rl.run():
                    if self.deleteRepeat.isChecked():
                        if res not in titleAll:
                            titleAll.append(res)
                    else:
                        titleAll.append(res)

            if self.takeUpSet.isChecked():
                random.shuffle(titleAll)

            self.send_parms = TitleStartNow(tparms, titleAll)
            self.send_parms.finishSignal_pc_up.connect(self.is_ok)
            self.send_parms.start()
        except Exception as e:
            print(e)

    def is_ok(self,reres):
        if reres[1] == 'success':
            QMessageBox.information(self, u'完成', u'生成完成')
            self.produceTitle.setDisabled(False)
        else:
            QMessageBox.information(self, u'失败', u'生成失败')
            self.produceTitle.setDisabled(False)

    def getKeyword(self,list):
        key = 1
        if len(list) > 0:
            for val in list[key]:
                self.str+=self.str+val
            key+=1
            return list[key]
    def testKeywordAll(self,str):
        zhu_list = []
        if str in '主变量':
            Title_first_content = self.BodyTitle_first_content.toPlainText()
            zhu_list = re.split('\n', Title_first_content)
        elif str in '变量1':
            Title_two_content = self.BodyTitle_two_content.toPlainText()
            zhu_list = re.split('\n', Title_two_content)
        elif str in '变量2':
            Title_three_content = self.BodyTitle_three_content.toPlainText()
            zhu_list = re.split('\n', Title_three_content)
        elif str in '变量3':
            Title_four_content = self.BodyTitle_four_content.toPlainText()
            zhu_list = re.split('\n', Title_four_content)
        else:
            zhu_list.append(str)
        return zhu_list
    def cityLeadDef(self):
        self.cityUi = QWidget()
        self.cityUi.resize(727, 607)
        self.number = -1

        self.provinceAll = QWidget(self.cityUi)

        self.topFiller = QWidget(self.provinceAll)
        self.topFiller.setMinimumSize(600, 200)  #######设置滚动条的尺寸

        self.conLayout = QGridLayout(self.topFiller)

        self.provinceAll = cityModel.getProvince()
        self.hang = 1
        self.provinceButton_click = locals()
        for filename in self.provinceAll:
            if self.number > 4:
                self.hang += 1
                self.number = 0
            else:
                self.number += 1

            self.provinceButton = QLabel(self.cityUi)
            self.provinceButton.setStyleSheet('min-width:120px;max-width:300px')
            self.provinceButton_click['{}'.format(filename)] = QCheckBox(self.provinceButton)
            self.provinceButton_click['{}'.format(filename)].setText(u'{}'.format(filename))

            self.conLayout.addWidget(self.provinceButton, self.hang, self.number)

        self.scroll = QScrollArea(self.cityUi)
        self.scroll.setMinimumSize(500, 200)
        self.scroll.setWidget(self.topFiller)
        self.scroll.setStyleSheet('max-width:500px;max-height:200px;')

        self.button = QWidget(self.cityUi)
        self.allSelect = QPushButton(QIcon(""), u"全选", self.button)
        self.fanSelect = QPushButton(QIcon(""), u"反选", self.button)
        self.allSelectNo = QPushButton(QIcon(""), u"全不选", self.button)
        self.allSelect.setGeometry(QRect(0, 20, 90, 30))
        self.fanSelect.setGeometry(QRect(0, 90, 90, 30))
        self.allSelectNo.setGeometry(QRect(0, 170, 90, 30))
        self.button.setGeometry(QRect(508, 0, 183, 221))

        self.allSelect.clicked.connect(self.allSelected)
        self.fanSelect.clicked.connect(self.fanSelected)
        self.allSelectNo.clicked.connect(self.allSelectedNo)

        self.cityList = QTextEdit(self.cityUi)
        self.cityList.setGeometry(10, 225, 230, 350)

        self.click_province = QCheckBox(self.cityUi)
        self.click_province.setChecked(True)
        self.click_province.setGeometry(QRect(271, 255, 110, 20))
        self.click_province.setText(u'去掉 “省')

        self.click_city = QCheckBox(self.cityUi)
        self.click_city.setChecked(True)
        self.click_city.setGeometry(QRect(271, 285, 110, 20))
        self.click_city.setText(u'去掉 “市')

        self.click_xian = QCheckBox(self.cityUi)
        self.click_xian.setChecked(True)
        self.click_xian.setGeometry(QRect(271, 315, 110, 20))
        self.click_xian.setText(u'去掉 “县')

        self.click_city_xian = QCheckBox(self.cityUi)
        self.click_city_xian.setChecked(True)
        self.click_city_xian.setGeometry(QRect(271, 345, 130, 20))
        self.click_city_xian.setText(u'去掉所有行政区划词')

        self.clear_btn = QPushButton(QIcon(""), u"清空", self.cityUi)
        self.clear_btn.setGeometry(QRect(271, 484, 128, 27))
        self.clear_btn.clicked.connect(self.clear_City)

        self.range_btn = QPushButton(QIcon(""), u"随机打乱", self.cityUi)
        self.range_btn.setGeometry(QRect(271, 518, 128, 27))
        self.range_btn.clicked.connect(self.random_City)

        self.addZhu_btn = QPushButton(QIcon(""), u"添加到主变量", self.cityUi)
        self.addZhu_btn.setGeometry(QRect(271, 552, 128, 27))
        self.addZhu_btn.clicked.connect(self.getCityContent)

        self.obtain_all_btn = QPushButton(QIcon(""), u"获取省+市+县", self.cityUi)
        self.obtain_all_btn.setGeometry(QRect(440, 230, 270, 37))
        self.obtain_all_btn.clicked.connect(lambda: self.obtainAllCity(1))

        self.obtain_provinceCity_btn = QPushButton(QIcon(""), u"获取省+市", self.cityUi)
        self.obtain_provinceCity_btn.setGeometry(QRect(440, 290, 270, 37))
        self.obtain_provinceCity_btn.clicked.connect(lambda: self.obtainAllCity(2))

        self.obtain_cityXian_btn = QPushButton(QIcon(""), u"获取市+县", self.cityUi)
        self.obtain_cityXian_btn.setGeometry(QRect(440, 340, 270, 37))
        self.obtain_cityXian_btn.clicked.connect(lambda: self.obtainAllCity(3))

        self.obtain_provinceXian_btn = QPushButton(QIcon(""), u"获取省+县", self.cityUi)
        self.obtain_provinceXian_btn.setGeometry(QRect(440, 390, 270, 37))
        self.obtain_provinceXian_btn.clicked.connect(lambda: self.obtainAllCity(4))

        self.obtain_province = QPushButton(QIcon(""), u"获取省", self.cityUi)
        self.obtain_province.setGeometry(QRect(440, 440, 270, 37))
        self.obtain_province.clicked.connect(lambda: self.obtainAllCity(5))

        self.obtain_city = QPushButton(QIcon(""), u"获取市", self.cityUi)
        self.obtain_city.setGeometry(QRect(440, 490, 270, 37))
        self.obtain_city.clicked.connect(lambda: self.obtainAllCity(6))

        self.obtain_xian = QPushButton(QIcon(""), u"获取县", self.cityUi)
        self.obtain_xian.setGeometry(QRect(440, 540, 270, 37))
        self.obtain_xian.clicked.connect(lambda: self.obtainAllCity(7))

        self.cityUi.setWindowTitle(u"地名生成器")
        self.cityUi.show()

    def getCityContent(self):
        cityContent = self.cityList.toPlainText()
        lastContent = self.BodyTitle_first_content.toPlainText()
        self.BodyTitle_first_content.setText(lastContent + cityContent)
        self.cityUi.close()

    def obtainAllCity(self, type):
        is_pro = 0
        is_city = 0
        is_xian = 0
        is_regionsp = 0

        if self.click_province.isChecked():
            is_pro = 1
        if self.click_city.isChecked():
            is_city = 1
        if self.click_xian.isChecked():
            is_xian = 1
        if self.click_city_xian.isChecked():
            is_regionsp = 1
        city = []
        for info in self.provinceAll:
            if self.provinceButton_click['{}'.format(info)].isChecked():
                city.append(self.provinceButton_click['{}'.format(info)].text())
        if type == 1:
            isnewCity = cityModel.getSelectedDataAll(city, is_pro, is_city, is_xian, is_regionsp)
        elif type == 2:
            isnewCity = cityModel.getSelectedDataProCity(city, is_pro, is_city, is_xian, is_regionsp)
        elif type == 3:
            isnewCity = cityModel.getSelectedDataCityXian(city, is_pro, is_city, is_xian, is_regionsp)
        elif type == 4:
            isnewCity = cityModel.getSelectedDataProXian(city, is_pro, is_city, is_xian, is_regionsp)
        elif type == 5:
            isnewCity = cityModel.getSelectedDataPro(city, is_pro, is_city, is_xian, is_regionsp)
        elif type == 6:
            isnewCity = cityModel.getSelectedDataCity(city, is_pro, is_city, is_xian, is_regionsp)
        elif type == 7:
            isnewCity = cityModel.getSelectedDataXian(city, is_pro, is_city, is_xian, is_regionsp)

        isnewCityText = ''
        for info in isnewCity:
            isnewCityText += info + '\n'
        isnewCityText = isnewCityText.strip('\n')
        self.cityList.setText(isnewCityText)

    def clear_City(self):
        self.cityList.setText('')

    def random_City(self):
        city_content = self.cityList.toPlainText()
        city_list = re.split('\n', city_content)
        random.shuffle(city_list)
        isnewCityText = ''
        for info in city_list:
            if len(info) > 0:
                isnewCityText += info + '\n'
        self.cityList.setText(isnewCityText)

    def random_Zhu(self):
        content = self.BodyTitle_first_content.toPlainText()
        list = re.split('\n', content)
        random.shuffle(list)
        isnewText = ''
        for info in list:
            if len(info) > 0:
                isnewText += info + '\n'
        self.BodyTitle_first_content.setText(isnewText)

    def random_Var1(self):
        content = self.BodyTitle_two_content.toPlainText()
        list = re.split('\n', content)
        random.shuffle(list)
        isnewText = ''
        for info in list:
            if len(info) > 0:
                isnewText += info + '\n'
        self.BodyTitle_two_content.setText(isnewText)

    def random_Var2(self):
        content = self.BodyTitle_three_content.toPlainText()
        list = re.split('\n', content)
        random.shuffle(list)
        isnewText = ''
        for info in list:
            if len(info) > 0:
                isnewText += info + '\n'
        self.BodyTitle_three_content.setText(isnewText)

    def random_Var3(self):
        content = self.BodyTitle_four_content.toPlainText()
        list = re.split('\n', content)
        random.shuffle(list)
        isnewText = ''
        for info in list:
            if len(info) > 0:
                isnewText += info + '\n'
        self.BodyTitle_four_content.setText(isnewText)

    def allSelected(self):
        for info in self.provinceAll:
            self.provinceButton_click['{}'.format(info)].setChecked(True)

    def fanSelected(self):
        for info in self.provinceAll:
            if self.provinceButton_click['{}'.format(info)].isChecked():
                self.provinceButton_click['{}'.format(info)].setChecked(False)
            else:
                self.provinceButton_click['{}'.format(info)].setChecked(True)

    def allSelectedNo(self):
        for info in self.provinceAll:
            self.provinceButton_click['{}'.format(info)].setChecked(False)

    def clearZhu(self):
        self.BodyTitle_first_content.setText('')

    def clearVar1(self):
        self.BodyTitle_two_content.setText('')

    def clearVar2(self):
        self.BodyTitle_three_content.setText('')

    def clearVar3(self):
        self.BodyTitle_four_content.setText('')

    def titleQLineEditLoading(self,tparms):
        try:
            data = optionModel.titleComposeData(tparms['admin_id'],tparms['task_id'],'title_compose',tparms['config_id'])
            if len(data) > 0:
                self.titleText.setText(data['title_info'])
                self.oneText.setText(data['keyword_var1'])
                self.twoText.setText(data['keyword_var2'])
                self.three2Text.setText(data['keyword_var3'])
                self.four2Text.setText(data['keyword_var4'])
                self.five2Text.setText(data['keyword_var4'])
        except Exception as e:
            print(e)


class TitleStartNow(QThread):
    finishSignal_pc_up = pyqtSignal(list)

    def __init__(self,tparms,title, *args, **kwargs):
        super(TitleStartNow, self).__init__(*args, **kwargs)
        self.title = title
        self.tparms = tparms
        self.lock = threading.RLock()
    def run(self):
        a = titleModel.titleDataAdd(self.tparms['admin_id'], self.title, self.tparms['task_id'], self.tparms['config_id'])
        if a == 1:
            self.finishSignal_pc_up.emit(['continue', 'success'])
        else:
            self.finishSignal_pc_up.emit(['continue', 'false'])

class Regex2List(object):
    def __init__(self, regex_path, regex_list):
        self.regex_arr = regex_path
        self.regex_list = regex_list
    @staticmethod
    def get_list(str_list):
        res, data = [], ['']
        for line in str_list:
            if line == '':
                continue
            else:
                data = itertools.product(data, line.split('|'))
        for result in data:
            res.append(str(result).replace(' ','').replace('\'','').replace('(','').replace(')','').replace(',','').replace('*1*',',').replace("*2*",'\'').replace("*3*",'(').replace("*4*",')').replace("*5*",' '))

        return res

    def run(self):
        res_list = []
        data = re.split("|".join(self.regex_list), self.regex_arr)
        newData = []
        for strnew in data:
            if len(strnew) > 0:
                newData.append(strnew)
        for res in self.get_list(newData):
            res_list.append(res)
        return res_list


if __name__ == '__main__':
    app = QApplication(sys.argv)
    tparms = {'admin_id':'99'}
    w = TabWidgetTitle(tparms,tabPosition=TabWidgetTitle.North)
    w.resize(1100,600)
    w.show()
    sys.exit(app.exec_())