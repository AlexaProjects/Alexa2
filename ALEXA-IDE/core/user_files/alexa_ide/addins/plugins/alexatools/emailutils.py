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
import replaceforqt

class EmailUtils(QWidget):

    def __init__(self, plugin):
        super(EmailUtils, self).__init__()

        self.plugin = plugin
        self.plug_path = plugin.plug_path

        self.initUI()

    def initUI(self):
        icon = QIcon()
        icon.addPixmap(QPixmap(self.plug_path + "/alexatools/images/mail-foward.png"), QIcon.Normal, QIcon.Off)
        self.setWindowIcon(icon)
        self.setWindowTitle("Al\'exa - E-Mail")
        self.setObjectName("self")
        self.resize(403, 326)
        self.pushButtonCancel = QPushButton(self)
        self.pushButtonCancel.setGeometry(QRect(10, 290, 75, 23))
        self.pushButtonCancel.setObjectName("pushButtonCancel")
        self.pushButtonAdd = QPushButton(self)
        self.pushButtonAdd.setGeometry(QRect(100, 290, 75, 23))
        self.pushButtonAdd.setObjectName("pushButtonAdd")
        self.gridLayoutWidget = QWidget(self)
        self.gridLayoutWidget.setGeometry(QRect(10, 10, 381, 271))
        self.gridLayoutWidget.setObjectName("gridLayoutWidget")
        self.gridLayout = QGridLayout(self.gridLayoutWidget)
        self.gridLayout.setMargin(0)
        self.gridLayout.setObjectName("gridLayout")
        self.labelSmtpPort = QLabel(self.gridLayoutWidget)
        self.labelSmtpPort.setObjectName("labelSmtpPort")
        self.gridLayout.addWidget(self.labelSmtpPort, 1, 2, 1, 1)
        self.lineEditSmtpServer = QLineEdit(self.gridLayoutWidget)
        self.lineEditSmtpServer.setObjectName("lineEditSmtpServer")
        self.gridLayout.addWidget(self.lineEditSmtpServer, 1, 1, 1, 1)
        self.labelErrorScreen = QLabel(self.gridLayoutWidget)
        self.labelErrorScreen.setObjectName("labelErrorScreen")
        self.gridLayout.addWidget(self.labelErrorScreen, 0, 0, 1, 1)
        self.labelSmtpServer = QLabel(self.gridLayoutWidget)
        self.labelSmtpServer.setObjectName("labelSmtpServer")
        self.gridLayout.addWidget(self.labelSmtpServer, 1, 0, 1, 1)
        self.lineEditErrorScreen = QLineEdit(self.gridLayoutWidget)
        self.lineEditErrorScreen.setObjectName("lineEditErrorScreen")
        self.gridLayout.addWidget(self.lineEditErrorScreen, 0, 1, 1, 3)
        self.labelMessage = QLabel(self.gridLayoutWidget)
        self.labelMessage.setObjectName("labelMessage")
        self.gridLayout.addWidget(self.labelMessage, 7, 0, 1, 1)
        self.labelSubject = QLabel(self.gridLayoutWidget)
        self.labelSubject.setObjectName("labelSubject")
        self.gridLayout.addWidget(self.labelSubject, 6, 0, 1, 1)
        self.spinBoxImgSize = QSpinBox(self.gridLayoutWidget)
        self.spinBoxImgSize.setObjectName("spinBoxImgSize")
        self.gridLayout.addWidget(self.spinBoxImgSize, 8, 3, 1, 1)
        self.lineEditSubject = QLineEdit(self.gridLayoutWidget)
        self.lineEditSubject.setObjectName("lineEditSubject")
        self.gridLayout.addWidget(self.lineEditSubject, 6, 1, 1, 3)
        self.labelImgSize = QLabel(self.gridLayoutWidget)
        self.labelImgSize.setObjectName("labelImgSize")
        self.gridLayout.addWidget(self.labelImgSize, 8, 2, 1, 1)
        self.lineEditMailFrom = QLineEdit(self.gridLayoutWidget)
        self.lineEditMailFrom.setObjectName("lineEditMailFrom")
        self.gridLayout.addWidget(self.lineEditMailFrom, 4, 1, 1, 3)
        self.lineEditMessage = QLineEdit(self.gridLayoutWidget)
        self.lineEditMessage.setObjectName("lineEditMessage")
        self.gridLayout.addWidget(self.lineEditMessage, 7, 1, 1, 3)
        self.labelMailFrom = QLabel(self.gridLayoutWidget)
        self.labelMailFrom.setObjectName("labelMailFrom")
        self.gridLayout.addWidget(self.labelMailFrom, 4, 0, 1, 1)
        self.labelSmtpPassword = QLabel(self.gridLayoutWidget)
        self.labelSmtpPassword.setObjectName("labelSmtpPassword")
        self.gridLayout.addWidget(self.labelSmtpPassword, 2, 2, 1, 1)
        self.spinBoxSmtpPort = QSpinBox(self.gridLayoutWidget)
        self.spinBoxSmtpPort.setObjectName("spinBoxSmtpPort")
        self.gridLayout.addWidget(self.spinBoxSmtpPort, 1, 3, 1, 1)
        self.labelSmtpUser = QLabel(self.gridLayoutWidget)
        self.labelSmtpUser.setObjectName("labelSmtpUser")
        self.gridLayout.addWidget(self.labelSmtpUser, 2, 0, 1, 1)
        self.labelMailTo = QLabel(self.gridLayoutWidget)
        self.labelMailTo.setObjectName("labelMailTo")
        self.gridLayout.addWidget(self.labelMailTo, 5, 0, 1, 1)
        self.labelImgQuality = QLabel(self.gridLayoutWidget)
        self.labelImgQuality.setObjectName("labelImgQuality")
        self.gridLayout.addWidget(self.labelImgQuality, 8, 0, 1, 1)
        self.spinBoxImgQuality = QSpinBox(self.gridLayoutWidget)
        self.spinBoxImgQuality.setObjectName("spinBoxImgQuality")
        self.gridLayout.addWidget(self.spinBoxImgQuality, 8, 1, 1, 1)
        self.lineEditMailTo = QLineEdit(self.gridLayoutWidget)
        self.lineEditMailTo.setObjectName("lineEditMailTo")
        self.gridLayout.addWidget(self.lineEditMailTo, 5, 1, 1, 3)
        self.lineEditSmtpPassword = QLineEdit(self.gridLayoutWidget)
        self.lineEditSmtpPassword.setObjectName("lineEditSmtpPassword")
        self.gridLayout.addWidget(self.lineEditSmtpPassword, 2, 3, 1, 1)
        self.lineEditSmtpUser = QLineEdit(self.gridLayoutWidget)
        self.lineEditSmtpUser.setObjectName("lineEditSmtpUser")
        self.gridLayout.addWidget(self.lineEditSmtpUser, 2, 1, 1, 1)
        self.labelTimeout = QLabel(self.gridLayoutWidget)
        self.labelTimeout.setObjectName("labelTimeout")
        self.gridLayout.addWidget(self.labelTimeout, 9, 0, 1, 1)
        self.spinBoxTimeout = QSpinBox(self.gridLayoutWidget)
        self.spinBoxTimeout.setObjectName("spinBoxTimeout")
        self.gridLayout.addWidget(self.spinBoxTimeout, 9, 1, 1, 1)

        self.pushButtonCancel.setText("Cancel")
        self.pushButtonAdd.setText("Add")
        self.labelSmtpPort.setText("Smtp Port")
        self.labelErrorScreen.setText("Error Screen Folder")
        self.labelSmtpServer.setText("Smtp Server")
        self.labelMessage.setText("Message")
        self.labelSubject.setText("Subject")
        self.labelImgSize.setText("Image Size (%)")
        self.labelMailFrom.setText("Mail From")
        self.labelSmtpPassword.setText("Smtp Password")
        self.labelSmtpUser.setText("Smtp User")
        self.labelMailTo.setText("Mail To")
        self.labelImgQuality.setText("Image Quality (%)")
        self.labelTimeout.setText("Timeout (s)")

        self.setWindowFlags(Qt.WindowCloseButtonHint | Qt.WindowStaysOnTopHint)
        self.setFixedSize(self.size())

        self.connect(self.pushButtonCancel, SIGNAL("clicked()"), self.CancelEvent)
        self.connect(self.pushButtonAdd, SIGNAL("clicked()"), self.AddCode)

    def AddCode(self):
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

        if self.lineEditErrorScreen.text() == "":
            editor_service.insert_text("Mail.ErrorScreenFolder = Log.Path")
        else:
            editor_service.insert_text("Mail.ErrorScreenFolder = \"" + replaceforqt.ReplacePythonChars(self.lineEditErrorScreen.text()) + "\"")
        editor_service.insert_text(os.linesep)
        editor_service.insert_text(leadingChar)
        editor_service.insert_text("Mail.SmtpServer = \"" + self.lineEditSmtpServer.text() + "\"")
        editor_service.insert_text(os.linesep)
        editor_service.insert_text(leadingChar)
        editor_service.insert_text("Mail.SmtpPort = " + str(self.spinBoxSmtpPort.value()))
        editor_service.insert_text(os.linesep)
        editor_service.insert_text(leadingChar)

        if self.lineEditSmtpUser.text() != "" and self.lineEditSmtpPassword.text() != "":
            editor_service.insert_text("Mail.SmtpUser = \"" + replaceforqt.ReplacePythonChars(self.lineEditSmtpUser.text()) + "\"")
            editor_service.insert_text(os.linesep)
            editor_service.insert_text(leadingChar)
            editor_service.insert_text("Mail.SmtpPassword = \"" + replaceforqt.ReplacePythonChars(self.lineEditSmtpPassword.text()) + "\"")
            editor_service.insert_text(os.linesep)
            editor_service.insert_text(leadingChar)

        editor_service.insert_text("Mail.From = \"" + self.lineEditMailFrom.text() + "\"")
        editor_service.insert_text(os.linesep)
        editor_service.insert_text(leadingChar)
        editor_service.insert_text("Mail.To = \"" + self.lineEditMailTo.text() + "\"")
        editor_service.insert_text(os.linesep)
        editor_service.insert_text(leadingChar)
        editor_service.insert_text("Mail.Subject = \"" + replaceforqt.ReplacePythonChars(self.lineEditSubject.text()) + "\"")
        editor_service.insert_text(os.linesep)
        editor_service.insert_text(leadingChar)
        editor_service.insert_text("Mail.Message = \"" + replaceforqt.ReplacePythonChars(self.lineEditMessage.text()) + "\"")
        #editor_service.insert_text("Mail.Message = \"" + self.lineEditMessage.text() + "\"")
        editor_service.insert_text(os.linesep)
        editor_service.insert_text(leadingChar)
        editor_service.insert_text("Mail.ResizeFactor = " + str(self.spinBoxImgSize.value()))
        editor_service.insert_text(os.linesep)
        editor_service.insert_text(leadingChar)
        editor_service.insert_text("Mail.ImageQuality = " + str(self.spinBoxImgQuality.value()))
        editor_service.insert_text(os.linesep)
        editor_service.insert_text(leadingChar)
        editor_service.insert_text("Mail.Send()")
        editor_service.insert_text(os.linesep)
        editor_service.insert_text(leadingChar)


    def keyPressEvent(self, event):

        if event.key() == Qt.Key_Escape:
            self.close()

    def CancelEvent(self):
        self.close()