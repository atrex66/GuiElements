# pylint: skip-file


import numpy
from pygame import freetype
from iconpack import IconPack
from pygame import *
from eventrect import *

font.init()
freetype.init()


class GuiElements(EventRect):
    background_color = Color('snow4')
    foreground_color = Color('grey10')
    border_color = Color('grey19')
    transparent_color = Color('pink')
    # font = font.SysFont(font.get_default_font(), 24)

    def __init__(self, rectangle):
        self.updated = False
        self.font = freetype.SysFont('liberationsansnarrow', 24)
        self.font.antialiased = True
        self.font.pad = True
        self.fonts = font.get_fonts()
        super().__init__(rectangle.name, rectangle.x, rectangle.y, rectangle.width, rectangle.height)


class Button(GuiElements):
    def __init__(self, name, text, rectangle):
        ev = EventRect(name, rectangle.x, rectangle.y, rectangle.width, rectangle.height)
        super().__init__(ev)
        self.button_surface = Surface((0, 0))
        self.hover_surface = Surface((0, 0))
        self.width = ev.width
        self.height = ev.height
        self.text = text
        self.roundness = 5
        self.flatstyle = False
        self.gradient_start = Color('snow4')
        self.gradient_end = Color('white')

    def update(self):
        self.button_surface = Surface((self.width, self.height))
        if not self.flatstyle:
            mask = Surface(self.size)
            mask.fill(self.transparent_color)
            draw.rect(mask,  # surface to be drawn
                      Color('black'),  # drawing color
                      (0, 0, self.width, self.height),  # drawing rectangle
                      0,
                      self.roundness)
        else:
            self.roundness = 0
            self.gradient_start = self.background_color
            self.gradient_end = self.background_color
        gd = Surface((1, 3))
        gd.set_at((0, 0), self.gradient_start)
        gd.set_at((0, 1), self.gradient_end)
        gd.set_at((0, 2), self.gradient_start)
        gd = transform.smoothscale(gd, self.size)
        # self.button_surface.fill(self.transparent_color)
        draw.rect(self.button_surface,  # surface to be drawn
                  self.background_color,  # drawing color
                  (1, 1, self.width - 2, self.height - 2),  # drawing rectangle
                  0,
                  self.roundness)
        self.button_surface.blit(gd, (0, 0))
        if not self.flatstyle:
            self.button_surface.blit(mask, (0, 0), special_flags=BLEND_SUB)
            self.button_surface.set_colorkey(self.button_surface.get_at((0, 0)))
        draw.rect(self.button_surface,  # surface to be drawn
                  self.border_color,  # drawing color
                  (0, 0, self.width, self.height),  # drawing rectangle
                  1,
                  self.roundness)
        fnt = self.font.render(self.text, self.foreground_color)
        fx, fy = fnt[1].size
        x = self.width / 2 - fx / 2
        y = self.height / 2 - fy / 2
        fnt[0].set_colorkey(self.background_color)
        self.button_surface.blit(fnt[0], (x, y))
        self.hover_surface = Surface((self.width, self.height))
        self.hover_surface.blit(self.button_surface, (0, 0))
        draw.rect(self.hover_surface,  # surface to be drawn
                  (20, 20, 20),  # drawing color
                  (0, 0, self.width, self.height),  # drawing rectangle
                  0,
                  self.roundness)
        self.updated = True

    def render(self):
        q = Surface((self.width, self.height))
        q.fill(self.transparent_color)
        q.set_colorkey(self.transparent_color)
        q.blit(self.button_surface, (0, 0))
        if self.hover and self.pressed == 0:
            q.blit(self.hover_surface, (0, 0), special_flags=BLEND_RGBA_ADD)
        if self.pressed > 0:
            q.blit(self.hover_surface, (0, 0), special_flags=BLEND_RGBA_SUB)
        return q


