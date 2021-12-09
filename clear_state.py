from pico2d import *
import game_framework
import load_state
import main_state
import game_world
import character
import server
PIXEL_PER_METER = (50.0 / 1.0)

dx = 0
time = 0
init = 0
on_bgm = False
bgm = None
def enter():
    global dx, init, on_bgm,time
    on_bgm = False
#     bgm = load_music('Area Clear.mp3')
#     bgm.set_volume(64)


    server.character.frame = 12
    server.character.right = 1
    dx = 0
    time = 0

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
    if server.level <= 3:
        if server.character.power_up >= 1 and server.character.y-server.character.h/4 > 4 * PIXEL_PER_METER :
            server.character.y -= 1
            return
        elif server.character.power_up == 0 and server.character.y > 4 * PIXEL_PER_METER :
            server.character.y -= 1
            return


    if dx<100:

        server.character.x += 1
        dx += 1
        server.character.frame = dx // 3 + 1
    elif time<10:
#         if not on_bgm:
#             bgm.play(1)
#             on_bgm = True
        server.character.frame = 0
        time += game_framework.frame_time
    else:
        server.level += 1
        game_framework.change_state(load_state)

    main_state.camera_bottom = server.character.y - 6 * PIXEL_PER_METER
    if main_state.camera_bottom <= 2 * PIXEL_PER_METER:
        main_state.camera_bottom = 2 * PIXEL_PER_METER
def draw():

    clear_canvas()
    for game_object in game_world.all_objects():
        if type(game_object) == type(character.Character()):
            h = 2
            if server.character.power_up == 0: h = 1
            if server.character.right == True:
                server.character.image.clip_draw(server.character.frame * 16,  (144-server.character.power_up*32), 16, h*16, server.character.x - main_state.camera_left+int(server.character.w/2), server.character.y- main_state.camera_bottom, server.character.w,server. character.h)

            else:
                server.character.image.clip_draw(server.character.frame * 16,  (144-server.character.power_up*32), 16, h*16, server.character.x - main_state.camera_left-int(server.character.w/2), server.character.y- main_state.camera_bottom, server.character.w,server. character.h)

        else:
            game_object.draw()
    update_canvas()