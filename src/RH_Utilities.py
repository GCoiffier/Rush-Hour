'''
Rush Hour by Guillaume Coiffier
<Module> Utilities : Utility graphic classes and functions
'''

## Imports

import pygame
from pygame.locals import *
import math
import os, sys
join = os.path.join

path = os.getcwd()
if path not in sys.path:
    sys.path.append(path)

from RH_Constants import *
from RH_Import import get_size
from pathfinder import get_path

## Fonctions Utilitaires Générales

def update_music_menu() :
    if not pygame.mixer.music.get_busy() : #si aucune musique n'est jouée
         # if sys.platform == "win32":
        pygame.mixer.pre_init( 44100 , -16 , 2 , 2048 )
        pygame.mixer.init()
        pygame.mixer.music.load(get_path("MenuTheme.mp3"))
        pygame.mixer.music.set_volume(music_volume)
        pygame.mixer.music.play(-1)

def load_image(name):
    ''' 
    load_image(name) : charge l'image 'name' et renvoie sa surface ainsi que le rect associé.
    name doit être de la forme "nom.format"
    '''
    
    fullname = get_path(name)
    image = pygame.image.load(fullname)
    
    if image.get_alpha() is None or name == 'background.png' or name == 'background2.png':
            image = image.convert()
    else:
            image = image.convert_alpha()
    return ( image, image.get_rect() )

## Classes Utilitaires

class Button(pygame.sprite.Sprite):
        ''' 
        un bouton cliquable qui sert dans le menu
        si corner : les coordonnées x,y sont celles du topleftcorner
        sinon, coordonnées du centre
        '''
        def __init__(self,text, font ,x,y, color, corner = False) :
                pygame.sprite.Sprite.__init__(self)
                self.text = text
                self.font = font
                self.rect = font.render(text,1,color).get_rect()
                if not corner :
                    self.rect.center = (x,y)
                else :
                    self.rect.topleft = (x,y)
                self.highlighten = False
                self.color = color #color du type (r,g,b) avec 0<= r,g,b <= 255
        
        def update(self,bliton) :
                x,y = pygame.mouse.get_pos()
                collided =  self.rect.collidepoint(x,y)
                if not self.highlighten :
                        if collided:
                                self.highlighten = True
                else:
                        if not collided :
                                self.highlighten = False
                color = self.highlight()
                texte = self.font.render(self.text,1,color)
                bliton.blit(texte , self.rect)
        
        def highlight(self) :
                '''met le bouton en évidence'''
                (r,g,b) = self.color
                if self.highlighten:
                        r = max(r-70,0)
                        b = max(b-70,0)
                        g = max(g-70,0)
                return (r,g,b)


class SlideButton(pygame.sprite.Sprite):
    ''' un bouton coulissant qui sert dans le menu des options '''
    def __init__(self, text, font, x, y, color):
        self.text = text
        self.font = font
        self.rect = font.render(text, 1, color).get_rect()
        self.rect.bottom += 50
        self.rect.centerx, self.rect.top = get_size()[0]//2, y
        self.highlighten = False
        self.color = color
        self.cursorx = x
        self.cursorrect = pygame.rect.Rect(x-3,
                                           self.rect.bottom - 50,
                                           6, 20)
        self.textrect = pygame.rect.Rect(self.rect.left,
                                         self.rect.top-50,
                                         self.rect.height - 50,
                                         self.rect.width)
        self.bound = False
        
    def update(self, bliton = None):
        if bliton is None :
            bliton = pygame.display.get_surface()
        x0 = get_size()[0]//2
        y0 = self.rect.bottom - 40
        line = pygame.draw.line(bliton, white, (x0-200,y0), (x0+200,y0))
        x, y = pygame.mouse.get_pos()
        if not self.highlighten:
            if self.cursorrect.collidepoint(x,y):
                self.highlighten = True
        else:
            if not self.cursorrect.collidepoint(x,y):
                self.highlighten = False
        color = self.highlight()
        texte = self.font.render(self.text, 1, self.color)
        bliton.blit(texte, self.textrect)
        if self.bound and abs(x0-x) <= 200:
            self.cursorrect.centerx = x
            self.cursorx = x
        pygame.draw.rect(bliton,color,self.cursorrect)

    def bind(self):
        ''' Lie le curseur à la souris '''
        self.bound = True

    def unbind(self):
        ''' Délie le curseur de la souris '''
        self.bound = False
    
    def highlight(self) :
        '''met le curseur en évidence'''
        (r,g,b) = self.color
        if self.highlighten:
            r = max(r-70,0)
            b = max(b-70,0)
            g = max(g-70,0)
        return (r,g,b)


