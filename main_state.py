import random
import json
import os

from pico2d import *
import game_framework
import load_state
import game_world
import death_state
import server
from collide import *
debug = False

score = 0




PIXEL_PER_METER = (50.0 / 1.0)

name = "MainState"


camera_left = 0
camera_bottom = 0

window_width = 800
window_height = 600

def enter():
    events = None
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
        server.character.lon_accel = -9.8
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
        # 적 - 등껍질
        for shell in server.objects:
             if type(shell) == type(load_state.Shell(0,0,0)) and enemy.hp > 0 and shell.lat_speed!=0:
                if collide(enemy,shell):
                    enemy.hp -= 2
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
        game_framework.change_state(death_state)



def draw():
    clear_canvas()
    for game_object in game_world.all_objects():
        game_object.draw()

    if debug:
        l, b, r, t = server.character.get_bb()
        draw_rectangle(l-camera_left,b-camera_bottom,r-camera_left,t-camera_bottom)
        x = (server.character.x // PIXEL_PER_METER) * PIXEL_PER_METER
        if x in server.blocks:
            for block in server.blocks[x]:
                l, b, r, t = block.get_bb()
                draw_rectangle(l-camera_left,b-camera_bottom,r-camera_left,t-camera_bottom)
        x += PIXEL_PER_METER
        if x in server.blocks:
            for block in server.blocks[x]:
                l, b, r, t = block.get_bb()
                draw_rectangle(l-camera_left,b-camera_bottom,r-camera_left,t-camera_bottom)
        for enemy in server.enemys:
            l, b, r, t = enemy.get_bb()
            draw_rectangle(l-camera_left,b-camera_bottom,r-camera_left,t-camera_bottom)
            x = (enemy.x//PIXEL_PER_METER) * PIXEL_PER_METER
            on_block = False
            if x in server.blocks:
                for block in server.blocks[x]:
                    l, b, r, t = block.get_bb()
                    draw_rectangle(l-camera_left,b-camera_bottom,r-camera_left,t-camera_bottom)

            x += PIXEL_PER_METER
            if x in server.blocks:
                for block in server.blocks[x]:
                    l, b, r, t = block.get_bb()
                    draw_rectangle(l-camera_left,b-camera_bottom,r-camera_left,t-camera_bottom)
        for fire in server.char_fires:
            l, b, r, t = fire.get_bb()
            draw_rectangle(l-camera_left,b-camera_bottom,r-camera_left,t-camera_bottom)
            x = (fire.x//PIXEL_PER_METER) * PIXEL_PER_METER

            if x in server.blocks:
                for block in server.blocks[x]:
                    l, b, r, t = block.get_bb()
                    draw_rectangle(l-camera_left,b-camera_bottom,r-camera_left,-camera_bottom)

            x += PIXEL_PER_METER
            if x in server.blocks:
                for block in server.blocks[x]:
                    l, b, r, t = block.get_bb()
                    draw_rectangle(l-camera_left,b-camera_bottom,r-camera_left,-camera_bottom)
        for object in server.objects:
            l, b, r, t = object.get_bb()
            draw_rectangle(l-camera_left,b-camera_bottom,r-camera_left,t-camera_bottom)
            x = (object.x//PIXEL_PER_METER) * PIXEL_PER_METER

            if x in server.blocks:
                for block in server.blocks[x]:
                    l, b, r, t = block.get_bb()
                    draw_rectangle(l-camera_left,b-camera_bottom,r-camera_left,-camera_bottom)

            x += PIXEL_PER_METER
            if x in server.blocks:
                for block in server.blocks[x]:
                    l, b, r, t = block.get_bb()
                    draw_rectangle(l-camera_left,b-camera_bottom,r-camera_left,-camera_bottom)

    update_canvas()






