'''
Rush Hour by Guillaume Coiffier
<Module> Import : interacts with .txt to get the level layouts
'''

import pygame
from pygame.locals import *
import sys
import os
join = os.path.join

path = os.getcwd().replace("src","")
if path not in sys.path:
    sys.path.append(path)

from RH_Constants import *
from pathfinder import get_path
from RH_Cars import Car

def get_level(n) : 
    '''
    n est le numéro du niveau à charger.
    renvoie la liste des voitures d'un niveau
    '''
    cars = []
    with open(get_path("levels.txt"),'r') as lv :
        lines = lv.readlines()
        level = lines[n-1].strip().split(";")
        for c in level :
            c = c.strip().split()
            cars.append(Car((int(c[0]),int(c[1])), int(c[2]), int(c[3]), int(c[4])))
    return cars

def extract_matrix(cars) :
    '''
    Return the obstacle's matrix of a level
    '''
    m = [[False for j in range(10)] for i in range(10)] # j for vertical, i for horizontal
    for i in range(10) :
        m[0][i] = True # Border of the grid
        m[i][0] = True
        m[9][i] = True
        m[i][9] = True
    m[9][cars[0].pos[1]] = False # La position d'arrivée
    for car in cars :
        i,j = car.pos
        m[i][j] = True
        if car.orient : # car is horizontal
            m[i+1][j] = True
            if car.len == 3 :
                m[i+2][j] = True
        else : # car is vertical
            m[i][j+1] = True
            if car.len == 3 :
                m[i][j+2] = True
    return m

def toggle_unlock(a_bool):
    ''' resets the unlocking of levels
    a_bool = True : all level unlocked
    a_bool = False : all level locked (except lvl 1)
    '''
    global od
    if a_bool :
        od["unlocked"] = 1
    else :
        od["unlocked"] = 1
    
def get_size():
    return w,h

def get_binary(char):
    '''
    returns the binary representation of the integer x
    x represents the 'unlocked' or 'success' option given in argument
    '''
    global od, nb_level
    if char == "u" :
        x = int(od["unlocked"])
    elif char == "s" :
        x = int(od["success"])
    l = []
    while x != 0 :
        l.append(x%2)
        x = x//2
    l.reverse()
    for i in range(nb_level- len(l)):
        l.append(0)
    return l

def get_unlocked():
    '''
    returns the boolean list of the unlocked levels
    l[n] = 1 if the n-th level is unlocked
    otherwise l[n] = 0
    '''
    return get_binary("u")

def get_success():
    '''
    returns the boolean list of the beaten levels
    l[n] = 1 if the n-th level is beaten unlocked
    otherwise l[n] = 0
    '''
    return get_binary("s")

def save_options() :
    global od
    open
