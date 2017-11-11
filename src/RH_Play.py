'''
Rush Hour by Guillaume coiffier
Main game loop
'''

## Imports

import pygame
from pygame.locals import *
import math
import sys
import os
join = os.path.join
from fractions import Fraction

path = os.getcwd()
if path not in sys.path:
    sys.path.append(path)

import RH_Utilities as Util
from RH_Constants import *
from RH_Cars import *
from RH_Import import *
from pathfinder import get_path

## Boucles de jeu et de fin de niveau

def wait_next_level():
    return True

def main(n, start = False): 
        '''n est le numéro du niveau qui va être joué.'''

        ## Initialisation diverses
        pygame.init()
        size = get_size()
        screen = pygame.display.set_mode(size)
        pygame.display.set_caption("Level %d" %n)
        clock = pygame.time.Clock()
        screen = pygame.display.get_surface()
        background = Util.Background(n)  
        RUNNING = 1 # variable de boucle
        FINISHED = False

        ## Initialisation du niveau
        cars = get_level(n)
        main_car = cars[0]
        finish_pos = main_car.pos[1]
        matrix = extract_matrix(cars)

        ## Initialisation du HUD
        reset_button = Util.Button("Restart Level", commentfont, 880, 600, yellow)
        exit_button = Util.Button("Quit", commentfont, 880, 700, yellow)
        compteur = Util.Score("Déplacements :", commentfont, 870, 200)
        level = Util.Score("Niveau :", commentfont, 870, 100, n)

        ## Initialisation du son
        '''if start :  #Si on a lancé le niveau depuis le menu (pas de changement de musique lors de l'enchainement de deux niveaux)
            pygame.mixer.pre_init( 44100 , -16 , 2 , 2048 )
            pygame.mixer.init()
            pygame.mixer.music.load(get_path("MainTheme.mp3"))
            pygame.mixer.music.set_volume(music_volume)
            pygame.mixer.music.play(-1)
        '''

        ## On lance la boucle de jeu
        while RUNNING:
                clock.tick(60) # on maximise le fps à 60
                lclick = False
                moved = False
                x,y = pygame.mouse.get_pos()
                FINISHED = matrix[9][finish_pos]

                screen = pygame.display.get_surface()

                # 1/ Gestion d'évènements divers
                for event in pygame.event.get():
                        
                        if event.type == MOUSEBUTTONDOWN:
                                if event.button == 1 :

                                    if reset_button.highlighten :
                                        cars = get_level(n)
                                        matrix = extract_matrix(cars)
                                        compteur.reset()

                                    elif exit_button.highlighten :
                                        RUNNING = 0
                                        return False

                                    lclick = True
                                    clickSound.play()

                        if event.type == QUIT: # le joueur choisit de quitter
                                RUNNING = 0
                                pygame.mixer.music.fadeout(200)
                                clock.tick(5)
                                pygame.quit()
                                return False

                # 2/ Récupération des input du joueur
                keys = pygame.key.get_pressed()
                right, left, up, down = keys[K_RIGHT] or keys[K_d], keys[K_LEFT] or keys[K_a], keys[K_UP] or keys[K_w], keys[K_DOWN] or keys[K_s]
                
                if keys[K_ESCAPE] :
                    pygame.mixer.music.fadeout(200)
                    clock.tick(5)
                    RUNNING = 0  # on retourne au menu
                    return False

                # 3/ Test de fin de niveau
                if FINISHED :
                    RUNNING = 0
                    return wait_next_level()
                    
                # 4/ On met à jour les sprites
                background.update(screen)
                reset_button.update(screen)
                exit_button.update(screen)
                compteur.update(screen)
                level.update(screen)

                for car in cars :
                    if lclick :
                        car.selected = False
                    matrix, moved = car.update(matrix, lclick, (x,y), right, left, up, down, screen)
                    if moved : # A car has been moved
                        compteur += 1

                # 5/ on met à jour l'ensemble de l'image
                pygame.display.flip()