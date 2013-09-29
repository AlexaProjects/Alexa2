/*  
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
*/

using System;
using System.Collections.Generic;
using System.Text;
using System.Runtime.InteropServices;
using System.Text.RegularExpressions;

namespace AlexaCloseWindow
{
    class Program
    {
        [DllImport("user32.dll", EntryPoint = "GetWindowText", ExactSpelling = false, CharSet = CharSet.Auto, SetLastError = true)]
        public static extern int GetWindowText(IntPtr hWnd, StringBuilder lpWindowText, int nMaxCount);

        [DllImport("user32.dll")]
        [return: MarshalAs(UnmanagedType.Bool)]
        public static extern bool IsWindowVisible(IntPtr hWnd);

        [DllImport("user32.dll")]
        public static extern int SendMessage(IntPtr hWnd, int Msg, int wParam, int lParam);

        [DllImport("user32.dll", EntryPoint = "EnumDesktopWindows", ExactSpelling = false, CharSet = CharSet.Auto, SetLastError = true)]
        public static extern bool EnumDesktopWindows(IntPtr hDesktop, EnumDelegate lpEnumCallbackFunction, IntPtr lParam);


        public delegate bool EnumDelegate(IntPtr hWnd, int lParam);

        public const int WM_SYSCOMMAND = 0x0112;
        public const int SC_CLOSE = 0xF060;

        static void Main(string[] args)
        {
            try
            {
                CloseWindow(args[0]);
            }
            catch
            {
            }
        }

        /// <summary>
        /// Close window
        /// </summary>
        /// <param name="regularExpression">The regular expression that is used to find the window</param>
        public static void CloseWindow(string regularExpression)
        {
            EnumDelegate enumDelegate = delegate(IntPtr hWnd, int lParam)
            {
                try
                {
                    StringBuilder strBuilderTitle = new StringBuilder(255);
                    int nLength = GetWindowText(hWnd, strBuilderTitle, strBuilderTitle.Capacity + 1);
                    string strTitle = strBuilderTitle.ToString();

                    if (IsWindowVisible(hWnd) == true && string.IsNullOrEmpty(strTitle) == false)
                    {
                        // close the window using API        
                        if (Regex.IsMatch(strTitle, regularExpression, RegexOptions.IgnoreCase))
                            SendMessage(hWnd, WM_SYSCOMMAND, SC_CLOSE, 0);
                    }
                }
                catch { }

                return true;

            };

            EnumDesktopWindows(IntPtr.Zero, enumDelegate, IntPtr.Zero);
        }
    }
}
