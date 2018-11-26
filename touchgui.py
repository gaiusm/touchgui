#!/usr/bin/env python
#
# touchgui.py a simple touch gui for Pygame.
#
# Copyright (C) 2018 Free Software Foundation, Inc.
# Contributed by Gaius Mulley <gaius@glam.ac.uk>.
#
# This file is part of TouchGui.
#
# TouchGui is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3, or (at your option)
# any later version.
#
# TouchGui is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with GNU Modula-2; see the file COPYING.  If not, write to the
# Free Software Foundation, 51 Franklin Street, Fifth Floor, Boston, MA
# 02110-1301, USA.
#

import pygame, os
from pygame.locals import *


from palate import *

display_width, display_height = None, None
fuzz = "100%"

double_tap = 500   # no of millisecs to perform double tap


def safe_system (command):
    r = os.system (command)
    if r != 0:
        _errorf ("os.system:  failed when trying to execute: " + command + " with an exit code " + str (r))


def check_exists (name):
    # print name
    if not os.path.isfile (cache_file (name)):
        _errorf ("convert has failed to generate " + name)

#
#  set_resolution - configures the resolution for the gui display.
#                   This must be called before, select.
#

def set_resolution (x, y):
    global display_width, display_height
    display_width, display, height = x, y


#
#  unitX - v is a floating point number and unitX returns the
#          distance in pixels.  0.0..1.0  X axis.
#

def unitX (v):
    return int (v * display_width)

#
#  unitY - v is a floating point number and unitY returns the
#          distance in pixels.  0.0..1.0  Y axis.
#

def unitY (v):
    return int (v * display_height)

#
#  posX - v is a floating point number and posX returns the
#         position in pixels.  0.0..1.0  X axis.
#

def posX (v):
    return int (v * display_width)

#
#  posY - v is a floating point number and posY returns the
#         position in pixels.  0.0..1.0  X axis.
#

def posY (v):
    return display_height - unitY (v)

class form:
    def __init__ (self, children):
        self.children = children
    def set_active (self):
        for c in self.children:
            c.set_active ()
    def set_frozen (self):
        for c in self.children:
            c.set_frozen ()
    def update (self):
        for c in self.children:
            c.update ()
    def select (self):
        for c in self.children:
            c.select ()
    def deselect (self):
        for c in self.children:
            c.deselect ()

def text_objects (text, font, colour = white):
    textSurface = font.render (text, True, colour)
    return textSurface, textSurface.get_rect ()

# tile_state enumerated type.  Order must be coordinated with the _colours list below
tile_frozen, tile_active, tile_activated, tile_pressed = range (4)

class text_tile:
    def __init__ (self, default_colour, activated_colour, pressed_colour, frozen_colour,
                  text_message, text_size,
                  x, y, width, height, action=None, tid=None, flush=None):
        # the _colour list must be in this order (the same as the tile_state above)
        self._colours = [frozen_colour, default_colour, activated_colour, pressed_colour]
        self._x = x
        self._y = y
        self._width = width
        self._height = height
        self._action = action
        self._getid = tid
        self._ticks = None
        self._text_message = text_message
        self._text_size = text_size
        self._text_font = pygame.font.SysFont (None, text_size)
        self._text_surf, self._text_rect = text_objects (text_message, self._text_font, white)
        self._text_rect.center = ( (x+(width/2)), (y+(height/2)) )
        self._state = tile_active
        self._flush = flush
    #
    #  select - test to see if the mouse position is over the tile and it is not frozen
    #           and if the mouse is activated call the action.
    #
    def select (self):
        if self._state != tile_frozen:
            mouse = pygame.mouse.get_pos ()
            click = pygame.mouse.get_pressed ()
            if self._x+self._width > mouse[0] > self._x and self._y+self._height > mouse[1] > self._y:
                self.set_activated ()
                if click[0] == 1:
                    self.set_pressed ()
                    if self._action != None:
                        if self._double_tap (pygame.time.get_ticks ()):
                            self._action (self._getid, 2)
                        else:
                            self._action (self._getid, 1)
    #
    #  _double_tap - return True if the tile was double tapped and remember this
    #                tap time.
    #
    def _double_tap (self, ticks):
        result = (not ((self._ticks == None) or (ticks - self._ticks > double_tap)))
        self._ticks = ticks
        return result
    def deselect (self):
        if self._state != tile_frozen:
            self.set_active ()
    #
    #  set_active - change the tile state to active and update if necessary
    #
    def set_active (self):
        if self._state != tile_active:
            self._state = tile_active
            self.update ()
    #
    #  set_activated - change the tile state to activated and update if necessary
    #
    def set_activated (self):
        if self._state != tile_activated:
            self._state = tile_activated
            self.update ()
    #
    #  set_frozen - change the tile state to frozen and update if necessary
    #
    def set_frozen (self):
        if self._state != tile_frozen:
            self._state = tile_frozen
            self.update ()
    #
    #  set_pressed - change the tile state to pressed and update if necessary
    #
    def set_pressed (self):
        if self._state != tile_frozen:
            self._state = tile_pressed
            self.update ()
    #
    #  update - redraw the tile.
    #
    def update (self):
        # print "update text_tile",
        pygame.draw.rect (gameDisplay, self._colours[self._state],
                          (self._x, self._y, self._width, self._height))
        # print self._x, self._y, self._width, self._height, self._y - self._height
        gameDisplay.blit (self._text_surf, self._text_rect)
    #
    #  flush_display - call the callback if one is registered.
    #
    def flush_display (self):
        if not (self._flush is None):
            self._flush ()