class ImgButton(Button):
    def __init__(self, name, text, rectangle, img):
        super().__init__(name, text, rectangle)
        self.image = transform.smoothscale(img,
                                           (self.height - int(self.height / 2.5),
                                            self.height - int(self.height / 2.5)))
        self.image_size = self.image.get_size()
        self.font_surface = self.font.render(self.text, self.foreground_color)
        self.text_size = self.font_surface[1]
        self.button_center = (self.size[0] / 2, self.size[1] / 2)

    def update(self):
        self.image = transform.smoothscale(self.image,
                                           (self.height - int(self.height / 2.5),
                                            self.height - int(self.height / 2.5)))
        self.image_size = self.image.get_size()
        self.font_surface = self.font.render(self.text, self.foreground_color)
        self.text_size = self.font_surface[1]
        self.button_center = (self.size[0] / 2, self.size[1] / 2)

        self.button_surface = Surface((self.width, self.height))
        mask = Surface(self.size)
        mask.fill(self.transparent_color)
        draw.rect(mask,  # surface to be drawn
                  Color('black'),  # drawing color
                  (0, 0, self.width, self.height),  # drawing rectangle
                  0,
                  self.roundness)
        gd = Surface((1, 3))
        gd.set_at((0, 0), self.gradient_start)
        gd.set_at((0, 1), self.gradient_end)
        gd.set_at((0, 2), self.gradient_start)
        gd = transform.smoothscale(gd, self.size)
        draw.rect(self.button_surface,  # surface to be drawn
                  self.background_color,  # drawing color
                  (1, 1, self.width - 2, self.height - 2),  # drawing rectangle
                  0,
                  self.roundness)
        self.button_surface.blit(gd, (0, 0))
        self.button_surface.blit(mask, (0, 0), special_flags=BLEND_SUB)
        self.button_surface.set_colorkey(self.button_surface.get_at((0, 0)))
        draw.rect(self.button_surface,  # surface to be drawn
                  self.border_color,  # drawing color
                  (0, 0, self.width, self.height),  # drawing rectangle
                  1,
                  self.roundness)
        fx, fy = self.text_size.size
        ix, iy = self.image_size
        x, y = self.button_center
        xi = x - ((ix + fx) / 2)
        yi = y - (iy / 2)
        xf = xi + ix + 4
        yf = y - (fy / 2)
        self.font_surface[0].set_colorkey(self.background_color)
        self.button_surface.blit(self.image, (xi, yi))
        self.button_surface.blit(self.font_surface[0], (xf, yf))
        self.hover_surface = Surface((self.width, self.height))
        self.hover_surface.blit(self.button_surface, (0, 0))
        draw.rect(self.hover_surface,  # surface to be drawn
                  (30, 30, 30, 30),  # drawing color
                  (0, 0, self.width, self.height),  # drawing rectangle
                  0,
                  self.roundness)
        self.updated = True


class EntryBox(GuiElements):
    def __init__(self, name: str, text: str, rectangle: Rect):
        ev = EventRect(name, rectangle.x, rectangle.y, rectangle.width, rectangle.height)
        super().__init__(ev)
        self.text = text
        self.accept_keyboard_events = True
        self.has_focus = True
        self.is_focus = False
        self.on_click = None
        self.on_keypress = None
        self.cursor_pos = len(self.text)
        self.entrybox_surface = Surface((self.width, self.height))
        self.focused_surface = Surface((self.width, self.height))
        # self.focused_surface.fill(self.transparent_color)
        self.roundness = 5
        draw.rect(self.focused_surface, (10, 10, 10),
                  Rect(2, 2, self.width - 4, self.height - 4), 0, self.roundness)
        # self.focused_surface.set_colorkey((0, 0, 0))
        self.text_offset = 6
        self.blink = 0
        self.ascii_dict = {'`': '~', '1': '!', '2': '@', '3': '#', '4': '$', '5': '%', '6': '^',
                           '7': '&', '8': '*', '9': '(', '0': ')', '-': '_', '=': '+', '[': '{',
                           ']': '}', ';': ':', "'": '"', ',': '<', '.': '>', '/': '?'}

    def entryboxclick(self):
        mousepos = mouse.get_pos()
        x = mousepos[0] - self.x
        y = mousepos[1] - self.y
        obx = 0
        t = self.text + " "
        for i in range(0, len(t)):
            fnt1 = self.font.render(t[:i], self.foreground_color)
            ox = fnt1[1].width + self.text_offset
            if ox >= x >= obx:
                self.cursor_pos = i - 1
                return None
            obx = ox
        self.cursor_pos = len(self.text)
        self.updated = True
        if self.on_click is not None:
            self.on_click(self)

    def process(self, events):
        # ha nincs fokusz ne hajtodjon vegre az interruptok feldolgozasa
        if not self.is_focus:
            return None
        for event in events:
            if event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    self.entryboxclick()
            if event.type == KEYDOWN:
                self.updated = False
                kn = key.name(event.key)
                if len(kn) > 1:
                    kn = kn.replace('[', '')
                    kn = kn.replace(']', '')
                if kn == 'space':
                    kn = ' '
                if kn == 'left':
                    if self.cursor_pos > 0:
                        self.cursor_pos -= 1
                if kn == 'right':
                    if self.cursor_pos < len(self.text):
                        self.cursor_pos += 1
                if kn == 'end':
                    self.cursor_pos = len(self.text)
                if kn == 'home':
                    self.cursor_pos = 0
                if kn == 'backspace':
                    if self.cursor_pos > 0:
                        self.text = self.text[:self.cursor_pos - 1] + self.text[self.cursor_pos:]
                        self.cursor_pos -= 1
                if kn == 'delete':
                    if self.cursor_pos < len(self.text):
                        self.text = self.text[:self.cursor_pos] + self.text[self.cursor_pos + 1:]
                if key.get_mods() & KMOD_LSHIFT or key.get_mods() & KMOD_RSHIFT:
                    if kn in self.ascii_dict.keys():
                        kn = self.ascii_dict[kn]
                    else:
                        kn = kn.upper()
                if len(kn) == 1:
                    if self.cursor_pos == len(self.text):
                        self.text += kn
                        self.cursor_pos = len(self.text)
                    else:
                        self.text = self.text[:self.cursor_pos] + kn + self.text[self.cursor_pos:]
                        self.cursor_pos += 1
                if self.on_keypress is not None:
                    self.on_keypress(self, kn)

    def update(self):
        self.blink += 1
        if self.blink > 30:
            self.blink = 0
        self.draw()
        self.updated = True

    def draw(self):
        txt = self.font.render(self.text, self.foreground_color)
        # self.entrybox_surface.fill(self.background_color)
        draw.rect(self.entrybox_surface, self.background_color,
                  Rect(1, 1, self.width - 2, self.height - 2), 0, self.roundness)
        draw.rect(self.entrybox_surface, self.foreground_color,
                  Rect(0, 0, self.width, self.height), 1, self.roundness)
        self.entrybox_surface.blit(txt[0], (self.text_offset, self.height / 2 - txt[1].height / 2))

    def render(self):
        temp_surface = Surface((self.entrybox_surface.get_size()))
        temp_surface.blit(self.entrybox_surface, (0, 0))
        s = self.font.render(self.text[:self.cursor_pos])
        x = s[0].get_size()[0]
        if self.is_focus:
            if self.blink < 15:
                draw.rect(temp_surface, Color('white'),
                          Rect(x + self.text_offset, 4, 1, self.height - 8),
                          0, self.roundness)
            temp_surface.blit(self.focused_surface, (0, 0), special_flags=BLEND_ADD)
        return temp_surface


