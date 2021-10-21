from character import *
from enemy import *
from pico2d import *

open_canvas()

char_image = load_image('resource\\Character_sprite.png')
enemy_image = load_image('resource\\Enemies_sprite.png')
object_image = load_image('resource\\Object_sprite.png')
a = 1
while(a):
    clear_canvas()

    clip_l = char.right*char.clip_l+(1-char.right)*(320-char.clip_l)
    clip_b = char.clip_b + char.right*80 - char.power_up*32

    char_image.clip_draw(clip_l, clip_b, char.clip_w, char.clip_h, char.x, char.y + char.h // 2, char.w, char.h)
    for enemy in enemys:
        clip_w = None
        clip_h = None
        if str(type(enemy)) == "<class 'enemy.Goomba'>":

            clip_w = 16
            clip_h = 16
            clip_b = 112 + (1-enemy.right) * 128
            clip_l = (1-enemy.right) * enemy.frame * clip_w + enemy.right * (112 - enemy.frame * clip_w)
        elif str(type(enemy)) == "<class 'enemy.Turtle'>":

            clip_w = 16
            clip_h = 32
            clip_b = 80 + (1-enemy.right) * 128
            clip_l = (1-enemy.right) * enemy.frame * clip_w + enemy.right * (112 - enemy.frame * clip_w)
        elif str(type(enemy)) == "<class 'enemy.Hammer'>":
            clip_w = 16
            clip_h = 32
            clip_b = 32 + (1-enemy.right) * 128
            clip_l = (1-enemy.right) * enemy.frame * clip_w + enemy.right * (112 - enemy.frame * clip_w)
        else:
            clip_w = 32
            clip_h = 32
            clip_b = 0 + (1-enemy.right) * 128
            clip_l = (1-enemy.right) * enemy.frame * clip_w + enemy.right * (96 - enemy.frame * clip_w)
        enemy_image.clip_draw(clip_l, clip_b, clip_w, clip_h, enemy.x, enemy.y + enemy.h // 2 , enemy.w, enemy.h)

    for object in objects:
        if str(type(object)) == "<class 'object.CharFire'>":
            clip_w = 8
            clip_h = 8
            clip_b = 0
            clip_l = 1+8*object.frame
        object_image.clip_draw(clip_l, clip_b, clip_w, clip_h, object.x, object.y, object.w, object.h)

    update_canvas()
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            a = 0
        elif event.type == SDL_KEYDOWN:
            if event.key == SDLK_ESCAPE:
                a = 0
            elif event.key == SDLK_LEFT:
                char.dir -= 1
            elif event.key == SDLK_RIGHT:
                char.dir += 1
            elif event.key == SDLK_z:
                char.attack()
        elif event.type == SDL_KEYUP:
            if event.key == SDLK_LEFT:
                char.dir += 1
            elif event.key == SDLK_RIGHT:
                char.dir -= 1
            elif event.key == SDLK_1:
                char.power_up = 1
            elif event.key == SDLK_0:
                char.power_up = 0
            elif event.key == SDLK_2:
                char.power_up = 2

    char.move()
    char.sprite()
    for enemy in enemys:
        enemy.attack()
        enemy.sprite()
    for object in objects:
        if str(type(object)) == "<class 'object.CharFire'>":
            object.move()
        object.sprite()

close_canvas()