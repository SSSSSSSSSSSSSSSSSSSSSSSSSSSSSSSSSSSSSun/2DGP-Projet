from pico2d import *
import game_framework
import main_state
import title_state
import server

time = 0
image = None

def enter():
    server.clear()
    game_world.clear()
    global image, time
    image = load_image('resource\\black_BG.png')
    time = 0
def handle_events():
    events = get_events()

    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
                game_framework.quit()

def exit():
    pass

def update():
    global time
    if time < 5.0:
        game_framework.change_state(title_state)

    time += game_framework.frame_time

def draw():
    w,h = main_state.window_width, main_state.window_height
    clear_canvas()

    image.clip_draw(0,0,256,240,w/2,h/2,w,h)
    server.font.draw(3*w/8,1*h/2,'Game Over',(255,255,255))
    update_canvas()