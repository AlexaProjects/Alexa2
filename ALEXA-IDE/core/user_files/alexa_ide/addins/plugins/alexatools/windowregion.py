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
import sys
import time

#QT Toolkit
from PyQt4.QtGui import *
from PyQt4.QtCore import *

from windowcropregion import CropRegionClass

from Alexa import *

import wx

if sys.platform == 'win32':
    import win32gui

class WindowRegion(QWidget):

    def __init__(self, plugin):
        super(WindowRegion, self).__init__()

        self.plugin = plugin
        self.plug_path = plugin.plug_path
        self.FirstTimeCheckBox = True
        self.hwndInComboBox = []

        self.CropRegionX = 0
        self.CropRegionY = 0
        self.CropRegionW = 0
        self.CropRegionH = 0

        self.windowX = 0
        self.windowY = 0

        self.initUI()

    def initUI(self):
        icon = QIcon()
        icon.addPixmap(QPixmap(self.plug_path + "/alexatools/images/preferences-desktop-theme.png"), QIcon.Normal, QIcon.Off)
        self.setWindowIcon(icon)
        self.setWindowTitle("Al\'exa - Windows and Region")
        self.setObjectName("self")
        self.resize(639, 412)
        self.tabWidget = QTabWidget(self)
        self.tabWidget.setGeometry(QRect(10, 10, 621, 361))
        self.tabWidget.setObjectName("tabWidget")
        self.tab = QWidget()
        self.tab.setObjectName("tab")
        self.pushButton = QPushButton(self.tab)
        self.pushButton.setGeometry(QRect(568, 10, 24, 20))
        self.pushButton.setText("")
        icon = QIcon()
        icon.addPixmap(QPixmap(self.plug_path + "/alexatools/images/arrow-down-4.png"), QIcon.Normal, QIcon.Off)
        self.pushButton.setIcon(icon)
        self.pushButton.setObjectName("pushButton")
        self.formLayoutWidget_2 = QWidget(self.tab)
        self.formLayoutWidget_2.setGeometry(QRect(10, 40, 521, 22))
        self.formLayoutWidget_2.setObjectName("formLayoutWidget_2")
        self.formLayout_2 = QFormLayout(self.formLayoutWidget_2)
        self.formLayout_2.setMargin(0)
        self.formLayout_2.setObjectName("formLayout_2")
        self.lineEditWindowRegEx = QLineEdit(self.formLayoutWidget_2)
        self.lineEditWindowRegEx.setObjectName("lineEditWindowRegEx")
        self.formLayout_2.setWidget(0, QFormLayout.FieldRole, self.lineEditWindowRegEx)
        self.label_2 = QLabel(self.formLayoutWidget_2)
        self.label_2.setObjectName("label_2")
        self.formLayout_2.setWidget(0, QFormLayout.LabelRole, self.label_2)
        self.gridLayoutWidget = QWidget(self.tab)
        self.gridLayoutWidget.setGeometry(QRect(10, 200, 351, 81))
        self.gridLayoutWidget.setObjectName("gridLayoutWidget")
        self.gridLayout = QGridLayout(self.gridLayoutWidget)
        self.gridLayout.setMargin(0)
        self.gridLayout.setObjectName("gridLayout")
        self.spinBoxWindowMoveHeight = QSpinBox(self.gridLayoutWidget)
        self.spinBoxWindowMoveHeight.setMinimum(-9999)
        self.spinBoxWindowMoveHeight.setMaximum(9999)
        self.spinBoxWindowMoveHeight.setObjectName("spinBoxWindowMoveHeight")
        self.gridLayout.addWidget(self.spinBoxWindowMoveHeight, 2, 1, 1, 1)
        self.label_4 = QLabel(self.gridLayoutWidget)
        self.label_4.setObjectName("label_4")
        self.gridLayout.addWidget(self.label_4, 1, 2, 1, 1)
        self.label_6 = QLabel(self.gridLayoutWidget)
        self.label_6.setObjectName("label_6")
        self.gridLayout.addWidget(self.label_6, 2, 2, 1, 1)
        self.spinBoxWindowMoveX = QSpinBox(self.gridLayoutWidget)
        self.spinBoxWindowMoveX.setMinimum(-999999)
        self.spinBoxWindowMoveX.setMaximum(9999)
        self.spinBoxWindowMoveX.setObjectName("spinBoxWindowMoveX")
        self.gridLayout.addWidget(self.spinBoxWindowMoveX, 1, 1, 1, 1)
        self.label_3 = QLabel(self.gridLayoutWidget)
        self.label_3.setObjectName("label_3")
        self.gridLayout.addWidget(self.label_3, 1, 0, 1, 1)
        self.spinBoxWindowMoveWidth = QSpinBox(self.gridLayoutWidget)
        self.spinBoxWindowMoveWidth.setMinimum(-9999)
        self.spinBoxWindowMoveWidth.setMaximum(9999)
        self.spinBoxWindowMoveWidth.setObjectName("spinBoxWindowMoveWidth")
        self.gridLayout.addWidget(self.spinBoxWindowMoveWidth, 2, 3, 1, 1)
        self.label_5 = QLabel(self.gridLayoutWidget)
        self.label_5.setObjectName("label_5")
        self.gridLayout.addWidget(self.label_5, 2, 0, 1, 1)
        self.spinBoxWindowMoveY = QSpinBox(self.gridLayoutWidget)
        self.spinBoxWindowMoveY.setMinimum(-999999)
        self.spinBoxWindowMoveY.setMaximum(9999)
        self.spinBoxWindowMoveY.setObjectName("spinBoxWindowMoveY")
        self.gridLayout.addWidget(self.spinBoxWindowMoveY, 1, 3, 1, 1)
        self.radioButtonWindowResize = QRadioButton(self.gridLayoutWidget)
        self.radioButtonWindowResize.setChecked(True)
        self.radioButtonWindowResize.setObjectName("radioButtonWindowResize")
        self.gridLayout.addWidget(self.radioButtonWindowResize, 0, 0, 1, 1)
        self.radioButtonWindowMove = QRadioButton(self.gridLayoutWidget)
        self.radioButtonWindowMove.setObjectName("radioButtonWindowMove")
        self.gridLayout.addWidget(self.radioButtonWindowMove, 0, 1, 1, 1)
        self.horizontalLayoutWidget = QWidget(self.tab)
        self.horizontalLayoutWidget.setGeometry(QRect(10, 290, 111, 31))
        self.horizontalLayoutWidget.setObjectName("horizontalLayoutWidget")
        self.horizontalLayout_2 = QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontalLayout_2.setMargin(0)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.pushButtonMoveResize = QPushButton(self.horizontalLayoutWidget)
        self.pushButtonMoveResize.setObjectName("pushButtonMoveResize")
        self.horizontalLayout_2.addWidget(self.pushButtonMoveResize)
        self.horizontalLayoutWidget_2 = QWidget(self.tab)
        self.horizontalLayoutWidget_2.setGeometry(QRect(10, 90, 411, 31))
        self.horizontalLayoutWidget_2.setObjectName("horizontalLayoutWidget_2")
        self.horizontalLayout = QHBoxLayout(self.horizontalLayoutWidget_2)
        self.horizontalLayout.setMargin(0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.pushButtonWindowBind = QPushButton(self.horizontalLayoutWidget_2)
        self.pushButtonWindowBind.setObjectName("pushButtonWindowBind")
        self.horizontalLayout.addWidget(self.pushButtonWindowBind)
        self.pushButtonWindowUnbind = QPushButton(self.horizontalLayoutWidget_2)
        self.pushButtonWindowUnbind.setObjectName("pushButtonWindowUnbind")
        self.horizontalLayout.addWidget(self.pushButtonWindowUnbind)
        self.pushButtonWindowWaitForExit = QPushButton(self.horizontalLayoutWidget_2)
        self.pushButtonWindowWaitForExit.setObjectName("pushButtonWindowWaitForExit")
        self.horizontalLayout.addWidget(self.pushButtonWindowWaitForExit)
        self.pushButtonWindowClose = QPushButton(self.horizontalLayoutWidget_2)
        self.pushButtonWindowClose.setObjectName("pushButtonWindowClose")
        self.horizontalLayout.addWidget(self.pushButtonWindowClose)
        self.label = QLabel(self.tab)
        self.label.setGeometry(QRect(10, 10, 77, 20))
        self.label.setObjectName("label")
        self.verticalLayoutWidget = QWidget(self.tab)
        self.verticalLayoutWidget.setGeometry(QRect(90, 10, 441, 22))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayout = QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setMargin(0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.comboBoxVisibleWindows = QComboBox(self.verticalLayoutWidget)
        self.comboBoxVisibleWindows.setObjectName("comboBoxVisibleWindows")
        self.verticalLayout.addWidget(self.comboBoxVisibleWindows)
        self.pushButton_2 = QPushButton(self.tab)
        self.pushButton_2.setGeometry(QRect(538, 10, 24, 20))
        self.pushButton_2.setText("")
        icon1 = QIcon()
        icon1.addPixmap(QPixmap(self.plug_path + "/alexatools/images/view-refresh-3.png"), QIcon.Normal, QIcon.Off)
        self.pushButton_2.setIcon(icon1)
        self.pushButton_2.setObjectName("pushButton_2")
        self.pushButtonTestBind = QPushButton(self.tab)
        self.pushButtonTestBind.setGeometry(QRect(539, 40, 53, 23))
        self.pushButtonTestBind.setObjectName("pushButtonTestBind")
        self.checkBoxMaximizeWindow = QCheckBox(self.tab)
        self.checkBoxMaximizeWindow.setGeometry(QRect(11, 65, 91, 17))
        self.checkBoxMaximizeWindow.setObjectName("checkBoxMaximizeWindow")
        self.pushButtonAddSize = QPushButton(self.tab)
        self.pushButtonAddSize.setGeometry(QRect(387, 227, 24, 22))
        self.pushButtonAddSize.setText("")
        icon2 = QIcon()
        icon2.addPixmap(QPixmap(self.plug_path + "/alexatools/images/view-restore.png"), QIcon.Normal, QIcon.Off)
        self.pushButtonAddSize.setIcon(icon2)
        self.pushButtonAddSize.setObjectName("pushButtonAddSize")
        self.gridLayoutWidget_3 = QWidget(self.tab)
        self.gridLayoutWidget_3.setGeometry(QRect(10, 130, 481, 61))
        self.gridLayoutWidget_3.setObjectName("gridLayoutWidget_3")
        self.gridLayout_3 = QGridLayout(self.gridLayoutWidget_3)
        self.gridLayout_3.setMargin(0)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.label_11 = QLabel(self.gridLayoutWidget_3)
        self.label_11.setObjectName("label_11")
        self.gridLayout_3.addWidget(self.label_11, 1, 2, 1, 1)
        self.spinBoxPerfWarning = QSpinBox(self.gridLayoutWidget_3)
        self.spinBoxPerfWarning.setMaximum(9999)
        self.spinBoxPerfWarning.setObjectName("spinBoxPerfWarning")
        self.gridLayout_3.addWidget(self.spinBoxPerfWarning, 1, 3, 1, 1)
        self.label_12 = QLabel(self.gridLayoutWidget_3)
        self.label_12.setObjectName("label_12")
        self.gridLayout_3.addWidget(self.label_12, 1, 4, 1, 1)
        self.spinBoxPerfCritical = QSpinBox(self.gridLayoutWidget_3)
        self.spinBoxPerfCritical.setMaximum(9999)
        self.spinBoxPerfCritical.setObjectName("spinBoxPerfCritical")
        self.gridLayout_3.addWidget(self.spinBoxPerfCritical, 1, 5, 1, 1)
        self.label_13 = QLabel(self.gridLayoutWidget_3)
        self.label_13.setObjectName("label_13")
        self.gridLayout_3.addWidget(self.label_13, 1, 0, 1, 1)
        self.lineEdit = QLineEdit(self.gridLayoutWidget_3)
        self.lineEdit.setObjectName("lineEdit")
        self.gridLayout_3.addWidget(self.lineEdit, 1, 1, 1, 1)
        self.checkBoxEnablePerfData = QCheckBox(self.gridLayoutWidget_3)
        self.checkBoxEnablePerfData.setObjectName("checkBoxEnablePerfData")
        self.gridLayout_3.addWidget(self.checkBoxEnablePerfData, 0, 0, 1, 2)
        self.tabWidget.addTab(self.tab, "")
        self.tab_2 = QWidget()
        self.tab_2.setObjectName("tab_2")
        self.gridLayoutWidget_2 = QWidget(self.tab_2)
        self.gridLayoutWidget_2.setGeometry(QRect(10, 50, 351, 61))
        self.gridLayoutWidget_2.setObjectName("gridLayoutWidget_2")
        self.gridLayout_2 = QGridLayout(self.gridLayoutWidget_2)
        self.gridLayout_2.setMargin(0)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.label_7 = QLabel(self.gridLayoutWidget_2)
        self.label_7.setObjectName("label_7")
        self.gridLayout_2.addWidget(self.label_7, 0, 0, 1, 1)
        self.label_10 = QLabel(self.gridLayoutWidget_2)
        self.label_10.setObjectName("label_10")
        self.gridLayout_2.addWidget(self.label_10, 1, 2, 1, 1)
        self.spinBoxRegionHeight = QSpinBox(self.gridLayoutWidget_2)
        self.spinBoxRegionHeight.setMaximum(9999)
        self.spinBoxRegionHeight.setObjectName("spinBoxRegionHeight")
        self.gridLayout_2.addWidget(self.spinBoxRegionHeight, 1, 1, 1, 1)
        self.spinBoxRegionX_2 = QSpinBox(self.gridLayoutWidget_2)
        self.spinBoxRegionX_2.setMinimum(-999999)
        self.spinBoxRegionX_2.setMaximum(9999)
        self.spinBoxRegionX_2.setObjectName("spinBoxRegionX_2")
        self.gridLayout_2.addWidget(self.spinBoxRegionX_2, 0, 3, 1, 1)
        self.label_9 = QLabel(self.gridLayoutWidget_2)
        self.label_9.setObjectName("label_9")
        self.gridLayout_2.addWidget(self.label_9, 1, 0, 1, 1)
        self.label_8 = QLabel(self.gridLayoutWidget_2)
        self.label_8.setObjectName("label_8")
        self.gridLayout_2.addWidget(self.label_8, 0, 2, 1, 1)
        self.spinBoxRegionX = QSpinBox(self.gridLayoutWidget_2)
        self.spinBoxRegionX.setMinimum(-999999)
        self.spinBoxRegionX.setMaximum(9999)
        self.spinBoxRegionX.setObjectName("spinBoxRegionX")
        self.gridLayout_2.addWidget(self.spinBoxRegionX, 0, 1, 1, 1)
        self.spinBoxRegionWidth = QSpinBox(self.gridLayoutWidget_2)
        self.spinBoxRegionWidth.setMaximum(9999)
        self.spinBoxRegionWidth.setObjectName("spinBoxRegionWidth")
        self.gridLayout_2.addWidget(self.spinBoxRegionWidth, 1, 3, 1, 1)
        self.horizontalLayoutWidget_3 = QWidget(self.tab_2)
        self.horizontalLayoutWidget_3.setGeometry(QRect(10, 130, 291, 41))
        self.horizontalLayoutWidget_3.setObjectName("horizontalLayoutWidget_3")
        self.horizontalLayout_3 = QHBoxLayout(self.horizontalLayoutWidget_3)
        self.horizontalLayout_3.setMargin(0)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.pushButtonCropRegion = QPushButton(self.horizontalLayoutWidget_3)
        self.pushButtonCropRegion.setObjectName("pushButtonCropRegion")
        self.horizontalLayout_3.addWidget(self.pushButtonCropRegion)
        self.pushButtonBindRegion = QPushButton(self.horizontalLayoutWidget_3)
        self.pushButtonBindRegion.setObjectName("pushButtonBindRegion")
        self.horizontalLayout_3.addWidget(self.pushButtonBindRegion)
        self.pushButtonUnbindRegion = QPushButton(self.horizontalLayoutWidget_3)
        self.pushButtonUnbindRegion.setObjectName("pushButtonUnbindRegion")
        self.horizontalLayout_3.addWidget(self.pushButtonUnbindRegion)
        self.checkBoxRegionOrigin = QCheckBox(self.tab_2)
        self.checkBoxRegionOrigin.setGeometry(QRect(10, 20, 161, 17))
        self.checkBoxRegionOrigin.setChecked(True)
        self.checkBoxRegionOrigin.setObjectName("checkBoxRegionOrigin")
        self.tabWidget.addTab(self.tab_2, "")
        self.pushButtonCancel = QPushButton(self)
        self.pushButtonCancel.setGeometry(QRect(20, 380, 75, 23))
        self.pushButtonCancel.setObjectName("pushButtonCancel")

        #self.retranslateUi(self)
        self.tabWidget.setCurrentIndex(0)
        #QMetaObject.connectSlotsByName(self)

        self.label_2.setText("Window Reg Ex")
        self.label_4.setText("y")
        self.label_6.setText("Width")
        self.label_3.setText("x")
        self.label_5.setText("Height")
        self.radioButtonWindowResize.setText("Resize")
        self.radioButtonWindowMove.setText("Move")
        self.pushButtonMoveResize.setText("Move or Resize")
        self.pushButtonWindowBind.setText("Bind")
        self.pushButtonWindowUnbind.setText("Unbind")
        self.pushButtonWindowWaitForExit.setText("Wait For Exit")
        self.pushButtonWindowClose.setText("Close")
        self.label.setText("Visible Windows")
        self.pushButtonTestBind.setText("Test")
        self.checkBoxMaximizeWindow.setText("Maximize")
        self.label_11.setText("Warning")
        self.label_12.setText("Critical")
        self.label_13.setText("Name")
        self.checkBoxEnablePerfData.setText("Enable Performance Data")
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), "Windows")
        self.label_7.setText("Offset x")
        self.label_10.setText("Width")
        self.label_9.setText("Height")
        self.label_8.setText("Offset y")
        self.pushButtonCropRegion.setText("Crop")
        self.pushButtonBindRegion.setText("Bind")
        self.pushButtonUnbindRegion.setText("Unbind")
        self.checkBoxRegionOrigin.setText("Origin point is the window...")
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), "Region")
        self.pushButtonCancel.setText("Cancel")

        self.setWindowFlags(Qt.WindowMinimizeButtonHint | Qt.WindowCloseButtonHint | Qt.WindowStaysOnTopHint)
        self.setFixedSize(self.size())

        self.connect(self.pushButtonCancel, SIGNAL("clicked()"), self.CancelEvent)
        self.connect(self.pushButton_2, SIGNAL("clicked()"), self.UpdateWinComboBox)
        self.connect(self.pushButton, SIGNAL("clicked()"), self.UpdateWinLineEdit)
        #self.connect(self.comboBoxVisibleWindows, SIGNAL("activated(int)"), self.WindowTitleSelectEvent)
        self.connect(self.pushButtonTestBind, SIGNAL("clicked()"), self.TestEvent)
        self.connect(self.pushButtonWindowBind, SIGNAL("clicked()"), self.BindWindow)
        self.connect(self.pushButtonWindowClose, SIGNAL("clicked()"), self.CloseWindow)
        self.connect(self.pushButtonWindowWaitForExit, SIGNAL("clicked()"), self.WaitForExit)
        self.connect(self.pushButtonWindowUnbind, SIGNAL("clicked()"), self.UnbindWindow)

        self.connect(self.checkBoxEnablePerfData, SIGNAL("clicked()"), self.UpdateNagiosSpinBoxes)

        self.connect(self.pushButtonAddSize, SIGNAL("clicked()"), self.ImportSizeEvent)
        self.connect(self.radioButtonWindowMove, SIGNAL("clicked()"), self.EnableMoveSpinBox)
        self.connect(self.radioButtonWindowResize, SIGNAL("clicked()"), self.EnableMoveSpinBox)
        self.connect(self.pushButtonMoveResize, SIGNAL("clicked()"), self.MoveOrResize)

        self.connect(self.pushButtonCropRegion, SIGNAL("clicked()"), self.CropRegion)
        self.connect(self.pushButtonBindRegion, SIGNAL("clicked()"), self.AddBindRegion)
        self.connect(self.pushButtonUnbindRegion, SIGNAL("clicked()"), self.AddUnbindRegion)

        self.UpdateWinComboBox()

        self.UpdateCropSpinBoxes()

        self.UpdateNagiosSpinBoxes()

    def UpdateNagiosSpinBoxes(self):
        if self.checkBoxEnablePerfData.isChecked() is False:
            self.label_13.setEnabled(False)
            self.label_11.setEnabled(False)
            self.label_12.setEnabled(False)
            self.lineEdit.setEnabled(False)
            self.spinBoxPerfCritical.setEnabled(False)
            self.spinBoxPerfWarning.setEnabled(False)
        else:
            self.label_13.setEnabled(True)
            self.label_11.setEnabled(True)
            self.label_12.setEnabled(True)
            self.lineEdit.setEnabled(True)
            self.spinBoxPerfCritical.setEnabled(True)
            self.spinBoxPerfWarning.setEnabled(True)

    def UpdateCropSpinBoxes(self):

        self.spinBoxRegionX.setValue(self.CropRegionX)
        self.spinBoxRegionX_2.setValue(self.CropRegionY)
        self.spinBoxRegionHeight.setValue(self.CropRegionH)
        self.spinBoxRegionWidth.setValue(self.CropRegionW)
        '''
        if self.checkBoxRegionOrigin.isChecked() is True:

            self.spinBoxRegionX.setValue(self.CropRegionX - self.windowX)
            self.spinBoxRegionX_2.setValue(self.CropRegionY - self.windowY)
            self.spinBoxRegionHeight.setValue(self.CropRegionH)
            self.spinBoxRegionWidth.setValue(self.CropRegionW)
        else:
            self.spinBoxRegionX.setValue(self.CropRegionX)
            self.spinBoxRegionX_2.setValue(self.CropRegionY)
            self.spinBoxRegionHeight.setValue(self.CropRegionH)
            self.spinBoxRegionWidth.setValue(self.CropRegionW)
        '''
    def WindowTitleSelectEvent(self, index):

        bbox = win32gui.GetWindowRect(self.hwndInComboBox[index])
        x = bbox[0]
        y = bbox[1]

        width = bbox[2] - bbox[0]
        height = bbox[3] - bbox[1]

        self.spinBoxWindowMoveX.setValue(x)
        self.spinBoxWindowMoveY.setValue(y)
        self.spinBoxWindowMoveWidth.setValue(width)
        self.spinBoxWindowMoveHeight.setValue(height)

    def TestEvent(self):
        #print self.lineEditWindowRegEx.text()
        if self.lineEditWindowRegEx.text() == "":
            self.message = QMessageBox.critical(self, 'Error', "You have to insert the Window Reg Ex value!", QMessageBox.Ok)
            return

        regex = self.lineEditWindowRegEx.text()
        Window.Bind(regex, timeout=0)
        Window.Unbind()

    def ImportSizeEvent(self):

        index = self.comboBoxVisibleWindows.currentIndex()
        bbox = win32gui.GetWindowRect(self.hwndInComboBox[index])
        x = bbox[0]
        y = bbox[1]

        width = bbox[2] - bbox[0]
        height = bbox[3] - bbox[1]

        self.spinBoxWindowMoveX.setValue(x)
        self.spinBoxWindowMoveY.setValue(y)
        self.spinBoxWindowMoveWidth.setValue(width)
        self.spinBoxWindowMoveHeight.setValue(height)

    def UpdateWinComboBox(self):

        self.comboBoxVisibleWindows.clear()
        self.hwndInComboBox = []

        if sys.platform == 'win32':

            toplist, winlist = [], []

            def enum_callback(hwnd, results):
                winlist.append((hwnd, win32gui.GetWindowText(hwnd)))

            win32gui.EnumWindows(enum_callback, toplist)

            visibleWindows = [(hwnd, curTitle) for hwnd, curTitle in winlist if win32gui.IsWindowVisible(hwnd) != 0]

            for window in visibleWindows:
                if window[1] != "" and window[1].lower() != "start":
                    self.comboBoxVisibleWindows.addItem(window[1])
                    self.hwndInComboBox.append(window[0])
            #self.comboBoxVisibleWindows.Width = 424
                    #pass
                #win32gui.PostMessage(hiddenTool[0], win32con.WM_CLOSE, 0, 0)


    def BindWindow(self):

        if self.lineEditWindowRegEx.text() == "":
            self.message = QMessageBox.critical(self, 'Error', "You have to insert the Window Reg Ex value!", QMessageBox.Ok)
            return

        if self.checkBoxEnablePerfData.isChecked() is True and self.lineEdit.text() == "":
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

        regex = self.lineEditWindowRegEx.text().replace("\\","\\\\")

        if self.checkBoxEnablePerfData.isChecked() is True:
            timeOut = self.spinBoxPerfCritical.value() + 15
        else:
            timeOut = 15

        if self.checkBoxMaximizeWindow.isChecked() is True:
            editor_service.insert_text("performance = Window.Bind(\"" + regex + "\", timeout=" + str(timeOut) + ", maximize=True)")
        else:
            editor_service.insert_text("performance = Window.Bind(\"" + regex + "\", timeout=" + str(timeOut) + ")")

        if self.checkBoxEnablePerfData.isChecked() is True:
            editor_service.insert_text(os.linesep)
            editor_service.insert_text(leadingChar + "NagiosUtils.AddPerformanceData(\"" + self.lineEdit.text() + "\", performance, " + str(self.spinBoxPerfWarning.value()) + ", " + str(self.spinBoxPerfCritical.value()) + ")")

        editor_service.insert_text(os.linesep)
        editor_service.insert_text(leadingChar)

    def UnbindWindow(self):

        if self.lineEditWindowRegEx.text() == "":
            self.message = QMessageBox.critical(self, 'Error', "You have to insert the Window Reg Ex value!", QMessageBox.Ok)
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

        editor_service.insert_text("Window.Unbind()")
        editor_service.insert_text(os.linesep)
        editor_service.insert_text(leadingChar)

    def CloseWindow(self):

        if self.lineEditWindowRegEx.text() == "":
            self.message = QMessageBox.critical(self, 'Error', "You have to insert the Window Reg Ex value!", QMessageBox.Ok)
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

        regex = self.lineEditWindowRegEx.text().replace("\\","\\\\")

        editor_service.insert_text("Window.Close(\"" + regex + "\")")

        editor_service.insert_text(os.linesep)
        editor_service.insert_text(leadingChar)

    def WaitForExit(self):

        if self.lineEditWindowRegEx.text() == "":
            self.message = QMessageBox.critical(self, 'Error', "You have to insert the Window Reg Ex value!", QMessageBox.Ok)
            return

        if self.checkBoxEnablePerfData.isChecked() is True and self.lineEdit.text() == "":
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

        regex = self.lineEditWindowRegEx.text().replace("\\","\\\\")

        if self.checkBoxEnablePerfData.isChecked() is True:
            timeOut = self.spinBoxPerfCritical.value() + 15
        else:
            timeOut = 15

        editor_service.insert_text("performance = Window.WaitForExit(\"" + regex + "\", timeout=" + str(timeOut) + ")")

        if self.checkBoxEnablePerfData.isChecked() is True:
            editor_service.insert_text(os.linesep)
            editor_service.insert_text(leadingChar + "NagiosUtils.AddPerformanceData(\"" + self.lineEdit.text() + "\", performance, " + str(self.spinBoxPerfWarning.value()) + ", " + str(self.spinBoxPerfCritical.value()) + ")")

        editor_service.insert_text(os.linesep)
        editor_service.insert_text(leadingChar)

    def UpdateWinLineEdit(self):
        self.lineEditWindowRegEx.setText(self.comboBoxVisibleWindows.currentText())

    def EnableMoveSpinBox(self):
        if self.radioButtonWindowMove.isChecked() is True:
            self.spinBoxWindowMoveHeight.setEnabled(False)
            self.spinBoxWindowMoveWidth.setEnabled(False)
            self.label_5.setEnabled(False)
            self.label_6.setEnabled(False)
        else:
            self.spinBoxWindowMoveHeight.setEnabled(True)
            self.spinBoxWindowMoveWidth.setEnabled(True)
            self.label_5.setEnabled(True)
            self.label_6.setEnabled(True)

    def MoveOrResize(self):
        #if self.lineEditWindowRegEx.text() == "":
        #    return

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

        #regex = self.lineEditWindowRegEx.text().replace("\\","\\\\")

        if self.radioButtonWindowResize.isChecked() is True:
            editor_service.insert_text("Window.Resize(" + str(self.spinBoxWindowMoveX.value()) + ", " + str(self.spinBoxWindowMoveY.value()) + ", " + str(self.spinBoxWindowMoveWidth.value()) + ", " + str(self.spinBoxWindowMoveHeight.value()) +")")
        else:
            editor_service.insert_text("Window.Move(" + str(self.spinBoxWindowMoveX.value()) + ", " + str(self.spinBoxWindowMoveY.value()) +")")
        editor_service.insert_text(os.linesep)
        editor_service.insert_text(leadingChar)

    def keyPressEvent(self, event):

        if event.key() == Qt.Key_Escape:
            self.close()

    def CancelEvent(self):
        self.close()

    def CropRegion(self):
        self.CropRegionX = 0
        self.CropRegionY = 0
        self.CropRegionW = 0
        self.CropRegionH = 0

        if self.plugin.undockWindowOpened is True:
            self.message = QMessageBox.critical(self, 'Error', "Please close the Al\'exa - tools menu!", QMessageBox.Ok)
            return

        if self.checkBoxRegionOrigin.isChecked() is True:
            regex = self.lineEditWindowRegEx.text()

            if self.lineEditWindowRegEx.text() == "":
                self.message = QMessageBox.critical(self, 'Error', "You have to insert the Window Reg Ex value!", QMessageBox.Ok)
                return

            Window.Bind(regex, timeout=0)

            if Window.x is None or Window.y is None:
                self.message = QMessageBox.critical(self, 'Error', "The Window was not found.\nTry to adjust the Window Reg Ex value!", QMessageBox.Ok)
                return

            self.windowX = Window.x
            self.windowY = Window.y

            Window.Unbind()

        self.setVisible(False)

        '''
        if sys.platform == 'win32':
            hwnd = win32gui.GetForegroundWindow()
            win32gui.ShowWindow(hwnd, 0)

            toplist = []
            winlist = []

            def enum_callback(hwnd, results):
                winlist.append((hwnd, win32gui.GetWindowText(hwnd)))
            win32gui.EnumWindows(enum_callback, toplist)
            #if self.undocked is False:
            firefox = [(hwnd, title) for hwnd, title in
                winlist if 'exa-ide' in title.lower() or 'exa tool' in title.lower() and 'about' not in title.lower() and 'command prompt' not in title.lower()]

            print firefox
            # just grab the first window that matches
            #firefox = firefox[0]
            for ninja in firefox:
                #print str(ninja[0]) + " " + ninja[1]
                win32gui.ShowWindow(ninja[0], 0)
            #else:
                #self.undockWindow.hide()
        '''
        time.sleep(1)

        app = wx.App(False)
        screen = wx.ScreenDC()
        size = screen.GetSize()
        bmp = wx.EmptyBitmap(size[0], size[1])
        mem = wx.MemoryDC(bmp)
        mem.Blit(0, 0, size[0], size[1], screen, 0, 0)
        del mem  # Release bitmap
        bmp.SaveFile(self.plug_path + os.sep +'alexatools' + os.sep + 'tmp' + os.sep + 'screenshot.png', wx.BITMAP_TYPE_PNG)

        self.cropWindow = CropRegionClass(self)
        self.cropWindow.setWindowTitle("alexa screen")
        self.cropWindow.showFullScreen()
        self.cropWindow.setMouseTracking(True)

    def AddBindRegion(self):
        if self.spinBoxRegionX.value() == 0 and self.spinBoxRegionX_2.value() == 0 and self.spinBoxRegionHeight.value() == 0 and self.spinBoxRegionWidth.value() == 0:
            self.message = QMessageBox.critical(self, 'Error', "You have to crop a region before to add the code!", QMessageBox.Ok)
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

        if self.checkBoxRegionOrigin.isChecked() is True:
            editor_service.insert_text("SearchRegion.Bind(" + str(self.spinBoxRegionX.value()) + " - Window.x, " + str(self.spinBoxRegionX_2.value()) + " - Window.y, " + str(self.spinBoxRegionWidth.value()) + ", " + str(self.spinBoxRegionHeight.value()) + ")")
        else:
            editor_service.insert_text("SearchRegion.Bind(" + str(self.spinBoxRegionX.value()) + ", " + str(self.spinBoxRegionX_2.value()) + ", " + str(self.spinBoxRegionWidth.value()) + ", " + str(self.spinBoxRegionHeight.value()) + ")")

        editor_service.insert_text(os.linesep)
        editor_service.insert_text(leadingChar)

    def AddUnbindRegion(self):
        if self.spinBoxRegionX.value() == 0 and self.spinBoxRegionX_2.value() == 0 and self.spinBoxRegionHeight.value() == 0 and self.spinBoxRegionWidth.value() == 0:
            self.message = QMessageBox.critical(self, 'Error', "You have to crop a region before to add the code!", QMessageBox.Ok)
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

        editor_service.insert_text("SearchRegion.Unbind()")

        editor_service.insert_text(os.linesep)
        editor_service.insert_text(leadingChar)