'''
Rush Hour by Guillaume Coiffier
'''

## Imports

import pygame
from pygame.locals import *
import math
import sys
import os

path = os.getcwd()
import RH_Utilities as Util
from RH_Constants import *
from random import randint
       

## Class Car

class Car(pygame.sprite.Sprite):
    '''Une voiture du jeu'''
    
    def __init__(self , pos, length, orient, is_player = False) :
        ''' 
        __init__(self, length, orient, is_player):
            pos = position of the top/left of the car
            length = 2 or 3 : length of the Car
            orient = bool : true for horizontal, false for vertical
            is_player : the player car 
        '''

        pygame.sprite.Sprite.__init__(self)
        if is_player :
            self.image, self.rect = Util.load_image("car0.png")
        else :
            if length == 2 : 
                col = randint(1,6)
                if orient :
                    self.image, self.rect = Util.load_image("carSH{0}.png".format(col))
                else :
                    self.image, self.rect = Util.load_image("carSV{0}.png".format(col))
            else : # length = 3
                col = randint(1,2)
                if orient :
                    self.image, self.rect = Util.load_image("carLH{0}.png".format(col))
                else :
                    self.image, self.rect = Util.load_image("carLV{0}.png".format(col))
        self.rect.move_ip(24+case*(pos[0]-1),24+case*(pos[1]-1))

        self.len = length
        self.pos = pos
        self.selected = False
        self.orient = orient

    def __str__(self) :
        return "longueur : {0}  | position : {1} ".format(self.len, self.pos)

    def highlight(self,bliton):
        pygame.draw.lines(bliton, red, True, [self.rect.topleft, self.rect.bottomleft, self.rect.bottomright, self.rect.topright], 2)

    def move_up(self, matrix):
        '''
        Moves the car one cell up and updates the obstacle matrix
        '''
        i,j = self.pos
        moved = False
        if not matrix[i][j-1] :
            self.rect.move_ip(0,-case)
            self.pos = (i,j-1)
            matrix[i][j-1] = True
            if self.len == 2 :
                matrix[i][j+1] = False
            elif self.len == 3 :
                matrix[i][j+2] = False
            pygame.time.wait(100)
            moved = True
        return matrix, moved

    def move_down(self, matrix):
        '''
        Moves the car one cell down and updates the obstacle matrix
        '''
        i,j = self.pos
        moved = False
        if (self.len == 2 and not matrix[i][j+2]) or (self.len == 3 and not matrix[i][j+3]) :
            self.rect.move_ip(0,case)
            self.pos = (i,j+1)
            matrix[i][j] = False
            if self.len == 2 :
                matrix[i][j+2] = True
            elif self.len == 3 :
                matrix[i][j+3] = True
            pygame.time.wait(100)
            moved = True
        return matrix, moved

    def move_left(self, matrix):
        '''
        Moves the car one cell left and updates the obstacle matrix
        '''
        i,j = self.pos
        moved = False
        if not matrix[i-1][j] :
            self.rect.move_ip(-case,0)
            self.pos = (i-1,j)
            matrix[i-1][j] = True
            if self.len == 2 :
                matrix[i+1][j] = False
            elif self.len == 3 :
                matrix[i+2][j] = False
            pygame.time.wait(100)
            moved = True
        return matrix, moved

    def move_right(self, matrix):
        '''
        Moves the car one cell right and updates the obstacle matrix
        '''
        i,j = self.pos
        moved = False
        if (self.len == 2 and not matrix[i+2][j]) or (self.len == 3 and not matrix[i+3][j]) :
            self.rect.move_ip(case,0)
            self.pos = (i+1,j)
            if self.len == 2 :
                matrix[i+2][j] = True
            elif self.len == 3 :
                matrix[i+3][j] = True
            matrix[i][j] = False
            pygame.time.wait(100)
            moved = True
        return matrix, moved

    def update(self, matrix, lclick, mousepos, right, left, up, down, bliton = None):
        ''' 
        update(self): update the cars position in relation to other cars
        matrix is the obstacle matrix
        lclick, mousepos, right, left, up, down are the player's inputs
        bliton = pygame.display.get_surface()
        '''

        x,y = mousepos
        moved = False
        if bliton is None :
            bliton = pygame.display.get_surface()
        if lclick and self.rect.collidepoint(x,y) :
            # On a cliqué sur la voiture -> voiture selectionnée
            self.selected = True
            selectSound.play()
        
        if self.selected :
            self.highlight(bliton)
            if self.orient : # la voiture est horizontale et ne peut bouger qu'horizontalement
                if right :
                    matrix,moved = self.move_right(matrix)
                elif left :
                    matrix,moved = self.move_left(matrix)
            else : # la voiture est verticale et ne peut bouger que verticalement
                if up :
                    matrix,moved = self.move_up(matrix)
                elif down :
                    matrix,moved = self.move_down(matrix)
        bliton.blit(self.image , self.rect)
        return matrix,moved


class MenuCar(pygame.sprite.Sprite):
    '''Une voiture dans le menu'''
    
    def __init__(self) :

        pygame.sprite.Sprite.__init__(self)
        length = randint(2,3)
        if length == 2 : 
            col = randint(1,6)
            self.image, self.rect = Util.load_image("carSV{0}.png".format(col))
        else : # length = 3
            col = randint(1,2)
            self.image, self.rect = Util.load_image("carLV{0}.png".format(col))
        if col%2 == 0 :
            self.rect.topleft = (770,768)
            self.direction = -1
        else :
            self.rect.bottomright = (640,0)
            self.direction = 1

    def update(self,bliton= None):
        ''' 
        update(self): met à jour la position de la voiture
        '''
        if bliton is None :
            bliton = pygame.display.get_surface()
        (x,y) = self.rect.topleft
        new_y = y + 2*self.direction
        if (new_y > 950) or (new_y < -180) : 
            return True
        self.rect.topleft = (x,new_y)
        bliton.blit(self.image , self.rect)
        return False