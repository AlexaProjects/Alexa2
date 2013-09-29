def ReplacePythonChars(text):
	newstr = text.replace("\\","\\\\")
	newstr = newstr.replace("\"","\\\"")
	newstr = newstr.replace("\'","\\'")
	return newstr