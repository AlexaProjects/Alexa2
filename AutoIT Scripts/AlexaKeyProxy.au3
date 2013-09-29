; Copyright (C) 2013 Alan Pipitone
    
; Al'exa is free software: you can redistribute it and/or modify
; it under the terms of the GNU General Public License as published by
; the Free Software Foundation, either version 3 of the License, or
; (at your option) any later version.

; Al'exa is distributed in the hope that it will be useful,
; but WITHOUT ANY WARRANTY; without even the implied warranty of
; MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
; GNU General Public License for more details.

; You should have received a copy of the GNU General Public License
; along with Al'exa.  If not, see <http://www.gnu.org/licenses/>.


$delay = 5
$text = ""
$action = "insert"

For $i = 1 To $CmdLine[0]
	select
	
		case $CmdLine[$i] = "/text"
			$text = $CmdLine[$i+1]

		case $CmdLine[$i] = "/delay"
			$delay = $CmdLine[$i+1]
			
		case $CmdLine[$i] = "/action"
			$action = $CmdLine[$i+1]
			
	EndSelect
Next

AutoItSetOption ("SendKeyDelay", $delay)

If $action = "insert" Then
	Send($text)
	
ElseIf $action = "clipPut" Then
	ClipPut($text)
	
EndIf

