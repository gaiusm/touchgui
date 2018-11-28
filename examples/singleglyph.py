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
    print "quit called"
    pygame.display.update ()  # need this to see the button pressed before we quit
    pygame.time.delay (toggle_delay * 2) #  delay program so we see the button change
    pygame.quit ()  #  now shutdown pygame
    quit ()  #  and shutdown python


def myreturn (name, tap):
    print "return called"


def imagedir (name):
    return os.path.join (touchguiconf.touchguidir, name)


def button_list (name):
    return [touchgui.image_gui (imagedir ("images/PNG/White/2x/%s.png") % (name)).white2grey (.5),
            touchgui.image_gui (imagedir ("images/PNG/White/2x/%s.png") % (name)).white2grey (.1),
            touchgui.image_gui (imagedir ("images/PNG/White/2x/%s.png") % (name)),
            touchgui.image_gui (imagedir ("images/PNG/White/2x/%s.png") % (name)).white2rgb (.1, .2, .4)]

#
#  button - create a single power button and return it in a list.
#

def button ():
    return [touchgui.image_tile (button_list ("power"),
                                 touchgui.posX (0.95), touchgui.posY (1.0),
                                 100, 100, myquit)]


def pressed (name, tap):
    print name, "pressed"


#
#  glyph - create a single glyph button and return it in a list.
#

def glyph ():
    return [touchgui.text_tile (touchguipalate.wood_dark, touchguipalate.gold, touchguipalate.wood_light, touchguipalate.wood_light,
                                u'\u00F7', touchgui.unitY (0.05),
                                touchgui.posX (0.0), touchgui.posY (1.0),
                                100, 100, pressed, "divide")]


def main ():
    pygame.init ()
    if full_screen:
        gameDisplay = pygame.display.set_mode ((display_width, display_height), FULLSCREEN)
    else:
        gameDisplay = pygame.display.set_mode ((display_width, display_height))

    pygame.display.set_caption ("Simple Test")
    touchgui.set_display (gameDisplay, display_width, display_height)

    forms = button () + glyph ()
    gameDisplay.fill (touchguipalate.black)
    touchgui.select (forms, event_test)

main ()
