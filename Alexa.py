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

#from __future__ import division
import time
#PIL
import Image
import ImageGrab
import ImageFilter
import ImageEnhance
#OPENCV
import cv2
import cv2.cv as cv
#TESSERACT
import tesseract
#NUMPY
import numpy
#PYTHON
import re
import os
import sys
import subprocess
import locale
import xml.etree.ElementTree as ET
from datetime import datetime
import threading
#import math

if sys.platform == 'win32':
	#PWIN32
	import win32gui
	import win32api, win32con, win32com
	import win32com.client as comclt
	from ctypes import *

	
class Log:
	DebugImages = False
	Level = "error"
	Enable = False
	Path = "Log"
	ImagePath = ""
	ImagePathSubFolder = ""
	ErrorImagePath = ""
	LogFileName = ""
	Path = ""
	LastTimedOutStep = ""
	IsInError = False
	ErrorMotivation = ""
	ExitOnError = False
	null_fds = [os.open(os.devnull, os.O_RDWR) for x in xrange(2)]
	save = os.dup(1), os.dup(2)
	
	@staticmethod
	def LastMethodError():
		if Log.IsInError == True:
			return True
		else:
			return False
			
	@staticmethod
	def DisableConsoleOutput():
		# open 2 fds
		Log.null_fds = [os.open(os.devnull, os.O_RDWR) for x in xrange(2)]
		# save the current file descriptors to a tuple
		Log.save = os.dup(1), os.dup(2)
		# put /dev/null fds on 1 and 2
		os.dup2(Log.null_fds[0], 1)
		os.dup2(Log.null_fds[1], 2)
		
	@staticmethod
	def EnableConsoleOutput():
		# restore file descriptors so I can print the results
		os.dup2(Log.save[0], 1)
		os.dup2(Log.save[1], 2)
		# close the temporary fds
		os.close(Log.null_fds[0])
		os.close(Log.null_fds[1])
			
	@staticmethod
	def CheckImageFolder():
		Log.ImagePath = Log.Path + os.sep + "Debug_Images" + os.sep + Log.ImagePathSubFolder
		Log.LogFileName = Log.Path + os.sep + "Alexa.log"
		
		if not os.path.exists(Log.ImagePath):
			os.makedirs(Log.ImagePath)
			
	@staticmethod
	def CheckErrorImageFolder():
		Log.ErrorImagePath = Log.Path + os.sep + "ERROR_IMAGES"
		Log.LogFileName = Log.Path + os.sep + "Alexa.log"
		
		if not os.path.exists(Log.ErrorImagePath):
			os.makedirs(Log.ErrorImagePath)
			
	@staticmethod
	def CheckFolder():
		Log.LogFileName = Log.Path + os.sep + "Alexa.log"
		if not os.path.exists(Log.Path):
			os.makedirs(Log.Path)
	
	@staticmethod
	def WriteCv2Image(imagename, image):
		if Log.Enable is True and Log.DebugImages is True and Log.Level.lower() == "debug":
			
			Log.CheckImageFolder()
			
			fullname = Log.ImagePath + os.sep + imagename
				
			with open(Log.LogFileName, "a") as text_file:
				text_file.write(time.strftime("%d/%b/%Y %H:%M:%S", time.localtime()) +
					"  DEBUG MESSAGE:  saving debug image " + fullname + os.linesep)	
			cv2.imwrite(fullname, image)
	
	@staticmethod	
	def WritePilImage(imagename, image):
		if Log.Enable is True and Log.DebugImages is True and Log.Level.lower() == "debug":
		
			Log.CheckImageFolder()
		
			fullname = Log.ImagePath + os.sep + imagename
				
			with open(Log.LogFileName, "a") as text_file:
				text_file.write(time.strftime("%d/%b/%Y %H:%M:%S", time.localtime()) +
					"  DEBUG MESSAGE:  saving debug image " + fullname + os.linesep)	
				
			image.save(fullname)
	
	@staticmethod
	def WriteCvImage(imagename, image):
		if Log.Enable is True and Log.DebugImages is True and Log.Level.lower() == "debug":
				
			Log.CheckImageFolder()
				
			fullname = Log.ImagePath + os.sep + imagename
				
			with open(Log.LogFileName, "a") as text_file:
				text_file.write(time.strftime("%d/%b/%Y %H:%M:%S", time.localtime()) +
					"  DEBUG MESSAGE:  saving debug image " + fullname + os.linesep)
				
			cv.SaveImage(fullname,image)
	
	@staticmethod	
	def WriteErrorImage(imagename,image):
		if Log.Enable is True:
		
			Log.CheckErrorImageFolder()

			fullname = Log.ErrorImagePath + os.sep + imagename

			#GrabDesktop().save(fullname)
			image.save(fullname)
	
	@staticmethod	
	def WriteMessage(level, message):
		if Log.Enable is True:
		
			try:
				#unicode(message,"UTF-8")
				if level.lower() == "debug" and Log.Level.lower() == "debug":
					
					Log.CheckFolder()
					
					with open(Log.LogFileName, "a") as text_file:
						text_file.write(time.strftime("%d/%b/%Y %H:%M:%S", time.localtime()) +
						"  DEBUG MESSAGE:  " + message + os.linesep)	
						
				elif level.lower() == "warning" and (Log.Level.lower() == "debug" or Log.Level.lower() == "warning"):
				
					Log.CheckFolder()
					
					with open(Log.LogFileName, "a") as text_file:
						text_file.write(time.strftime("%d/%b/%Y %H:%M:%S", time.localtime()) +
						"  WARNING MESSAGE:  " + message + os.linesep)	

				elif level.lower() == "error":
				
					Log.CheckFolder()
				
					with open(Log.LogFileName, "a") as text_file:
						text_file.write(time.strftime("%d/%b/%Y %H:%M:%S", time.localtime()) +
						"  ERROR MESSAGE:  " + message + os.linesep)	
			except Exception, err:
				print "an exception has occurred: " + str(err) + " on line " + str(sys.exc_traceback.tb_lineno)


class Mail:
	ErrorScreenFolder = ""
	SmtpServer = ""
	SmtpPort = 25
	From = ""
	To = ""
	Subject = ""
	Message = ""
	SmtpUser = "none"
	SmtpPassword = "none"
	ResizeFactor = 80
	ImageQuality = 50
				
	@staticmethod
	def Send():
		#print "\"" + Mail.ErrorScreenFolder + "\" " + Mail.SmtpHost + " " + str(Mail.SmtpPort) + " " + Mail.From + " " + Mail.To + " \"" + Mail.Subject + "\" \"" + Mail.Message + "\" " + Mail.SmtpUser + " " + Mail.SmtpPassword + " " + str(Mail.ResizeFactor) + " " + str(Mail.ImageQuality)
		try:
			Log.IsInError = False
			if sys.platform == 'win32':
				RunCmd(["AlexaSendMail.exe", Mail.ErrorScreenFolder, Mail.SmtpServer, str(Mail.SmtpPort), Mail.From, Mail.To, Mail.Subject, Mail.Message, Mail.SmtpUser, Mail.SmtpPassword, str(Mail.ResizeFactor), str(Mail.ImageQuality)], 60).Run()
		except Exception, err:
			Log.IsInError = True
			Log.WriteMessage("ERROR", "an exception has occurred: " + str(err) + " on line " + str(sys.exc_traceback.tb_lineno))

					
class Label:
	def __init__(self):

		self.Width = 0
		self.Height = 0

		self.OffsetX = 0
		self.OffsetY = 0

		self.Position = ""

		self.Text = ""

		self.Binarize = False

		self.Brightness = 0.45
		self.Contrast = 1
		
		self.Language = "eng"


