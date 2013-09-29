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
import os
import sys

#QT Toolkit
from PyQt4.QtGui import *
from PyQt4.QtCore import *

#PIL
import Image

if sys.platform == 'win32':
    import win32gui
    import win32con

class CropRegionClass(QWidget):
    def __init__(self, caller):
        QWidget.__init__(self)

        self.caller = caller
        self.plug_path = self.caller.plugin.path

        SERVICE_NAME = "editor"
        self.editor_service = self.caller.plugin.locator.get_service(SERVICE_NAME)

        #set pixmap for the background
        self.pixmap = QPixmap()
        self.pixmap.load(self.plug_path + os.sep + 'tmp' + os.sep + 'screenshot.png')
        self.OriginalScreenshot = Image.open(self.plug_path + os.sep + 'tmp' + os.sep + 'screenshot.png')

        #store if mouse is pressed
        self.pressed = False
        self.released = False
        self.printLabelBorder = False

        #store mouse position
        self.mouseOldX = 0
        self.mouseOldY = 0
        self.mouseNewX = 0
        self.mouseNewY = 0


    def paintEvent(self, event):

        paint = QPainter()
        paint.begin(self)

        paint.drawPixmap(0, 0, self.pixmap)

        pen = QPen()

        #serve per creare un quadrato senza angoli smussati
        pen.setJoinStyle(Qt.MiterJoin)

        center = QPoint(QCursor.pos())


        if self.caller.CropRegionX != 0 or self.caller.CropRegionY != 0 or self.caller.CropRegionW != 0 or self.caller.CropRegionH != 0:

                x = self.caller.CropRegionX
                y = self.caller.CropRegionY
                w = self.caller.CropRegionW
                h = self.caller.CropRegionH

                pen.setStyle(Qt.SolidLine)
                pen.setBrush(QColor(0, 78, 255, 255))
                pen.setWidth(1)
                paint.setPen(pen)
                paint.fillRect(x, y, w, h,
                    QBrush(QColor(100, 80, 155, 100)))

                newRect = QRect(x, y, w, h)

                paint.drawRect(newRect)

        #paint.restore()
        self.mouseNewX = center.x()
        self.mouseNewY = center.y()

        if self.pressed is False:

            #pen.setStyle(Qt.DashDotLine)
            pen.setDashPattern([1, 1])

            pen.setWidth(1)
            pen.setBrush(QColor(32, 178, 170, 255))
            #pen.setBrush(QColor(225, 0, 0, 255))
            paint.setPen(pen)

            #dal centro in alto
            paint.drawLine(center.x(), center.y(), center.x(), 0)
            #dal centro in basso
            paint.drawLine(center.x(), center.y(), center.x(), self.height())
            paint.drawLine(center.x(), center.y(), 0, center.y())
            paint.drawLine(center.x(), center.y(), self.width(), center.y())

            pen.setStyle(Qt.SolidLine)
            pen.setWidth(1)
            pen.setBrush(Qt.red)
            pen.setCapStyle(Qt.RoundCap)
            pen.setJoinStyle(Qt.RoundJoin)
        else:
            pen.setWidth(1)
            pen.setStyle(Qt.SolidLine)
            #pen.setBrush(QColor(128, 128, 128, 255))
            pen.setBrush(QBrush(QColor(0, 255, 0, 255)))
            paint.setPen(pen)
            paint.fillRect(self.mouseOldX + 1,
                self.mouseOldY + 1,
                center.x() - self.mouseOldX - 1,
                center.y() - self.mouseOldY - 1,
                QBrush(QColor(32, 178, 170, 100)))
            rect = QRect(self.mouseOldX, self.mouseOldY,
                center.x() - self.mouseOldX, center.y() - self.mouseOldY)
            paint.drawRect(rect)

        self.setCursor(QCursor(Qt.CrossCursor))
        #self.setCursor(QCursor(Qt.BlankCursor))
        paint.end()

    def mouseMoveEvent(self, event):

        self.update()

    #mouse press event
    def mousePressEvent(self, event):

        if event.buttons() == Qt.LeftButton:

            #self.setCursor(QCursor(Qt.BlankCursor))
            self.pressed = True
            origin = QPoint(QCursor.pos())
            self.mouseOldX = origin.x()
            self.mouseOldY = origin.y()
            self.update()


    #mouse release event
    def mouseReleaseEvent(self, event):

        #if(event.type() == QEvent.MouseButtonRelease):
        if event.button() == Qt.LeftButton:

            self.pressed = False
            self.released = True

            width = self.mouseNewX - self.mouseOldX
            height = self.mouseNewY - self.mouseOldY

            rect = QRect(self.mouseOldX, self.mouseOldY, width, height)

            if (rect.width() >= 3 or rect.width() <= -3) and (rect.height() >= 3 or rect.height() <= -3):

                if (rect.width() < 0 and rect.height() < 0):

                    x = rect.x() + rect.width()
                    y = rect.y() + rect.height()
                    w = -rect.width()
                    h = -rect.height()
                    ##rect = QRect(x, y, w, h)

                elif (rect.width() < 0 and rect.height() > 0):

                    x = rect.x() + rect.width()
                    y = rect.y()
                    w = -rect.width()
                    h = rect.height()
                    ##rect = QRect(x, y, w, h)

                elif (rect.width() > 0 and rect.height() < 0):

                    x = rect.x()
                    y = rect.y() + rect.height()
                    w = rect.width()
                    h = -rect.height()
                    ##rect = QRect(x, y, w, h)
                else:
                    x = rect.x()
                    y = rect.y()
                    w = rect.width()
                    h = rect.height()
                    ##rect = QRect(x, y, w, h)

                if width < 0:
                    width = width * -1
                if height < 0:
                    height = height * -1

                #AlexaObject.Height = height
                #AlexaObject.Width = width
                self.caller.CropRegionH = h
                self.caller.CropRegionW = w
                self.caller.CropRegionX = x
                self.caller.CropRegionY = y

                self.caller.UpdateCropSpinBoxes()

            self.update()
            #self.closeExtended()

    def keyPressEvent(self, event):

        if event.key() == Qt.Key_Escape:
            self.closeExtended2()

    def closeExtended2(self):
        self.caller.setVisible(True)
        self.close()

    def closeExtended(self):

        if sys.platform == 'win32':
            toplist = []
            winlist = []

            def enum_callback(hwnd, results):
                winlist.append((hwnd, win32gui.GetWindowText(hwnd)))
            win32gui.EnumWindows(enum_callback, toplist)

            if self.caller.plugin.undockWindowOpened is True:
                firefox = [(hwnd, title) for hwnd, title in
                    winlist if 'exa-ide' in title.lower() or 'exa tool' in title.lower() and 'about' not in title.lower()]
            else:
                firefox = [(hwnd, title) for hwnd, title in
                    winlist if 'exa-ide' in title.lower() and 'about' not in title.lower() and 'exa tool' not in title.lower()]
            # just grab the first window that matches
            #firefox = firefox[0]
            for ninja in firefox:
                win32gui.ShowWindow(ninja[0], win32con.SW_SHOW)
                #print str(ninja[0]) + " " + ninja[1]

        self.caller.setVisible(True)
        self.close()


