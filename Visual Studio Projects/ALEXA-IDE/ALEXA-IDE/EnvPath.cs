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
using System.Collections;
using System.IO;

namespace ALEXA_IDE
{
    static class EnvPath
    {
        public static ArrayList GetPythonPath()
        {
            ArrayList pathCollection = new ArrayList(Environment.GetEnvironmentVariable("path").Split(';'));

            ArrayList pythonPathCollection = new ArrayList();

            foreach (string envPath in pathCollection)
            {
                string path = envPath;

                if (path.ToLower().IndexOf("python") != -1)
                {
                    //obtain only python root
                    if (path.ToLower().IndexOf('\\', path.ToLower().IndexOf("python")) != -1)
                    {
                        path = path.Remove(path.ToLower().IndexOf('\\', path.ToLower().IndexOf("python")));
                    }

                    if (pythonPathCollection.Count > 0)
                    {
                        bool alreadyPresent = false;
                        foreach (string pythonPath in pythonPathCollection)
                        {
                            string pyPath = pythonPath;

                            //obtain only python root
                            if (pyPath.ToLower().IndexOf('\\', pyPath.ToLower().IndexOf("python")) != -1)
                            {
                                pyPath = pyPath.Remove(pyPath.ToLower().IndexOf('\\', pyPath.ToLower().IndexOf("python")));
                            }

                            if (path == pyPath)
                            {
                                alreadyPresent = true;
                                break;
                            }
                        }

                        if (alreadyPresent == false)
                        {
                            pythonPathCollection.Add(path);
                        }
                    }
                    else
                    {
                        pythonPathCollection.Add(path);
                    }
                }
            }

            return pythonPathCollection;
        }

        public static ArrayList GetPythonExecutables()
        {

            ArrayList pythonExes = new ArrayList();

            DriveInfo[] allDrives = DriveInfo.GetDrives();

            foreach (DriveInfo d in allDrives)
            {
                try
                {
                    DirectoryInfo directoryInfo = new DirectoryInfo(d.RootDirectory.Name);

                    DirectoryInfo[] subdirectoryInfo = directoryInfo.GetDirectories();

                    foreach (DirectoryInfo subDirectory in subdirectoryInfo)
                    {

                        string pythonExe = subDirectory.FullName + @"\python.exe";
                        if (File.Exists(pythonExe))
                        {
                            pythonExes.Add(pythonExe);
                        }

                    }
                }
                catch (Exception ex)
                {
                }

            }

            return pythonExes;
        }
    }
}
