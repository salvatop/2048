#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Nov  8 14:10:11 2018

@author: spalazzo
"""

# import modules
# skeleton.py file to use as a template when porting CodeSkulptor
# projects over to PyGame.  It should provide the basic structure
# to allow moving your code into PyGame.  It will not make your
# code work automatically, but does provide the *new* pieces of code
# that are required to make your Codeskulptor projects run in
# PyGame.  You then need to replace calls to simplegui functions
# with their equivalent functions in PyGame.  Good Luck!
#
# As it is setup it will run a simple text animation illustrating
# the draw handler and timers.



# import modules
import os
import pygame
import random
import math
# pygame specific locals/constants
from pygame.locals import *

# some resource related warnings
if not pygame.font: print('Warning, fonts disabled')
if not pygame.mixer: print('Warning, sound disabled')

#import SimpleGUICS2Pygame library  (a browser Python interpreter)
try:
    import simplegui
except ImportError:
    import SimpleGUICS2Pygame.simpleguics2pygame as simplegui


# initializations
pygame.init()

# a bit similar to CodeSkulptor frame creation -- we'll call the window the canvas
canvas = pygame.display.set_mode((640, 480))
pygame.display.set_caption("My_Project")

# Pygame Wrapper functions -- resource loading sanity checks
# Taken from the "Monkey tutorial" and updated for 3.3 by me
#
# load Image:
# A colorkey is used in graphics to represent a color of the image
# that is transparent (r, g, b). -1 = top left pixel colour is used.
def load_image(name, colorkey=None):
    fullname = os.path.join('data\images', name)
    try:
        image = pygame.image.load(fullname)
    except pygame.error as message:
        print('Cannot load image:', name)
        raise SystemExit(message)
    if colorkey is not None:
        image = image.convert()
        if colorkey is -1:
            colorkey = image.get_at((0,0))
        image.set_colorkey(colorkey, RLEACCEL)
    else:
        image = image.convert_alpha()
    return image, image.get_rect()

# Load Sound
def load_sound(name):
    class NoneSound:
        def play(self): pass
    if not pygame.mixer:
        return NoneSound()
    fullname = os.path.join('data\sounds', name)
    try:
        sound = pygame.mixer.Sound(fullname)
    except pygame.error as message:
        print('Cannot load sound:', name)
        raise SystemExit(message)
    return sound

# need to create fonts and colour objects in PyGame
#fontObj = pygame.font.Font('ARBERKLEY.ttf', 32)
#fontObj2 = pygame.font.Font('ARBERKLEY.ttf', 24)
fontObj3 = pygame.font.Font(pygame.font.match_font('timesnewroman'), 32)

gold_color = pygame.Color(255, 215, 0)
white_color = pygame.Color(255, 255, 255)

# ------------------------Begin Your CodeSkulptor Port-------------------------


# Tile Images
IMAGENAME = "assets_2048.png"
TILE_SIZE = 100
HALF_TILE_SIZE = TILE_SIZE / 2
BORDER_SIZE = 45

# Directions
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

class GUI:
    """
    Class to run game GUI.
    """

    def __init__(self, game):
        self._rows = game.get_grid_height()
        self._cols = game.get_grid_width()
        self._frame = simplegui.create_frame('2048',
                        self._cols * TILE_SIZE + 2 * BORDER_SIZE,
                        self._rows * TILE_SIZE + 2 * BORDER_SIZE)
        self._frame.add_button('New Game', self.start)
        self._frame.set_keydown_handler(self.keydown)
        self._frame.set_draw_handler(self.draw)
        self._frame.set_canvas_background("#BCADA1")
        self._frame.start()
        self._game = game
        url = codeskulptor.file2url(IMAGENAME)
        self._tiles = load_image(url)
        self._directions = {"up": UP, "down": DOWN,
                            "left": LEFT, "right": RIGHT}


    def keydown(self, key):
        """
        Keydown handler
        """
        for dirstr, dirval in self._directions.items():
            if key == pygame.KEY_MAP[dirstr]:
                self._game.move(dirval)
                break

    def draw(self, canvas):
        """
        Draw handler
        """
        for row in range(self._rows):
            for col in range(self._cols):
                tile = game.get_tile(row, col)
                if tile == 0:
                    val = 0
                else:
                    val = int(math.log(tile, 2))
                canvas.draw_image(self._tiles,
                    [HALF_TILE_SIZE + val * TILE_SIZE, HALF_TILE_SIZE],
                    [TILE_SIZE, TILE_SIZE],
                    [col * TILE_SIZE + HALF_TILE_SIZE + BORDER_SIZE,
                     row * TILE_SIZE + HALF_TILE_SIZE + BORDER_SIZE],
                    [TILE_SIZE, TILE_SIZE])

    def start(self):
        """
        Start the game.
        """
        self._game.reset()

def run_gui(game):
    """
    Instantiate and run the GUI.
    """
    gui = GUI(game)
    gui.start()


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
    
     

# ------------------------End Your CodeSkulptor Port-------------------------


count = 0
draw_colour = white_color
def draw_handler(canvas):

    # clear canvas -- fill canvas with uniform colour, then draw everything below.
    # this removes everything previously drawn and refreshes 
    canvas.fill((0, 0, 0))
    

    # draw example
    global count
    count += 1
    
    text_draw = fontObj3.render("CodeSkulptor Port", True, draw_colour)
    text_draw2 = fontObj3.render("Tutorial", True, draw_colour)

    if count % 90 < 45:
        canvas.blit(text_draw, (190, 220))
    else:
        canvas.blit(text_draw2, (250, 220))

    # update the display
    pygame.display.update()

def t_example():
    global draw_colour
    if draw_colour == white_color:
        draw_colour = gold_color
    else:
        draw_colour = white_color

# pygame has no start() and stop() methods -- 0 time is off any other value is on
# set some on/off constants for readability with each timer
TIMER_OFF = 0

# timer for example -- 1500 milliseconds when on
TIMER_EXAMPLE_ON = 1500
# set the timer name to its user event for readability
timer_example = USEREVENT + 1
pygame.time.set_timer(timer_example, TIMER_EXAMPLE_ON) 			

# call this function to start everything
# could be thought of as the implemntation of the CodeSkulptor frame .start() method.
def main():
    # initialize loop until quit variable
    running = True
    
    # create our FPS timer clock
    clock = pygame.time.Clock()    
    # start the GUI and call the game
    run_gui(TwentyFortyEight(4, 4))

#---------------------------Frame is now Running-----------------------------------------
    
    # doing the infinte loop until quit -- the game is running
    while running:
        
        # event queue iteration
        for event in pygame.event.get():
            
            # window GUI ('x' the window)
            if event.type == pygame.QUIT:
                running = False

            # input - key and mouse event handlers
            elif event.type == pygame.MOUSEBUTTONDOWN:
                pass
                # just respond to left mouse clicks
                #if pygame.mouse.get_pressed()[0]:
                    #mc_handler(pygame.mouse.get_pos())
            elif event.type == pygame.KEYDOWN:
                pass
                #kd_handler(event.key)

            # timers
            elif event.type == timer_example:
                t_example()
          
                
        # the call to the draw handler
        draw_handler(canvas)
        
        # FPS limit to 60 -- essentially, setting the draw handler timing
        # it micro pauses so while loop only runs 60 times a second max.
        clock.tick(60)
        
#-----------------------------Frame Stops------------------------------------------

    # quit game -- we're now allowed to hit the quit call
    pygame.quit ()

# this calls the 'main' function when this script is executed
# could be thought of as a call to frame.start() of sorts
if __name__ == '__main__': main() 

