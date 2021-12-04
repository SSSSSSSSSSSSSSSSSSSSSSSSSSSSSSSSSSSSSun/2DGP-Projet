import random
import json
import os
import pickle

from pico2d import *
import game_framework
import load_state
import game_world
import server
from collide import *
debug = False

score = 0
click, eraser = 0, 0

obj_select = 0
select = 0

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
    main_state.camera_left = server.character.x - 6 * PIXEL_PER_METER

    main_state.camera_bottom = server.character.y - 6 * PIXEL_PER_METER

def exit():
    pass

def pause():
    pass


def resume():
    pass


def handle_events():
    global debug, click, eraser
    global obj_select, select
    events = get_events()

    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_v:
            debug = 1 - debug
        elif event.type == SDL_KEYDOWN and event.key == SDLK_1:
            save()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_2:
            game_framework.change_state(load_state)
        elif event.type == SDL_KEYDOWN and event.key == SDLK_3:
            server.character.x, server.character.y = 200, 200
        elif event.type == SDL_KEYDOWN:
            if event.key == SDLK_y:
                if obj_select == 0: select = (select+1)%5
                else: obj_select = 0
            if event.key == SDLK_u:
                if obj_select == 1: select = (select+1)%11
                else:
                    obj_select = 1
                    select = 0
            if event.key == SDLK_i:
                if obj_select == 2: select = (select+1)%12
                else:
                    obj_select = 2
                    select = 0
            if event.key == SDLK_o:
                if obj_select == 3: select = (select+1)%10
                else:
                    obj_select = 3
                    select = 0
            if event.key == SDLK_h:
                if obj_select == 0: select = (select-1)%5
                else:
                    obj_select = 0
                    select = 0
            if event.key == SDLK_j:
                if obj_select == 1: select = (select-1)%11
                else:
                    obj_select = 1
                    select = 0
            if event.key == SDLK_k:
                if obj_select == 2: select = (select-1)%16
                else:
                    obj_select = 2
                    select = 0
            if event.key == SDLK_l:
                if obj_select == 3: select = (select-1)%10
                else:
                    obj_select = 3
                    select = 0
            else:
                server.character.handle_event(event)

        elif event.type == SDL_MOUSEBUTTONDOWN:
            if event.button == SDL_BUTTON_LEFT:
                click = 1
            else:
                eraser = 1
        elif event.type == SDL_MOUSEMOTION :
            x, y = event.x, event.y
            if click == 1:
                build(x,y)
            elif eraser == 1:
                delete(x,y)
        elif event.type == SDL_MOUSEBUTTONUP:
            if event.button == SDL_BUTTON_LEFT:
                click = 0
            else:
                eraser = 0
        else:
            server.character.handle_event(event)

def build(x,y):
    global click, eraser
    y = window_height - y
    x = main_state.camera_left + x +50 - x%50
    y = main_state.camera_bottom + y +50 - y%50
    input = None
    if obj_select == 0:

        if select == 0:
            input = load_state.Goomba(x,y)
        if select == 1:
            input = load_state.Black_Goomba(x,y)
        if select == 2:
            input = load_state.Turtle(x,y,0)
        if select == 3:
            input = load_state.Hammer(x,y)
        if select == 4:
            input = load_state.Boss(x,y)
        server.enemys.append(input)
        game_world.add_object(input,4)
    elif obj_select == 1:
        if select == 0:
            input = load_state.Platform(x,y,0)
        if select == 1:
            input = load_state.Platform(x,y,1)
        if select == 2:
            input = load_state.Brick(x,y,0)
        if select == 3:
            input = load_state.Brick(x,y,1)
        if select == 4:
            input = load_state.Box(x,y,[load_state.Mushroom(x,y)])
        if select == 5:
            input = load_state.Box(x,y,[load_state.Flower(x,y)])
        if select == 6:
            input = load_state.Coin(x,y)
        if select == 7:
            input = load_state.Flag(x,y,0)
        if select == 8:
            input = load_state.Flag(x,y,1)
        if select == 9:
            input = load_state.Flag(x,y,2)
        if select == 10:
            input = load_state.Axe(x,y)
        if not x in server.blocks:
            server.blocks[x] = []
        else:
            for i in server.blocks[x]:
                if i.x== input.x and i.y == input.y:
                    return
            server.blocks[x].append(input)
        game_world.add_object(input,3)
    elif obj_select == 2:

        input = load_state.Pipe(x,y,select//4,select%4)

        if not x in server.blocks:
            server.blocks[x] = []
        else:
            for i in server.blocks[x]:
                if i.x== input.x and i.y == input.y:
                    return
            server.blocks[x].append(input)
        game_world.add_object(input,3)
    elif obj_select == 3:
        if select == 0:
            input = load_state.Big_grass(x,y)
        if select == 1:
            input = load_state.grass(x,y)
        if select == 2:
            input = load_state.Big_cloud(x,y)
        if select == 3:
            input = load_state.cloud(x,y)
        if select == 4:
            input = load_state.Big_tree(x,y)
        if select == 5:
            input = load_state.tree(x,y)
        if select == 6:
            input = load_state.lava(x,y)
        if select == 7:
            input = load_state.BG_pipe(x,y)
        if select == 8:
            input = load_state.castle(x,y)
        if select == 9:
            input = load_state.Big_castle(x,y)
        server.bg.append(input)
        game_world.add_object(input,1)


def delete(x,y):
    y = window_height - y
    x = main_state.camera_left + x +50 - x%50
    y = main_state.camera_bottom + y +50 - y%50

    for i in server.bg:
        if i.x -25<= x and i.x +25>= x and i.y -25<= y and i.y +25>= y:
            server.bg.remove(i)
            game_world.remove_object(i)
    for i in server.enemys:
        if i.x -25<= x and i.x +25>= x and i.y -25<= y and i.y +25>= y:
            server.enemys.remove(i)
            game_world.remove_object(i)
    for i in server.char_fires:
        if i.x -25<= x and i.x +25>= x and i.y -25<= y and i.y +25>= y:
            server.char_fires.remove(i)
            game_world.remove_object(i)
    for i in server.objects:
        if i.x -25<= x and i.x +25>= x and i.y -25<= y and i.y +25>= y:
            server.objects.remove(i)
            game_world.remove_object(i)
    for j in server.blocks.values():
        for i in j:
            if i.x == x and i.y == y:
                server.blocks[x].remove(i)
                game_world.remove_object(i)


def save():
    with open('map\\%d_%d\\character.pickle' % (server.stage,server.level), 'wb') as f:
        pickle.dump(server.character, f)
    with open('map\\%d_%d\\bg.pickle' % (server.stage,server.level), 'wb') as f:
        pickle.dump(server.bg, f)
    with open('map\\%d_%d\\bg_image.pickle' % (server.stage,server.level), 'wb') as f:
        pickle.dump(server.bg_image, f)
    with open('map\\%d_%d\\enemys.pickle' % (server.stage,server.level), 'wb') as f:
        pickle.dump(server.enemys, f)
    with open('map\\%d_%d\\blocks.pickle' % (server.stage,server.level), 'wb') as f:
        pickle.dump(server.blocks, f)
    with open('map\\%d_%d\\char_fires.pickle' % (server.stage,server.level), 'wb') as f:
        pickle.dump(server.char_fires, f)
    with open('map\\%d_%d\\objects.pickle' % (server.stage,server.level), 'wb') as f:
        pickle.dump(server.objects, f)


def update():
    server.character.update()
    return #에디터이므로 update 불필요
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
        game_framework.change_state(load_state)



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






