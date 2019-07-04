import pyglet as pg
from pyglet.window import key
from Vector2D import Vector2D
from Driver import Driver
from Car import Car
from Wall import Wall
from RewardGate import RewardGate

# Init globals:
mode = 2
window = pg.window.Window(1280, 720, resizable=True)
keys_pressed, last_keys = None, None
driver, car = None, None
walls, rgs, space = None, None, None
is_wall_building, is_rg_building = None, None


@window.event
def on_key_press(symbol, modifiers):
    keys_pressed[symbol] = True
    if mode == 2 and symbol == 32:  # space
        reset()


@window.event
def on_key_release(symbol, modifiers):
    keys_pressed[symbol] = False


@window.event
def on_mouse_press(x, y, button, modifiers):
    if is_wall_building:
        global last_wall_vec, walls
        if button == 1:  # Left Click to add point
            v = Vector2D(x, y)
            walls.append(Wall(last_wall_vec.tuple(), v.tuple()))
            last_wall_vec = v
        elif button == 4:  # Right Click to undo
            walls = walls[:-1]
            last_wall_vec = walls[-1].b
    if is_rg_building:
        global tmp_a
        if button == 1:  # Left Click to add point
            v = Vector2D(x, y)
            if tmp_a is None:
                tmp_a = v
            else:
                tmp_rg = RewardGate(tmp_a, v)
                rgs.append(tmp_rg)
                tmp_a = None
        elif button == 4:  # Right Click to undo
            if tmp_a is None:
                tmp_a = rgs[-1].a
                del rgs[-1]
            else:
                tmp_a = None


@window.event
def on_mouse_release(x, y, button, modifiers):
    pass


@window.event
def on_mouse_drag(x, y, dx, dy, buttons, modifiers):
    pass


@window.event
def on_draw():
    window.clear()
    for w in walls:
        w.draw()
    for rg in rgs:
        rg.draw()
    if driver is not None:
        driver.draw()
    else:
        car.draw()


def update_driver(dt):
    global last_keys
    if dt > 1/30.0:
        return
    needs_reset = driver.update(dt, walls, rgs)
    if needs_reset:
        reset()


def update_wasd(dt):
    global last_keys
    car.update_keys(dt, keys_pressed, walls)
    last_keys = keys_pressed.copy()


def reset():
    global rgs, space
    # Reset reward gates:
    for r in rgs:
        r.flip(True)
    for i in range(space):
        rgs[-i-1].flip(False)


def initialize(mode):
    # Modes:
    #   1 - AI controlled
    #   2 - WASD controlled

    # Init in game objects
    global walls, rgs, space, car, driver, is_wall_building, last_wall_vec, is_rg_building, tmp_a, keys_pressed, \
        last_keys
    walls = [Wall((167, 277), (173, 392)), Wall((173, 392), (205, 479)), Wall((205, 479), (297, 534)),
             Wall((297, 534), (427, 541)), Wall((427, 541), (557, 522)), Wall((557, 522), (559, 452)),
             Wall((559, 452), (461, 364)), Wall((461, 364), (459, 332)), Wall((459, 332), (491, 316)),
             Wall((491, 316), (568, 352)), Wall((568, 352), (712, 391)), Wall((712, 391), (825, 375)),
             Wall((825, 375), (876, 306)), Wall((876, 306), (879, 228)), Wall((879, 228), (789, 159)),
             Wall((789, 159), (635, 119)), Wall((635, 119), (361, 98)), Wall((361, 98), (224, 112)),
             Wall((224, 112), (192, 171)), Wall((192, 171), (167, 277)), Wall((219, 280), (223, 349)),
             Wall((223, 349), (229, 404)), Wall((229, 404), (243, 450)), Wall((243, 450), (309, 476)),
             Wall((309, 476), (375, 483)), Wall((375, 483), (433, 485)), Wall((433, 485), (486, 476)),
             Wall((486, 476), (438, 429)), Wall((438, 429), (408, 382)), Wall((408, 382), (399, 315)),
             Wall((399, 315), (432, 286)), Wall((432, 286), (488, 267)), Wall((488, 267), (571, 297)),
             Wall((571, 297), (660, 327)), Wall((660, 327), (751, 335)), Wall((751, 335), (796, 319)),
             Wall((796, 319), (822, 268)), Wall((822, 268), (798, 228)), Wall((798, 228), (698, 185)),
             Wall((698, 185), (598, 164)), Wall((598, 164), (476, 151)), Wall((476, 151), (359, 144)),
             Wall((359, 144), (255, 158)), Wall((255, 158), (221, 252)), Wall((221, 252), (219, 280))]
    rgs = [RewardGate((155, 323), (236, 322)), RewardGate((154, 368), (241, 360)), RewardGate((164, 422), (248, 401)),
           RewardGate((190, 480), (259, 435)), RewardGate((261, 529), (289, 452)), RewardGate((324, 551), (338, 461)),
           RewardGate((401, 555), (398, 467)), RewardGate((474, 549), (443, 466)), RewardGate((460, 464), (568, 528)),
           RewardGate((449, 453), (544, 424)), RewardGate((421, 421), (494, 377)), RewardGate((376, 328), (478, 350)),
           RewardGate((488, 339), (455, 266)), RewardGate((506, 335), (535, 271)), RewardGate((570, 365), (599, 293)),
           RewardGate((641, 384), (659, 311)), RewardGate((708, 403), (710, 313)), RewardGate((790, 395), (763, 305)),
           RewardGate((882, 338), (790, 281)), RewardGate((792, 237), (854, 181)), RewardGate((746, 221), (786, 139)),
           RewardGate((672, 195), (693, 120)), RewardGate((590, 177), (608, 99)), RewardGate((506, 167), (513, 94)),
           RewardGate((430, 161), (436, 87)), RewardGate((357, 155), (355, 89)), RewardGate((308, 163), (281, 93)),
           RewardGate((268, 172), (198, 131)), RewardGate((249, 218), (167, 197)), RewardGate((237, 259), (154, 252))]
    space = 5
    for i in range(space):
        rgs[-i - 1].flip(False)
    car = Car((10, 20), (128, 128, 255), (193, 296))
    if mode == 1:
        driver = Driver(car, False)
    elif mode == 2:
        pass # Do nothing

    # Wall or Reward Gate building:
    is_wall_building = False
    if is_wall_building:
        last_wall_vec = walls[-1].b
    is_rg_building = False
    if is_rg_building:
        tmp_a = None

    # Init controls:
    keys_pressed = {key.W: False, key.A: False, key.S: False, key.D: False}
    last_keys = keys_pressed.copy()

    # Choose update function:
    if mode == 1:
        update = update_driver
    elif mode == 2:
        update = update_wasd
    else:
        update = None
    pg.clock.schedule_interval(update, 1/60.0)
    pg.app.run()


initialize(mode)
