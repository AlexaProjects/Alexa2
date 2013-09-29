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
using System.Diagnostics;
using System.IO;

namespace ALEXA_IDE
{
    static class AlexaIDE
    {

        public static void RunIde(string pythonpath)
        {
            string alexaIdePath = GetIdePath();

            CreatePythonwShortcut(pythonpath, alexaIdePath);

            ProcessStartInfo startInfo = new ProcessStartInfo(alexaIdePath + @"\core\ALEXA-IDE.lnk");
            //startInfo.UseShellExecute = true;
            //startInfo.WindowStyle = ProcessWindowStyle.Maximized;

            //Process.Start(startInfo);

            //startInfo.Arguments = alexaIdePath + @"\core\ninja-ide.py";

            Process.Start(startInfo);
        }

        private static string GetIdePath()
        {
            //get the current directory of this script
            System.Reflection.Assembly a = System.Reflection.Assembly.GetEntryAssembly();
            return System.IO.Path.GetDirectoryName(a.Location);
        }

        private static void CreatePythonwShortcut(string pythonVersion, string alexaIdePath)
        {
            string alexaRootPath = Path.GetDirectoryName(alexaIdePath);
            //read the vbs template and replace directory
            string text = File.ReadAllText(alexaIdePath + @"\core\CreateShortcutTemplate.vbs");
            text = text.Replace("%ALEXA-PATH%", alexaRootPath);
            text = text.Replace("%ALEXAIDE-PATH%", alexaIdePath);
            text = text.Replace("%PYTHON-PATH%", pythonVersion);

            using (StreamWriter outfile = new StreamWriter(alexaIdePath + @"\core\CreateShortcut.vbs"))
            {
                outfile.Write(text);
            }

            Process scriptProc = new Process();
            scriptProc.StartInfo.FileName = @"cscript";
            scriptProc.StartInfo.Arguments = "//B //Nologo \"" + alexaIdePath + "\\core\\CreateShortcut.vbs\"";
            scriptProc.StartInfo.WindowStyle = ProcessWindowStyle.Hidden; //prevent console window from popping up
            scriptProc.Start();
            scriptProc.WaitForExit();
            scriptProc.Close();

        }

        public static void SavePythonVersionConfigured(string pythonwFullName)
        {
            string alexaPathOnUserFolder = Environment.ExpandEnvironmentVariables("%USERPROFILE%") + @"\.alexa_ide";

            Directory.CreateDirectory(alexaPathOnUserFolder);

            string path = GetIdePath();
            string settingsFile = path + @"\core\user_files\settingstemplate.ini";
            string[] lines = File.ReadAllLines(settingsFile);

            //line 1 is: "execution\pythonPath="
            lines[1] = lines[1] + pythonwFullName;

            //save txt file
            File.WriteAllLines(alexaPathOnUserFolder + @"\settings.ini", lines);

            CopyDirectory(path + @"\core\user_files\alexa_ide", alexaPathOnUserFolder, false);

        }

        public static bool PythonVersionConfigured()
        {
            string alexaPathOnUserFolder = Environment.ExpandEnvironmentVariables("%HOMEDRIVE%%HOMEPATH%") + @"\.alexa_ide";

            if (!Directory.Exists(alexaPathOnUserFolder) || !File.Exists(alexaPathOnUserFolder + "\\settings.ini"))
            {
                return false;
            }
            else
            {
                return true;
            }

            /*string path = GetIdePath();
            string settingsFile = path + @"\core\user_files\settingstemplate.ini";
            string[] lines = File.ReadAllLines(settingsFile);

            if (lines[1] == @"execution\pythonPath=")
            {
                return false;
            }
            else
            {
                return true;
            }*/
        }

        private static bool CopyDirectory(string SrcPath, string DestPath, bool overwriteexisting)
        {
            bool returnValue = true;
            try
            {
                SrcPath = SrcPath.EndsWith(@"\") ? SrcPath : SrcPath + @"\";
                DestPath = DestPath.EndsWith(@"\") ? DestPath : DestPath + @"\";

                if (Directory.Exists(SrcPath))
                {
                    if (Directory.Exists(DestPath) == false)
                        Directory.CreateDirectory(DestPath);

                    foreach (string fls in Directory.GetFiles(SrcPath))
                    {
                        FileInfo flinfo = new FileInfo(fls);
                        flinfo.CopyTo(DestPath + flinfo.Name, overwriteexisting);
                    }
                    foreach (string drs in Directory.GetDirectories(SrcPath))
                    {
                        DirectoryInfo drinfo = new DirectoryInfo(drs);
                        if (CopyDirectory(drs, DestPath + drinfo.Name, overwriteexisting) == false)
                            returnValue = false;
                    }
                }
                else
                {
                    returnValue = false;
                }
            }
            catch (Exception ex)
            {
                returnValue = false;
            }
            return returnValue;
        }
    }
}
