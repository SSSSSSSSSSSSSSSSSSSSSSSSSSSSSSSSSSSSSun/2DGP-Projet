import random
import json
import os

from pico2d import *
import game_framework
import game_world
import server
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
camera_left = 0
camera_down = 0


def enter():
    global camera_left, camera_down
    camera_left = 0
    camera_down = 0

#=====임시=========

    server.character = Character()

    server.enemys = [Goomba(800,230), Turtle(400,230,False), Boss(600,330)]

    server.objects = []

    blocks_list = [Platform(i,j,0) for i in range(0,5000,int(PIXEL_PER_METER)) for j in range(0,200,int(PIXEL_PER_METER))]
    blocks_list +=  [Brick(300,300,1),Brick(350,300,0), Platform(400,300,1), Box(450,300,[Mushroom(450,300), Flower(450,300)])]
    blocks_list +=[Brick(300,200,1)]
    for block in blocks_list:
        if not block.x in server.blocks:
            server.blocks[block.x] = []
        server.blocks[block.x].append(block)

    game_world.add_object(server.character, 4)
    game_world.add_objects(server.enemys, 3)
    game_world.add_objects(server.objects,1)
    for i in server.blocks.values():
        game_world.add_objects(i, 2)
#=====임시=========

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

            server.character.handle_event(event)


def update():
    for game_object in game_world.all_objects():
        game_object.update()
    # 주인공 - 적
    for enemy in server.enemys:
        if enemy.hp > 0:
            if collide(server.character,enemy):
                collide_enemy(server.character,enemy)
    # 주인공 - 오브젝트
    for object in server.objects:
        if collide(server.character,object):
            object.do(server.character)
    # 주인공 - 블록
    x = (server.character.x//PIXEL_PER_METER) * PIXEL_PER_METER
    on_block = False

    if x in server.blocks:
        for block in server.blocks[x]:

            if drop_a_collide(server.character,block):
                collide_block(server.character,block)
                if a_position_than_b(server.character, block) == 1:
                    on_block = True



    x += PIXEL_PER_METER
    if x in server.blocks:
        for block in server.blocks[x]:

            if drop_a_collide(server.character,block):
                collide_block(server.character,block)
                if a_position_than_b(server.character, block) == 1:
                    on_block = True

    if not on_block:
        server.character.jump = True
        server.character.lon_accel = -0.1475
    # 적 - 블록

    for enemy in server.enemys:
        x = (enemy.x//PIXEL_PER_METER) * PIXEL_PER_METER
        on_block = False
        if x in server.blocks:
            for block in server.blocks[x]:
                if drop_a_collide(enemy,block):
                    collide_enemy_block(enemy,block)
                    on_block = True

        x += PIXEL_PER_METER
        if x in server.blocks:
            for block in server.blocks[x]:
                if drop_a_collide(enemy,block):
                    collide_enemy_block(enemy,block)
                    on_block = True
        if not on_block:
            enemy.lon_accel = -0.1475
        # 적 - 파이어볼
        for fire in server.char_fires:
            if enemy.hp > 0:
                if collide(enemy,fire):
                    enemy.hp -= 2
                    server.char_fires.remove(fire)
                    game_world.remove_object(fire)
                    del fire
    # 파이어볼 - 블록
    for fire in server.char_fires:
        x = (fire.x//PIXEL_PER_METER) * PIXEL_PER_METER

        if x in server.blocks:
            for block in server.blocks[x]:
                if collide(fire,block):

                    collide_fire_block(fire,block)

        x += PIXEL_PER_METER
        if x in server.blocks:
            for block in server.blocks[x]:
                if collide(fire,block):
                    collide_fire_block(fire,block)
#

    # 오브젝트 - 블록
    for object in server.objects:
        x = (object.x//PIXEL_PER_METER) * PIXEL_PER_METER
        on_block = False
        if x in server.blocks:
            for block in server.blocks[x]:
                if object.timer <= 0:
                    if drop_a_collide(object,block):
                        collide_object_block(object, block)
                        on_block = True
        x += PIXEL_PER_METER
        if x in server.blocks:
            for block in server.blocks[x]:
                if object.timer <= 0:
                    if drop_a_collide(object,block):
                        collide_object_block(object, block)
                        on_block = True
        if not on_block:
            object.lon_accel = -0.1475
def draw():
    clear_canvas()
    for game_object in game_world.all_objects():
        game_object.draw()

    if debug:
        draw_rectangle(*server.character.get_bb())
        x = (server.character.x // PIXEL_PER_METER) * PIXEL_PER_METER
        if x in server.blocks:
            for block in server.blocks[x]:
                draw_rectangle(*block.get_bb())
        x += PIXEL_PER_METER
        if x in server.blocks:
            for block in server.blocks[x]:
                draw_rectangle(*block.get_bb())
        for enemy in server.enemys:
            draw_rectangle(*enemy.get_bb())
            x = (enemy.x//PIXEL_PER_METER) * PIXEL_PER_METER
            on_block = False
            if x in server.blocks:
                for block in server.blocks[x]:
                    draw_rectangle(*block.get_bb())

            x += PIXEL_PER_METER
            if x in server.blocks:
                for block in server.blocks[x]:
                    draw_rectangle(*block.get_bb())
        for fire in server.char_fires:
            draw_rectangle(*fire.get_bb())
            x = (fire.x//PIXEL_PER_METER) * PIXEL_PER_METER

            if x in server.blocks:
                for block in blocks[x]:
                    draw_rectangle(*block.get_bb())

            x += PIXEL_PER_METER
            if x in server.blocks:
                for block in blocks[x]:
                    draw_rectangle(*block.get_bb())

    update_canvas()