class ListBox(GuiElements):
    def __init__(self, name, text, rectangle):
        ev = EventRect(name, rectangle.x, rectangle.y, rectangle.width, rectangle.height)
        super().__init__(ev)
        self.__list_position = 0
        self.list_container = list()
        self.__select_rectangle = Rect(0, 0, 0, 0)
        self.scrollable = True
        self.__listbox_surface = Surface(self.size)
        self.__list_surface = Surface((0, 0))
        self.text = text
        self.__selected_index = -1
        self.selected_index_changed = self.dummy
        self.on_click = self.click
        self.on_keypress = self.keypress
        self.update()

    def dummy(self, obj, ind):
        pass

    def keypress(self, obj, key):
        print(key)
        pass

    def click(self, obj, mousepos=(0, 0)):
        fy = self.font.get_sized_height()
        relpos_y = mousepos[1] - self.y
        oszto = fy
        rect_y = int(relpos_y / oszto)
        pos = (relpos_y / oszto) - (self.__list_position / oszto)
        if 0 <= pos:
            if pos <= len(self.list_container):
                self.__selected_index = int(pos)
                self.__select_rectangle = Rect(0, rect_y * fy, self.width, fy)
        else:
            self.__selected_index = -1
            self.__select_rectangle = Rect(0, 0, 0, 0)
        self.selected_index_changed(self, self.__selected_index)
        self.updated = False

    def add(self, text):
        if type(text) != list:
            self.list_container.append(text)
        else:
            for k in text:
                self.list_container.append(k)
        self.update()

    def scroll(self, buttons, mousepos=(0, 0)):
        fy = self.font.get_sized_height()
        if buttons == 5:
            if self.__list_position > self.height - (len(self.list_container) * fy):
                self.__list_position -= fy
        if buttons == 4:
            if self.__list_position < 0:
                self.__list_position += fy
        self.__selected_index = -1
        self.__select_rectangle = Rect(0, 0, 0, 0)
        self.updated = False

    def update(self):
        self.__listbox_surface = Surface(self.size)
        fy = self.font.get_sized_height()
        self.__list_surface = Surface((self.width,
                                       len(self.list_container) * fy))
        self.__list_surface.fill(self.background_color)
        self.__list_surface.set_colorkey(self.transparent_color)
        q = 0
        for i in self.list_container:
            fs = self.font.render(i, self.foreground_color)
            a = self.font.get_sized_height()
            self.__list_surface.blit(fs[0], (5, (a * q)))
            q += 1
        self.__listbox_surface = Surface((self.width, self.height))
        self.__listbox_surface.fill(self.background_color)
        self.__listbox_surface.set_colorkey(self.transparent_color)
        self.__listbox_surface.blit(self.__list_surface, (1, self.__list_position))
        draw.rect(self.__listbox_surface, self.border_color, (0, 0, self.width, self.height), 1)
        s = Surface((self.__select_rectangle.width, self.__select_rectangle.height))
        s.fill((30, 70, 100))
        self.__listbox_surface.blit(s, (0, self.__select_rectangle.y), special_flags=BLEND_RGBA_ADD)
        draw.rect(self.__listbox_surface, self.border_color, self.__select_rectangle, 1)
        self.updated = True

    def render(self):
        return self.__listbox_surface


