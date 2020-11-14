#!/usr/bin/python3.6
#pylint: skip-file

import operator
from pygame import *
import guielements


class EventRect(Rect):

    def __init__(self, name, x, y, w, h):
        self.name = name
        self.pressed = 0
        self.hover = False
        self.on_click = None
        self.on_mouse_enter = None
        self.on_mouse_leave = None
        self.on_mouse_move = None
        self.mouse_over = False
        self.scrollable = False
        self.enter = False
        self.counter = 0
        self.mouse_lock = False
        self.updated = True
        self.rectangle = Rect(x, y, w, h)
        super().__init__(x, y, w, h)

    def set_on_click(self, funct):
        self.on_click = funct

    def set_on_enter(self, funct):
        self.on_mouse_enter = funct

    def set_on_leave(self, funct):
        self.on_mouse_leave = funct

    def set_on_move(self, funct):
        self.on_mouse_move = funct

    def set_events_target(self, oc, oe, ol, om):
        self.on_click = oc
        self.on_mouse_enter = oe
        self.on_mouse_leave = ol
        self.on_mouse_move = om

    def get_rect(self):
        return Rect(self.x, self.y, self.width, self.height)


class EventContainer:
    def __init__(self, name):
        self.names = list()
        self.name = name
        self.evc_surface = Surface((0, 0))
        self.has_focus = False
        self.is_focus = False
        self.focused = None
        self.rectangle = ()
        self.ev_objects = []
        self.names = []

    def set_focused(self, obj):
        obj.is_focus = True
        self.focused = obj

    def drop_focused(self, obj):
        obj.is_focus = False
        self.focused = None

    def add(self, obj):
        self.names.append(obj.name)
        self.ev_objects.append(obj)

    def get_object_by(self, name=None, index=None):
        if name is not None:
            return self.ev_objects[self.names.index(name)]
        if index is not None:
            return self.ev_objects[index]
        return None

    def index(self, name):
        return self.names.index(name)

    def process(self, events: list, rel=None):
        mp = mouse.get_pos()
        if rel is not None:
            x, y = mp
            x -= rel.x
            y -= rel.y
            mp = (x, y)
        skip = False
        if self.focused is not None:
            if not self.focused.collidepoint(mp):
                for k in events:
                    if k.type == MOUSEBUTTONDOWN:
                        if k.button == 1:
                            self.drop_focused(self.focused)
                            skip = True
            if not skip:
                self.focused.process(events)
                return None
        for k in events:
            for i in self.ev_objects:
                if i.collidepoint(mp):
                    i.updated = False
                    if not i.enter:
                        if i.on_mouse_enter is not None:
                            i.on_mouse_enter(i)
                    if k.type == MOUSEBUTTONDOWN:
                        if k.button == 1:
                            if hasattr(i, 'has_focus'):
                                self.set_focused(i)
                            if i.on_click is not None:
                                i.on_click(i, mousepos=mp)
                            i.pressed = 10
                        if k.button == 4 or k.button == 5:
                            if i.scrollable:
                                i.scroll(k.button, mousepos=mp)
                    if k.type == MOUSEMOTION:
                        if i.on_mouse_move is not None:
                            i.on_mouse_move(i, event=k)
                        i.hover = True
                    if k.type == KEYDOWN:
                        if hasattr(i, 'on_keypress'):
                            if i.on_keypress is not None:
                                i.on_keypress(i, k.key)
                    i.enter = True
                    i.mouse_over = True
                else:
                    if i.enter and i.on_mouse_leave is not None:
                        i.on_mouse_leave(i)
                    i.enter = False
                    i.mouse_over = False
                    i.hover = False

    def update(self):
        cover = list()
        for i in self.ev_objects:
            cover.append(Rect(i.x, i.y, i.width, i.height))
            self.rectangle = Rect(0, 0, 0, 0).unionall(cover)
            if hasattr(i, 'update'):
                i.update()
            if i.pressed > 0:
                i.pressed -= 1
        # utoljara rajzoljuk a fokuszalt elemet hogy legfelul legyen
        self.evc_surface = Surface((self.rectangle.width, self.rectangle.height))
        self.evc_surface.set_colorkey(self.evc_surface.get_at((0, 0)))
        for i in self.ev_objects:
            if i is not self.focused:
                if hasattr(i, 'render'):
                    self.evc_surface.blit(i.render(), (i.x, i.y))
        if self.focused is not None:
            self.evc_surface.blit(self.focused.render(), (self.focused.x, self.focused.y))
        #draw.rect(self.evc_surface, Color('red'), self.rectangle, 1)

    def set_rectangle(self, rect):
        self.rectangle = rect

    def render(self):
        return self.evc_surface
