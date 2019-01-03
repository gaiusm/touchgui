#!/usr/bin/env python

import pygame, touchgui, touchguipalate, touchguiconf, math, os
from pygame.locals import *

# display_width, display_height = 1920, 1080
display_width, display_height = 800, 600
display_width, display_height = 1920, 1080
full_screen = False
full_screen = True
toggle_delay = 250


def event_test (event):
    if (event.type == KEYDOWN) and (event.key == K_ESCAPE):
        myquit (None)


def myquit (name = None, tap = 1):
    pygame.display.update ()
    pygame.time.delay (toggle_delay * 2)
    pygame.quit ()
    quit ()


def myreturn (name, tap = 1):
    global selection_complete
    pygame.display.update ()
    selection_complete = True


def imagedir (name):
    return os.path.join (touchguiconf.touchguidir, name)


def button_list (name):
    return [touchgui.image_gui (imagedir ("images/PNG/White/2x/%s.png") % (name)).white2grey (.5),
            touchgui.image_gui (imagedir ("images/PNG/White/2x/%s.png") % (name)).white2grey (.1),
            touchgui.image_gui (imagedir ("images/PNG/White/2x/%s.png") % (name)),
            touchgui.image_gui (imagedir ("images/PNG/White/2x/%s.png") % (name)).white2rgb (.1, .2, .4)]


def buttons ():
    return [touchgui.image_tile (button_list ("power"),
                                 touchgui.posX (0.95), touchgui.posY (1.0),
                                 100, 100, myquit),
            touchgui.image_tile (button_list ("return"),
                                 touchgui.posX (0.0), touchgui.posY (1.0),
                                 100, 100, myreturn)]

def more_buttons ():
    size = 75
    limit = -1
    count = 0
    b = []
    for x in range (0, display_width-size, size):
        for y in range (100, display_height-size, size):
            b += [touchgui.image_tile (button_list ("return"),
                                       x, y,
                                       size, size, myreturn)]
            if count == limit:
                return b
            count += 1
    return b



def main ():
    global players

    pygame.init ()
    if full_screen:
        gameDisplay = pygame.display.set_mode ((display_width, display_height), FULLSCREEN)
    else:
        gameDisplay = pygame.display.set_mode ((display_width, display_height))

    touchgui.set_display (gameDisplay, display_width, display_height)

    forms = buttons () + more_buttons ()
    print len (forms)
    gameDisplay.fill (touchguipalate.black)
    touchgui.select (forms, event_test)


main ()