class AlignmentGrid(Rect):
    def __init__(self, rectangle, columns, rows):
        super().__init__(rectangle.x, rectangle.y, rectangle.width, rectangle.height)
        self.columns = list()
        self.rows = list()
        self.alignmentgrid_surface = Surface(self.size)
        for i in numpy.arange(0, self.width, self.width / columns):
            self.columns.append(int(i))
        self.columns.append(self.width)
        for i in numpy.arange(0, self.height, self.height / rows):
            self.rows.append(int(i))
        self.rows.append(self.height)
        self.draw_grid = False
        pass

    def pack_to(self, obj):
        self.columns = list()
        self.rows = list()
        for i in numpy.arange(0, obj.width, obj.width / self.columns):
            self.columns.append(int(i))
        self.columns.append(obj.width)
        for i in numpy.arange(0, obj.height, obj.height / self.rows):
            self.rows.append(int(i))
        self.rows.append(obj.height)
        pass

    def pack_start(self, obj, column, row):
        obj.x = self.columns[column]
        obj.y = self.rows[row]
        if hasattr(obj, 'draw'):
            obj.draw()

    def pack_end(self, obj, column, row):
        obj.width = self.columns[column] - obj.x
        obj.height = self.rows[row] - obj.y
        if hasattr(obj, 'draw'):
            obj.draw()

    def update(self):
        if self.draw_grid:
            self.alignmentgrid_surface.fill(Color('black'))
            self.alignmentgrid_surface.set_alpha(10)
            for i in self.columns:
                draw.line(self.alignmentgrid_surface, Color('white'), (i, 0), (i, self.height), 1)
            for i in self.rows:
                draw.line(self.alignmentgrid_surface, Color('white'), (0, i), (self.width, i), 1)
            self.alignmentgrid_surface.set_alpha(30)
        return None

    def render(self):
        return self.alignmentgrid_surface


class Window(GuiElements):
    def __init__(self, name, text, rectangle):
        ev = EventRect(name, rectangle.x, rectangle.y, rectangle.width, rectangle.height)
        super().__init__(ev)
        self.__window_surface = Surface(self.size)
        self.objects = EventContainer(name)
        self.name = name
        self.objects.has_focus = True  # make sure keyboard events grab when in focus
        self.objects.is_focus = False
        self.has_focus = True
        self.is_focus = False
        self.active = False
        self.text = text
        self.grid = AlignmentGrid(Rect(self.x, self.y, self.width, self.height), 30, 30)
        self.eltol = self.font.get_sized_height() + 4
        self.movearea = EventRect('WindowBar', 0, 0, self.width, self.eltol)
        self.window_area = EventRect('WindowArea', 0, 0, self.width, self.height)
        self.movearea.on_mouse_move = self.windowbar_mouse_move
        self.window_area.on_click = self.windowclick
        self.objects.add(self.movearea)
        self.objects.add(self.window_area)
        self.update()

    def show(self):
        self.active = True
        self.is_focus = True
        self.movearea = EventRect('WindowBar', 0, 0, self.width, self.eltol)
        self.window_area = EventRect('WindowArea', 0, 0, self.width, self.height)

    def hide(self):
        self.active = False
        self.is_focus = False

    def windowclick(self, obj, mousepos=(0, 0)):
        # self.is_focus = True
        return None

    def windowbar_mouse_move(self, obj, event):
        mb = mouse.get_pressed(3)
        if mb[0] == 1:
            self.move_ip(event.rel)
            # self.draw()

    def add(self, obj):
        self.objects.add(obj)

    def process(self, events):
        if self.active:
            self.objects.process(events, rel=self)

    def draw(self):
        self.grid = AlignmentGrid(Rect(self.x, self.y, self.width, self.height), 30, 30)
        self.__window_surface = Surface((self.width, self.height))
        self.movearea = EventRect('WindowBar', 0, 0, self.width, self.eltol)
        self.window_area = EventRect('WindowArea', 0, 0, self.width, self.height)

        self.__window_surface.fill(self.background_color)
        for i in self.objects.ev_objects:
            if hasattr(i, 'render'):
                self.__window_surface.blit(i.render(), (i.x, i.y))
        draw.rect(self.__window_surface, self.border_color, (1, 1, self.width - 2, self.eltol))
        draw.rect(self.__window_surface, self.border_color, (0, 0, self.width, self.height), 1)
        q = self.font.render(self.text, self.background_color)
        x = self.width / 2 - q[1].width / 2
        y = self.eltol / 2 - q[1].height / 2
        self.__window_surface.blit(q[0], (x, y))
        if not self.is_focus:
            darken = Surface(self.__window_surface.get_size())
            darken.fill((0, 0, 0))
            darken.set_alpha(120)
            self.__window_surface.blit(darken, (0, 0))

    def update(self):
        self.objects.update()
        # for i in self.objects.ev_objects:
        #    if hasattr(i, 'update'):
        #        i.update()

    def render(self):
        self.draw()
        if self.active:
            return self.__window_surface
        return Surface((0, 0))


