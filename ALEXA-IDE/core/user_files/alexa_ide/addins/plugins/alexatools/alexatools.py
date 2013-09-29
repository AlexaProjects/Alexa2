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
import time
#NINJA
from ninja_ide.core import plugin
from ninja_ide.tools import json_manager
from ninja_ide.core import plugin_interfaces
from ninja_ide.core import file_manager

try:
    import json
except ImportError:
    import simplejson as json

#alexaplugin
from appobjectcapturescreen import AppObjectCaptureScreenshot
from appimagecapturescreen import AppImageCaptureScreenshot
from apptextcapturescreen import AppTextCaptureScreenshot
from wizard import PagePluginProperties
from menu import Menu
from exportedmenu import ExportedMenu
from nagiostools import NagiosTools
from mousekeyboard import MouseKeyboard
from windowregion import WindowRegion
from processutils import ProcessUtils
from emailutils import EmailUtils
import closewindow


PROJECT_TYPE = "Al\'exa Test Case"
#QT Toolkit
from PyQt4.QtGui import *
from PyQt4.QtCore import *

#WX
import wx
#ALEXA
from Alexa import *

if sys.platform == 'win32':
    import win32gui
    import win32con


class AlexaTools(plugin.Plugin):

    def initialize(self):
        # Init your plugin
        self.AlexaAppObjCnt = 0
        self.AlexaAppImgCnt = 0
        #self.explorer_s = self.locator.get_service('explorer')
        #self.explorer_s.add_tab(AAA(self), 'Al\'exa Tools')

        self.undockWindow = None
        self.undockWindowOpened = False
        self.screenshotDelay = 0

        self.plug_path = os.path.abspath(__file__)
        self.plug_path = os.path.dirname(self.path)

        self.toolbar_s = self.locator.get_service('toolbar')
        #self.toolbar_s.setIconSize(QSize(16,32))

        toolBarAlexaBindWinReg = QAction(QIcon(self.plug_path + "/alexatools/images/preferences-desktop-theme.png"), 'Bind Windows and Region', self)
        self.connect(toolBarAlexaBindWinReg, SIGNAL('triggered()'), self.OpenWindowBind)
        self.toolbar_s.add_action(toolBarAlexaBindWinReg)

        toolBarAlexaBindObject = QAction(QIcon(self.plug_path + "/alexatools/images/bind.png"), 'Bind Application Objects',self)
        #toolBarAlexaBindObject.setShortcut('Ctrl+Q')
        #toolBarAlexaBindObject.setStatusTip('Bind Application Objects')
        self.connect(toolBarAlexaBindObject, SIGNAL('triggered()'), self.OpenAppObjectCaptureScreen)
        self.toolbar_s.add_action(toolBarAlexaBindObject)

        toolBarAlexaBindImage = QAction(QIcon(self.plug_path + "/alexatools/images/image.png"), 'Bind Application Images', self)
        self.connect(toolBarAlexaBindImage, SIGNAL('triggered()'), self.OpenAppImageCaptureScreen)
        self.toolbar_s.add_action(toolBarAlexaBindImage)

        toolBarAlexaBindText = QAction(QIcon(self.plug_path + "/alexatools/images/text-x-gettext-translation.png"), 'Bind Application Text', self)
        self.connect(toolBarAlexaBindText, SIGNAL('triggered()'), self.OpenAppTextCaptureScreen)
        self.toolbar_s.add_action(toolBarAlexaBindText)

        toolBarAlexaEmail = QAction(QIcon(self.plug_path + "/alexatools/images/mail-foward.png"), 'E-Mail', self)
        self.connect(toolBarAlexaEmail, SIGNAL('triggered()'), self.ShowEmailUtils)
        self.toolbar_s.add_action(toolBarAlexaEmail)

        toolBarAlexaProcesses = QAction(QIcon(self.plug_path + "/alexatools/images/gksu-root-terminal.png"), 'Process Utilities', self)
        self.connect(toolBarAlexaProcesses, SIGNAL('triggered()'), self.ShowProcessUtils)
        self.toolbar_s.add_action(toolBarAlexaProcesses)

        toolBarAlexaMouse = QAction(QIcon(self.plug_path + "/alexatools/images/input-mouse-6.png"), 'Mouse and Keyboard Actions', self)
        self.connect(toolBarAlexaMouse, SIGNAL('triggered()'), self.OpenMouseAndKeyboard)
        self.toolbar_s.add_action(toolBarAlexaMouse)

        toolBarAlexaNagios = QAction(QIcon(self.plug_path + "/alexatools/images/view-statistics2.png"), 'Nagios Utilities', self)
        #toolBarAlexaNagios = QAction(QIcon(self.plug_path + "/alexatools/images/gnome-power-statistics.png"), 'Nagios Utilities', self)
        self.connect(toolBarAlexaNagios, SIGNAL('triggered()'), self.ShowNagiosUtils)
        self.toolbar_s.add_action(toolBarAlexaNagios)

        toolBarAlexaUndock = QAction(QIcon(self.plug_path + "/alexatools/images/view-sort-ascending.png"), 'Export Al\'exa Tools', self)
        self.connect(toolBarAlexaUndock, SIGNAL('triggered()'), self.Undock)
        self.toolbar_s.add_action(toolBarAlexaUndock)

        SERVICE_NAME = 'explorer'
        self.explorer_s = self.locator.get_service(SERVICE_NAME)
        alexa_project_handler = AlexaProjectHandler(self.locator)
        self.explorer_s.set_project_type_handler(PROJECT_TYPE, alexa_project_handler)

        #SERVICE_NAME = "editor"
        #editor_service = self.locator.get_service(SERVICE_NAME)
        #editor_service.fileSaved.connect(self.FileSavedHandler)
        #editor_service.fileOpened.connect(self.FileSavedHandler)

    def FileSavedHandler(self, fileName):
        self.ChangeOcrDataFolder(fileName)

    def FileOpenedHandler(self, fileName):
        self.ChangeOcrDataFolder(fileName)

    def ChangeOcrDataFolder(self, fileName):
        #the code goes here!
        #print fileName
        dataPath = ""
        f = open(fileName)
        for line in f:
            #print line
            if "Ocr.Data =" in line or "Ocr.Data=" in line:
                try:
                    if line.index('#') < line.index('Ocr.Data'):
                        continue
                except:
                    pass
                dataPath = line.split('=')[1]
                dataPath = dataPath.strip()
                #print dataPath

        f.close()

        if dataPath != "":
            try:
                jsfile = json_manager.read_json(fileName.replace(".py", ".nja"))
                jsfile['ocrdatafolder'] = dataPath.replace("\\\\", "\\")
                jsfile['ocrdatafolder'] = jsfile['ocrdatafolder'].replace("\"", "")
                #print jsfile
                fileNameWithExtension = os.path.split(fileName)[1]
                fileNameWithOutExtension = os.path.splitext(fileNameWithExtension)[0]
                json_manager.create_ninja_project(os.path.split(fileName)[0], fileNameWithOutExtension, jsfile)
            except:
                pass

    def HideEditor(self):

        self.plugin = plugin

        SERVICE_NAME = "editor"
        self.editor_service = self.locator.get_service(SERVICE_NAME)
        fullFileName = self.editor_service.get_editor_path()

        try:  # check if .nja file exists
            filePath = os.path.split(fullFileName)[0]
            fileName = os.path.split(fullFileName)[1]
            #print os.path.splitext(fileName)[1]
            self.jsonfile = json_manager.read_json(filePath + os.sep + fileName.replace(os.path.splitext(fileName)[1], ".nja"))
            #filetoparse = filePath + os.sep + fileName.replace("py", "nja")
            self.ocrdata = self.jsonfile["ocrdatafolder"]
        except:
            self.message = QMessageBox.critical(self.editor_service.get_editor(), 'Error', "You can use this button only on an Al'exa Project!", QMessageBox.Ok)
            return


        #if self.undockWindowOpened is True:
            #self.undockWindow.close()

        closewindow.CloseHideAllWindow(True)

        if self.undockWindowOpened is True:
            self.undockWindow.setVisible(False)
        elif sys.platform == 'win32':
            hwnd = win32gui.GetForegroundWindow()
            win32gui.ShowWindow(hwnd, 0)

            toplist = []
            winlist = []

            def enum_callback(hwnd, results):
                winlist.append((hwnd, win32gui.GetWindowText(hwnd)))
            win32gui.EnumWindows(enum_callback, toplist)
            #if self.undocked is False:
            firefox = [(hwnd, title) for hwnd, title in
                winlist if 'exa-ide' in title.lower() or 'exa tool' in title.lower() and 'about' not in title.lower() and 'command prompt' not in title.lower()]

            # just grab the first window that matches
            #firefox = firefox[0]
            for ninja in firefox:
                #print str(ninja[0]) + " " + ninja[1]
                win32gui.ShowWindow(ninja[0], 0)
            #else:
                #self.undockWindow.hide()

        time.sleep(0.5)

        if self.undockWindowOpened is True:
            time.sleep(self.screenshotDelay)

        app = wx.App(False)
        screen = wx.ScreenDC()
        size = screen.GetSize()
        bmp = wx.EmptyBitmap(size[0], size[1])
        mem = wx.MemoryDC(bmp)
        mem.Blit(0, 0, size[0], size[1], screen, 0, 0)
        del mem  # Release bitmap
        bmp.SaveFile(self.plug_path + os.sep +'alexatools' + os.sep + 'tmp' + os.sep + 'screenshot.png', wx.BITMAP_TYPE_PNG)

    def OpenAppObjectCaptureScreen(self):
        self.HideEditor()
        self.window = AppObjectCaptureScreenshot(self)
        self.window.setWindowTitle("alexa screen")
        self.window.showFullScreen()
        self.window.setMouseTracking(True)

    def OpenAppImageCaptureScreen(self):
        self.HideEditor()
        self.window = AppImageCaptureScreenshot(self)
        self.window.setWindowTitle("alexa screen")
        self.window.showFullScreen()
        self.window.setMouseTracking(True)

    def OpenAppTextCaptureScreen(self):
        self.HideEditor()
        self.window = AppTextCaptureScreenshot(self)
        self.window.setWindowTitle("alexa screen")
        self.window.showFullScreen()
        self.window.setMouseTracking(True)

    def OpenWindowBind(self):
        SERVICE_NAME = "editor"
        self.editor_service = self.locator.get_service(SERVICE_NAME)
        fullFileName = self.editor_service.get_editor_path()

        try:  # check if .nja file exists
            filePath = os.path.split(fullFileName)[0]
            fileName = os.path.split(fullFileName)[1]
            #print os.path.splitext(fileName)[1]
            self.jsonfile = json_manager.read_json(filePath + os.sep + fileName.replace(os.path.splitext(fileName)[1], ".nja"))
            #filetoparse = filePath + os.sep + fileName.replace("py", "nja")
            self.ocrdata = self.jsonfile["ocrdatafolder"]
        except:
            self.message = QMessageBox.critical(self.editor_service.get_editor(), 'Error', "You can use this button only on an Al'exa Project!", QMessageBox.Ok)
            return
        self.windowRegion = WindowRegion(self)
        self.windowRegion.show()

    def OpenMouseAndKeyboard(self):
        SERVICE_NAME = "editor"
        self.editor_service = self.locator.get_service(SERVICE_NAME)
        fullFileName = self.editor_service.get_editor_path()

        try:  # check if .nja file exists
            filePath = os.path.split(fullFileName)[0]
            fileName = os.path.split(fullFileName)[1]
            #print os.path.splitext(fileName)[1]
            self.jsonfile = json_manager.read_json(filePath + os.sep + fileName.replace(os.path.splitext(fileName)[1], ".nja"))
            #filetoparse = filePath + os.sep + fileName.replace("py", "nja")
            self.ocrdata = self.jsonfile["ocrdatafolder"]
        except:
            self.message = QMessageBox.critical(self.editor_service.get_editor(), 'Error', "You can use this button only on an Al'exa Project!", QMessageBox.Ok)
            return
        self.mouseAndKey = MouseKeyboard(self)
        self.mouseAndKey.show()

    def ShowProcessUtils(self):

        SERVICE_NAME = "editor"
        self.editor_service = self.locator.get_service(SERVICE_NAME)
        fullFileName = self.editor_service.get_editor_path()

        try:  # check if .nja file exists
            filePath = os.path.split(fullFileName)[0]
            fileName = os.path.split(fullFileName)[1]
            #print os.path.splitext(fileName)[1]
            self.jsonfile = json_manager.read_json(filePath + os.sep + fileName.replace(os.path.splitext(fileName)[1], ".nja"))
            #filetoparse = filePath + os.sep + fileName.replace("py", "nja")
            self.ocrdata = self.jsonfile["ocrdatafolder"]
        except:
            self.message = QMessageBox.critical(self.editor_service.get_editor(), 'Error', "You can use this button only on an Al'exa Project!", QMessageBox.Ok)
            return
        self.processUtils = ProcessUtils(self)
        self.processUtils.show()

    def ShowEmailUtils(self):

        SERVICE_NAME = "editor"
        self.editor_service = self.locator.get_service(SERVICE_NAME)
        fullFileName = self.editor_service.get_editor_path()

        try:  # check if .nja file exists
            filePath = os.path.split(fullFileName)[0]
            fileName = os.path.split(fullFileName)[1]
            #print os.path.splitext(fileName)[1]
            self.jsonfile = json_manager.read_json(filePath + os.sep + fileName.replace(os.path.splitext(fileName)[1], ".nja"))
            #filetoparse = filePath + os.sep + fileName.replace("py", "nja")
            self.ocrdata = self.jsonfile["ocrdatafolder"]
        except:
            self.message = QMessageBox.critical(self.editor_service.get_editor(), 'Error', "You can use this button only on an Al'exa Project!", QMessageBox.Ok)
            return
        self.emailUtils = EmailUtils(self)
        self.emailUtils.show()

    def ShowNagiosUtils(self):

        SERVICE_NAME = "editor"
        self.editor_service = self.locator.get_service(SERVICE_NAME)
        fullFileName = self.editor_service.get_editor_path()

        try:  # check if .nja file exists
            filePath = os.path.split(fullFileName)[0]
            fileName = os.path.split(fullFileName)[1]
            #print os.path.splitext(fileName)[1]
            self.jsonfile = json_manager.read_json(filePath + os.sep + fileName.replace(os.path.splitext(fileName)[1], ".nja"))
            #filetoparse = filePath + os.sep + fileName.replace("py", "nja")
            self.ocrdata = self.jsonfile["ocrdatafolder"]
        except:
            self.message = QMessageBox.critical(self.editor_service.get_editor(), 'Error', "You can use this button only on an Al'exa Project!", QMessageBox.Ok)
            return
        self.nagiosTools = NagiosTools(self)
        self.nagiosTools.show()

    def Undock(self):
        #self.undocked = True
        self.undockWindowOpened = True
        self.undockWindow = ExportedMenu(self)
        self.undockWindow.show()

        '''
        self.undockWindow.setWindowTitle("Al\'exa tools")
        self.undockWindow.resize(490, 36)

        self.undockWindow.setStyleSheet("""
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

        self.pushButtonAppObj = QPushButton(self.undockWindow)
        self.pushButtonAppObj.setGeometry(QRect(8, 5, 34, 28))
        iconAppObj = QIcon()
        iconAppObj.addPixmap(QPixmap(self.plug_path + "/alexatools/images/bind.png"), QIcon.Normal, QIcon.Off)
        self.pushButtonAppObj.setIcon(iconAppObj)
        self.pushButtonAppObj.setIconSize(QSize(24, 24))
        self.pushButtonAppObj.setToolTip("Bind Application Objects (Ctrl + O)")


        self.pushButtonAppImage = QPushButton(self.undockWindow)
        self.pushButtonAppImage.setGeometry(QRect(51, 4, 34, 28))
        iconAppImg = QIcon()
        iconAppImg.addPixmap(QPixmap(self.plug_path + "/alexatools/images/image.png"), QIcon.Normal, QIcon.Off)
        self.pushButtonAppImage.setIcon(iconAppImg)
        self.pushButtonAppImage.setIconSize(QSize(24, 24))
        self.pushButtonAppImage.setToolTip("Bind Application Images (Ctrl + I)")

        self.pushButtonAppText = QPushButton(self.undockWindow)
        self.pushButtonAppText.setGeometry(QRect(94, 4, 34, 28))
        iconAppText = QIcon()
        iconAppText.addPixmap(QPixmap(self.plug_path + "/alexatools/images/text-x-gettext-translation.png"), QIcon.Normal, QIcon.Off)
        self.pushButtonAppText.setIcon(iconAppText)
        self.pushButtonAppText.setIconSize(QSize(24, 24))
        self.pushButtonAppText.setToolTip("Bind Application Text (Ctrl + T)")


        #self.pushButtonAppObj = QPushButton(self.window)
        self.undockWindow.setWindowFlags(Qt.WindowCloseButtonHint | Qt.WindowStaysOnTopHint)
        self.undockWindow.setFixedSize(self.undockWindow.size())

        self.undockWindow.connect(self.pushButtonAppObj, SIGNAL("clicked()"), self.OpenAppObjectCaptureScreen)
        shortcutObj = QShortcut(QKeySequence("Ctrl+O"), self.undockWindow);
        self.undockWindow.connect(shortcutObj, SIGNAL("activated()"), self.OpenAppObjectCaptureScreen);

        self.undockWindow.connect(self.pushButtonAppImage, SIGNAL("clicked()"), self.OpenAppImageCaptureScreen)
        shortcutImg = QShortcut(QKeySequence("Ctrl+I"), self.undockWindow);
        self.undockWindow.connect(shortcutImg, SIGNAL("activated()"), self.OpenAppImageCaptureScreen);

        self.undockWindow.connect(self.pushButtonAppText, SIGNAL("clicked()"), self.OpenAppTextCaptureScreen)
        shortcutTxt = QShortcut(QKeySequence("Ctrl+T"), self.undockWindow);
        self.undockWindow.connect(shortcutTxt, SIGNAL("activated()"), self.OpenAppTextCaptureScreen);

        self.undockWindow.show()

        #print self.undockWindow.parentWidget()
        '''

    def finish(self):
        # Shutdown your plugin
        if self.undockWindow is not None:
            self.undockWindow.close()

    def get_preferences_widget(self):
        # Return a widget for customize your plugin
        pass


