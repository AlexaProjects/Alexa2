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

class AppTextDialog(QWidget):

    def __init__(self, caller, objectIndex, openTabIndex):
        super(AppTextDialog, self).__init__()
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
        icon.addPixmap(QPixmap(self.plug_path + "/images/text-x-gettext-translation.png"), QIcon.Normal, QIcon.Off)
        self.setWindowIcon(icon)
        self.tabWidget = QTabWidget(self)
        self.tabWidget.setGeometry(QRect(5, 6, 331, 321))
        self.tabWidget.setObjectName("tabWidget")
        self.tabObject = QWidget()
        self.tabObject.setObjectName("tabObject")
        self.gridLayoutWidget_2 = QWidget(self.tabObject)
        self.gridLayoutWidget_2.setGeometry(QRect(10, 20, 301, 226))
        self.gridLayoutWidget_2.setObjectName("gridLayoutWidget_2")
        self.gridLayoutObjectProperties = QGridLayout(self.gridLayoutWidget_2)
        self.gridLayoutObjectProperties.setMargin(0)
        self.gridLayoutObjectProperties.setObjectName("gridLayoutObjectProperties")
        self.spinBoxObjWidth = QSpinBox(self.gridLayoutWidget_2)
        self.spinBoxObjWidth.setMaximum(999999)
        self.spinBoxObjWidth.setObjectName("spinBoxObjWidth")
        self.gridLayoutObjectProperties.addWidget(self.spinBoxObjWidth, 3, 1, 1, 1)
        self.lineEditObjName = QLineEdit(self.gridLayoutWidget_2)
        self.lineEditObjName.setObjectName("lineEditObjName")
        self.gridLayoutObjectProperties.addWidget(self.lineEditObjName, 0, 1, 1, 2)
        self.checkBoxObjTollerancePreview = QCheckBox(self.gridLayoutWidget_2)
        self.checkBoxObjTollerancePreview.setObjectName("checkBoxObjTollerancePreview")
        self.gridLayoutObjectProperties.addWidget(self.checkBoxObjTollerancePreview, 4, 2, 1, 2)
        self.spinBoxObjWidthTollerance = QSpinBox(self.gridLayoutWidget_2)
        self.spinBoxObjWidthTollerance.setMaximum(999999)
        self.spinBoxObjWidthTollerance.setObjectName("spinBoxObjWidthTollerance")
        self.gridLayoutObjectProperties.addWidget(self.spinBoxObjWidthTollerance, 3, 3, 1, 1)
        self.labelObjWidthTollerance = QLabel(self.gridLayoutWidget_2)
        self.labelObjWidthTollerance.setObjectName("labelObjWidthTollerance")
        self.gridLayoutObjectProperties.addWidget(self.labelObjWidthTollerance, 3, 2, 1, 1)
        self.spinBoxObjHeight = QSpinBox(self.gridLayoutWidget_2)
        self.spinBoxObjHeight.setMaximum(999999)
        self.spinBoxObjHeight.setObjectName("spinBoxObjHeight")
        self.gridLayoutObjectProperties.addWidget(self.spinBoxObjHeight, 2, 1, 1, 1)
        self.checkBoxObjBinarizeImage = QCheckBox(self.gridLayoutWidget_2)
        self.checkBoxObjBinarizeImage.setEnabled(False)
        self.checkBoxObjBinarizeImage.setChecked(True)
        self.checkBoxObjBinarizeImage.setObjectName("checkBoxObjBinarizeImage")
        self.gridLayoutObjectProperties.addWidget(self.checkBoxObjBinarizeImage, 5, 2, 1, 2)
        self.doubleSpinBoxObjContrastImage = QDoubleSpinBox(self.gridLayoutWidget_2)
        self.doubleSpinBoxObjContrastImage.setEnabled(False)
        self.doubleSpinBoxObjContrastImage.setSingleStep(0.01)
        self.doubleSpinBoxObjContrastImage.setObjectName("doubleSpinBoxObjContrastImage")
        self.gridLayoutObjectProperties.addWidget(self.doubleSpinBoxObjContrastImage, 6, 3, 1, 1)
        self.labelObjWidth = QLabel(self.gridLayoutWidget_2)
        self.labelObjWidth.setObjectName("labelObjWidth")
        self.gridLayoutObjectProperties.addWidget(self.labelObjWidth, 3, 0, 1, 1)
        self.doubleSpinBoxObjBrightnessImage = QDoubleSpinBox(self.gridLayoutWidget_2)
        self.doubleSpinBoxObjBrightnessImage.setEnabled(False)
        self.doubleSpinBoxObjBrightnessImage.setSingleStep(0.01)
        self.doubleSpinBoxObjBrightnessImage.setObjectName("doubleSpinBoxObjBrightnessImage")
        self.gridLayoutObjectProperties.addWidget(self.doubleSpinBoxObjBrightnessImage, 6, 1, 1, 1)
        self.labelObjBinarizeImage = QLabel(self.gridLayoutWidget_2)
        self.labelObjBinarizeImage.setObjectName("labelObjBinarizeImage")
        self.gridLayoutObjectProperties.addWidget(self.labelObjBinarizeImage, 5, 0, 1, 1)
        self.checkBoxObjBordersViewPreview = QCheckBox(self.gridLayoutWidget_2)
        self.checkBoxObjBordersViewPreview.setObjectName("checkBoxObjBordersViewPreview")
        self.gridLayoutObjectProperties.addWidget(self.checkBoxObjBordersViewPreview, 4, 0, 1, 2)
        self.comboBoxObjBinarizeImage = QComboBox(self.gridLayoutWidget_2)
        self.comboBoxObjBinarizeImage.setObjectName("comboBoxObjBinarizeImage")
        self.comboBoxObjBinarizeImage.addItem("")
        self.comboBoxObjBinarizeImage.addItem("")
        self.gridLayoutObjectProperties.addWidget(self.comboBoxObjBinarizeImage, 5, 1, 1, 1)
        self.labelObjBrightnessImage = QLabel(self.gridLayoutWidget_2)
        self.labelObjBrightnessImage.setEnabled(False)
        self.labelObjBrightnessImage.setObjectName("labelObjBrightnessImage")
        self.gridLayoutObjectProperties.addWidget(self.labelObjBrightnessImage, 6, 0, 1, 1)
        self.labelObjName = QLabel(self.gridLayoutWidget_2)
        self.labelObjName.setObjectName("labelObjName")
        self.gridLayoutObjectProperties.addWidget(self.labelObjName, 0, 0, 1, 1)
        self.labelObjContrastImage = QLabel(self.gridLayoutWidget_2)
        self.labelObjContrastImage.setEnabled(False)
        self.labelObjContrastImage.setObjectName("labelObjContrastImage")
        self.gridLayoutObjectProperties.addWidget(self.labelObjContrastImage, 6, 2, 1, 1)
        self.labelObjHeight = QLabel(self.gridLayoutWidget_2)
        self.labelObjHeight.setObjectName("labelObjHeight")
        self.gridLayoutObjectProperties.addWidget(self.labelObjHeight, 2, 0, 1, 1)
        self.spinBoxObjHeightTollerance = QSpinBox(self.gridLayoutWidget_2)
        self.spinBoxObjHeightTollerance.setMaximum(999999)
        self.spinBoxObjHeightTollerance.setObjectName("spinBoxObjHeightTollerance")
        self.gridLayoutObjectProperties.addWidget(self.spinBoxObjHeightTollerance, 2, 3, 1, 1)
        self.labelObjHeightTollerance = QLabel(self.gridLayoutWidget_2)
        self.labelObjHeightTollerance.setObjectName("labelObjHeightTollerance")
        self.gridLayoutObjectProperties.addWidget(self.labelObjHeightTollerance, 2, 2, 1, 1)
        self.textEditObjDescription = QTextEdit(self.gridLayoutWidget_2)
        self.textEditObjDescription.setLineWrapMode(QTextEdit.NoWrap)
        self.textEditObjDescription.setObjectName("textEditObjDescription")
        self.gridLayoutObjectProperties.addWidget(self.textEditObjDescription, 1, 1, 1, 3)
        self.labelObjDescription = QLabel(self.gridLayoutWidget_2)
        self.labelObjDescription.setObjectName("labelObjDescription")
        self.gridLayoutObjectProperties.addWidget(self.labelObjDescription, 1, 0, 1, 1)
        self.tabWidget.addTab(self.tabObject, "")
        self.tabLabel = QWidget()
        self.tabLabel.setObjectName("tabLabel")
        self.gridLayoutWidget = QWidget(self.tabLabel)
        self.gridLayoutWidget.setGeometry(QRect(10, 20, 301, 211))
        self.gridLayoutWidget.setObjectName("gridLayoutWidget")
        self.gridLayoutLabelProperties = QGridLayout(self.gridLayoutWidget)
        self.gridLayoutLabelProperties.setMargin(0)
        self.gridLayoutLabelProperties.setObjectName("gridLayoutLabelProperties")
        self.doubleSpinBoxObjContrastLabel = QDoubleSpinBox(self.gridLayoutWidget)
        self.doubleSpinBoxObjContrastLabel.setEnabled(False)
        self.doubleSpinBoxObjContrastLabel.setSingleStep(0.01)
        self.doubleSpinBoxObjContrastLabel.setObjectName("doubleSpinBoxObjContrastLabel")
        self.gridLayoutLabelProperties.addWidget(self.doubleSpinBoxObjContrastLabel, 3, 3, 1, 1)
        self.labelObjContrastLabel = QLabel(self.gridLayoutWidget)
        self.labelObjContrastLabel.setEnabled(False)
        self.labelObjContrastLabel.setObjectName("labelObjContrastLabel")
        self.gridLayoutLabelProperties.addWidget(self.labelObjContrastLabel, 3, 2, 1, 1)
        self.labelObjBinarizeLabel = QLabel(self.gridLayoutWidget)
        self.labelObjBinarizeLabel.setObjectName("labelObjBinarizeLabel")
        self.gridLayoutLabelProperties.addWidget(self.labelObjBinarizeLabel, 2, 0, 1, 1)
        self.labelObjBrightnessLabel = QLabel(self.gridLayoutWidget)
        self.labelObjBrightnessLabel.setEnabled(False)
        self.labelObjBrightnessLabel.setObjectName("labelObjBrightnessLabel")
        self.gridLayoutLabelProperties.addWidget(self.labelObjBrightnessLabel, 3, 0, 1, 1)
        self.comboBoxObjBinarizeLabel = QComboBox(self.gridLayoutWidget)
        self.comboBoxObjBinarizeLabel.setObjectName("comboBoxObjBinarizeLabel")
        self.comboBoxObjBinarizeLabel.addItem("")
        self.comboBoxObjBinarizeLabel.addItem("")
        self.gridLayoutLabelProperties.addWidget(self.comboBoxObjBinarizeLabel, 2, 1, 1, 1)
        self.doubleSpinBoxObjBrightnessLabel = QDoubleSpinBox(self.gridLayoutWidget)
        self.doubleSpinBoxObjBrightnessLabel.setEnabled(False)
        self.doubleSpinBoxObjBrightnessLabel.setSingleStep(0.01)
        self.doubleSpinBoxObjBrightnessLabel.setObjectName("doubleSpinBoxObjBrightnessLabel")
        self.gridLayoutLabelProperties.addWidget(self.doubleSpinBoxObjBrightnessLabel, 3, 1, 1, 1)
        self.labelObjLabelText = QLabel(self.gridLayoutWidget)
        self.labelObjLabelText.setObjectName("labelObjLabelText")
        self.gridLayoutLabelProperties.addWidget(self.labelObjLabelText, 0, 0, 1, 1)
        self.lineEditObjOcrWhiteList = QLineEdit(self.gridLayoutWidget)
        self.lineEditObjOcrWhiteList.setObjectName("lineEditObjOcrWhiteList")
        self.gridLayoutLabelProperties.addWidget(self.lineEditObjOcrWhiteList, 4, 1, 1, 3)
        self.labelObjOcrWhiteList = QLabel(self.gridLayoutWidget)
        self.labelObjOcrWhiteList.setObjectName("labelObjOcrWhiteList")
        self.gridLayoutLabelProperties.addWidget(self.labelObjOcrWhiteList, 4, 0, 1, 1)
        self.labelObjOcrLanguage = QLabel(self.gridLayoutWidget)
        self.labelObjOcrLanguage.setObjectName("labelObjOcrLanguage")
        self.gridLayoutLabelProperties.addWidget(self.labelObjOcrLanguage, 5, 0, 1, 1)
        self.lineEditObjOcrLanguage = QLineEdit(self.gridLayoutWidget)
        self.lineEditObjOcrLanguage.setObjectName("lineEditObjOcrLanguage")
        self.gridLayoutLabelProperties.addWidget(self.lineEditObjOcrLanguage, 5, 1, 1, 2)
        self.checkBoxObjBinarizeLabel = QCheckBox(self.gridLayoutWidget)
        self.checkBoxObjBinarizeLabel.setEnabled(False)
        self.checkBoxObjBinarizeLabel.setChecked(True)
        self.checkBoxObjBinarizeLabel.setTristate(False)
        self.checkBoxObjBinarizeLabel.setObjectName("checkBoxObjBinarizeLabel")
        self.gridLayoutLabelProperties.addWidget(self.checkBoxObjBinarizeLabel, 2, 2, 1, 2)
        self.pushButtonObjLabelLookup = QPushButton(self.gridLayoutWidget)
        self.pushButtonObjLabelLookup.setObjectName("pushButtonObjLabelLookup")
        self.gridLayoutLabelProperties.addWidget(self.pushButtonObjLabelLookup, 1, 3, 1, 1)
        self.textEdit = QTextEdit(self.gridLayoutWidget)
        self.textEdit.setObjectName("textEdit")
        self.textEdit.setLineWrapMode(QTextEdit.NoWrap)
        self.gridLayoutLabelProperties.addWidget(self.textEdit, 0, 1, 1, 3)
        self.tabWidget.addTab(self.tabLabel, "")
        self.tab_3 = QWidget()
        self.tab_3.setObjectName("tab_3")
        self.gridLayoutWidget_3 = QWidget(self.tab_3)
        self.gridLayoutWidget_3.setGeometry(QRect(10, 20, 301, 261))
        self.gridLayoutWidget_3.setObjectName("gridLayoutWidget_3")
        self.gridLayoutExtraActions = QGridLayout(self.gridLayoutWidget_3)
        self.gridLayoutExtraActions.setMargin(0)
        self.gridLayoutExtraActions.setObjectName("gridLayoutExtraActions")
        self.radioButtonObjClick = QRadioButton(self.gridLayoutWidget_3)
        self.radioButtonObjClick.setChecked(True)
        self.radioButtonObjClick.setObjectName("radioButtonObjClick")
        self.gridLayoutExtraActions.addWidget(self.radioButtonObjClick, 1, 0, 1, 1)
        self.spinBoxObjRegionY = QSpinBox(self.gridLayoutWidget_3)
        self.spinBoxObjRegionY.setEnabled(False)
        self.spinBoxObjRegionY.setMinimum(-999999)
        self.spinBoxObjRegionY.setMaximum(999999)
        self.spinBoxObjRegionY.setObjectName("spinBoxObjRegionY")
        self.gridLayoutExtraActions.addWidget(self.spinBoxObjRegionY, 7, 3, 1, 1)
        self.labelObjWarningPerfData = QLabel(self.gridLayoutWidget_3)
        self.labelObjWarningPerfData.setEnabled(False)
        self.labelObjWarningPerfData.setObjectName("labelObjWarningPerfData")
        self.gridLayoutExtraActions.addWidget(self.labelObjWarningPerfData, 5, 0, 1, 1)
        self.spinBoxObjRegionHeight = QSpinBox(self.gridLayoutWidget_3)
        self.spinBoxObjRegionHeight.setEnabled(False)
        self.spinBoxObjRegionHeight.setMaximum(999999)
        self.spinBoxObjRegionHeight.setObjectName("spinBoxObjRegionHeight")
        self.gridLayoutExtraActions.addWidget(self.spinBoxObjRegionHeight, 8, 1, 1, 1)
        self.spinBoxObjCriticalPerfData = QSpinBox(self.gridLayoutWidget_3)
        self.spinBoxObjCriticalPerfData.setEnabled(False)
        self.spinBoxObjCriticalPerfData.setMaximum(3600)
        self.spinBoxObjCriticalPerfData.setObjectName("spinBoxObjCriticalPerfData")
        self.gridLayoutExtraActions.addWidget(self.spinBoxObjCriticalPerfData, 5, 3, 1, 1)
        self.checkBoxObjUseMouse = QCheckBox(self.gridLayoutWidget_3)
        self.checkBoxObjUseMouse.setChecked(True)
        self.checkBoxObjUseMouse.setObjectName("checkBoxObjUseMouse")
        self.gridLayoutExtraActions.addWidget(self.checkBoxObjUseMouse, 0, 0, 1, 2)
        self.checkBoxObjUseKeyboard = QCheckBox(self.gridLayoutWidget_3)
        self.checkBoxObjUseKeyboard.setObjectName("checkBoxObjUseKeyboard")
        self.gridLayoutExtraActions.addWidget(self.checkBoxObjUseKeyboard, 2, 0, 1, 2)
        self.spinBoxObjRegionX = QSpinBox(self.gridLayoutWidget_3)
        self.spinBoxObjRegionX.setEnabled(False)
        self.spinBoxObjRegionX.setMinimum(-999999)
        self.spinBoxObjRegionX.setMaximum(999999)
        self.spinBoxObjRegionX.setObjectName("spinBoxObjRegionX")
        self.gridLayoutExtraActions.addWidget(self.spinBoxObjRegionX, 7, 1, 1, 1)
        self.spinBoxObjRegionWidth = QSpinBox(self.gridLayoutWidget_3)
        self.spinBoxObjRegionWidth.setEnabled(False)
        self.spinBoxObjRegionWidth.setMaximum(999999)
        self.spinBoxObjRegionWidth.setObjectName("spinBoxObjRegionWidth")
        self.gridLayoutExtraActions.addWidget(self.spinBoxObjRegionWidth, 8, 3, 1, 1)
        self.labelObjRegionY = QLabel(self.gridLayoutWidget_3)
        self.labelObjRegionY.setEnabled(False)
        self.labelObjRegionY.setObjectName("labelObjRegionY")
        self.gridLayoutExtraActions.addWidget(self.labelObjRegionY, 7, 2, 1, 1)
        self.spinBoxObjWarningPerfData = QSpinBox(self.gridLayoutWidget_3)
        self.spinBoxObjWarningPerfData.setEnabled(False)
        self.spinBoxObjWarningPerfData.setMaximum(3600)
        self.spinBoxObjWarningPerfData.setObjectName("spinBoxObjWarningPerfData")
        self.gridLayoutExtraActions.addWidget(self.spinBoxObjWarningPerfData, 5, 1, 1, 1)
        self.pushButtonObjBindRegion = QPushButton(self.gridLayoutWidget_3)
        self.pushButtonObjBindRegion.setObjectName("pushButtonObjBindRegion")
        self.gridLayoutExtraActions.addWidget(self.pushButtonObjBindRegion, 6, 0, 1, 1)
        self.labelObjRegionWidth = QLabel(self.gridLayoutWidget_3)
        self.labelObjRegionWidth.setEnabled(False)
        self.labelObjRegionWidth.setObjectName("labelObjRegionWidth")
        self.gridLayoutExtraActions.addWidget(self.labelObjRegionWidth, 8, 2, 1, 1)
        self.lineEditObjInsertText = QLineEdit(self.gridLayoutWidget_3)
        self.lineEditObjInsertText.setEnabled(False)
        self.lineEditObjInsertText.setObjectName("lineEditObjInsertText")
        self.gridLayoutExtraActions.addWidget(self.lineEditObjInsertText, 3, 1, 1, 3)
        self.radioButtonObjDoubleClick = QRadioButton(self.gridLayoutWidget_3)
        self.radioButtonObjDoubleClick.setObjectName("radioButtonObjDoubleClick")
        self.gridLayoutExtraActions.addWidget(self.radioButtonObjDoubleClick, 1, 1, 1, 2)
        self.labelObjRegionX = QLabel(self.gridLayoutWidget_3)
        self.labelObjRegionX.setEnabled(False)
        self.labelObjRegionX.setObjectName("labelObjRegionX")
        self.gridLayoutExtraActions.addWidget(self.labelObjRegionX, 7, 0, 1, 1)
        self.checkBoxObjEnablePerfData = QCheckBox(self.gridLayoutWidget_3)
        self.checkBoxObjEnablePerfData.setObjectName("checkBoxObjEnablePerfData")
        self.gridLayoutExtraActions.addWidget(self.checkBoxObjEnablePerfData, 4, 0, 1, 4)
        self.labelObjCriticalPerfData = QLabel(self.gridLayoutWidget_3)
        self.labelObjCriticalPerfData.setEnabled(False)
        self.labelObjCriticalPerfData.setObjectName("labelObjCriticalPerfData")
        self.gridLayoutExtraActions.addWidget(self.labelObjCriticalPerfData, 5, 2, 1, 1)
        self.labelObjInsertText = QLabel(self.gridLayoutWidget_3)
        self.labelObjInsertText.setEnabled(False)
        self.labelObjInsertText.setObjectName("labelObjInsertText")
        self.gridLayoutExtraActions.addWidget(self.labelObjInsertText, 3, 0, 1, 1)
        self.labelObjRegionHeight = QLabel(self.gridLayoutWidget_3)
        self.labelObjRegionHeight.setEnabled(False)
        self.labelObjRegionHeight.setObjectName("labelObjRegionHeight")
        self.gridLayoutExtraActions.addWidget(self.labelObjRegionHeight, 8, 0, 1, 1)
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

        self.setWindowTitle("self")
        self.checkBoxObjTollerancePreview.setText("Tollerance Preview")
        self.labelObjWidthTollerance.setText("Tollerance")
        self.checkBoxObjBinarizeImage.setText("Binarize Preview")
        self.labelObjWidth.setText("Width")
        self.labelObjBinarizeImage.setText("Binarize Image")
        self.checkBoxObjBordersViewPreview.setText("Borders View Preview")
        self.comboBoxObjBinarizeImage.setItemText(0, "No")
        self.comboBoxObjBinarizeImage.setItemText(1, "Yes")
        self.labelObjBrightnessImage.setText("Brightness")
        self.labelObjName.setText("Name")
        self.labelObjContrastImage.setText("Contrast")
        self.labelObjHeight.setText("Height")
        self.labelObjHeightTollerance.setText("Tollerance")
        self.labelObjDescription.setText("Description")
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tabObject), "Object Properties")
        self.labelObjContrastLabel.setText("Contrast")
        self.labelObjBinarizeLabel.setText("Binarize Label")
        self.labelObjBrightnessLabel.setText("Brightness")
        self.comboBoxObjBinarizeLabel.setItemText(0, "No")
        self.comboBoxObjBinarizeLabel.setItemText(1, "Yes")
        self.labelObjLabelText.setText("Text Value")
        self.labelObjOcrWhiteList.setText("Ocr White List")
        self.labelObjOcrLanguage.setText("Ocr Language")
        self.checkBoxObjBinarizeLabel.setText("Binarize Preview")
        self.pushButtonObjLabelLookup.setText("Lookup")
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tabLabel), "Text Properties")
        self.radioButtonObjClick.setText("Click")
        self.labelObjWarningPerfData.setText("Warning")
        self.checkBoxObjUseMouse.setText("Use Mouse")
        self.checkBoxObjUseKeyboard.setText("Use Keyboard")
        self.labelObjRegionY.setText("Region y")
        self.pushButtonObjBindRegion.setText("Bind Region")
        self.labelObjRegionWidth.setText("Region Width")
        self.radioButtonObjDoubleClick.setText("Double Click")
        self.labelObjRegionX.setText("Region x")
        self.checkBoxObjEnablePerfData.setText("Enable Performance Data")
        self.labelObjCriticalPerfData.setText("Critical")
        self.labelObjInsertText.setText("Insert Text")
        self.labelObjRegionHeight.setText("Region Height")
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_3), "Extra Actions")
        self.pushButtonApply.setText("Apply")
        self.pushButtonReset.setText("Reset")
        self.pushButtonTest.setText("Test")

        self.setGeometry(300, 300, 339, 376)
        #self.setGeometry(300, 300, 600, self.controlOffsetY + 200)
        self.setFixedSize(self.size())

        self.setWindowTitle('Application Text Properties')
        #self.setWindowFlags(Qt.Window | Qt.WindowMinimizeButtonHint)
        #self.setWindowFlags(Qt.FramelessWindowHint)
        self.setWindowFlags(Qt.WindowCloseButtonHint | Qt.WindowStaysOnTopHint)

        self.connect(self.tabWidget, SIGNAL("currentChanged(int)"), self, SLOT("TabChangedEvent(int)"))
        self.connect(self.lineEditObjName, SIGNAL('textChanged(QString)'), self.LineEditObjNameEvent)
        self.connect(self.textEditObjDescription, SIGNAL('textChanged()'), self.TextEditObjDescriptionEvent)
        self.connect(self.spinBoxObjHeight, SIGNAL('valueChanged(int)'), self.SpinBoxObjHeightChangeEvent)
        self.connect(self.spinBoxObjWidth, SIGNAL('valueChanged(int)'), self.SpinBoxObjWidthChangeEvent)
        self.connect(self.spinBoxObjHeightTollerance, SIGNAL('valueChanged(int)'), self.SpinBoxObjHeightTolleranceChangeEvent)
        self.connect(self.spinBoxObjWidthTollerance, SIGNAL('valueChanged(int)'), self.SpinBoxObjWidthTolleranceChangeEvent)
        self.connect(self.checkBoxObjBordersViewPreview, SIGNAL('stateChanged(int)'), self.CheckBoxObjBordersViewPreviewEvent)
        self.connect(self.checkBoxObjTollerancePreview, SIGNAL('stateChanged(int)'), self.CheckBoxObjTollerancePreviewEvent)
        self.comboBoxObjBinarizeImage.activated.connect(self.ComboBoxObjBinarizeImageEvent)
        self.connect(self.checkBoxObjBinarizeImage, SIGNAL('stateChanged(int)'), self.CheckBoxObjBinarizeImageEvent)
        self.connect(self.doubleSpinBoxObjBrightnessImage, SIGNAL('valueChanged(double)'), self.DoubleSpinBoxObjBrightnessImageEvent)
        self.connect(self.doubleSpinBoxObjContrastImage, SIGNAL('valueChanged(double)'), self.DoubleSpinBoxObjContrastImageEvent)
        self.connect(self.textEdit, SIGNAL('textChanged()'), self.LineEditObjLabelTextEvent)
        self.comboBoxObjBinarizeLabel.activated.connect(self.ComboBoxObjBinarizeLabelEvent)
        self.connect(self.checkBoxObjBinarizeLabel, SIGNAL('stateChanged(int)'), self.CheckBoxObjBinarizeLabelEvent)
        self.connect(self.doubleSpinBoxObjBrightnessLabel, SIGNAL('valueChanged(double)'), self.DoubleSpinBoxObjBrightnessLabelEvent)
        self.connect(self.doubleSpinBoxObjContrastLabel, SIGNAL('valueChanged(double)'), self.DoubleSpinBoxObjContrastLabelEvent)
        self.connect(self.lineEditObjOcrWhiteList, SIGNAL('textChanged(QString)'), self.LineEditObjOcrWhiteListEvent)
        self.connect(self.lineEditObjOcrLanguage, SIGNAL('textChanged(QString)'), self.LineEditObjOcrLanguageEvent)
        self.connect(self.checkBoxObjUseMouse, SIGNAL('stateChanged(int)'), self.CheckBoxObjUseMouseEvent)
        #self.connect(self.radioButtonObjClick, SIGNAL('stateChanged(int)'), self.RadioButtonObjClickEvent)
        #self.connect(self.radioButtonObjDoubleClick, SIGNAL('stateChanged(int)'), self.RadioButtonObjDoubleClickEvent)
        self.connect(self.checkBoxObjUseKeyboard, SIGNAL('stateChanged(int)'), self.CheckBoxObjUseKeyboardEvent)
        self.connect(self.lineEditObjInsertText, SIGNAL('textChanged(QString)'), self.LineEditObjInsertTextEvent)
        self.connect(self.pushButtonObjLabelLookup, SIGNAL('clicked()'), self.PushButtonObjLabelLookupEvent)
        self.connect(self.checkBoxObjEnablePerfData, SIGNAL('stateChanged(int)'), self.CheckBoxObjEnablePerfDataEvent)
        self.connect(self.spinBoxObjWarningPerfData, SIGNAL('valueChanged(int)'), self.SpinBoxObjWarningPerfDataEvent)
        self.connect(self.spinBoxObjCriticalPerfData, SIGNAL('valueChanged(int)'), self.SpinBoxObjCriticalPerfDataEvent)
        self.connect(self.pushButtonObjBindRegion, SIGNAL("clicked()"), self.PushButtonObjBindRegionEvent)
        self.connect(self.spinBoxObjRegionX, SIGNAL('valueChanged(int)'), self.SpinBoxObjRegionXEvent)
        self.connect(self.spinBoxObjRegionY, SIGNAL('valueChanged(int)'), self.SpinBoxObjRegionYEvent)
        self.connect(self.spinBoxObjRegionHeight, SIGNAL('valueChanged(int)'), self.SpinBoxObjRegionHeightEvent)
        self.connect(self.spinBoxObjRegionWidth, SIGNAL('valueChanged(int)'), self.SpinBoxObjRegionWidthEvent)
        self.connect(self.pushButtonApply, SIGNAL("clicked()"), self.PushButtonApplyEvent)
        self.connect(self.pushButtonReset, SIGNAL("clicked()"), self.PushButtonResetEvent)
        self.connect(self.pushButtonTest, SIGNAL("clicked()"), self.PushButtonTestEvent)

        self.UpdateControls()

        self.show()

    @pyqtSlot(int)
    def TabChangedEvent(self, tabIndex):
        self.RadioButtonObjClickEvent()
        self.RadioButtonObjDoubleClickEvent()
        self.ComboBoxObjBinarizeImageEvent()
        self.ComboBoxObjBinarizeLabelEvent()
        if tabIndex != 0:
            self.checkBoxObjTollerancePreview.setChecked(False)

    def LineEditObjNameEvent(self):
        self.lineEditObjName.setText(self.lineEditObjName.text().replace(" ","_"))
        self.caller.AlexaAppObjects[self.objectIndex].Name = self.lineEditObjName.text()

    def TextEditObjDescriptionEvent(self):
        self.caller.AlexaAppObjects[self.objectIndex].Description = self.textEditObjDescription.toPlainText()

    def CheckBoxObjBordersViewPreviewEvent(self):
        if self.checkBoxObjBordersViewPreview.isChecked() is True:
            if self.caller.AlexaAppObjects[self.objectIndex].ImageBinarize is True:
                self.checkBoxObjBinarizeImage.setChecked(False)
            self.caller.DoCanny()
        else:
            self.caller.pixmap.load(self.plug_path + os.sep + 'tmp' + os.sep + 'screenshot.png')
        self.caller.update()

    def CheckBoxObjTollerancePreviewEvent(self):
        if self.checkBoxObjTollerancePreview.isChecked() is True:
            self.caller.TollerancePreview = True
        else:
            self.caller.TollerancePreview = False
        self.caller.update()

    def SpinBoxObjHeightChangeEvent(self):
        self.caller.AlexaAppObjects[self.objectIndex].ObjH = self.spinBoxObjHeight.value()
        self.caller.update()

    def SpinBoxObjWidthChangeEvent(self):
        self.caller.AlexaAppObjects[self.objectIndex].ObjW = self.spinBoxObjWidth.value()
        self.caller.update()

    def SpinBoxObjHeightTolleranceChangeEvent(self):
        self.caller.AlexaAppObjects[self.objectIndex].HeightTollerance = self.spinBoxObjHeightTollerance.value()
        self.caller.update()

    def SpinBoxObjWidthTolleranceChangeEvent(self):
        self.caller.AlexaAppObjects[self.objectIndex].WidthTollerance = self.spinBoxObjWidthTollerance.value()
        self.caller.update()

    def ComboBoxObjBinarizeImageEvent(self):
        if self.comboBoxObjBinarizeImage.currentText() == "Yes":
            self.checkBoxObjBinarizeImage.setEnabled(True)
            self.doubleSpinBoxObjBrightnessImage.setEnabled(True)
            self.doubleSpinBoxObjContrastImage.setEnabled(True)
            self.labelObjBrightnessImage.setEnabled(True)
            self.labelObjContrastImage.setEnabled(True)
            self.caller.AlexaAppObjects[self.objectIndex].ImageBinarize = True

            if self.checkBoxObjBinarizeImage.isChecked() == True and self.tabWidget.currentIndex () == 0:
                #self.caller.binarizeImagePreviewFlag = True
                self.checkBoxObjBordersViewPreview.setChecked(False)
                self.caller.DoBinarizeImage(self.caller.AlexaAppObjects[self.objectIndex].ImageBrightness, self.caller.AlexaAppObjects[self.objectIndex].ImageContrast)
            else:
                #self.caller.binarizeImagePreviewFlag = False
                self.caller.pixmap.load(self.plug_path + os.sep + 'tmp' + os.sep + 'screenshot.png')
        else:
            self.checkBoxObjBinarizeImage.setEnabled(False)
            self.doubleSpinBoxObjBrightnessImage.setEnabled(False)
            self.doubleSpinBoxObjContrastImage.setEnabled(False)
            self.labelObjBrightnessImage.setEnabled(False)
            self.labelObjContrastImage.setEnabled(False)
            #self.caller.binarizeImagePreviewFlag = False
            self.caller.AlexaAppObjects[self.objectIndex].ImageBinarize = False
            self.checkBoxObjBordersViewPreview.setChecked(False)
            self.caller.pixmap.load(self.plug_path + os.sep + 'tmp' + os.sep + 'screenshot.png')

        self.UpdateControls()

    def DoubleSpinBoxObjBrightnessImageEvent(self):
        if self.caller.AlexaAppObjects[self.objectIndex].ImageBinarize == True:
            self.caller.AlexaAppObjects[self.objectIndex].ImageBrightness = self.doubleSpinBoxObjBrightnessImage.value()
            if self.checkBoxObjBinarizeImage.isChecked() is True:
                self.caller.DoBinarizeImage(self.caller.AlexaAppObjects[self.objectIndex].ImageBrightness, self.caller.AlexaAppObjects[self.objectIndex].ImageContrast)

    def DoubleSpinBoxObjContrastImageEvent(self):
        if self.caller.AlexaAppObjects[self.objectIndex].ImageBinarize == True:
            self.caller.AlexaAppObjects[self.objectIndex].ImageContrast = self.doubleSpinBoxObjContrastImage.value()
            if self.checkBoxObjBinarizeImage.isChecked() is True:
                self.caller.DoBinarizeImage(self.caller.AlexaAppObjects[self.objectIndex].ImageBrightness, self.caller.AlexaAppObjects[self.objectIndex].ImageContrast)

    def CheckBoxObjBinarizeImageEvent(self):
        if self.checkBoxObjBinarizeImage.isChecked():
            self.checkBoxObjBordersViewPreview.setChecked(False)
        self.ComboBoxObjBinarizeImageEvent()

    def LineEditObjLabelTextEvent(self):
        self.caller.AlexaAppObjects[self.objectIndex].Text = self.textEdit.toPlainText()

    def ComboBoxObjBinarizeLabelEvent(self):
        if self.comboBoxObjBinarizeLabel.currentText() == "Yes":
            self.checkBoxObjBinarizeLabel.setEnabled(True)
            self.doubleSpinBoxObjBrightnessLabel.setEnabled(True)
            self.doubleSpinBoxObjContrastLabel.setEnabled(True)
            self.labelObjBrightnessLabel.setEnabled(True)
            self.labelObjContrastLabel.setEnabled(True)
            self.caller.AlexaAppObjects[self.objectIndex].Binarize = True

            if self.checkBoxObjBinarizeLabel.isChecked() == True and self.tabWidget.currentIndex () == 1:
                #self.caller.binarizeLabelPreviewFlag = True
                self.caller.DoBinarizeLabel(self.caller.AlexaAppObjects[self.objectIndex].Brightness, self.caller.AlexaAppObjects[self.objectIndex].Contrast)
                #self.caller.printLabelBorder = True
            else:
                self.caller.pixmap.load(self.plug_path + os.sep + 'tmp' + os.sep + 'screenshot.png')
                #self.caller.printLabelBorder = False
        else:
            self.checkBoxObjBinarizeLabel.setEnabled(False)
            self.doubleSpinBoxObjBrightnessLabel.setEnabled(False)
            self.doubleSpinBoxObjContrastLabel.setEnabled(False)
            self.labelObjBrightnessLabel.setEnabled(False)
            self.labelObjContrastLabel.setEnabled(False)
            #self.caller.binarizeLabelPreviewFlag = False
            self.caller.AlexaAppObjects[self.objectIndex].Binarize = False
            self.caller.pixmap.load(self.plug_path + os.sep + 'tmp' + os.sep + 'screenshot.png')
            self.caller.printLabelBorder = False

        if self.tabWidget.currentIndex () == 0:
            self.ComboBoxObjBinarizeImageEvent()

        if self.checkBoxObjBordersViewPreview.isChecked() == True and self.tabWidget.currentIndex () == 0 and self.caller.AlexaAppObjects[self.objectIndex].ImageBinarize is False:
            #print "ssdsd"
            self.caller.DoCanny()
            self.caller.update()
        elif self.checkBoxObjBordersViewPreview.isChecked() == True and self.tabWidget.currentIndex () == 0 and self.caller.AlexaAppObjects[self.objectIndex].ImageBinarize is True and self.checkBoxObjBinarizeImage.isChecked() is False:
            self.caller.DoCanny()
            self.caller.update()

        self.UpdateControls()

    def DoubleSpinBoxObjBrightnessLabelEvent(self):
        if self.caller.AlexaAppObjects[self.objectIndex].Binarize is True:
            self.caller.AlexaAppObjects[self.objectIndex].Brightness = self.doubleSpinBoxObjBrightnessLabel.value()
            if self.checkBoxObjBinarizeLabel.isChecked() is True:
                self.caller.DoBinarizeLabel(self.caller.AlexaAppObjects[self.objectIndex].Brightness, self.caller.AlexaAppObjects[self.objectIndex].Contrast)

    def DoubleSpinBoxObjContrastLabelEvent(self):
        if self.caller.AlexaAppObjects[self.objectIndex].Binarize is True:
            self.caller.AlexaAppObjects[self.objectIndex].Contrast = self.doubleSpinBoxObjContrastLabel.value()
            if self.checkBoxObjBinarizeLabel.isChecked() is True:
                self.caller.DoBinarizeLabel(self.caller.AlexaAppObjects[self.objectIndex].Brightness, self.caller.AlexaAppObjects[self.objectIndex].Contrast)

    def CheckBoxObjBinarizeLabelEvent(self):
        self.ComboBoxObjBinarizeLabelEvent()

    def LineEditObjOcrWhiteListEvent(self):
        self.caller.AlexaAppObjects[self.objectIndex].OcrWhiteList = self.lineEditObjOcrWhiteList.text()

    def LineEditObjOcrLanguageEvent(self):
        self.caller.AlexaAppObjects[self.objectIndex].Language = self.lineEditObjOcrLanguage.text()

    def CheckBoxObjUseMouseEvent(self):
        if self.caller.AlexaAppObjects[self.objectIndex].UseMouse is True and self.ResetPressed is True:
            self.checkBoxObjUseMouse.setChecked(True)
            self.radioButtonObjClick.setEnabled(True)
            self.radioButtonObjDoubleClick.setEnabled(True)
        elif self.checkBoxObjUseMouse.isChecked() is True:
            self.radioButtonObjClick.setEnabled(True)
            self.radioButtonObjDoubleClick.setEnabled(True)
            self.RadioButtonObjClickEvent()
            self.RadioButtonObjDoubleClickEvent()
            self.caller.AlexaAppObjects[self.objectIndex].UseMouse = True
        else:
            self.radioButtonObjClick.setEnabled(False)
            self.radioButtonObjDoubleClick.setEnabled(False)
            #self.caller.AlexaAppObjects[self.objectIndex].Click = False
            #self.caller.AlexaAppObjects[self.objectIndex].DoubleClick = False
            self.caller.AlexaAppObjects[self.objectIndex].UseMouse = False

        '''
        if self.caller.AlexaAppObjects[self.objectIndex].DoubleClick is True:
            self.radioButtonObjDoubleClick.setChecked(True)
        else:
            self.radioButtonObjClick.setChecked(True)
        '''
    def RadioButtonObjClickEvent(self):
        #print "ooooooooooooooooooooo oooooooooo o o o ooooooooooo"
        if self.radioButtonObjClick.isChecked():
            self.caller.AlexaAppObjects[self.objectIndex].Click = True
            self.caller.AlexaAppObjects[self.objectIndex].DoubleClick = False

    def RadioButtonObjDoubleClickEvent(self):
        #print "sdsdsdsdsdssddsddssd dfd sfd sfd sf sf"
        if self.radioButtonObjDoubleClick.isChecked():
            self.caller.AlexaAppObjects[self.objectIndex].Click = False
            self.caller.AlexaAppObjects[self.objectIndex].DoubleClick = True

    def CheckBoxObjUseKeyboardEvent(self):
        if self.checkBoxObjUseKeyboard.isChecked() is True:
            self.lineEditObjInsertText.setEnabled(True)
            self.labelObjInsertText.setEnabled(True)
        else:
            self.lineEditObjInsertText.setEnabled(False)
            self.labelObjInsertText.setEnabled(False)

    def LineEditObjInsertTextEvent(self):
        self.caller.AlexaAppObjects[self.objectIndex].InsertText = self.lineEditObjInsertText.text()

    def PushButtonObjLabelLookupEvent(self):

        #Log.Enable = True
        #Log.DebugImages = True
        #Log.Level = "debug"
        #Log.Path = "c:\\logggggg"

        Screen.ImageFromIde = self.caller.OriginalScreenshot.copy()
        self.caller.AlexaAppObjects[self.objectIndex].LookupLabelForIde = True
        self.caller.AlexaAppObjects[self.objectIndex].xFromIde = self.caller.AlexaAppObjects[self.objectIndex].RectX
        self.caller.AlexaAppObjects[self.objectIndex].yFromIde = self.caller.AlexaAppObjects[self.objectIndex].RectY
        self.caller.AlexaAppObjects[self.objectIndex].Height = self.caller.AlexaAppObjects[self.objectIndex].ObjH
        self.caller.AlexaAppObjects[self.objectIndex].Width = self.caller.AlexaAppObjects[self.objectIndex].ObjW
        #print self.caller.AlexaAppObjects[self.objectIndex].xFromIde
        #print self.caller.AlexaAppObjects[self.objectIndex].yFromIde
        #self.caller.AlexaAppObjects[self.objectIndex]._externalImage = self.caller.OriginalScreenshot.copy()
        self.caller.AlexaAppObjects[self.objectIndex].Bind(0)

        if self.caller.AlexaAppObjects[self.objectIndex].x is None and self.caller.AlexaAppObjects[self.objectIndex].y is None:
            self.message = QMessageBox.critical(self, 'Error', "The edges of the object were not found,\ntry to adjust the bind rectangle.", QMessageBox.Ok)
        else:
            self.caller.AlexaAppObjects[self.objectIndex].RectX = self.caller.AlexaAppObjects[self.objectIndex].x
            self.caller.AlexaAppObjects[self.objectIndex].RectY = self.caller.AlexaAppObjects[self.objectIndex].y

            #mettere qui controllo oggetto trovato
            self.caller.update()

            Ocr.Data = str(self.caller.jsonfile["ocrdatafolder"])

            OldOcrWhiteList = copy.deepcopy(Ocr.WhiteList)

            newChar = self.lineEditObjOcrWhiteList.text().encode('utf-8')
            #print newChar
            Ocr.WhiteList = newChar
            OldOcrLanguage = copy.deepcopy(Ocr.Language)
            Ocr.Language = str(self.lineEditObjOcrLanguage.text())

            PilImage = Image.open(self.plug_path + os.sep + 'tmp' + os.sep + 'screenshot.png')
            #self.caller.UpdateLabelOfInterest()
            left = self.caller.AlexaAppObjects[self.objectIndex].RectX
            top = self.caller.AlexaAppObjects[self.objectIndex].RectY
            width = self.caller.AlexaAppObjects[self.objectIndex].ObjW
            height = self.caller.AlexaAppObjects[self.objectIndex].ObjH
            cropped = (left, top, left + width, top + height)

            area = PilImage.crop(cropped)
            area = area.resize(((cropped[2] - cropped[0]) * 3, (cropped[3] - cropped[1]) * 3), Image.BICUBIC)

            #print "before text"
            if self.caller.AlexaAppObjects[self.objectIndex].Binarize is True:
                #print self.caller.AlexaAppObjects[self.objectIndex].Brightness, self.caller.AlexaAppObjects[self.objectIndex].Label.Contrast
                TextFound = Ocr.GetText(area, True, self.caller.AlexaAppObjects[self.objectIndex].Brightness, self.caller.AlexaAppObjects[self.objectIndex].Contrast)
            else:
                TextFound = Ocr.GetText(area)
            #print "after text"
            self.textEdit.setText(TextFound)
            '''
            self.textEdit.setText(self.textEdit.toPlainText().replace("\n", ".*"))
            self.textEdit.setText(self.textEdit.toPlainText().replace("\r", ""))
            #self.textEdit.setText(self.textEdit.toPlainText().replace(" ", ".*"))
            self.textEdit.setText(self.textEdit.toPlainText().replace(".*.*", ".*"))
            #self.textEdit.setText(self.textEdit.toPlainText().replace(".*.*.*", ".*"))
            self.textEdit.setText(self.textEdit.toPlainText().strip(".*"))
            self.textEdit.setText(self.textEdit.toPlainText().strip(" "))
            '''
            if self.textEdit.toPlainText() == "":
                self.message = QMessageBox.question(self, 'Error', "The label of the object was not found,\ntry with another label position\nor with a \"custom\" label.", QMessageBox.Ok)

            Ocr.WhiteList = copy.deepcopy(OldOcrWhiteList)
            Ocr.Language = copy.deepcopy(OldOcrLanguage)

        self.caller.AlexaAppObjects[self.objectIndex].x = None
        self.caller.AlexaAppObjects[self.objectIndex].y = None
        self.caller.AlexaAppObjects[self.objectIndex].LookupLabelForIde = False

    def CheckBoxObjEnablePerfDataEvent(self):
        if self.checkBoxObjEnablePerfData.isChecked() is True:
            self.caller.AlexaAppObjects[self.objectIndex].EnablePerfData = True
            self.labelObjWarningPerfData.setEnabled(True)
            self.spinBoxObjWarningPerfData.setEnabled(True)
            self.labelObjCriticalPerfData.setEnabled(True)
            self.spinBoxObjCriticalPerfData.setEnabled(True)
        else:
            self.caller.AlexaAppObjects[self.objectIndex].EnablePerfData = False
            self.labelObjWarningPerfData.setEnabled(False)
            self.spinBoxObjWarningPerfData.setEnabled(False)
            self.labelObjCriticalPerfData.setEnabled(False)
            self.spinBoxObjCriticalPerfData.setEnabled(False)

    def SpinBoxObjWarningPerfDataEvent(self):
        self.caller.AlexaAppObjects[self.objectIndex].PerfWarningLevel = self.spinBoxObjWarningPerfData.value()

    def SpinBoxObjCriticalPerfDataEvent(self):
        self.caller.AlexaAppObjects[self.objectIndex].PerfCriticalLevel = self.spinBoxObjCriticalPerfData.value()

    def PushButtonObjBindRegionEvent(self):
        self.caller.CropRegion = True
        self.close()

    def SpinBoxObjRegionXEvent(self):
        self.caller.AlexaAppObjects[self.objectIndex].CropRegionX = self.spinBoxObjRegionX.value()
        self.caller.update()

    def SpinBoxObjRegionYEvent(self):
        self.caller.AlexaAppObjects[self.objectIndex].CropRegionY = self.spinBoxObjRegionY.value()
        self.caller.update()

    def SpinBoxObjRegionHeightEvent(self):
        self.caller.AlexaAppObjects[self.objectIndex].CropRegionHeight = self.spinBoxObjRegionHeight.value()
        self.caller.update()

    def SpinBoxObjRegionWidthEvent(self):
        self.caller.AlexaAppObjects[self.objectIndex].CropRegionWidth = self.spinBoxObjRegionWidth.value()
        self.caller.update()

    def PushButtonApplyEvent(self):
        self.Apply()
        self.caller.AlexaAppObjectsBackup[self.objectIndex] = copy.deepcopy(self.caller.AlexaAppObjects[self.objectIndex])

    def PushButtonResetEvent(self):
        self.ResetPressed = True
        self.caller.indexFound = None
        self.caller.AlexaAppObjects[self.objectIndex] = copy.deepcopy(self.caller.AlexaAppObjectsBackup[self.objectIndex])

        #self.RadioButtonObjClickEvent()
        #self.RadioButtonObjDoubleClickEvent()
        #print self.caller.AlexaAppObjects[self.objectIndex].UseMouse
        if self.caller.AlexaAppObjects[self.objectIndex].ImageBinarize is True:
            self.comboBoxObjBinarizeImage.setCurrentIndex(1)
        else:
            self.comboBoxObjBinarizeImage.setCurrentIndex(0)
        #print self.caller.AlexaAppObjects[self.objectIndex].UseMouse
        self.checkBoxObjBinarizeImage.setChecked(True)
        if self.caller.AlexaAppObjects[self.objectIndex].Binarize is True:
            self.comboBoxObjBinarizeLabel.setCurrentIndex(1)
        else:
            self.comboBoxObjBinarizeLabel.setCurrentIndex(0)
        self.checkBoxObjBinarizeLabel.setChecked(True)
        self.ComboBoxObjBinarizeImageEvent()
        self.ComboBoxObjBinarizeLabelEvent()
        if self.caller.AlexaAppObjects[self.objectIndex].UseMouse is True:
            self.checkBoxObjUseMouse.setChecked(True)
        if self.caller.AlexaAppObjects[self.objectIndex].UseKeyboard is False:
            self.checkBoxObjUseKeyboard.setChecked(False)
        if self.caller.AlexaAppObjects[self.objectIndex].EnablePerfData is False:
            self.checkBoxObjEnablePerfData.setChecked(False)
        self.caller.update()
        self.UpdateControls()
        self.ResetPressed = False

    def PushButtonTestEvent(self):

        self.caller.AlexaAppObjects[self.objectIndex].Language = str(self.lineEditObjOcrLanguage.text())

        Ocr.Data = str(self.caller.jsonfile["ocrdatafolder"])

        OldOcrWhiteList = copy.deepcopy(Ocr.WhiteList)

        newChar = self.lineEditObjOcrWhiteList.text().encode('utf-8')
        #print newChar
        Ocr.WhiteList = newChar
        OldOcrLanguage = copy.deepcopy(Ocr.Language)
        Ocr.Language = str(self.lineEditObjOcrLanguage.text())

        Screen.ImageFromIde = self.caller.OriginalScreenshot.copy()
        #self.caller.AlexaAppObjects[self.objectIndex]._externalImage = self.caller.OriginalScreenshot.copy()
        oldX = self.caller.AlexaAppObjects[self.objectIndex].RectX
        oldY = self.caller.AlexaAppObjects[self.objectIndex].RectY
        oldW = self.caller.AlexaAppObjects[self.objectIndex].ObjW
        oldH = self.caller.AlexaAppObjects[self.objectIndex].ObjH
        self.caller.AlexaAppObjects[self.objectIndex].Height = self.caller.AlexaAppObjects[self.objectIndex].ObjH
        self.caller.AlexaAppObjects[self.objectIndex].Width = self.caller.AlexaAppObjects[self.objectIndex].ObjW

        self.caller.AlexaAppObjects[self.objectIndex].Bind(0)

        #self.caller.AlexaAppObjects[self.objectIndex].ObjW = oldW
        #self.caller.AlexaAppObjects[self.objectIndex].ObjH = oldH
        #if self.caller.AlexaAppObjects[self.objectIndex].x is not None and self.caller.AlexaAppObjects[self.objectIndex].y is not None:
        if self.caller.AlexaAppObjects[self.objectIndex].ObjX >= self.caller.AlexaAppObjects[self.objectIndex].RectX - 15 and\
        self.caller.AlexaAppObjects[self.objectIndex].ObjX <= self.caller.AlexaAppObjects[self.objectIndex].RectX + 15 and\
        self.caller.AlexaAppObjects[self.objectIndex].ObjY >= self.caller.AlexaAppObjects[self.objectIndex].RectY - 15 and\
        self.caller.AlexaAppObjects[self.objectIndex].ObjY <= self.caller.AlexaAppObjects[self.objectIndex].RectY + 15:
            #self.message = QMessageBox.question(self, 'Removal', "Are you sure ", QMessageBox.Yes | QMessageBox.No)
            self.caller.AlexaAppObjects[self.objectIndex].ObjW = self.caller.AlexaAppObjects[self.objectIndex].ObjW
            self.caller.AlexaAppObjects[self.objectIndex].ObjH = self.caller.AlexaAppObjects[self.objectIndex].ObjH
            self.caller.AlexaAppObjects[self.objectIndex].RectX = self.caller.AlexaAppObjects[self.objectIndex].ObjX
            self.caller.AlexaAppObjects[self.objectIndex].RectY = self.caller.AlexaAppObjects[self.objectIndex].ObjY
            self.caller.indexFound = self.objectIndex
        else:
            self.caller.indexFound = None
            self.caller.AlexaAppObjects[self.objectIndex].RectX = oldX
            self.caller.AlexaAppObjects[self.objectIndex].RectY = oldY
            self.caller.AlexaAppObjects[self.objectIndex].ObjW = oldW
            self.caller.AlexaAppObjects[self.objectIndex].ObjH = oldH
            self.message = QMessageBox.question(self, 'Error', "Application Object not found", QMessageBox.Ok)
        self.caller.update()
        self.UpdateControls()

        Ocr.WhiteList = copy.deepcopy(OldOcrWhiteList)
        Ocr.Language = copy.deepcopy(OldOcrLanguage)

        #self.caller.AlexaAppObjects[self.objectIndex].x = None
        #self.caller.AlexaAppObjects[self.objectIndex].y = None
        #self.caller.AlexaAppObjects[self.objectIndex].ObjX = None
        #self.caller.AlexaAppObjects[self.objectIndex].ObjY = None

    def UpdateControls(self):

        self.lineEditObjName.setText(self.caller.AlexaAppObjects[self.objectIndex].Name)

        self.textEditObjDescription.setText(self.caller.AlexaAppObjects[self.objectIndex].Description)

        self.spinBoxObjHeight.setValue(self.caller.AlexaAppObjects[self.objectIndex].ObjH)
        self.spinBoxObjHeightTollerance.setValue(self.caller.AlexaAppObjects[self.objectIndex].HeightTollerance)
        self.spinBoxObjWidth.setValue(self.caller.AlexaAppObjects[self.objectIndex].ObjW)
        self.spinBoxObjWidthTollerance.setValue(self.caller.AlexaAppObjects[self.objectIndex].WidthTollerance)

        if self.caller.AlexaAppObjects[self.objectIndex].ImageBinarize is True:
            comboIndex = self.comboBoxObjBinarizeImage.findText('Yes')
            if comboIndex != -1:
                self.comboBoxObjBinarizeImage.setCurrentIndex(comboIndex)
            self.checkBoxObjBinarizeImage.setEnabled(True)
            self.doubleSpinBoxObjBrightnessImage.setEnabled(True)
            self.doubleSpinBoxObjContrastImage.setEnabled(True)

        if self.tabWidget.currentIndex () == 0:
            self.doubleSpinBoxObjBrightnessImage.setValue(self.caller.AlexaAppObjects[self.objectIndex].ImageBrightness)
            self.doubleSpinBoxObjContrastImage.setValue(self.caller.AlexaAppObjects[self.objectIndex].ImageContrast)

        self.textEdit.setText(self.caller.AlexaAppObjects[self.objectIndex].Text)

        if self.caller.AlexaAppObjects[self.objectIndex].Binarize is True:
            comboIndex = self.comboBoxObjBinarizeLabel.findText('Yes')
            if comboIndex != -1:
                self.comboBoxObjBinarizeLabel.setCurrentIndex(comboIndex)
            self.checkBoxObjBinarizeLabel.setEnabled(True)
            self.doubleSpinBoxObjBrightnessLabel.setEnabled(True)
            self.doubleSpinBoxObjContrastLabel.setEnabled(True)

        if self.tabWidget.currentIndex() == 1:
            self.doubleSpinBoxObjBrightnessLabel.setValue(self.caller.AlexaAppObjects[self.objectIndex].Brightness)
            self.doubleSpinBoxObjContrastLabel.setValue(self.caller.AlexaAppObjects[self.objectIndex].Contrast)

        self.lineEditObjOcrWhiteList.setText(self.caller.AlexaAppObjects[self.objectIndex].OcrWhiteList)

        self.lineEditObjOcrLanguage.setText(self.caller.AlexaAppObjects[self.objectIndex].Language)

        if self.caller.AlexaAppObjects[self.objectIndex].DoubleClick is True:
            self.radioButtonObjDoubleClick.setChecked(True)
        else:
            self.radioButtonObjClick.setChecked(True)

        if self.caller.AlexaAppObjects[self.objectIndex].UseMouse is False:
            self.checkBoxObjUseMouse.setChecked(False)

        self.CheckBoxObjUseMouseEvent()

        if self.caller.AlexaAppObjects[self.objectIndex].UseKeyboard is True:
            self.lineEditObjInsertText.setEnabled(True)
            self.labelObjInsertText.setEnabled(True)
            self.checkBoxObjUseKeyboard.setChecked(True)
        self.lineEditObjInsertText.setText(self.caller.AlexaAppObjects[self.objectIndex].InsertText)

        if self.caller.AlexaAppObjects[self.objectIndex].EnablePerfData is True:
            self.checkBoxObjEnablePerfData.setChecked(True)

        self.spinBoxObjWarningPerfData.setValue(self.caller.AlexaAppObjects[self.objectIndex].PerfWarningLevel)
        self.spinBoxObjCriticalPerfData.setValue(self.caller.AlexaAppObjects[self.objectIndex].PerfCriticalLevel)

        self.spinBoxObjRegionX.setValue(self.caller.AlexaAppObjects[self.objectIndex].CropRegionX)
        self.spinBoxObjRegionY.setValue(self.caller.AlexaAppObjects[self.objectIndex].CropRegionY)
        self.spinBoxObjRegionHeight.setValue(self.caller.AlexaAppObjects[self.objectIndex].CropRegionHeight)
        self.spinBoxObjRegionWidth.setValue(self.caller.AlexaAppObjects[self.objectIndex].CropRegionWidth)

        if self.caller.AlexaAppObjects[self.objectIndex].CropRegionX != 0 and self.caller.AlexaAppObjects[self.objectIndex].CropRegionY != 0 and self.caller.AlexaAppObjects[self.objectIndex].CropRegionWidth != 0 and self.caller.AlexaAppObjects[self.objectIndex].CropRegionHeight != 0:
            self.spinBoxObjRegionX.setEnabled(True)
            self.spinBoxObjRegionY.setEnabled(True)
            self.spinBoxObjRegionHeight.setEnabled(True)
            self.spinBoxObjRegionWidth.setEnabled(True)
            self.labelObjRegionX.setEnabled(True)
            self.labelObjRegionY.setEnabled(True)
            self.labelObjRegionWidth.setEnabled(True)
            self.labelObjRegionHeight.setEnabled(True)
        else:
            self.spinBoxObjRegionX.setEnabled(False)
            self.spinBoxObjRegionY.setEnabled(False)
            self.spinBoxObjRegionHeight.setEnabled(False)
            self.spinBoxObjRegionWidth.setEnabled(False)
            self.labelObjRegionX.setEnabled(False)
            self.labelObjRegionY.setEnabled(False)
            self.labelObjRegionWidth.setEnabled(False)
            self.labelObjRegionHeight.setEnabled(False)

        self.caller.update()

        self.update()

    def keyPressEvent(self, event):

        if event.key() == Qt.Key_Escape:
            self.close()

    def closeEvent(self, event):
        self.Apply()

        self.caller.binarizeImagePreviewFlag = False
        self.caller.binarizeLabelPreviewFlag = False
        self.caller.pixmap.load(self.plug_path + os.sep + 'tmp' + os.sep + 'screenshot.png')
        #self.caller.AlexaAppObjects[self.objectIndex] = copy.deepcopy(self.caller.AlexaAppObjectsBackup[self.objectIndex])

        self.caller.DialogOpened = False
        self.caller.TollerancePreview = False
        self.caller.printLabelBorder = False
        self.caller.indexFound = None
        self.caller.update()

    def Apply(self):
        self.caller.AlexaAppObjects[self.objectIndex].Name = self.lineEditObjName.text()
        self.caller.AlexaAppObjects[self.objectIndex].Description = self.textEditObjDescription.toPlainText()
        self.caller.AlexaAppObjects[self.objectIndex].OcrWhiteList = self.lineEditObjOcrWhiteList.text()
        self.caller.AlexaAppObjects[self.objectIndex].Language = self.lineEditObjOcrLanguage.text()
        self.caller.AlexaAppObjects[self.objectIndex].Text = self.textEdit.toPlainText()

        if self.radioButtonObjClick.isChecked():
            self.caller.AlexaAppObjects[self.objectIndex].Click = True
            self.caller.AlexaAppObjects[self.objectIndex].DoubleClick = False
        else:
            self.caller.AlexaAppObjects[self.objectIndex].Click = False
            self.caller.AlexaAppObjects[self.objectIndex].DoubleClick = True

        if self.checkBoxObjUseKeyboard.isChecked() is True:
            self.caller.AlexaAppObjects[self.objectIndex].UseKeyboard = True
            self.caller.AlexaAppObjects[self.objectIndex].InsertText = self.lineEditObjInsertText.text()
        else:
            self.caller.AlexaAppObjects[self.objectIndex].UseKeyboard = False


