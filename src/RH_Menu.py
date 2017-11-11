'''
Rush Hour by Guillaume Coiffier
Main Menu Loop
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

srcpath = os.getcwd()
path = srcpath.replace("src", "")
print(path)

if path not in sys.path:
    sys.path.append(path)

from RH_Constants import *
#from RH_Editor import *
from RH_Play import *
from RH_Selection import *
from RH_Cars import *
#from RH_Solve import *
from RH_Options import options_menu, instructions_menu
import RH_Utilities as Util


def run_game() :
    pygame.init()

    size = get_size()
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption("RUSH HOUR")

    background = Util.Background(-1)
    screen.blit(background.image , (0,0) )
    decoration_cars = []

    clock = pygame.time.Clock()
    RUNNING = 1 # variable de boucle
    randomizer = 0

    titre = titlefont.render("Rush Hour", 1, white)
    titrepos = titre.get_rect(centerx=230, centery = 100)

    start_game = Util.Button("Start Game", font,
                                    50, 200, yellow, True)
    level_select = Util.Button("Level Selection", font,
                                      50, 300, yellow, True)
    exit_game = Util.Button("Exit Game", font,
                                   50, 700, yellow, True)
    instructions = Util.Button("Instructions", font,
                                 50, 400, yellow, True)
    options = Util.Button("Options", font,
                                 50, 500, yellow, True)

    # On lance la boucle d'affichage
    while RUNNING:
        clock.tick(60) # on maximise le fps à 60
        screen = pygame.display.get_surface()

        # 1/ Update des boutons
        background.update(screen)
        screen.blit(titre, titrepos)
        start_game.update(screen)
        exit_game.update(screen)
        level_select.update(screen)
        instructions.update(screen)
        options.update(screen)

        # 2/ Update de la musique
        #Util.update_music_menu()

        # 3/ Update des voitures
        if randomizer == 0 :
            n = MenuCar()
            decoration_cars.append(n)
            randomizer = randint(150,300)

        for car in decoration_cars :
            a_bool = car.update(screen)
            if a_bool : # La voiture est arrivée au bout
                decoration_cars.remove(car)

        randomizer -= 1

        # 4/ Gestion de événements
        for event in pygame.event.get():
            if event.type ==  QUIT:
                RUNNING = 0
                pygame.mixer.music.fadeout(200)
                clock.tick(5)
                pygame.quit()
            elif event.type == MOUSEBUTTONDOWN and event.button == 1:

                if exit_game.highlighten :
                    RUNNING = 0
                    clickSound.play()
                    clock.tick(4)
                    pygame.quit()

                elif start_game.highlighten :
                    clickSound.play()
                    pygame.mixer.music.fadeout(200)
                    clock.tick(5)
                    n = 1
                    k = main(n,True)
                    while k :
                        n += 1
                        k = main(n)
                    if not pygame.mixer.get_init():
                        return
                    pygame.display.set_caption("Rush Hour")

                elif level_select.highlighten :
                    clickSound.play()
                    k = level_selection_menu()
                    if not k:
                        RUNNING = 0
                        pygame.quit()
                    else:
                        pygame.display.set_caption("Rush Hour")

                elif instructions.highlighten :
                    clickSound.play()
                    k = instructions_menu()
                    if not k :
                        return

                elif options.highlighten:
                    clickSound.play()
                    k = options_menu()
                    if not k :
                        return


        # 5/ Affichage
        pygame.display.flip()
