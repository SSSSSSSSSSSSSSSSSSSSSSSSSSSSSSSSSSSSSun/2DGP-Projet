from pico2d import *
import game_framework
import load_state
import game_world
import server

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

    #=====임시=========
    server.max_width = 3000
    server.max_height = 1000
    server.character = Character()

    server.enemys = [Hammer(800,200), Turtle(400,250,False), Boss(600,200)]
    server.bg = [Big_castle(500,450)]
    server.objects = []
    blocks_list = [Pipe(100,300,0,0),Pipe(150,300,0,1),Pipe(100,350,0,2),Pipe(150,350,1,3)]
    blocks_list += [Platform(i,j,0) for i in range(0,5000,int(PIXEL_PER_METER)) for j in range(0,200,int(PIXEL_PER_METER))]
    blocks_list +=  [Brick(300,300,1),Coin(350,300), Platform(400,300,1), Box(450,300,[Mushroom(450,300), Flower(450,300)])]
    blocks_list +=[Brick(300,200,1)]

    for block in blocks_list:
        x = block.x - block.x%50
        if not x in server.blocks:
            server.blocks[x] = []
        server.blocks[x].append(block)

    game_world.add_object(server.character,5)
    game_world.add_objects(server.bg, 1)
    game_world.add_objects(server.enemys, 4)
    game_world.add_objects(server.objects,2)
    for i in server.blocks.values():
        game_world.add_objects(i, 3)

    global image
    image = load_image('resource\\Object_sprite.png')
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
    if (load_time > 3.0):
        load_time = 0
        game_framework.change_state(main_state)
    load_time += game_framework.frame_time

def draw():
    clear_canvas()
    global image
    image.draw(400, 300)
    update_canvas()

