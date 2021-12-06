from pico2d import *
import game_framework
import load_state
import main_state
import game_world
import gameover_state
import character
import server
PIXEL_PER_METER = (50.0 / 1.0)

dx = 0
time = 0

def enter():
    global dx, time



    server.character.frame = 19
    server.character.right = 1
    dx = 0
    time = 0
    server.character.lon_speed = 5
def handle_events():
    events = get_events()

    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
                game_framework.quit()
        else:

            server.character.handle_event(event)
def exit():
    pass

def update():
    global dx, time

    if time<30:
        server.character.y += 2
    elif time<60:
        server.character.y += 0.5
    elif time<90:
        pass
    elif time<300:
        server.character.y -= 1.5
    else:
        server.life -= 1
        if server.life < 0:
            game_framework.change_state(gameover_state)
        else:
            game_framework.change_state(load_state)

    time += 1
def draw():

    clear_canvas()
    for game_object in game_world.all_objects():
        if type(game_object) == type(character.Character()):
            if server.character.right == True:
                server.character.image.clip_draw(server.character.frame * 16,  (144), 16, int(server.character.h*16), server.character.x - main_state.camera_left+int(server.character.w/2), server.character.y- main_state.camera_bottom, server.character.w,server. character.h)

            else:
                server.character.image.clip_draw(server.character.frame * 16,  (144), 16, int(server.character.h*16), server.character.x - main_state.camera_left-int(server.character.w/2), server.character.y- main_state.camera_bottom, server.character.w,server. character.h)

        else:
            game_object.draw()
    update_canvas()