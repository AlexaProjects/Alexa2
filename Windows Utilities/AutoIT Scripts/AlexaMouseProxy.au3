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


$action = "move"
$scrollDirection = "down"
$scrollStep = 1
$button = "left"
$speed = 10
$x = 0
$y = 0
$x2 = 0
$y2 = 0

For $i = 1 To $CmdLine[0]
	select
	
		case $CmdLine[$i] = "/x"
			$x = $CmdLine[$i+1]

		case $CmdLine[$i] = "/y"
			$y = $CmdLine[$i+1]
			
		case $CmdLine[$i] = "/x2"
			$x2 = $CmdLine[$i+1]

		case $CmdLine[$i] = "/y2"
			$y2 = $CmdLine[$i+1]
			
		case $CmdLine[$i] = "/action"
			$action = $CmdLine[$i+1]
			
		case $CmdLine[$i] = "/button"
			$button = $CmdLine[$i+1]
			
		case $CmdLine[$i] = "/speed"
			$speed = $CmdLine[$i+1]
		
		case $CmdLine[$i] = "/direction"
			$scrollDirection = $CmdLine[$i+1]
			
		case $CmdLine[$i] = "/step"
			$scrollStep = $CmdLine[$i+1]
			
	EndSelect
Next


If $action = "move" Then
	MouseMove($x, $y, $speed)
	
ElseIf $action = "click" Then
	MouseClick($button , $x, $y, 1, $speed)
	
ElseIf $action = "drag" Then
	MouseMove($x, $y, $speed)
	MouseDown("left")
	MouseMove($x2, $y2, $speed)
	MouseUp("left")
	
ElseIf $action = "doubleClick" Then
	MouseClick("left", $x, $y, 2, $speed)
	
ElseIf $action = "scroll" Then
	MouseWheel($scrollDirection, $scrollStep)
	
EndIf
