' changeIcon.vbs - Create a Shortcut to pythonw.exe with Al'exa Icon.
' VBScript to create .lnk file
' Author Alan Pipitone http://www.alan-pipitone.com
' Version 2.3 - July 2013
' ------------------------------------------------------------------'

Dim objShell, objLink
Dim strAppPath, strWorkDir, strIconPath

strWorkDir = "%ALEXAIDE-PATH%"
strAppPath = "%PYTHON-PATH%\pythonw.exe"
strIconPath = "%ALEXAIDE-PATH%\core\icon.ico"

Set objShell = CreateObject("WScript.Shell")
Set objLink = objShell.CreateShortcut("%ALEXAIDE-PATH%\core\ALEXA-IDE.lnk")

objLink.Description = "ALEXA-IDE"
objLink.IconLocation = strIconPath
objLink.TargetPath = strAppPath
objLink.Arguments =  "%ALEXAIDE-PATH%\core\ninja-ide.py"
objLink.WindowStyle = 2
objLink.WorkingDirectory = strWorkDir
objLink.Save

WScript.Quit
