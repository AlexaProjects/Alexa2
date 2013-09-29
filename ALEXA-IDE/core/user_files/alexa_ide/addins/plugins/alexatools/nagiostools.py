# -*- coding: utf-8 -*-
#
# Copyright (C) 2013 Alan Pipitone
#
# This file is part of Al'EXA-IDE.
#
# Al'EXA-IDE is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Al'EXA-IDE is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Al'EXA-IDE.  If not, see <http://www.gnu.org/licenses/>.

import os

#QT Toolkit
from PyQt4.QtGui import *
from PyQt4.QtCore import *


class NagiosTools(QWidget):

    def __init__(self, plugin):
        super(NagiosTools, self).__init__()

        self.plugin = plugin
        self.plug_path = plugin.plug_path

        self.initUI()

    def initUI(self):
        icon = QIcon()
        icon.addPixmap(QPixmap(self.plug_path + "/alexatools/images/view-statistics2.png"), QIcon.Normal, QIcon.Off)
        self.setWindowIcon(icon)
        self.setWindowTitle("Al\'exa - Nagios Utilities")
        #self.setObjectName("self")
        self.resize(380, 432)
        self.tabWidget = QTabWidget(self)
        self.tabWidget.setGeometry(QRect(10, 10, 359, 374))
        self.tabWidget.setObjectName("tabWidget")
        self.tab = QWidget()
        self.tab.setObjectName("tab")
        self.lineEditGraphName2 = QLineEdit(self.tab)
        self.lineEditGraphName2.setGeometry(QRect(90, 50, 253, 20))
        self.lineEditGraphName2.setObjectName("lineEditGraphName2")
        self.labelGraphState = QLabel(self.tab)
        self.labelGraphState.setGeometry(QRect(10, 84, 46, 13))
        self.labelGraphState.setObjectName("labelGraphState")
        self.pushButtonAdd2 = QPushButton(self.tab)
        self.pushButtonAdd2.setGeometry(QRect(9, 120, 75, 23))
        self.pushButtonAdd2.setObjectName("pushButtonAdd2")
        self.labelGraphName2 = QLabel(self.tab)
        self.labelGraphName2.setGeometry(QRect(10, 53, 46, 13))
        self.labelGraphName2.setObjectName("labelGraphName2")
        self.label_2 = QLabel(self.tab)
        self.label_2.setGeometry(QRect(7, 16, 141, 16))
        self.label_2.setObjectName("label_2")
        self.comboBoxState = QComboBox(self.tab)
        self.comboBoxState.setGeometry(QRect(90, 83, 69, 22))
        self.comboBoxState.setObjectName("comboBoxState")
        self.comboBoxState.addItem("")
        self.comboBoxState.addItem("")
        self.comboBoxState.addItem("")
        self.comboBoxState.addItem("")
        self.gridLayoutWidget = QWidget(self.tab)
        self.gridLayoutWidget.setGeometry(QRect(10, 200, 331, 101))
        self.gridLayoutWidget.setObjectName("gridLayoutWidget")
        self.gridLayout = QGridLayout(self.gridLayoutWidget)
        self.gridLayout.setMargin(0)
        self.gridLayout.setObjectName("gridLayout")
        self.labelCriticalLevel = QLabel(self.gridLayoutWidget)
        self.labelCriticalLevel.setObjectName("labelCriticalLevel")
        self.gridLayout.addWidget(self.labelCriticalLevel, 2, 2, 1, 1)
        self.labelGraphName = QLabel(self.gridLayoutWidget)
        self.labelGraphName.setObjectName("labelGraphName")
        self.gridLayout.addWidget(self.labelGraphName, 0, 0, 1, 1)
        self.spinBoxCriticalLevel = QSpinBox(self.gridLayoutWidget)
        self.spinBoxCriticalLevel.setObjectName("spinBoxCriticalLevel")
        self.gridLayout.addWidget(self.spinBoxCriticalLevel, 2, 3, 1, 1)
        self.spinBoxWarnLevel = QSpinBox(self.gridLayoutWidget)
        self.spinBoxWarnLevel.setObjectName("spinBoxWarnLevel")
        self.gridLayout.addWidget(self.spinBoxWarnLevel, 2, 1, 1, 1)
        self.labelWarnLevel = QLabel(self.gridLayoutWidget)
        self.labelWarnLevel.setObjectName("labelWarnLevel")
        self.gridLayout.addWidget(self.labelWarnLevel, 2, 0, 1, 1)
        self.labelGraphValue = QLabel(self.gridLayoutWidget)
        self.labelGraphValue.setObjectName("labelGraphValue")
        self.gridLayout.addWidget(self.labelGraphValue, 1, 0, 1, 1)
        self.lineEditGraphName = QLineEdit(self.gridLayoutWidget)
        self.lineEditGraphName.setObjectName("lineEditGraphName")
        self.gridLayout.addWidget(self.lineEditGraphName, 0, 1, 1, 3)
        self.lineEditGraphValue = QLineEdit(self.gridLayoutWidget)
        self.lineEditGraphValue.setObjectName("lineEditGraphValue")
        self.gridLayout.addWidget(self.lineEditGraphValue, 1, 1, 1, 2)
        self.label = QLabel(self.tab)
        self.label.setGeometry(QRect(11, 170, 141, 16))
        self.label.setObjectName("label")
        self.pushButtonAdd1 = QPushButton(self.tab)
        self.pushButtonAdd1.setGeometry(QRect(9, 314, 75, 23))
        self.pushButtonAdd1.setObjectName("pushButtonAdd1")
        self.tabWidget.addTab(self.tab, "")
        self.tab_2 = QWidget()
        self.tab_2.setObjectName("tab_2")
        self.gridLayoutWidget_2 = QWidget(self.tab_2)
        self.gridLayoutWidget_2.setGeometry(QRect(9, 50, 331, 74))
        self.gridLayoutWidget_2.setObjectName("gridLayoutWidget_2")
        self.gridLayout_2 = QGridLayout(self.gridLayoutWidget_2)
        self.gridLayout_2.setMargin(0)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.labelGraphOutputMessage = QLabel(self.gridLayoutWidget_2)
        self.labelGraphOutputMessage.setObjectName("labelGraphOutputMessage")
        self.gridLayout_2.addWidget(self.labelGraphOutputMessage, 0, 0, 1, 1)
        self.pushButtonGraphOutputMessage = QPushButton(self.gridLayoutWidget_2)
        self.pushButtonGraphOutputMessage.setObjectName("pushButtonGraphOutputMessage")
        self.gridLayout_2.addWidget(self.pushButtonGraphOutputMessage, 1, 0, 1, 1)
        self.lineEditGraphOutputMessage = QLineEdit(self.gridLayoutWidget_2)
        self.lineEditGraphOutputMessage.setObjectName("lineEditGraphOutputMessage")
        self.gridLayout_2.addWidget(self.lineEditGraphOutputMessage, 0, 1, 1, 1)
        self.label_3 = QLabel(self.tab_2)
        self.label_3.setGeometry(QRect(10, 20, 211, 16))
        self.label_3.setObjectName("label_3")
        self.tabWidget.addTab(self.tab_2, "")
        self.pushButtonCancel = QPushButton(self)
        self.pushButtonCancel.setGeometry(QRect(16, 397, 75, 23))
        self.pushButtonCancel.setObjectName("pushButtonCancel")

        self.tabWidget.setCurrentIndex(0)

        self.labelGraphState.setText("State")
        self.comboBoxState.setItemText(0, "3")
        self.comboBoxState.setItemText(1, "2")
        self.comboBoxState.setItemText(2, "1")
        self.comboBoxState.setItemText(3, "0")
        self.pushButtonAdd2.setText("Add")
        self.labelGraphName2.setText("Name")
        self.label_2.setText("Init New Performance Data:")
        self.labelCriticalLevel.setText("Critical")
        self.labelGraphName.setText("Name")
        self.labelWarnLevel.setText("Warning")
        self.labelGraphValue.setText("Value")
        self.label.setText("Add New Performance Data:")
        self.pushButtonAdd1.setText("Add")
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), "Performance Data")
        self.labelGraphOutputMessage.setText("Message")
        self.pushButtonGraphOutputMessage.setText("Add")
        self.label_3.setText("Print message:")
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), "Output Utilities")
        self.pushButtonCancel.setText("Cancel")

        self.setWindowFlags(Qt.WindowCloseButtonHint | Qt.WindowStaysOnTopHint)
        self.setFixedSize(self.size())

        self.connect(self.pushButtonAdd2, SIGNAL("clicked()"), self.AddEmptyPerfData)
        self.connect(self.pushButtonAdd1, SIGNAL("clicked()"), self.AddPerfData)
        self.connect(self.pushButtonGraphOutputMessage, SIGNAL("clicked()"), self.AddMessage)
        self.connect(self.pushButtonCancel, SIGNAL("clicked()"), self.CancelEvent)

    def AddEmptyPerfData(self):
        SERVICE_NAME = "editor"
        editor_service = self.plugin.locator.get_service(SERVICE_NAME)

        curLineText = editor_service.get_current_line_text()

        if editor_service.use_tab() is False:
            leadingSpaceNumber = len(curLineText) - len(curLineText.lstrip(' '))
            tabChar = ' ' * editor_service.get_indentation()
        else:
            leadingSpaceNumber = len(curLineText) - len(curLineText.lstrip('\t'))
            tabChar = '\t'

        leadingChar = ""

        if editor_service.use_tab() is False:
            for x in range(leadingSpaceNumber):
                leadingChar = leadingChar + " "
        else:
            for x in range(leadingSpaceNumber):
                leadingChar = leadingChar + "\t"

        state = self.comboBoxState.currentText()

        if self.lineEditGraphName2.text() != "":

            editor_service.insert_text("NagiosUtils.AddPerformanceData(\"" + self.lineEditGraphName2.text() + "\", \"\", \"\", \"\", " + state + ")")
            editor_service.insert_text(os.linesep)
            editor_service.insert_text(leadingChar)

    def AddPerfData(self):
        SERVICE_NAME = "editor"
        editor_service = self.plugin.locator.get_service(SERVICE_NAME)

        curLineText = editor_service.get_current_line_text()

        if editor_service.use_tab() is False:
            leadingSpaceNumber = len(curLineText) - len(curLineText.lstrip(' '))
            tabChar = ' ' * editor_service.get_indentation()
        else:
            leadingSpaceNumber = len(curLineText) - len(curLineText.lstrip('\t'))
            tabChar = '\t'

        leadingChar = ""

        if editor_service.use_tab() is False:
            for x in range(leadingSpaceNumber):
                leadingChar = leadingChar + " "
        else:
            for x in range(leadingSpaceNumber):
                leadingChar = leadingChar + "\t"

        if self.lineEditGraphName.text() != "" and self.lineEditGraphValue.text() != "":

            if self.spinBoxWarnLevel.value() == 0:
                warnLevel = "\"\""
            else:
                warnLevel = str(self.spinBoxWarnLevel.value())

            if self.spinBoxCriticalLevel.value() == 0:
                critLevel = "\"\""
            else:
                critLevel = str(self.spinBoxCriticalLevel.value())

            editor_service.insert_text("NagiosUtils.AddPerformanceData(\"" + self.lineEditGraphName.text() + "\", " + self.lineEditGraphValue.text() + ", " + warnLevel + ", " + critLevel + ")")
            editor_service.insert_text(os.linesep)
            editor_service.insert_text(leadingChar)

    def AddMessage(self):
        SERVICE_NAME = "editor"
        editor_service = self.plugin.locator.get_service(SERVICE_NAME)

        curLineText = editor_service.get_current_line_text()

        if editor_service.use_tab() is False:
            leadingSpaceNumber = len(curLineText) - len(curLineText.lstrip(' '))
            tabChar = ' ' * editor_service.get_indentation()
        else:
            leadingSpaceNumber = len(curLineText) - len(curLineText.lstrip('\t'))
            tabChar = '\t'

        leadingChar = ""

        if editor_service.use_tab() is False:
            for x in range(leadingSpaceNumber):
                leadingChar = leadingChar + " "
        else:
            for x in range(leadingSpaceNumber):
                leadingChar = leadingChar + "\t"

        if self.lineEditGraphOutputMessage.text() != "":
            editor_service.insert_text("NagiosUtils.PrintOutput(\"" + self.lineEditGraphOutputMessage.text() + "\")")
            editor_service.insert_text(os.linesep)
            editor_service.insert_text(leadingChar)

    def keyPressEvent(self, event):

        if event.key() == Qt.Key_Escape:
            self.close()

    def CancelEvent(self):
        self.close()