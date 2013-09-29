import sys

def CloseHideAllWindow(close=True):
    if sys.platform == 'win32':
        import win32gui
        import win32con

        toplist, winlist = [], []

        def enum_callback(hwnd, results):
            winlist.append((hwnd, win32gui.GetWindowText(hwnd)))

        win32gui.EnumWindows(enum_callback, toplist)

        #^(?!.*details\.cfm).*selector=size.*$
        #window = [(hwnd, curTitle) for hwnd, curTitle in winlist if re.match("al.*exa.*(tool|nagios utilities|mouse and keyboard).*", curTitle, re.DOTALL | re.IGNORECASE) != None and win32gui.IsWindowVisible(hwnd) != 0]
        windows = [(hwnd, curTitle) for hwnd, curTitle in winlist if win32gui.GetWindowTextLength(hwnd) > 0]

        # just grab the hwnd for first window matching title
        #print "toplist", top
        if len(windows) > 0:
            toplist, winlist = [], []
            #print windows

            for window in windows:
                try:
                    #if openedWindow[0].lower() == 'Al\'exa tools':
                    title = window[1]

                    if 'al\'exa - nagios utilities' == title.lower() or 'al\'exa - mouse and keyboard' == title.lower() or 'al\'exa - windows and region' == title.lower() or 'al\'exa - process utilities' == title.lower() or 'al\'exa - e-mail' == title.lower():
                        if close is True:
                            win32gui.PostMessage(window[0], win32con.WM_CLOSE, 0, 0)
                        else:
                            win32gui.ShowWindow(window[0], 0)
                except:
                    continue