class AlexaProjectHandler(plugin_interfaces.IProjectTypeHandler):

    EXT = '.alexa'

    def __init__(self, locator):
        self.locator = locator

    def get_context_menus(self):
        return (Menu(self.locator), )

    def get_pages(self):
        return [PagePluginProperties(self.locator)]

    def on_wizard_finish(self, wizard):
        global PROJECT_TYPE
        ids = wizard.pageIds()
        # Manipulate default data for NINJA-IDE projects
        page = wizard.page(ids[2])
        path = unicode(page.txtPlace.text())
        if not path:
            QMessageBox.critical(self, self.tr("Incorrect Location"),
                self.tr("The project couldn\'t be create"))
            return
        project = {}
        name = unicode(page.txtName.text())
        project['name'] = name
        project['project-type'] = PROJECT_TYPE
        project['description'] = unicode(page.txtDescription.toPlainText())
        project['license'] = unicode(page.cboLicense.currentText())
        project['venv'] = unicode(page.vtxtPlace.text())

        # Manipulate plugin project data
        page = wizard.page(ids[1])
        project['ocrdatafolder'] = str(page.txtOcrLangFolder.text())
        project['logfolder'] = str(page.txtLogFolder.text())
        project['author'] = str(page.txtAuthors.text())
        project['website'] = str(page.txtUrl.text())

        # Create a folder to contain all the project data (<path>/<name>/)
        #path = os.path.join(path, name)
        if not os.path.exists(path):
            file_manager.create_folder(path, add_init_file=False)

        logPath = unicode(page.txtLogFolder.text())
        if not os.path.exists(logPath):
            file_manager.create_folder(logPath, add_init_file=False)
        # Create the .nja file
        json_manager.create_ninja_project(path, name, project)

        #plugin_dict = self.create_descriptor(page, path)
        self.create_plugin_class(page, path, project)

        # Load the project!
        wizard._load_project(path)

    def create_descriptor(self, page, path):
        plugin = {}

        plugin['ocrdatafolder'] = unicode(page.txtOcrLangFolder.text())
        plugin['logfolder'] = unicode(page.txtLogFolder.text())

        fileName = os.path.join(path, "alexa.desc")
        # Create the .plugin file with metadata
        self.create_file(fileName, plugin)
        # Return the dictionary
        return plugin

    def create_plugin_class(self, page, path, plugin_dict):
        name = plugin_dict['name']
        author = plugin_dict['author']
        website = plugin_dict['website']
        description = plugin_dict['description']
        logFolder = plugin_dict['logfolder']
        ocrFolder = plugin_dict['ocrdatafolder']

        authWebsDesc = "# -*- coding: UTF-8 -*-"

        if author != "":
            authWebsDesc = authWebsDesc + os.linesep + "'''" + os.linesep + "AUTHOR: " + author + os.linesep
        if website != "":
            if author != "":
                authWebsDesc = authWebsDesc + "WEBSITE: " + website + os.linesep
            else:
                authWebsDesc = authWebsDesc + os.linesep + "'''" + os.linesep + "WEBSITE: " + website + os.linesep
        if description != "":
            if author != "" or website != "":
                authWebsDesc = authWebsDesc + "DESCRIPTION:" + os.linesep + description + os.linesep
            else:
                authWebsDesc = authWebsDesc + os.linesep + "'''" + os.linesep + "DESCRIPTION: " + description + os.linesep

        if authWebsDesc != "# -*- coding: UTF-8 -*-":
            authWebsDesc = authWebsDesc + "'''"
        content = TEMPLATE_PLUGIN_HEADER % authWebsDesc
        content = content + TEMPLATE_PLUGIN_BEGIN
        content = content + TEMPLATE_USERCODE_SECTION
        content = content + TEMPLATE_SETUP_SECTION
        content = content + TEMPLATE_OCR_SECTION % ocrFolder.replace("\\", "\\\\")
        content = content + TEMPLATE_LOG_SECTION % logFolder.replace("\\", "\\\\")
        content = content + TEMPLATE_NAGIOS_SECTION
        content = content + TEMPLATE_END_SECTION
        '''
        if page.checkEditorS.checkState() == Qt.Checked:
            content += TEMPLATE_EDITOR_S
            completed = True

        if page.checkToolbarS.checkState() == Qt.Checked:
            content += TEMPLATE_TOOLBAR_S
            completed = True

        if page.checkMenuPluginS.checkState() == Qt.Checked:
            content += TEMPLATE_MENU_S
            completed = True

        if page.checkMiscS.checkState() == Qt.Checked:
            content += TEMPLATE_MISC_S
            completed = True

        if page.checkExplorerS.checkState() == Qt.Checked:
            content += TEMPLATE_EXPLORER_S
            completed = True

        if not completed:
            content += TEMPLATE_PASS_STATMENT

        content += TEMPLATE_PLUGIN_FINISH
        '''
        content = content
        # Create the folder
        #file_manager.create_folder(os.path.join(path, module))
        # Create the file
        fileName = os.path.join(path, name + '.py')
        # Write to the file
        file_manager.store_file_content(fileName, content)
        # Create the __init__.py with the imports!
        #file_manager.create_init_file_complete(os.path.join(path, module))

    def create_file(self, fileName, structure):
        f = open(fileName, mode='w')
        json.dump(structure, f, indent=2)
        f.close()


