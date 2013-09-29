# -*- coding: utf-8 -*-
#
# Last Modified: 2013-09-02 by Alan Pipitone
#                added lines for Al'exa-Ide
#
# This file is part of NINJA-IDE (http://ninja-ide.org).
#
# NINJA-IDE is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# any later version.
#
# NINJA-IDE is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with NINJA-IDE; If not, see <http://www.gnu.org/licenses/>.
from __future__ import absolute_import

import math
import re
import copy
import time

from PyQt4.QtGui import QWidget
from PyQt4.QtGui import QBrush
from PyQt4.QtGui import QLinearGradient
from PyQt4.QtGui import QPixmap
from PyQt4.QtGui import QColor
from PyQt4.QtGui import QPolygonF
from PyQt4.QtGui import QFontMetrics
from PyQt4.QtGui import QPainter
#from PyQt4.QtGui import QCursor
from PyQt4.QtCore import Qt
from PyQt4.QtCore import QPointF

from ninja_ide import resources
from ninja_ide.core import settings
from ninja_ide.gui.editor import helpers

#based on: http://john.nachtimwald.com/2009/08/15/qtextedit-with-line-numbers/
#(MIT license)


class SidebarWidget(QWidget):

    def __init__(self, editor):
        QWidget.__init__(self, editor)
        self.edit = editor
        self.highest_line = 0
        self.foldArea = 15
        self.rightArrowIcon = QPixmap()
        self.downArrowIcon = QPixmap()
        self.bindIcon = QPixmap()
        self.pat = re.compile(
            "(\s)*def |(\s)*class |(\s)*if |(\s)*while |"
            "(\s)*else:|(\s)*elif |(\s)*for |"
            "(\s)*try:|(\s)*except:|(\s)*except |(\s)*#begin-fold|"
            "(\s)*#AppObject:|(\s)*#Alexa Log|(\s)*#AppImage:|"
            "(\s)*#AppText:")
        self.patNotPython = re.compile('(\s)*#begin-fold:|(.)*{')
        self._foldedBlocks = []
        self._oldFoldedBlocks = []
        self._breakpoints = []
        self._bookmarks = []
        self._pep8Lines = []
        self._errorsLines = []
        self._migrationLines = []
        self._firstPaintEvent = True
        self._oldCursorLine = 0
        self._oldVerticalScrollbarPosition = 0
        self._oldHorizontalScrollbarPosition = 0
        self._oldAlexaAppObjIconsCoords = []
        self._oldAlexaAppImgIconsCoords = []
        self._oldAlexaAppTextIconsCoords = []
        self._foldedAlexaObject = []
        self._foldedAlexaImage = []
        self._foldedAlexaText = []
        self._oldAlexaLogIconsCoords = []
        self._foldedAlexaLog = []
        self.lineToFold = []
        self._alexaFolded = False
        self._alexaObjectsPresent = False
        self.strings = []
        self.jumpedUP = False
        self._keypress = False
        self._originalTotalLine = 0
        self._currentTotalLine = 0
        self.alexaFoundLines = []
        #self.edit.go_to_line(0)

    def update_area(self):
        maxLine = math.ceil(math.log10(self.edit.blockCount()))
        width = QFontMetrics(
            self.edit.document().defaultFont()).width('0' * int(maxLine)) \
                + 10 + self.foldArea
        if self.width() != width:
            self.setFixedWidth(width)
            self.edit.setViewportMargins(width, 0, 0, 0)
        self.update()

    def update(self, *args):
        QWidget.update(self, *args)

    def pep8_check_lines(self, lines):
        self._pep8Lines = lines

    def static_errors_lines(self, lines):
        self._errorsLines = lines

    def migration_lines(self, lines):
        self._migrationLines = lines

    def code_folding_event(self, lineNumber):
        if self._is_folded(lineNumber):
            self._fold(lineNumber)
        else:
            self._unfold(lineNumber)

        self.edit.update()
        self.update()

    def _fold(self, lineNumber):
        startBlock = self.edit.document().findBlockByNumber(lineNumber - 1)
        endPos = self._find_fold_closing(startBlock)
        endBlock = self.edit.document().findBlockByNumber(endPos)

        block = startBlock.next()
        while block.isValid() and block != endBlock:
            block.setVisible(False)
            block.setLineCount(0)
            block = block.next()

        self._foldedBlocks.append(startBlock.blockNumber())
        #self._oldFoldedBlocks = copy.deepcopy(self._foldedBlocks)
        self.edit.document().markContentsDirty(startBlock.position(), endPos)
        self.updateAlexaCoords()

    def _unfold(self, lineNumber):
        startBlock = self.edit.document().findBlockByNumber(lineNumber - 1)
        endPos = self._find_fold_closing(startBlock)
        endBlock = self.edit.document().findBlockByNumber(endPos)
        block = startBlock.next()
        tmpBlock = None  # avoid loop (alan)
        while block.isValid() and block != endBlock:
            block.setVisible(True)
            block.setLineCount(block.layout().lineCount())
            endPos = block.position() + block.length()

            if block.blockNumber() in self._foldedBlocks:# and block != tmpBlock:
                close = self._find_fold_closing(block)
                block = self.edit.document().findBlockByNumber(close)
            else:
                block = block.next()
            tmpBlock = block
        #self._oldFoldedBlocks = copy.deepcopy(self._foldedBlocks)
        self._foldedBlocks.remove(startBlock.blockNumber())
        self.edit.document().markContentsDirty(startBlock.position(), endPos)
        self.updateAlexaCoords()

    def _is_folded(self, line):
        block = self.edit.document().findBlockByNumber(line)
        if not block.isValid():
            return False
        return block.isVisible()

    def _find_fold_closing(self, block):
        text = block.text()
        pat = re.compile('(\s)*#begin-fold:')
        patAlexaAppObject = re.compile('(\s)*#AppObject:')
        patAlexaLog = re.compile('(\s)*#Alexa Log')
        patAlexaAppImage = re.compile('(\s)*#AppImage:')
        patAlexaAppText = re.compile('(\s)*#AppText:')
        patBrace = re.compile('(.)*{$')
        if pat.match(text):
            return self._find_fold_closing_label(block)
        elif patAlexaAppObject.match(text):
            return self._find_fold_closing_alexaAppObject(block)
        elif patAlexaLog.match(text):
            return self._find_fold_closing_alexaLog(block)
        elif patAlexaAppImage.match(text):
            return self._find_fold_closing_alexaAppImage(block)
        elif patAlexaAppText.match(text):
            return self._find_fold_closing_alexaAppText(block)
        elif patBrace.match(text):
            return self._find_fold_closing_brace(block)

        spaces = helpers.get_leading_spaces(text)
        pat = re.compile('^\s*$|^\s*#')
        block = block.next()
        while block.isValid():
            text2 = block.text()
            if not pat.match(text2):
                spacesEnd = helpers.get_leading_spaces(text2)
                if len(spacesEnd) <= len(spaces):
                    if pat.match(block.previous().text()):
                        return block.previous().blockNumber()
                    else:
                        return block.blockNumber()
            block = block.next()
        return block.previous().blockNumber()

    def _find_fold_closing_label(self, block):
        text = block.text()
        label = text.split(':')[1]
        block = block.next()
        pat = re.compile('\s*#end-fold:' + label)
        while block.isValid():
            if pat.match(block.text()):
                return block.blockNumber() + 1
            block = block.next()
        return block.blockNumber()

    def _find_fold_closing_alexaAppObject(self, block):
        #text = block.text()
        #label = text.split(':')[1]
        block = block.next()
        pat = re.compile('\s*#end\.\.\.')
        while block.isValid():
            if pat.match(block.text()):
                return block.blockNumber() + 1
            block = block.next()
        return block.blockNumber()

    def _find_fold_closing_alexaAppImage(self, block):
        #text = block.text()
        #label = text.split(':')[1]
        block = block.next()
        pat = re.compile('\s*#end\.\.\.')
        while block.isValid():
            if pat.match(block.text()):
                return block.blockNumber() + 1
            block = block.next()
        return block.blockNumber()

    def _find_fold_closing_alexaAppText(self, block):
        #text = block.text()
        #label = text.split(':')[1]
        block = block.next()
        pat = re.compile('\s*#end\.\.\.')
        while block.isValid():
            if pat.match(block.text()):
                return block.blockNumber() + 1
            block = block.next()
        return block.blockNumber()

    def _find_fold_closing_alexaLog(self, block):
        #text = block.text()
        #label = text.split(':')[1]
        block = block.next()
        pat = re.compile('\s*#end...')
        while block.isValid():
            if pat.match(block.text()):
                return block.blockNumber() + 1
            block = block.next()
        return block.blockNumber()

    def _find_fold_closing_brace(self, block):
        block = block.next()
        openBrace = 1
        while block.isValid():
            openBrace += block.text().count('{')
            openBrace -= block.text().count('}')
            if openBrace == 0:
                return block.blockNumber() + 1
            elif openBrace < 0:
                return block.blockNumber()
            block = block.next()
        return block.blockNumber()

    def paintEvent(self, event):

        page_bottom = self.edit.viewport().height()

        font_metrics = QFontMetrics(self.edit.document().defaultFont())
        current_block = self.edit.document().findBlock(
            self.edit.textCursor().position())

        if self._firstPaintEvent is True:
            self.jumpedUP = False
            self.strings = self.edit.toPlainText().split('\n')
            self._originalTotalLine = len(self.strings)
            self.edit.jump_to_line(len(self.strings) - 2)
        elif self.jumpedUP is False:
            self.edit.jump_to_line(1)
            self.edit.verticalScrollBar().setValue(0)
            self.jumpedUP = True
            return

        pattern = self.pat if self.edit.lang == "python" else self.patNotPython

        painter = QPainter(self)
        background = resources.CUSTOM_SCHEME.get('sidebar-background',
            resources.COLOR_SCHEME['sidebar-background'])
        foreground = resources.CUSTOM_SCHEME.get('sidebar-foreground',
            resources.COLOR_SCHEME['sidebar-foreground'])
        pep8color = resources.CUSTOM_SCHEME.get('pep8-underline',
            resources.COLOR_SCHEME['pep8-underline'])
        errorcolor = resources.CUSTOM_SCHEME.get('error-underline',
            resources.COLOR_SCHEME['error-underline'])
        migrationcolor = resources.CUSTOM_SCHEME.get('migration-underline',
            resources.COLOR_SCHEME['migration-underline'])
        painter.fillRect(self.rect(), QColor(background))

        '''
        if self._firstPaintEvent is True:
            block = self.edit.document().findBlock(0)
        else:
            block = self.edit.firstVisibleBlock()
        '''
        block = self.edit.firstVisibleBlock()
        viewport_offset = self.edit.contentOffset()
        line_count = block.blockNumber()
        painter.setFont(self.edit.document().defaultFont())

        pat = re.compile('\s*#AppObject:')
        patAlexaAppImage = re.compile('\s*#AppImage:')
        patAlexaAppText = re.compile('\s*#AppText:')
        patAlexaLog = re.compile('\s*#Alexa Log')

        while block.isValid():
            line_count += 1
            # The top left position of the block in the document
            position = self.edit.blockBoundingGeometry(block).topLeft() + \
                viewport_offset
            # Check if the position of the block is outside of the visible area
            if position.y() > page_bottom:
                break

            # Set the Painter Pen depending on special lines
            error = False
            if settings.CHECK_STYLE and \
               ((line_count - 1) in self._pep8Lines):
                painter.setPen(QColor(pep8color))
                font = painter.font()
                font.setItalic(True)
                font.setUnderline(True)
                painter.setFont(font)
                error = True
            elif settings.FIND_ERRORS and \
                 ((line_count - 1) in self._errorsLines):
                painter.setPen(QColor(errorcolor))
                font = painter.font()
                font.setItalic(True)
                font.setUnderline(True)
                painter.setFont(font)
                error = True
            elif settings.SHOW_MIGRATION_TIPS and \
                 ((line_count - 1) in self._migrationLines):
                painter.setPen(QColor(migrationcolor))
                font = painter.font()
                font.setItalic(True)
                font.setUnderline(True)
                painter.setFont(font)
                error = True
            else:
                painter.setPen(QColor(foreground))

            # We want the line number for the selected line to be bold.
            bold = False
            if block == current_block:
                bold = True
                font = painter.font()
                font.setBold(True)
                painter.setFont(font)

            # Draw the line number right justified at the y position of the
            # line. 3 is a magic padding number. drawText(x, y, text).
            if block.isVisible():
                painter.drawText(self.width() - self.foldArea -
                    font_metrics.width(str(line_count)) - 3,
                    round(position.y()) + font_metrics.ascent() +
                    font_metrics.descent() - 1,
                    str(line_count))

            # Remove the bold style if it was set previously.
            if bold:
                font = painter.font()
                font.setBold(False)
                painter.setFont(font)
            if error:
                font = painter.font()
                font.setItalic(False)
                font.setUnderline(False)
                painter.setFont(font)

            block = block.next()

        self.highest_line = line_count

        #Code Folding
        xofs = self.width() - self.foldArea
        painter.fillRect(xofs, 0, self.foldArea, self.height(),
                QColor(resources.CUSTOM_SCHEME.get('fold-area',
                resources.COLOR_SCHEME['fold-area'])))
        if self.foldArea != self.rightArrowIcon.width():
            polygon = QPolygonF()

            self.rightArrowIcon = QPixmap(self.foldArea, self.foldArea)
            self.rightArrowIcon.fill(Qt.transparent)
            self.downArrowIcon = QPixmap(self.foldArea, self.foldArea)
            self.downArrowIcon.fill(Qt.transparent)

            polygon.append(QPointF(self.foldArea * 0.4, self.foldArea * 0.25))
            polygon.append(QPointF(self.foldArea * 0.4, self.foldArea * 0.75))
            polygon.append(QPointF(self.foldArea * 0.8, self.foldArea * 0.5))
            iconPainter = QPainter(self.rightArrowIcon)
            iconPainter.setRenderHint(QPainter.Antialiasing)
            iconPainter.setPen(Qt.NoPen)
            iconPainter.setBrush(QColor(
                resources.CUSTOM_SCHEME.get('fold-arrow',
                resources.COLOR_SCHEME['fold-arrow'])))
            iconPainter.drawPolygon(polygon)

            polygon.clear()
            polygon.append(QPointF(self.foldArea * 0.25, self.foldArea * 0.4))
            polygon.append(QPointF(self.foldArea * 0.75, self.foldArea * 0.4))
            polygon.append(QPointF(self.foldArea * 0.5, self.foldArea * 0.8))
            iconPainter = QPainter(self.downArrowIcon)
            iconPainter.setRenderHint(QPainter.Antialiasing)
            iconPainter.setPen(Qt.NoPen)
            iconPainter.setBrush(QColor(
                resources.CUSTOM_SCHEME.get('fold-arrow',
                resources.COLOR_SCHEME['fold-arrow'])))
            iconPainter.drawPolygon(polygon)

        if self._firstPaintEvent is True:
            block = self.edit.document().findBlock(0)
        else:
            block = self.edit.firstVisibleBlock()
        #block = self.edit.firstVisibleBlock()
        line_count = block.blockNumber()
        while block.isValid():
        #while line_count < 5000:
            line_count += 1
            position = self.edit.blockBoundingGeometry(
                block).topLeft() + viewport_offset
            #Check if the position of the block is outside of the visible area
            if position.y() > page_bottom:
                break


            #block.isVisible() and
            if block.isVisible() and pat.match(block.text()) and block not in self._foldedAlexaObject:
                self._fold(line_count)
                self._foldedAlexaObject.append(block)
                self._alexaObjectsPresent = True
            elif block.isVisible() and patAlexaAppImage.match(block.text()) and block not in self._foldedAlexaImage:
                self._fold(line_count)
                self._foldedAlexaImage.append(block)
                self._alexaObjectsPresent = True
            elif block.isVisible() and patAlexaAppText.match(block.text()) and block not in self._foldedAlexaText:
                self._fold(line_count)
                self._foldedAlexaText.append(block)
                self._alexaObjectsPresent = True
            elif block.isVisible() and patAlexaLog.match(block.text()) and block not in self._foldedAlexaLog:
                self._fold(line_count)
                self._foldedAlexaLog.append(block)
                self._alexaObjectsPresent = True
            elif pattern.match(block.text()) and block.isVisible():
                if block.blockNumber() in self._foldedBlocks:
                    painter.drawPixmap(xofs, round(position.y()),
                        self.rightArrowIcon)
                else:
                    #block.setVisible(True)
                    painter.drawPixmap(xofs, round(position.y()),
                        self.downArrowIcon)
            #Add Bookmarks and Breakpoint
            elif block.blockNumber() in self._breakpoints:
                linear_gradient = QLinearGradient(
                    xofs, round(position.y()),
                    xofs + self.foldArea, round(position.y()) + self.foldArea)
                linear_gradient.setColorAt(0, QColor(255, 11, 11))
                linear_gradient.setColorAt(1, QColor(147, 9, 9))
                painter.setRenderHints(QPainter.Antialiasing, True)
                painter.setPen(Qt.NoPen)
                painter.setBrush(QBrush(linear_gradient))
                painter.drawEllipse(
                    xofs + 1,
                    round(position.y()) + 6,
                    self.foldArea - 1, self.foldArea - 1)
            elif block.blockNumber() in self._bookmarks:
                linear_gradient = QLinearGradient(
                    xofs, round(position.y()),
                    xofs + self.foldArea, round(position.y()) + self.foldArea)
                linear_gradient.setColorAt(0, QColor(13, 62, 243))
                linear_gradient.setColorAt(1, QColor(5, 27, 106))
                painter.setRenderHints(QPainter.Antialiasing, True)
                painter.setPen(Qt.NoPen)
                painter.setBrush(QBrush(linear_gradient))
                painter.drawRoundedRect(
                    xofs + 1,
                    round(position.y()) + 6,
                    self.foldArea - 2, self.foldArea - 1,
                    3, 3)

            block = block.next()

        block = self.edit.document().findBlock(0)
        line_count = 0
        line_hidden = 0
        while block.isValid():
            line_count += 1
            if not block.isVisible():
                line_hidden += 1
            block = block.next()
        endScrollBar = line_count - line_hidden
        self.edit.verticalScrollBar().setRange(0, endScrollBar)

        if self._firstPaintEvent is True:
            self._firstPaintEvent = False

        #self.updateAlexaAppObjCoords()
        #self.updateAlexaLogCoords()
        painter.end()

        '''
        #self.edit.update()
        if self.edit.verticalScrollBar().value() != self._oldVerticalScrollbarPosition and self._alexaObjectsPresent is True:
            self._oldVerticalScrollbarPosition = self.edit.verticalScrollBar().value()
            self.updateAlexaCoords()
            self.edit.update()  # in this way we can refresh alexa icon position

        if self.edit.horizontalScrollBar().value() != self._oldHorizontalScrollbarPosition and self._alexaObjectsPresent is True:
            self._oldHorizontalScrollbarPosition = self.edit.horizontalScrollBar().value()
            self.updateAlexaCoords()
            self.edit.update()  # in this way we can refresh alexa icon position
        '''

        self.strings = self.edit.toPlainText().split('\n')
        self._currentTotalLine = len(self.strings)

        if self._currentTotalLine != self._originalTotalLine:
            self._originalTotalLine = self._currentTotalLine
            self.updateAlexaCoords()
            self.edit.update()

        '''
        if self._returnPressed is True:
            self._returnPressed = False
            self.updateAlexaAppObjCoords()
            self.updateAlexaLogCoords()
            self.edit.update()

        if self._backspacePressed is True:
            self._backspacePressed = False
            self.strings = self.edit.toPlainText().split('\n')
            self._currentTotalLine = len(self.strings)
            if self._currentTotalLine != self._originalTotalLine:
                self.updateAlexaAppObjCoords()
                self.updateAlexaLogCoords()
                self.edit.update()
        '''

        if self.edit._alexaAppObjIconsCoords != self._oldAlexaAppObjIconsCoords:
            self._oldAlexaAppObjIconsCoords = copy.deepcopy(self.edit._alexaAppObjIconsCoords)
            self.edit.update()

        if self.edit._alexaAppImgIconsCoords != self._oldAlexaAppImgIconsCoords:
            self._oldAlexaAppImgIconsCoords = copy.deepcopy(self.edit._alexaAppImgIconsCoords)
            self.edit.update()

        if self.edit._alexaAppTextIconsCoords != self._oldAlexaAppTextIconsCoords:
            self._oldAlexaAppTextIconsCoords = copy.deepcopy(self.edit._alexaAppTextIconsCoords)
            self.edit.update()

        if self.edit._alexaLogIconsCoords != self._oldAlexaLogIconsCoords:
            self._oldAlexaLogIconsCoords = copy.deepcopy(self.edit._alexaLogIconsCoords)
            self.edit.update()

        selectedLine = self.edit.textCursor().selectedText()
        textAtCursorPos = self.edit.textCursor().block().text()

        try:
            #tmp = selectedLine.index("#   AppObject")
            if (pat.match(selectedLine) or patAlexaLog.match(selectedLine) or \
            pat.match(textAtCursorPos) or patAlexaLog.match(textAtCursorPos) or \
            patAlexaAppImage.match(selectedLine) or patAlexaAppImage.match(textAtCursorPos) or\
            patAlexaAppText.match(selectedLine) or patAlexaAppText.match(textAtCursorPos)) and \
            self._keypress is True:
                self._keypress = False
                self.updateAlexaCoords()
        except:
            pass

        QWidget.paintEvent(self, event)

        '''
        if self._alexaFolded is False:  # and self._alexaFolded is False:
            self._alexaFolded = True
            #return
            #self.edit.setCursor(QCursor(Qt.WaitCursor))
            load = loading.Loading(self)
            load.show()

            #self._alexaFolded = True
            line_alexa_cnt = 1
            strings = self.edit.toPlainText().split('\n')

            for line in strings:
                #print line
                percent = (line_alexa_cnt * 100) / len(strings)
                #print percent
                tmpObj = -1
                try:
                    tmpObj = line.index('#   AppObject:')
                    #self.lineToFold.append(line_alexa_cnt)
                    self._fold(line_alexa_cnt)
                    self._alexaObjectsPresent = True
                    self.loading.update()
                except:
                    pass

                try:
                    if tmpObj == -1:
                        tmpObj = line.index('#   Alexa Log')
                        self._fold(line_alexa_cnt)
                        self._alexaObjectsPresent = True
                except:
                    tmpObj = -1
                line_alexa_cnt += 1
        '''

    def mousePressEvent(self, event):
        if self.foldArea > 0:
            xofs = self.width() - self.foldArea
            font_metrics = QFontMetrics(self.edit.document().defaultFont())
            fh = font_metrics.lineSpacing()
            ys = event.posF().y()
            lineNumber = 0
            #self.code_folding_event(lineNumber)
            if event.pos().x() > xofs:
                pattern = self.pat
                if self.edit.lang != "python":
                    pattern = self.patNotPython
                block = self.edit.firstVisibleBlock()
                viewport_offset = self.edit.contentOffset()
                page_bottom = self.edit.viewport().height()
                while block.isValid():
                    position = self.edit.blockBoundingGeometry(
                        block).topLeft() + viewport_offset
                    if position.y() > page_bottom:
                        break
                    if position.y() < ys and (position.y() + fh) > ys and \
                      pattern.match(str(block.text())):
                        lineNumber = block.blockNumber() + 1
                        break
                    elif position.y() < ys and (position.y() + fh) > ys and \
                      event.button() == Qt.LeftButton:
                        line = block.blockNumber()
                        if line in self._breakpoints:
                            self._breakpoints.remove(line)
                        else:
                            self._breakpoints.append(line)
                        self.update()
                        break
                    elif position.y() < ys and (position.y() + fh) > ys and \
                      event.button() == Qt.RightButton:
                        line = block.blockNumber()
                        if line in self._bookmarks:
                            self._bookmarks.remove(line)
                        else:
                            self._bookmarks.append(line)
                        self.update()
                        break
                    block = block.next()
                self._save_breakpoints_bookmarks()
            if lineNumber > 0:
                self.code_folding_event(lineNumber)

    def _save_breakpoints_bookmarks(self):
        if self._bookmarks and self.edit.ID != "":
            settings.BOOKMARKS[self.edit.ID] = self._bookmarks
        elif self.edit.ID in settings.BOOKMARKS:
            settings.BOOKMARKS.pop(self.edit.ID)
        if self._breakpoints and self.edit.ID != "":
            settings.BREAKPOINTS[self.edit.ID] = self._breakpoints
        elif self.edit.ID in settings.BREAKPOINTS:
            settings.BREAKPOINTS.pop(self.edit.ID)

    def set_breakpoint(self, lineno):
        if lineno in self._breakpoints:
            self._breakpoints.remove(lineno)
        else:
            self._breakpoints.append(lineno)
        self.update()
        self._save_breakpoints_bookmarks()

    def set_bookmark(self, lineno):
        if lineno in self._bookmarks:
            self._bookmarks.remove(lineno)
        else:
            self._bookmarks.append(lineno)
        self.update()
        self._save_breakpoints_bookmarks()

    def updateAlexaCoords(self):
        #t0 = time.time()
        self.updateAlexaAppObjCoords()
        self.updateAlexaAppImgCoords()
        self.updateAlexaAppTextCoords()
        self.updateAlexaLogCoords()
        #print "tempo impiegato:", time.time() - t0


    def updateAlexaAppObjCoords(self):
        self.edit._alexaAppObjIconsCoords = []
        #block = self.edit.document().findBlock(0)
        block = self.edit.firstVisibleBlock()
        line_count = block.blockNumber()

        pat = re.compile('\s*#AppObject:')

        viewport_offset = self.edit.contentOffset()

        while block.isValid():
            line_count += 1
            #maxLine = math.ceil(math.log10(self.edit.blockCount()))
            font_metrics = QFontMetrics(self.edit.document().defaultFont())

            position = self.edit.blockBoundingGeometry(block).topLeft() + viewport_offset
            width = self.edit.blockBoundingGeometry(block).width()
            '''
            width = 4
            for char in block.text():
                width += font_metrics.width(char)
            '''

            x = 4 + viewport_offset.x()
            if pat.match(block.text()):
                try:
                    if self.edit.useTabs:
                        x += block.text().index("    #") * (font_metrics.width('.') * self.edit.indent)
                    else:
                        x += block.text().index("    #") * font_metrics.width('.')
                except:
                    pass
                if block.isVisible():  # da notare che il blocco è la riga e non il blocco compreso tra i tag di Al'exa
                    self.edit._alexaAppObjIconsCoords.append((x, position.y(), width, line_count))

            block = block.next()

    def updateAlexaAppImgCoords(self):
        self.edit._alexaAppImgIconsCoords = []
        #block = self.edit.document().findBlock(0)
        block = self.edit.firstVisibleBlock()
        line_count = block.blockNumber()

        pat = re.compile('\s*#AppImage:')

        viewport_offset = self.edit.contentOffset()

        while block.isValid():
            line_count += 1
            #maxLine = math.ceil(math.log10(self.edit.blockCount()))
            font_metrics = QFontMetrics(self.edit.document().defaultFont())

            position = self.edit.blockBoundingGeometry(block).topLeft() + viewport_offset
            width = self.edit.blockBoundingGeometry(block).width()
            '''
            width = 4
            for char in block.text():
                width += font_metrics.width(char)
            '''

            x = 5 + viewport_offset.x()
            if pat.match(block.text()):
                try:
                    if self.edit.useTabs:
                        x += block.text().index("    #") * (font_metrics.width('.') * self.edit.indent)
                    else:
                        x += block.text().index("    #") * font_metrics.width('.')
                except:
                    pass
                if block.isVisible():  # da notare che il blocco è la riga e non il blocco compreso tra i tag di Al'exa
                    self.edit._alexaAppImgIconsCoords.append((x, position.y(), width, line_count))

            block = block.next()

    def updateAlexaAppTextCoords(self):

        self.edit._alexaAppTextIconsCoords = []
        #block = self.edit.document().findBlock(0)
        block = self.edit.firstVisibleBlock()
        line_count = block.blockNumber()

        pat = re.compile('\s*#AppText:')

        viewport_offset = self.edit.contentOffset()

        while block.isValid():
            line_count += 1

            #maxLine = math.ceil(math.log10(self.edit.blockCount()))
            font_metrics = QFontMetrics(self.edit.document().defaultFont())

            position = self.edit.blockBoundingGeometry(block).topLeft() + viewport_offset
            width = self.edit.blockBoundingGeometry(block).width()

            x = 4 + viewport_offset.x()
            if pat.match(block.text()):
                try:
                    if self.edit.useTabs:
                        #x += block.text().index("#") * (font_metrics.width('.') * self.edit.indent)
                        x += block.text().index("    #") * (font_metrics.width('.') * self.edit.indent)
                    else:
                        #x += block.text().index("#") * font_metrics.width('.')
                        x += block.text().index("    #") * font_metrics.width('.')
                except:
                    pass
                if block.isVisible():  # da notare che il blocco è la riga e non il blocco compreso tra i tag di Al'exa
                    self.edit._alexaAppTextIconsCoords.append((x, position.y(), width, line_count))

            block = block.next()

    def updateAlexaLogCoords(self):

        self.edit._alexaLogIconsCoords = []
        #block = self.edit.document().findBlock(0)
        block = self.edit.firstVisibleBlock()
        line_count = block.blockNumber()

        pat = re.compile('\s*#Alexa Log')

        viewport_offset = self.edit.contentOffset()

        while block.isValid():
            line_count += 1

            #maxLine = math.ceil(math.log10(self.edit.blockCount()))
            font_metrics = QFontMetrics(self.edit.document().defaultFont())

            position = self.edit.blockBoundingGeometry(block).topLeft() + viewport_offset
            width = self.edit.blockBoundingGeometry(block).width()

            x = 2 + viewport_offset.x()
            if pat.match(block.text()):
                try:
                    if self.edit.useTabs:
                        #x += block.text().index("#") * (font_metrics.width('.') * self.edit.indent)
                        x += block.text().index("    #") * (font_metrics.width('.') * self.edit.indent)
                    else:
                        #x += block.text().index("#") * font_metrics.width('.')
                        x += block.text().index("    #") * font_metrics.width('.')
                except:
                    pass
                if block.isVisible():  # da notare che il blocco è la riga e non il blocco compreso tra i tag di Al'exa
                    self.edit._alexaLogIconsCoords.append((x, position.y(), width, line_count))

            block = block.next()


