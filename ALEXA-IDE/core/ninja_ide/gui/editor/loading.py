# -*- coding: utf-8 -*-
'''
Copyright (C) 2013 Alan Pipitone

Al'exa is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

Al'exa is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with Al'exa.  If not, see <http://www.gnu.org/licenses/>.
'''
from __future__ import absolute_import

from PyQt4.QtGui import QWidget
from PyQt4.QtGui import QBrush
from PyQt4.QtGui import QLinearGradient
from PyQt4.QtGui import QPixmap
from PyQt4.QtGui import QColor
from PyQt4.QtGui import QPolygonF
from PyQt4.QtGui import QFontMetrics
from PyQt4.QtGui import QPainter
from PyQt4.QtGui import QLabel
from PyQt4.QtCore import Qt
from PyQt4.QtCore import QRect
from PyQt4.QtCore import QPointF

from ninja_ide import resources
from ninja_ide.core import settings
from ninja_ide.gui.editor import helpers

#based on: http://john.nachtimwald.com/2009/08/15/qtextedit-with-line-numbers/
#(MIT license)


class Loading(QWidget):
    def __init__(self, caller):
        super(Loading, self).__init__()

        self.setObjectName("Form")
        self.resize(485, 98)
        self.caller = caller
        self.labelLoading = QLabel(self)
        self.labelLoading.setGeometry(QRect(20, 20, 171, 16))
        self.labelLoading.setObjectName("labelLoading")

        self.setWindowTitle("Loading")
        self.labelLoading.setText("Loading: xx%")
        self.first = False
        self.folded = False

    def paintEvent(self, event):
        pass