def load_image (name):
    return pygame.image.load (name).convert_alpha ()


def flattern_directories (name):
    name = name.replace ("/", "-")
    # print "flattened", name
    return name

def cache_file (name):
    name = flattern_directories (name)
    assert (name[0] != "-")
    return os.path.join (os.path.join (os.path.join (os.environ["HOME"], ".cache"), "touchgui"), name)


def cache_exists (name):
    """
    print "looking up cache", name,
    if os.path.isfile (cache_file (name)):
        print "yes"
    else:
        print "no"
    """
    return os.path.isfile (cache_file (name))

#
#  find_file - looks in the current directory for, name, and then looks up the cache.
#

def find_file (name):
    if os.path.isfile (name):
        return name
    if os.path.isfile (cache_file (name)):
        return cache_file (name)
    _errorf ("unable to find file " + name)


def _errorf (s):
    print s
    os.sys.exit (1)


class image_gui:
    def __init__ (self, name):
        if not os.path.isfile (name):
            _errorf ("image " + name + " not found")
        self.name = name

    #
    #  grey -
    #

    def grey (self):
        newname = "%s-grey" % (self.name.split ("/")[-1])
        if cache_exists (newname):
            self.name = newname
            return self
        safe_system ("convert %s -set colorspace Gray -separate -average %s" % (find_file (self.name), cache_file (newname)))
        check_exists (newname)
        self.name = newname
        return self

    #
    #  white2red -
    #

    def white2red (self):
        newname = "%s-red" % (self.name.split ("/")[-1])
        if cache_exists (newname):
            self.name = newname
            return self
        safe_system ("convert %s -fuzz %s -fill red -opaque white %s" % (find_file (self.name), fuzz, cache_file (newname)))
        check_exists (newname)
        self.name = newname
        return self

    #
    #  white2blue -
    #

    def white2blue (self):
        newname = "%s-blue" % (self.name.split ("/")[-1])
        if cache_exists (newname):
            self.name = newname
            return self
        safe_system ("convert %s -fuzz %s -fill blue -opaque white %s" % (find_file (self.name), fuzz, cache_file (newname)))
        check_exists (newname)
        self.name = newname
        return self

    #
    #  white2grey -
    #

    def white2grey (self, value=.85):
        newname = "%s-grey" % (self.name.split ("/")[-1])
        if cache_exists (newname):
            self.name = newname
            return self
        safe_system ("convert %s -fuzz %s -fill 'rgb(%d,%d,%d)' -opaque white %s" % (find_file (self.name), fuzz,
                                                                                     int (value * 255.0), int (value * 255.0), int (value * 255.0),
                                                                                     cache_file (newname)))
        check_exists (newname)
        self.name = newname
        return self

    #
    #  white2rgb -
    #

    def white2rgb (self, r=.85, g=.85, b=.85):
        r = int (r * 256.0)
        g = int (g * 256.0)
        b = int (b * 256.0)
        newname = "%s-rgb-%d-%d-%d" % (self.name.split ("/")[-1], r, g, b)
        if cache_exists (newname):
            self.name = newname
            return self
        safe_system ("convert %s -fuzz %s -fill 'rgb(%d,%d,%d)' -opaque white %s" % (find_file (self.name), fuzz, r, g, b, cache_file (newname)))
        check_exists (newname)
        self.name = newname
        return self

    #
    #  resize -
    #

    def resize (self, width, height):
        newname = "%s-%dx%d" % (self.name.split ("/")[-1], width, height)
        if cache_exists (newname):
            self.name = newname
            return self
        safe_system ("convert %s -resize %dx%d\! %s" % (find_file (self.name), width, height, cache_file (newname)))
        check_exists (newname)
        self.name = newname
        return self

    #
    #  load_image -
    #

    def load_image (self):
        if cache_exists (self.name):
            return pygame.image.load (cache_file (self.name)).convert_alpha ()
        return pygame.image.load (self.name).convert_alpha ()


