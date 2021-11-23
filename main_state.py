import random
import json
import os

from pico2d import *
import game_framework
import load_state
import game_world
import server
from collide import *
debug = False




PIXEL_PER_METER = (50.0 / 1.0)

name = "MainState"

stage = 1
level = 1
camera_left = 0
camera_bottom = 0

window_width = 800
window_height = 600

def enter():
    global camera_left, camera_bottom
    camera_left = 0
    camera_down = 0


def exit():
    pass

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
                if object.timer <= 0 and object in server.objects:
                    if drop_a_collide(object,block):
                        collide_object_block(object, block)
                        on_block = True
        x += PIXEL_PER_METER
        if x in server.blocks:
            for block in server.blocks[x]:
                if object.timer <= 0 and object in server.objects:
                    if drop_a_collide(object,block):
                        collide_object_block(object, block)
                        on_block = True
        if not on_block:
            object.lon_accel = -0.1475

    if server.character.power_up < 0:
        game_framework.change_state(load_state)



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
                for block in server.blocks[x]:
                    draw_rectangle(*block.get_bb())

            x += PIXEL_PER_METER
            if x in server.blocks:
                for block in server.blocks[x]:
                    draw_rectangle(*block.get_bb())

    update_canvas()






