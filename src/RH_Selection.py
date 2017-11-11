'''
Rush Hour by Guillaume Coiffier
Level Selection Menu loop
'''

## Imports

import pygame
from pygame.locals import *
from pygame.font import *
import math
import sys
import os
join = os.path.join
from fractions import Fraction

#chemin d'accès aux fichiers

path = os.getcwd().replace("src","")
if path not in sys.path:
    sys.path.append(path)

from RH_Constants import *
import RH_Utilities as Util
from RH_Import import *
from RH_Play import main

def level_selection_menu() :

    size = get_size()
    screen = pygame.display.set_mode(size)   
    
    background = Util.Background(-1)
    
    clock = pygame.time.Clock()
    RUNNING = 1 # variable de boucle
    
    buttons = pygame.sprite.Group()
    
    unlocked = get_unlocked() # Les niveaux débloqués
    beaten = get_success() # Les niveaux terminés

    titre = Util.Message("LEVEL SELECT", 20, 20, titlefont2, white, True)
    back = Util.Button("Back" , font, 200, 670, yellow)

    help_msg = pygame.sprite.Group()
    help_msg1 = Util.Message("You can only select levels you've unlocked." , 15, 700, commentfont2, white, True)
    help_msg2 = Util.Message("To unlock a level, beat all the previous ones", 15, 730, commentfont2, white, True)
    help_msg.add(help_msg1, help_msg2)
    
    n, i, j = 1, 0, 0
    
    #on charge les boutons des niveaux
    for k in range(nb_level) :
        if i > 490 :
            i=0
            j+=100
        if beaten[n-1] :
            b = Util.Button("#"+str(n), commentfont, 50+j, 150+i, orange)
        else :
            b = Util.Button("#"+str(n), commentfont, 50+j, 150+i, yellow)
        buttons.add(b)
        i += 50
        n +=1

    # On lance la boucle d'affichage
    while RUNNING:
        clock.tick(60) # on maximise le fps à 60
        background.update(screen)
        titre.update(screen)
        help_msg.update(screen)
        
        back.update(screen)
        buttons.update(screen)
        
        # Util.update_music_menu()
        
        pygame.display.flip()
        
        for event in pygame.event.get():
            if event.type ==  QUIT:
                clickSound.play()
                pygame.mixer.music.fadeout(200)
                clock.tick(5)
                RUNNING = 0
                return False
            elif event.type == MOUSEBUTTONDOWN and event.button == 1 :
                if back.highlighten :
                    clickSound.play()
                    RUNNING = 0
                    return True
                else :
                    for button in buttons :
                        i = int(button.text[1:])
                        if button.highlighten :
                            if unlocked[i-1] :
                                clickSound.play()
                                pygame.mixer.music.fadeout(200)
                                clock.tick(5)
                                k = main(i , True)
                                if not pygame.mixer.get_init():
                                    return False
                                pygame.display.set_caption("Rush Hour")

if __name__ == '__main__':
    level_selection_menu()
