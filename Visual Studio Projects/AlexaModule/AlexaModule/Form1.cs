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
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Text;
using System.Windows.Forms;
using System.Diagnostics;
using System.Collections;
using System.IO;
using Microsoft.Win32;

namespace AlexaModule
{
    public partial class Form1 : Form
    {

        private static bool manually = false;
        private static bool firstTime = false;

        private void Form1_Load(object sender, EventArgs e)
        {
            ArrayList pythonExecutables = EnvPath.GetPythonExecutables();

            ArrayList pythonPath = EnvPath.GetPythonPath();

            foreach (string pyPath in pythonPath)
            {
                try
                {
                    string pythonExe = @"\python.exe";

                    bool alreadyPresent = false;
                    foreach (string pyExec in pythonExecutables)
                    {
                        if (pyExec.ToLower() == pyPath.ToLower() + pythonExe)
                        {
                            alreadyPresent = true;
                            break;
                        }
                    }

                    if (alreadyPresent == false && File.Exists(pyPath + pythonExe))
                    {
                        pythonExecutables.Add(pyPath + pythonExe);
                    }
                }
                catch
                {
                }

            }

            foreach (string python in pythonExecutables)
            {
                listBoxPythonVersion.Items.Add(python.Remove(python.LastIndexOf('\\')));
            }

            //this.Opacity = 0;
            //this.ShowInTaskbar = false;
            //this.Visible = false;
        }

        public Form1()
        {
            InitializeComponent();
        }

        private void buttonCancel_Click(object sender, EventArgs e)
        {
            this.Close();
            Program.ExitApplication(3);

        }

        private void buttonOk_Click(object sender, EventArgs e)
        {
            string pythonVersion;

            //verify if user input is user's choice is valid
            if (textBoxInsertManually.Visible == false && listBoxPythonVersion.SelectedIndex == -1)
            {
                return;
            }
            else if (textBoxInsertManually.Visible == true && (textBoxInsertManually.Text == "" || textBoxInsertManually.Text == "Insert here the full name of pythonw executable"))
            {
                return;
            }

            //save the settings.ini file and copy .alaexa_ide folder
            if (textBoxInsertManually.Visible == true)
            {
                pythonVersion = textBoxInsertManually.Text;
            }
            else
            {
                pythonVersion = listBoxPythonVersion.Items[listBoxPythonVersion.SelectedIndex].ToString();
            }

            //get the current directory of this script
            System.Reflection.Assembly a = System.Reflection.Assembly.GetEntryAssembly();
            string currentScriptDir = System.IO.Path.GetDirectoryName(a.Location);

            CopyDirectory(currentScriptDir + "\\Alexa-Utils", pythonVersion, true);

            File.Copy(currentScriptDir + "\\Alexa.py", pythonVersion + "\\Lib\\site-packages\\Alexa.py", true);

            ArrayList pathCollection = new ArrayList(Environment.GetEnvironmentVariable("path").Split(';'));

            bool pythonHomeIsPresent = false;

            foreach (string pyPath in pathCollection)
            {
                if (pyPath.ToLower() == pythonVersion.ToLower())
                {
                    pythonHomeIsPresent = true;
                    break;
                }
            }

            if (pythonHomeIsPresent == false)
            {
                string path = pythonVersion + ";" + Environment.GetEnvironmentVariable("Path", EnvironmentVariableTarget.Machine);
                Environment.SetEnvironmentVariable("Path", path, EnvironmentVariableTarget.Machine);
            }

            RegistryKey key = RegistryUtils.GetCompatibilityModeKey();
            key.SetValue(pythonVersion + "\\python.exe", "WIN7RTM");
            key.SetValue(pythonVersion + "\\pythonw.exe", "WIN7RTM");

            key.Close();

            this.Close();
            Program.ExitApplication(0);
        }

        private void buttonInsertManually_Click(object sender, EventArgs e)
        {
            if (manually == false)
            {
                buttonInsertManually.Text = "Return to List";
                listBoxPythonVersion.Visible = false;
                textBoxInsertManually.Visible = true;
                this.Height = this.Height - 70;
                buttonOk.Location = new Point(buttonOk.Location.X, buttonOk.Location.Y - 75);
                buttonCancel.Location = new Point(buttonCancel.Location.X, buttonCancel.Location.Y - 75);
                buttonInsertManually.Location = new Point(buttonInsertManually.Location.X, buttonInsertManually.Location.Y - 75);
            }
            else
            {
                buttonInsertManually.Text = "Insert Manually";
                listBoxPythonVersion.Visible = true;
                textBoxInsertManually.Visible = false;
                this.Height = this.Height + 70;
                buttonOk.Location = new Point(buttonOk.Location.X, buttonOk.Location.Y + 75);
                buttonCancel.Location = new Point(buttonCancel.Location.X, buttonCancel.Location.Y + 75);
                buttonInsertManually.Location = new Point(buttonInsertManually.Location.X, buttonInsertManually.Location.Y + 75);
            }

            manually = !manually;
        }

        private void textBoxInsertManually_TextChanged(object sender, EventArgs e)
        {

        }

        private void textBoxInsertManually_MouseClick(object sender, MouseEventArgs e)
        {
            if (firstTime == false)
            {
                textBoxInsertManually.Text = "";
                firstTime = true;
            }
        }

        private bool CopyDirectory(string SrcPath, string DestPath, bool overwriteexisting)
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