class Ocr:
	Data = ""
	WhiteList = "'0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ&:/-_\,+()*.=[]<>@"
	Language = "eng"
	LastTextFound = ""
	
	Api = tesseract.TessBaseAPI()
	
	@staticmethod
	def Init():
		Ocr.Api.Init(Ocr.Data,Ocr.Language,tesseract.OEM_DEFAULT)
		Ocr.Api.SetPageSegMode(tesseract.PSM_AUTO)
		Ocr.Api.SetVariable("tessedit_char_whitelist", Ocr.WhiteList)
	

	@staticmethod
	def GetText(labelImage, binarize = False, brightness = 0.45, contrast = 1):
			
		timex = time.time()
		
		Ocr.Init()
		
		if binarize is True:
			enhancer = ImageEnhance.Brightness(labelImage)
			labelImage = enhancer.enhance(brightness)
			
			enhancer = ImageEnhance.Contrast(labelImage)
			labelImage = enhancer.enhance(contrast)
			

		color_img = cv.CreateImageHeader(labelImage.size, cv.IPL_DEPTH_8U, 3)

		cv.SetData(color_img, labelImage.tostring())

		grey_img = cv.CreateImage(cv.GetSize(color_img), 8, 1)

		cv.CvtColor(color_img,grey_img,cv.CV_RGB2GRAY) 
			
		if binarize is True:
			threshold=100
			colour=255
			cv.Threshold(grey_img,grey_img, threshold,colour,cv.CV_THRESH_BINARY) 
		
		tesseract.SetCvImage(grey_img,Ocr.Api)
					
		#write debug image
		Log.WriteCvImage(datetime.now().strftime("%H_%M_%S_%f") + '_Grey.png', grey_img)
		
		text=Ocr.Api.GetUTF8Text()
		
		print "text from Ocr engine:",text
		print "ocr time:", time.time() - timex,"sec."

		# write debug message
		Log.WriteMessage("debug", "text from Ocr engine: " + text)	
		
		return text
		
	@staticmethod
	def CompareLabelText(textToCompare, labelImage, binarize = False, brightness = 0.45, contrast = 1):
				
		timex = time.time()
		print Ocr.Data
		Ocr.Init()

		if binarize is True:
			enhancer = ImageEnhance.Brightness(labelImage)
			labelImage = enhancer.enhance(brightness)
			
			enhancer = ImageEnhance.Contrast(labelImage)
			labelImage = enhancer.enhance(contrast)
			

		color_img = cv.CreateImageHeader(labelImage.size, cv.IPL_DEPTH_8U, 3)

		cv.SetData(color_img, labelImage.tostring())

		grey_img = cv.CreateImage(cv.GetSize(color_img), 8, 1)

		cv.CvtColor(color_img,grey_img,cv.CV_RGB2GRAY) 
			
		if binarize is True:
			threshold=100
			colour=255
			cv.Threshold(grey_img,grey_img, threshold,colour,cv.CV_THRESH_BINARY) 
		
		tesseract.SetCvImage(grey_img,Ocr.Api)
					
		#write debug image
		Log.WriteCvImage(datetime.now().strftime("%H_%M_%S_%f") + '_Grey.png', grey_img)
		
		text=Ocr.Api.GetUTF8Text()
				
		result = re.match(".*" + textToCompare + ".*", text, re.DOTALL | re.IGNORECASE)
		#result = re.match(textToCompare, text, re.DOTALL | re.IGNORECASE)
		
		print "text from Ocr engine:",text
		Ocr.LastTextFound = text
		print "ocr time:", time.time() - timex,"sec."

		# write debug message
		Log.WriteMessage("debug", "text from Ocr engine: " + text)	
		
		if result != None:
			return True
		else:
			return False

	@staticmethod
	def GetTextCoordinates(textToCompare, textImage, binarize = False, brightness = 0.45, contrast = 1):
		
		phrase = ""
		concatWord = False
		wordLine = None
		
		timex = time.time()
		
		Ocr.Init()
		
		if binarize is True:
			enhancer = ImageEnhance.Brightness(textImage)
			textImage = enhancer.enhance(brightness)
			
			enhancer = ImageEnhance.Contrast(textImage)
			textImage = enhancer.enhance(contrast)
			

		color_img = cv.CreateImageHeader(textImage.size, cv.IPL_DEPTH_8U, 3)

		cv.SetData(color_img, textImage.tostring())

		grey_img = cv.CreateImage(cv.GetSize(color_img), 8, 1)

		cv.CvtColor(color_img,grey_img,cv.CV_RGB2GRAY) 
			
		if binarize is True:
			threshold=100
			colour=255
			cv.Threshold(grey_img,grey_img, threshold,colour,cv.CV_THRESH_BINARY) 
		
		tesseract.SetCvImage(grey_img,Ocr.Api)
					
		#write debug image
		Log.WriteCvImage(datetime.now().strftime("%H_%M_%S_%f") + '_Grey.png', grey_img)

		#text=Ocr.Api.GetUTF8Text()

		text = Ocr.Api.GetHOCRText(0)
		
		#print text
		root = ET.fromstring(text)
		
		for span in root.iter('span'):
			try:
				#print span.attrib,span.text
				#print span.get('title')
				
				
				title = span.get('title')
				title = title.replace(';','')
				coordinates = title.split(' ')
				
				if span.get('class') == 'ocr_line':
					line = span.get('id')
					line = line.replace('line_','')
					lineNr = line
				
				if 	not span.find('strong') ==  None:
					span.text = span.find('strong').text
				
				if not span.find('em') ==  None:
					span.text = span.find('em').text
				
				if not span.find('strong/em') ==  None:
					span.text = span.find('strong/em').text
					
				if span.text == None:
					continue
				
				phrase = phrase + " " + span.text
				
				result = re.match(".*" + unicode(textToCompare,"UTF-8") + ".*", phrase, re.DOTALL | re.IGNORECASE)
				
				#print span.text," >> line:",lineNr,"coordinates:",int(coordinates[1])/3,int(coordinates[2])/3,int(coordinates[3])/3,int(coordinates[4])/3
				#print "text found:",phrase
			
				#print "tempo ocr", time.time() - timex
				if result != None:

					try:
						print "text from Ocr engine:",phrase			
						print "ocr time:",time.time() - timex,"sec."
					except:
						pass
					
					# write debug message
					Log.WriteMessage("debug", "text from Ocr engine: " + phrase)

					return int(coordinates[1]),int(coordinates[2]),int(coordinates[3]),int(coordinates[4])
					
			except Exception, err:
				Log.IsInError = True
				Log.WriteMessage("ERROR", "an exception has occurred: " + str(err) + " on line " + str(sys.exc_traceback.tb_lineno))
		
		try:
			print "text from Ocr engine:",phrase
			print "ocr time:",time.time() - timex,"sec."
		except:
			pass
			
		# write debug message
		Log.WriteMessage("debug", "text from Ocr engine: " + phrase)
		
		return None
				
		
class Window:

	Title = None
	TitleRegEx = None
	Timeout = 15
	Hwnd = None
	Bbox = None
	x = None
	y = None
	Width = None
	Height = None
	LookupLabelForIde = False
	
	@staticmethod	
	def Bind(title, timeout = 15, maximize = False):
		try:
			Log.IsInError = False
			Window.TitleRegEx = title
			Window.Timeout = timeout
			if sys.platform == 'win32':
				toplist, winlist = [], []
				
				def enum_callback(hwnd, results):
					winlist.append((hwnd, win32gui.GetWindowText(hwnd)))
				
				t0 = time.time()
				Log.WriteMessage("debug", "wait for window \"" + title + "\"")
				
				cntLoop = 0
				while(True):
					
					tstep = time.time()
					allBoxesImg = None
					
					#print time.time() - t0
					print "wait for window \"" + title + "\", time elapsed: " + str(time.time() - t0)
					if(time.time() - t0 > timeout) and cntLoop > 0:
						# write debug message
						Log.WriteMessage("error", "window title \"" + title + "\" not found after timeout")	
						Log.IsInError = True
						return time.time() - t0
					
					win32gui.EnumWindows(enum_callback, toplist)

					window = [(hwnd, curTitle) for hwnd, curTitle in winlist if re.match(".*" + title + ".*", curTitle, re.DOTALL | re.IGNORECASE) != None and win32gui.IsWindowVisible(hwnd) != 0]
					
					# just grab the hwnd for first window matching title
					if len(window) > 0:
						Log.WriteMessage("debug", "bind window \"" + title + "\"")
						t1 = time.time()
						totale = t1 - t0
						tempoStepCorrente = t1 - tstep

						#print "total time:",totale
						#print "last step time:",tempoStepCorrente
						
						#windowTime = time.time() - t0
						window = window[0]
						Window.Hwnd = window[0]
						Window.Title = window[1]
						
						if (win32gui.IsIconic(Window.Hwnd) != 0):
							Window.Restore()
							
						#if foreground window title is not equal to window title
						if re.match(".*" + title + ".*", win32gui.GetWindowText(win32gui.GetForegroundWindow()), re.DOTALL | re.IGNORECASE) == None:
							Window.SetForeground()
						
						Window.Bbox = win32gui.GetWindowRect(Window.Hwnd)
						Window.x = Window.Bbox[0]
						Window.y = Window.Bbox[1]
						Window.Width = Window.Bbox[2] - Window.Bbox[0]
						Window.Height = Window.Bbox[3] - Window.Bbox[1]
						
						if Window.x == 0 and Window.y == 0 and Window.Height == 300 and Window.Width == 300:
							Window.SetForeground()
							
							toplist, winlist = [], []
							#time.sleep(5)
							win32gui.EnumWindows(enum_callback, toplist)
							window = [(hwnd, curTitle) for hwnd, curTitle in winlist if re.match(".*" + title + ".*", curTitle, re.DOTALL | re.IGNORECASE) != None]
							window = window[0]
							Window.Hwnd = window[0]
							Window.Title = window[1]
							
							Window.Bbox = win32gui.GetWindowRect(Window.Hwnd)	
							Window.x = Window.Bbox[0]
							Window.y = Window.Bbox[1]
							Window.Width = Window.Bbox[2] - Window.Bbox[0]
							Window.Height = Window.Bbox[3] - Window.Bbox[1]
						
						if maximize is True:
							win32gui.ShowWindow(Window.Hwnd, win32con.SW_MAXIMIZE)
						Log.WriteMessage("debug", "window full title is: \"" + Window.Title + "\"")
						print "window \"" + title + "\" found, the full title is: \"" + Window.Title + "\""
						print "window handle:",Window.Hwnd
						print "time elapsed:",totale - tempoStepCorrente
						print "window properties: x=" + str(Window.x) + ", y=" + str(Window.y) + ", width=" + str(Window.Width) + ", height=" + str(Window.Height)
						#return windowTime

						return (totale - tempoStepCorrente)
					cntLoop = cntLoop + 1
			else:
				import sdsfdsfsdfgfsdgsgfv
		except Exception, err:
			Log.IsInError = True
			Log.WriteMessage("ERROR", "an exception has occurred: " + str(err) + " on line " + str(sys.exc_traceback.tb_lineno))

			
	
	@staticmethod	
	def GetAllWindows(isVisible = True):
		try:
			Log.IsInError = False
			if sys.platform == 'win32':
				toplist, winlist = [], []
				
				def enum_callback(hwnd, results):
					winlist.append((hwnd, win32gui.GetWindowText(hwnd)))
				
				win32gui.EnumWindows(enum_callback, toplist)

				if isVisible is True:
					windows = [(hwnd, curTitle) for hwnd, curTitle in winlist if win32gui.IsWindowVisible(hwnd) != 0 and win32gui.GetWindowTextLength(hwnd) > 0]
				else:
					windows = [(hwnd, curTitle) for hwnd, curTitle in winlist if win32gui.GetWindowTextLength(hwnd) > 0]
					
				# just grab the hwnd for first window matching title
				for window in windows:
					print window
				
			else:
				import sdsfdsfsdfgfsdgsgfv
		except Exception, err:
			Log.IsInError = True
			Log.WriteMessage("ERROR", "an exception has occurred: " + str(err) + " on line " + str(sys.exc_traceback.tb_lineno))
	
	@staticmethod	
	def Unbind():
		Window.Title = None
		Window.TitleRegEx = None
		Window.Hwnd = None
		Window.Bbox = None
		Window.x = None
		Window.y = None
		Window.Width = None
		Window.Height = None
	
	@staticmethod	
	def SetForeground():
		try:
			Log.IsInError = True
			if sys.platform == 'win32':
				shell = win32com.client.Dispatch('WScript.Shell')
				shell.Run("AlexaSetForeground.exe " + str(Window.Hwnd),1,1)
				#time.sleep(1)
				#win32gui.SetForegroundWindow(Window.Hwnd)

			else:
				pass
		except Exception, err:
			Log.IsInError = True
			Log.WriteMessage("ERROR", "an exception has occurred: " + str(err) + " on line " + str(sys.exc_traceback.tb_lineno))

	@staticmethod	
	def Restore():
		try:
			Log.IsInError = False
			if sys.platform == 'win32':
				shell = win32com.client.Dispatch('WScript.Shell')
				shell.Run("AlexaRestoreWindow.exe " + str(Window.Hwnd),1,1)
			else:
				pass
		except Exception, err:
			Log.IsInError = True
			Log.WriteMessage("ERROR", "an exception has occurred: " + str(err) + " on line " + str(sys.exc_traceback.tb_lineno))

	
	@staticmethod	
	def Resize(x, y, w, h):
		try:
			Log.IsInError = False	
			if Window.Hwnd != None:
				if sys.platform == 'win32':
					win32gui.MoveWindow(Window.Hwnd, x, y, w, h, True)
					Window.Bbox = win32gui.GetWindowRect(Window.Hwnd)
		except Exception, err:
			Log.IsInError = True
			Log.WriteMessage("ERROR", "an exception has occurred: " + str(err) + " on line " + str(sys.exc_traceback.tb_lineno))

	@staticmethod	
	def Move(x, y):
		try:
			if Window.Hwnd != None:
				if sys.platform == 'win32':
					win32gui.MoveWindow(Window.Hwnd, x, y, Window.Width, Window.Height, True)
					Window.Bbox = win32gui.GetWindowRect(Window.Hwnd)
		except Exception, err:
			#print Exception
			#print err
			#print sys.exc_traceback.tb_lineno
			
			Log.WriteMessage("ERROR", "an exception has occurred: " + str(err) + " on line " + str(sys.exc_traceback.tb_lineno))	

	@staticmethod	
	def WaitForExit(title, timeout = 15):
		try:
			Log.IsInError = False
			if sys.platform == 'win32':
				toplist, winlist = [], []
				
				def enum_callback(hwnd, results):
					winlist.append((hwnd, win32gui.GetWindowText(hwnd)))
				
				t0 = time.time()
				
				while(True):
					
					tstep = time.time()
					
					#print time.time() - t0
					print "wait for exit of window \"" + title + "\", time elapsed: " + str(time.time() - t0)
					if(time.time() - t0 > timeout):
						# write debug message
						Log.WriteMessage("error", "window title \"" + title + "\" found after timeout.")
						Log.IsInError = True
						return time.time() - t0
					
					win32gui.EnumWindows(enum_callback, toplist)

					window = [(hwnd, curTitle) for hwnd, curTitle in winlist if re.match(".*" + title + ".*", curTitle, re.DOTALL | re.IGNORECASE) != None]
					
					# just grab the hwnd for first window matching title
					if len(window) > 0:
						Log.WriteMessage("debug", "window \"" + title + "\" found, wait for exit...")
						toplist, winlist = [], []
					else:
						returnTime = time.time() - t0
						Log.WriteMessage("debug", "window \"" + title + "\" has been closed.")
						return returnTime
			else:
				import sdsfdsfsdfgfsdgsgfv
		except Exception, err:
			Log.IsInError = True
			Log.WriteMessage("ERROR", "an exception has occurred: " + str(err) + " on line " + str(sys.exc_traceback.tb_lineno))
			
	@staticmethod	
	def Close(titleRegEx):
		try:
			Log.IsInError = False
			if sys.platform == 'win32':
				RunCmd(["AlexaCloseWindow.exe", titleRegEx], 8).Run()
		except Exception, err:
			Log.IsInError = True
			Log.WriteMessage("ERROR", "an exception has occurred: " + str(err) + " on line " + str(sys.exc_traceback.tb_lineno))