class Message(pygame.sprite.Sprite):
    '''
    A class for manipulating text messages and bring them on screen easily.
    :param parent: the Surface on which the text is plotted.
    :param msg: the actual text to display.
    :param font=textFont: font of the message.
    :param color: color of the message.
    '''
    def __init__(self, msg, x, y, font, color=yellow, corner = False):
        pygame.sprite.Sprite.__init__(self)
        self.text = msg
        self.font = font
        self.image = font.render(msg, True, color)
        self.rect = self.image.get_rect()
        if corner :
            self.rect.topleft = (x,y)
        else :
            self.rect.center = (x,y)
        self.color = color

    def changeMessage(self, newMsg):
        self.text = newMsg
        self.image = self.font.render(newMsg, True, self.color)
        self.rect = self.image.get_rect(center=self.rect.center)

    def update(self, bliton=None):
        '''
        Brings the message on screen
        '''
        if bliton is None :
            bliton = pygame.display.get_surface()
        bliton.blit(self.image, self.rect)

class Score(pygame.sprite.Sprite):
    '''
    A score message to be displayed
    '''
    def __init__(self, msg, font, x, y, value = 0):
        pygame.sprite.Sprite.__init__(self)
        self.msg = Message(msg, x, y, font)
        self.l = self.msg.rect.right+10

        self.val = value
        self.val_msg = Message(str(value), x, y, font)
        self.val_msg.rect.left = self.l

        self.pos = (x,y)
        self.val_to_update = False # If val_to_update : the plot will change at next update

    def __iadd__(self,x) :
        self.val += x
        self.val_to_update = True
        return self

    def reset(self):
        ''' sets the score back to 0'''
        self.val = 0
        self.val_to_update = True

    def update(self, bliton):
        if self.val_to_update :
            self.val_msg.changeMessage(str(self.val))
            self.val_to_update = False

        self.val_msg.update(bliton)
        self.msg.update(bliton)

class EndLevel:
    '''
    The message that is displayed when the player finishes a level.
    Contains 2 buttons : "next level" and "back to menu"
    Displays the score of the player on this level
    '''
    def __init__(self, nb_move):
        self.nb = nb_move

    def update(self,bliton):
        return


class Line(pygame.sprite.Sprite):

    def __init__(self, pos1, pos2, color, width):
        ''' A line '''
        pygame.sprite.Sprite.__init__(self)
        self.pos1 = pos1
        self.pos2 = pos2
        self.color = color
        self.w = width

    def update(self,bliton):
        pygame.draw.line(bliton, self.color, self.pos1, self.pos2, self.w)

class Background:
    
    def __init__(self , nlevel) : #nlevel est le numéro du niveau à charger. -1 pour le menu
        if (nlevel>=20 and not custom):
            self.image = load_image('background2.png')[0]  #potentiellement un background différent pour les hauts niveaux
        elif nlevel == -1 : # Le menu
            self.image = load_image("background_menu.png")[0]
        elif nlevel == -2 : # Menu des options/selection de niveau
            self.image = load_image("background_options.png")[0]
        else : 
            self.image = load_image('background.png')[0]

        if nlevel <= 0 :
            self.is_level = False
        else :
            self.is_level = True

        if self.is_level : # Initialisation
            self.lines = pygame.sprite.Group()
            l1 = Line((24,24),(744,24), yellow2, 5)
            l2 = Line((744,24),(744,744), yellow2, 5)
            l3 = Line((744,744),(24,744), yellow2, 5)
            l4 = Line((24,744),(24,24), yellow2, 5)
            self.lines.add(l1,l2,l3,l4)
            for i in range(1,8):
                l1 = Line((24+90*i,24),(24+90*i,744), yellow2, 3)
                l2 = Line((24,24+90*i),(744,24+90*i), yellow2, 3)
                self.lines.add(l1,l2)

    def update(self,bliton):
        bliton.blit(self.image, (0,0))
        if self.is_level :
            self.lines.update(bliton)

