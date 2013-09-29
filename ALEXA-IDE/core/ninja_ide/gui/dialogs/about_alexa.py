# -*- coding: utf-8 -*-
#
# Last Modified: 2013-09-22 by Alan Pipitone
#                added/modified lines for Al'exa-Ide
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

import webbrowser

from PyQt4.QtGui import QDialog
from PyQt4.QtGui import QVBoxLayout
from PyQt4.QtGui import QHBoxLayout
from PyQt4.QtGui import QLabel
from PyQt4.QtGui import QPixmap
from PyQt4.QtCore import Qt
from PyQt4.QtCore import QSize
from PyQt4.QtCore import SIGNAL

import ninja_ide
from ninja_ide import resources


class AboutAlexa(QDialog):

    def __init__(self, parent=None):
        QDialog.__init__(self, parent, Qt.Dialog)
        self.setWindowTitle(self.tr("About AL\'EXA-IDE"))
        self.setMaximumSize(QSize(0, 0))

        vbox = QVBoxLayout(self)

        #Create an icon for the Dialog
        pixmap = QPixmap(resources.IMAGES['iconalexaabout'])
        self.lblIcon = QLabel()
        self.lblIcon.setPixmap(pixmap)

        self.setStyleSheet("background-color: white; color: black;")


        hbox = QHBoxLayout()
        hbox.addWidget(self.lblIcon)
        '''
        lblTitle = QLabel(
                '<h1>AL\'EXA-IDE</h1>\n<i>By Alan Pipitone<i>')
        lblTitle.setStyleSheet("color:#ff9e21;")
        lblTitle.setTextFormat(Qt.RichText)
        lblTitle.setAlignment(Qt.AlignLeft)
        '''
        #hbox.addWidget(lblTitle)
        vbox.addLayout(hbox)

        #Add description
        vbox.addWidget(QLabel(
self.tr("""AL'EXA-IDE is an integrated development environment specially design
to build Al'exa Test Cases.
AL'EXA-IDE is a total conversion of NINJA-IDE.

AL'EXA-IDE and Al'exa Engine are developed and maintained by
Alan Pipitone.""")))
        vbox.addWidget(QLabel(self.tr("Version: %s") % ninja_ide.__alexaversion__))
        link_alexa = QLabel(
            self.tr('Al\'exa Website: <a href="%s"><span style=" '
            'text-decoration: underline; color:#3414f7;">%s</span></a>') %
                (ninja_ide.__alexaurl__, ninja_ide.__alexaurl__))
        vbox.addWidget(link_alexa)
        link_source = QLabel(
            self.tr('Al\'exa Source Code: <a href="%s"><span style=" '
            'text-decoration: underline; color:#3414f7;">%s</span></a>') %
                (ninja_ide.__alexasource__, ninja_ide.__alexasource__))
        vbox.addWidget(link_source)
        link_ninja = QLabel(
            self.tr('Ninja Website: <a href="%s"><span style=" '
            'text-decoration: underline; color:#3414f7;">%s</span></a>') %
                (ninja_ide.__url__, ninja_ide.__url__))
        vbox.addWidget(link_ninja)

        sponsored = QLabel(self.tr("""
Al'exa is sponsored by:"""))
        vbox.addWidget(sponsored)

                #Create an icon for the Dialog
        pixmap = QPixmap(resources.IMAGES['iconalexaaboutsponsor'])
        self.lblIcon = QLabel()
        self.lblIcon.setPixmap(pixmap)

        hbox = QHBoxLayout()
        hbox.addWidget(self.lblIcon)

        vbox.addLayout(hbox)

        link_wuerth = QLabel(
            self.tr('NetEye Website: <a href="%s"><span style=" '
            'text-decoration: underline; color:#3414f7;">%s</span></a>') %
                (ninja_ide.__neteyewebsite__, ninja_ide.__neteyewebsite__))
        vbox.addWidget(link_wuerth)

        self.connect(link_alexa, SIGNAL("linkActivated(QString)"),
            self.link_activated)

        self.connect(link_source, SIGNAL("linkActivated(QString)"),
            self.link_activated)

        self.connect(link_ninja, SIGNAL("linkActivated(QString)"),
            self.link_activated)

        self.connect(link_wuerth, SIGNAL("linkActivated(QString)"),
            self.link_activated)

    def link_activated(self, link):
        webbrowser.open(str(link))
