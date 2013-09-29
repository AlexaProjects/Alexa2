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
using System.Management;
using System.Threading;

namespace AlexaKillProcesses
{
    class Program
    {
        static void Main(string[] args)
        {
            try
            {
                bool result = KillProcesses(Environment.UserDomainName, Environment.UserName, args[0]);
            }
            catch
            {

            }

        }

        public static bool KillProcesses(string userDomain, string userName, string procName)
        {
            //set the WMI query to get all processes
            using (ManagementObjectSearcher searcher = new ManagementObjectSearcher("SELECT * FROM Win32_Process WHERE Name LIKE '%" + procName + "%'"))
            {
                //loop through all results
                foreach (ManagementObject mngObject in searcher.Get())
                {
                    try
                    {
                        //this object array will contain username and user domain
                        Object[] argObj = new Object[2];

                        //Get the user name and user domain of current process
                        mngObject.InvokeMethod("GetOwner", argObj);

                        string processUserName = (string)argObj[0];
                        string processUserDomain = (string)argObj[1];

                        //if the process user name and user domain are equal to the arguments
                        if (processUserName == userName && processUserDomain == userDomain)
                        {
                            mngObject.InvokeMethod("Terminate", null);
                        }
                    }
                    catch
                    {
                        return false;
                    }
                }

                return true;
            }
        }
    }
}