class Label(GuiElements):
    def __init__(self, name, text, rectangle):
        ev = EventRect(name, rectangle.x, rectangle.y, rectangle.width, rectangle.height)
        super().__init__(ev)
        self.x = rectangle.x
        self.y = rectangle.y
        self.width = rectangle.width
        self.height = rectangle.height
        self.name = name
        self.text = text
        self.shadow = False
        self.shadow_color = Color('black')
        self.shadow_x = 2
        self.shadow_y = 2
        # self.font.antialiased = False
        self.label_surface = Surface((self.width, self.height))

    def update(self):
        self.draw()

    def draw(self):
        surface = display.get_surface()
        self.label_surface = Surface(self.get_rect().size)
        self.label_surface.blit(surface, (0, 0), Rect(self.x, self.y, self.width, self.height))
        # self.label_surface.set_colorkey(self.transparent_color)
        tex = self.font.render(self.text, self.foreground_color)
        tx = tex[1].width
        ty = tex[1].height
        fx, fy = self.label_surface.get_size()
        x = fx / 2 - tx / 2
        y = fy / 2 - ty / 2
        if self.shadow:
            q = self.font.render(self.text, self.shadow_color)
            q[0].set_alpha(128)
            self.label_surface.blit(q[0], (x + self.shadow_x, y + self.shadow_y))
        self.font.render_to(self.label_surface, (x, y), self.text, self.foreground_color)

    def render(self):
        return self.label_surface