###############################################################################
# TEMPLATES
###############################################################################

TEMPLATE_PLUGIN_HEADER = """%s
"""

TEMPLATE_PLUGIN_BEGIN = """
import os
import sys
import time
import subprocess
from Alexa import *

ProjectPath = os.path.dirname(os.path.realpath(__file__))
RunStartString = time.strftime("%d_%b_%Y__%H_%M_%S", time.localtime())
ExitOnError = True

"""

TEMPLATE_SETUP_SECTION = """
def Setup():
"""

TEMPLATE_OCR_SECTION = """
    Ocr.Data = "%s"
"""

TEMPLATE_LOG_SECTION = """
        #Alexa Log
    Log.DisableConsoleOutput()
    Log.Enable = True
    Log.DebugImages = True
    Log.Level = "debug"
    Log.Path = "%s\\\\" + RunStartString
    #end...
"""

TEMPLATE_NAGIOS_SECTION = """
    #Init here your Nagios Data Source

"""
TEMPLATE_USERCODE_SECTION = """
def Main():
    try:
        #Insert here your test case code
    except Exception, error:
        errorLine = str(sys.exc_traceback.tb_lineno)
        Finish("UNKNOWN: an exception has occurred at line " + errorLine +
        ": " + str(error), 3)

"""

TEMPLATE_END_SECTION = """
def Finish(message=None, exitcode=None):

    Log.EnableConsoleOutput()

    if message is None:
        NagiosUtils.PrintOutput()
    else:
        NagiosUtils.PrintOutput(message)

    if exitcode is None:
        sys.exit(NagiosUtils.GetExitCode())
    else:
        sys.exit(exitcode)


if __name__ == '__main__':
    try:
        Setup()
        Main()
        Finish()
    except Exception, error:
        errorLine = str(sys.exc_traceback.tb_lineno)
        Finish("UNKNOWN: an exception has occurred at line " + errorLine +
        ": " + str(error), 3)
"""