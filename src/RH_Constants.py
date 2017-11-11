'''
Rush Hour by Guillaume Coiffier
<Module> Constants.py: extracts every constants and options of the game at launch
Each global variable of the game should be defined here
'''

# -- Imports --
import pygame.font
import os
from pathfinder import get_path

# -- Constants --
def _getOptionsDict():
	# "_" so that the function is not imported when from Constants import * is
	# executed
	with open(get_path("options.txt"), "r") as opt:
		optionsDict = {}
		lines = opt.readlines()
	for line in lines:
		line = line.split("=")
		optionsDict[line[0]] = line[1]
	return optionsDict

od = _getOptionsDict()
print(od)

resol = od["resolution"].split("x")
w, h = int(resol[0]), int(resol[1])
case = 90
fps = 60
resolutions = [
"960x720",
"1024x768",
"1280x720", "1280x800", "1280x960",
"1366x768",
"1440x810", "1440x900", "1440x1080",
"1920x1080", "1920x1200", "1920x1440"]

fx_volume = float(od["fx_volume"])
music_volume = float(od["music_volume"])

nb_level = int(od["nb_level"])

## Colors
white = (250, 250, 245)
yellow = (255,255,0)
yellow2 = (203,190,77)
orange = (255,127,39)
gray = (200, 200, 200)
black = (40, 40, 40)
red = (255, 200, 200)
blue = (200, 200, 255)
pink = (245, 184, 254)
green = (168,255,197)

## Fonts
pygame.font.init()
fontpath = get_path("bombard.ttf")
font = pygame.font.Font(fontpath, 45)
titlefont = pygame.font.Font(fontpath, 90)
titlefont2 = pygame.font.Font(fontpath, 80)
commentfont = pygame.font.Font(fontpath, 35)
commentfont2 = pygame.font.Font(fontpath, 24)

## Sounds
pygame.mixer.init()
clickSound = pygame.mixer.Sound(get_path("click_sound.wav"))
selectSound = pygame.mixer.Sound(get_path("select_sound.wav"))