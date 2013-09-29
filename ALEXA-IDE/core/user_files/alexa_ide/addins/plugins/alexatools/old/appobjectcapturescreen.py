# -*- coding: UTF-8 -*-
#PYTHON
import os
import sys

import copy
#NINJA
from ninja_ide.tools import json_manager
from appobjectdialog import AppObjDialog

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


class AppObjectCaptureScreenshot(QWidget):
    def __init__(self, plugin):
        QWidget.__init__(self)

        self.plugin = plugin

        SERVICE_NAME = "editor"
        self.editor_service = self.plugin.locator.get_service(SERVICE_NAME)
        fullFileName = self.editor_service.get_editor_path()
        #from os.path import basename

        filePath = os.path.split(fullFileName)[0]
        fileName = os.path.split(fullFileName)[1]
        print os.path.splitext(fileName)[1]
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
        self.pixmap.load("screenshot.png")
        self.OriginalScreenshot = Image.open("screenshot.png")

        #store if mouse is pressed
        self.pressed = False
        self.released = False
        self.printLabelBorder = False

        self.InsideRect = False
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

    def UpdateLabelOfInterest(self):
        self.LabelOfInterest = []

        if self.AlexaAppObjects[self.AppObjectFeedbackIndex].Label.Width != 0 and self.AlexaAppObjects[self.AppObjectFeedbackIndex].Label.Height != 0:
            left = self.AlexaAppObjects[self.AppObjectFeedbackIndex].RectX + self.AlexaAppObjects[self.AppObjectFeedbackIndex].Label.OffsetX
            top = self.AlexaAppObjects[self.AppObjectFeedbackIndex].RectY + self.AlexaAppObjects[self.AppObjectFeedbackIndex].Label.OffsetY
            width = self.AlexaAppObjects[self.AppObjectFeedbackIndex].Label.Width
            height = self.AlexaAppObjects[self.AppObjectFeedbackIndex].Label.Height
            box = (left, top, left + width, top + height)
            self.LabelOfInterest.append(box)
        elif self.AlexaAppObjects[self.AppObjectFeedbackIndex].Label.Position == "top":
            self.AddLabelOfInterestTop()
        elif self.AlexaAppObjects[self.AppObjectFeedbackIndex].Label.Position == "left":
            self.AddLabelOfInterestLeft()
        elif self.AlexaAppObjects[self.AppObjectFeedbackIndex].Label.Position == "inside":
            self.AddLabelOfInterestInside()
        elif self.AlexaAppObjects[self.AppObjectFeedbackIndex].Label.Position == "right":
            self.AddLabelOfInterestRight()
        elif self.AlexaAppObjects[self.AppObjectFeedbackIndex].Label.Position == "":
            self.AddLabelOfInterestTop()
            self.AddLabelOfInterestLeft()
            self.AddLabelOfInterestInside()
            self.AddLabelOfInterestRight()

    def AddLabelOfInterestTop(self):
        left = self.AlexaAppObjects[self.AppObjectFeedbackIndex].RectX - 10
        top = self.AlexaAppObjects[self.AppObjectFeedbackIndex].RectY - (self.AlexaAppObjects[self.AppObjectFeedbackIndex].Height + (self.AlexaAppObjects[self.AppObjectFeedbackIndex].Height / 2))
        width = self.AlexaAppObjects[self.AppObjectFeedbackIndex].Width + 20
        height = (self.AlexaAppObjects[self.AppObjectFeedbackIndex].Height + (self.AlexaAppObjects[self.AppObjectFeedbackIndex].Height / 2))
        box = (left, top, left + width, top + height)
        self.LabelOfInterest.append(box)

    def AddLabelOfInterestLeft(self):
        left = self.AlexaAppObjects[self.AppObjectFeedbackIndex].RectX - (self.AlexaAppObjects[self.AppObjectFeedbackIndex].Width * 2)
        top = self.AlexaAppObjects[self.AppObjectFeedbackIndex].RectY
        width = self.AlexaAppObjects[self.AppObjectFeedbackIndex].Width * 2
        height = self.AlexaAppObjects[self.AppObjectFeedbackIndex].Height
        box = (left, top, left + width, top + height)
        self.LabelOfInterest.append(box)

    def AddLabelOfInterestInside(self):
        left = self.AlexaAppObjects[self.AppObjectFeedbackIndex].RectX
        top = self.AlexaAppObjects[self.AppObjectFeedbackIndex].RectY
        width = self.AlexaAppObjects[self.AppObjectFeedbackIndex].Width
        height = self.AlexaAppObjects[self.AppObjectFeedbackIndex].Height
        box = (left, top, left + width, top + height)
        self.LabelOfInterest.append(box)

    def AddLabelOfInterestRight(self):
        left = self.AlexaAppObjects[self.AppObjectFeedbackIndex].RectX + self.AlexaAppObjects[self.AppObjectFeedbackIndex].Width
        top = self.AlexaAppObjects[self.AppObjectFeedbackIndex].RectY
        width = self.AlexaAppObjects[self.AppObjectFeedbackIndex].Width * 2
        height = self.AlexaAppObjects[self.AppObjectFeedbackIndex].Height
        box = (left, top, left + width, top + height)
        self.LabelOfInterest.append(box)

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
            AlexaAppObject.Width + (AlexaAppObject.WidthTollerance * 2),
            AlexaAppObject.Height + (AlexaAppObject.HeightTollerance * 2))

        if AlexaAppObject.Width >= (AlexaAppObject.WidthTollerance * 2) and AlexaAppObject.Height >= (AlexaAppObject.HeightTollerance * 2):
            InnerPath = QPainterPath()

            InnerPath.addRect(AlexaAppObject.RectX + AlexaAppObject.WidthTollerance,
                AlexaAppObject.RectY + AlexaAppObject.HeightTollerance,
                AlexaAppObject.Width - (AlexaAppObject.WidthTollerance * 2),
                AlexaAppObject.Height - (AlexaAppObject.HeightTollerance * 2))

            FillPath = OuterPath.subtracted(InnerPath)
            paint.fillPath(FillPath, QColor(255, 0, 255, 130))
        else:
            paint.fillPath(OuterPath, QColor(255, 0, 255, 130))

        pen.setWidth(1)
        pen.setStyle(Qt.DashLine)
        paint.setPen(pen)

        paint.drawRect(AlexaAppObject.RectX - AlexaAppObject.WidthTollerance,
            AlexaAppObject.RectY - AlexaAppObject.HeightTollerance,
            AlexaAppObject.Width + (AlexaAppObject.WidthTollerance * 2),
            AlexaAppObject.Height + (AlexaAppObject.HeightTollerance * 2))
        pen.setStyle(Qt.SolidLine)
        paint.setPen(pen)

        #paint.drawRect(x, y, AlexaAppObject.Width, AlexaAppObject.Height)

        pen.setStyle(Qt.DashLine)
        paint.setPen(pen)
        if AlexaAppObject.Width >= (AlexaAppObject.WidthTollerance * 2) and AlexaAppObject.Height >= (AlexaAppObject.HeightTollerance * 2):
            paint.drawRect(AlexaAppObject.RectX + AlexaAppObject.WidthTollerance,
                AlexaAppObject.RectY + AlexaAppObject.HeightTollerance,
                AlexaAppObject.Width - (AlexaAppObject.WidthTollerance * 2),
                AlexaAppObject.Height - (AlexaAppObject.HeightTollerance * 2))
        elif AlexaAppObject.Width >= (AlexaAppObject.WidthTollerance * 2):
            paint.drawLine(AlexaAppObject.RectX + AlexaAppObject.WidthTollerance,
                AlexaAppObject.RectY + (AlexaAppObject.Height / 2),
                AlexaAppObject.RectX + AlexaAppObject.Width - AlexaAppObject.WidthTollerance,
                AlexaAppObject.RectY + (AlexaAppObject.Height / 2))
            #paint.drawLine(AlexaAppObject.RectX + 8, AlexaAppObject.RectY + (h/2), AlexaAppObject.RectX + 8 + 1, AlexaAppObject.RectY + (h/2))
            #paint.drawLine(AlexaAppObject.RectX + w - 8, AlexaAppObject.RectY + (h/2), AlexaAppObject.RectX + w - 8, AlexaAppObject.RectY + (h/2))
            #pen.setStyle(Qt.SolidLine)
            #paint.setPen(pen)
            #paint.drawLine(AlexaAppObject.RectX + 8, y, AlexaAppObject.RectX + 8, AlexaAppObject.RectY + h)
        elif AlexaAppObject.Height >= (AlexaAppObject.HeightTollerance * 2):
            paint.drawLine(AlexaAppObject.RectX + (AlexaAppObject.Width / 2),
                AlexaAppObject.RectY + AlexaAppObject.HeightTollerance,
                AlexaAppObject.RectX + (AlexaAppObject.Width / 2),
                AlexaAppObject.RectY + AlexaAppObject.Height - AlexaAppObject.HeightTollerance)
        else:
            paint.drawLine(AlexaAppObject.RectX + (AlexaAppObject.Width / 2),
                AlexaAppObject.RectY + (AlexaAppObject.Height / 2),
                AlexaAppObject.RectX + (AlexaAppObject.Width / 2),
                AlexaAppObject.RectY + (AlexaAppObject.Height / 2))

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
        #ciclo per disegno rettangoli e tooltip
        for appObject in self.AlexaAppObjects:

            pen.setBrush(QColor(255, 0, 0, 255))
            pen.setWidth(1)
            paint.setPen(pen)

            if self.printLabelBorder is True:
                for box in self.LabelOfInterest:
                    pen.setWidth(1)
                    pen.setStyle(Qt.DashLine)
                    if self.indexFound is not None and self.indexFound == self.AppObjectFeedbackIndex:
                        pen.setBrush(QColor(112, 81, 213, 255))
                    else:
                        pen.setBrush(QColor(255, 0, 0, 255))
                    paint.setPen(pen)
                    newRect = QRect(box[0], box[1], box[2] - box[0], box[3] - box[1])
                    paint.drawRect(newRect)

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
                    "Height: " + str(appObject.Height) +
                    ", Width: " + str(appObject.Width))
                '''

                #appObject.Height = 200

                #self.PaintRectHover(paint, x, y, w, h)
                self.PaintRectTollerance(paint, appObject)

            elif (center.x() > appObject.RectX and
                center.x() < appObject.Width + appObject.RectX and
                center.y() > appObject.RectY and
                center.y() < appObject.Height + appObject.RectY and
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
                        appObject.Width,
                        appObject.Height,
                        QBrush(QColor(0, 255, 0, 130)))
                else:
                    paint.fillRect(appObject.RectX,
                        appObject.RectY,
                        appObject.Width,
                        appObject.Height,
                        QBrush(QColor(255, 0, 255, 130)))

                newRect = QRect(appObject.RectX,
                    appObject.RectY,
                    appObject.Width,
                    appObject.Height)

                paint.drawRect(newRect)

                #self.PaintRectHover(paint, x, y, appObject)

                self.InsideRect = True
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
                        appObject.Width,
                        appObject.Height,
                        QBrush(QColor(0, 255, 0, 130)))
                else:
                    paint.fillRect(appObject.RectX,
                        appObject.RectY,
                        appObject.Width,
                        appObject.Height,
                        QBrush(QColor(255, 0, 255, 130)))
                '''
                paint.fillRect(appObject.RectX,
                    appObject.RectY,
                    appObject.Width,
                    appObject.Height,
                    QBrush(QColor(255, 0, 255, 100)))
                '''
                newRect = QRect(appObject.RectX,
                    appObject.RectY,
                    appObject.Width,
                    appObject.Height)

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

            if appObject.Label.OffsetX != 0 and appObject.Label.OffsetY != 0 and appObject.Label.Width != 0 and appObject.Label.Height != 0:
                '''
                x = appObject.RectX
                y = appObject.RectY
                w = appObject.Width
                h = appObject.Height
                #paint.setRenderHint(QPainter.SmoothPixmapTransform)
                pen.setStyle(Qt.DashLine)
                #pen.setStyle(Qt.DashDotLine)
                #pen.setDashPattern([1, 1])
                pen.setBrush(QColor(255, 0, 0, 255))
                pen.setWidth(1)
                paint.setPen(pen)
                newRect = QRect(x + appObject.Label.OffsetX,
                    y + appObject.Label.OffsetY,
                    appObject.Label.Width,
                    appObject.Label.Height)
                paint.drawRect(newRect)
                '''

            cnt = cnt + 1

        #paint.restore()
        self.mouseNewX = center.x()
        self.mouseNewY = center.y()

        if self.InsideRect is True:
            if self.DialogOpened is True:
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

        print self.LastRectHover
        print self.InsideRect

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
        if self.DialogOpened is True:
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
            self.Dialog = AppObjDialog(self, self.LastRectHover, 0)
            self.Dialog.show()
            self.AppObjectFeedbackIndex = self.Dialog.objectIndex
            return

    #mouse release event
    def mouseReleaseEvent(self, event):

        self.MovingAppObject = False

        if self.DialogOpened is True:
            #self.BringWindowToFront()
            return

        if self.InsideRect is True:
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
                AlexaObject = AlexaAppObjectPlus()

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

                    #AlexaObject.Height = height
                    #AlexaObject.Width = width
                    AlexaObject.Height = h
                    AlexaObject.Width = w
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
                    self.Dialog = AppObjDialog(self, len(self.AlexaAppObjects)-1, 0)
                    self.Dialog.show()
                    self.AppObjectFeedbackIndex = self.Dialog.objectIndex
                elif self.CropLabel is True:

                    self.AlexaAppObjects[self.AppObjectFeedbackIndex].Label.OffsetX = x - self.AlexaAppObjects[self.AppObjectFeedbackIndex].RectX
                    self.AlexaAppObjects[self.AppObjectFeedbackIndex].Label.OffsetY = y - self.AlexaAppObjects[self.AppObjectFeedbackIndex].RectY
                    self.AlexaAppObjects[self.AppObjectFeedbackIndex].Label.Width = w
                    self.AlexaAppObjects[self.AppObjectFeedbackIndex].Label.Height = h

                    self.DialogOpened = True
                    #self.Dialog = AppObjDialog(self, len(self.AlexaAppObjects)-1)
                    self.Dialog = AppObjDialog(self, len(self.AlexaAppObjects)-1, 1)
                    self.Dialog.show()
                    self.AppObjectFeedbackIndex = self.Dialog.objectIndex
                    self.CropLabel = False
                elif self.CropRegion is True:
                    self.AlexaAppObjects[self.AppObjectFeedbackIndex].CropRegionX = x - self.AlexaAppObjects[self.AppObjectFeedbackIndex].RectX
                    self.AlexaAppObjects[self.AppObjectFeedbackIndex].CropRegionY = y - self.AlexaAppObjects[self.AppObjectFeedbackIndex].RectY
                    self.AlexaAppObjects[self.AppObjectFeedbackIndex].CropRegionWidth = w
                    self.AlexaAppObjects[self.AppObjectFeedbackIndex].CropRegionHeight = h
                    self.DialogOpened = True
                    #self.Dialog = AppObjDialog(self, len(self.AlexaAppObjects)-1)
                    self.Dialog = AppObjDialog(self, len(self.AlexaAppObjects)-1, 2)
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

        if sys.platform == 'win32':
            toplist = []
            winlist = []

            def enum_callback(hwnd, results):
                winlist.append((hwnd, win32gui.GetWindowText(hwnd)))
            win32gui.EnumWindows(enum_callback, toplist)
            firefox = [(hwnd, title) for hwnd, title in
                winlist if 'exa-ide' in title.lower() and 'about' not in title.lower()]
            # just grab the first window that matches
            #firefox = firefox[0]
            for ninja in firefox:
                win32gui.ShowWindow(ninja[0], win32con.SW_SHOW)
                print str(ninja[0]) + " " + ninja[1]

        SERVICE_NAME = "editor"
        editor_service = self.plugin.locator.get_service(SERVICE_NAME)
        #print "EDITO:",editor_service.get_editor_path()

        #print editor_service.get_lines_count()

        for alexaAppObject in self.AlexaAppObjects:

            #maxLineLen = 0
            #commentLine = ""
            description = ""

            if alexaAppObject.Name is not None and alexaAppObject.Name != "":
                #objName = alexaAppObject.Name.replace(" ", "")
                objName = alexaAppObject.Name
            else:
                objName = "object" + str(self.plugin.AlexaAppObjCnt)

            editor_service.insert_text("#   AppObject: " + objName)
            editor_service.insert_text(os.linesep)

            if alexaAppObject.Description != "":

                description = alexaAppObject.Description.splitlines(True)
                editor_service.insert_text("'''")
                editor_service.insert_text(os.linesep)
                editor_service.insert_text("Description:")
                editor_service.insert_text(os.linesep)
                for line in description:
                    editor_service.insert_text(line)
                editor_service.insert_text(os.linesep)
                editor_service.insert_text("'''")
                editor_service.insert_text(os.linesep)

            editor_service.insert_text(objName + " = AppObject()")
            editor_service.insert_text(os.linesep)

            editor_service.insert_text(objName + ".Name = \"" + objName + "\"")
            editor_service.insert_text(os.linesep)

            editor_service.insert_text(objName + ".Height = " + str(alexaAppObject.Height))
            editor_service.insert_text(os.linesep)
            editor_service.insert_text(objName + ".Width = " + str(alexaAppObject.Width))
            editor_service.insert_text(os.linesep)
            editor_service.insert_text(objName + ".HeightTollerance = " + str(alexaAppObject.HeightTollerance))
            editor_service.insert_text(os.linesep)
            editor_service.insert_text(objName + ".WidthTollerance = " + str(alexaAppObject.WidthTollerance))
            editor_service.insert_text(os.linesep)

            if alexaAppObject.ImageBinarize is True:
                editor_service.insert_text(objName + ".ImageBinarize = True")
                editor_service.insert_text(os.linesep)
                editor_service.insert_text(objName + ".ImageBrightness = " + str(alexaAppObject.ImageBrightness))
                editor_service.insert_text(os.linesep)
                editor_service.insert_text(objName + ".ImageContrast = " + str(alexaAppObject.ImageContrast))
                editor_service.insert_text(os.linesep)

            if alexaAppObject.Label.Text != "":
                editor_service.insert_text(objName + ".Label.Text = \"" + alexaAppObject.Label.Text + "\"")
                editor_service.insert_text(os.linesep)
                editor_service.insert_text(objName + ".Label.Language = \"" + alexaAppObject.Label.Language + "\"")
                editor_service.insert_text(os.linesep)

            if alexaAppObject.Label.OffsetX != 0 and alexaAppObject.Label.OffsetY != 0 and alexaAppObject.Label.Width != 0 and alexaAppObject.Label.Height != 0:
                editor_service.insert_text(objName + ".Label.OffsetX = " + str(alexaAppObject.Label.OffsetX))
                editor_service.insert_text(os.linesep)
                editor_service.insert_text(objName + ".Label.OffsetY = " + str(alexaAppObject.Label.OffsetY))
                editor_service.insert_text(os.linesep)
                editor_service.insert_text(objName + ".Label.Width = " + str(alexaAppObject.Label.Width))
                editor_service.insert_text(os.linesep)
                editor_service.insert_text(objName + ".Label.Height = " + str(alexaAppObject.Label.Height))
                editor_service.insert_text(os.linesep)
            elif alexaAppObject.Label.Position != "":
                editor_service.insert_text(objName + ".Label.Position = \"" + alexaAppObject.Label.Position + "\"")
                editor_service.insert_text(os.linesep)

            if alexaAppObject.Label.Binarize is True:
                editor_service.insert_text(objName + ".Label.Binarize = True")
                editor_service.insert_text(os.linesep)
                editor_service.insert_text(objName + ".Label.Brightness = " + str(alexaAppObject.Label.Brightness))
                editor_service.insert_text(os.linesep)
                editor_service.insert_text(objName + ".Label.Contrast = " + str(alexaAppObject.Label.Contrast))
                editor_service.insert_text(os.linesep)

            if alexaAppObject.OcrWhiteList != Ocr.WhiteList:
                editor_service.insert_text("Ocr.WhiteList = \"" + alexaAppObject.OcrWhiteList + "\"")
                editor_service.insert_text(os.linesep)

            editor_service.insert_text("performance = " + objName + ".Bind(15)")
            editor_service.insert_text(os.linesep)

            if alexaAppObject.EnablePerfData is True:
                editor_service.insert_text("NagiosUtils.AddPerformanceData(\"" + objName + "\", performance, " + str(alexaAppObject.PerfWarningLevel) + ", " + str(alexaAppObject.PerfCriticalLevel) + ")")
                editor_service.insert_text(os.linesep)

            if alexaAppObject.Click is True and alexaAppObject.UseMouse is True:
                editor_service.insert_text("Mouse.Click(" + objName + ".x + (" + objName + ".Width / 2), " + objName + ".y + (" + objName + ".Height / 2))")
                editor_service.insert_text(os.linesep)

            if alexaAppObject.DoubleClick is True and alexaAppObject.UseMouse is True:
                editor_service.insert_text("Mouse.DoubleClick(" + objName + ".x + (" + objName + ".Width / 2), " + objName + ".y + (" + objName + ".Height / 2))")
                editor_service.insert_text(os.linesep)

            if alexaAppObject.UseKeyboard is True:
                editor_service.insert_text("Keyboard.InsertText(\"" + alexaAppObject.InsertText + "\")")
                editor_service.insert_text(os.linesep)

            if alexaAppObject.OcrWhiteList != Ocr.WhiteList:
                editor_service.insert_text("Ocr.WhiteList = \"" + Ocr.WhiteList + "\"")
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

                editor_service.insert_text("SearchRegion.Bind(" + objName + ".x " + cropOperatorX + " " + str(cropRegionX) + ", " + objName + ".y " + cropOperatorY + " " + str(cropRegionY) + ", " +
                str(alexaAppObject.CropRegionWidth) + ", " + str(alexaAppObject.CropRegionHeight) + ")")
                editor_service.insert_text(os.linesep)

            editor_service.insert_text("#end AppObject")
            editor_service.insert_text(os.linesep)
            editor_service.insert_text(os.linesep)

            '''
            editor_service.insert_text("mouseX = " + objName + ".x + (" + objName + ".Width / 2)")
            editor_service.insert_text(os.linesep)
            editor_service.insert_text("mouseY = " + objName + ".y + (" + objName + ".Height / 2)")
            editor_service.insert_text(os.linesep)

            editor_service.insert_text(os.linesep)
            #editor_service.insert_text('self, text')
            #editor_service.insert_text(os.linesep)
            '''
            self.plugin.AlexaAppObjCnt = self.plugin.AlexaAppObjCnt + 1
        #print editor_service.get_text()
        self.close()

    def DoBinarizeLabel(self, brightness, contrast):
        print brightness, contrast
        self.UpdateLabelOfInterest()

        PilImage2 = self.OriginalScreenshot.copy()

        for box in self.LabelOfInterest:

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

        img = cv2.imread('screenshot.png')

        blue, green, red = cv2.split(img)

        # Run canny edge detection on each channel
        blue_edges = self.medianCanny(blue, 0.2, 0.3)
        green_edges = self.medianCanny(green, 0.2, 0.3)
        red_edges = self.medianCanny(red, 0.2, 0.3)

        # Join edges back into image
        edges = blue_edges | green_edges | red_edges

        cv2.imwrite("canny.png", edges)
        self.pixmap.load("canny.png")

    def medianCanny(self, img, thresh1, thresh2):
        median = numpy.median(img)
        img = cv2.Canny(img, int(thresh1 * median), int(thresh2 * median))
        return img


class AlexaAppObjectPlus(AppObject, object):

    def __init__(self):
        super(AlexaAppObjectPlus, self).__init__()
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
