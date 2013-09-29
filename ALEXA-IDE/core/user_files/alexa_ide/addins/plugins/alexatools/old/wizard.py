# *-* coding: UTF-8 *-*

import re

from PyQt4.QtGui import QWizardPage
from PyQt4.QtGui import QGridLayout
from PyQt4.QtGui import QLabel
from PyQt4.QtGui import QLineEdit
from PyQt4.QtGui import QCheckBox
from PyQt4.QtGui import QMessageBox
from PyQt4.QtGui import QPushButton
from PyQt4.QtCore import SIGNAL
from PyQt4.QtGui import QFileDialog


class PagePluginProperties(QWizardPage):

    def __init__(self, locator):
        QWizardPage.__init__(self)
        # service locator
        self.locator = locator
        # grid
        grid = QGridLayout(self)
        grid.addWidget(QLabel('Ocr Data Folder:'), 0, 0)
        self.txtOcrLangFolder = QLineEdit()
        grid.addWidget(self.txtOcrLangFolder, 0, 1)
        self.registerField('ocrLangFolder*', self.txtOcrLangFolder)
        self.btnExamineOcrFolder = QPushButton(self.tr("Browse..."))
        grid.addWidget(self.btnExamineOcrFolder, 0, 2)

        grid.addWidget(QLabel('Log Folder:'), 1, 0)
        self.txtLogFolder = QLineEdit()
        grid.addWidget(self.txtLogFolder, 1, 1)
        self.registerField('txtLogFolder*', self.txtLogFolder)
        self.btnExamineLogFolder = QPushButton(self.tr("Browse..."))
        grid.addWidget(self.btnExamineLogFolder, 1, 2)

        grid.addWidget(QLabel('Author(s):'), 2, 0)
        self.txtAuthors = QLineEdit()
        grid.addWidget(self.txtAuthors, 2, 1)
        self.registerField('txtAuthors', self.txtAuthors)

        grid.addWidget(QLabel('Website:'), 3, 0)
        self.txtUrl = QLineEdit()
        grid.addWidget(self.txtUrl, 3, 1)

        self.connect(self.btnExamineOcrFolder, SIGNAL('clicked()'), self.load_ocrLangFolder)
        self.connect(self.btnExamineLogFolder, SIGNAL('clicked()'), self.load_LogFolder)

    def load_ocrLangFolder(self):
        self.txtOcrLangFolder.setText(QFileDialog.getExistingDirectory(
            self, self.tr("Select Ocr Languages Folder")))

    def load_LogFolder(self):
        self.txtLogFolder.setText(QFileDialog.getExistingDirectory(
            self, self.tr("Select Log Folder")))

    def validatePage(self):
        return True
