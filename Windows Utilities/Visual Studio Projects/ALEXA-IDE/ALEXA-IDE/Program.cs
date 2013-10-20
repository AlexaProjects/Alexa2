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
using System.Windows.Forms;
using System.IO;
using Microsoft.Win32;


namespace ALEXA_IDE
{
    static class Program
    {
        /// <summary>
        /// The main entry point for the application.
        /// </summary>
        [STAThread]
        static void Main()
        {
            if (AlexaIDE.PythonVersionConfigured() == false)
            {
                Application.EnableVisualStyles();
                Application.SetCompatibleTextRenderingDefault(false);
                Application.Run(new Form1());
            }
            else
            {

                //string path = AlexaIDE.GetIdePath();
                string alexaSettingFile = Environment.ExpandEnvironmentVariables("%USERPROFILE%") + @"\.alexa_ide\settings.ini";
                string[] lines = File.ReadAllLines(alexaSettingFile);
                string pythonpath = "";

                //get the pythonPath=
                foreach (string line in lines)
                {
                    if (line.IndexOf("execution\\pythonPath=") != -1)
                    {
                        pythonpath = line.Replace("execution\\pythonPath=", "");
                        pythonpath = pythonpath.Replace("/","\\").Replace("\\python.exe","");
                    }
                }

                AlexaIDE.RunIde(pythonpath);
            }

        }
    }
}
