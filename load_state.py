from pico2d import *
import game_framework
import load_state
import game_world
import server
import pickle
PIXEL_PER_METER = (50.0 / 1.0)  # 50 pixel 1meter
from character import Character
from bg import *
from enemy import *
from object import *
from block import *

name = "LoadState"
image = None
load_time = 0.0

def enter():
    server.clear()
    game_world.clear()

    Character(), Object(0,0), Enemy(0,0), Block(0,0), BGround(0,0), Object(0,0), Blue_BG(), Black_BG()



    load()

    if server.level == 1:
        server.max_height = 30 * PIXEL_PER_METER
    elif server.level == 2:
        server.max_height = 18 * PIXEL_PER_METER
    rightest = max(server.blocks.keys())
    server.max_width = rightest
#     server.character.x = server.max_width - PIXEL_PER_METER * 15
    game_world.add_object(server.character,5)
    game_world.add_objects(server.bg, 1)
    game_world.add_object(server.bg_image, 0)
    game_world.add_objects(server.enemys, 4)
    game_world.add_objects(server.objects,2)
    for i in server.blocks.values():
        game_world.add_objects(i, 3)

    global image
    image = load_image('resource\\black_BG.png')

def load():
    with open('map\\%d_%d\\character.pickle' % (server.stage,server.level), 'rb') as f:
        server.character = pickle.load(f)
    with open('map\\%d_%d\\bg.pickle' % (server.stage,server.level), 'rb') as f:
        server.bg = pickle.load(f)
    with open('map\\%d_%d\\bg_image.pickle' % (server.stage,server.level), 'rb') as f:
        server.bg_image = pickle.load(f)
    with open('map\\%d_%d\\enemys.pickle' % (server.stage,server.level), 'rb') as f:
        server.enemys = pickle.load(f)
    with open('map\\%d_%d\\char_fires.pickle' % (server.stage,server.level), 'rb') as f:
        server.char_fires = pickle.load(f)
    with open('map\\%d_%d\\blocks.pickle' % (server.stage,server.level), 'rb') as f:
        server.blocks = pickle.load(f)
    with open('map\\%d_%d\\objects.pickle' % (server.stage,server.level), 'rb') as f:
        server.objects = pickle.load(f)


def handle_events():
    events = get_events()

    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
                game_framework.quit()
        else:

            server.character.handle_event(event)

def exit():
    global image
    del(image)

def update():
    global load_time
    if (load_time > 3.0):
        load_time = 0
        game_framework.change_state(main_state)
    load_time += game_framework.frame_time

def draw():
    clear_canvas()
    global image
    w, h = main_state.window_width, main_state.window_height
    image.clip_draw(0,0,4,4,w/2,h/2,w,h)
    server.font.draw(7*w/16,5*h/8,'%d-%d' % (server.stage, server.level),(255,255,255))
    server.font.draw(15*w/32,h/2,'X  %d' % (server.life),(255,255,255))
    server.character.image.clip_draw(0,112,16,32, 3/8 * w,h/2 , server.character.w, server.character.h*2)
    update_canvas()