class MainMenu(GuiElements):
    """
    Menu object with on_click events,
    Usage:
    file_menu = OrderedDict()
    file_menu['File'] = (None, None)  # this element is defining the root menu
    file_menu['New'] = (IconName, Function to call)
    file_menu['Open'] = (IconName, Function to call)
    file_menu['Save'] = (IconName, Function to call)
    file_menu['Save as..'] = (IconName, Function to call)
    file_menu['---------'] = (None, dummy function make nothing)
    file_menu['Exit'] = (IconName, Function)
    menu = MainMenu()
    menu.add_element(file_menu)
    menu.add_element(other_menu)
    menu.add_element(another_menu)

    In the main loop:
        menu.update(events)
        menu.draw()
        menu.blit(screen, (menu.x, menu.y)

    """
    def __init__(self):
        self.menu = []
        self.menu_surface = []
        self.sub_surfaces = []
        self.menu_rectangles = []
        # self.font = []
        self.margin = 8
        self.vertical_space = 2
        self.space = 10
        self.scrn_size = []
        self.fontsize = 32
        self.iconpack = []
        self.active_menu = 0
        self.topline_rect = Rect(0, 0, 0, 0)
        self.print_once = 0
        self.selected_root = -1
        self.selected_sub = -1
        self.sub_rectangles = []
        self.selected_sub_item = 0
        self.selected_sub_rect = Rect(0, 0, 0, 0)
        self.topline_surface = []
        self.active = True
        self.iconpack = IconPack()
        self.scrn_size = display.get_surface().get_size()
        super().__init__(EventRect('MainMenu', 0, 0, self.scrn_size[0], self.scrn_size[1]))
        self.menu_surface = Surface((self.scrn_size[0], self.scrn_size[1] / 2))
        self.set_font_size(16)
        self.font.antialiased = True

    def get_rect(self):
        a = list()
        a.append(self.topline_rect)
        a.append(self.sub_rectangles)
        return a

    def add_element(self, element):
        """

        :param element: menu element to display
        """
        self.menu.append(element)

    def set_colors(self, background=Color(0x68, 0x68, 0x68),
                   fore_color=Color(0xff, 0xff, 0xff),
                   border_color=Color(0x20, 0x20, 0x20)):
        self.bckgnd = background
        self.frgnd = fore_color
        self.brdrc = border_color

    def set_font_size(self, size):
        self.fontsize = size
        self.topline_rect = Rect(0, 0, self.scrn_size[0], self.fontsize + (self.vertical_space * 2))
        self.topline_surface = Surface(self.topline_rect.size)
        self.render()

    def render(self):
        draw.rect(self.topline_surface, self.background_color, self.topline_rect)
        draw.rect(self.topline_surface, self.border_color, self.topline_rect, 1)
        self.sub_surfaces = []
        self.sub_rectangles = []
        self.menu_rectangles = []
        menu_rct = []
        ti = self.margin
        for i in self.menu:
            frct = self.font.render_to(self.topline_surface,
                                       (ti, 0),
                                       list(i.keys())[0],
                                       self.foreground_color,
                                       None,
                                       size=self.fontsize)
            frct.x = ti
            frct.y = 0
            menu_rct.append(frct)
            ti += frct.width + (self.margin * 2)
            mxlength = 0
            fg = list(i.keys())[1:]
            for j in fg:
                k = self.font.get_rect(j, size=self.fontsize)
                st = j
                if k.width > mxlength:
                    mxlength = k.width
            k = self.font.get_rect(st, size=self.fontsize)
            sze = (mxlength + (self.margin * 3) + self.fontsize,
                   (k.height * len(fg)) + self.vertical_space)
            p = Surface(sze)
            p.fill(self.background_color)
            q = 0
            sub_rct = []
            for j in fg:
                k = self.font.get_rect(j, size=self.fontsize)
                if j != '-':
                    frct = self.font.render_to(p,
                                               ((self.margin * 2) + self.fontsize, q * k.height),
                                               j,
                                               self.foreground_color, None, size=self.fontsize)
                    frct.x, frct.y = ((self.margin * 2) + self.fontsize, q * k.height)
                    sub_rct.append(frct)
                else:
                    draw.line(p, self.border_color,
                              (self.margin, (q * k.height) + (k.height / 2)),
                              (p.get_rect().width - self.margin,
                               (q * k.height) + (k.height / 2)), 2)
                idx = i[j][0]
                if idx is not None:
                    icon = self.iconpack.get_icon(idx)
                    trans = transform.smoothscale(icon, (self.fontsize, self.fontsize))
                    p.blit(trans, (self.margin, q * k.height + (self.vertical_space * 1.5)))
                q += 1
            self.sub_rectangles.append(sub_rct)
            self.sub_surfaces.append(p)
            self.menu_rectangles.append(menu_rct)
            menu_rct = []
        return self.menu_surface

    def update(self, events):
        q = 0
        collided = -1
        mousepos = mouse.get_pos()
        # if mouse positoin is not collide with toplevel menu or submenus reset the selection
        if not self.topline_rect.collidepoint(mousepos) and not self.selected_sub_rect.collidepoint(mousepos):
            self.selected_root = -1
            self.selected_sub_item = -1
        for i in events:
            if i.type == MOUSEBUTTONDOWN:
                if i.button == 1 and self.selected_sub_rect.collidepoint(mousepos):
                    try:
                        root = list(self.menu[self.selected_root].keys())
                        k = self.menu[self.selected_root][root[self.selected_sub_item + 1]][1]
                        k()
                    except (KeyError, TypeError):
                        print("Exception!")
                        print(root)
                        print(root[self.selected_sub_item + 1])
                        pass

        scan_rect = self.sub_rectangles[self.selected_root]
        if self.selected_sub_rect.collidepoint(mousepos):
            x, y = self.selected_sub_rect.topleft
            q = 0
            for i in self.sub_rectangles[self.selected_root]:
                a = i.x + x
                b = i.y + y
                temp = i.copy()
                temp.x = a
                temp.y = b
                if temp.collidepoint(mousepos):
                    self.selected_sub_item = q
                q += 1
        # scan for the selected menu
        for i in self.menu_rectangles:
            if i[0].collidepoint(mousepos):
                collided = q
            q += 1
        # store the 'new' selection
        if self.topline_rect.collidepoint(mousepos):
            if collided != -1:
                self.selected_root = collided
        # return 1 when selection to indicate mouse handled
        if self.selected_root != -1:
            return 1
        else:
            return 0

    def draw(self, surface=Surface):
        # set transparency of the menu
        self.menu_surface.fill(self.transparent_color)
        self.menu_surface.set_colorkey(self.transparent_color)
        # one time render for menu surfaces creation
        if self.print_once == 0:
            self.render()
            self.print_once = 1
        # blit topline menu to menu surface
        self.menu_surface.blit(self.topline_surface, (0, 0))
        q = 0
        for k in self.sub_surfaces:
            if self.selected_root == q:
                draw.rect(k, self.border_color, k.get_rect(), 1)
                self.selected_sub_rect = self.menu_surface.blit(k,
                                                                (self.menu_rectangles[q][0].x,
                                                                 self.fontsize + (self.vertical_space * 2)))
            q += 1
        try:
            if self.selected_sub_item != -1:
                root_xy = self.menu_rectangles[self.selected_root][0].bottomleft
                subsurface_width = self.sub_surfaces[self.selected_root].get_rect().width
                px = root_xy[0]
                py = root_xy[1] + self.sub_rectangles[self.selected_root][self.selected_sub_item].y
                sub_height = self.sub_rectangles[self.selected_root][self.selected_sub_item].size[1]
                temp_surf = Surface((subsurface_width, sub_height))
                temp_surf.fill(self.border_color)
                self.menu_surface.blit(temp_surf, (px, py), special_flags=BLEND_ADD)
        except IndexError:
            print("Exception!")
            print(self.selected_root, self.selected_sub_item)
            print(self.sub_rectangles)
            pass


