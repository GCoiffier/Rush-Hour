'''
Rush Hour by Guillaume Coiffier
Option menu loop
'''
## Imports

import pygame
from pygame.locals import *
from pygame.font import *
import math
import sys
import os
join = os.path.join

#chemin d'accès aux fichiers

path = os.getcwd()
if path not in sys.path:
    sys.path.append(path)

import RH_Utilities as Util
from RH_Constants import *
from RH_Import import *

def options_menu() :
    pygame.font.init()  #module de pygame qui gère le texte

    size = get_size()
    screen = pygame.display.set_mode(size)

    background = Util.Background(-2)

    clock = pygame.time.Clock()
    RUNNING = 1 # variable de boucle

    titre = Util.Message("OPTIONS", 512, 50, titlefont, white)
    back = Util.Button("Back" , font, 512, 400, yellow)
    credits = Util.Message("Developped by Guillaume Coiffier, 2016", 512, 700, commentfont, white)

    x1 = 312 + 400*music_volume
    x2 = 312 + 400*fx_volume
    music_button = Util.SlideButton("Music",font, x1, 200, yellow)
    noise_button = Util.SlideButton("Sound Effects",font, x2, 300, yellow)

    buttons = [music_button, noise_button]
    zero = commentfont.render("0", 1, white)
    cent = commentfont.render("100", 1, white)
    numbers = [ (zero, zero.get_rect(centerx = 312, centery = 170)),
                (zero, zero.get_rect(centerx = 312, centery = 270)),
                (cent, cent.get_rect(centerx = 712, centery = 170)),
                (cent, cent.get_rect(centerx = 712, centery = 270))]

    # On lance la boucle d'affichage
    while RUNNING:
        clock.tick(60) # on maximise le fps à 60

        for event in pygame.event.get():
            if event.type ==  QUIT:
                clickSound.play()
                clock.tick(5)
                pygame.mixer.music.fadeout(200)
                pygame.quit()
                return False
            if event.type == MOUSEBUTTONDOWN and event.button == 1 :
                if back.highlighten :
                    clickSound.play()
                    return True
                else:
                    for b in buttons:
                        if b.highlighten:
                            clickSound.play()
                            b.bind()
                            break
            elif event.type == MOUSEBUTTONUP and event.button == 1:
                OPTIONS = open(join(path,"options.txt"), mode='w')
                L = 400
                R = []
                for b in buttons:
                    b.unbind()
                    r = (b.cursorx-312)/L
                    R.append(r)
                OPTIONS.write("music_volume=" + str(R[0]) + "\n")
                OPTIONS.write("fx_volume=" + str(R[1]) + "\n")
                OPTIONS.write("resolution=1024x768" + "\n")
                OPTIONS.write("fullscreen=0" + "\n")
                OPTIONS.write("unlocked=1048575 \n")
                OPTIONS.write("success=3 \n")
                OPTIONS.write("nb_level=22 \n")
                OPTIONS.close()
                pygame.mixer.music.set_volume(music_volume)

        background.update(screen)
        titre.update(screen)

        for b in buttons:
            b.update(screen)
        credits.update(screen)
        back.update(screen)
        for n in numbers:
            screen.blit(n[0], n[1])

        pygame.display.flip()

def instructions_menu() :
    pygame.font.init()  #module de pygame qui gère le texte

    size = get_size()
    screen = pygame.display.set_mode(size)

    background = Util.Background(-2)
    screen.blit(background.image , (0,0) )

    clock = pygame.time.Clock()
    RUNNING = 1 # variable de boucle

    titre = Util.Message("INSTRUCTIONS", 512, 50, titlefont, white)
    back = Util.Button("Back" , font, 512, 720, yellow)

    instructions_msg = pygame.sprite.Group()
    l1 = Util.Message("Select with mouse, move with arrows", 512, 300, font, white)
    instructions_msg.add(l1)

    # On lance la boucle d'affichage
    while RUNNING:
        clock.tick(60) # on maximise le fps à 60
        screen = pygame.display.get_surface()

        # Gestion des événements
        for event in pygame.event.get():
            if event.type ==  QUIT:
                clickSound.play()
                clock.tick(5)
                pygame.mixer.music.fadeout(200)
                pygame.quit()
                return False
            if event.type == MOUSEBUTTONDOWN and event.button == 1 :
                if back.highlighten :
                    clickSound.play()
                    return True

        # Actualisation des éléments sur l'écran
        background.update(screen)
        titre.update(screen)
        back.update(screen)
        instructions_msg.update(screen)

        # Affichage
        pygame.display.flip()

if __name__ == '__main__':
    pygame.init()
    options_menu()
    pygame.quit()
