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


class ProcessUtils(QWidget):

    def __init__(self, plugin):
        super(ProcessUtils, self).__init__()

        self.plugin = plugin
        self.plug_path = plugin.plug_path

        self.initUI()

    def initUI(self):
        icon = QIcon()
        icon.addPixmap(QPixmap(self.plug_path + "/alexatools/images/gksu-root-terminal.png"), QIcon.Normal, QIcon.Off)
        self.setWindowIcon(icon)
        self.setWindowTitle("Al\'exa - Process Utilities")
        self.setObjectName("self")
        self.resize(377, 270)
        self.pushButtonCancel = QPushButton(self)
        self.pushButtonCancel.setGeometry(QRect(10, 240, 75, 23))
        self.pushButtonCancel.setObjectName("pushButtonCancel")
        self.tabWidget = QTabWidget(self)
        self.tabWidget.setGeometry(QRect(10, 10, 357, 221))
        self.tabWidget.setObjectName("tabWidget")
        self.tab = QWidget()
        self.tab.setObjectName("tab")
        self.gridLayoutWidget_2 = QWidget(self.tab)
        self.gridLayoutWidget_2.setGeometry(QRect(10, 10, 331, 111))
        self.gridLayoutWidget_2.setObjectName("gridLayoutWidget_2")
        self.gridLayout_2 = QGridLayout(self.gridLayoutWidget_2)
        self.gridLayout_2.setMargin(0)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.labelExecutable = QLabel(self.gridLayoutWidget_2)
        self.labelExecutable.setObjectName("labelExecutable")
        self.gridLayout_2.addWidget(self.labelExecutable, 0, 0, 1, 1)
        self.labelArguments = QLabel(self.gridLayoutWidget_2)
        self.labelArguments.setObjectName("labelArguments")
        self.gridLayout_2.addWidget(self.labelArguments, 1, 0, 1, 1)
        self.lineEditExecutable = QLineEdit(self.gridLayoutWidget_2)
        self.lineEditExecutable.setObjectName("lineEditExecutable")
        self.gridLayout_2.addWidget(self.lineEditExecutable, 0, 1, 1, 1)
        self.lineEditArguments = QLineEdit(self.gridLayoutWidget_2)
        self.lineEditArguments.setObjectName("lineEditArguments")
        self.gridLayout_2.addWidget(self.lineEditArguments, 1, 1, 1, 1)
        self.pushButtonAddExe = QPushButton(self.gridLayoutWidget_2)
        self.pushButtonAddExe.setObjectName("pushButtonAddExe")
        self.gridLayout_2.addWidget(self.pushButtonAddExe, 2, 0, 1, 1)
        self.tabWidget.addTab(self.tab, "")
        self.tab_2 = QWidget()
        self.tab_2.setObjectName("tab_2")
        self.gridLayoutWidget = QWidget(self.tab_2)
        self.gridLayoutWidget.setGeometry(QRect(10, 10, 331, 171))
        self.gridLayoutWidget.setObjectName("gridLayoutWidget")
        self.gridLayout = QGridLayout(self.gridLayoutWidget)
        self.gridLayout.setMargin(0)
        self.gridLayout.setObjectName("gridLayout")
        self.labelNamePerf = QLabel(self.gridLayoutWidget)
        self.labelNamePerf.setObjectName("labelNamePerf")
        self.gridLayout.addWidget(self.labelNamePerf, 2, 0, 1, 1)
        self.labelProcName = QLabel(self.gridLayoutWidget)
        self.labelProcName.setObjectName("labelProcName")
        self.gridLayout.addWidget(self.labelProcName, 0, 0, 1, 1)
        self.labelCriticalPerf = QLabel(self.gridLayoutWidget)
        self.labelCriticalPerf.setObjectName("labelCriticalPerf")
        self.gridLayout.addWidget(self.labelCriticalPerf, 3, 2, 1, 1)
        self.spinBoxWarningPerf = QSpinBox(self.gridLayoutWidget)
        self.spinBoxWarningPerf.setObjectName("spinBoxWarningPerf")
        self.gridLayout.addWidget(self.spinBoxWarningPerf, 3, 1, 1, 1)
        self.lineEditProcName = QLineEdit(self.gridLayoutWidget)
        self.lineEditProcName.setObjectName("lineEditProcName")
        self.gridLayout.addWidget(self.lineEditProcName, 0, 1, 1, 3)
        self.labelWarningPerf = QLabel(self.gridLayoutWidget)
        self.labelWarningPerf.setObjectName("labelWarningPerf")
        self.gridLayout.addWidget(self.labelWarningPerf, 3, 0, 1, 1)
        self.lineEditNamePerf = QLineEdit(self.gridLayoutWidget)
        self.lineEditNamePerf.setObjectName("lineEditNamePerf")
        self.gridLayout.addWidget(self.lineEditNamePerf, 2, 1, 1, 2)
        self.spinBoxCriticalPerf = QSpinBox(self.gridLayoutWidget)
        self.spinBoxCriticalPerf.setObjectName("spinBoxCriticalPerf")
        self.gridLayout.addWidget(self.spinBoxCriticalPerf, 3, 3, 1, 1)
        self.checkBoxEnablePerf = QCheckBox(self.gridLayoutWidget)
        self.checkBoxEnablePerf.setObjectName("checkBoxEnablePerf")
        self.gridLayout.addWidget(self.checkBoxEnablePerf, 1, 0, 1, 2)
        self.pushButtonWaitForExit = QPushButton(self.gridLayoutWidget)
        self.pushButtonWaitForExit.setObjectName("pushButtonWaitForExit")
        self.gridLayout.addWidget(self.pushButtonWaitForExit, 4, 1, 1, 1)
        self.pushButtonKill = QPushButton(self.gridLayoutWidget)
        self.pushButtonKill.setObjectName("pushButtonKill")
        self.gridLayout.addWidget(self.pushButtonKill, 4, 0, 1, 1)
        self.tabWidget.addTab(self.tab_2, "")

        self.tabWidget.setCurrentIndex(0)

        self.pushButtonCancel.setText("Cancel")
        self.labelExecutable.setText("Executable")
        self.labelArguments.setText("Arguments")
        self.pushButtonAddExe.setText("Add")
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), "Run")
        self.labelNamePerf.setText("Name")
        self.labelProcName.setText("Process Name")
        self.labelCriticalPerf.setText("Critical")
        self.labelWarningPerf.setText("Warning")
        self.checkBoxEnablePerf.setText("Enable Perfomance Data")
        self.pushButtonWaitForExit.setText("Wait For Exit")
        self.pushButtonKill.setText("Kill")
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), "Extra Actions")

        self.setWindowFlags(Qt.WindowCloseButtonHint | Qt.WindowStaysOnTopHint)
        self.setFixedSize(self.size())

        self.connect(self.pushButtonCancel, SIGNAL("clicked()"), self.CancelEvent)
        self.connect(self.checkBoxEnablePerf, SIGNAL("clicked()"), self.UpdatePerfData)
        self.connect(self.pushButtonAddExe, SIGNAL("clicked()"), self.InsertExecuteCommand)
        self.connect(self.pushButtonKill, SIGNAL("clicked()"), self.InsertKillCommand)
        self.connect(self.pushButtonWaitForExit, SIGNAL("clicked()"), self.InsertWaitForExit)

        self.UpdatePerfData()

    def UpdatePerfData(self):
        if self.checkBoxEnablePerf.isChecked() is True:
            self.labelNamePerf.setEnabled(True)
            self.lineEditNamePerf.setEnabled(True)
            self.labelWarningPerf.setEnabled(True)
            self.spinBoxWarningPerf.setEnabled(True)
            self.labelCriticalPerf.setEnabled(True)
            self.spinBoxCriticalPerf.setEnabled(True)
        else:
            self.labelNamePerf.setEnabled(False)
            self.lineEditNamePerf.setEnabled(False)
            self.labelWarningPerf.setEnabled(False)
            self.spinBoxWarningPerf.setEnabled(False)
            self.labelCriticalPerf.setEnabled(False)
            self.spinBoxCriticalPerf.setEnabled(False)

    def InsertExecuteCommand(self):

        if self.lineEditExecutable.text() == "":
            self.message = QMessageBox.critical(self, 'Error', "You have to insert the executable full name!", QMessageBox.Ok)
            return

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

        executable = self.lineEditExecutable.text()
        executable = executable.replace('\\','\\\\')

        if self.lineEditArguments.text() == "":
            editor_service.insert_text("subprocess.Popen([\"" + executable + "\"])")
        else:
            arguments = self.lineEditArguments.text()
            arguments = arguments.replace("\\","\\\\")
            editor_service.insert_text("subprocess.Popen([\"" + executable + "\", " + arguments + "])")
        editor_service.insert_text(os.linesep)
        editor_service.insert_text(leadingChar)

    def InsertKillCommand(self):

        if self.lineEditProcName.text() == "":
            self.message = QMessageBox.critical(self, 'Error', "You have to insert the process name!", QMessageBox.Ok)
            return

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

        editor_service.insert_text("Process.Kill(\"" + self.lineEditProcName.text() + "\")")

        editor_service.insert_text(os.linesep)
        editor_service.insert_text(leadingChar)

    def InsertWaitForExit(self):

        if self.lineEditProcName.text() == "":
            self.message = QMessageBox.critical(self, 'Error', "You have to insert the process name!", QMessageBox.Ok)
            return

        if self.checkBoxEnablePerf.isChecked() is True and self.lineEditNamePerf.text() == "":
            self.message = QMessageBox.critical(self, 'Error', "You have to insert a valid Performance Data Name", QMessageBox.Ok)
            return

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

        if self.checkBoxEnablePerf.isChecked() is True:
            timeOut = self.spinBoxCriticalPerf.value() + 15
        else:
            timeOut = 15

        editor_service.insert_text("performance = Process.WaitForExit(\"" + self.lineEditProcName.text() + "\", timeout=" + str(timeOut) + ")")

        if self.checkBoxEnablePerf.isChecked() is True:
            editor_service.insert_text(os.linesep)
            editor_service.insert_text(leadingChar + "NagiosUtils.AddPerformanceData(\"" + self.lineEditNamePerf.text() + "\", performance, " + str(self.spinBoxWarningPerf.value()) + ", " + str(self.spinBoxCriticalPerf.value()) + ")")

        editor_service.insert_text(os.linesep)
        editor_service.insert_text(leadingChar)

    def keyPressEvent(self, event):

        if event.key() == Qt.Key_Escape:
            self.close()

    def CancelEvent(self):
        self.close()