import pyglet as pg
from pyglet.window import key
from Vector2D import Vector2D
from Car import Car
from Wall import Wall
from statistics import mean, median

window = pg.window.Window(1280, 720, resizable=True)
label = pg.text.Label('Hello World', font_name='Times New Roman',
                      font_size=36, x=window.width // 2, y=window.height // 2, anchor_x='center', anchor_y='center')

player = Car((10, 20), (128, 128, 255), (193, 296))
walls = [Wall((167, 277), (173, 392)), Wall((173, 392), (205, 479)), Wall((205, 479), (297, 534)), Wall((297, 534), (427, 541)), Wall((427, 541), (557, 522)), Wall((557, 522), (559, 452)), Wall((559, 452), (461, 364)), Wall((461, 364), (459, 332)), Wall((459, 332), (491, 316)), Wall((491, 316), (568, 352)), Wall((568, 352), (712, 391)), Wall((712, 391), (825, 375)), Wall((825, 375), (876, 306)), Wall((876, 306), (879, 228)), Wall((879, 228), (789, 159)), Wall((789, 159), (635, 119)), Wall((635, 119), (361, 98)), Wall((361, 98), (224, 112)), Wall((224, 112), (192, 171)), Wall((192, 171), (167, 277)), Wall((219, 280), (223, 349)), Wall((223, 349), (229, 404)), Wall((229, 404), (243, 450)), Wall((243, 450), (309, 476)), Wall((309, 476), (375, 483)), Wall((375, 483), (433, 485)), Wall((433, 485), (486, 476)), Wall((486, 476), (438, 429)), Wall((438, 429), (408, 382)), Wall((408, 382), (399, 315)), Wall((399, 315), (432, 286)), Wall((432, 286), (488, 267)), Wall((488, 267), (571, 297)), Wall((571, 297), (660, 327)), Wall((660, 327), (751, 335)), Wall((751, 335), (796, 319)), Wall((796, 319), (822, 268)), Wall((822, 268), (798, 228)), Wall((798, 228), (698, 185)), Wall((698, 185), (598, 164)), Wall((598, 164), (476, 151)), Wall((476, 151), (359, 144)), Wall((359, 144), (255, 158)), Wall((255, 158), (221, 252)), Wall((221, 252), (219, 280))]
times = []

is_wall_building = False
if is_wall_building:
    last = walls[-1].b

keys_pressed = {key.W: False, key.A: False, key.S: False, key.D: False}
last_keys = keys_pressed.copy()


@window.event
def on_draw():
    window.clear()
    player.draw()
    for w in walls:
        w.draw()


@window.event
def on_key_press(symbol, modifiers):
    keys_pressed[symbol] = True
    if is_wall_building:
        if symbol == 32:  # space
            for w in walls:
                print(str(w) + ", ", end='')
    else:
        if symbol == 32:  # space
            global player
            player = Car((10, 20), (128, 128, 255), (193, 296))


@window.event
def on_key_release(symbol, modifiers):
    keys_pressed[symbol] = False


@window.event
def on_mouse_press(x, y, button, modifiers):
    if is_wall_building:
        global last, walls
        if button == 1:
            v = Vector2D(x, y)
            walls.append(Wall(last.tuple(), v.tuple()))
            last = v
        elif button == 4:
            walls = walls[:-1]
            last = walls[-1].b


@window.event
def on_mouse_release(x, y, button, modifiers):
    pass


@window.event
def on_mouse_drag(x, y, dx, dy, buttons, modifiers):
    pass


def update(dt):
    global last_keys
    player.update(dt, keys_pressed, last_keys, walls)
    last_keys = keys_pressed.copy()
    times.append(dt)


pg.clock.schedule_interval(update, 1/60.0)
pg.app.run()
print("Average frame time: ", mean(times))
print("Median frame time: ", median(times))
