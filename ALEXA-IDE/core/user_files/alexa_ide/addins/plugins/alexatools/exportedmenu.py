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

#QT Toolkit
from PyQt4.QtGui import *
from PyQt4.QtCore import *


class ExportedMenu(QWidget):

    def __init__(self, plugin):
        super(ExportedMenu, self).__init__()

        self.plugin = plugin
        self.plug_path = plugin.path

        self.initUI()

    def initUI(self):

        self.setWindowTitle("Al\'exa tools")
        self.resize(490, 36)

        self.setStyleSheet("""
        QPushButton {
            border: none;
        }

        QPushButton:hover {
            border-radius: 5px;
            border-width: 1px;
            border-color:#a8a8a8;
            border-style: solid;
            background-color: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                                       stop: 0 #dadbde, stop: 1 #f6f7fa);

        }

        QPushButton:pressed {
            border-radius: 5px;
            border-width: 1px;
            border-color:gray;
            border-style: solid;
        }
        """)

        self.pushButtonAppObj = QPushButton(self)
        self.pushButtonAppObj.setGeometry(QRect(8, 5, 34, 28))
        iconAppObj = QIcon()
        iconAppObj.addPixmap(QPixmap(self.plug_path + "/images/bind.png"), QIcon.Normal, QIcon.Off)
        self.pushButtonAppObj.setIcon(iconAppObj)
        self.pushButtonAppObj.setIconSize(QSize(24, 24))
        self.pushButtonAppObj.setToolTip("Bind Application Objects (Ctrl + O)")


        self.pushButtonAppImage = QPushButton(self)
        self.pushButtonAppImage.setGeometry(QRect(51, 4, 34, 28))
        iconAppImg = QIcon()
        iconAppImg.addPixmap(QPixmap(self.plug_path + "/images/image.png"), QIcon.Normal, QIcon.Off)
        self.pushButtonAppImage.setIcon(iconAppImg)
        self.pushButtonAppImage.setIconSize(QSize(24, 24))
        self.pushButtonAppImage.setToolTip("Bind Application Images (Ctrl + I)")

        self.pushButtonAppText = QPushButton(self)
        self.pushButtonAppText.setGeometry(QRect(94, 4, 34, 28))
        iconAppText = QIcon()
        iconAppText.addPixmap(QPixmap(self.plug_path + "/images/text-x-gettext-translation.png"), QIcon.Normal, QIcon.Off)
        self.pushButtonAppText.setIcon(iconAppText)
        self.pushButtonAppText.setIconSize(QSize(24, 24))
        self.pushButtonAppText.setToolTip("Bind Application Text (Ctrl + T)")

        self.spinBox = QSpinBox(self)
        self.spinBox.setGeometry(QRect(434, 7, 42, 22))

        self.label = QLabel(self)
        self.label.setGeometry(QRect(387, 11, 41, 16))
        self.label.setText("Delay")


        #self.pushButtonAppObj = QPushButton(self.window)
        self.setWindowFlags(Qt.WindowCloseButtonHint | Qt.WindowStaysOnTopHint)
        self.setFixedSize(self.size())

        self.connect(self.pushButtonAppObj, SIGNAL("clicked()"), self.plugin.OpenAppObjectCaptureScreen)
        shortcutObj = QShortcut(QKeySequence("Ctrl+O"), self);
        self.connect(shortcutObj, SIGNAL("activated()"), self.plugin.OpenAppObjectCaptureScreen)

        self.connect(self.pushButtonAppImage, SIGNAL("clicked()"), self.plugin.OpenAppImageCaptureScreen)
        shortcutImg = QShortcut(QKeySequence("Ctrl+I"), self);
        self.connect(shortcutImg, SIGNAL("activated()"), self.plugin.OpenAppImageCaptureScreen)

        self.connect(self.pushButtonAppText, SIGNAL("clicked()"), self.plugin.OpenAppTextCaptureScreen)
        shortcutTxt = QShortcut(QKeySequence("Ctrl+T"), self);
        self.connect(shortcutTxt, SIGNAL("activated()"), self.plugin.OpenAppTextCaptureScreen)

        self.connect(self.spinBox, SIGNAL('valueChanged(int)'), self.SpinBoxEvent)

        self.spinBox.setValue(self.plugin.screenshotDelay)

    def SpinBoxEvent(self):
        self.plugin.screenshotDelay = self.spinBox.value()

    def keyPressEvent(self, event):

        if event.key() == Qt.Key_Escape:
            self.close()

    def closeEvent(self, event):
        self.plugin.undockWindowOpened = False