class Process:
	
	@staticmethod	
	def Kill(procName):
		try:
			Log.IsInError = False
			if sys.platform == 'win32':
				RunCmd(["AlexaKillProcesses.exe", procName], 8).Run()
		except Exception, err:
			Log.IsInError = True
			Log.WriteMessage("ERROR", "an exception has occurred: " + str(err) + " on line " + str(sys.exc_traceback.tb_lineno))

	@staticmethod	
	def WaitForExit(procname, timeout = 15):
		try:
			Log.IsInError = False
			if sys.platform == 'win32':
				
				
				t0 = time.time()
				
				while(True):
					
					tstep = time.time()
					
					#print time.time() - t0
					print "wait for exit of process \"" + procname + "\", time elapsed: " + str(time.time() - t0)
					if(time.time() - t0 > timeout):
						# write debug message
						Log.WriteMessage("error", "process \"" + procname + "\" found after timeout.")
						Log.IsInError = True
						return time.time() - t0
					
					WMI = comclt.GetObject('winmgmts:')
					processes = WMI.InstancesOf('Win32_Process')
					process_list = [(p.Properties_("ProcessID").Value, p.Properties_("Name").Value, p.Properties_("CommandLine").Value) for p in processes if p.Properties_("Name").Value == procname]
					
					# just grab the hwnd for first window matching title
					if len(process_list) > 0:
						Log.WriteMessage("debug", "window \"" + procname + "\" found, wait for exit...")
					else:
						returnTime = time.time() - t0
						Log.WriteMessage("debug", "process \"" + procname + "\" has been closed.")
						return returnTime
			else:
				import sdsfdsfsdfgfsdgsgfv
		except Exception, err:
			Log.IsInError = True
			Log.WriteMessage("ERROR", "an exception has occurred: " + str(err) + " on line " + str(sys.exc_traceback.tb_lineno))
	
	@staticmethod
	def AlexaAlreadyRunning():
		try:
		
			alexaRunningProcesses = 0
				
			if sys.platform == 'win32':
				procname = "python.exe"

				WMI = comclt.GetObject('winmgmts:')
				processes = WMI.InstancesOf('Win32_Process')
				process_list = [(p.Properties_("ProcessID").Value, p.Properties_("Name").Value, p.Properties_("CommandLine").Value) for p in processes
				if p.Properties_("Name").Value.lower() == procname]


				for proc in process_list:

					argument = proc[2]
					
					if "-u" in argument:
						filename = argument[argument.find("-u" ) + 2:]
					else:
						filename = argument[argument.find(".exe") + 4:]
					
					filename = filename.lstrip(' ')
					
					print "File Name:",filename
					
					input = open(filename,'r')
					
					for line in input.readlines():
					
						if "import" in line.lower() and "alexa" in line.lower():
							alexaRunningProcesses = alexaRunningProcesses + 1
							break
			if alexaRunningProcesses >= 2:
				return True
			else:
				return False
		except Exception, err:
			Log.IsInError = True
			Log.WriteMessage("ERROR", "an exception has occurred: " + str(err) + " on line " + str(sys.exc_traceback.tb_lineno))

class Screen:

	ImageFromIde = None
	
	# grab a screenshot
	@staticmethod	
	def GrabDesktop():
		try:
			import wx
		except ImportError:
			pass
		else:
		
			if Screen.ImageFromIde is not None:
				PilImage = Screen.ImageFromIde.copy()
				return PilImage
			
			app = wx.App(False)  #Need to create an App instance before doing anything
			screen = wx.ScreenDC()
			size = screen.GetSize()
			bmp = wx.EmptyBitmap(size[0], size[1])
			mem = wx.MemoryDC(bmp)
			mem.Blit(0, 0, size[0], size[1], screen, 0, 0)
			del mem  # Release bitmap
			#bmp.SaveFile('screenshot.png', wx.BITMAP_TYPE_PNG)
			myWxImage = wx.ImageFromBitmap( bmp )
			tmpPilImage = Image.new( 'RGB', (myWxImage.GetWidth(), myWxImage.GetHeight()) )
			tmpPilImage.fromstring( myWxImage.GetData() )
			
			#tmpPilImage = ImageGrab.grab()

			return tmpPilImage
			
	@staticmethod	
	def CropImage(x, y, width, height):
		try:
			import wx
		except ImportError:
			pass
		else:
			if Screen.ImageFromIde is not None:
				PilImage = Screen.ImageFromIde.copy()
				cropped = (left, top, left+width, top+height)
				tmpPilImage = PilImage.crop(cropped)
			else:
				app = wx.App(False)  #Need to create an App instance before doing anything
				screen = wx.ScreenDC()
				bmp = wx.EmptyBitmap(width, height)
				mem = wx.MemoryDC(bmp)
				#self.OriginX = self.CropRegion.x
				#self.OriginY = self.CropRegion.y
				mem.Blit(0, 0, width, height, screen, x, y)
				del mem  # Release bitmap
				#bmp.SaveFile('screenshot.png', wx.BITMAP_TYPE_PNG)
				myWxImage = wx.ImageFromBitmap( bmp )
				tmpPilImage = Image.new( 'RGB', (myWxImage.GetWidth(), myWxImage.GetHeight()) )
				tmpPilImage.fromstring( myWxImage.GetData() )
				
			#tmpPilImage = ImageGrab.grab()

			return tmpPilImage
				
class SearchRegion:
	x = None
	y = None
	Width = None
	Height = None
	
	@staticmethod	
	def Bind(x, y, width, height):
		try:
			Log.IsInError = False
			SearchRegion.x = x
			SearchRegion.y = y
			SearchRegion.Width = width
			SearchRegion.Height = height
		except Exception, err:
			Log.IsInError = True
			Log.WriteMessage("ERROR", "an exception has occurred: " + str(err) + " on line " + str(sys.exc_traceback.tb_lineno))

	@staticmethod	
	def Unbind():
		SearchRegion.x = None
		SearchRegion.y = None
		SearchRegion.Width = None
		SearchRegion.Height = None
	
