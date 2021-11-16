import random
import json
import os

from pico2d import *
import game_framework
import game_world
from collide import *
debug = False

from character import Character
from enemy import *
from object import *
from block import *


PIXEL_PER_METER = (50.0 / 1.0)

name = "MainState"

stage = 1
level = 1

character = None
enemys = []
char_fires = []
objects = []
blocks = dict()
def enter():
    global character
    character = Character()
    global enemys
    enemys = [Goomba(800,60), Turtle(800,130,False), Hammer(800,230), Boss(800,330)]
    global objects
    global blocks
    blocks_list = [Platform(150,80),Platform(200,550)]
    for block in blocks_list:
        if not block.x in blocks:
            blocks[block.x] = []
        blocks[block.x].append(block)

    game_world.add_object(character, 4)
    game_world.add_objects(enemys, 3)
    for i in blocks.values():
        game_world.add_objects(i, 2)


def exit():
    game_world.clear()

def pause():
    pass


def resume():
    pass


def handle_events():
    global debug
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
                game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_v:
                debug = 1 - debug
        else:
            character.handle_event(event)


def update():
    for game_object in game_world.all_objects():
        game_object.update()
    # 주인공 - 적
    for enemy in enemys:
        if collide(character,enemy):
            print('c-e')
    # 주인공 - 오브젝트
    for object in objects:
        if collide(character,object):
            print('c-o')
    # 주인공 - 블록
    x = (character.x//PIXEL_PER_METER) * PIXEL_PER_METER
    on_block = False
    if x in blocks:
        for block in blocks[x]:
            if collide(character,block):
                collide_block(character,block)
                on_block = True

    x += PIXEL_PER_METER
    if x in blocks:
        for block in blocks[x]:
            if collide(character,block):
                collide_block(character,block)
                on_block = True

    if not on_block:
        character.lon_accel = -0.1475
def draw():
    clear_canvas()
    for game_object in game_world.all_objects():
        game_object.draw()

    if debug:
        draw_rectangle(*character.get_bb())
        x = (character.x // PIXEL_PER_METER) * PIXEL_PER_METER
        if x in blocks:
            for block in blocks[x]:
                draw_rectangle(*block.get_bb())
        x += PIXEL_PER_METER
        if x in blocks:
            for block in blocks[x]:
                draw_rectangle(*block.get_bb())
    update_canvas()






