#!/usr/bin/python3.6
# pylint: skip-file

import pygame.freetype
from collections import OrderedDict
from guielements import *
import math

# from eventrect import set_events

pygame.init()
screen_size = (1400, 859)
DONE = False

screen = pygame.display.set_mode(screen_size, flags=DOUBLEBUF)  # , flalignmentgrid1s=pygame.FULLSCREEN | pygame.DOUBLEBUF
clock = pygame.time.Clock()
ip = IconPack()
font = pygame.freetype.SysFont(pygame.freetype.get_default_font(), 24)
list1 = list()
for q in range(0, 200):
    list1.append('Contour{0}'.format(q))

img = pygame.image.load('background.jpg').convert()
img = pygame.transform.smoothscale(img, screen_size)

vrt = VirtualKeyboard()
showvrt = False


def dummy(obj, mousepos=(0, 0)):
    obj.counter += 1
    obj.text = str(obj.counter)
    pass


def new_item():
    pass


def exit_prog():
    global DONE
    DONE = True


file_menu = OrderedDict()
file_menu['File'] = (None, None)
file_menu['New'] = ('document-new', dummy)
file_menu['Open'] = ('document-open', dummy)
file_menu['Save'] = ('document-save', dummy)
file_menu['Save as..'] = ('document-save-as', dummy)
file_menu['---------'] = (None, dummy)
file_menu['Exit'] = ('exit', exit_prog)

insert_menu = OrderedDict()
insert_menu['Create'] = (None, None)
insert_menu['Contour'] = (None, dummy)
insert_menu['Tool'] = (None, dummy)
insert_menu['Block Form'] = (None, dummy)

select_menu = OrderedDict()
select_menu['Select'] = (None, None)
select_menu['Contour'] = (None, dummy)
select_menu['Tool'] = (None, dummy)
select_menu['Block Form'] = (None, dummy)

edit_menu = OrderedDict()
edit_menu['Edit'] = (None, None)
edit_menu['Copy'] = ('edit-copy', dummy)
edit_menu['Paste'] = (37, dummy)
edit_menu['Cut'] = (31, dummy)

view_menu = OrderedDict()
view_menu['View'] = (None, None)
view_menu['Zoom all'] = (350, dummy)
view_menu['Zoom out'] = (354, dummy)
view_menu['Zoom in'] = (352, dummy)
view_menu['Clip half'] = (331, dummy)
view_menu['Show rapid'] = (342, dummy)
view_menu['Select part color'] = (None, dummy)

info_menu = OrderedDict()
info_menu['Info'] = (None, None)
info_menu['About'] = (None, dummy)
info_menu['Help'] = (None, dummy)

menu = MainMenu()
# menu.set_font_name('Monoton-Regular.ttf')
menu.add_element(file_menu)
menu.add_element(edit_menu)
menu.add_element(select_menu)
menu.add_element(insert_menu)
menu.add_element(view_menu)
menu.add_element(info_menu)
menu.set_font_size(20)

alignmentgrid1 = AlignmentGrid(pygame.Rect(0, 0, screen_size[0], screen_size[1]), 30, 30)

window1 = Window('Window1', '>Grab Here 1<', pygame.Rect(100, 100, 200, 200))
window2 = Window('Window2', '>Grab Here 2<', pygame.Rect(300, 100, 200, 200))
button2 = Button('Button2', "Open", pygame.Rect(10, 190 - 32, 70, 32))
button3 = Button('Button3', 'Close', pygame.Rect(190 - 70, 190 - 32, 70, 32))

button4 = Button('Button4', "Select", pygame.Rect(10, 190 - 32, 70, 32))
button5 = Button('Button5', 'Cancel', pygame.Rect(190 - 70, 190 - 32, 70, 32))
button2.gradient_end = pygame.Color('chartreuse')
button2.gradient_start = pygame.Color('chartreuse4')
button2.roundness = 5
button3.roundness = 5

listbox2 = ListBox('listbox2', '', pygame.Rect(10, 40, 180, 100))
listbox2.add(list1)

listbox3 = ListBox('listbox3', '', pygame.Rect(10, 40, 180, 100))
listbox3.add(list1)

eventcontainer1 = EventContainer('MainScreen')
eventcontainer1.set_rectangle(pygame.Rect(0, 0, screen_size[0], screen_size[1]))
button1 = Button('Button1', 'Exit', pygame.Rect(0, 0, 32, 32))
button9 = Button('Button5', 'Hello', pygame.Rect(0, 0, 32, 32))
listbox1 = ListBox('ListBox1', '', pygame.Rect(0, 0, 0, 0))

button9.on_click = dummy

alignmentgrid1.pack_start(button1, 1, 26)
alignmentgrid1.pack_end(button1, 6, 27)
alignmentgrid1.pack_start(button9, 7, 26)
alignmentgrid1.pack_end(button9, 10, 27)

