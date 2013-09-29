# -*- coding: UTF-8 -*-
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

#PYTHON
import copy

#QT Toolkit
from PyQt4.QtGui import *
from PyQt4.QtCore import *
#PIL
import Image
#ALEXA
from Alexa import *


class AppImgDialog(QWidget):

    def __init__(self, caller, objectIndex, openTabIndex):
        super(AppImgDialog, self).__init__()
        self.caller = caller
        self.plug_path = caller.plug_path
        self.objectIndex = objectIndex
        self.openTabIndex = openTabIndex
        self.caller.CropLabel = False
        self.controlOffsetY = 20
        self.controlOffsetStep = 30
        self.OkIsPressed = False
        self.ResetPressed = False
        self.initUI()

    def initUI(self):
        icon = QIcon()
        icon.addPixmap(QPixmap(self.plug_path + "/images/image.png"), QIcon.Normal, QIcon.Off)
        self.setWindowIcon(icon)
        self.tabWidget = QTabWidget(self)
        self.tabWidget.setGeometry(QRect(5, 6, 331, 321))
        self.tabWidget.setObjectName("tabWidget")
        self.tabObject = QWidget()
        self.tabObject.setObjectName("tabObject")
        self.gridLayoutWidget_2 = QWidget(self.tabObject)
        self.gridLayoutWidget_2.setGeometry(QRect(10, 20, 301, 151))
        self.gridLayoutWidget_2.setObjectName("gridLayoutWidget_2")
        self.gridLayoutObjectProperties = QGridLayout(self.gridLayoutWidget_2)
        self.gridLayoutObjectProperties.setMargin(0)
        self.gridLayoutObjectProperties.setObjectName("gridLayoutObjectProperties")
        self.textEditImgDescription = QTextEdit(self.gridLayoutWidget_2)
        self.textEditImgDescription.setLineWrapMode(QTextEdit.NoWrap)
        self.textEditImgDescription.setObjectName("textEditImgDescription")
        self.gridLayoutObjectProperties.addWidget(self.textEditImgDescription, 1, 1, 1, 3)
        self.labelImgName = QLabel(self.gridLayoutWidget_2)
        self.labelImgName.setObjectName("labelImgName")
        self.gridLayoutObjectProperties.addWidget(self.labelImgName, 0, 0, 1, 1)
        self.labelImgHeight = QLabel(self.gridLayoutWidget_2)
        self.labelImgHeight.setObjectName("labelImgHeight")
        self.gridLayoutObjectProperties.addWidget(self.labelImgHeight, 2, 0, 1, 1)
        self.lineEditImgName = QLineEdit(self.gridLayoutWidget_2)
        self.lineEditImgName.setObjectName("lineEditImgName")
        self.gridLayoutObjectProperties.addWidget(self.lineEditImgName, 0, 1, 1, 2)
        self.spinBoxImgHeight = QSpinBox(self.gridLayoutWidget_2)
        self.spinBoxImgHeight.setMaximum(999999)
        self.spinBoxImgHeight.setObjectName("spinBoxImgHeight")
        self.gridLayoutObjectProperties.addWidget(self.spinBoxImgHeight, 2, 1, 1, 1)
        self.labelImgDescription = QLabel(self.gridLayoutWidget_2)
        self.labelImgDescription.setObjectName("labelImgDescription")
        self.gridLayoutObjectProperties.addWidget(self.labelImgDescription, 1, 0, 1, 1)
        self.spinBoxImgWidth = QSpinBox(self.gridLayoutWidget_2)
        self.spinBoxImgWidth.setMaximum(999999)
        self.spinBoxImgWidth.setObjectName("spinBoxImgWidth")
        self.gridLayoutObjectProperties.addWidget(self.spinBoxImgWidth, 3, 1, 1, 1)
        self.labelImgThreshold = QLabel(self.gridLayoutWidget_2)
        self.labelImgThreshold.setObjectName("labelImgThreshold")
        self.gridLayoutObjectProperties.addWidget(self.labelImgThreshold, 2, 2, 1, 1)
        self.labelImgWidth = QLabel(self.gridLayoutWidget_2)
        self.labelImgWidth.setObjectName("labelImgWidth")
        self.gridLayoutObjectProperties.addWidget(self.labelImgWidth, 3, 0, 1, 1)
        self.doubleSpinBoxImgThreshold = QDoubleSpinBox(self.gridLayoutWidget_2)
        self.doubleSpinBoxImgThreshold.setDecimals(3)
        self.doubleSpinBoxImgThreshold.setMaximum(100000.0)
        self.doubleSpinBoxImgThreshold.setSingleStep(0.001)
        self.doubleSpinBoxImgThreshold.setObjectName("doubleSpinBoxImgThreshold")
        self.gridLayoutObjectProperties.addWidget(self.doubleSpinBoxImgThreshold, 2, 3, 1, 1)
        self.tabWidget.addTab(self.tabObject, "")
        self.tab_3 = QWidget()
        self.tab_3.setObjectName("tab_3")
        self.gridLayoutWidget_3 = QWidget(self.tab_3)
        self.gridLayoutWidget_3.setGeometry(QRect(10, 20, 301, 261))
        self.gridLayoutWidget_3.setObjectName("gridLayoutWidget_3")
        self.gridLayoutExtraActions = QGridLayout(self.gridLayoutWidget_3)
        self.gridLayoutExtraActions.setMargin(0)
        self.gridLayoutExtraActions.setObjectName("gridLayoutExtraActions")
        self.radioButtonImgClick = QRadioButton(self.gridLayoutWidget_3)
        self.radioButtonImgClick.setChecked(True)
        self.radioButtonImgClick.setObjectName("radioButtonImgClick")
        self.gridLayoutExtraActions.addWidget(self.radioButtonImgClick, 1, 0, 1, 1)
        self.spinBoxImgRegionY = QSpinBox(self.gridLayoutWidget_3)
        self.spinBoxImgRegionY.setEnabled(False)
        self.spinBoxImgRegionY.setMinimum(-999999)
        self.spinBoxImgRegionY.setMaximum(999999)
        self.spinBoxImgRegionY.setObjectName("spinBoxImgRegionY")
        self.gridLayoutExtraActions.addWidget(self.spinBoxImgRegionY, 7, 3, 1, 1)
        self.labelImgWarningPerfData = QLabel(self.gridLayoutWidget_3)
        self.labelImgWarningPerfData.setEnabled(False)
        self.labelImgWarningPerfData.setObjectName("labelImgWarningPerfData")
        self.gridLayoutExtraActions.addWidget(self.labelImgWarningPerfData, 5, 0, 1, 1)
        self.spinBoxImgRegionHeight = QSpinBox(self.gridLayoutWidget_3)
        self.spinBoxImgRegionHeight.setEnabled(False)
        self.spinBoxImgRegionHeight.setMaximum(999999)
        self.spinBoxImgRegionHeight.setObjectName("spinBoxImgRegionHeight")
        self.gridLayoutExtraActions.addWidget(self.spinBoxImgRegionHeight, 8, 1, 1, 1)
        self.spinBoxImgCriticalPerfData = QSpinBox(self.gridLayoutWidget_3)
        self.spinBoxImgCriticalPerfData.setEnabled(False)
        self.spinBoxImgCriticalPerfData.setMaximum(3600)
        self.spinBoxImgCriticalPerfData.setObjectName("spinBoxImgCriticalPerfData")
        self.gridLayoutExtraActions.addWidget(self.spinBoxImgCriticalPerfData, 5, 3, 1, 1)
        self.checkBoxImgUseMouse = QCheckBox(self.gridLayoutWidget_3)
        self.checkBoxImgUseMouse.setChecked(True)
        self.checkBoxImgUseMouse.setObjectName("checkBoxImgUseMouse")
        self.gridLayoutExtraActions.addWidget(self.checkBoxImgUseMouse, 0, 0, 1, 2)
        self.checkBoxImgUseKeyboard = QCheckBox(self.gridLayoutWidget_3)
        self.checkBoxImgUseKeyboard.setObjectName("checkBoxImgUseKeyboard")
        self.gridLayoutExtraActions.addWidget(self.checkBoxImgUseKeyboard, 2, 0, 1, 2)
        self.spinBoxImgRegionX = QSpinBox(self.gridLayoutWidget_3)
        self.spinBoxImgRegionX.setEnabled(False)
        self.spinBoxImgRegionX.setMinimum(-999999)
        self.spinBoxImgRegionX.setMaximum(999999)
        self.spinBoxImgRegionX.setObjectName("spinBoxImgRegionX")
        self.gridLayoutExtraActions.addWidget(self.spinBoxImgRegionX, 7, 1, 1, 1)
        self.spinBoxImgRegionWidth = QSpinBox(self.gridLayoutWidget_3)
        self.spinBoxImgRegionWidth.setEnabled(False)
        self.spinBoxImgRegionWidth.setMaximum(999999)
        self.spinBoxImgRegionWidth.setObjectName("spinBoxImgRegionWidth")
        self.gridLayoutExtraActions.addWidget(self.spinBoxImgRegionWidth, 8, 3, 1, 1)
        self.labelImgRegionY = QLabel(self.gridLayoutWidget_3)
        self.labelImgRegionY.setEnabled(False)
        self.labelImgRegionY.setObjectName("labelImgRegionY")
        self.gridLayoutExtraActions.addWidget(self.labelImgRegionY, 7, 2, 1, 1)
        self.spinBoxImgWarningPerfData = QSpinBox(self.gridLayoutWidget_3)
        self.spinBoxImgWarningPerfData.setEnabled(False)
        self.spinBoxImgWarningPerfData.setMaximum(3600)
        self.spinBoxImgWarningPerfData.setObjectName("spinBoxImgWarningPerfData")
        self.gridLayoutExtraActions.addWidget(self.spinBoxImgWarningPerfData, 5, 1, 1, 1)
        self.pushButtonImgBindRegion = QPushButton(self.gridLayoutWidget_3)
        self.pushButtonImgBindRegion.setObjectName("pushButtonImgBindRegion")
        self.gridLayoutExtraActions.addWidget(self.pushButtonImgBindRegion, 6, 0, 1, 1)
        self.labelImgRegionWidth = QLabel(self.gridLayoutWidget_3)
        self.labelImgRegionWidth.setEnabled(False)
        self.labelImgRegionWidth.setObjectName("labelImgRegionWidth")
        self.gridLayoutExtraActions.addWidget(self.labelImgRegionWidth, 8, 2, 1, 1)
        self.lineEditImgInsertText = QLineEdit(self.gridLayoutWidget_3)
        self.lineEditImgInsertText.setEnabled(False)
        self.lineEditImgInsertText.setObjectName("lineEditImgInsertText")
        self.gridLayoutExtraActions.addWidget(self.lineEditImgInsertText, 3, 1, 1, 3)
        self.radioButtonImgDoubleClick = QRadioButton(self.gridLayoutWidget_3)
        self.radioButtonImgDoubleClick.setObjectName("radioButtonImgDoubleClick")
        self.gridLayoutExtraActions.addWidget(self.radioButtonImgDoubleClick, 1, 1, 1, 2)
        self.labelImgRegionX = QLabel(self.gridLayoutWidget_3)
        self.labelImgRegionX.setEnabled(False)
        self.labelImgRegionX.setObjectName("labelImgRegionX")
        self.gridLayoutExtraActions.addWidget(self.labelImgRegionX, 7, 0, 1, 1)
        self.checkBoxImgEnablePerfData = QCheckBox(self.gridLayoutWidget_3)
        self.checkBoxImgEnablePerfData.setObjectName("checkBoxImgEnablePerfData")
        self.gridLayoutExtraActions.addWidget(self.checkBoxImgEnablePerfData, 4, 0, 1, 4)
        self.labelImgCriticalPerfData = QLabel(self.gridLayoutWidget_3)
        self.labelImgCriticalPerfData.setEnabled(False)
        self.labelImgCriticalPerfData.setObjectName("labelImgCriticalPerfData")
        self.gridLayoutExtraActions.addWidget(self.labelImgCriticalPerfData, 5, 2, 1, 1)
        self.labelImgInsertText = QLabel(self.gridLayoutWidget_3)
        self.labelImgInsertText.setEnabled(False)
        self.labelImgInsertText.setObjectName("labelImgInsertText")
        self.gridLayoutExtraActions.addWidget(self.labelImgInsertText, 3, 0, 1, 1)
        self.labelImgRegionHeight = QLabel(self.gridLayoutWidget_3)
        self.labelImgRegionHeight.setEnabled(False)
        self.labelImgRegionHeight.setObjectName("labelImgRegionHeight")
        self.gridLayoutExtraActions.addWidget(self.labelImgRegionHeight, 8, 0, 1, 1)
        self.tabWidget.addTab(self.tab_3, "")
        self.pushButtonApply = QPushButton(self)
        self.pushButtonApply.setGeometry(QRect(10, 339, 75, 23))
        self.pushButtonApply.setObjectName("pushButtonApply")
        self.pushButtonReset = QPushButton(self)
        self.pushButtonReset.setGeometry(QRect(100, 339, 75, 23))
        self.pushButtonReset.setObjectName("pushButtonReset")
        self.pushButtonTest = QPushButton(self)
        self.pushButtonTest.setGeometry(QRect(250, 339, 75, 23))
        self.pushButtonTest.setObjectName("pushButtonTest")
        self.line = QFrame(self)
        self.line.setGeometry(QRect(203, 330, 20, 41))
        self.line.setFrameShape(QFrame.VLine)
        self.line.setFrameShadow(QFrame.Sunken)
        self.line.setObjectName("line")

        self.tabWidget.setCurrentIndex(self.openTabIndex)

        self.labelImgName.setText("Name")
        self.labelImgHeight.setText("Height")
        self.labelImgDescription.setText("Description")
        self.labelImgThreshold.setText("Threshold")
        self.labelImgWidth.setText("Width")
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tabObject), "Image Properties")
        self.radioButtonImgClick.setText("Click")
        self.labelImgWarningPerfData.setText("Warning")
        self.checkBoxImgUseMouse.setText("Use Mouse")
        self.checkBoxImgUseKeyboard.setText("Use Keyboard")
        self.labelImgRegionY.setText("Region y")
        self.pushButtonImgBindRegion.setText("Bind Region")
        self.labelImgRegionWidth.setText("Region Width")
        self.radioButtonImgDoubleClick.setText("Double Click")
        self.labelImgRegionX.setText("Region x")
        self.checkBoxImgEnablePerfData.setText("Enable Perselfance Data")
        self.labelImgCriticalPerfData.setText("Critical")
        self.labelImgInsertText.setText("Insert Text")
        self.labelImgRegionHeight.setText("Region Height")
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_3), "Extra Actions")
        self.pushButtonApply.setText("Apply")
        self.pushButtonReset.setText("Reset")
        self.pushButtonTest.setText("Test")

        self.setGeometry(300, 300, 339, 376)
        #self.setGeometry(300, 300, 600, self.controlOffsetY + 200)
        self.setFixedSize(self.size())

        self.setWindowTitle('Application Image Properties')
        #self.setWindowFlags(Qt.Window | Qt.WindowMinimizeButtonHint)
        #self.setWindowFlags(Qt.FramelessWindowHint)
        self.setWindowFlags(Qt.WindowCloseButtonHint | Qt.WindowStaysOnTopHint)

        self.connect(self.tabWidget, SIGNAL("currentChanged(int)"), self, SLOT("TabChangedEvent(int)"))
        self.connect(self.lineEditImgName, SIGNAL('textChanged(QString)'), self.LineEditImgNameEvent)
        self.connect(self.textEditImgDescription, SIGNAL('textChanged()'), self.TextEditImgDescriptionEvent)
        self.connect(self.spinBoxImgHeight, SIGNAL('valueChanged(int)'), self.SpinBoxImgHeightChangeEvent)
        self.connect(self.spinBoxImgWidth, SIGNAL('valueChanged(int)'), self.SpinBoxImgWidthChangeEvent)
        self.connect(self.doubleSpinBoxImgThreshold, SIGNAL('valueChanged(double)'), self.DoubleSpinBoxImgThresholdEvent)

        self.connect(self.checkBoxImgUseMouse, SIGNAL('stateChanged(int)'), self.CheckBoxImgUseMouseEvent)
        #self.connect(self.radioButtonImgClick, SIGNAL('stateChanged(int)'), self.RadioButtonImgClickEvent)
        #self.connect(self.radioButtonImgDoubleClick, SIGNAL('stateChanged(int)'), self.RadioButtonImgDoubleClickEvent)
        self.connect(self.checkBoxImgUseKeyboard, SIGNAL('stateChanged(int)'), self.CheckBoxImgUseKeyboardEvent)
        self.connect(self.lineEditImgInsertText, SIGNAL('textChanged(QString)'), self.LineEditImgInsertTextEvent)
        self.connect(self.checkBoxImgEnablePerfData, SIGNAL('stateChanged(int)'), self.CheckBoxImgEnablePerfDataEvent)
        self.connect(self.spinBoxImgWarningPerfData, SIGNAL('valueChanged(int)'), self.SpinBoxImgWarningPerfDataEvent)
        self.connect(self.spinBoxImgCriticalPerfData, SIGNAL('valueChanged(int)'), self.SpinBoxImgCriticalPerfDataEvent)
        self.connect(self.pushButtonImgBindRegion, SIGNAL("clicked()"), self.PushButtonImgBindRegionEvent)
        self.connect(self.spinBoxImgRegionX, SIGNAL('valueChanged(int)'), self.SpinBoxImgRegionXEvent)
        self.connect(self.spinBoxImgRegionY, SIGNAL('valueChanged(int)'), self.SpinBoxImgRegionYEvent)
        self.connect(self.spinBoxImgRegionHeight, SIGNAL('valueChanged(int)'), self.SpinBoxImgRegionHeightEvent)
        self.connect(self.spinBoxImgRegionWidth, SIGNAL('valueChanged(int)'), self.SpinBoxImgRegionWidthEvent)
        self.connect(self.pushButtonApply, SIGNAL("clicked()"), self.PushButtonApplyEvent)
        self.connect(self.pushButtonReset, SIGNAL("clicked()"), self.PushButtonResetEvent)
        self.connect(self.pushButtonTest, SIGNAL("clicked()"), self.PushButtonTestEvent)

        self.UpdateControls()

        self.show()

    @pyqtSlot(int)
    def TabChangedEvent(self, tabIndex):
        self.RadioButtonImgClickEvent()
        self.RadioButtonImgDoubleClickEvent()

    def LineEditImgNameEvent(self):
        self.lineEditImgName.setText(self.lineEditImgName.text().replace(" ","_"))
        self.caller.AlexaAppImages[self.objectIndex].Name = self.lineEditImgName.text()

    def TextEditImgDescriptionEvent(self):
        self.caller.AlexaAppImages[self.objectIndex].Description = self.textEditImgDescription.toPlainText()

    def SpinBoxImgHeightChangeEvent(self):
        self.caller.AlexaAppImages[self.objectIndex].Height = self.spinBoxImgHeight.value()
        self.caller.update()

    def SpinBoxImgWidthChangeEvent(self):
        self.caller.AlexaAppImages[self.objectIndex].Width = self.spinBoxImgWidth.value()
        self.caller.update()

    def DoubleSpinBoxImgThresholdEvent(self):
        self.caller.AlexaAppImages[self.objectIndex].Threshold = self.doubleSpinBoxImgThreshold.value()

    def CheckBoxImgUseMouseEvent(self):
        if self.caller.AlexaAppImages[self.objectIndex].UseMouse is True and self.ResetPressed is True:
            self.checkBoxImgUseMouse.setChecked(True)
            self.radioButtonImgClick.setEnabled(True)
            self.radioButtonImgDoubleClick.setEnabled(True)
        elif self.checkBoxImgUseMouse.isChecked() is True:
            self.radioButtonImgClick.setEnabled(True)
            self.radioButtonImgDoubleClick.setEnabled(True)
            self.RadioButtonImgClickEvent()
            self.RadioButtonImgDoubleClickEvent()
            self.caller.AlexaAppImages[self.objectIndex].UseMouse = True
        else:
            self.radioButtonImgClick.setEnabled(False)
            self.radioButtonImgDoubleClick.setEnabled(False)
            #self.caller.AlexaAppImages[self.objectIndex].Click = False
            #self.caller.AlexaAppImages[self.objectIndex].DoubleClick = False
            self.caller.AlexaAppImages[self.objectIndex].UseMouse = False

        '''
        if self.caller.AlexaAppImages[self.objectIndex].DoubleClick is True:
            self.radioButtonImgDoubleClick.setChecked(True)
        else:
            self.radioButtonImgClick.setChecked(True)
        '''
    def RadioButtonImgClickEvent(self):
        #print "ooooooooooooooooooooo oooooooooo o o o ooooooooooo"
        if self.radioButtonImgClick.isChecked():
            self.caller.AlexaAppImages[self.objectIndex].Click = True
            self.caller.AlexaAppImages[self.objectIndex].DoubleClick = False

    def RadioButtonImgDoubleClickEvent(self):
        #print "sdsdsdsdsdssddsddssd dfd sfd sfd sf sf"
        if self.radioButtonImgDoubleClick.isChecked():
            self.caller.AlexaAppImages[self.objectIndex].Click = False
            self.caller.AlexaAppImages[self.objectIndex].DoubleClick = True

    def CheckBoxImgUseKeyboardEvent(self):
        if self.checkBoxImgUseKeyboard.isChecked() is True:
            self.lineEditImgInsertText.setEnabled(True)
            self.labelImgInsertText.setEnabled(True)
        else:
            self.lineEditImgInsertText.setEnabled(False)
            self.labelImgInsertText.setEnabled(False)

    def LineEditImgInsertTextEvent(self):
        self.caller.AlexaAppImages[self.objectIndex].InsertText = self.lineEditImgInsertText.text()

    def CheckBoxImgEnablePerfDataEvent(self):
        if self.checkBoxImgEnablePerfData.isChecked() is True:
            self.caller.AlexaAppImages[self.objectIndex].EnablePerfData = True
            self.labelImgWarningPerfData.setEnabled(True)
            self.spinBoxImgWarningPerfData.setEnabled(True)
            self.labelImgCriticalPerfData.setEnabled(True)
            self.spinBoxImgCriticalPerfData.setEnabled(True)
        else:
            self.caller.AlexaAppImages[self.objectIndex].EnablePerfData = False
            self.labelImgWarningPerfData.setEnabled(False)
            self.spinBoxImgWarningPerfData.setEnabled(False)
            self.labelImgCriticalPerfData.setEnabled(False)
            self.spinBoxImgCriticalPerfData.setEnabled(False)

    def SpinBoxImgWarningPerfDataEvent(self):
        self.caller.AlexaAppImages[self.objectIndex].PerfWarningLevel = self.spinBoxImgWarningPerfData.value()

    def SpinBoxImgCriticalPerfDataEvent(self):
        self.caller.AlexaAppImages[self.objectIndex].PerfCriticalLevel = self.spinBoxImgCriticalPerfData.value()

    def PushButtonImgBindRegionEvent(self):
        self.caller.CropRegion = True
        self.close()

    def SpinBoxImgRegionXEvent(self):
        self.caller.AlexaAppImages[self.objectIndex].CropRegionX = self.spinBoxImgRegionX.value()
        self.caller.update()

    def SpinBoxImgRegionYEvent(self):
        self.caller.AlexaAppImages[self.objectIndex].CropRegionY = self.spinBoxImgRegionY.value()
        self.caller.update()

    def SpinBoxImgRegionHeightEvent(self):
        self.caller.AlexaAppImages[self.objectIndex].CropRegionHeight = self.spinBoxImgRegionHeight.value()
        self.caller.update()

    def SpinBoxImgRegionWidthEvent(self):
        self.caller.AlexaAppImages[self.objectIndex].CropRegionWidth = self.spinBoxImgRegionWidth.value()
        self.caller.update()

    def PushButtonApplyEvent(self):
        self.Apply()
        self.caller.AlexaAppImagesBackup[self.objectIndex] = copy.deepcopy(self.caller.AlexaAppImages[self.objectIndex])

    def PushButtonResetEvent(self):
        self.ResetPressed = True
        self.caller.indexFound = None
        self.caller.AlexaAppImages[self.objectIndex] = copy.deepcopy(self.caller.AlexaAppImagesBackup[self.objectIndex])

        if self.caller.AlexaAppImages[self.objectIndex].UseMouse is True:
            self.checkBoxImgUseMouse.setChecked(True)
        if self.caller.AlexaAppImages[self.objectIndex].UseKeyboard is False:
            self.checkBoxImgUseKeyboard.setChecked(False)
        if self.caller.AlexaAppImages[self.objectIndex].EnablePerfData is False:
            self.checkBoxImgEnablePerfData.setChecked(False)
        self.caller.update()
        self.UpdateControls()
        self.ResetPressed = False

    def PushButtonTestEvent(self):

        Screen.ImageFromIde = self.caller.OriginalScreenshot.copy()

        SERVICE_NAME = "editor"
        editor_service = self.caller.plugin.locator.get_service(SERVICE_NAME)
        fullFileName = editor_service.get_editor_path()
        filePath = os.path.split(fullFileName)[0]
        if os.path.exists(os.path.join(filePath, 'images')) is False:
            os.makedirs(os.path.join(filePath, 'images'))

        PilImage = Image.open(self.plug_path + os.sep + 'tmp' + os.sep + 'screenshot.png')
        cropped = (self.caller.AlexaAppImages[self.objectIndex].RectX, self.caller.AlexaAppImages[self.objectIndex].RectY, self.caller.AlexaAppImages[self.objectIndex].RectX + self.caller.AlexaAppImages[self.objectIndex].Width, self.caller.AlexaAppImages[self.objectIndex].RectY + self.caller.AlexaAppImages[self.objectIndex].Height)
        #print self.plug_path + os.sep + 'tmp' + os.sep
        area = PilImage.crop(cropped)
        area.save(os.path.join(filePath, 'images', "test.png"))
        self.caller.AlexaAppImages[self.objectIndex].Path = os.path.join(filePath, 'images', "test.png")
        self.caller.AlexaAppImages[self.objectIndex].Bind(0)
        #print self.caller.AlexaAppImages[self.objectIndex].x, self.caller.AlexaAppImages[self.objectIndex].y
        #if self.caller.AlexaAppImages[self.objectIndex].x is not None and self.caller.AlexaAppImages[self.objectIndex].y is not None:
        if self.caller.AlexaAppImages[self.objectIndex].x >= self.caller.AlexaAppImages[self.objectIndex].RectX - 15 and\
        self.caller.AlexaAppImages[self.objectIndex].x <= self.caller.AlexaAppImages[self.objectIndex].RectX + 15 and\
        self.caller.AlexaAppImages[self.objectIndex].y >= self.caller.AlexaAppImages[self.objectIndex].RectY - 15 and\
        self.caller.AlexaAppImages[self.objectIndex].y <= self.caller.AlexaAppImages[self.objectIndex].RectY + 15:
            #self.message = QMessageBox.question(self, 'Removal', "Are you sure ", QMessageBox.Yes | QMessageBox.No)
            self.caller.AlexaAppImages[self.objectIndex].x = None
            self.caller.AlexaAppImages[self.objectIndex].y = None
            self.caller.indexFound = self.objectIndex
        else:
            self.caller.indexFound = None
            self.message = QMessageBox.question(self, 'Error', "Application Imgage not found", QMessageBox.Ok)
        self.caller.update()

    def UpdateControls(self):

        self.lineEditImgName.setText(self.caller.AlexaAppImages[self.objectIndex].Name)

        self.textEditImgDescription.setText(self.caller.AlexaAppImages[self.objectIndex].Description)

        self.spinBoxImgHeight.setValue(self.caller.AlexaAppImages[self.objectIndex].Height)
        self.spinBoxImgWidth.setValue(self.caller.AlexaAppImages[self.objectIndex].Width)
        self.doubleSpinBoxImgThreshold.setValue(self.caller.AlexaAppImages[self.objectIndex].Threshold)


        if self.caller.AlexaAppImages[self.objectIndex].DoubleClick is True:
            self.radioButtonImgDoubleClick.setChecked(True)
        else:
            self.radioButtonImgClick.setChecked(True)

        if self.caller.AlexaAppImages[self.objectIndex].UseMouse is False:
            self.checkBoxImgUseMouse.setChecked(False)

        self.CheckBoxImgUseMouseEvent()

        if self.caller.AlexaAppImages[self.objectIndex].UseKeyboard is True:
            self.lineEditImgInsertText.setEnabled(True)
            self.labelImgInsertText.setEnabled(True)
            self.checkBoxImgUseKeyboard.setChecked(True)
        self.lineEditImgInsertText.setText(self.caller.AlexaAppImages[self.objectIndex].InsertText)

        if self.caller.AlexaAppImages[self.objectIndex].EnablePerfData is True:
            self.checkBoxImgEnablePerfData.setChecked(True)

        self.spinBoxImgWarningPerfData.setValue(self.caller.AlexaAppImages[self.objectIndex].PerfWarningLevel)
        self.spinBoxImgCriticalPerfData.setValue(self.caller.AlexaAppImages[self.objectIndex].PerfCriticalLevel)

        self.spinBoxImgRegionX.setValue(self.caller.AlexaAppImages[self.objectIndex].CropRegionX)
        self.spinBoxImgRegionY.setValue(self.caller.AlexaAppImages[self.objectIndex].CropRegionY)
        self.spinBoxImgRegionHeight.setValue(self.caller.AlexaAppImages[self.objectIndex].CropRegionHeight)
        self.spinBoxImgRegionWidth.setValue(self.caller.AlexaAppImages[self.objectIndex].CropRegionWidth)

        if self.caller.AlexaAppImages[self.objectIndex].CropRegionX != 0 and self.caller.AlexaAppImages[self.objectIndex].CropRegionY != 0 and self.caller.AlexaAppImages[self.objectIndex].CropRegionWidth != 0 and self.caller.AlexaAppImages[self.objectIndex].CropRegionHeight != 0:
            self.spinBoxImgRegionX.setEnabled(True)
            self.spinBoxImgRegionY.setEnabled(True)
            self.spinBoxImgRegionHeight.setEnabled(True)
            self.spinBoxImgRegionWidth.setEnabled(True)
            self.labelImgRegionX.setEnabled(True)
            self.labelImgRegionY.setEnabled(True)
            self.labelImgRegionWidth.setEnabled(True)
            self.labelImgRegionHeight.setEnabled(True)
        else:
            self.spinBoxImgRegionX.setEnabled(False)
            self.spinBoxImgRegionY.setEnabled(False)
            self.spinBoxImgRegionHeight.setEnabled(False)
            self.spinBoxImgRegionWidth.setEnabled(False)
            self.labelImgRegionX.setEnabled(False)
            self.labelImgRegionY.setEnabled(False)
            self.labelImgRegionWidth.setEnabled(False)
            self.labelImgRegionHeight.setEnabled(False)

        self.caller.update()

        self.update()

    def keyPressEvent(self, event):

        if event.key() == Qt.Key_Escape:
            self.close()

    def closeEvent(self, event):
        self.Apply()

        self.caller.DialogOpened = False
        self.caller.indexFound = None
        self.caller.update()

    def Apply(self):
        self.caller.AlexaAppImages[self.objectIndex].Name = self.lineEditImgName.text()
        self.caller.AlexaAppImages[self.objectIndex].Description = self.textEditImgDescription.toPlainText()

        if self.radioButtonImgClick.isChecked():
            self.caller.AlexaAppImages[self.objectIndex].Click = True
            self.caller.AlexaAppImages[self.objectIndex].DoubleClick = False
        else:
            self.caller.AlexaAppImages[self.objectIndex].Click = False
            self.caller.AlexaAppImages[self.objectIndex].DoubleClick = True

        if self.checkBoxImgUseKeyboard.isChecked() is True:
            self.caller.AlexaAppImages[self.objectIndex].UseKeyboard = True
            self.caller.AlexaAppImages[self.objectIndex].InsertText = self.lineEditImgInsertText.text()
        else:
            self.caller.AlexaAppImages[self.objectIndex].UseKeyboard = False