class color_tile:
    #
    #  create a tile of a color
    #
    def __init__ (self, color, width, height):
        self.color = color
        self.size = (width, height)
        self.surface = pygame.Surface ((width, height))
    def load_image (self):
        return self.surface.convert_alpha ()


class image_tile:
    #
    #  image_tile - create an image_tile at point x, y
    #               with a width, height.
    #               The image_list be in the following order:
    #               [frozen, active, activated, pressed].
    #               action (tid) is called if this tile is pressed.
    #               --fixme-- do we need flush?
    #
    def __init__ (self, image_list,
                  x, y, width, height, action=None, tid=None, flush=None):
        #  the _image list must be in this order (the same as the tile_state above)
        self._images = image_list
        self._x = x
        self._y = y
        self._width = width
        self._height = height
        self._action = action
        self._getid = tid
        self._ticks = None
        mouse = pygame.mouse.get_pos ()
        if self._x+self._width > mouse[0] > self._x and self._y+self._height > mouse[1] > self._y:
            self._state = tile_activated
        else:
            self._state = tile_active
        self._flush = flush
    #
    #  select - test to see if the mouse position is over the tile and it is not frozen
    #           and if the mouse is activated call the action.
    #
    def select (self):
        if self._state != tile_frozen:
            mouse = pygame.mouse.get_pos ()
            click = pygame.mouse.get_pressed ()
            if self._x+self._width > mouse[0] > self._x and self._y+self._height > mouse[1] > self._y:
                self.set_activated ()
                if click[0] == 1:
                    self.set_pressed ()
                    if self._action != None:
                        if self._double_tap (pygame.time.get_ticks ()):
                            self._action (self._getid, 2)
                        else:
                            self._action (self._getid, 1)
    #
    #  _double_tap - return True if the tile was double tapped and remember this
    #                tap time.
    #
    def _double_tap (self, ticks):
        result = (not ((self._ticks == None) or (ticks - self._ticks > double_tap)))
        self._ticks = ticks
        return result
    #
    #  dselect - set active all unfrozen tiles.
    #
    def deselect (self):
        if self._state != tile_frozen:
            self.set_active ()
    #
    #  set_active - change the tile state to active and update if necessary
    #
    def set_active (self):
        if self._state != tile_active:
            self._state = tile_active
            self.update ()
    #
    #  set_activated - change the tile state to activated and update if necessary
    #
    def set_activated (self):
        if self._state != tile_activated:
            self._state = tile_activated
            self.update ()
    #
    #  set_frozen - change the tile state to frozen and update if necessary
    #
    def set_frozen (self):
        if self._state != tile_frozen:
            self._state = tile_frozen
            self.update ()
    #
    #  set_pressed - change the tile state to pressed and update if necessary
    #
    def set_pressed (self):
        if self._state != tile_frozen:
            self._state = tile_pressed
            self.update ()
    #
    #  update - redraw the tile.
    #
    def update (self):
        self._image_rect = self._images[self._state].load_image ().get_rect ()
        self._image_rect.center = ( (self._x+(self._width/2)), (self._y+(self._height/2)) )

        # print "update text_tile",
        pygame.draw.rect (gameDisplay, black,
                          (self._x, self._y, self._width, self._height))
        # print self._x, self._y, self._width, self._height, self._y - self._height
        gameDisplay.blit (self._images[self._state].load_image (), self._image_rect)
    #
    #  flush_display - call the callback if one is registered.
    #
    def flush_display (self):
        if not (self._flush is None):
            self._flush ()
    #
    #  set_images - set the image list to image_list.
    #
    def set_images (self, image_list):
        self._images = image_list
        self.update ()