class VirtualKeyboard(GuiElements):
    def __init__(self):
        self.image = image.load('data/virtualkeyboard.png')
        self.keyboard_surface = Surface(self.image.get_size())
        sfax = display.get_surface()
        swidth, sheight = sfax.get_size()
        width, height = self.keyboard_surface.get_size()
        x = swidth / 2 - width / 2
        y = sheight - height
        super().__init__(EventRect('virtual_keyboard', x, y, width, height))
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.keys_position = ((9, 71), (89, 71), (169, 71), (249, 71), (329, 71), (409, 71),
                              (489, 71), (569, 71), (649, 71), (729, 71),
                              (49, 136), (129, 136), (209, 136), (289, 136), (369, 136), (449, 136),
                              (529, 136), (609, 136), (689, 136), (89, 201), (169, 201), (249, 201),
                              (329, 201), (409, 201), (489, 201), (569, 201), (649, 201), (729, 201),
                              (569, 271), (649, 271), (729, 271))
        self.keys_size = (72, 57)
        self.keys = "qwertyuiopasdfghjklzxcvbnm,.   "
        self.keys_shifted = "QWERTYUIOPASDFGHJKLZXCVBNM<>   "
        self.keys_symbols = "1234567890~!@#%&*()-+*/=[]{}   "
        self.keys_shift = (Rect(9, 144, 72, 57), Rect(809, 144, 97, 57))
        self.backspace = Rect(809, 14, 97, 57)
        self.enter = Rect(769, 79, 137, 57)
        self.switch = Rect(9, 214, 152, 57)
        self.hide = Rect(809, 214, 97, 57)
        self.font = freetype.SysFont('freesans', 36)
        self.rectagle = Rect(0, 0, 0, 0)
        self.font.antialiased = True
        self.font.pad = False
        self.ev_objects = EventContainer('VirtualKeys')
        self.keyboard_surface.fill(self.background_color)
        self.keyboard_surface.blit(self.image, (0, 0))
        self.has_focus = False
        self.event_list = list()
        self.myevent = None
        q = 0
        fx = self.keys_size[0]
        fy = self.keys_size[1]
        keys = self.keys
        for i in self.keys_position:
            char = self.font.render(keys[q], self.foreground_color)
            pos = Rect(i[0], i[1] - fy, fx, fy).center
            x = pos[0] - char[1][2] / 2
            y = pos[1] - char[1][3] / 2
            self.font.render_to(self.keyboard_surface, (x, y), keys[q], self.foreground_color)
            ev = EventRect(keys[q], i[0], i[1] - fy, fx, fy)
            ev.counter = (ord(self.keys[q]), ord(self.keys_shifted[q]), ord(self.keys_symbols[q]))
            ev.on_click = self.keys_on_click
            self.ev_objects.add(ev)
            q += 1
        pos = self.backspace
        ev = EventRect('backspace', pos.x, pos.y, pos.width, pos.height)
        ev.on_click = self.keys_on_click
        self.ev_objects.add(ev)
        pos = self.enter
        ev = EventRect('enter', pos.x, pos.y, pos.width, pos.height)
        ev.on_click = self.keys_on_click
        self.ev_objects.add(ev)
        pos = self.switch
        ev = EventRect('switch', pos.x, pos.y, pos.width, pos.height)
        ev.on_click = self.keys_on_click
        self.ev_objects.add(ev)
        pos = self.keys_shift[0]
        ev = EventRect('shift', pos.x, pos.y, pos.width, pos.height)
        ev.on_click = self.keys_on_click
        self.ev_objects.add(ev)
        pos = self.keys_shift[1]
        ev = EventRect('shift', pos.x, pos.y, pos.width, pos.height)
        ev.on_click = self.keys_on_click
        self.ev_objects.add(ev)
        self.ctr = 0
        self.shifted = False
        self.strect = None

    def keys_on_click(self, obj, mousepos=(0, 0)):
        self.pressed = 10
        if obj.name == 'shift' and not self.shifted:
            if self.ctr != 2:
                self.strect = self.keys_shift[0]
                self.shifted = True
                self.ctr = 1
        if obj.name == 'switch':
            if self.ctr != 2:
                self.strect = self.switch
                self.ctr = 2
            else:
                self.ctr = 0
        if len(obj.name) == 1:
            self.myevent = {'key': obj.counter[self.ctr]}
            e = event.Event(KEYDOWN, self.myevent)
            self.myevent = e
            self.strect = obj.rectangle
            if self.shifted:
                self.shifted = False
                self.strect = None
                self.ctr = 0
        if obj.name == 'enter':
            self.myevent = {'key': K_RETURN}
            e = event.Event(KEYDOWN, self.myevent)
            self.myevent = e
            self.strect = self.enter
        if obj.name == 'backspace':
            self.myevent = {'key': K_BACKSPACE}
            e = event.Event(KEYDOWN, self.myevent)
            self.strect = self.backspace
            self.myevent = e

    def draw(self):
        self.keyboard_surface = Surface(self.image.get_size())
        self.keyboard_surface.fill(self.background_color)
        self.keyboard_surface.blit(self.image, (0, 0))
        fx = self.keys_size[0]
        fy = self.keys_size[1]
        for k in range(0, len(self.keys)):
            i = self.keys_position[k]
            j = self.ev_objects.ev_objects[k]
            char = self.font.render(chr(j.counter[self.ctr]), self.foreground_color)
            pos = Rect(i[0], i[1] - fy, fx, fy).center
            x = pos[0] - char[1][2] / 2
            y = pos[1] - char[1][3] / 2
            self.font.render_to(self.keyboard_surface, (x, y), chr(j.counter[self.ctr]), self.foreground_color)
        if self.strect is not None and self.pressed > 0:
            s = Surface((self.strect.width, self.strect.height))
            s.fill(Color('black'))
            s.set_alpha(128)
            self.keyboard_surface.blit(s, (self.strect.x, self.strect.y))
            self.pressed -= 1

    def update(self, events):
        self.ev_objects.process(events, rel=self)
        newev = list()
        for i in events:
            if i.type == MOUSEBUTTONDOWN:
                if i.button != 0:
                    if not self.collidepoint(i.pos):
                        newev.append(i)
            else:
                newev.append(i)
        if self.myevent is not None:
            newev.append(self.myevent)
            self.myevent = None
        return newev

    def render(self):
        self.draw()
        return self.keyboard_surface