class AppObject:

	Number = 0
	
	def __init__(self):
				
		#self.Log = Log("Log")
		self.Name = None
		
		# object coordinates
		self.x = None
		self.y = None
		
		self.xFromIde = None
		self.yFromIde = None
		
		# object size properties
		self.Width = 0
		self.Height = 0

		self.WidthTollerance = 0
		self.HeightTollerance = 0

		self.MinWidth = 0 
		self.MinHeight = 0

		self.MaxWidth = 0
		self.MaxHeight = 0

		# image filters
		self.ImageBinarize = False;
		
		self.ImageBrightness = 0.54
		self.ImageContrast = 1
		
		# object label properties
		self.Label = Label()
		self.Label.Language = "eng"
		
		self.AppObjectsForIde = []
		self.LookupLabelForIde = False
				
		self.TimeOut = False
		
		AppObject.Number = AppObject.Number + 1
		
	
	# find the object and save the coordinates
	def Bind(self,timeout = 15):
		
		print timeout
		self.x = None
		self.y = None
		
		Ocr.Language = self.Label.Language
		Log.WriteMessage("debug", "wait for object with label \"" + self.Label.Text + "\"")
		
		if self.Name == None:
			Log.ImagePathSubFolder = datetime.now().strftime("%H_%M_%S") + "_AppObject_Num_" + str(AppObject.Number)
		else:
			Log.ImagePathSubFolder = datetime.now().strftime("%H_%M_%S") + "_" + self.Name
			
		t0 = time.time()
		
		cntLoop = 0
		while(True):
			
			try:
				Log.IsInError = False
				allBoxesImg = None
		
				tstep = time.time()
			
				#print time.time() - t0
				try:
					print "wait for object with label \"" + self.Label.Text + "\", time elapsed: " + str(time.time() - t0)				
				except:
					pass
					
				#PilImage = self.GrabScreen()
				if SearchRegion.x != None and SearchRegion.y != None:
					
					if Window.TitleRegEx != None:
						Window.Bind(Window.TitleRegEx,Window.Timeout)
						Mouse.x0 = SearchRegion.x + Window.x
						Mouse.y0 = SearchRegion.y + Window.y
					else:
						Mouse.x0 = SearchRegion.x
						Mouse.y0 = SearchRegion.y
						
					PilImage = Screen.CropImage(Mouse.x0, Mouse.y0, SearchRegion.Width, SearchRegion.Height)
					
				elif Window.Hwnd != None:
					Window.Bind(Window.TitleRegEx,Window.Timeout)
					Mouse.x0 = Window.x
					Mouse.y0 = Window.y
					PilImage = Screen.CropImage(Window.x, Window.y, Window.Width, Window.Height)
				else:
					Mouse.x0 = 0
					Mouse.y0 = 0
					PilImage = Screen.GrabDesktop()
				
				if(time.time() - t0 > timeout) and cntLoop > 0:
					if self.Name == None:
						Log.WriteErrorImage(datetime.now().strftime("%H_%M_%S") + "_LookingFor_AppObject_Num_" + str(AppObject.Number) + ".png", PilImage)
					else:
						Log.WriteErrorImage(datetime.now().strftime("%H_%M_%S") + "_LookingFor_" + self.Name + ".png", PilImage)
					Log.IsInError = True
					self.TimeOut = True
					Log.LastTimedOutStep = self.Name
					duration = time.time() - t0
					NagiosUtils.TimedOutSteps.append((self.Name, duration, timeout))
					return duration
				
				if self.ImageBinarize is True:
					PilImage2 = PilImage.copy()
					enhancer = ImageEnhance.Brightness(PilImage2)
					PilImage2 = enhancer.enhance(self.ImageBrightness)
					
					enhancer = ImageEnhance.Contrast(PilImage2)
					PilImage2 = enhancer.enhance(self.ImageContrast)
					
					cv_im = cv.CreateImageHeader(PilImage2.size, cv.IPL_DEPTH_8U, 3)
					cv.SetData(cv_im, PilImage2.tostring())
				else:
					cv_im = cv.CreateImageHeader(PilImage.size, cv.IPL_DEPTH_8U, 3)
					cv.SetData(cv_im, PilImage.tostring())

				mat = cv.GetMat(cv_im)
				img = numpy.asarray(mat)
				
				img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR) 
							
				#save images if debug is on
				Log.WriteCv2Image(datetime.now().strftime("%H_%M_%S_%f") + "_screenshot.png", img)
				
				if self.ImageBinarize is True:
					gray_image = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
					thresh = 127
					im_bw = cv2.threshold(gray_image, thresh, 255, cv2.THRESH_BINARY)[1]
					
					#save images if debug is on
					Log.WriteCv2Image(datetime.now().strftime("%H_%M_%S_%f") + "bw.png", im_bw)
				
					# Find the contours
					contours,hierarchy = cv2.findContours(im_bw, cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
				else:
				
					# Split out each channel
					blue, green, red = cv2.split(img)

						
					# Run canny edge detection on each channel
					blue_edges = self.medianCanny(blue, 0.2, 0.3)
					green_edges = self.medianCanny(green, 0.2, 0.3)
					red_edges = self.medianCanny(red, 0.2, 0.3)

					# Join edges back into image
					edges = blue_edges | green_edges | red_edges
					#edges = cv2.cvtColor(edges, cv2.COLOR_RGB2BGR) 

					#save images if debug is on
					Log.WriteCv2Image(datetime.now().strftime("%H_%M_%S_%f") + "_borders.png", edges)

					# Find the contours
					contours,hierarchy = cv2.findContours(edges, cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)

				hierarchy = hierarchy[0] # get the actual inner list of hierarchy descriptions
				
				allBoxImgName = datetime.now().strftime("%H_%M_%S_%f") + "_all.png"
				matchImgName = datetime.now().strftime("%H_%M_%S_%f") + "_match.png"
				
				if (Log.Enable is True and Log.DebugImages is True):
					allBoxesImg = numpy.copy(img)
				
				#save debug images
				#Log.WriteCv2Image(datetime.now().strftime("%H_%M_%S_%f") + "_foo2.png", numpy.asarray(mat))
				
				if self.Width != 0 and self.Height != 0:
					self.MinWidth = self.MaxWidth  = self.Width
					self.MinHeight = self.MaxHeight = self.Height
					#print self.MinWidth,self.MaxWidth,self.MinHeight,self.MaxHeight
					
				if self.WidthTollerance != 0 and self.Width != 0 and self.Height != 0:
					self.MinWidth = self.MinWidth -  self.WidthTollerance
					self.MaxWidth = self.MaxWidth + self.WidthTollerance

					
				if self.HeightTollerance != 0 and self.Width != 0 and self.Height != 0:
					self.MinHeight = self.MinHeight - self.HeightTollerance
					self.MaxHeight = self.MaxHeight + self.HeightTollerance

				cnt = 0
				# For each contour, find the bounding rectangle and draw it
				for component in reversed(zip(contours, hierarchy)):
					currentContour = component[0].astype('int') #ho messo astype('int') per evitare il bug
					currentHierarchy = component[1].astype('int') #ho messo astype('int') per evitare il bug
					x,y,w,h = cv2.boundingRect(currentContour)
					
					if (Log.Enable is True and Log.DebugImages is True):
						cv2.rectangle(allBoxesImg,(x,y),(x+w,y+h),(0,0,255),3)
					
					#print "x", self.xFromIde - 50, self.xFromIde + 50
					#print "y", self.yFromIde - 50, self.yFromIde + 50
					#for ide
					#print "screen", Screen.ImageFromIde
					if self.LookupLabelForIde is True:
						#diagonale = math.sqrt((w**2)+(h**2))
						#ratioFound = float(w/h)
						#ratioOri = float(self.Width/self.Height)

						#print ratioFound, ratioOri
						if (x >= self.xFromIde - 20 and x <= self.xFromIde + 20 and y >= self.yFromIde - 20 and y <= self.yFromIde + 20) and \
						(w >= self.Width - 20 and w <= self.Width + 20 and h >= self.Height - 20 and h <= self.Height + 20):
						
							self.AppObjectsForIde.append((x, y, w, h))
							
							'''
							for appObj in self.AppObjectsForIde
								self.x = x
								self.y = y
								self.Width = w
								self.Height = h
								return
							'''
					elif(w >= self.MinWidth and w <= self.MaxWidth and h >= self.MinHeight and h <= self.MaxHeight):
							
						cv2.rectangle(img,(x,y),(x+w,y+h),(0,0,255),3)
						
						#crop
						ocrt1 = time.time()
						
						textFound = False
						customLabel = False
						
						#top = (Bitmap)ResizeImage(top, new Size(top.Width * 3, top.Height * 3));
						if (self.Label.Width != 0 or self.Label.Height != 0 or self.Label.OffsetX != 0 or self.Label.OffsetY != 0) and textFound is False:
							customLabel = True
							left = x + self.Label.OffsetX
							top = y + self.Label.OffsetY
							width = self.Label.Width
							height = self.Label.Height
							
							if height < 8 or width < 8:
								continue
								
							cropped = (left, top, left+width, top+height)
							area = PilImage.crop(cropped)
							area = area.resize((width * 3, height * 3), Image.BICUBIC) 
							#save images if debug is on
							Log.WritePilImage(datetime.now().strftime("%H_%M_%S_%f") + '_CustomLabel.png', area)
							
							if self.Label.Binarize is True:
								textFound = Ocr.CompareLabelText(self.Label.Text, area, True, self.Label.Brightness, self.Label.Contrast)
							else:
								textFound = Ocr.CompareLabelText(self.Label.Text, area)
							
						if (self.Label.Position == "top" or self.Label.Position == "") and textFound is False and customLabel is False:
						
							left = x - 10
							top = y - (h + (h/2))
							width = w + 20
							height = (h + (h/2))
							
							if height < 8:
								continue
						
							cropped = (left, top, left+width, top+height)
							area = PilImage.crop(cropped)
							area = area.resize((width * 3, height * 3), Image.BICUBIC)							
							#save images if debug is on
							Log.WritePilImage(datetime.now().strftime("%H_%M_%S_%f") + '_TopLabel.png', area)
			
							if self.Label.Binarize is True:
								textFound = Ocr.CompareLabelText(self.Label.Text, area, True, self.Label.Brightness, self.Label.Contrast)
							else:
								textFound = Ocr.CompareLabelText(self.Label.Text, area)
							
						if (self.Label.Position == "left" or self.Label.Position == "") and textFound is False and customLabel is False:
						
							left = x - (w * 2)
							top = y
							width = w*2
							height = h
							
							if height < 8 or width < 8:
								continue
							
							cropped = (left, top, left+width, top+height)
							area = PilImage.crop(cropped)
							area = area.resize((width * 3, height * 3), Image.BICUBIC) 
							#save images if debug is on
							Log.WritePilImage(datetime.now().strftime("%H_%M_%S_%f") + '_LeftLabel.png', area)
							
							if self.Label.Binarize is True:
								textFound = Ocr.CompareLabelText(self.Label.Text, area, True, self.Label.Brightness, self.Label.Contrast)
							else:
								textFound = Ocr.CompareLabelText(self.Label.Text, area)
							
						if (self.Label.Position == "inside" or self.Label.Position == "") and textFound is False and customLabel is False:

							left = x + 2
							top = y + 2
							width = w - 4
							height = h - 4
							
							print width, height
							if w - 2 < 8 or h - 2 < 8:
								continue
							
							cropped = (left, top, left+width, top+height)
							area = PilImage.crop(cropped)
							area = area.resize((width * 3, height * 3), Image.BICUBIC) 
							#save images if debug is on
							Log.WritePilImage(datetime.now().strftime("%H_%M_%S_%f") + '_InsideLabel.png', area)
							
							if self.Label.Binarize is True:
								textFound = Ocr.CompareLabelText(self.Label.Text, area, True, self.Label.Brightness, self.Label.Contrast)
							else:
								textFound = Ocr.CompareLabelText(self.Label.Text, area)
							
						if (self.Label.Position == "right" or self.Label.Position == "") and textFound is False and customLabel is False:

							left = x + w
							top = y
							width = w*2
							height = h
							
							if height < 8 or width < 8:
								continue
							
							cropped = (left, top, left+width, top+height)
							area = PilImage.crop(cropped)
							area = area.resize((width * 3, height * 3), Image.BICUBIC) 
							#save images if debug is on
							Log.WritePilImage(datetime.now().strftime("%H_%M_%S_%f") + '_RightLabel.png', area)
							
							if self.Label.Binarize is True:
								textFound = Ocr.CompareLabelText(self.Label.Text, area, True, self.Label.Brightness, self.Label.Contrast)
							else:
								textFound = Ocr.CompareLabelText(self.Label.Text, area)
							
						if textFound is True:
							
							t1 = time.time()
							totale = t1 - t0
							tempoStepCorrente = t1 - tstep
							
							self.TimeOut = False
							
							self.x = x
							self.y = y
							
							self.Width = w
							self.Height = h
							
							Log.WriteCv2Image(matchImgName,img)
							Log.WriteCv2Image(allBoxImgName,allBoxesImg)
							# write debug message
							Log.WriteMessage("debug", "object with label \"" + self.Label.Text + "\" found")
							Log.WriteMessage("debug", "object properties: x=" + str(self.x) + ", y=" + str(self.y) + ", width=" + str(w) + ", height=" + str(h))	

							#print "tempo totale:",totale
							#print "tempo ultimo step:",tempoStepCorrente
							print "object with label \"" + self.Label.Text + "\" found"
							print "time elapsed:",totale - tempoStepCorrente
							print "object properties: x=" + str(self.x) + ", y=" + str(self.y) + ", width=" + str(w) + ", height=" + str(h)
							return (totale - tempoStepCorrente)

					cnt = cnt + 1
					
				if self.LookupLabelForIde is True:
					if len(self.AppObjectsForIde) > 0:
						retX = retY = retW = retH = 0
						print self.AppObjectsForIde
						for appObj in self.AppObjectsForIde:
							if appObj[2] > retW and appObj[3] > retH and appObj[2] >= 8 and appObj[3] >= 8:
								retX = appObj[0]
								retY = appObj[1]
								retW = appObj[2]
								retH = appObj[3]
						
						self.AppObjectsForIde = []
						
						#print retX, retY, retW, retH
						if retX ==0 or retY == 0 or retW == 0 or retH == 0:
							self.x = None
							self.y = None
						else:
							self.x = retX
							self.y = retY
							self.Width = retW
							self.Height = retH
					else:
						self.x = None
						self.y = None
					return
				#save images if debug is on
				#Log.WriteCv2Image(datetime.now().strftime("%H_%M_%S_%f") + "_foo2.png", numpy.asarray(mat))
				Log.WriteCv2Image(matchImgName,img)
				Log.WriteCv2Image(allBoxImgName,allBoxesImg)
				
				#print "tempo impiegato",time.time() - tstep,"secondi"
				
			except Exception, err:
				#print Exception
				#print err
				#print sys.exc_traceback.tb_lineno
				Log.IsInError = True
				Log.WriteMessage("ERROR", "an exception has occurred: " + str(err) + " on line " + str(sys.exc_traceback.tb_lineno))	
				
				if(time.time() - t0 > timeout):
					Log.IsInError = True
					self.TimeOut = True
					Log.LastTimedOutStep = self.Name
					duration = time.time() - t0
					NagiosUtils.TimedOutSteps.append((self.Name, duration, timeout))
					return duration
				
			cntLoop = cntLoop + 1
		
	def medianCanny(self,img, thresh1, thresh2):
		median = numpy.median(img)
		img = cv2.Canny(img, int(thresh1 * median), int(thresh2 * median))
		return img	


class AppImage:
	
	Number = 0

	def __init__(self):
		
		self.Name = None
				
		# object coordinates
		self.x = None
		self.y = None
		
		self.Path = None
		self.Threshold = 0.003
		
		self.Width = None
		self.Height = None
		
		self.TimeOut = False	
		
		AppImage.Number = AppImage.Number + 1
	
	# find the object and save the coordinates
	def Bind(self,timeout = 15):
		
		print timeout
		self.x = None
		self.y = None
		
		Log.WriteMessage("debug", "wait for image \"" + self.Path + "\"")
		
		if self.Name == None:
			Log.ImagePathSubFolder = datetime.now().strftime("%H_%M_%S") + "_AppImage_Num_" + str(AppImage.Number)
		else:
			Log.ImagePathSubFolder = datetime.now().strftime("%H_%M_%S") + "_" + self.Name

		'''
		if os.path.isabs(self.Path) is False:
			self.Path = os.path.join(os.path.realpath(__file__),"images")
			print self.Path
		'''
		
		t0 = time.time()
		
		cntLoop = 0
		while(True):
			try:
				Log.IsInError = False
				tstep = time.time()
		
				#print time.time() - t0
				print "wait for image, time elapsed: " + str(time.time() - t0)
					
				#PilImage = self.GrabScreen()
				if SearchRegion.x != None and SearchRegion.y != None:
					
					if Window.TitleRegEx != None:
						Window.Bind(Window.TitleRegEx,Window.Timeout)
						Mouse.x0 = SearchRegion.x + Window.x
						Mouse.y0 = SearchRegion.y + Window.y
					else:
						Mouse.x0 = SearchRegion.x
						Mouse.y0 = SearchRegion.y
						
					PilImage = Screen.CropImage(Mouse.x0, Mouse.y0, SearchRegion.Width, SearchRegion.Height)
					
				elif Window.Hwnd != None:
					Window.Bind(Window.TitleRegEx,Window.Timeout)
					Mouse.x0 = Window.x
					Mouse.y0 = Window.y
					PilImage = Screen.CropImage(Window.x, Window.y, Window.Width, Window.Height)
				else:
					Mouse.x0 = 0
					Mouse.y0 = 0
					PilImage = Screen.GrabDesktop()
				
				if(time.time() - t0 > timeout) and cntLoop > 0:
					if self.Name == None:
						Log.WriteErrorImage(datetime.now().strftime("%H_%M_%S") + "_LookingFor_AppImage_Num_" + str(AppImage.Number) + ".png", PilImage)
					else:
						Log.WriteErrorImage(datetime.now().strftime("%H_%M_%S") + "_LookingFor_" + self.Name + ".png", PilImage)
					Log.IsInError = True
					self.TimeOut = True
					Log.LastTimedOutStep = self.Name					
					duration = time.time() - t0
					NagiosUtils.TimedOutSteps.append((self.Name, duration, timeout))
					return duration
					
				cv_im = cv.CreateImageHeader(PilImage.size, cv.IPL_DEPTH_8U, 3)
				cv.SetData(cv_im, PilImage.tostring())

				mat = cv.GetMat(cv_im)
				img = numpy.asarray(mat)
				
				img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR) 
							
				#save images if debug is on
				Log.WriteCv2Image(datetime.now().strftime("%H_%M_%S_%f") + "_screenshot.png", img)
				
				matchImgName = datetime.now().strftime("%H_%M_%S_%f") + "_match.png"
							
				imgToCompare = cv2.imread(self.Path)

				result = cv2.matchTemplate(img,imgToCompare,cv2.TM_SQDIFF_NORMED)

				min_val, max_val, min_loc,max_loc = cv2.minMaxLoc(result)

				print min_val
				
				if min_val < self.Threshold:
				
					t1 = time.time()
					totale = t1 - t0
					tempoStepCorrente = t1 - tstep
					
					self.TimeOut = False
					
					self.Height = imgToCompare.shape[0]
					self.Width = imgToCompare.shape[1]
					
					self.x = min_loc[0]
					self.y = min_loc[1]
						
					'''
					if SearchRegion.x != None and SearchRegion.y != None:
						self.x = min_loc[0] + SearchRegion.x
						self.y = min_loc[1] + SearchRegion.y
					elif Window.Hwnd != None:
						self.x = min_loc[0] + Window.x
						self.y = min_loc[1] + Window.x
					else:
						self.x = min_loc[0]
						self.y = min_loc[1]
					'''
					
					cv2.rectangle(img,min_loc,(min_loc[0] + self.Width, min_loc[1] + self.Height),(0,0,255),3)
					Log.WriteCv2Image(matchImgName,img)
					# write debug message
					Log.WriteMessage("debug", "image found, image properties: x=" + str(self.x) + ", y=" + str(self.y) + ", width=" + str(self.Width) + ", height=" + str(self.Height))
					#Log.WriteMessage("debug", "object coordinates x: " + str(self.x) + ", y: " + str(self.y) + ", object height: " + str(h) + ", width: " + str(w))	

					#print "tempo totale:",totale
					#print "tempo ultimo step:",tempoStepCorrente
					print "image found"
					print "time elapsed:",totale - tempoStepCorrente
					print "image properties: x=" + str(self.x) + ", y=" + str(self.y) + ", width=" + str(self.Width) + ", height=" + str(self.Height)
					return (totale - tempoStepCorrente)
				
				#print "tempo impiegato",time.time() - tstep,"secondi"
			except Exception, err:
				#print Exception
				#print err
				#print sys.exc_traceback.tb_lineno
				Log.IsInError = True
				Log.WriteMessage("ERROR", "an exception has occurred: " + str(err) + " on line " + str(sys.exc_traceback.tb_lineno))
				
				if(time.time() - t0 > timeout):
					Log.IsInError = True
					self.TimeOut = True		
					Log.LastTimedOutStep = self.Name					
					duration = time.time() - t0
					NagiosUtils.TimedOutSteps.append((self.Name, duration, timeout))
					return duration
			cntLoop = cntLoop + 1

