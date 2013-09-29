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

import copy
#NINJA
from ninja_ide.tools import json_manager
from apptextdialog import AppTextDialog
from apptextdialog import AppTextInRegionDialog

try:
    import json
except ImportError:
    import simplejson as json

#QT Toolkit
from PyQt4.QtGui import *
from PyQt4.QtCore import *
import ImageQt
#OPENCV
import cv2
import cv2.cv as cv
#PIL
import Image
#NUMPY
import numpy
#ALEXA
from Alexa import *


class AppTextCaptureScreenshot(QWidget):
    def __init__(self, plugin):
        QWidget.__init__(self)

        self.plugin = plugin
        self.plug_path = plugin.path

        SERVICE_NAME = "editor"
        self.editor_service = self.plugin.locator.get_service(SERVICE_NAME)
        fullFileName = self.editor_service.get_editor_path()
        #from os.path import basename

        filePath = os.path.split(fullFileName)[0]
        fileName = os.path.split(fullFileName)[1]
        #print os.path.splitext(fileName)[1]
        self.jsonfile = json_manager.read_json(filePath + os.sep + fileName.replace(os.path.splitext(fileName)[1], ".nja"))
        #filetoparse = filePath + os.sep + fileName.replace("py", "nja")
        self.jsonfile["ocrdatafolder"]

        self.isCanny = False

        self.MovingAppObject = False

        self.TollerancePreview = False

        #self.binarizeImagePreviewFlag = False
        #self.Brightness = 0.0
        #self.Contrast = 0.0

        #self.binarizeLabelPreviewFlag = False

        #set pixmap for the background
        self.pixmap = QPixmap()
        self.pixmap.load(self.plug_path + os.sep + 'tmp' + os.sep + 'screenshot.png')
        self.OriginalScreenshot = Image.open(self.plug_path + os.sep + 'tmp' + os.sep + 'screenshot.png')

        #store if mouse is pressed
        self.pressed = False
        self.released = False
        self.printLabelBorder = False

        self.InsideRect = False
        self.InsideRegion = False
        self.AdjustOnlyHeightTollerance = False
        self.AdjustOnlyWidthTollerance = False

        #store mouse position
        self.mouseOldX = 0
        self.mouseOldY = 0
        self.mouseNewX = 0
        self.mouseNewY = 0

        self.rectLabelCollection = []
        self.rectLabelCollectionDeleted = []

        #Al'exa AppObject
        self.AlexaAppObjectsBackup = []
        self.AlexaAppObjectsBackupDeleted = []
        self.AlexaAppObjects = []
        self.AlexaAppObjectsDeleted = []

        self.LabelOfInterest = []

        self.LastRectHover = 0

        self.Dialog = None
        self.DialogOpened = False
        self.DialogHwnd = None

        self.CropLabel = False
        self.CropRegion = False
        self.AppObjectFeedbackIndex = None
        self.indexFound = None
        self.indexFoundAppText = None

    def BringWindowToFront(self):

        if sys.platform == 'win32':
            win32gui.SetForegroundWindow(self.DialogHwnd)

    def PaintRectTollerance(self, paint, AlexaAppObject):

        pen = QPen()
        pen.setWidth(1)
        pen.setBrush(QColor(255, 0, 0, 255))
        paint.setPen(pen)

        OuterPath = QPainterPath()
        OuterPath.setFillRule(Qt.WindingFill)

        OuterPath.addRect(AlexaAppObject.RectX - AlexaAppObject.WidthTollerance,
            AlexaAppObject.RectY - AlexaAppObject.HeightTollerance,
            AlexaAppObject.ObjW + (AlexaAppObject.WidthTollerance * 2),
            AlexaAppObject.ObjH + (AlexaAppObject.HeightTollerance * 2))

        if AlexaAppObject.ObjW >= (AlexaAppObject.WidthTollerance * 2) and AlexaAppObject.ObjH >= (AlexaAppObject.HeightTollerance * 2):
            InnerPath = QPainterPath()

            InnerPath.addRect(AlexaAppObject.RectX + AlexaAppObject.WidthTollerance,
                AlexaAppObject.RectY + AlexaAppObject.HeightTollerance,
                AlexaAppObject.ObjW - (AlexaAppObject.WidthTollerance * 2),
                AlexaAppObject.ObjH - (AlexaAppObject.HeightTollerance * 2))

            FillPath = OuterPath.subtracted(InnerPath)
            paint.fillPath(FillPath, QColor(255, 0, 255, 130))
        else:
            paint.fillPath(OuterPath, QColor(255, 0, 255, 130))

        pen.setWidth(1)
        pen.setStyle(Qt.DashLine)
        paint.setPen(pen)

        paint.drawRect(AlexaAppObject.RectX - AlexaAppObject.WidthTollerance,
            AlexaAppObject.RectY - AlexaAppObject.HeightTollerance,
            AlexaAppObject.ObjW + (AlexaAppObject.WidthTollerance * 2),
            AlexaAppObject.ObjH + (AlexaAppObject.HeightTollerance * 2))
        pen.setStyle(Qt.SolidLine)
        paint.setPen(pen)

        #paint.drawRect(x, y, AlexaAppObject.ObjW, AlexaAppObject.ObjH)

        pen.setStyle(Qt.DashLine)
        paint.setPen(pen)
        if AlexaAppObject.ObjW >= (AlexaAppObject.WidthTollerance * 2) and AlexaAppObject.ObjH >= (AlexaAppObject.HeightTollerance * 2):
            paint.drawRect(AlexaAppObject.RectX + AlexaAppObject.WidthTollerance,
                AlexaAppObject.RectY + AlexaAppObject.HeightTollerance,
                AlexaAppObject.ObjW - (AlexaAppObject.WidthTollerance * 2),
                AlexaAppObject.ObjH - (AlexaAppObject.HeightTollerance * 2))
        elif AlexaAppObject.ObjW >= (AlexaAppObject.WidthTollerance * 2):
            paint.drawLine(AlexaAppObject.RectX + AlexaAppObject.WidthTollerance,
                AlexaAppObject.RectY + (AlexaAppObject.ObjH / 2),
                AlexaAppObject.RectX + AlexaAppObject.ObjW - AlexaAppObject.WidthTollerance,
                AlexaAppObject.RectY + (AlexaAppObject.ObjH / 2))
            #paint.drawLine(AlexaAppObject.RectX + 8, AlexaAppObject.RectY + (h/2), AlexaAppObject.RectX + 8 + 1, AlexaAppObject.RectY + (h/2))
            #paint.drawLine(AlexaAppObject.RectX + w - 8, AlexaAppObject.RectY + (h/2), AlexaAppObject.RectX + w - 8, AlexaAppObject.RectY + (h/2))
            #pen.setStyle(Qt.SolidLine)
            #paint.setPen(pen)
            #paint.drawLine(AlexaAppObject.RectX + 8, y, AlexaAppObject.RectX + 8, AlexaAppObject.RectY + h)
        elif AlexaAppObject.ObjH >= (AlexaAppObject.HeightTollerance * 2):
            paint.drawLine(AlexaAppObject.RectX + (AlexaAppObject.ObjW / 2),
                AlexaAppObject.RectY + AlexaAppObject.HeightTollerance,
                AlexaAppObject.RectX + (AlexaAppObject.ObjW / 2),
                AlexaAppObject.RectY + AlexaAppObject.ObjH - AlexaAppObject.HeightTollerance)
        else:
            paint.drawLine(AlexaAppObject.RectX + (AlexaAppObject.ObjW / 2),
                AlexaAppObject.RectY + (AlexaAppObject.ObjH / 2),
                AlexaAppObject.RectX + (AlexaAppObject.ObjW / 2),
                AlexaAppObject.RectY + (AlexaAppObject.ObjH / 2))

        pen.setWidth(1)
        pen.setStyle(Qt.SolidLine)
        pen.setBrush(QBrush(QColor(0, 255, 0, 255)))
        paint.setPen(pen)

        #paint.drawLine(x, AlexaAppObject.RectY - 5 - 10, AlexaAppObject.RectX + w, AlexaAppObject.RectY - 5 - 10)
        #paint.drawLine(x, AlexaAppObject.RectY - 5 - 6, x, AlexaAppObject.RectY - 5 - 14)
        #paint.drawLine(AlexaAppObject.RectX + w, AlexaAppObject.RectY - 5 - 6, AlexaAppObject.RectX + w, AlexaAppObject.RectY - 5 - 14)

    def paintEvent(self, event):

        paint = QPainter()
        paint.begin(self)

        paint.drawPixmap(0, 0, self.pixmap)

        pen = QPen()

        #serve per creare un quadrato senza angoli smussati
        pen.setJoinStyle(Qt.MiterJoin)

        center = QPoint(QCursor.pos())

        cnt = 0
        self.InsideRect = False
        self.InsideRegion = False

        #ciclo per disegno rettangoli e tooltip
        for appObject in self.AlexaAppObjects:

            pen.setBrush(QColor(255, 0, 0, 255))
            pen.setWidth(1)
            paint.setPen(pen)

            if self.TollerancePreview is True and self.CropLabel is False and self.CropRegion is False and cnt == self.AppObjectFeedbackIndex:

                pen.setBrush(QColor(255, 0, 0, 255))
                pen.setWidth(1)
                paint.setPen(pen)

                font = paint.font()

                paint.setFont(font)

                x = appObject.RectX
                y = appObject.RectY
                #w = appObject.Width
                #h = appObject.Height

                '''
                paint.drawText(x, y - 30,
                    "Height: " + str(appObject.ObjH) +
                    ", Width: " + str(appObject.Width))
                '''

                #appObject.ObjH = 200

                #self.PaintRectHover(paint, x, y, w, h)
                self.PaintRectTollerance(paint, appObject)

            elif (center.x() > appObject.RectX and
                center.x() < appObject.ObjW + appObject.RectX and
                center.y() > appObject.RectY and
                center.y() < appObject.ObjH + appObject.RectY and
                self.CropLabel is False and self.CropRegion is False):

                pen.setStyle(Qt.SolidLine)
                if self.indexFound is not None and self.indexFound == self.AppObjectFeedbackIndex and self.indexFound == cnt:
                    pen.setBrush(QColor(112, 81, 213, 255))
                else:
                    pen.setBrush(QColor(255, 0, 0, 255))
                pen.setWidth(1)
                paint.setPen(pen)

                font = paint.font()

                paint.setFont(font)

                x = appObject.RectX
                y = appObject.RectY

                if self.indexFound is not None and self.indexFound == self.AppObjectFeedbackIndex and self.indexFound == cnt:
                    paint.fillRect(appObject.RectX,
                        appObject.RectY,
                        appObject.ObjW,
                        appObject.ObjH,
                        QBrush(QColor(0, 255, 0, 130)))
                else:
                    paint.fillRect(appObject.RectX,
                        appObject.RectY,
                        appObject.ObjW,
                        appObject.ObjH,
                        QBrush(QColor(255, 0, 255, 130)))

                newRect = QRect(appObject.RectX,
                    appObject.RectY,
                    appObject.ObjW,
                    appObject.ObjH)

                paint.drawRect(newRect)

                #self.PaintRectHover(paint, x, y, appObject)

                self.InsideRect = True
                self.LastRectHover = cnt
            elif (center.x() > appObject.RectX + appObject.CropRegionX and
                center.x() < appObject.RectX + appObject.CropRegionX + appObject.CropRegionWidth and
                center.y() > appObject.RectY + appObject.CropRegionY and
                center.y() < appObject.RectY + appObject.CropRegionY + appObject.CropRegionHeight and
                self.CropLabel is False and self.CropRegion is False):
                pen.setStyle(Qt.SolidLine)
                if self.indexFound is not None and self.indexFound == self.AppObjectFeedbackIndex and self.indexFound == cnt:
                    pen.setBrush(QColor(112, 81, 213, 255))
                else:
                    pen.setBrush(QColor(255, 0, 0, 255))
                pen.setWidth(1)
                paint.setPen(pen)

                font = paint.font()

                paint.setFont(font)

                x = appObject.RectX
                y = appObject.RectY

                if self.indexFound is not None and self.indexFound == self.AppObjectFeedbackIndex and self.indexFound == cnt:
                    paint.fillRect(appObject.RectX,
                        appObject.RectY,
                        appObject.ObjW,
                        appObject.ObjH,
                        QBrush(QColor(0, 255, 0, 130)))
                else:
                    paint.fillRect(appObject.RectX,
                        appObject.RectY,
                        appObject.ObjW,
                        appObject.ObjH,
                        QBrush(QColor(255, 0, 255, 130)))

                newRect = QRect(appObject.RectX,
                    appObject.RectY,
                    appObject.ObjW,
                    appObject.ObjH)

                paint.drawRect(newRect)

                #self.PaintRectHover(paint, x, y, appObject)

                self.InsideRegion = True
                self.LastRectHover = cnt
            else:
                #paint.setRenderHint(QPainter.SmoothPixmapTransform)
                pen.setStyle(Qt.SolidLine)

                if self.indexFound is not None and self.indexFound == self.AppObjectFeedbackIndex and self.indexFound == cnt:
                    pen.setBrush(QColor(112, 81, 213, 255))
                else:
                    pen.setBrush(QColor(255, 0, 0, 255))
                pen.setWidth(1)
                paint.setPen(pen)

                if self.indexFound is not None and self.indexFound == self.AppObjectFeedbackIndex and self.indexFound == cnt:
                    paint.fillRect(appObject.RectX,
                        appObject.RectY,
                        appObject.ObjW,
                        appObject.ObjH,
                        QBrush(QColor(0, 255, 0, 130)))
                else:
                    paint.fillRect(appObject.RectX,
                        appObject.RectY,
                        appObject.ObjW,
                        appObject.ObjH,
                        QBrush(QColor(255, 0, 255, 130)))
                '''
                paint.fillRect(appObject.RectX,
                    appObject.RectY,
                    appObject.ObjW,
                    appObject.ObjH,
                    QBrush(QColor(255, 0, 255, 100)))
                '''
                newRect = QRect(appObject.RectX,
                    appObject.RectY,
                    appObject.ObjW,
                    appObject.ObjH)

                paint.drawRect(newRect)

                pen.setWidth(1)
                paint.setPen(pen)

            if self.indexFound is not None and self.indexFound == self.AppObjectFeedbackIndex:
                #pen.setBrush(QColor(112, 81, 213, 255))
                pen.setBrush(QColor(255, 0, 0, 255))
                pen.setStyle(Qt.DashLine)
                paint.setPen(pen)
                newRect = QRect(appObject.x, appObject.y, appObject.Width, appObject.Height)
                paint.drawRect(newRect)

            if appObject.CropRegionX != 0 and appObject.CropRegionY != 0 and appObject.CropRegionWidth != 0 and appObject.CropRegionHeight != 0:
                x = appObject.RectX
                y = appObject.RectY
                w = appObject.CropRegionWidth
                h = appObject.CropRegionHeight
                '''
                pen.setStyle(Qt.DashLine)
                pen.setBrush(QColor(0, 0, 255, 255))
                pen.setWidth(1)
                paint.setPen(pen)

                newRect = QRect(x + appObject.CropRegionX,
                    y + appObject.CropRegionY, w, h)
                paint.drawRect(newRect)

                '''
                pen.setStyle(Qt.SolidLine)
                pen.setBrush(QColor(0, 78, 255, 255))
                pen.setWidth(1)
                paint.setPen(pen)
                paint.fillRect(x + appObject.CropRegionX,
                    y + appObject.CropRegionY, w, h,
                    QBrush(QColor(100, 80, 155, 100)))

                newRect = QRect(x + appObject.CropRegionX,
                    y + appObject.CropRegionY, w, h)

                paint.drawRect(newRect)

                if self.indexFoundAppText is not None and self.indexFoundAppText == self.AppObjectFeedbackIndex and self.indexFoundAppText == cnt:
                    pen.setWidth(1)
                    pen.setStyle(Qt.DashLine)
                    pen.setBrush(QColor(255, 0, 255, 255))

                    paint.setPen(pen)
                    newRect = QRect(x + appObject.CropRegionX + appObject.AppText.x, y + appObject.CropRegionY + appObject.AppText.y, appObject.AppText.Width, appObject.AppText.Height)
                    paint.drawRect(newRect)

            cnt = cnt + 1

        #paint.restore()
        self.mouseNewX = center.x()
        self.mouseNewY = center.y()

        if self.InsideRect is True or self.InsideRegion is True:
            if self.DialogOpened is True or self.InsideRegion is True:
                self.setCursor(QCursor(Qt.ArrowCursor))
            else:
                self.setCursor(QCursor(Qt.SizeAllCursor))
            return

        if self.pressed is False:
            if self.DialogOpened is True:
                self.setCursor(QCursor(Qt.ArrowCursor))
                return

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

        pos = event.pos()
        #print('mouse move: (%d, %d)' % (pos.x(), pos.y()))

        if self.InsideRect is True and self.pressed is True:

            self.MovingAppObject = True

            #newRect = QRect(pos.x() - self.xOffset, pos.y() - self.yOffset,
                #self.AlexaAppObjects[self.LastRectHover].width(),
                #self.AlexaAppObjects[self.LastRectHover].height())
            self.AlexaAppObjects[self.LastRectHover].RectX = pos.x() - self.xOffset
            self.AlexaAppObjects[self.LastRectHover].RectY =  pos.y() - self.yOffset

            #self.rectObjCollection[self.LastRectHover].x = pos.x()
            #self.rectObjCollection[self.LastRectHover].y = pos.y()
        #rise paint event
        #self.color = QColor(Qt.red)
        self.update()

    def wheelEvent(self, event):

        if self.DialogOpened is True:
            return

        #print self.LastRectHover
        #print self.InsideRect

        if self.InsideRect is True:

            if self.AdjustOnlyHeightTollerance is True:
                self.AlexaAppObjects[self.LastRectHover].HeightTollerance = self.AlexaAppObjects[self.LastRectHover].HeightTollerance + event.delta() / 120
                if self.AlexaAppObjects[self.LastRectHover].HeightTollerance < 0:
                    self.AlexaAppObjects[self.LastRectHover].HeightTollerance = 0
            elif self.AdjustOnlyWidthTollerance is True:
                self.AlexaAppObjects[self.LastRectHover].WidthTollerance = self.AlexaAppObjects[self.LastRectHover].WidthTollerance + event.delta() / 120

                if self.AlexaAppObjects[self.LastRectHover].WidthTollerance < 0:
                    self.AlexaAppObjects[self.LastRectHover].WidthTollerance = 0
            else:
                self.AlexaAppObjects[self.LastRectHover].HeightTollerance = self.AlexaAppObjects[self.LastRectHover].HeightTollerance + event.delta() / 120
                if self.AlexaAppObjects[self.LastRectHover].HeightTollerance < 0:
                    self.AlexaAppObjects[self.LastRectHover].HeightTollerance = 0

                self.AlexaAppObjects[self.LastRectHover].WidthTollerance = self.AlexaAppObjects[self.LastRectHover].WidthTollerance + event.delta() / 120
                if self.AlexaAppObjects[self.LastRectHover].WidthTollerance < 0:
                    self.AlexaAppObjects[self.LastRectHover].WidthTollerance = 0

            self.update()

    #mouse press event
    def mousePressEvent(self, event):
        if self.DialogOpened is True or self.InsideRegion is True:
            #self.BringWindowToFront()
            return

        if event.buttons() == Qt.LeftButton:

            if self.InsideRect is True:
                pos = QPoint(QCursor.pos())
                self.xOffset = pos.x() - self.AlexaAppObjects[self.LastRectHover].RectX
                self.yOffset = pos.y() - self.AlexaAppObjects[self.LastRectHover].RectY

            #self.setCursor(QCursor(Qt.BlankCursor))
            self.pressed = True
            origin = QPoint(QCursor.pos())
            self.mouseOldX = origin.x()
            self.mouseOldY = origin.y()
            self.update()

    def mouseDoubleClickEvent(self, event):
        if self.DialogOpened is True:
            #self.BringWindowToFront()
            return

        if self.InsideRect is True:
            self.DialogOpened = True
            self.Dialog = AppTextDialog(self, self.LastRectHover, 0)
            self.Dialog.show()
            self.AppObjectFeedbackIndex = self.Dialog.objectIndex
            return

        if self.InsideRegion is True:
            self.DialogOpened = True
            self.Dialog = AppTextInRegionDialog(self, self.LastRectHover, 0)
            self.Dialog.show()
            self.AppObjectFeedbackIndex = self.Dialog.objectIndex
            return

    #mouse release event
    def mouseReleaseEvent(self, event):

        self.MovingAppObject = False

        if self.DialogOpened is True:
            #self.BringWindowToFront()
            return

        if self.InsideRect is True or self.InsideRegion is True:
            self.pressed = False
            #self.AlexaAppObjectsBackup[self.LastRectHover] = copy.deepcopy(self.AlexaAppObjects[self.LastRectHover])
            self.update()
            return

        #if(event.type() == QEvent.MouseButtonRelease):
        if event.button() == Qt.LeftButton:

            if self.DialogOpened is True:
                #self.BringWindowToFront()
                return
            self.pressed = False
            self.released = True

            width = self.mouseNewX - self.mouseOldX
            height = self.mouseNewY - self.mouseOldY

            rect = QRect(self.mouseOldX, self.mouseOldY, width, height)

            if (rect.width() >= 3 or rect.width() <= -3) and (rect.height() >= 3 or rect.height() <= -3):
                AlexaObject = AlexaAppTextPlus1()

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

                if self.CropLabel is False and self.CropRegion is False:

                    #AlexaObject.ObjH = height
                    #AlexaObject.ObjW = width
                    AlexaObject.ObjH = h
                    AlexaObject.ObjW = w
                    AlexaObject.HeightTollerance = 10
                    AlexaObject.WidthTollerance = 10
                    AlexaObject.RectX = x
                    AlexaObject.RectY = y

                    self.AlexaAppObjects.append(AlexaObject)
                    #self.AlexaAppObjectsBackup.append(AlexaObject)
                    self.AlexaAppObjectsBackup.append(copy.deepcopy(AlexaObject))
                    self.AlexaAppObjectsDeleted = []

                    ##self.rectObjCollection.append(rect)
                    ##self.rectObjCollectionDeleted = []

                    self.DialogOpened = True

                    #self.Dialog = AppObjDialog(self, len(self.AlexaAppObjects)-1)
                    self.Dialog = AppTextDialog(self, len(self.AlexaAppObjects)-1, 0)
                    self.Dialog.show()
                    self.AppObjectFeedbackIndex = self.Dialog.objectIndex

                elif self.CropRegion is True:
                    self.AlexaAppObjects[self.AppObjectFeedbackIndex].CropRegionX = x - self.AlexaAppObjects[self.AppObjectFeedbackIndex].RectX
                    self.AlexaAppObjects[self.AppObjectFeedbackIndex].CropRegionY = y - self.AlexaAppObjects[self.AppObjectFeedbackIndex].RectY
                    self.AlexaAppObjects[self.AppObjectFeedbackIndex].CropRegionWidth = w
                    self.AlexaAppObjects[self.AppObjectFeedbackIndex].CropRegionHeight = h

                    self.DialogOpened = True
                    self.Dialog = AppTextInRegionDialog(self, len(self.AlexaAppObjects)-1, 0)
                    self.Dialog.show()
                    self.AppObjectFeedbackIndex = self.Dialog.objectIndex

                    self.CropRegion = False
                #ui = Ui_Dialog()
                #ui.setupUi(Dialog)
                #self.Dialog.show()

                #if sys.platform == 'win32':
                    #self.DialogHwnd = win32self, textgui.GetForegroundWindow()

            self.update()
            #self.closeExtended()

    def keyPressEvent(self, event):

        if self.DialogOpened is True:
            #self.BringWindowToFront()
            return

        if event.modifiers() == Qt.ControlModifier and self.InsideRect is True:
            self.AdjustOnlyHeightTollerance = True

        if event.modifiers() == Qt.AltModifier and self.InsideRect is True:
            self.AdjustOnlyWidthTollerance = True

        if event.modifiers() == Qt.ControlModifier and event.key() == Qt.Key_Z:

            if len(self.AlexaAppObjects) > 0:

                self.AlexaAppObjectsDeleted.append(self.AlexaAppObjects[-1])
                self.AlexaAppObjectsBackupDeleted.append(self.AlexaAppObjectsBackup[-1])

                del self.AlexaAppObjects[-1]
                del self.AlexaAppObjectsBackup[-1]

                self.update()

        if event.modifiers() == Qt.ControlModifier and event.key() == Qt.Key_Y:

            if len(self.AlexaAppObjectsDeleted) > 0:

                self.AlexaAppObjects.append(self.AlexaAppObjectsDeleted[-1])
                self.AlexaAppObjectsBackup.append(self.AlexaAppObjectsBackupDeleted[-1])

                del self.AlexaAppObjectsDeleted[-1]
                del self.AlexaAppObjectsBackupDeleted[-1]
                #self.AlexaAppObjects = []

                self.update()
        if event.key() == Qt.Key_Escape:
            self.closeExtended()

    def keyReleaseEvent(self, event):

        #print event.key()
        if event.key() == Qt.Key_Control:
        #if event.modifiers() == Qt.ControlModifier:
            self.AdjustOnlyHeightTollerance = False

        if event.key() == Qt.Key_Alt:
            self.AdjustOnlyWidthTollerance = False

    def closeExtended(self):

        if self.plugin.undockWindowOpened is True:
            self.plugin.undockWindow.setVisible(True)
        elif sys.platform == 'win32':
            toplist = []
            winlist = []

            def enum_callback(hwnd, results):
                winlist.append((hwnd, win32gui.GetWindowText(hwnd)))
            win32gui.EnumWindows(enum_callback, toplist)

            firefox = [(hwnd, title) for hwnd, title in
                winlist if 'exa-ide' in title.lower() and 'about' not in title.lower() and 'exa tool' not in title.lower()]
            # just grab the first window that matches
            #firefox = firefox[0]
            for ninja in firefox:
                win32gui.ShowWindow(ninja[0], win32con.SW_SHOW)
                #print str(ninja[0]) + " " + ninja[1]

        SERVICE_NAME = "editor"
        editor_service = self.plugin.locator.get_service(SERVICE_NAME)
        #print "EDITO:",editor_service.get_editor_path()

        #print editor_service.get_lines_count()

        curLineText = editor_service.get_current_line_text()

        if editor_service.use_tab() is False:
            leadingSpaceNumber = len(curLineText) - len(curLineText.lstrip(' '))
            tabChar = ' ' * editor_service.get_indentation()
        else:
            leadingSpaceNumber = len(curLineText) - len(curLineText.lstrip('\t'))
            tabChar = '\t'

        if editor_service.use_tab() is False:
            leadingSpaceNumber = len(curLineText) - len(curLineText.lstrip(' '))
        else:
            leadingSpaceNumber = len(curLineText) - len(curLineText.lstrip('\t'))

        leadingChar = ""

        if editor_service.use_tab() is False:
            for x in range(leadingSpaceNumber):
                leadingChar = leadingChar + " "
        else:
            for x in range(leadingSpaceNumber):
                leadingChar = leadingChar + "\t"

        for alexaAppObject in self.AlexaAppObjects:

            #maxLineLen = 0
            #commentLine = ""
            description = ""

            if alexaAppObject.Name is not None and alexaAppObject.Name != "":
                #objName = alexaAppObject.Name.replace(" ", "")
                objName = alexaAppObject.Name
            else:
                objName = "object" + str(self.plugin.AlexaAppObjCnt)

            editor_service.insert_text("    #AppText: " + objName)
            editor_service.insert_text(os.linesep)

            if alexaAppObject.Description != "":

                description = alexaAppObject.Description.splitlines(True)
                editor_service.insert_text(leadingChar + "\'\'\'")
                editor_service.insert_text(os.linesep)
                editor_service.insert_text(leadingChar + "Description:")
                editor_service.insert_text(os.linesep)
                for line in description:
                    editor_service.insert_text(leadingChar + line)
                editor_service.insert_text(os.linesep)
                editor_service.insert_text(leadingChar + "\'\'\'")
                editor_service.insert_text(os.linesep)

            editor_service.insert_text(leadingChar + objName + " = AppText()")
            editor_service.insert_text(os.linesep)

            editor_service.insert_text(leadingChar + objName + ".Name = \"" + objName + "\"")
            editor_service.insert_text(os.linesep)

            editor_service.insert_text(leadingChar + objName + ".Height = " + str(alexaAppObject.ObjH))
            editor_service.insert_text(os.linesep)
            editor_service.insert_text(leadingChar + objName + ".Width = " + str(alexaAppObject.ObjW))
            editor_service.insert_text(os.linesep)
            editor_service.insert_text(leadingChar + objName + ".HeightTollerance = " + str(alexaAppObject.HeightTollerance))
            editor_service.insert_text(os.linesep)
            editor_service.insert_text(leadingChar + objName + ".WidthTollerance = " + str(alexaAppObject.WidthTollerance))
            editor_service.insert_text(os.linesep)

            if alexaAppObject.ImageBinarize is True:
                editor_service.insert_text(leadingChar + objName + ".ImageBinarize = True")
                editor_service.insert_text(os.linesep)
                editor_service.insert_text(leadingChar + objName + ".ImageBrightness = " + str(alexaAppObject.ImageBrightness))
                editor_service.insert_text(os.linesep)
                editor_service.insert_text(leadingChar + objName + ".ImageContrast = " + str(alexaAppObject.ImageContrast))
                editor_service.insert_text(os.linesep)

            if alexaAppObject.Text != "":
                editor_service.insert_text(leadingChar + objName + ".Text = \"" + alexaAppObject.Text + "\"")
                editor_service.insert_text(os.linesep)
                editor_service.insert_text(leadingChar + objName + ".Language = \"" + alexaAppObject.Language + "\"")
                editor_service.insert_text(os.linesep)

            if alexaAppObject.Binarize is True:
                editor_service.insert_text(leadingChar + objName + ".Binarize = True")
                editor_service.insert_text(os.linesep)
                editor_service.insert_text(leadingChar + objName + ".Brightness = " + str(alexaAppObject.Brightness))
                editor_service.insert_text(os.linesep)
                editor_service.insert_text(leadingChar + objName + ".Contrast = " + str(alexaAppObject.Contrast))
                editor_service.insert_text(os.linesep)

            if alexaAppObject.OcrWhiteList != Ocr.WhiteList:
                editor_service.insert_text(leadingChar + "Ocr.WhiteList = \"" + alexaAppObject.OcrWhiteList + "\"")
                editor_service.insert_text(os.linesep)

            timeOutTime = 15
            if alexaAppObject.EnablePerfData is True:
                timeOutTime = timeOutTime + alexaAppObject.PerfCriticalLevel

            editor_service.insert_text(leadingChar + "performance = " + objName + ".Bind(" + str(timeOutTime) + ")")
            editor_service.insert_text(os.linesep)

            if alexaAppObject.EnablePerfData is True:
                editor_service.insert_text(leadingChar + "NagiosUtils.AddPerformanceData(\"" + objName + "\", performance, " + str(alexaAppObject.PerfWarningLevel) + ", " + str(alexaAppObject.PerfCriticalLevel) + ")")
                editor_service.insert_text(os.linesep)

            if alexaAppObject.UseMouse is True or alexaAppObject.UseKeyboard is True or\
            alexaAppObject.CropRegionX != 0 or alexaAppObject.CropRegionY != 0 or alexaAppObject.CropRegionHeight != 0 or alexaAppObject.CropRegionWidth != 0:
                editor_service.insert_text(leadingChar + "if " + objName + ".TimeOut is False:")
                editor_service.insert_text(os.linesep)
            else:
                editor_service.insert_text(leadingChar + "if " + objName + ".TimeOut is False:")
                editor_service.insert_text(os.linesep)
                editor_service.insert_text(leadingChar + tabChar + "pass")
                editor_service.insert_text(os.linesep)

            if alexaAppObject.Click is True and alexaAppObject.UseMouse is True:
                editor_service.insert_text(leadingChar + tabChar + "Mouse.Click(" + objName + ".x + (" + objName + ".Width / 2), " + objName + ".y + (" + objName + ".Height / 2))")
                editor_service.insert_text(os.linesep)

            if alexaAppObject.DoubleClick is True and alexaAppObject.UseMouse is True:
                editor_service.insert_text(leadingChar + tabChar + "Mouse.DoubleClick(" + objName + ".x + (" + objName + ".Width / 2), " + objName + ".y + (" + objName + ".Height / 2))")
                editor_service.insert_text(os.linesep)

            if alexaAppObject.UseKeyboard is True:
                editor_service.insert_text(leadingChar + tabChar + "Keyboard.InsertText(\"" + alexaAppObject.InsertText + "\")")
                editor_service.insert_text(os.linesep)

            if alexaAppObject.CropRegionX != 0 or alexaAppObject.CropRegionY != 0 or alexaAppObject.CropRegionHeight != 0 or alexaAppObject.CropRegionWidth != 0:

                if alexaAppObject.CropRegionX < 0:
                    cropRegionX = -alexaAppObject.CropRegionX
                    cropOperatorX = "-"
                else:
                    cropRegionX = alexaAppObject.CropRegionX
                    cropOperatorX = "+"

                if alexaAppObject.CropRegionY < 0:
                    cropRegionY = -alexaAppObject.CropRegionY
                    cropOperatorY = "-"
                else:
                    cropRegionY = alexaAppObject.CropRegionY
                    cropOperatorY = "+"

                editor_service.insert_text(leadingChar + tabChar + "SearchRegion.Bind(" + objName + ".ObjX " + cropOperatorX + " " + str(cropRegionX) + ", " + objName + ".ObjY " + cropOperatorY + " " + str(cropRegionY) + ", " +
                str(alexaAppObject.CropRegionWidth) + ", " + str(alexaAppObject.CropRegionHeight) + ")")
                editor_service.insert_text(os.linesep)

            editor_service.insert_text(leadingChar + "elif " + objName + ".TimeOut is True and ExitOnError is True:")
            editor_service.insert_text(os.linesep)
            editor_service.insert_text(leadingChar + tabChar + "Finish()")
            editor_service.insert_text(os.linesep)

            if alexaAppObject.OcrWhiteList != Ocr.WhiteList:
                editor_service.insert_text(leadingChar + "Ocr.WhiteList = \"" + Ocr.WhiteList + "\"")
                editor_service.insert_text(os.linesep)

            editor_service.insert_text(leadingChar + "#end...")
            editor_service.insert_text(os.linesep)

            self.plugin.AlexaAppObjCnt = self.plugin.AlexaAppObjCnt + 1

            if alexaAppObject.CropRegionX != 0 or alexaAppObject.CropRegionY != 0 or alexaAppObject.CropRegionHeight != 0 or alexaAppObject.CropRegionWidth != 0:

                editor_service.insert_text(os.linesep)

                description = ""

                if alexaAppObject.AppText.Name is not None and alexaAppObject.AppText.Name != "":
                    #objName = alexaAppObject.AppText.Name.replace(" ", "")
                    objName = alexaAppObject.AppText.Name
                else:
                    objName = "object" + str(self.plugin.AlexaAppObjCnt)

                editor_service.insert_text(leadingChar + "    #AppText: " + objName)
                editor_service.insert_text(os.linesep)

                if alexaAppObject.AppText.Description != "":

                    description = alexaAppObject.AppText.Description.splitlines(True)
                    editor_service.insert_text(leadingChar + "\'\'\'")
                    editor_service.insert_text(os.linesep)
                    editor_service.insert_text(leadingChar + "Description:")
                    editor_service.insert_text(os.linesep)
                    for line in description:
                        editor_service.insert_text(leadingChar + line)
                    editor_service.insert_text(os.linesep)
                    editor_service.insert_text(leadingChar + "\'\'\'")
                    editor_service.insert_text(os.linesep)

                editor_service.insert_text(leadingChar + objName + " = AppText()")
                editor_service.insert_text(os.linesep)

                editor_service.insert_text(leadingChar + objName + ".Name = \"" + objName + "\"")
                editor_service.insert_text(os.linesep)

                if alexaAppObject.AppText.Text != "":
                    editor_service.insert_text(leadingChar + objName + ".Text = \"" + alexaAppObject.AppText.Text + "\"")
                    editor_service.insert_text(os.linesep)
                    editor_service.insert_text(leadingChar + objName + ".Language = \"" + alexaAppObject.AppText.Language + "\"")
                    editor_service.insert_text(os.linesep)

                if alexaAppObject.AppText.Binarize is True:
                    editor_service.insert_text(leadingChar + objName + ".Binarize = True")
                    editor_service.insert_text(os.linesep)
                    editor_service.insert_text(leadingChar + objName + ".Brightness = " + str(alexaAppObject.AppText.Brightness))
                    editor_service.insert_text(os.linesep)
                    editor_service.insert_text(leadingChar + objName + ".Contrast = " + str(alexaAppObject.AppText.Contrast))
                    editor_service.insert_text(os.linesep)

                if alexaAppObject.AppText.OcrWhiteList != Ocr.WhiteList:
                    editor_service.insert_text(leadingChar + "Ocr.WhiteList = \"" + alexaAppObject.AppText.OcrWhiteList + "\"")
                    editor_service.insert_text(os.linesep)

                timeOutTime = 15
                if alexaAppObject.AppText.EnablePerfData is True:
                    timeOutTime = timeOutTime + alexaAppObject.AppText.PerfCriticalLevel

                editor_service.insert_text(leadingChar + "performance = " + objName + ".Bind(" + str(timeOutTime) + ")")
                editor_service.insert_text(os.linesep)

                if alexaAppObject.AppText.EnablePerfData is True:
                    editor_service.insert_text(leadingChar + "NagiosUtils.AddPerformanceData(\"" + objName + "\", performance, " + str(alexaAppObject.AppText.PerfWarningLevel) + ", " + str(alexaAppObject.AppText.PerfCriticalLevel) + ")")
                    editor_service.insert_text(os.linesep)

                if alexaAppObject.AppText.UseMouse is True or alexaAppObject.AppText.UseKeyboard is True:
                    editor_service.insert_text(leadingChar + "if " + objName + ".TimeOut is False:")
                    editor_service.insert_text(os.linesep)
                else:
                    editor_service.insert_text(leadingChar + "if " + objName + ".TimeOut is False:")
                    editor_service.insert_text(os.linesep)
                    editor_service.insert_text(leadingChar + tabChar + "pass")
                    editor_service.insert_text(os.linesep)

                if alexaAppObject.AppText.Click is True and alexaAppObject.AppText.UseMouse is True:
                    editor_service.insert_text(leadingChar + tabChar + "Mouse.Click(" + objName + ".x + (" + objName + ".Width / 2), " + objName + ".y + (" + objName + ".Height / 2))")
                    editor_service.insert_text(os.linesep)

                if alexaAppObject.AppText.DoubleClick is True and alexaAppObject.AppText.UseMouse is True:
                    editor_service.insert_text(leadingChar + tabChar + "Mouse.DoubleClick(" + objName + ".x + (" + objName + ".Width / 2), " + objName + ".y + (" + objName + ".Height / 2))")
                    editor_service.insert_text(os.linesep)

                if alexaAppObject.AppText.UseKeyboard is True:
                    editor_service.insert_text(leadingChar + tabChar + "Keyboard.InsertText(\"" + alexaAppObject.AppText.InsertText + "\")")
                    editor_service.insert_text(os.linesep)

                editor_service.insert_text(leadingChar + "elif " + objName + ".TimeOut is True and ExitOnError is True:")
                editor_service.insert_text(os.linesep)
                editor_service.insert_text(leadingChar + tabChar + "Finish()")
                editor_service.insert_text(os.linesep)

                if alexaAppObject.AppText.OcrWhiteList != Ocr.WhiteList:
                    editor_service.insert_text(leadingChar + "Ocr.WhiteList = \"" + Ocr.WhiteList + "\"")
                    editor_service.insert_text(os.linesep)

                editor_service.insert_text(leadingChar + "SearchRegion.Unbind()")
                editor_service.insert_text(os.linesep)

                editor_service.insert_text(leadingChar + "#end...")
                editor_service.insert_text(os.linesep)

                self.plugin.AlexaAppObjCnt = self.plugin.AlexaAppObjCnt + 1

            editor_service.insert_text(os.linesep)
            editor_service.insert_text(leadingChar)

        #print editor_service.get_text()
        self.close()

    def DoBinarizeLabel(self, brightness, contrast):
        #print brightness, contrast

        PilImage2 = self.OriginalScreenshot.copy()

        left = self.AlexaAppObjects[self.AppObjectFeedbackIndex].RectX
        top = self.AlexaAppObjects[self.AppObjectFeedbackIndex].RectY
        width = self.AlexaAppObjects[self.AppObjectFeedbackIndex].Width
        height = self.AlexaAppObjects[self.AppObjectFeedbackIndex].Height
        box = (left, top, left + width, top + height)

        region = PilImage2.crop(box)

        #region.save("c:\\region.png")

        enhancer = ImageEnhance.Brightness(region)
        region = enhancer.enhance(brightness)
        enhancer = ImageEnhance.Contrast(region)
        region = enhancer.enhance(contrast)

        #PilImage2.paste(region, box)

        cv_im = cv.CreateImageHeader(region.size, cv.IPL_DEPTH_8U, 3)
        cv.SetData(cv_im, region.tostring())
        mat = cv.GetMat(cv_im)
        img = numpy.asarray(mat)
        img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
        gray_image = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        thresh = 100
        im_bw = cv2.threshold(gray_image, thresh, 255, cv2.THRESH_BINARY)[1]

        im = Image.fromarray(im_bw)
        PilImage2.paste(im, box)

        self.QtImage1 = ImageQt.ImageQt(PilImage2)
        self.QtImage2 = QImage(self.QtImage1)
        self.pixmap = QPixmap.fromImage(self.QtImage2)

        #self.pixmap.load("im_bw.png")
        self.update()

    def DoBinarizeRegion(self, brightness, contrast):

        PilImage2 = self.OriginalScreenshot.copy()

        x = self.AlexaAppObjects[self.AppObjectFeedbackIndex].RectX + self.AlexaAppObjects[self.AppObjectFeedbackIndex].CropRegionX
        y = self.AlexaAppObjects[self.AppObjectFeedbackIndex].RectY + self.AlexaAppObjects[self.AppObjectFeedbackIndex].CropRegionY
        w = self.AlexaAppObjects[self.AppObjectFeedbackIndex].RectX + self.AlexaAppObjects[self.AppObjectFeedbackIndex].CropRegionX + self.AlexaAppObjects[self.AppObjectFeedbackIndex].CropRegionWidth
        h = self.AlexaAppObjects[self.AppObjectFeedbackIndex].RectY + self.AlexaAppObjects[self.AppObjectFeedbackIndex].CropRegionY + self.AlexaAppObjects[self.AppObjectFeedbackIndex].CropRegionHeight
        box = (x, y, w, h)

        region = PilImage2.crop(box)

        #region.save("c:\\region.png")

        enhancer = ImageEnhance.Brightness(region)
        region = enhancer.enhance(brightness)
        enhancer = ImageEnhance.Contrast(region)
        region = enhancer.enhance(contrast)

        #PilImage2.paste(region, box)

        cv_im = cv.CreateImageHeader(region.size, cv.IPL_DEPTH_8U, 3)
        cv.SetData(cv_im, region.tostring())
        mat = cv.GetMat(cv_im)
        img = numpy.asarray(mat)
        img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
        gray_image = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        thresh = 100
        im_bw = cv2.threshold(gray_image, thresh, 255, cv2.THRESH_BINARY)[1]

        im = Image.fromarray(im_bw)
        PilImage2.paste(im, box)

        self.QtImage1 = ImageQt.ImageQt(PilImage2)
        self.QtImage2 = QImage(self.QtImage1)
        self.pixmap = QPixmap.fromImage(self.QtImage2)

        #self.pixmap.load("im_bw.png")
        self.update()

    def DoBinarizeImage(self, brightness, contrast):

        PilImage2 = self.OriginalScreenshot.copy()

        left = self.x()
        top = self.y()
        width = self.width()
        height = self.height()
        box = (left, top, left+width, top+height)

        region = PilImage2.crop(box)

        #region.save("c:\\region.png")

        enhancer = ImageEnhance.Brightness(region)
        region = enhancer.enhance(brightness)
        enhancer = ImageEnhance.Contrast(region)
        region = enhancer.enhance(contrast)

        #PilImage2.paste(region, box)

        cv_im = cv.CreateImageHeader(region.size, cv.IPL_DEPTH_8U, 3)
        cv.SetData(cv_im, region.tostring())
        mat = cv.GetMat(cv_im)
        img = numpy.asarray(mat)
        img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
        gray_image = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        thresh = 127
        im_bw = cv2.threshold(gray_image, thresh, 255, cv2.THRESH_BINARY)[1]
        im = Image.fromarray(im_bw)
        PilImage2.paste(im, box)
        #PilImage2.save("im_bw.png")self, text

        self.QtImage1 = ImageQt.ImageQt(PilImage2)
        self.QtImage2 = QImage(self.QtImage1)
        self.pixmap = QPixmap.fromImage(self.QtImage2)

        #self.pixmap.load("im_bw.png")
        self.update()

    def DoCanny(self):
        '''
        PilImage = Image.open('screenshot.png')

        cv_im = cv.CreateImageHeader(PilImage.size, cv.IPL_DEPTH_8U, 3)
        cv.SetData(cv_im, PilImage.tostring())

        mat = cv.GetMat(cv_im)
        img = numpy.asarray(mat)
        img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
        '''

        img = cv2.imread(self.plug_path + os.sep + 'tmp' + os.sep + 'screenshot.png')

        blue, green, red = cv2.split(img)

        # Run canny edge detection on each channel
        blue_edges = self.medianCanny(blue, 0.2, 0.3)
        green_edges = self.medianCanny(green, 0.2, 0.3)
        red_edges = self.medianCanny(red, 0.2, 0.3)

        # Join edges back into image
        edges = blue_edges | green_edges | red_edges

        cv2.imwrite(self.plug_path + os.sep + 'tmp' + os.sep + 'canny.png', edges)
        self.pixmap.load(self.plug_path + os.sep + 'tmp' + os.sep + 'canny.png')

    def medianCanny(self, img, thresh1, thresh2):
        median = numpy.median(img)
        img = cv2.Canny(img, int(thresh1 * median), int(thresh2 * median))
        return img