class AppTextInRegionDialog(QWidget):

    def __init__(self, caller, objectIndex, openTabIndex):
        super(AppTextInRegionDialog, self).__init__()
        self.caller = caller
        self.plug_path = caller.plug_path
        self.objectIndex = objectIndex
        self.openTabIndex = openTabIndex
        self.caller.CropLabel = False
        self.controlOffsetY = 20
        self.controlOffsetStep = 30
        self.OkIsPressed = False
        self.ResetPressed = False

        try:
            self.caller.AlexaAppObjectsBackup = self.caller.AlexaAppImagesBackup
            self.caller.AlexaAppObjects = self.caller.AlexaAppImages
        except:
            pass

        self.initUI()

    def initUI(self):
        icon = QIcon()
        icon.addPixmap(QPixmap(self.plug_path + "/images/text-x-gettext-translation.png"), QIcon.Normal, QIcon.Off)
        self.setWindowIcon(icon)
        self.tabWidget = QTabWidget(self)
        self.tabWidget.setGeometry(QRect(5, 6, 331, 281))
        self.tabWidget.setObjectName("tabWidget")
        self.tabObject = QWidget()
        self.tabObject.setObjectName("tabObject")
        self.gridLayoutWidget_2 = QWidget(self.tabObject)
        self.gridLayoutWidget_2.setGeometry(QRect(10, 20, 301, 101))
        self.gridLayoutWidget_2.setObjectName("gridLayoutWidget_2")
        self.gridLayoutObjectProperties = QGridLayout(self.gridLayoutWidget_2)
        self.gridLayoutObjectProperties.setMargin(0)
        self.gridLayoutObjectProperties.setObjectName("gridLayoutObjectProperties")
        self.lineEditObjName = QLineEdit(self.gridLayoutWidget_2)
        self.lineEditObjName.setObjectName("lineEditObjName")
        self.gridLayoutObjectProperties.addWidget(self.lineEditObjName, 0, 1, 1, 2)
        self.labelObjName = QLabel(self.gridLayoutWidget_2)
        self.labelObjName.setObjectName("labelObjName")
        self.gridLayoutObjectProperties.addWidget(self.labelObjName, 0, 0, 1, 1)
        self.textEditObjDescription = QTextEdit(self.gridLayoutWidget_2)
        self.textEditObjDescription.setLineWrapMode(QTextEdit.NoWrap)
        self.textEditObjDescription.setObjectName("textEditObjDescription")
        self.gridLayoutObjectProperties.addWidget(self.textEditObjDescription, 1, 1, 1, 3)
        self.labelObjDescription = QLabel(self.gridLayoutWidget_2)
        self.labelObjDescription.setObjectName("labelObjDescription")
        self.gridLayoutObjectProperties.addWidget(self.labelObjDescription, 1, 0, 1, 1)
        self.tabWidget.addTab(self.tabObject, "")
        self.tabLabel = QWidget()
        self.tabLabel.setObjectName("tabLabel")
        self.gridLayoutWidget = QWidget(self.tabLabel)
        self.gridLayoutWidget.setGeometry(QRect(10, 20, 301, 206))
        self.gridLayoutWidget.setObjectName("gridLayoutWidget")
        self.gridLayoutLabelProperties = QGridLayout(self.gridLayoutWidget)
        self.gridLayoutLabelProperties.setMargin(0)
        self.gridLayoutLabelProperties.setObjectName("gridLayoutLabelProperties")
        self.doubleSpinBoxObjContrastLabel = QDoubleSpinBox(self.gridLayoutWidget)
        self.doubleSpinBoxObjContrastLabel.setEnabled(False)
        self.doubleSpinBoxObjContrastLabel.setSingleStep(0.01)
        self.doubleSpinBoxObjContrastLabel.setObjectName("doubleSpinBoxObjContrastLabel")
        self.gridLayoutLabelProperties.addWidget(self.doubleSpinBoxObjContrastLabel, 3, 3, 1, 1)
        self.labelObjContrastLabel = QLabel(self.gridLayoutWidget)
        self.labelObjContrastLabel.setEnabled(False)
        self.labelObjContrastLabel.setObjectName("labelObjContrastLabel")
        self.gridLayoutLabelProperties.addWidget(self.labelObjContrastLabel, 3, 2, 1, 1)
        self.labelObjBinarizeLabel = QLabel(self.gridLayoutWidget)
        self.labelObjBinarizeLabel.setObjectName("labelObjBinarizeLabel")
        self.gridLayoutLabelProperties.addWidget(self.labelObjBinarizeLabel, 2, 0, 1, 1)
        self.labelObjBrightnessLabel = QLabel(self.gridLayoutWidget)
        self.labelObjBrightnessLabel.setEnabled(False)
        self.labelObjBrightnessLabel.setObjectName("labelObjBrightnessLabel")
        self.gridLayoutLabelProperties.addWidget(self.labelObjBrightnessLabel, 3, 0, 1, 1)
        self.comboBoxObjBinarizeLabel = QComboBox(self.gridLayoutWidget)
        self.comboBoxObjBinarizeLabel.setObjectName("comboBoxObjBinarizeLabel")
        self.comboBoxObjBinarizeLabel.addItem("")
        self.comboBoxObjBinarizeLabel.addItem("")
        self.gridLayoutLabelProperties.addWidget(self.comboBoxObjBinarizeLabel, 2, 1, 1, 1)
        self.doubleSpinBoxObjBrightnessLabel = QDoubleSpinBox(self.gridLayoutWidget)
        self.doubleSpinBoxObjBrightnessLabel.setEnabled(False)
        self.doubleSpinBoxObjBrightnessLabel.setSingleStep(0.01)
        self.doubleSpinBoxObjBrightnessLabel.setObjectName("doubleSpinBoxObjBrightnessLabel")
        self.gridLayoutLabelProperties.addWidget(self.doubleSpinBoxObjBrightnessLabel, 3, 1, 1, 1)
        self.labelObjLabelText = QLabel(self.gridLayoutWidget)
        self.labelObjLabelText.setObjectName("labelObjLabelText")
        self.gridLayoutLabelProperties.addWidget(self.labelObjLabelText, 0, 0, 1, 1)
        self.lineEditObjOcrWhiteList = QLineEdit(self.gridLayoutWidget)
        self.lineEditObjOcrWhiteList.setObjectName("lineEditObjOcrWhiteList")
        self.gridLayoutLabelProperties.addWidget(self.lineEditObjOcrWhiteList, 4, 1, 1, 3)
        self.labelObjOcrWhiteList = QLabel(self.gridLayoutWidget)
        self.labelObjOcrWhiteList.setObjectName("labelObjOcrWhiteList")
        self.gridLayoutLabelProperties.addWidget(self.labelObjOcrWhiteList, 4, 0, 1, 1)
        self.labelObjOcrLanguage = QLabel(self.gridLayoutWidget)
        self.labelObjOcrLanguage.setObjectName("labelObjOcrLanguage")
        self.gridLayoutLabelProperties.addWidget(self.labelObjOcrLanguage, 5, 0, 1, 1)
        self.lineEditObjOcrLanguage = QLineEdit(self.gridLayoutWidget)
        self.lineEditObjOcrLanguage.setObjectName("lineEditObjOcrLanguage")
        self.gridLayoutLabelProperties.addWidget(self.lineEditObjOcrLanguage, 5, 1, 1, 2)
        self.checkBoxObjBinarizeLabel = QCheckBox(self.gridLayoutWidget)
        self.checkBoxObjBinarizeLabel.setEnabled(False)
        self.checkBoxObjBinarizeLabel.setChecked(True)
        self.checkBoxObjBinarizeLabel.setTristate(False)
        self.checkBoxObjBinarizeLabel.setObjectName("checkBoxObjBinarizeLabel")
        self.gridLayoutLabelProperties.addWidget(self.checkBoxObjBinarizeLabel, 2, 2, 1, 2)
        self.textEdit = QTextEdit(self.gridLayoutWidget)
        self.textEdit.setLineWrapMode(QTextEdit.NoWrap)
        self.textEdit.setObjectName("textEdit")
        self.gridLayoutLabelProperties.addWidget(self.textEdit, 0, 1, 1, 3)
        self.pushButtonObjLabelLookup = QPushButton(self.gridLayoutWidget)
        self.pushButtonObjLabelLookup.setObjectName("pushButtonObjLabelLookup")
        self.gridLayoutLabelProperties.addWidget(self.pushButtonObjLabelLookup, 1, 3, 1, 1)
        self.tabWidget.addTab(self.tabLabel, "")
        self.tab_3 = QWidget()
        self.tab_3.setObjectName("tab_3")
        self.gridLayoutWidget_3 = QWidget(self.tab_3)
        self.gridLayoutWidget_3.setGeometry(QRect(10, 20, 301, 171))
        self.gridLayoutWidget_3.setObjectName("gridLayoutWidget_3")
        self.gridLayoutExtraActions = QGridLayout(self.gridLayoutWidget_3)
        self.gridLayoutExtraActions.setMargin(0)
        self.gridLayoutExtraActions.setObjectName("gridLayoutExtraActions")
        self.radioButtonObjClick = QRadioButton(self.gridLayoutWidget_3)
        self.radioButtonObjClick.setChecked(True)
        self.radioButtonObjClick.setObjectName("radioButtonObjClick")
        self.gridLayoutExtraActions.addWidget(self.radioButtonObjClick, 1, 0, 1, 1)
        self.labelObjWarningPerfData = QLabel(self.gridLayoutWidget_3)
        self.labelObjWarningPerfData.setEnabled(False)
        self.labelObjWarningPerfData.setObjectName("labelObjWarningPerfData")
        self.gridLayoutExtraActions.addWidget(self.labelObjWarningPerfData, 5, 0, 1, 1)
        self.spinBoxObjCriticalPerfData = QSpinBox(self.gridLayoutWidget_3)
        self.spinBoxObjCriticalPerfData.setEnabled(False)
        self.spinBoxObjCriticalPerfData.setMaximum(3600)
        self.spinBoxObjCriticalPerfData.setObjectName("spinBoxObjCriticalPerfData")
        self.gridLayoutExtraActions.addWidget(self.spinBoxObjCriticalPerfData, 5, 3, 1, 1)
        self.checkBoxObjUseMouse = QCheckBox(self.gridLayoutWidget_3)
        self.checkBoxObjUseMouse.setChecked(True)
        self.checkBoxObjUseMouse.setObjectName("checkBoxObjUseMouse")
        self.gridLayoutExtraActions.addWidget(self.checkBoxObjUseMouse, 0, 0, 1, 2)
        self.checkBoxObjUseKeyboard = QCheckBox(self.gridLayoutWidget_3)
        self.checkBoxObjUseKeyboard.setObjectName("checkBoxObjUseKeyboard")
        self.gridLayoutExtraActions.addWidget(self.checkBoxObjUseKeyboard, 2, 0, 1, 2)
        self.spinBoxObjWarningPerfData = QSpinBox(self.gridLayoutWidget_3)
        self.spinBoxObjWarningPerfData.setEnabled(False)
        self.spinBoxObjWarningPerfData.setMaximum(3600)
        self.spinBoxObjWarningPerfData.setObjectName("spinBoxObjWarningPerfData")
        self.gridLayoutExtraActions.addWidget(self.spinBoxObjWarningPerfData, 5, 1, 1, 1)
        self.lineEditObjInsertText = QLineEdit(self.gridLayoutWidget_3)
        self.lineEditObjInsertText.setEnabled(False)
        self.lineEditObjInsertText.setObjectName("lineEditObjInsertText")
        self.gridLayoutExtraActions.addWidget(self.lineEditObjInsertText, 3, 1, 1, 3)
        self.radioButtonObjDoubleClick = QRadioButton(self.gridLayoutWidget_3)
        self.radioButtonObjDoubleClick.setObjectName("radioButtonObjDoubleClick")
        self.gridLayoutExtraActions.addWidget(self.radioButtonObjDoubleClick, 1, 1, 1, 2)
        self.checkBoxObjEnablePerfData = QCheckBox(self.gridLayoutWidget_3)
        self.checkBoxObjEnablePerfData.setObjectName("checkBoxObjEnablePerfData")
        self.gridLayoutExtraActions.addWidget(self.checkBoxObjEnablePerfData, 4, 0, 1, 4)
        self.labelObjCriticalPerfData = QLabel(self.gridLayoutWidget_3)
        self.labelObjCriticalPerfData.setEnabled(False)
        self.labelObjCriticalPerfData.setObjectName("labelObjCriticalPerfData")
        self.gridLayoutExtraActions.addWidget(self.labelObjCriticalPerfData, 5, 2, 1, 1)
        self.labelObjInsertText = QLabel(self.gridLayoutWidget_3)
        self.labelObjInsertText.setEnabled(False)
        self.labelObjInsertText.setObjectName("labelObjInsertText")
        self.gridLayoutExtraActions.addWidget(self.labelObjInsertText, 3, 0, 1, 1)
        self.tabWidget.addTab(self.tab_3, "")
        self.pushButtonApply = QPushButton(self)
        self.pushButtonApply.setGeometry(QRect(10, 300, 75, 23))
        self.pushButtonApply.setObjectName("pushButtonApply")
        self.pushButtonReset = QPushButton(self)
        self.pushButtonReset.setGeometry(QRect(100, 300, 75, 23))
        self.pushButtonReset.setObjectName("pushButtonReset")
        self.pushButtonTest = QPushButton(self)
        self.pushButtonTest.setGeometry(QRect(250, 300, 75, 23))
        self.pushButtonTest.setObjectName("pushButtonTest")
        self.line = QFrame(self)
        self.line.setGeometry(QRect(203, 291, 20, 41))
        self.line.setFrameShape(QFrame.VLine)
        self.line.setFrameShadow(QFrame.Sunken)
        self.line.setObjectName("line")

        self.tabWidget.setCurrentIndex(self.openTabIndex)

        self.setWindowTitle("self")
        self.labelObjName.setText("Name")
        self.labelObjDescription.setText("Description")
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tabObject), "General Properties")
        self.labelObjContrastLabel.setText("Contrast")
        self.labelObjBinarizeLabel.setText("Binarize Text")
        self.labelObjBrightnessLabel.setText("Brightness")
        self.comboBoxObjBinarizeLabel.setItemText(0, "No")
        self.comboBoxObjBinarizeLabel.setItemText(1, "Yes")
        self.labelObjLabelText.setText("Text Value")
        self.labelObjOcrWhiteList.setText("Ocr White List")
        self.labelObjOcrLanguage.setText("Ocr Language")
        self.checkBoxObjBinarizeLabel.setText("Binarize Preview")
        self.pushButtonObjLabelLookup.setText("Lookup")
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tabLabel), "Text Properties")
        self.radioButtonObjClick.setText("Click")
        self.labelObjWarningPerfData.setText("Warning")
        self.checkBoxObjUseMouse.setText("Use Mouse")
        self.checkBoxObjUseKeyboard.setText("Use Keyboard")
        self.radioButtonObjDoubleClick.setText("Double Click")
        self.checkBoxObjEnablePerfData.setText("Enable Perselfance Data")
        self.labelObjCriticalPerfData.setText("Critical")
        self.labelObjInsertText.setText("Insert Text")
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_3), "Extra Actions")
        self.pushButtonApply.setText("Apply")
        self.pushButtonReset.setText("Reset")
        self.pushButtonTest.setText("Test")

        self.setGeometry(300, 300, 339, 338)
        #self.setGeometry(300, 300, 600, self.controlOffsetY + 200)
        self.setFixedSize(self.size())

        self.setWindowTitle('Application Text Properties')
        #self.setWindowFlags(Qt.Window | Qt.WindowMinimizeButtonHint)
        #self.setWindowFlags(Qt.FramelessWindowHint)
        self.setWindowFlags(Qt.WindowCloseButtonHint | Qt.WindowStaysOnTopHint)


        self.connect(self.tabWidget, SIGNAL("currentChanged(int)"), self, SLOT("TabChangedEvent(int)"))
        self.connect(self.lineEditObjName, SIGNAL('textChanged(QString)'), self.LineEditObjNameEvent)
        self.connect(self.textEditObjDescription, SIGNAL('textChanged()'), self.TextEditObjDescriptionEvent)

        self.connect(self.textEdit, SIGNAL('textChanged()'), self.TextEditObjTextValueEvent)
        self.comboBoxObjBinarizeLabel.activated.connect(self.ComboBoxObjBinarizeLabelEvent)

        self.connect(self.checkBoxObjBinarizeLabel, SIGNAL('stateChanged(int)'), self.CheckBoxObjBinarizeLabelEvent)

        self.connect(self.doubleSpinBoxObjBrightnessLabel, SIGNAL('valueChanged(double)'), self.DoubleSpinBoxObjBrightnessLabelEvent)
        self.connect(self.doubleSpinBoxObjContrastLabel, SIGNAL('valueChanged(double)'), self.DoubleSpinBoxObjContrastLabelEvent)
        self.connect(self.lineEditObjOcrWhiteList, SIGNAL('textChanged(QString)'), self.LineEditObjOcrWhiteListEvent)
        self.connect(self.lineEditObjOcrLanguage, SIGNAL('textChanged(QString)'), self.LineEditObjOcrLanguageEvent)
        self.connect(self.checkBoxObjUseMouse, SIGNAL('stateChanged(int)'), self.CheckBoxObjUseMouseEvent)
        #self.connect(self.radioButtonObjClick, SIGNAL('stateChanged(int)'), self.RadioButtonObjClickEvent)
        #self.connect(self.radioButtonObjDoubleClick, SIGNAL('stateChanged(int)'), self.RadioButtonObjDoubleClickEvent)
        self.connect(self.checkBoxObjUseKeyboard, SIGNAL('stateChanged(int)'), self.CheckBoxObjUseKeyboardEvent)
        self.connect(self.lineEditObjInsertText, SIGNAL('textChanged(QString)'), self.LineEditObjInsertTextEvent)
        self.connect(self.pushButtonObjLabelLookup, SIGNAL('clicked()'), self.PushButtonObjLabelLookupEvent)
        self.connect(self.checkBoxObjEnablePerfData, SIGNAL('stateChanged(int)'), self.CheckBoxObjEnablePerfDataEvent)
        self.connect(self.spinBoxObjWarningPerfData, SIGNAL('valueChanged(int)'), self.SpinBoxObjWarningPerfDataEvent)
        self.connect(self.spinBoxObjCriticalPerfData, SIGNAL('valueChanged(int)'), self.SpinBoxObjCriticalPerfDataEvent)

        self.connect(self.pushButtonApply, SIGNAL("clicked()"), self.PushButtonApplyEvent)
        self.connect(self.pushButtonReset, SIGNAL("clicked()"), self.PushButtonResetEvent)
        self.connect(self.pushButtonTest, SIGNAL("clicked()"), self.PushButtonTestEvent)

        self.UpdateControls()

        self.show()

    @pyqtSlot(int)
    def TabChangedEvent(self, tabIndex):
        self.RadioButtonObjClickEvent()
        self.RadioButtonObjDoubleClickEvent()
        self.ComboBoxObjBinarizeLabelEvent()

    def LineEditObjNameEvent(self):
        self.lineEditObjName.setText(self.lineEditObjName.text().replace(" ","_"))
        self.caller.AlexaAppObjects[self.objectIndex].AppText.Name = self.lineEditObjName.text()

    def TextEditObjDescriptionEvent(self):
        self.caller.AlexaAppObjects[self.objectIndex].AppText.Description = self.textEditObjDescription.toPlainText()

    def TextEditObjTextValueEvent(self):
        self.caller.AlexaAppObjects[self.objectIndex].AppText.Text = self.textEdit.toPlainText()

    def ComboBoxObjBinarizeLabelEvent(self):
        if self.comboBoxObjBinarizeLabel.currentText() == "Yes":
            self.checkBoxObjBinarizeLabel.setEnabled(True)
            self.doubleSpinBoxObjBrightnessLabel.setEnabled(True)
            self.doubleSpinBoxObjContrastLabel.setEnabled(True)
            self.labelObjBrightnessLabel.setEnabled(True)
            self.labelObjContrastLabel.setEnabled(True)
            self.caller.AlexaAppObjects[self.objectIndex].AppText.Binarize = True

            if self.checkBoxObjBinarizeLabel.isChecked() == True and self.tabWidget.currentIndex () == 1:
                #self.caller.binarizeLabelPreviewFlag = True
                self.caller.DoBinarizeRegion(self.caller.AlexaAppObjects[self.objectIndex].AppText.Brightness, self.caller.AlexaAppObjects[self.objectIndex].AppText.Contrast)
            else:
                self.caller.pixmap.load(self.plug_path + os.sep + 'tmp' + os.sep + 'screenshot.png')
        else:
            self.checkBoxObjBinarizeLabel.setEnabled(False)
            self.doubleSpinBoxObjBrightnessLabel.setEnabled(False)
            self.doubleSpinBoxObjContrastLabel.setEnabled(False)
            self.labelObjBrightnessLabel.setEnabled(False)
            self.labelObjContrastLabel.setEnabled(False)
            #self.caller.binarizeLabelPreviewFlag = False
            self.caller.AlexaAppObjects[self.objectIndex].AppText.Binarize = False
            self.caller.pixmap.load(self.plug_path + os.sep + 'tmp' + os.sep + 'screenshot.png')

        self.UpdateControls()

    def DoubleSpinBoxObjBrightnessLabelEvent(self):
        if self.caller.AlexaAppObjects[self.objectIndex].AppText.Binarize is True:
            self.caller.AlexaAppObjects[self.objectIndex].AppText.Brightness = self.doubleSpinBoxObjBrightnessLabel.value()
            if self.checkBoxObjBinarizeLabel.isChecked() is True:
                self.caller.DoBinarizeRegion(self.caller.AlexaAppObjects[self.objectIndex].AppText.Brightness, self.caller.AlexaAppObjects[self.objectIndex].AppText.Contrast)

    def DoubleSpinBoxObjContrastLabelEvent(self):
        if self.caller.AlexaAppObjects[self.objectIndex].AppText.Binarize is True:
            self.caller.AlexaAppObjects[self.objectIndex].AppText.Contrast = self.doubleSpinBoxObjContrastLabel.value()
            if self.checkBoxObjBinarizeLabel.isChecked() is True:
                self.caller.DoBinarizeRegion(self.caller.AlexaAppObjects[self.objectIndex].AppText.Brightness, self.caller.AlexaAppObjects[self.objectIndex].AppText.Contrast)

    def CheckBoxObjBinarizeLabelEvent(self):
        self.ComboBoxObjBinarizeLabelEvent()

    def LineEditObjOcrWhiteListEvent(self):
        self.caller.AlexaAppObjects[self.objectIndex].AppText.OcrWhiteList = self.lineEditObjOcrWhiteList.text()

    def LineEditObjOcrLanguageEvent(self):
        self.caller.AlexaAppObjects[self.objectIndex].AppText.Language = self.lineEditObjOcrLanguage.text()

    def CheckBoxObjUseMouseEvent(self):
        if self.caller.AlexaAppObjects[self.objectIndex].AppText.UseMouse is True and self.ResetPressed is True:
            self.checkBoxObjUseMouse.setChecked(True)
            self.radioButtonObjClick.setEnabled(True)
            self.radioButtonObjDoubleClick.setEnabled(True)
        elif self.checkBoxObjUseMouse.isChecked() is True:
            self.radioButtonObjClick.setEnabled(True)
            self.radioButtonObjDoubleClick.setEnabled(True)
            self.RadioButtonObjClickEvent()
            self.RadioButtonObjDoubleClickEvent()
            self.caller.AlexaAppObjects[self.objectIndex].AppText.UseMouse = True
        else:
            self.radioButtonObjClick.setEnabled(False)
            self.radioButtonObjDoubleClick.setEnabled(False)
            #self.caller.AlexaAppObjects[self.objectIndex].AppText.Click = False
            #self.caller.AlexaAppObjects[self.objectIndex].AppText.DoubleClick = False
            self.caller.AlexaAppObjects[self.objectIndex].AppText.UseMouse = False

        '''
        if self.caller.AlexaAppObjects[self.objectIndex].AppText.DoubleClick is True:
            self.radioButtonObjDoubleClick.setChecked(True)
        else:
            self.radioButtonObjClick.setChecked(True)
        '''
    def RadioButtonObjClickEvent(self):
        #print "ooooooooooooooooooooo oooooooooo o o o ooooooooooo"
        if self.radioButtonObjClick.isChecked():
            self.caller.AlexaAppObjects[self.objectIndex].AppText.Click = True
            self.caller.AlexaAppObjects[self.objectIndex].AppText.DoubleClick = False

    def RadioButtonObjDoubleClickEvent(self):
        #print "sdsdsdsdsdssddsddssd dfd sfd sfd sf sf"
        if self.radioButtonObjDoubleClick.isChecked():
            self.caller.AlexaAppObjects[self.objectIndex].AppText.Click = False
            self.caller.AlexaAppObjects[self.objectIndex].AppText.DoubleClick = True

    def CheckBoxObjUseKeyboardEvent(self):
        if self.checkBoxObjUseKeyboard.isChecked() is True:
            self.lineEditObjInsertText.setEnabled(True)
            self.labelObjInsertText.setEnabled(True)
        else:
            self.lineEditObjInsertText.setEnabled(False)
            self.labelObjInsertText.setEnabled(False)

    def LineEditObjInsertTextEvent(self):
        self.caller.AlexaAppObjects[self.objectIndex].AppText.InsertText = self.lineEditObjInsertText.text()

    def PushButtonObjLabelLookupEvent(self):
        #Log.Enable = True
        #Log.DebugImages = True
        #Log.Level = "debug"
        #Log.Path = "c:\\logggggg"

        #Screen.ImageFromIde = self.caller.OriginalScreenshot.copy()

        Ocr.Data = str(self.caller.jsonfile["ocrdatafolder"])

        OldOcrWhiteList = copy.deepcopy(Ocr.WhiteList)

        newChar = self.lineEditObjOcrWhiteList.text().encode('utf-8')
        #print newChar
        Ocr.WhiteList = newChar
        OldOcrLanguage = copy.deepcopy(Ocr.Language)
        Ocr.Language = str(self.lineEditObjOcrLanguage.text())

        PilImage = Image.open(self.plug_path + os.sep + 'tmp' + os.sep + 'screenshot.png')

        x = self.caller.AlexaAppObjects[self.objectIndex].RectX + self.caller.AlexaAppObjects[self.objectIndex].CropRegionX
        y = self.caller.AlexaAppObjects[self.objectIndex].RectY + self.caller.AlexaAppObjects[self.objectIndex].CropRegionY
        w = self.caller.AlexaAppObjects[self.objectIndex].RectX + self.caller.AlexaAppObjects[self.objectIndex].CropRegionX + self.caller.AlexaAppObjects[self.objectIndex].CropRegionWidth
        h = self.caller.AlexaAppObjects[self.objectIndex].RectY + self.caller.AlexaAppObjects[self.objectIndex].CropRegionY + self.caller.AlexaAppObjects[self.objectIndex].CropRegionHeight
        box = (x, y, w, h)
        area = PilImage.crop(box)
        area = area.resize(((box[2] - box[0]) * 3, (box[3] - box[1]) * 3), Image.BICUBIC)

        #print "before text"
        if self.caller.AlexaAppObjects[self.objectIndex].AppText.Binarize is True:
            #print self.caller.AlexaAppObjects[self.objectIndex].AppText.Brightness, self.caller.AlexaAppObjects[self.objectIndex].AppText.Contrast
            TextFound = Ocr.GetText(area, True, self.caller.AlexaAppObjects[self.objectIndex].AppText.Brightness, self.caller.AlexaAppObjects[self.objectIndex].AppText.Contrast)
        else:
            TextFound = Ocr.GetText(area)
        #print "after text"
        self.textEdit.setText(TextFound)

        if self.textEdit.toPlainText() == "":
            self.message = QMessageBox.question(self, 'Error', "The text inside the region was not found,\ntry to adjust region size.", QMessageBox.Ok)

        Ocr.WhiteList = copy.deepcopy(OldOcrWhiteList)
        Ocr.Language = copy.deepcopy(OldOcrLanguage)

        self.caller.AlexaAppObjects[self.objectIndex].AppText.x = None
        self.caller.AlexaAppObjects[self.objectIndex].AppText.y = None

    def CheckBoxObjEnablePerfDataEvent(self):
        if self.checkBoxObjEnablePerfData.isChecked() is True:
            self.caller.AlexaAppObjects[self.objectIndex].AppText.EnablePerfData = True
            self.labelObjWarningPerfData.setEnabled(True)
            self.spinBoxObjWarningPerfData.setEnabled(True)
            self.labelObjCriticalPerfData.setEnabled(True)
            self.spinBoxObjCriticalPerfData.setEnabled(True)
        else:
            self.caller.AlexaAppObjects[self.objectIndex].AppText.EnablePerfData = False
            self.labelObjWarningPerfData.setEnabled(False)
            self.spinBoxObjWarningPerfData.setEnabled(False)
            self.labelObjCriticalPerfData.setEnabled(False)
            self.spinBoxObjCriticalPerfData.setEnabled(False)

    def SpinBoxObjWarningPerfDataEvent(self):
        self.caller.AlexaAppObjects[self.objectIndex].AppText.PerfWarningLevel = self.spinBoxObjWarningPerfData.value()

    def SpinBoxObjCriticalPerfDataEvent(self):
        self.caller.AlexaAppObjects[self.objectIndex].AppText.PerfCriticalLevel = self.spinBoxObjCriticalPerfData.value()

    def PushButtonObjBindRegionEvent(self):
        self.caller.CropRegion = True
        self.close()

    def SpinBoxObjRegionXEvent(self):
        self.caller.AlexaAppObjects[self.objectIndex].AppText.CropRegionX = self.spinBoxObjRegionX.value()
        self.caller.update()

    def SpinBoxObjRegionYEvent(self):
        self.caller.AlexaAppObjects[self.objectIndex].AppText.CropRegionY = self.spinBoxObjRegionY.value()
        self.caller.update()

    def SpinBoxObjRegionHeightEvent(self):
        self.caller.AlexaAppObjects[self.objectIndex].AppText.CropRegionHeight = self.spinBoxObjRegionHeight.value()
        self.caller.update()

    def SpinBoxObjRegionWidthEvent(self):
        self.caller.AlexaAppObjects[self.objectIndex].AppText.CropRegionWidth = self.spinBoxObjRegionWidth.value()
        self.caller.update()

    def PushButtonApplyEvent(self):
        self.Apply()
        self.caller.AlexaAppObjects[self.objectIndex].AppTextBackup = copy.deepcopy(self.caller.AlexaAppObjects[self.objectIndex].AppText)

    def PushButtonResetEvent(self):
        self.ResetPressed = True
        self.caller.indexFound = None
        self.caller.AlexaAppObjects[self.objectIndex].AppText = copy.deepcopy(self.caller.AlexaAppObjects[self.objectIndex].AppTextBackup)

        if self.caller.AlexaAppObjects[self.objectIndex].AppText.Binarize is True:
            self.comboBoxObjBinarizeLabel.setCurrentIndex(1)
        else:
            self.comboBoxObjBinarizeLabel.setCurrentIndex(0)
        self.checkBoxObjBinarizeLabel.setChecked(True)
        self.ComboBoxObjBinarizeLabelEvent()
        if self.caller.AlexaAppObjects[self.objectIndex].AppText.UseMouse is True:
            self.checkBoxObjUseMouse.setChecked(True)
        if self.caller.AlexaAppObjects[self.objectIndex].AppText.UseKeyboard is False:
            self.checkBoxObjUseKeyboard.setChecked(False)
        if self.caller.AlexaAppObjects[self.objectIndex].AppText.EnablePerfData is False:
            self.checkBoxObjEnablePerfData.setChecked(False)
        self.caller.update()
        self.UpdateControls()
        self.ResetPressed = False

    def PushButtonTestEvent(self):
        self.caller.AlexaAppObjects[self.objectIndex].AppText.x = None
        self.caller.AlexaAppObjects[self.objectIndex].AppText.y = None
        self.caller.AlexaAppObjects[self.objectIndex].AppText.Width = 0
        self.caller.AlexaAppObjects[self.objectIndex].AppText.Height = 0

        self.caller.indexFoundAppText = None

        self.caller.AlexaAppObjects[self.objectIndex].AppText.Language = str(self.lineEditObjOcrLanguage.text())

        Ocr.Data = str(self.caller.jsonfile["ocrdatafolder"])

        OldOcrWhiteList = copy.deepcopy(Ocr.WhiteList)

        newChar = self.lineEditObjOcrWhiteList.text().encode('utf-8')
        #print newChar
        Ocr.WhiteList = newChar
        OldOcrLanguage = copy.deepcopy(Ocr.Language)
        Ocr.Language = str(self.lineEditObjOcrLanguage.text())

        PilImage = Image.open(self.plug_path + os.sep + 'tmp' + os.sep + 'screenshot.png')

        x = self.caller.AlexaAppObjects[self.objectIndex].RectX + self.caller.AlexaAppObjects[self.objectIndex].CropRegionX
        y = self.caller.AlexaAppObjects[self.objectIndex].RectY + self.caller.AlexaAppObjects[self.objectIndex].CropRegionY
        w = self.caller.AlexaAppObjects[self.objectIndex].RectX + self.caller.AlexaAppObjects[self.objectIndex].CropRegionX + self.caller.AlexaAppObjects[self.objectIndex].CropRegionWidth
        h = self.caller.AlexaAppObjects[self.objectIndex].RectY + self.caller.AlexaAppObjects[self.objectIndex].CropRegionY + self.caller.AlexaAppObjects[self.objectIndex].CropRegionHeight
        box = (x, y, w, h)
        area = PilImage.crop(box)

        Screen.ImageFromIde = area.copy()

        #self.caller.AlexaAppObjects[self.objectIndex].AppText.Text = self.textEdit.toPlainText()
        self.caller.AlexaAppObjects[self.objectIndex].AppText.Bind(0)
        #self.caller.AlexaAppObjects[self.objectIndex].AppText.Width = oldW
        #self.caller.AlexaAppObjects[self.objectIndex].AppText.Height = oldH
        #if self.caller.AlexaAppObjects[self.objectIndex].AppText.x is not None and self.caller.AlexaAppObjects[self.objectIndex].AppText.y is not None:
        if self.caller.AlexaAppObjects[self.objectIndex].AppText.x is not None and self.caller.AlexaAppObjects[self.objectIndex].AppText.y is not None:
            #self.message = QMessageBox.question(self, 'Removal', "Are you sure ", QMessageBox.Yes | QMessageBox.No)
            self.caller.indexFoundAppText = self.objectIndex
        else:
            self.caller.indexFoundAppText = None
            self.message = QMessageBox.question(self, 'Error', "Application Text not found", QMessageBox.Ok)
        self.caller.update()

        Ocr.WhiteList = copy.deepcopy(OldOcrWhiteList)
        Ocr.Language = copy.deepcopy(OldOcrLanguage)

    def UpdateControls(self):

        self.lineEditObjName.setText(self.caller.AlexaAppObjects[self.objectIndex].AppText.Name)

        self.textEditObjDescription.setText(self.caller.AlexaAppObjects[self.objectIndex].AppText.Description)

        self.textEdit.setText(self.caller.AlexaAppObjects[self.objectIndex].AppText.Text)

        if self.caller.AlexaAppObjects[self.objectIndex].AppText.Binarize is True:
            comboIndex = self.comboBoxObjBinarizeLabel.findText('Yes')
            if comboIndex != -1:
                self.comboBoxObjBinarizeLabel.setCurrentIndex(comboIndex)
            self.checkBoxObjBinarizeLabel.setEnabled(True)
            self.doubleSpinBoxObjBrightnessLabel.setEnabled(True)
            self.doubleSpinBoxObjContrastLabel.setEnabled(True)

        if self.tabWidget.currentIndex() == 1:
            self.doubleSpinBoxObjBrightnessLabel.setValue(self.caller.AlexaAppObjects[self.objectIndex].AppText.Brightness)
            self.doubleSpinBoxObjContrastLabel.setValue(self.caller.AlexaAppObjects[self.objectIndex].AppText.Contrast)

        self.lineEditObjOcrWhiteList.setText(self.caller.AlexaAppObjects[self.objectIndex].AppText.OcrWhiteList)

        self.lineEditObjOcrLanguage.setText(self.caller.AlexaAppObjects[self.objectIndex].AppText.Language)

        if self.caller.AlexaAppObjects[self.objectIndex].AppText.DoubleClick is True:
            self.radioButtonObjDoubleClick.setChecked(True)
        else:
            self.radioButtonObjClick.setChecked(True)

        if self.caller.AlexaAppObjects[self.objectIndex].AppText.UseMouse is False:
            self.checkBoxObjUseMouse.setChecked(False)

        self.CheckBoxObjUseMouseEvent()

        if self.caller.AlexaAppObjects[self.objectIndex].AppText.UseKeyboard is True:
            self.lineEditObjInsertText.setEnabled(True)
            self.labelObjInsertText.setEnabled(True)
            self.checkBoxObjUseKeyboard.setChecked(True)
        self.lineEditObjInsertText.setText(self.caller.AlexaAppObjects[self.objectIndex].AppText.InsertText)

        if self.caller.AlexaAppObjects[self.objectIndex].AppText.EnablePerfData is True:
            self.checkBoxObjEnablePerfData.setChecked(True)

        self.spinBoxObjWarningPerfData.setValue(self.caller.AlexaAppObjects[self.objectIndex].AppText.PerfWarningLevel)
        self.spinBoxObjCriticalPerfData.setValue(self.caller.AlexaAppObjects[self.objectIndex].AppText.PerfCriticalLevel)

        self.caller.update()

        self.update()

    def keyPressEvent(self, event):

        if event.key() == Qt.Key_Escape:
            self.close()

    def closeEvent(self, event):
        self.Apply()

        self.caller.binarizeImagePreviewFlag = False
        self.caller.binarizeLabelPreviewFlag = False
        self.caller.pixmap.load(self.plug_path + os.sep + 'tmp' + os.sep + 'screenshot.png')
        #self.caller.AlexaAppObjects[self.objectIndex] = copy.deepcopy(self.caller.AlexaAppObjectsBackup[self.objectIndex])

        self.caller.DialogOpened = False
        self.caller.TollerancePreview = False
        self.caller.printLabelBorder = False
        self.caller.indexFound = None
        self.caller.indexFoundAppText = None
        self.caller.update()

    def Apply(self):
        self.caller.AlexaAppObjects[self.objectIndex].AppText.Name = self.lineEditObjName.text()
        self.caller.AlexaAppObjects[self.objectIndex].AppText.Description = self.textEditObjDescription.toPlainText()
        self.caller.AlexaAppObjects[self.objectIndex].AppText.OcrWhiteList = self.lineEditObjOcrWhiteList.text()
        self.caller.AlexaAppObjects[self.objectIndex].AppText.Language = self.lineEditObjOcrLanguage.text()
        self.caller.AlexaAppObjects[self.objectIndex].AppText.Text = self.textEdit.toPlainText()

        if self.radioButtonObjClick.isChecked():
            self.caller.AlexaAppObjects[self.objectIndex].AppText.Click = True
            self.caller.AlexaAppObjects[self.objectIndex].AppText.DoubleClick = False
        else:
            self.caller.AlexaAppObjects[self.objectIndex].AppText.Click = False
            self.caller.AlexaAppObjects[self.objectIndex].AppText.DoubleClick = True

        if self.checkBoxObjUseKeyboard.isChecked() is True:
            self.caller.AlexaAppObjects[self.objectIndex].AppText.UseKeyboard = True
            self.caller.AlexaAppObjects[self.objectIndex].AppText.InsertText = self.lineEditObjInsertText.text()
        else:
            self.caller.AlexaAppObjects[self.objectIndex].AppText.UseKeyboard = False