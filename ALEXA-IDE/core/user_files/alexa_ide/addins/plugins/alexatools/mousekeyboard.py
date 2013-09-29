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


class MouseKeyboard(QWidget):

    def __init__(self, plugin):
        super(MouseKeyboard, self).__init__()

        self.plugin = plugin
        self.plug_path = plugin.plug_path
        self.FirstTimeCheckBox = True

        self.initUI()

    def initUI(self):
        icon = QIcon()
        icon.addPixmap(QPixmap(self.plug_path + "/alexatools/images/input-mouse-6.png"), QIcon.Normal, QIcon.Off)
        self.setWindowIcon(icon)
        self.setWindowTitle("Al\'exa - Mouse and Keyboard")
        self.setObjectName("self")
        self.resize(368, 344)
        self.tabWidget = QTabWidget(self)
        self.tabWidget.setGeometry(QRect(10, 10, 349, 291))
        self.tabWidget.setObjectName("tabWidget")
        self.tab = QWidget()
        self.tab.setObjectName("tab")
        self.gridLayoutWidget = QWidget(self.tab)
        self.gridLayoutWidget.setGeometry(QRect(10, 28, 321, 111))
        self.gridLayoutWidget.setObjectName("gridLayoutWidget")
        self.gridLayout = QGridLayout(self.gridLayoutWidget)
        self.gridLayout.setMargin(0)
        self.gridLayout.setObjectName("gridLayout")
        self.labelClickMoveX = QLabel(self.gridLayoutWidget)
        self.labelClickMoveX.setObjectName("labelClickMoveX")
        self.gridLayout.addWidget(self.labelClickMoveX, 2, 0, 1, 1)
        self.labelClickMoveY = QLabel(self.gridLayoutWidget)
        self.labelClickMoveY.setObjectName("labelClickMoveY")
        self.gridLayout.addWidget(self.labelClickMoveY, 2, 2, 1, 1)
        self.lineEditClickMoveY = QLineEdit(self.gridLayoutWidget)
        self.lineEditClickMoveY.setObjectName("lineEditClickMoveY")
        self.gridLayout.addWidget(self.lineEditClickMoveY, 2, 3, 1, 1)
        self.lineEditClickMoveX = QLineEdit(self.gridLayoutWidget)
        self.lineEditClickMoveX.setObjectName("lineEditClickMoveX")
        self.gridLayout.addWidget(self.lineEditClickMoveX, 2, 1, 1, 1)
        self.radioButtonDoubleClick = QRadioButton(self.gridLayoutWidget)
        self.radioButtonDoubleClick.setObjectName("radioButtonDoubleClick")
        self.gridLayout.addWidget(self.radioButtonDoubleClick, 0, 2, 1, 1)
        self.comboBoxButton = QComboBox(self.gridLayoutWidget)
        self.comboBoxButton.setObjectName("comboBoxButton")
        self.comboBoxButton.addItem("")
        self.comboBoxButton.addItem("")
        self.gridLayout.addWidget(self.comboBoxButton, 1, 1, 1, 2)
        self.radioButtonClick = QRadioButton(self.gridLayoutWidget)
        self.radioButtonClick.setObjectName("radioButtonClick")
        self.gridLayout.addWidget(self.radioButtonClick, 0, 1, 1, 1)
        self.labelButton = QLabel(self.gridLayoutWidget)
        self.labelButton.setObjectName("labelButton")
        self.gridLayout.addWidget(self.labelButton, 1, 0, 1, 1)
        self.checkBoxEnableClick = QCheckBox(self.gridLayoutWidget)
        self.checkBoxEnableClick.setObjectName("checkBoxEnableClick")
        self.gridLayout.addWidget(self.checkBoxEnableClick, 0, 0, 1, 1)
        self.pushButtonClickMove = QPushButton(self.tab)
        self.pushButtonClickMove.setGeometry(QRect(10, 150, 75, 23))
        self.pushButtonClickMove.setObjectName("pushButtonClickMove")
        self.tabWidget.addTab(self.tab, "")
        self.tab_3 = QWidget()
        self.tab_3.setObjectName("tab_3")
        self.gridLayoutWidget_3 = QWidget(self.tab_3)
        self.gridLayoutWidget_3.setGeometry(QRect(10, 40, 321, 71))
        self.gridLayoutWidget_3.setObjectName("gridLayoutWidget_3")
        self.gridLayout_3 = QGridLayout(self.gridLayoutWidget_3)
        self.gridLayout_3.setMargin(0)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.labelDragStartX = QLabel(self.gridLayoutWidget_3)
        self.labelDragStartX.setFrameShape(QFrame.NoFrame)
        self.labelDragStartX.setObjectName("labelDragStartX")
        self.gridLayout_3.addWidget(self.labelDragStartX, 0, 0, 1, 1)
        self.lineEditDragStartX = QLineEdit(self.gridLayoutWidget_3)
        self.lineEditDragStartX.setObjectName("lineEditDragStartX")
        self.gridLayout_3.addWidget(self.lineEditDragStartX, 0, 1, 1, 1)
        self.lineEditDragStartY = QLineEdit(self.gridLayoutWidget_3)
        self.lineEditDragStartY.setObjectName("lineEditDragStartY")
        self.gridLayout_3.addWidget(self.lineEditDragStartY, 0, 3, 1, 1)
        self.labelDragEndX = QLabel(self.gridLayoutWidget_3)
        self.labelDragEndX.setObjectName("labelDragEndX")
        self.gridLayout_3.addWidget(self.labelDragEndX, 1, 0, 1, 1)
        self.lineEditDragEndX = QLineEdit(self.gridLayoutWidget_3)
        self.lineEditDragEndX.setObjectName("lineEditDragEndX")
        self.gridLayout_3.addWidget(self.lineEditDragEndX, 1, 1, 1, 1)
        self.labelDragEndY = QLabel(self.gridLayoutWidget_3)
        self.labelDragEndY.setObjectName("labelDragEndY")
        self.gridLayout_3.addWidget(self.labelDragEndY, 1, 2, 1, 1)
        self.labelDragStartY = QLabel(self.gridLayoutWidget_3)
        self.labelDragStartY.setObjectName("labelDragStartY")
        self.gridLayout_3.addWidget(self.labelDragStartY, 0, 2, 1, 1)
        self.lineEditDragEndY = QLineEdit(self.gridLayoutWidget_3)
        self.lineEditDragEndY.setObjectName("lineEditDragEndY")
        self.gridLayout_3.addWidget(self.lineEditDragEndY, 1, 3, 1, 1)
        self.gridLayoutWidget_4 = QWidget(self.tab_3)
        self.gridLayoutWidget_4.setGeometry(QRect(10, 190, 321, 31))
        self.gridLayoutWidget_4.setObjectName("gridLayoutWidget_4")
        self.gridLayout_4 = QGridLayout(self.gridLayoutWidget_4)
        self.gridLayout_4.setMargin(0)
        self.gridLayout_4.setObjectName("gridLayout_4")
        self.labelScrollStep = QLabel(self.gridLayoutWidget_4)
        self.labelScrollStep.setObjectName("labelScrollStep")
        self.gridLayout_4.addWidget(self.labelScrollStep, 0, 2, 1, 1)
        self.comboBoxScrollDirection = QComboBox(self.gridLayoutWidget_4)
        self.comboBoxScrollDirection.setObjectName("comboBoxScrollDirection")
        self.comboBoxScrollDirection.addItem("")
        self.comboBoxScrollDirection.addItem("")
        self.gridLayout_4.addWidget(self.comboBoxScrollDirection, 0, 1, 1, 1)
        self.labelScrollDirection = QLabel(self.gridLayoutWidget_4)
        self.labelScrollDirection.setObjectName("labelScrollDirection")
        self.gridLayout_4.addWidget(self.labelScrollDirection, 0, 0, 1, 1)
        self.spinBoxScrollStep = QSpinBox(self.gridLayoutWidget_4)
        self.spinBoxScrollStep.setMinimum(1)
        self.spinBoxScrollStep.setObjectName("spinBoxScrollStep")
        self.gridLayout_4.addWidget(self.spinBoxScrollStep, 0, 3, 1, 1)
        self.label_9 = QLabel(self.tab_3)
        self.label_9.setGeometry(QRect(10, 10, 151, 16))
        self.label_9.setObjectName("label_9")
        self.pushButtonDrag = QPushButton(self.tab_3)
        self.pushButtonDrag.setGeometry(QRect(10, 120, 75, 23))
        self.pushButtonDrag.setObjectName("pushButtonDrag")
        self.label_10 = QLabel(self.tab_3)
        self.label_10.setGeometry(QRect(10, 165, 211, 16))
        self.label_10.setObjectName("label_10")
        self.pushButtonScroll = QPushButton(self.tab_3)
        self.pushButtonScroll.setGeometry(QRect(10, 231, 75, 23))
        self.pushButtonScroll.setObjectName("pushButtonScroll")
        self.tabWidget.addTab(self.tab_3, "")
        self.tab_2 = QWidget()
        self.tab_2.setObjectName("tab_2")
        self.gridLayoutWidget_2 = QWidget(self.tab_2)
        self.gridLayoutWidget_2.setGeometry(QRect(10, 32, 321, 31))
        self.gridLayoutWidget_2.setObjectName("gridLayoutWidget_2")
        self.gridLayout_2 = QGridLayout(self.gridLayoutWidget_2)
        self.gridLayout_2.setMargin(0)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.labelText = QLabel(self.gridLayoutWidget_2)
        self.labelText.setObjectName("labelText")
        self.gridLayout_2.addWidget(self.labelText, 0, 0, 1, 1)
        self.lineEdit = QLineEdit(self.gridLayoutWidget_2)
        self.lineEdit.setObjectName("lineEdit")
        self.gridLayout_2.addWidget(self.lineEdit, 0, 1, 1, 1)
        self.pushButton_2 = QPushButton(self.tab_2)
        self.pushButton_2.setGeometry(QRect(10, 109, 75, 23))
        self.pushButton_2.setObjectName("pushButton_2")
        self.gridLayoutWidget_5 = QWidget(self.tab_2)
        self.gridLayoutWidget_5.setGeometry(QRect(10, 150, 321, 31))
        self.gridLayoutWidget_5.setObjectName("gridLayoutWidget_5")
        self.gridLayout_5 = QGridLayout(self.gridLayoutWidget_5)
        self.gridLayout_5.setMargin(0)
        self.gridLayout_5.setObjectName("gridLayout_5")
        self.lineEdit_2 = QLineEdit(self.gridLayoutWidget_5)
        self.lineEdit_2.setObjectName("lineEdit_2")
        self.gridLayout_5.addWidget(self.lineEdit_2, 0, 1, 1, 1)
        self.label = QLabel(self.gridLayoutWidget_5)
        self.label.setObjectName("label")
        self.gridLayout_5.addWidget(self.label, 0, 0, 1, 1)
        self.pushButton = QPushButton(self.tab_2)
        self.pushButton.setGeometry(QRect(10, 226, 75, 23))
        self.pushButton.setObjectName("pushButton")
        self.gridLayoutWidget_6 = QWidget(self.tab_2)
        self.gridLayoutWidget_6.setGeometry(QRect(10, 70, 261, 31))
        self.gridLayoutWidget_6.setObjectName("gridLayoutWidget_6")
        self.gridLayout_6 = QGridLayout(self.gridLayoutWidget_6)
        self.gridLayout_6.setMargin(0)
        self.gridLayout_6.setObjectName("gridLayout_6")
        self.labelDelay = QLabel(self.gridLayoutWidget_6)
        self.labelDelay.setObjectName("labelDelay")
        self.gridLayout_6.addWidget(self.labelDelay, 0, 0, 1, 1)
        self.spinBoxDelay = QSpinBox(self.gridLayoutWidget_6)
        self.spinBoxDelay.setObjectName("spinBoxDelay")
        self.gridLayout_6.addWidget(self.spinBoxDelay, 0, 1, 1, 1)
        self.checkBoxInsertDQuote = QCheckBox(self.gridLayoutWidget_6)
        self.checkBoxInsertDQuote.setChecked(True)
        self.checkBoxInsertDQuote.setObjectName("checkBoxInsertDQuote")
        self.gridLayout_6.addWidget(self.checkBoxInsertDQuote, 0, 2, 1, 1)
        self.checkBoxClipBoardDQuote = QCheckBox(self.tab_2)
        self.checkBoxClipBoardDQuote.setGeometry(QRect(10, 194, 115, 17))
        self.checkBoxClipBoardDQuote.setChecked(True)
        self.checkBoxClipBoardDQuote.setObjectName("checkBoxClipBoardDQuote")
        self.tabWidget.addTab(self.tab_2, "")
        self.pushButtonCancel = QPushButton(self)
        self.pushButtonCancel.setGeometry(QRect(13, 311, 75, 23))
        self.pushButtonCancel.setObjectName("pushButtonCancel")

        self.tabWidget.setCurrentIndex(0)

        self.labelClickMoveX.setText(" x")
        self.labelClickMoveY.setText("y")
        self.radioButtonDoubleClick.setText("Double Click")
        self.comboBoxButton.setItemText(0, "Left")
        self.comboBoxButton.setItemText(1, "Right")
        self.radioButtonClick.setText("Click")
        self.labelButton.setText("Button")
        self.checkBoxEnableClick.setText("Enable Click")
        self.pushButtonClickMove.setText("Add")
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), "Click and Move")
        self.labelDragStartX.setText("Start x")
        self.labelDragEndX.setText("End x")
        self.labelDragEndY.setText("End y")
        self.labelDragStartY.setText("Start y")
        self.labelScrollStep.setText("Step")
        self.comboBoxScrollDirection.setItemText(0, "down")
        self.comboBoxScrollDirection.setItemText(1, "up")
        self.labelScrollDirection.setText("Direction")
        self.label_9.setText("Drag and Drop")
        self.pushButtonDrag.setText("Add")
        self.label_10.setText("Scroll")
        self.pushButtonScroll.setText("Add")
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_3), "Other Mouse Actions")
        self.labelText.setText("Text to Insert")
        self.pushButton_2.setText("Add")
        self.label.setText("Put to clipboard")
        self.pushButton.setText("Add")
        self.labelDelay.setText("Key Delay")
        self.checkBoxInsertDQuote.setText("Use Double Quotes")
        self.checkBoxClipBoardDQuote.setText("Use Double Quotes")
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), "Keyboard")
        self.pushButtonCancel.setText("Cancel")

        self.setWindowFlags(Qt.WindowCloseButtonHint | Qt.WindowStaysOnTopHint)
        self.setFixedSize(self.size())

        self.radioButtonClick.setChecked(True)

        self.connect(self.pushButtonCancel, SIGNAL("clicked()"), self.CancelEvent)
        self.connect(self.checkBoxEnableClick, SIGNAL('clicked()'), self.CheckBoxEnableClickEvent)
        self.connect(self.pushButtonClickMove, SIGNAL("clicked()"), self.InsertMouseMoveClickAction)
        self.connect(self.pushButtonDrag, SIGNAL("clicked()"), self.InsertDragAction)
        self.connect(self.pushButton_2, SIGNAL("clicked()"), self.InsertTextAction)
        self.connect(self.pushButton, SIGNAL("clicked()"), self.PutToClipBoardAction)
        self.connect(self.pushButtonScroll, SIGNAL("clicked()"), self.PushButtonScrollAction)

        self.radioButtonClick.setEnabled(False)
        self.radioButtonDoubleClick.setEnabled(False)
        self.labelButton.setEnabled(False)
        self.comboBoxButton.setEnabled(False)

        self.spinBoxDelay.setValue(25)

    def CheckBoxEnableClickEvent(self):

        if self.checkBoxEnableClick.isChecked() is True:
            self.radioButtonClick.setEnabled(True)
            self.radioButtonDoubleClick.setEnabled(True)
            self.labelButton.setEnabled(True)
            self.comboBoxButton.setEnabled(True)
        else:
            self.radioButtonClick.setEnabled(False)
            self.radioButtonDoubleClick.setEnabled(False)
            self.labelButton.setEnabled(False)
            self.comboBoxButton.setEnabled(False)

    def InsertMouseMoveClickAction(self):

        if self.lineEditClickMoveX.text() == "" or self.lineEditClickMoveY.text() == "":
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

        if self.checkBoxEnableClick.isChecked() is True:

            button = self.comboBoxButton.currentText().lower()

            if self.radioButtonClick.isChecked() is True:
                if button == "left":
                    editor_service.insert_text("Mouse.Click(" + self.lineEditClickMoveX.text() + ", " + self.lineEditClickMoveY.text() + ")")
                    editor_service.insert_text(os.linesep)
                    editor_service.insert_text(leadingChar)
                else:
                    editor_service.insert_text("Mouse.Click(" + self.lineEditClickMoveX.text() + ", " + self.lineEditClickMoveY.text() + ", button=\"right\")")
                    editor_service.insert_text(os.linesep)
                    editor_service.insert_text(leadingChar)
            else:
                if button == "left":
                    editor_service.insert_text("Mouse.DoubleClick(" + self.lineEditClickMoveX.text() + ", " + self.lineEditClickMoveY.text() + ")")
                    editor_service.insert_text(os.linesep)
                    editor_service.insert_text(leadingChar)
                else:
                    editor_service.insert_text("Mouse.DoubleClick(" + self.lineEditClickMoveX.text() + ", " + self.lineEditClickMoveY.text() + ", button=\"right\")")
                    editor_service.insert_text(os.linesep)
                    editor_service.insert_text(leadingChar)
        else:
            editor_service.insert_text("Mouse.Move(" + self.lineEditClickMoveX.text() + ", " + self.lineEditClickMoveY.text() + ")")
            editor_service.insert_text(os.linesep)
            editor_service.insert_text(leadingChar)

    def InsertDragAction(self):

        if self.lineEditDragStartX.text() == "" or self.lineEditDragStartY.text() == "" or self.lineEditDragEndX.text() == "" or self.lineEditDragEndY.text() == "":
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

        editor_service.insert_text("Mouse.Drag(" + self.lineEditDragStartX.text() + ", " + self.lineEditDragStartY.text() + ", " + self.lineEditDragEndX.text() + ", " + self.lineEditDragEndY.text() + ")")
        editor_service.insert_text(os.linesep)
        editor_service.insert_text(leadingChar)

    def PushButtonScrollAction(self):
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

        direction = self.comboBoxScrollDirection.currentText().lower()
        step = self.spinBoxScrollStep.value()

        if step == 1:
            editor_service.insert_text("Mouse.Scroll(\"" + direction + "\")")
        else:
            editor_service.insert_text("Mouse.Scroll(\"" + direction + "\", step=" + str(step) + ")")
        editor_service.insert_text(os.linesep)
        editor_service.insert_text(leadingChar)

    def InsertTextAction(self):

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

        if self.lineEdit.text() != "":
            if self.spinBoxDelay.value() == 25:
                if self.checkBoxInsertDQuote.isChecked() is True:
                    editor_service.insert_text("Keyboard.InsertText(\"" + self.lineEdit.text() + "\")")
                else:
                    editor_service.insert_text("Keyboard.InsertText(" + self.lineEdit.text() + ")")
                editor_service.insert_text(os.linesep)
                editor_service.insert_text(leadingChar)
            else:
                if self.checkBoxInsertDQuote.isChecked() is True:
                    editor_service.insert_text("Keyboard.InsertText(\"" + self.lineEdit.text() + "\", delay=" + str(self.spinBoxDelay.value()) + ")")
                else:
                    editor_service.insert_text("Keyboard.InsertText(" + self.lineEdit.text() + ", delay=" + str(self.spinBoxDelay.value()) + ")")
                editor_service.insert_text(os.linesep)
                editor_service.insert_text(leadingChar)

    def PutToClipBoardAction(self):
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

        if self.lineEdit_2.text() != "":
            if self.checkBoxClipBoardDQuote.isChecked() is True:
                editor_service.insert_text("Keyboard.PutToClipBoard(\"" + self.lineEdit_2.text() + "\")")
            else:
                editor_service.insert_text("Keyboard.PutToClipBoard(" + self.lineEdit_2.text() + ")")
            editor_service.insert_text(os.linesep)
            editor_service.insert_text(leadingChar)

    def keyPressEvent(self, event):

        if event.key() == Qt.Key_Escape:
            self.close()

    def CancelEvent(self):
        self.close()