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
from appimagedialog import AppImgDialog
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


class AppImageCaptureScreenshot(QWidget):
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
        self.AlexaAppImagesBackup = []
        self.AlexaAppImagesBackupDeleted = []
        self.AlexaAppImages = []
        self.AlexaAppImagesDeleted = []

        self.AlexaAppObjectsBackup = []
        self.AlexaAppObjects = []

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
        for appImage in self.AlexaAppImages:

            pen.setBrush(QColor(255, 0, 0, 255))
            pen.setWidth(1)
            paint.setPen(pen)

            if (center.x() > appImage.RectX and
                center.x() < appImage.Width + appImage.RectX and
                center.y() > appImage.RectY and
                center.y() < appImage.Height + appImage.RectY and
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

                x = appImage.RectX
                y = appImage.RectY

                if self.indexFound is not None and self.indexFound == self.AppObjectFeedbackIndex and self.indexFound == cnt:
                    paint.fillRect(appImage.RectX,
                        appImage.RectY,
                        appImage.Width,
                        appImage.Height,
                        QBrush(QColor(0, 255, 0, 130)))
                else:
                    paint.fillRect(appImage.RectX,
                        appImage.RectY,
                        appImage.Width,
                        appImage.Height,
                        QBrush(QColor(255, 0, 255, 130)))

                newRect = QRect(appImage.RectX,
                    appImage.RectY,
                    appImage.Width,
                    appImage.Height)

                paint.drawRect(newRect)

                #self.PaintRectHover(paint, x, y, appObject)

                self.InsideRect = True
                self.LastRectHover = cnt
            elif (center.x() > appImage.RectX + appImage.CropRegionX and
                center.x() < appImage.RectX + appImage.CropRegionX + appImage.CropRegionWidth and
                center.y() > appImage.RectY + appImage.CropRegionY and
                center.y() < appImage.RectY + appImage.CropRegionY + appImage.CropRegionHeight and
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

                x = appImage.RectX
                y = appImage.RectY

                if self.indexFound is not None and self.indexFound == self.AppObjectFeedbackIndex and self.indexFound == cnt:
                    paint.fillRect(appImage.RectX,
                        appImage.RectY,
                        appImage.Width,
                        appImage.Height,
                        QBrush(QColor(0, 255, 0, 130)))
                else:
                    paint.fillRect(appImage.RectX,
                        appImage.RectY,
                        appImage.Width,
                        appImage.Height,
                        QBrush(QColor(255, 0, 255, 130)))

                newRect = QRect(appImage.RectX,
                    appImage.RectY,
                    appImage.Width,
                    appImage.Height)

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
                    paint.fillRect(appImage.RectX,
                        appImage.RectY,
                        appImage.Width,
                        appImage.Height,
                        QBrush(QColor(0, 255, 0, 130)))
                else:
                    paint.fillRect(appImage.RectX,
                        appImage.RectY,
                        appImage.Width,
                        appImage.Height,
                        QBrush(QColor(255, 0, 255, 130)))
                '''
                paint.fillRect(appImage.RectX,
                    appImage.RectY,
                    appImage.Width,
                    appImage.Height,
                    QBrush(QColor(255, 0, 255, 100)))
                '''
                newRect = QRect(appImage.RectX,
                    appImage.RectY,
                    appImage.Width,
                    appImage.Height)

                paint.drawRect(newRect)

            if appImage.CropRegionX != 0 and appImage.CropRegionY != 0 and appImage.CropRegionWidth != 0 and appImage.CropRegionHeight != 0:
                x = appImage.RectX
                y = appImage.RectY
                w = appImage.CropRegionWidth
                h = appImage.CropRegionHeight
                '''
                pen.setStyle(Qt.DashLine)
                pen.setBrush(QColor(0, 0, 255, 255))
                pen.setWidth(1)
                paint.setPen(pen)

                newRect = QRect(x + appImage.CropRegionX,
                    y + appImage.CropRegionY, w, h)
                paint.drawRect(newRect)

                '''
                pen.setStyle(Qt.SolidLine)
                pen.setBrush(QColor(0, 78, 255, 255))
                pen.setWidth(1)
                paint.setPen(pen)
                paint.fillRect(x + appImage.CropRegionX,
                    y + appImage.CropRegionY, w, h,
                    QBrush(QColor(100, 80, 155, 100)))

                newRect = QRect(x + appImage.CropRegionX,
                    y + appImage.CropRegionY, w, h)

                paint.drawRect(newRect)

                if self.indexFoundAppText is not None and self.indexFoundAppText == self.AppObjectFeedbackIndex and self.indexFoundAppText == cnt:
                    pen.setWidth(1)
                    pen.setStyle(Qt.DashLine)
                    pen.setBrush(QColor(255, 0, 255, 255))

                    paint.setPen(pen)
                    newRect = QRect(x + appImage.CropRegionX + appImage.AppText.x, y + appImage.CropRegionY + appImage.AppText.y, appImage.AppText.Width, appImage.AppText.Height)
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
                #self.AlexaAppImages[self.LastRectHover].width(),
                #self.AlexaAppImages[self.LastRectHover].height())
            self.AlexaAppImages[self.LastRectHover].RectX = pos.x() - self.xOffset
            self.AlexaAppImages[self.LastRectHover].RectY =  pos.y() - self.yOffset

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
                self.AlexaAppImages[self.LastRectHover].HeightTollerance = self.AlexaAppImages[self.LastRectHover].HeightTollerance + event.delta() / 120
                if self.AlexaAppImages[self.LastRectHover].HeightTollerance < 0:
                    self.AlexaAppImages[self.LastRectHover].HeightTollerance = 0
            elif self.AdjustOnlyWidthTollerance is True:
                self.AlexaAppImages[self.LastRectHover].WidthTollerance = self.AlexaAppImages[self.LastRectHover].WidthTollerance + event.delta() / 120

                if self.AlexaAppImages[self.LastRectHover].WidthTollerance < 0:
                    self.AlexaAppImages[self.LastRectHover].WidthTollerance = 0
            else:
                self.AlexaAppImages[self.LastRectHover].HeightTollerance = self.AlexaAppImages[self.LastRectHover].HeightTollerance + event.delta() / 120
                if self.AlexaAppImages[self.LastRectHover].HeightTollerance < 0:
                    self.AlexaAppImages[self.LastRectHover].HeightTollerance = 0

                self.AlexaAppImages[self.LastRectHover].WidthTollerance = self.AlexaAppImages[self.LastRectHover].WidthTollerance + event.delta() / 120
                if self.AlexaAppImages[self.LastRectHover].WidthTollerance < 0:
                    self.AlexaAppImages[self.LastRectHover].WidthTollerance = 0

            self.update()

    #mouse press event
    def mousePressEvent(self, event):
        if self.DialogOpened is True or self.InsideRegion is True:
            #self.BringWindowToFront()
            return

        if event.buttons() == Qt.LeftButton:

            if self.InsideRect is True:
                pos = QPoint(QCursor.pos())
                self.xOffset = pos.x() - self.AlexaAppImages[self.LastRectHover].RectX
                self.yOffset = pos.y() - self.AlexaAppImages[self.LastRectHover].RectY

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
            self.Dialog = AppImgDialog(self, self.LastRectHover, 0)
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
            #self.AlexaAppImagesBackup[self.LastRectHover] = copy.deepcopy(self.AlexaAppImages[self.LastRectHover])
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
                AlexaObject = AlexaAppImagePlus()

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

                if self.CropRegion is False:

                    #AlexaObject.Height = height
                    #AlexaObject.Width = width
                    AlexaObject.Height = h
                    AlexaObject.Width = w
                    AlexaObject.HeightTollerance = 10
                    AlexaObject.WidthTollerance = 10
                    AlexaObject.RectX = x
                    AlexaObject.RectY = y

                    self.AlexaAppImages.append(AlexaObject)
                    #self.AlexaAppImagesBackup.append(AlexaObject)
                    self.AlexaAppImagesBackup.append(copy.deepcopy(AlexaObject))
                    self.AlexaAppImagesDeleted = []

                    ##self.rectObjCollection.append(rect)
                    ##self.rectObjCollectionDeleted = []

                    #todo
                    self.DialogOpened = True
                    self.Dialog = AppImgDialog(self, len(self.AlexaAppImages)-1, 0)
                    self.Dialog.show()
                    self.AppObjectFeedbackIndex = self.Dialog.objectIndex
                elif self.CropRegion is True:
                    self.AlexaAppImages[self.AppObjectFeedbackIndex].CropRegionX = x - self.AlexaAppImages[self.AppObjectFeedbackIndex].RectX
                    self.AlexaAppImages[self.AppObjectFeedbackIndex].CropRegionY = y - self.AlexaAppImages[self.AppObjectFeedbackIndex].RectY
                    self.AlexaAppImages[self.AppObjectFeedbackIndex].CropRegionWidth = w
                    self.AlexaAppImages[self.AppObjectFeedbackIndex].CropRegionHeight = h
                    #todo
                    self.DialogOpened = True
                    self.Dialog = AppTextInRegionDialog(self, len(self.AlexaAppImages)-1, 0)
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

            if len(self.AlexaAppImages) > 0:

                self.AlexaAppImagesDeleted.append(self.AlexaAppImages[-1])
                self.AlexaAppImagesBackupDeleted.append(self.AlexaAppImagesBackup[-1])

                del self.AlexaAppImages[-1]
                del self.AlexaAppImagesBackup[-1]

                self.update()

        if event.modifiers() == Qt.ControlModifier and event.key() == Qt.Key_Y:

            if len(self.AlexaAppImagesDeleted) > 0:

                self.AlexaAppImages.append(self.AlexaAppImagesDeleted[-1])
                self.AlexaAppImagesBackup.append(self.AlexaAppImagesBackupDeleted[-1])

                del self.AlexaAppImagesDeleted[-1]
                del self.AlexaAppImagesBackupDeleted[-1]
                #self.AlexaAppImages = []

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

        for alexaAppImage in self.AlexaAppImages:

            #maxLineLen = 0
            #commentLine = ""
            description = ""

            if alexaAppImage.Name is not None and alexaAppImage.Name != "":
                #objName = alexaAppImage.Name.replace(" ", "")
                objName = alexaAppImage.Name
            else:
                objName = "image" + str(self.plugin.AlexaAppImgCnt)

            editor_service.insert_text("    #AppImage: " + objName)
            editor_service.insert_text(os.linesep)

            if alexaAppImage.Description != "":

                description = alexaAppImage.Description.splitlines(True)
                editor_service.insert_text(leadingChar + "'''")
                editor_service.insert_text(os.linesep)
                editor_service.insert_text(leadingChar + "Description:")
                editor_service.insert_text(os.linesep)
                for line in description:
                    editor_service.insert_text(leadingChar + line)
                editor_service.insert_text(os.linesep)
                editor_service.insert_text(leadingChar + "'''")
                editor_service.insert_text(os.linesep)

            editor_service.insert_text(leadingChar + objName + " = AppImage()")
            editor_service.insert_text(os.linesep)

            editor_service.insert_text(leadingChar + objName + ".Name = \"" + objName + "\"")
            editor_service.insert_text(os.linesep)

            editor_service.insert_text(leadingChar + objName + ".Path = ProjectPath + \"\\\\" + os.path.join("images",objName + ".png").replace("\\","\\\\") + "\"")
            editor_service.insert_text(os.linesep)

            fullFileName = editor_service.get_editor_path()
            #from os.path import basename

            filePath = os.path.split(fullFileName)[0]
            if os.path.exists(os.path.join(filePath, 'images')) is False:
                os.makedirs(os.path.join(filePath, 'images'))

            PilImage = Image.open(self.plug_path + os.sep + 'tmp' + os.sep + 'screenshot.png')
            cropped = (alexaAppImage.RectX, alexaAppImage.RectY, alexaAppImage.RectX + alexaAppImage.Width, alexaAppImage.RectY + alexaAppImage.Height)
            #print self.plug_path + os.sep + 'tmp' + os.sep
            area = PilImage.crop(cropped)
            area.save(os.path.join(filePath, 'images', objName + ".png"))

            editor_service.insert_text(leadingChar + objName + ".Threshold = " + str(alexaAppImage.Threshold))
            editor_service.insert_text(os.linesep)

            timeOutTime = 15
            if alexaAppImage.EnablePerfData is True:
                timeOutTime = timeOutTime + alexaAppImage.PerfCriticalLevel

            editor_service.insert_text(leadingChar + "performance = " + objName + ".Bind(" + str(timeOutTime) + ")")
            editor_service.insert_text(os.linesep)

            if alexaAppImage.EnablePerfData is True:
                editor_service.insert_text(leadingChar + "NagiosUtils.AddPerformanceData(\"" + objName + "\", performance, " + str(alexaAppImage.PerfWarningLevel) + ", " + str(alexaAppImage.PerfCriticalLevel) + ")")
                editor_service.insert_text(os.linesep)

            if alexaAppImage.UseMouse is True or alexaAppImage.UseKeyboard is True or\
            alexaAppImage.CropRegionX != 0 or alexaAppImage.CropRegionY != 0 or alexaAppImage.CropRegionHeight != 0 or alexaAppImage.CropRegionWidth != 0:
                editor_service.insert_text(leadingChar + "if " + objName + ".TimeOut is False:")
                editor_service.insert_text(os.linesep)
            else:
                editor_service.insert_text(leadingChar + "if " + objName + ".TimeOut is False:")
                editor_service.insert_text(os.linesep)
                editor_service.insert_text(leadingChar + tabChar + "pass")
                editor_service.insert_text(os.linesep)

            if alexaAppImage.Click is True and alexaAppImage.UseMouse is True:
                editor_service.insert_text(leadingChar + tabChar + "Mouse.Click(" + objName + ".x + (" + objName + ".Width / 2), " + objName + ".y + (" + objName + ".Height / 2))")
                editor_service.insert_text(os.linesep)

            if alexaAppImage.DoubleClick is True and alexaAppImage.UseMouse is True:
                editor_service.insert_text(leadingChar + tabChar + "Mouse.DoubleClick(" + objName + ".x + (" + objName + ".Width / 2), " + objName + ".y + (" + objName + ".Height / 2))")
                editor_service.insert_text(os.linesep)

            if alexaAppImage.UseKeyboard is True:
                editor_service.insert_text(leadingChar + tabChar + "Keyboard.InsertText(\"" + alexaAppImage.InsertText + "\")")
                editor_service.insert_text(os.linesep)

            if alexaAppImage.CropRegionX != 0 or alexaAppImage.CropRegionY != 0 or alexaAppImage.CropRegionHeight != 0 or alexaAppImage.CropRegionWidth != 0:

                if alexaAppImage.CropRegionX < 0:
                    cropRegionX = -alexaAppImage.CropRegionX
                    cropOperatorX = "-"
                else:
                    cropRegionX = alexaAppImage.CropRegionX
                    cropOperatorX = "+"

                if alexaAppImage.CropRegionY < 0:
                    cropRegionY = -alexaAppImage.CropRegionY
                    cropOperatorY = "-"
                else:
                    cropRegionY = alexaAppImage.CropRegionY
                    cropOperatorY = "+"

                editor_service.insert_text(leadingChar + tabChar + "SearchRegion.Bind(" + objName + ".x " + cropOperatorX + " " + str(cropRegionX) + ", " + objName + ".y " + cropOperatorY + " " + str(cropRegionY) + ", " +
                str(alexaAppImage.CropRegionWidth) + ", " + str(alexaAppImage.CropRegionHeight) + ")")
                editor_service.insert_text(os.linesep)

            editor_service.insert_text(leadingChar + "elif " + objName + ".TimeOut is True and ExitOnError is True:")
            editor_service.insert_text(os.linesep)
            editor_service.insert_text(leadingChar + tabChar + "Finish()")
            editor_service.insert_text(os.linesep)

            editor_service.insert_text(leadingChar + "#end...")
            editor_service.insert_text(os.linesep)

            '''
            editor_service.insert_text(leadingChar + "mouseX = " + objName + ".x + (" + objName + ".Width / 2)")
            editor_service.insert_text(os.linesep)
            editor_service.insert_text(leadingChar + "mouseY = " + objName + ".y + (" + objName + ".Height / 2)")
            editor_service.insert_text(os.linesep)

            editor_service.insert_text(os.linesep)
            #editor_service.insert_text(leadingChar + 'self, text')
            #editor_service.insert_text(os.linesep)
            '''
            self.plugin.AlexaAppObjCnt = self.plugin.AlexaAppObjCnt + 1

            if alexaAppImage.CropRegionX != 0 or alexaAppImage.CropRegionY != 0 or alexaAppImage.CropRegionHeight != 0 or alexaAppImage.CropRegionWidth != 0:

                editor_service.insert_text(os.linesep)

                description = ""

                if alexaAppImage.AppText.Name is not None and alexaAppImage.AppText.Name != "":
                    #objName = alexaAppImage.AppText.Name.replace(" ", "")
                    objName = alexaAppImage.AppText.Name
                else:
                    objName = "object" + str(self.plugin.AlexaAppObjCnt)

                editor_service.insert_text(leadingChar + "    #AppText: " + objName)
                editor_service.insert_text(os.linesep)

                if alexaAppImage.AppText.Description != "":

                    description = alexaAppImage.AppText.Description.splitlines(True)
                    editor_service.insert_text(leadingChar + "'''")
                    editor_service.insert_text(os.linesep)
                    editor_service.insert_text(leadingChar + "Description:")
                    editor_service.insert_text(os.linesep)
                    for line in description:
                        editor_service.insert_text(leadingChar + line)
                    editor_service.insert_text(os.linesep)
                    editor_service.insert_text(leadingChar + "'''")
                    editor_service.insert_text(os.linesep)

                editor_service.insert_text(leadingChar + objName + " = AppText()")
                editor_service.insert_text(os.linesep)

                editor_service.insert_text(leadingChar + objName + ".Name = \"" + objName + "\"")
                editor_service.insert_text(os.linesep)

                if alexaAppImage.AppText.Text != "":
                    editor_service.insert_text(leadingChar + objName + ".Text = \"" + alexaAppImage.AppText.Text + "\"")
                    editor_service.insert_text(os.linesep)
                    editor_service.insert_text(leadingChar + objName + ".Language = \"" + alexaAppImage.AppText.Language + "\"")
                    editor_service.insert_text(os.linesep)

                if alexaAppImage.AppText.Binarize is True:
                    editor_service.insert_text(leadingChar + objName + ".Binarize = True")
                    editor_service.insert_text(os.linesep)
                    editor_service.insert_text(leadingChar + objName + ".Brightness = " + str(alexaAppImage.AppText.Brightness))
                    editor_service.insert_text(os.linesep)
                    editor_service.insert_text(leadingChar + objName + ".Contrast = " + str(alexaAppImage.AppText.Contrast))
                    editor_service.insert_text(os.linesep)

                if alexaAppImage.AppText.OcrWhiteList != Ocr.WhiteList:
                    editor_service.insert_text(leadingChar + "Ocr.WhiteList = \"" + alexaAppImage.AppText.OcrWhiteList + "\"")
                    editor_service.insert_text(os.linesep)

                timeOutTime = 15
                if alexaAppImage.AppText.EnablePerfData is True:
                    timeOutTime = timeOutTime + alexaAppImage.AppText.PerfCriticalLevel

                editor_service.insert_text(leadingChar + "performance = " + objName + ".Bind(" + str(timeOutTime) + ")")
                editor_service.insert_text(os.linesep)

                if alexaAppImage.AppText.EnablePerfData is True:
                    editor_service.insert_text(leadingChar + "NagiosUtils.AddPerformanceData(\"" + objName + "\", performance, " + str(alexaAppImage.AppText.PerfWarningLevel) + ", " + str(alexaAppImage.AppText.PerfCriticalLevel) + ")")
                    editor_service.insert_text(os.linesep)

                if alexaAppImage.AppText.UseMouse is True or alexaAppImage.AppText.UseKeyboard is True:
                    editor_service.insert_text(leadingChar + "if " + objName + ".TimeOut is False:")
                    editor_service.insert_text(os.linesep)
                else:
                    editor_service.insert_text(leadingChar + "if " + objName + ".TimeOut is False:")
                    editor_service.insert_text(os.linesep)
                    editor_service.insert_text(leadingChar + tabChar + "pass")
                    editor_service.insert_text(os.linesep)

                if alexaAppImage.AppText.Click is True and alexaAppImage.AppText.UseMouse is True:
                    editor_service.insert_text(leadingChar + tabChar + "Mouse.Click(" + objName + ".x + (" + objName + ".Width / 2), " + objName + ".y + (" + objName + ".Height / 2))")
                    editor_service.insert_text(os.linesep)

                if alexaAppImage.AppText.DoubleClick is True and alexaAppImage.AppText.UseMouse is True:
                    editor_service.insert_text(leadingChar + tabChar + "Mouse.DoubleClick(" + objName + ".x + (" + objName + ".Width / 2), " + objName + ".y + (" + objName + ".Height / 2))")
                    editor_service.insert_text(os.linesep)

                if alexaAppImage.AppText.UseKeyboard is True:
                    editor_service.insert_text(leadingChar + tabChar + "Keyboard.InsertText(\"" + alexaAppImage.AppText.InsertText + "\")")
                    editor_service.insert_text(os.linesep)

                editor_service.insert_text(leadingChar + "elif " + objName + ".TimeOut is True and ExitOnError is True:")
                editor_service.insert_text(os.linesep)
                editor_service.insert_text(leadingChar + tabChar + "Finish()")
                editor_service.insert_text(os.linesep)

                if alexaAppImage.AppText.OcrWhiteList != Ocr.WhiteList:
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

    def DoBinarizeRegion(self, brightness, contrast):
        #print brightness, contrast
        self.UpdateLabelOfInterest()

        PilImage2 = self.OriginalScreenshot.copy()

        x = self.AlexaAppImages[self.AppObjectFeedbackIndex].RectX + self.AlexaAppImages[self.AppObjectFeedbackIndex].CropRegionX
        y = self.AlexaAppImages[self.AppObjectFeedbackIndex].RectY + self.AlexaAppImages[self.AppObjectFeedbackIndex].CropRegionY
        w = self.AlexaAppImages[self.AppObjectFeedbackIndex].RectX + self.AlexaAppImages[self.AppObjectFeedbackIndex].CropRegionX + self.AlexaAppImages[self.AppObjectFeedbackIndex].CropRegionWidth
        h = self.AlexaAppImages[self.AppObjectFeedbackIndex].RectY + self.AlexaAppImages[self.AppObjectFeedbackIndex].CropRegionY + self.AlexaAppImages[self.AppObjectFeedbackIndex].CropRegionHeight
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

class AlexaAppImagePlus(AppImage, object):

    def __init__(self):
        super(AlexaAppImagePlus, self).__init__()
        self.RectX = None
        self.RectY = None
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
        self.AppText = AlexaAppTextPlus()
        self.AppTextBackup = AlexaAppTextPlus()
class AlexaAppTextPlus(AppText, object):

    def __init__(self):
        super(AlexaAppTextPlus, self).__init__()
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
