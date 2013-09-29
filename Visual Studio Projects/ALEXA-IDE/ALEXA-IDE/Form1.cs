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

namespace ALEXA_IDE
{
    public partial class Form1 : Form
    {
        private static bool firstTime = false;
        private static bool manually = false;

        public Form1()
        {
            InitializeComponent();
        }

        private void Form1_Load(object sender, EventArgs e)
        {

            this.MaximizeBox = false;
            this.MinimizeBox = false;

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

            foreach (string pythonw in pythonExecutables)
            {
                listBoxPythonApp.Items.Add(pythonw);
            }

            //this.Opacity = 0;
            //this.ShowInTaskbar = false;
            //this.Visible = false;
        }

        private void buttonAccept_Click(object sender, EventArgs e)
        {
            string pythonVersion;

            //verify if user input is user's choice is valid
            if (textBoxPythonApp.Visible == false && listBoxPythonApp.SelectedIndex == -1)
            {
                return;
            }
            else if(textBoxPythonApp.Visible == true && (textBoxPythonApp.Text == "" || textBoxPythonApp.Text == "Insert here the full name of pythonw executable"))
            {
                return;
            }

            //save the settings.ini file and copy .alaexa_ide folder
            if (textBoxPythonApp.Visible == true)
            {
                pythonVersion = textBoxPythonApp.Text;
                //ninja uses double slash to separate python dir and subdirs
                pythonVersion = pythonVersion.Replace("\\", "/");
                AlexaIDE.SavePythonVersionConfigured(pythonVersion);
            }
            else
            {
                pythonVersion = listBoxPythonApp.Items[listBoxPythonApp.SelectedIndex].ToString();
                //ninja uses double slash to separate python dir and subdirs
                pythonVersion = pythonVersion.Replace("\\", "/");
                AlexaIDE.SavePythonVersionConfigured(pythonVersion);
            }

            AlexaIDE.RunIde(pythonVersion.Replace("/","\\").Replace("\\python.exe",""));
            this.Close();
        }

        private void textBoxPythonApp_MouseClick(object sender, MouseEventArgs e)
        {
            if (firstTime == false)
            {
                textBoxPythonApp.Text = "";
                firstTime = true;
            }
        }

        private void buttonInsertManually_Click(object sender, EventArgs e)
        {

            if (manually == false)
            {
                buttonInsertManually.Text = "Return to List";
                listBoxPythonApp.Visible = false;
                textBoxPythonApp.Visible = true;
                this.Height = this.Height - 35;
                buttonAccept.Location = new Point(buttonAccept.Location.X, buttonAccept.Location.Y - 40);
                buttonCancel.Location = new Point(buttonCancel.Location.X, buttonCancel.Location.Y - 40);
                buttonInsertManually.Location = new Point(buttonInsertManually.Location.X, buttonInsertManually.Location.Y - 40);
            }
            else
            {
                buttonInsertManually.Text = "Insert Manually";
                listBoxPythonApp.Visible = true;
                textBoxPythonApp.Visible = false;
                this.Height = this.Height + 35;
                buttonAccept.Location = new Point(buttonAccept.Location.X, buttonAccept.Location.Y + 40);
                buttonCancel.Location = new Point(buttonCancel.Location.X, buttonCancel.Location.Y + 40);
                buttonInsertManually.Location = new Point(buttonInsertManually.Location.X, buttonInsertManually.Location.Y + 40);
            }

            manually = !manually;
        }

        private void buttonCancel_Click(object sender, EventArgs e)
        {
            this.Close();
        }

        /*protected override void SetVisibleCore(bool value)
        {
            if (!this.IsHandleCreated)
            {
                value = false;
                CreateHandle();
            }
            base.SetVisibleCore(value);
        }*/
    }
}
