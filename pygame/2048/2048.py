#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Nov  8 11:53:33 2016

@author: Salvatore Palazzo
"""

"""
Clone of 2048 game.
"""

# import modules
import os
import pygame
import random
import math
#import 2048_gui.py


# pygame specific locals/constants
from pygame.locals import *

# some resource related warnings
if not pygame.font: print('Warning, fonts disabled')
if not pygame.mixer: print('Warning, sound disabled')






# Directions for the GUI
UP = 1
DOWN = 2
LEFT = 3
RIGHT = 4

# Offsets for computing tile indices in each direction.
OFFSETS = { UP: (1, 0),
            DOWN: (-1, 0),
            LEFT: (0, 1),
            RIGHT: (0, -1) 
          }

def merge(line):
    """
    Function that merges a single row or column in 2048.
    """
    merged_list = [i for i in line if i]
    merged_list += [0 for num in range(len(line) - len(merged_list))]
    for indx in range(0,len(line)-1):
        if merged_list[indx] == merged_list[indx +1]:
           merged_list[indx] *= 2
           merged_list[indx +1] = 0    
    # remove zeros after merge and return the list
    merged = [i for i in merged_list if i]
    merged += [0 for num in range(len(merged_list) - len(merged))]
    return merged

class TwentyFortyEight:
    """
    Class to run the game logic.
    """
    def __init__(self, grid_height, grid_width):
        self._board = []
        self._grid_height = grid_height
        self._grid_width = grid_width
        self.reset()
        self._slide = {UP    : [[0,element] for element in range(self.get_grid_width())],
                       DOWN  : [[self.get_grid_height() - 1, element] for element in range(self.get_grid_width())],
                       LEFT  : [[element, 0] for element in range(self.get_grid_height())],
                       RIGHT : [[element, self.get_grid_width() - 1] for element in range (self.get_grid_height())]}       
             
    def reset(self):
        """
        Reset the game so the grid is empty except for two
        initial tiles.
        """
        #create the board
        self._board =  [[0 for dummycol in range(self.get_grid_width())] 
                           for dummyrow in range(self.get_grid_height())]
        
        #place 2 to tiles at begin of the game
        for dummy_num in range(2):
            self.new_tile()

    def get_grid_height(self):
        """
        Get the height of the board.
        """
        return self._grid_height

    def get_grid_width(self):
        """
        Get the width of the board.
        """
        return self._grid_width
    
    def __str__(self):
        """
        Return a string representation of the grid for debugging.
        """
        msg = " "
        for dummy_row in range(self.get_grid_height()):
            msg += str(self._board[dummy_row]) + "\n "
        return msg

    def move(self, direction):
        """
        Move all tiles in the given direction and add
        a new tile if any tiles moved.
        """ 
        if(direction == UP):
            self.move_helper(direction, self.get_grid_height())
        elif(direction == DOWN):
            self.move_helper(direction, self.get_grid_height())
        elif(direction == LEFT):
            self.move_helper(direction, self.get_grid_width())
        elif(direction == RIGHT):
            self.move_helper(direction, self.get_grid_width())
            
    def move_helper(self, direction, border):
        """
        Move all columns and merge
        """      
        slides_list = list(self._slide[direction])
        tmp_list = []
        
        #get a snapshopt of the board
        before_move = str(self._board)
        
        # rotate the grid and call merge function
        for element in slides_list:
            tmp_list.append(element)
            
            for indx in range(1, border):
                tmp_list.append([dummy_row + dummy_col for dummy_row, 
                                 dummy_col in zip(tmp_list[-1], 
                                 OFFSETS[direction])])
            index= []
            
            for indx in tmp_list:
                index.append(self.get_tile(indx[0], indx[1]))

            merged_list = merge(index)

            for indx_x, indx_y in zip(merged_list, tmp_list):
                self.set_tile(indx_y[0], indx_y[1], indx_x)       
            
            tmp_list = []
            
        #get a new snapshopt of the board
        after_move = str(self._board)
        
        # if sometihing changes add a new tile
        if before_move != after_move:
            self.new_tile()
        
    def set_tile(self, row, col, value):
         """
         Set the tile at position row, col to have the given value.
         """  
         self._board[row][col] = value
                        
    def new_tile(self):
        """
        Create a new tile in a randomly selected empty
        square.  The tile should be 2 90% of the time and
        4 10% of the time.
        """
        tile = None
        num = float('%.1f' %(random.random()))
        if num < 0.9 :
            tile = 2
        else:
            tile = 4 
            
        blank_tiles = []
        # scan the grid for available position where to place the new tile
        for dummy_row in range(self.get_grid_height()):
            for dummy_col in range(self.get_grid_width()):               
                
                # check if there is a winner
                if self._board[dummy_row][dummy_col] == 2048:
                    return "Congratulations you win!"                   
                
                if self._board[dummy_row][dummy_col] == 0:
                    blank_tiles.append([dummy_row, dummy_col])              
        
        #place the new tile to a random available location 
        tile_to_place = random.choice(blank_tiles)
        self.set_tile(tile_to_place[0], tile_to_place[1], tile)
    
    def get_tile(self, row, col):
        """
        Return the value of the tile at position row, col.
        """
        return self._board[row][col]
    
     
# start the GUI and call the game
run_gui(TwentyFortyEight(4, 4))