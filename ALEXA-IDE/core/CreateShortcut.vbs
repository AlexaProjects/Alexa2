' changeIcon.vbs - Create a Shortcut to pythonw.exe with Al'exa Icon.
' VBScript to create .lnk file
' Author Alan Pipitone http://www.alan-pipitone.com
' Version 2.3 - July 2013
' ------------------------------------------------------------------'

Dim objShell, objLink
Dim strAppPath, strWorkDir, strIconPath

strWorkDir = "C:\Alexa\ALEXA-IDE"
strAppPath = "C:\Python27-32\pythonw.exe"
strIconPath = "C:\Alexa\ALEXA-IDE\core\icon.ico"

Set objShell = CreateObject("WScript.Shell")
Set objLink = objShell.CreateShortcut("C:\Alexa\ALEXA-IDE\core\ALEXA-IDE.lnk")

objLink.Description = "ALEXA-IDE"
objLink.IconLocation = strIconPath
objLink.TargetPath = strAppPath
objLink.Arguments =  "C:\Alexa\ALEXA-IDE\core\ninja-ide.py"
objLink.WindowStyle = 2
objLink.WorkingDirectory = strWorkDir
objLink.Save

WScript.Quit