class AlexaAppTextPlus1(AppText, object):

    def __init__(self):
        super(AlexaAppTextPlus1, self).__init__()
        self.RectX = None
        self.RectY = None
        #self.OcrWhiteList = "'0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ&:/-_\,+()*.=[]<>@"
        self.OcrWhiteList = Ocr.WhiteList
        self.Click = False
        self.DoubleClick = False
        self.UseMouse = True
        self.UseKeyboard = False
        self.InsertText = ""
        self.CropRegionX = 0
        self.CropRegionY = 0
        self.CropRegionHeight = 0
        self.CropRegionWidth = 0
        self.Description = ""
        self.EnablePerfData = False
        self.PerfWarningLevel = 0
        self.PerfCriticalLevel = 0
        self.AppText = AlexaAppTextPlus2()
        self.AppTextBackup = AlexaAppTextPlus2()


class AlexaAppTextPlus2(AppText, object):

    def __init__(self):
        super(AlexaAppTextPlus2, self).__init__()
        self.OcrWhiteList = Ocr.WhiteList
        self.Click = False
        self.DoubleClick = False
        self.UseMouse = True
        self.UseKeyboard = False
        self.Description = ""
        self.EnablePerfData = False
        self.PerfWarningLevel = 0
        self.PerfCriticalLevel = 0
        self.InsertText = ""