alignmentgrid1.pack_start(window1, 1, 2)
alignmentgrid1.pack_end(window1, 6, 10)

window1.grid.pack_start(button2, 1, 25)
window1.grid.pack_end(button2, 14, 29)
window1.grid.pack_start(listbox2, 1, 5)
window1.grid.pack_end(listbox2, 29, 24)
window1.grid.pack_start(button3, 16, 25)
window1.grid.pack_end(button3, 29, 29)

alignmentgrid1.pack_start(listbox1, 20, 1)
alignmentgrid1.pack_end(listbox1, 29, 29)
label1 = Label('Label1', 'Hello World', pygame.Rect(0, 0, 500, 20))
#label1.foreground_color = Color('white')
label1.shadow = True
label1.shadow_color = Color('white')


def entrybox1_keypress(obj, key):
    global label1
    label1.text = obj.text


def entrybox_on_click(obj, mousepos=(0, 0)):
    global showvrt
    # showvrt = True


entrybox1 = EntryBox('EntryBox1', 'The quick brown fox jumps over the lazy dog', pygame.Rect(10, 400, 850, 64))
entrybox1.on_keypress = entrybox1_keypress
entrybox1.on_click = entrybox_on_click
entrybox1.roundness = 10
window1.add(button2)
window1.add(button3)
window1.add(listbox2)
window1.active = True
window2.active = True

button4.flatstyle = True

window2.add(button4)
window2.add(button5)
window2.add(listbox3)

ls = listbox1.fonts
ls.sort()

alignmentgrid1.pack_start(label1, 8, 10)
alignmentgrid1.pack_end(label1, 20, 12)

drawing_area1 = DrawingArea(Rect(0, 24, 300, 300), 90, Color('grey55'), Color('grey19'))
# alignmentgrid1.pack_start(drawing_area1, 0, 1)
# alignmentgrid1.pack_end(drawing_area1, 29, 25)
drawing_area1.set_grid(20, 20)
drawing_area1.set_gradient((164, 192, 237), Color('grey19'))
drawing_area1.draw()


listbox1.add(ls)
button1.roundness = 10
eventcontainer1.add(button1)
eventcontainer1.add(button9)
eventcontainer1.add(listbox1)
eventcontainer1.add(entrybox1)
eventcontainer1.add(label1)
eventcontainer1.add(drawing_area1)


def selected_changed(obj, ind):
    global entrybox1, label1
    entrybox1.font = pygame.freetype.SysFont(listbox1.list_container[ind], 48)
    label1.font = pygame.freetype.SysFont(listbox1.list_container[ind], 48)


def on_click(obj, mousepos=(0, 0)):
    global DONE
    print('on_click event on {0}'.format(obj.name))
    DONE = True


def window1_button_onclick(obj, mousepos=(0, 0)):
    global window2, window1
    if obj.name == 'Button2':
        window2.show()
    if obj.name == 'Button3':
        window1.hide()


def window2_button_onclick(obj, mousepos=(0, 0)):
    global window2
    if obj.name == 'Button5':
        window2.hide()


button1.on_click = on_click

obj_events = {'Button1': ('on_click', on_click),
              'ListBox1': ('selected_index_changed', selected_changed)}
window1_events = {'Button2': ('on_click', window1_button_onclick),
                  'Button3': ('on_click', window1_button_onclick)}
window2_events = {'Button5': ('on_click', window2_button_onclick)}

listbox1.selected_index_changed = selected_changed

srf = Surface((2, screen_size[1]))

x = 0
y = 0
fok = 0
k = math.pi / 180
while not DONE:
    events = pygame.event.get()
    for event in events:  # User did something
        if event.type == pygame.QUIT:  # If user clicked close
            DONE = True  # Flalignmentgrid1 that we are done so we exit this loop

    # screen.fill(pygame.Color('white'))
    srf.blit(img, (0, 0), Rect(screen_size[0]-2, 0, 2, screen_size[1]))
    img.scroll(2, 0)
    img.blit(srf, (0, 0))
    screen.blit(img, (0, 0))
    #screen.blit(alignmentgrid1.render(), (alignmentgrid1.x, alignmentgrid1.y))

    if len(events) > 0:
        if showvrt:
            events = vrt.update(events)
        eventcontainer1.process(events)
        menu.update(events)

    x = math.sin(fok * k) * 10
    y = math.cos(fok * k) * 3
    fok += 3
    label1.shadow_x = x
    label1.shadow_y = y

    menu.draw()
    eventcontainer1.update()
    alignmentgrid1.update()

    screen.blit(eventcontainer1.render(), (eventcontainer1.rectangle.x, eventcontainer1.rectangle.y))
    screen.blit(menu.render(), (0, 0))
    if showvrt:
        screen.blit(vrt.render(), (vrt.x, vrt.y))

    clock.tick(60)
    pygame.display.flip()

pygame.quit()
