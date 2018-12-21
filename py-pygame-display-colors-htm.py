#!/usr/bin/python
#
# py-pygame-display-colors-htm.py
#
# Produces a table of all the pygame colours.
#
# This  program  is free software: you can redistribute it and/or  modify it
# under the terms of the GNU General Public License as published by the Free
# Software  Foundation, either version 3 of the License, or (at your option)
# any later version.
#
# This  program  is  distributed  in the hope that it will  be  useful,  but 
# WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY
# or  FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public  License
# for more details.
#
# You  should  have received a copy of the GNU General Public License  along
# with this program.  If not, see <http://www.gnu.org/licenses/>.
#
# https://stackoverflow.com/questions/3121979
#
import sys
import pygame 
   
_format = { 'header'  : ( '<table width=800 style="' +
                          'vertical-align:middle;' +
                          'background:#ffffff; ' + 
                          'padding:0px; line-height:133%; ' + 
                          'font-family:monospace; white-space:nowrap; '
                          'white-space:pre; overflow:auto; ' + 
                          'font-size:10pt; color:#696969;"' +
                          '><tr>'),
 
            'colour'  : ( '<td width=64 style="' +
                          'background:'),
 
            'name'    : ( '">&nbsp;</td><td>&nbsp;'),
 
            'newline' : ('</td></tr>'),
 
            'footer'  : ('</table><br><p>\n')}
 
#def _RGB (_red, _blue, _green, _alpha):
def _RGB (_color):
  return '#%06X' %  ((_color[0] * 256 + _color[1]) * 256 +_color[2]) # Ignores alpha
 
#_colour_names = pygame.colordict.THECOLORS.items()
#_colour_names.sort(key=lambda name: name[0]) # Sort list by colour name

_colour_names = sorted(pygame.colordict.THECOLORS.items()) # Sort list by colour name
 
sys.stdout.write(_format['header'] + "\n")
for _colour in _colour_names:
  sys.stdout.write(_format['colour'] + _RGB(_colour[1]))
  sys.stdout.write(_format['name'] + _RGB(_colour[1]) + " " + _colour[0])
  sys.stdout.write(_format['newline'] + "\n")
    
sys.stdout.write(_format['footer'] + "\n")
 
pygame.quit()
#exit()