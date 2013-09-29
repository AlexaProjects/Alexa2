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
using Microsoft.Win32;
using Microsoft.Win32.SafeHandles;
using System.Runtime.InteropServices;
using System.Reflection;

namespace AlexaModule
{
    class RegistryUtils
    {

        [DllImport("advapi32.dll", CharSet = CharSet.Auto)]
        public static extern int RegOpenKeyEx(IntPtr hKey, string subKey, int ulOptions, int samDesired, out int phkResult);

        enum RegWow64Options
        {
            None = 0,
            KEY_WOW64_64KEY = 0x0100,
            KEY_WOW64_32KEY = 0x0200
        }

        static RegistryKey OpenSubKey(RegistryKey parentKey, string subKeyName, bool writable, RegWow64Options regOptions)
        {
            int rights = (int)131097;

            if (writable)
                rights = (int)131078;

            Type keyType = typeof(RegistryKey);

            FieldInfo fieldInfo = keyType.GetField("hkey", BindingFlags.NonPublic | BindingFlags.Instance);

            IntPtr keyHandle = ((SafeHandle)fieldInfo.GetValue(parentKey)).DangerousGetHandle();

            if (parentKey == null || keyHandle == IntPtr.Zero)
                return null;

            int subKeyHandle, result = RegOpenKeyEx(keyHandle, subKeyName, 0, rights | (int)regOptions, out subKeyHandle);

            if (result != 0)
                return null;

            IntPtr hKey = (IntPtr)subKeyHandle;

            Type safeHandleType = typeof(SafeHandleZeroOrMinusOneIsInvalid).Assembly.GetType("Microsoft.Win32.SafeHandles.SafeRegistryHandle");
            Type[] safeHandleConstructorTypes = new Type[] { typeof(IntPtr), typeof(bool) };

            Type[] keyConstructorTypes = new Type[] { safeHandleType, typeof(bool) };

            ConstructorInfo safeHandleConstructorInfo = safeHandleType.GetConstructor(BindingFlags.Instance | BindingFlags.NonPublic, null, safeHandleConstructorTypes, null);

            Object[] keyAndOwns = new Object[] { hKey, false };

            Object[] invokeParameters = new Object[] { safeHandleConstructorInfo.Invoke(keyAndOwns), writable };

            ConstructorInfo keyConstructorInfo = keyType.GetConstructor(BindingFlags.Instance | BindingFlags.NonPublic, null, keyConstructorTypes, null);

            return (RegistryKey)keyConstructorInfo.Invoke(invokeParameters);
        }

        public static RegistryKey GetCompatibilityModeKey()
        {
            RegistryKey retKey = null;

            try
            {
                RegistryKey appCompatFlag = OpenSubKey(Registry.LocalMachine, @"SOFTWARE\Microsoft\Windows NT\CurrentVersion\AppCompatFlags", true, RegWow64Options.KEY_WOW64_64KEY);

                if(appCompatFlag != null)
                {
                    RegistryKey Layers = appCompatFlag.OpenSubKey("Layers");

                    if (Layers == null)
                    {
                        appCompatFlag.CreateSubKey("Layers");
                        appCompatFlag.Close();
                    }

                    retKey = OpenSubKey(Registry.LocalMachine, @"SOFTWARE\Microsoft\Windows NT\CurrentVersion\AppCompatFlags\Layers", true, RegWow64Options.KEY_WOW64_64KEY);
                }
                
            }
            catch
            {
            }

            if (retKey == null)
            {
                RegistryKey appCompatFlag = Registry.LocalMachine.OpenSubKey(@"SOFTWARE\Microsoft\Windows NT\CurrentVersion\AppCompatFlags", true);

                if (appCompatFlag != null)
                {
                    RegistryKey Layers = appCompatFlag.OpenSubKey("Layers");

                    if (Layers == null)
                    {
                        appCompatFlag.CreateSubKey("Layers");
                        appCompatFlag.Close();
                    }

                    retKey = Registry.LocalMachine.OpenSubKey(@"SOFTWARE\Microsoft\Windows NT\CurrentVersion\AppCompatFlags\Layers", true);
                }

            }

            return retKey;
        }
    }
}