#
#  update - redraw all tiles in forms.
#

def update (forms):
    for f in forms:
        f.update ()

#
#  select - choose a tile in forms if the mouse is hovering and invoke
#           action if the mouse button is pressed.
#

def _select (forms):
    for f in forms:
        f.select ()

#
#  dselect - set active all tiles which are not frozen.
#

def deselect (forms):
    for f in forms:
        f.deselect ()


#
#  never_finish - a dummy function used if the user does
#                 supply a finish function.
#

def never_finish ():
    return False


def wait_for_no_more_events ():
    pressed = pygame.mouse.get_pressed ()
    while pressed[0] == 1:
        event = pygame.event.wait ()
        pressed = pygame.mouse.get_pressed ()


#
#  select - redraw all tiles in forms.
#           finished is polled to see if the function should return.
#           timeout is the maximum no. of milliseconds the function
#           can poll.
#

def select (forms, event_test, finished = None, timeout = -1):
    if timeout == -1:
        blocking_select (forms, event_test, finished)
    else:
        nonblocking_select (forms, event_test, finished, timeout)


def nonblocking_select (forms, event_test, finished, timeout):
    global need_update

    if finished == None:
        finished = never_finish
    wait_for_no_more_events ()
    update (forms)
    pygame.display.update ()
    #
    #  initially select the form, as the mouse might be hovering over an existing tile.
    #
    _select (forms)
    lastTime = pygame.time.get_ticks ()
    lastBounce = None
    update (forms)
    pygame.display.update ()
    while not finished ():
        for event in pygame.event.get ():
            # event = pygame.event.wait ()
            if event_test (event):
                pass
            elif (timeout != -1) and (pygame.time.get_ticks () - lastTime > timeout):
                deselect (forms)
                _select (forms)
                update (forms)
                pygame.display.update ()
                return
            elif event.type == pygame.MOUSEBUTTONDOWN:
                deselect (forms)
                _select (forms)
                update (forms)
                pygame.display.update ()
            elif event.type == pygame.MOUSEBUTTONUP:
                deselect (forms)
                _select (forms)
                update (forms)
                pygame.display.update ()
            else:
                deselect (forms)
                _select (forms)
                update (forms)
                pygame.display.update ()
        #
        #  now check the timeout at the end of the loop
        #  to allow the user to poll with timeout = 0
        #
        if (timeout != -1) and (pygame.time.get_ticks () - lastTime > timeout):
            deselect (forms)
            _select (forms)
            update (forms)
            pygame.display.update ()
            return


def blocking_select (forms, event_test, finished):
    global need_update

    if finished == None:
        finished = never_finish
    wait_for_no_more_events ()
    update (forms)
    pygame.display.update ()
    #
    #  initially select the form, as the mouse might be hovering over an existing tile.
    #
    _select (forms)
    update (forms)
    pygame.display.update ()
    while not finished ():
        event = pygame.event.wait ()
        if event_test (event):
            pass
        elif event.type == pygame.MOUSEBUTTONDOWN:
            deselect (forms)
            _select (forms)
            update (forms)
            pygame.display.update ()
        elif event.type == pygame.MOUSEBUTTONUP:
            deselect (forms)
            _select (forms)
            update (forms)
            pygame.display.update ()
        else:
            deselect (forms)
            _select (forms)
            update (forms)
            pygame.display.update ()


def set_display (display, width, height):
    global gameDisplay, display_width, display_height
    gameDisplay = display
    display_width, display_height = width, height

def create_cache ():
    d = os.path.join (os.path.join (os.environ["HOME"], ".cache"), "touchgui")
    os.system ("mkdir -p %s" % (d))

def reset_cache ():
    d = os.path.join (os.path.join (os.environ["HOME"], ".cache"), "touchgui")
    safe_system ("rm -r %s" % (d))
    create_cache ()

# reset_cache ()
