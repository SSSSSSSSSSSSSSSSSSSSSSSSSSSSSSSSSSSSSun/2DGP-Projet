from pico2d import *
import game_framework
import load_state
import game_world
import server
import pickle

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
    #=====임시=========
    server.max_width = 3000
    server.max_height = 1000



    load()
    server.bg_image = Black_BG()
    game_world.add_object(server.character,5)
    game_world.add_object(server.bg_image,0)
    game_world.add_objects(server.bg, 1)
    game_world.add_objects(server.enemys, 4)
    game_world.add_objects(server.objects,2)
    for i in server.blocks.values():
        game_world.add_objects(i, 3)

    global image


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

#=====임시=========
def handle_events():
    events = get_events()

    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
                game_framework.quit()


def exit():
    global image
    del(image)

def update():
    global load_time
    game_framework.change_state(main_state)
    load_time += game_framework.frame_time

def draw():
    clear_canvas()
    global image
    image.draw(400, 300)
    update_canvas()

