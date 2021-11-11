import random
import json
import os

from pico2d import *
import game_framework
import game_world

from character import Character
from enemy import *

PIXEL_PER_METER = (50.0 / 1.0)

name = "MainState"

character = None
enemy = []
move_object = []
def enter():
    global character
    character = Character()
    global enemy
    enemy = [Goomba(800,60), Turtle(800,130,False), Hammer(800,230), Boss(800,330)]
    # grass = Grass()
    # game_world.add_object(grass, 0)
    game_world.add_object(character, 4)
    game_world.add_objects(enemy, 3)


def exit():
    game_world.clear()

def pause():
    pass


def resume():
    pass


def handle_events():
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
                game_framework.quit()
        else:
            character.handle_event(event)


def update():
    for game_object in game_world.all_objects():
        game_object.update()
    # fill here


def draw():
    clear_canvas()
    for game_object in game_world.all_objects():
        game_object.draw()
    update_canvas()