class AppText:

	Number = 0
	
	def __init__(self):
	
		#self.Log = Log("Log")
		self.Name = None
		
		# object coordinates
		self.x = None
		self.y = None
		
		self.xFromIde = None
		self.yFromIde = None
		
		self.ObjX = None
		self.ObjY = None
		self.ObjW = None
		self.ObjH = None
		
		# object size properties
		self.Width = 0
		self.Height = 0

		self.WidthTollerance = 0
		self.HeightTollerance = 0

		self.MinWidth = 0 
		self.MinHeight = 0

		self.MaxWidth = 0
		self.MaxHeight = 0

		# image filters
		self.ImageBinarize = False;
		
		self.ImageBrightness = 0.54
		self.ImageContrast = 1
		
		self.Binarize = False
		self.Brightness = 0.54
		self.Contrast = 1
		
		self.Language = "eng"
		
		#self.TextFound = ""
		
		self.Text = ""
		
		self.AppTextObjectsForIde = []
		self.LookupLabelForIde = False
		
		self.TimeOut = False	
							
		AppText.Number = AppText.Number + 1
	
	# find the object and save the coordinates
	def Bind(self,timeout = 15):
		
		self.x = None
		self.y = None
		self.ObjX = None
		self.ObjY = None

		self.TextFound = ""
		
		Ocr.Language = self.Language
		Log.WriteMessage("debug", "wait for text \"" + self.Text + "\"")
		
		if self.Name == None:
			Log.ImagePathSubFolder = datetime.now().strftime("%H_%M_%S") + "_AppText_Num_" + str(AppText.Number)
		else:
			Log.ImagePathSubFolder = datetime.now().strftime("%H_%M_%S") + "_" + self.Name
			
		t0 = time.time()
		
		cntLoop = 0		
		while(True):
			try:
				Log.IsInError = False
				allBoxesImg = None
				
				tstep = time.time()
				
				try:
					print "wait for text \"" + self.Text + "\", time elapsed: " + str(time.time() - t0)
				except:
					pass
					
				#PilImage = self.GrabScreen()
				if SearchRegion.x != None and SearchRegion.y != None:
					
					if Window.TitleRegEx != None:
						Window.Bind(Window.TitleRegEx,Window.Timeout)
						Mouse.x0 = SearchRegion.x + Window.x
						Mouse.y0 = SearchRegion.y + Window.y
					else:
						Mouse.x0 = SearchRegion.x
						Mouse.y0 = SearchRegion.y
						
					PilImage = Screen.CropImage(Mouse.x0, Mouse.y0, SearchRegion.Width, SearchRegion.Height)
					
				elif Window.Hwnd != None:
					Window.Bind(Window.TitleRegEx,Window.Timeout)
					Mouse.x0 = Window.x
					Mouse.y0 = Window.y
					PilImage = Screen.CropImage(Window.x, Window.y, Window.Width, Window.Height)
				else:
					Mouse.x0 = 0
					Mouse.y0 = 0
					PilImage = Screen.GrabDesktop()
				
				if(time.time() - t0 > timeout) and cntLoop > 0:
					if self.Name == None:
						Log.WriteErrorImage(datetime.now().strftime("%H_%M_%S") + "_LookingFor_AppText_Num_" + str(AppText.Number) + ".png", PilImage)
					else:
						Log.WriteErrorImage(datetime.now().strftime("%H_%M_%S") + "_LookingFor_" + self.Name + ".png", PilImage)
					Log.LastTimedOutStep = self.Name
					Log.IsInError = True	
					self.TimeOut = True			
					Log.LastTimedOutStep = self.Name					
					duration = time.time() - t0
					NagiosUtils.TimedOutSteps.append((self.Name, duration, timeout))
					return duration
					
				if self.ImageBinarize is True:
					PilImage2 = PilImage.copy()
					enhancer = ImageEnhance.Brightness(PilImage2)
					PilImage2 = enhancer.enhance(self.ImageBrightness)
					
					enhancer = ImageEnhance.Contrast(PilImage2)
					PilImage2 = enhancer.enhance(self.ImageContrast)
					
					cv_im = cv.CreateImageHeader(PilImage2.size, cv.IPL_DEPTH_8U, 3)
					cv.SetData(cv_im, PilImage2.tostring())
				else:
					cv_im = cv.CreateImageHeader(PilImage.size, cv.IPL_DEPTH_8U, 3)
					cv.SetData(cv_im, PilImage.tostring())

				mat = cv.GetMat(cv_im)
				img = numpy.asarray(mat)
				
				img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR) 
							
				#save images if debug is on
				Log.WriteCv2Image(datetime.now().strftime("%H_%M_%S_%f") + "_screenshot.png", img)
				
				if self.ImageBinarize is True:
					gray_image = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
					thresh = 127
					im_bw = cv2.threshold(gray_image, thresh, 255, cv2.THRESH_BINARY)[1]
					
					#save images if debug is on
					Log.WriteCv2Image(datetime.now().strftime("%H_%M_%S_%f") + "bw.png", im_bw)
				
					# Find the contours
					contours,hierarchy = cv2.findContours(im_bw, cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
				else:
				
					# Split out each channel
					blue, green, red = cv2.split(img)

						
					# Run canny edge detection on each channel
					blue_edges = self.medianCanny(blue, 0.2, 0.3)
					green_edges = self.medianCanny(green, 0.2, 0.3)
					red_edges = self.medianCanny(red, 0.2, 0.3)

					# Join edges back into image
					edges = blue_edges | green_edges | red_edges
					#edges = cv2.cvtColor(edges, cv2.COLOR_RGB2BGR) 

					#save images if debug is on
					Log.WriteCv2Image(datetime.now().strftime("%H_%M_%S_%f") + "_borders.png", edges)

					# Find the contours
					contours,hierarchy = cv2.findContours(edges, cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)

				hierarchy = hierarchy[0] # get the actual inner list of hierarchy descriptions
				
				allBoxImgName = datetime.now().strftime("%H_%M_%S_%f") + "_all.png"
				matchImgName = datetime.now().strftime("%H_%M_%S_%f") + "_match.png"
				
				if (Log.Enable is True and Log.DebugImages is True):
					allBoxesImg = numpy.copy(img)
				
				#save debug images
				#Log.WriteCv2Image(datetime.now().strftime("%H_%M_%S_%f") + "_foo2.png", numpy.asarray(mat))

				if self.Width == 0 and self.Height == 0 and self.MinWidth == 0  and self.MinHeight == 0 and self.MaxWidth == 0 and self.MaxHeight == 0:
				
					area = PilImage
					width, height = area.size
					area = area.resize((width * 3, height * 3), Image.BICUBIC) 
					#save images if debug is on
					Log.WritePilImage(datetime.now().strftime("%H_%M_%S_%f") + '_text.png', area)
					
					'''
					if self.Text == "":
						if self.Binarize is True:
							self.TextFound = Ocr.GetText(area, True, self.Brightness, self.Contrast)
						else:
							self.TextFound = Ocr.GetText(area)

						return 0.0
					'''					
					
					textFound = None
					if self.Binarize is True:
						textFound = Ocr.GetTextCoordinates(self.Text, area, True, self.Brightness, self.Contrast)
					else:
						textFound = Ocr.GetTextCoordinates(self.Text, area)
									
					if textFound != None:
						t1 = time.time()
						totale = t1 - t0
						tempoStepCorrente = t1 - tstep
						
						self.TimeOut = False
						
						self.x = int(textFound[0])/3
						self.y = int(textFound[1])/3
						
						self.Width = (int(textFound[2]) - int(textFound[0]))/3
						self.Height = (int(textFound[3]) - int(textFound[1]))/3
						
						# write debug message
						Log.WriteMessage("debug", "text found, text properties: x=" + str(self.x) + ", y=" + str(self.y) + ", width=" + str(self.Width) + ", height=" + str(self.Height))	

						print "tempo totale:",totale
						print "tempo ultimo step:",tempoStepCorrente
						print "text \"" + self.Text + "\" found"
						print "time elapsed:",totale - tempoStepCorrente
						print "text properties: x=" + str(self.x) + ", y=" + str(self.y) + ", width=" + str(self.Width) + ", height=" + str(self.Height)
						return (totale - tempoStepCorrente)
				else:
				
					if self.Width != 0 and self.Height != 0:
						self.MinWidth = self.MaxWidth  = self.Width
						self.MinHeight = self.MaxHeight = self.Height
						#print self.MinWidth,self.MaxWidth,self.MinHeight,self.MaxHeight
						
					if self.WidthTollerance != 0 and self.Width != 0 and self.Height != 0:
						self.MinWidth = self.MinWidth -  self.WidthTollerance
						self.MaxWidth = self.MaxWidth + self.WidthTollerance

						
					if self.HeightTollerance != 0 and self.Width != 0 and self.Height != 0:
						self.MinHeight = self.MinHeight - self.HeightTollerance
						self.MaxHeight = self.MaxHeight + self.HeightTollerance
					
					#print self.MinHeight	
					#print self.MaxHeight	
					#print self.MinWidth
					#print self.MaxWidth
					
					if self.MinHeight < 0:
						self.MinHeight = 0
					
					cnt = 0
					textFound = None
					# For each contour, find the bounding rectangle and draw it
					for component in reversed(zip(contours, hierarchy)):
						currentContour = component[0].astype('int') #ho messo astype('int') per evitare il bug
						currentHierarchy = component[1].astype('int') #ho messo astype('int') per evitare il bug
						x,y,w,h = cv2.boundingRect(currentContour)
									
						if (Log.Enable is True and Log.DebugImages is True):
							cv2.rectangle(allBoxesImg,(x,y),(x+w,y+h),(0,0,255),3)
						if self.LookupLabelForIde is True:
							#diagonale = math.sqrt((w**2)+(h**2))
							#ratioFound = float(w/h)
							#ratioOri = float(self.Width/self.Height)

							#print ratioFound, ratioOri
							if (x >= self.xFromIde - 20 and x <= self.xFromIde + 20 and y >= self.yFromIde - 20 and y <= self.yFromIde + 20) and \
							(w >= self.Width - 20 and w <= self.Width + 20 and h >= self.Height - 20 and h <= self.Height + 20):
							
								self.AppTextObjectsForIde.append((x, y, w, h))

						elif(w >= self.MinWidth and w <= self.MaxWidth and h >= self.MinHeight and h <= self.MaxHeight and textFound is None):
									
							cv2.rectangle(img,(x,y),(x+w,y+h),(0,0,255),3)
							
							#crop
							ocrt1 = time.time()
							
							textFound = False

							left = x
							top = y
							width = w
							height = h
							
							if h < 8 or w < 8:
								continue
							
							cropped = (left, top, left+width, top+height)
							area = PilImage.crop(cropped)
							area = area.resize((width * 3, height * 3), Image.BICUBIC) 
							#save images if debug is on
							Log.WritePilImage(datetime.now().strftime("%H_%M_%S_%f") + '_text.png', area)
							
							'''
							if self.Text == "":
								if self.Binarize is True:
									self.TextFound = Ocr.GetText(area, True, self.Brightness, self.Contrast)
								else:
									self.TextFound = Ocr.GetText(area)
							
								return 0.0
							'''
							
							if self.Binarize is True:
								textFound = Ocr.GetTextCoordinates(self.Text, area, True, self.Brightness, self.Contrast)
							else:
								textFound = Ocr.GetTextCoordinates(self.Text, area)
								
							if textFound != None:
								
								t1 = time.time()
								totale = t1 - t0
								tempoStepCorrente = t1 - tstep
								self.TimeOut = False	
								self.ObjX = x
								self.ObjY = y
								self.ObjW = w
								self.ObjH = h

								self.x = int(textFound[0])/3 + x
								self.y = int(textFound[1])/3 + y
								
								self.Width = (int(textFound[2]) - int(textFound[0]))/3
								self.Height = (int(textFound[3]) - int(textFound[1]))/3
								
								Log.WriteCv2Image(matchImgName,img)
								Log.WriteCv2Image(allBoxImgName,allBoxesImg)
								# write debug message
								Log.WriteMessage("debug", "text found, text properties: x=" + str(self.x) + ", y=" + str(self.y) + ", width=" + str(self.Width) + ", height=" + str(self.Height))

								#print "tempo totale:",totale
								#print "tempo ultimo step:",tempoStepCorrente
								print "text \"" + self.Text + "\" found"
								print "time elapsed:",totale - tempoStepCorrente
								print "text properties: x=" + str(self.x) + ", y=" + str(self.y) + ", width=" + str(self.Width) + ", height=" + str(self.Height)
								return (totale - tempoStepCorrente)

						cnt = cnt + 1
						
					if self.LookupLabelForIde is True:
						if len(self.AppTextObjectsForIde) > 0:
							retX = retY = retW = retH = 0
							print self.AppTextObjectsForIde
							for appText in self.AppTextObjectsForIde:
								if appText[2] > retW and appText[3] > retH and appText[2] >= 8 and appText[3] >= 8:
									retX = appText[0]
									retY = appText[1]
									retW = appText[2]
									retH = appText[3]
							
							self.AppTextObjectsForIde = []
							self.x = retX
							self.y = retY
							self.Width = retW
							self.Height = retH
							self.ObjW = retW
							self.ObjH = retH
						else:
							self.x = None
							self.y = None
						return
					#save images if debug is on
					#Log.WriteCv2Image(datetime.now().strftime("%H_%M_%S_%f") + "_foo2.png", numpy.asarray(mat))
					Log.WriteCv2Image(matchImgName,img)
					Log.WriteCv2Image(allBoxImgName,allBoxesImg)
				
				#print "tempo impiegato",time.time() - tstep,"secondi"
			except Exception, err:
				#print Exception
				#print err
				#print sys.exc_traceback.tb_lineno
				Log.IsInError = True
				Log.WriteMessage("ERROR", "an exception has occurred: " + str(err) + " on line " + str(sys.exc_traceback.tb_lineno))
				
				if(time.time() - t0 > timeout):
					Log.IsInError = True	
					self.TimeOut = True	
					Log.LastTimedOutStep = self.Name					
					duration = time.time() - t0
					NagiosUtils.TimedOutSteps.append((self.Name, duration, timeout))
					return duration
			cntLoop = cntLoop + 1

	# find the object and save the coordinates
	def ReadText(self):
		
		Ocr.Language = self.Language
		
		if self.Name == None:
			Log.ImagePathSubFolder = datetime.now().strftime("%H_%M_%S") + "_AppText_Num_" + str(AppText.Number)
		else:
			Log.ImagePathSubFolder = datetime.now().strftime("%H_%M_%S") + "_" + self.Name
			
				
		try:
			Log.IsInError = False
			allBoxesImg = None
				
			#PilImage = self.GrabScreen()
			if SearchRegion.x != None and SearchRegion.y != None:
				
				if Window.TitleRegEx != None:
					Window.Bind(Window.TitleRegEx,Window.Timeout)
					Mouse.x0 = SearchRegion.x + Window.x
					Mouse.y0 = SearchRegion.y + Window.y
				else:
					Mouse.x0 = SearchRegion.x
					Mouse.y0 = SearchRegion.y
					
				PilImage = Screen.CropImage(Mouse.x0, Mouse.y0, SearchRegion.Width, SearchRegion.Height)
				
			elif Window.Hwnd != None:
				Window.Bind(Window.TitleRegEx,Window.Timeout)
				Mouse.x0 = Window.x
				Mouse.y0 = Window.y
				PilImage = Screen.CropImage(Window.x, Window.y, Window.Width, Window.Height)
			else:
				Mouse.x0 = 0
				Mouse.y0 = 0
				PilImage = Screen.GrabDesktop()
			
				
			if self.ImageBinarize is True:
				PilImage2 = PilImage.copy()
				enhancer = ImageEnhance.Brightness(PilImage2)
				PilImage2 = enhancer.enhance(self.ImageBrightness)
				
				enhancer = ImageEnhance.Contrast(PilImage2)
				PilImage2 = enhancer.enhance(self.ImageContrast)
				
				cv_im = cv.CreateImageHeader(PilImage2.size, cv.IPL_DEPTH_8U, 3)
				cv.SetData(cv_im, PilImage2.tostring())
			else:
				cv_im = cv.CreateImageHeader(PilImage.size, cv.IPL_DEPTH_8U, 3)
				cv.SetData(cv_im, PilImage.tostring())

			mat = cv.GetMat(cv_im)
			img = numpy.asarray(mat)
			
			img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR) 
						
			#save images if debug is on
			Log.WriteCv2Image(datetime.now().strftime("%H_%M_%S_%f") + "_screenshot.png", img)
			
			if self.ImageBinarize is True:
				gray_image = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
				thresh = 127
				im_bw = cv2.threshold(gray_image, thresh, 255, cv2.THRESH_BINARY)[1]
				
				#save images if debug is on
				Log.WriteCv2Image(datetime.now().strftime("%H_%M_%S_%f") + "bw.png", im_bw)
			
				# Find the contours
				contours,hierarchy = cv2.findContours(im_bw, cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
			else:
			
				# Split out each channel
				blue, green, red = cv2.split(img)

					
				# Run canny edge detection on each channel
				blue_edges = self.medianCanny(blue, 0.2, 0.3)
				green_edges = self.medianCanny(green, 0.2, 0.3)
				red_edges = self.medianCanny(red, 0.2, 0.3)

				# Join edges back into image
				edges = blue_edges | green_edges | red_edges
				#edges = cv2.cvtColor(edges, cv2.COLOR_RGB2BGR) 

				#save images if debug is on
				Log.WriteCv2Image(datetime.now().strftime("%H_%M_%S_%f") + "_borders.png", edges)

				# Find the contours
				contours,hierarchy = cv2.findContours(edges, cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)

			hierarchy = hierarchy[0] # get the actual inner list of hierarchy descriptions
			
			allBoxImgName = datetime.now().strftime("%H_%M_%S_%f") + "_all.png"
			matchImgName = datetime.now().strftime("%H_%M_%S_%f") + "_match.png"
			
			if (Log.Enable is True and Log.DebugImages is True):
				allBoxesImg = numpy.copy(img)
			
			#save debug images
			#Log.WriteCv2Image(datetime.now().strftime("%H_%M_%S_%f") + "_foo2.png", numpy.asarray(mat))

			if self.Width == 0 and self.Height == 0 and self.MinWidth == 0  and self.MinHeight == 0 and self.MaxWidth == 0 and self.MaxHeight == 0:
			
				area = PilImage
				width, height = area.size
				area = area.resize((width * 3, height * 3), Image.BICUBIC) 
				#save images if debug is on
				Log.WritePilImage(datetime.now().strftime("%H_%M_%S_%f") + '_text.png', area)
				
				if self.Binarize is True:
					TextFound = Ocr.GetText(area, True, self.Brightness, self.Contrast)
				else:
					TextFound = Ocr.GetText(area)
					
				return TextFound

			else:
			
				if self.Width != 0 and self.Height != 0:
					self.MinWidth = self.MaxWidth  = self.Width
					self.MinHeight = self.MaxHeight = self.Height
					#print self.MinWidth,self.MaxWidth,self.MinHeight,self.MaxHeight
					
				if self.WidthTollerance != 0 and self.Width != 0 and self.Height != 0:
					self.MinWidth = self.MinWidth -  self.WidthTollerance
					self.MaxWidth = self.MaxWidth + self.WidthTollerance

					
				if self.HeightTollerance != 0 and self.Width != 0 and self.Height != 0:
					self.MinHeight = self.MinHeight - self.HeightTollerance
					self.MaxHeight = self.MaxHeight + self.HeightTollerance
				
				if self.MinHeight < 0:
					self.MinHeight = 0
				
				textFound = None
				# For each contour, find the bounding rectangle and draw it
				for component in reversed(zip(contours, hierarchy)):
					currentContour = component[0].astype('int') #ho messo astype('int') per evitare il bug
					currentHierarchy = component[1].astype('int') #ho messo astype('int') per evitare il bug
					x,y,w,h = cv2.boundingRect(currentContour)
								
					if (Log.Enable is True and Log.DebugImages is True):
						cv2.rectangle(allBoxesImg,(x,y),(x+w,y+h),(0,0,255),3)
				
					if(w >= self.MinWidth and w <= self.MaxWidth and h >= self.MinHeight and h <= self.MaxHeight and textFound is None):
						
						cv2.rectangle(img,(x,y),(x+w,y+h),(0,0,255),3)
						
						#crop
						ocrt1 = time.time()
						
						textFound = False

						left = x
						top = y
						width = w
						height = h
						
						cropped = (left, top, left+width, top+height)
						area = PilImage.crop(cropped)
						area = area.resize((width * 3, height * 3), Image.BICUBIC) 
						#save images if debug is on
						Log.WritePilImage(datetime.now().strftime("%H_%M_%S_%f") + '_text.png', area)
						
						if self.Binarize is True:
							TextFound = Ocr.GetText(area, True, self.Brightness, self.Contrast)
						else:
							TextFound = Ocr.GetText(area)
						
						Log.WriteCv2Image(matchImgName,img)
						Log.WriteCv2Image(allBoxImgName,allBoxesImg)
						return TextFound

				#save images if debug is on
				#Log.WriteCv2Image(datetime.now().strftime("%H_%M_%S_%f") + "_foo2.png", numpy.asarray(mat))
				Log.WriteCv2Image(matchImgName,img)
				Log.WriteCv2Image(allBoxImgName,allBoxesImg)
			
			#print "tempo impiegato",time.time() - tstep,"secondi"
		except Exception, err:
			#print Exception
			#print err
			#print sys.exc_traceback.tb_lineno
			Log.IsInError = True
			Log.WriteMessage("ERROR", "an exception has occurred: " + str(err) + " on line " + str(sys.exc_traceback.tb_lineno))					
	
	def medianCanny(self,img, thresh1, thresh2):
		median = numpy.median(img)
		img = cv2.Canny(img, int(thresh1 * median), int(thresh2 * median))
		return img	

class Mouse:

	x0 = 0  #None
	y0 = 0  #None
	
	@staticmethod
	def Move(x, y, button = "left"):
		try:
			Log.IsInError = False
			if sys.platform == 'win32':
				#win32api.SetCursorPos((x,y))
				#subprocess.Popen(["c:\\Program Files\\AutoIt3\\AutoIt3.exe","C:\\autoit\\mouse.au3", str(x), str(y), "move"])
				subprocess.call(["AlexaMouseProxy.exe", "/x", str(x + Mouse.x0), "/y", str(y + Mouse.y0), "/action", "move"])
		except Exception, err:
			Log.IsInError = True
			Log.WriteMessage("ERROR", "an exception has occurred: " + str(err) + " on line " + str(sys.exc_traceback.tb_lineno))		
			
	@staticmethod
	def Move2(x, y, button = "left"):
		try:
			Log.IsInError = False
			if sys.platform == 'win32':
				point = _point_t()
				result = windll.user32.GetCursorPos(pointer(point))
				print (point.x, point.y)
				
				'''
				for currX in range(point.x, x):
					#for currX in range(point.x, x):
					#time.sleep(.001)
					windll.user32.SetCursorPos(currX, y)
				'''
		except Exception, err:
			Log.IsInError = True
			Log.WriteMessage("ERROR", "an exception has occurred: " + str(err) + " on line " + str(sys.exc_traceback.tb_lineno))	
			
	@staticmethod
	def Drag(startX, startY, endX, endY):
		try:
			Log.IsInError = False
			if sys.platform == 'win32':
				subprocess.call(["AlexaMouseProxy.exe", "/x", str(startX + Mouse.x0), "/y", str(startY + Mouse.y0), "/x2", str(endX + Mouse.x0), "/y2", str(endY + Mouse.y0), "/action", "drag"])
		except Exception, err:
			Log.IsInError = True
			Log.WriteMessage("ERROR", "an exception has occurred: " + str(err) + " on line " + str(sys.exc_traceback.tb_lineno))			
	
	@staticmethod
	def Click(x, y, button = "left"):
		try:
			Log.IsInError = False
			if sys.platform == 'win32':
				subprocess.call(["AlexaMouseProxy.exe", "/x", str(x + Mouse.x0), "/y", str(y + Mouse.y0), "/action", "click", "/button", button])
		except Exception, err:
			Log.IsInError = True
			Log.WriteMessage("ERROR", "an exception has occurred: " + str(err) + " on line " + str(sys.exc_traceback.tb_lineno))	
				
	@staticmethod
	def DoubleClick(x, y, button = "left"):
		try:
			Log.IsInError = False
			if sys.platform == 'win32':
				subprocess.call(["AlexaMouseProxy.exe", "/x", str(x + Mouse.x0), "/y", str(y + Mouse.y0), "/action", "doubleClick"])
		except Exception, err:
			Log.IsInError = True
			Log.WriteMessage("ERROR", "an exception has occurred: " + str(err) + " on line " + str(sys.exc_traceback.tb_lineno))	
			
	@staticmethod
	def Scroll(direction = "down", step = "1"):
		try:
			Log.IsInError = False
			if sys.platform == 'win32':
				subprocess.call(["AlexaMouseProxy.exe", "/action", "scroll", "/direction", direction, "/step", str(step)])
		except Exception, err:
			Log.IsInError = True
			Log.WriteMessage("ERROR", "an exception has occurred: " + str(err) + " on line " + str(sys.exc_traceback.tb_lineno))	

			
class _point_t(Structure):
    _fields_ = [
                ('x',  c_long),
                ('y',  c_long),
               ]

			   
class Keyboard:

	init = False
	wsh = None
	#SendDelay = 0.030
	
	'''
	@staticmethod
	def Send(text):
		try:
			time.sleep(0.5)
			Log.IsInError = False		
			myStr = text.decode('utf-8')
			if sys.platform == 'win32':
				shell = win32com.client.Dispatch('WScript.Shell')
				
				for c in myStr:
					time.sleep(Keyboard.SendDelay)
					#print c.encode(locale.getpreferredencoding())
					shell.SendKeys(c.encode(locale.getpreferredencoding()))
					#cv2.norm(img1,img2)
			else:
				pass
		except Exception, err:
			Log.IsInError = True
			print err
			Log.WriteMessage("ERROR", "an exception has occurred: " + str(err) + " on line " + str(sys.exc_traceback.tb_lineno))
	'''
	
	@staticmethod
	def Send(text):
		try:
			#time.sleep(0.5)
			Log.IsInError = False		
			myStr = text.decode('utf-8')
			if sys.platform == 'win32':
				shell = win32com.client.Dispatch('WScript.Shell')
				
				shell.SendKeys(myStr.encode(locale.getpreferredencoding()))
			else:
				pass
		except Exception, err:
			Log.IsInError = True
			print err
			Log.WriteMessage("ERROR", "an exception has occurred: " + str(err) + " on line " + str(sys.exc_traceback.tb_lineno))
	
	@staticmethod
	def InsertText(text, delay = 25):
		try:
			Log.IsInError = False
			myStr = text.decode('utf-8')
			
			if sys.platform == 'win32':
				subprocess.call(["AlexaKeyProxy.exe", "/text", myStr.encode(locale.getpreferredencoding()), "/delay", str(delay), "/action", "insert"])

		except Exception, err:
			Log.IsInError = True
			Log.WriteMessage("ERROR", "an exception has occurred: " + str(err) + " on line " + str(sys.exc_traceback.tb_lineno))	
		
	@staticmethod
	def PutToClipBoard(text):
		try:
			Log.IsInError = False
			myStr = text.decode('utf-8')
		
			if sys.platform == 'win32':
				subprocess.call(["AlexaKeyProxy.exe", "/text", myStr.encode(locale.getpreferredencoding()), "/action", "clipPut"])
		except Exception, err:
			Log.IsInError = True
			Log.WriteMessage("ERROR", "an exception has occurred: " + str(err) + " on line " + str(sys.exc_traceback.tb_lineno))	

	@staticmethod
	def GetLatency(text):

		try:
			Log.IsInError = False		
			myStr = text.decode('utf-8')
			if sys.platform == 'win32':
				shell = win32com.client.Dispatch('WScript.Shell')
				
				time.sleep(5)
				
				for c in myStr:
					#print c.encode(locale.getpreferredencoding())
					shell.SendKeys(c.encode(locale.getpreferredencoding()))
					#cv2.norm(img1,img2)
			else:
				pass
		except Exception, err:
			Log.IsInError = True
			Log.WriteMessage("ERROR", "an exception has occurred: " + str(err) + " on line " + str(sys.exc_traceback.tb_lineno))

class NagiosUtils:
	PerformanceData = []
	TimedOutSteps = []

	@staticmethod
	def AddPerformanceData(name, value, warning = "", critical = "", state = 0):
		try:
			Log.IsInError = False
			if (state == 0):
				if value == "":
					state = 3
				elif critical != "" and value >= critical:
					state = 2
				elif warning != "" and  value >= warning:
					state = 1
					
			cnt = 0
			for performance in NagiosUtils.PerformanceData:
				if (performance[0] == name):
					NagiosUtils.PerformanceData[cnt] = (name, value, warning, critical, state)
					return
				cnt = cnt + 1
				
			NagiosUtils.PerformanceData.append((name, value, warning, critical, state))
		except Exception, err:
			Log.IsInError = True
			Log.WriteMessage("ERROR", "an exception has occurred: " + str(err) + " on line " + str(sys.exc_traceback.tb_lineno))
	
	@staticmethod
	def GetPerformanceDataString():
		try:
			Log.IsInError = False
			retString = ""
			cnt = 0
			for performance in NagiosUtils.PerformanceData:
			
				name = performance[0]
				value = performance[1]
				warning = performance[2]
				critical = performance[3]
				
				if cnt == 0:
					retString = retString + name + "=" + str(value) + "s;" + str(warning) + ";" + str(critical) + ";;"
				else:
					retString = retString + " " + name + "=" + str(value) + "s;" + str(warning) + ";" + str(critical) + ";;"
					
				cnt = cnt + 1
				
			return retString
		except Exception, err:
			Log.IsInError = True
			Log.WriteMessage("ERROR", "an exception has occurred: " + str(err) + " on line " + str(sys.exc_traceback.tb_lineno))
			return ""
	
	@staticmethod	
	def PrintOutput(message = None):
		try:
			Log.IsInError = False
			exitCode = NagiosUtils.GetExitCode()
			performanceData = NagiosUtils.GetPerformanceDataString()
			
			if len(performanceData) > 0:
				performanceData = "|" + performanceData
			else:
				performanceData = ""
			

			if message is not None:
				print message + performanceData
			elif exitCode == 2:
				print "CRITICAL: one or more steps are in critical state" + performanceData
			elif exitCode == 1:
				print "WARNING: one or more steps are in warning state" + performanceData
			elif exitCode == 3:
				print "UNKNOWN: some unknown error occured" + performanceData
			elif len(NagiosUtils.TimedOutSteps) > 0:
				print "CRITICAL: one or more steps are in timeout state" + performanceData
			else:
				print "OK: all steps are ok" + performanceData
	
			for performance in NagiosUtils.PerformanceData:
			
				name = performance[0]
				value = performance[1]
				warning = performance[2]
				critical = performance[3]
				state = performance[4]
				
				if (state == 0):
					print "OK: " + name + " time is " + str(value) + " sec."
				elif (state == 1):
					print "WARNING: " + name + " time is " + str(value) + " sec."
				elif (state == 2):
					if value != "":
						print "CRITICAL: " + name + " time is " + str(value) + " sec."
					else:
						print "CRITICAL: " + name + " time is null."
				else:
					if value != "":
						print "UNKNOWN: " + name + " time is " + str(value) + " sec."
					else:
						print "UNKNOWN: " + name + " time is null."
						
		except Exception, err:
			Log.IsInError = True
			Log.WriteMessage("ERROR", "an exception has occurred: " + str(err) + " on line " + str(sys.exc_traceback.tb_lineno))
			
	@staticmethod	
	def GetExitCode():
		exitcode = 0
		
		try:
			Log.IsInError = False
			for performance in NagiosUtils.PerformanceData:
			
				state = performance[4]
				if (state > exitcode):
					exitcode = state

				if (exitcode == 2):
					break
					
			return exitcode
			
		except Exception, err:
			Log.IsInError = True
			Log.WriteMessage("ERROR", "an exception has occurred: " + str(err) + " on line " + str(sys.exc_traceback.tb_lineno))
			return 3

class RunCmd(threading.Thread):
    def __init__(self, cmd, timeout):
        threading.Thread.__init__(self)
        self.cmd = cmd
        self.timeout = timeout

    def run(self):
        self.p = subprocess.Popen(self.cmd)
        self.p.wait()

    def Run(self):
        self.start()
        self.join(self.timeout)

        if self.is_alive():
            self.p.terminate()
            self.join()
		