class DrawingArea(Surface):
    def __init__(self, rectngle: Rect, angle, bckgnd, brdr):
        self.x = rectngle.x
        self.y = rectngle.y
        self.width = rectngle.width
        self.height = rectngle.height
        self.rectangle = Rect(self.x, self.y, self.width, self.height)
        self.angle = angle
        super().__init__((self.width, self.height))
        self.gradient = None
        self.draw_surface = self
        self.border_color = brdr
        self.background_color = bckgnd
        self.clear()
        self.enter = None
        self.on_mouse_leave = self.mouse_leave
        self.on_mouse_enter = self.mouse_enter
        self.on_mouse_move = None
        self.on_click = None
        self.pressed = 0
        self.name = 'DrawingArea'
        self.gridx = 0
        self.gridy = 0
        self.draw()

    def mouse_enter(self, obj):
        mouse.set_system_cursor(SYSTEM_CURSOR_CROSSHAIR)
        pass

    def mouse_leave(self, obj):
        mouse.set_system_cursor(SYSTEM_CURSOR_ARROW)
        pass

    def collidepoint(self, point):
        return self.rectangle.collidepoint(point)

    def map_mouse(self, mousepos):
        x = mousepos[0] - self.x
        y = mousepos[1] - self.y
        return x, y

    def set_grid(self, x, y):
        self.gridx = x
        self.gridy = y

    def update(self):
        pass

    def set_gradient(self, grad_start, grad_end):
        s = Surface((2, 1))
        s.set_at((1, 0), grad_start)
        s.set_at((0, 0), grad_end)
        self.gradient = transform.smoothscale(s, (self.width, self.height))

    def draw(self):
        self.clear()
        if self.gridy > 0 and self.gridx > 0:
            for i in range(0, self.width, self.gridx):
                for j in range(0, self.height, self.gridy):
                    draw.line(self.draw_surface, self.border_color, (i, j), (i, j), 1)

    def clear(self):
        if self.gradient is None:
            self.draw_surface.fill(self.background_color)
        else:
            self.draw_surface.blit(self.gradient, (0, 0))
        draw.rect(self.draw_surface, self.border_color, Rect(0, 0, self.width, self.height), 2)

    def render(self):
        b = transform.rotate(self.draw_surface, self.angle)
        self.width, self.height = b.get_size()
        self.rectangle = Rect(self.x, self.y, self.width, self.height)
        return b
