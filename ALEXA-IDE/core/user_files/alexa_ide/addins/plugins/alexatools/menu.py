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

#from tempfile import mkstemp
#from shutil import move
import os
import copy
#import fileinput

from PyQt4.QtGui import QMenu
from PyQt4.QtGui import QMessageBox
from PyQt4.QtCore import SIGNAL
from PyQt4.QtCore import QProcess
from PyQt4.QtGui import QFileDialog

from ninja_ide import resources
from ninja_ide.tools import json_manager


class Menu(QMenu):

    def __init__(self, locator):
        QMenu.__init__(self, 'Al\'exa Project: IDE Properties')
        self.ocrdatafolder = ""
        self.logFolder = ""
        self._locator = locator
        self.explorer_s = self._locator.get_service('explorer')
        self._proc = QProcess(self)
        action_change_ocr_data_folder = self.addAction('Select Ocr Data Folder')
        self.connect(action_change_ocr_data_folder, SIGNAL("triggered()"), self.change_ocr_data_folder)

        action_change_log_folder = self.addAction('Select Log Folder')
        self.connect(action_change_log_folder, SIGNAL("triggered()"), self.change_log_folder)

    def change_ocr_data_folder(self):
        folder = self.explorer_s.get_tree_projects()._get_project_root().path
        plugin = json_manager.read_ninja_project(folder)

        self.ocrdatafolder = QFileDialog.getExistingDirectory(
            self, self.tr("Select Ocr Languages Folder"), plugin["ocrdatafolder"])

        if self.ocrdatafolder != "":
            plugin["ocrdatafolder"] = self.ocrdatafolder
            json_manager.create_ninja_project(folder, plugin["name"], plugin)

    def change_log_folder(self):
        folder = self.explorer_s.get_tree_projects()._get_project_root().path
        plugin = json_manager.read_ninja_project(folder)

        self.logFolder = QFileDialog.getExistingDirectory(
            self, self.tr("Select Log Folder"), plugin["logfolder"])

        if self.logFolder != "":
            plugin["logfolder"] = self.logFolder
            json_manager.create_ninja_project(folder, plugin["name"], plugin)

    def replace(self, file_path, pattern, subst):
        #Create temp file
        f = open(file_path, 'r+')
        text = f.read()
        text = text.replace(pattern, subst)
        f.seek(0)
        f.write(text)
        f.truncate()
        f.close()
        '''
        fh, abs_path = mkstemp()
        new_file = open(abs_path,'w')
        old_file = open(file_path)
        for line in old_file:
            new_file.write(line.replace(pattern, subst))
        #close temp file
        new_file.close()
        os.close(fh)
        old_file.close()
        #Remove original file
        os.remove(file_path)
        #Move new file
        move(abs_path, file_path)
        '''