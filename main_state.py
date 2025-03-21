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

time = 200
camera_left = 0
camera_bottom = 0

window_width = 800
window_height = 600

bgm = None
hurry_bgm = None
on_hurry_bgm = False


def enter():
    server.font = load_font('ENCR10B.TTF', int(24*main_state.window_height/600))
    events = None
    global camera_left, camera_bottom, time,score,on_hurry_bgm,bgm,hurry_bgm
    time = 200
    score = 0
    camera_left = 0
    camera_down = 0
    hurry_bgm= False
#     if server.level == 1 or server.level == 3:
#         bgm = load_music('resource\\Super Mario Bros.mp3')
#         hurry_bgm = load_music('resource\\Hurry - Super Mario Bros.mp3')
#     if server.level == 2:
#         bgm = load_music('resource\\Underground.mp3')
#         hurry_bgm = load_music('resource\\Hurry - Underground.mp3')
#     if server.level == 4:
#         bgm = load_music("resource\\King Koopa's Castle.mp3")
#         hurry_bgm = load_music("resource\\Hurry - castle.mp3")
#     bgm.set_volume(64)
#     bgm.repeat_play()
def exit():
#     bgm.stop()
#     hurry_bgm.stop()
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
    global time
    time -= game_framework.frame_time

#     if not on_hurry_bgm and time<100:
#         bgm.stop()
#         hurry_bgm.set_volume(64)
#         hurry_bgm.repeat_play()
    if time < 0:
        server.character.power_up = -1


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
    w,h = main_state.window_width, main_state.window_height
    server.font.draw(0.01*w, 0.95*h, 'score', (255,255,255))
    server.font.draw(0.1*w, 0.9*h, '%d' % (score), (255,255,255))
    server.font.draw(0.89*w, 0.95*h, 'time', (255,255,255))
    server.font.draw(0.9*w, 0.9*h, '%d' % (int(time)), (255,255,255))


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






