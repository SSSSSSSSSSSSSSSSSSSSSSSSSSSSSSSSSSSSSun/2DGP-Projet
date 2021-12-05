import game_framework
import main_state
from pico2d import *


import game_world
import server
import object

# Run Speed
PIXEL_PER_METER = (50.0 / 1.0)  # 50 pixel 1meter
RUN_SPEED_MPSS = 20    # m/s^2
MAX_SPEED_MPS = 5


# Action Speed
TIME_PER_ACTION = 9.0
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION = 3

RIGHT_DOWN, LEFT_DOWN, RIGHT_UP, LEFT_UP, X_DOWN, X_UP = range(6)

key_event_table = {
    (SDL_KEYDOWN, SDLK_RIGHT): RIGHT_DOWN,
    (SDL_KEYDOWN, SDLK_LEFT): LEFT_DOWN,
    (SDL_KEYUP, SDLK_RIGHT): RIGHT_UP,
    (SDL_KEYUP, SDLK_LEFT): LEFT_UP,
    (SDL_KEYDOWN, SDLK_x): X_DOWN,
    (SDL_KEYUP, SDLK_x): X_UP
}

class IdleState:

    def enter(character, event):
        if character.dir == 0 and not (event == None) and not (event == X_UP):
            character.cur_state = RunState
            RunState.enter(character,event)
            return

        if event == RIGHT_DOWN:
            character.dir += 1
        elif event == LEFT_DOWN:
            character.dir -= 1
        elif event == RIGHT_UP:
            character.dir -= 1
        elif event == LEFT_UP:
            character.dir += 1



    def exit(character, event):
        pass

    def do(character):
        if (-MAX_SPEED_MPS < character.lat_speed) and (character.lat_speed <MAX_SPEED_MPS):
            if character.dir > 0:
                character.lat_accel = RUN_SPEED_MPSS
            elif character.dir < 0:
                character.lat_accel = -RUN_SPEED_MPSS
            elif character.lat_speed == 0:
                character.lat_accel = 0
            else:
                if character.lat_speed > 0:
                    if character.lat_speed < 0.05:
                        character.lat_speed = 0
                        character.lat_accel = 0
                    else: character.lat_accel = -RUN_SPEED_MPSS
                else:
                    if character.lat_speed > -0.05:
                        character.lat_speed = 0
                        character.lat_accel = 0
                    else: character.lat_accel = RUN_SPEED_MPSS
        else:
            if character.dir == 0:
                if character.lat_speed > 0:
                    character.lat_accel = -RUN_SPEED_MPSS
                else:
                    character.lat_accel = RUN_SPEED_MPSS
            elif character.dir/abs(character.dir) == character.lat_speed/abs(character.lat_speed):
                character.lat_accel = 0
            else:
                if character.dir / abs(character.dir) > 0:
                    character.lat_accel = RUN_SPEED_MPSS
                else:
                    character.lat_accel = -RUN_SPEED_MPSS

        if character.lat_speed > 0 : character.right = True
        elif character.lat_speed < 0 : character.right = False

        character.lat_speed = character.lat_speed + character.lat_accel * game_framework.frame_time
        character.x = character.x + PIXEL_PER_METER * character.lat_speed * game_framework.frame_time
        character.frame = 0

    def draw(character):
        if character.power_up:
            h = 2
        else:
            h = 1

        if character.jump:
            if character.right:
                    character.image.clip_draw(5 * 16, 144-character.power_up*32, 16, h*16, character.x - main_state.camera_left, character.y- main_state.camera_bottom, character.w,character.h)
            else:
                    character.image.clip_draw(320 - 5 * 16, 64-character.power_up*32, 16, h*16, character.x - main_state.camera_left, character.y- main_state.camera_bottom,character.w, character.h)
            return
        if character.right:
            character.image.clip_draw(0,144-character.power_up*32,16,h* 16,character.x - main_state.camera_left, character.y- main_state.camera_bottom, character.w, character.h)
        else:
            character.image.clip_draw(320, 64-character.power_up*32, 16,h*16, character.x - main_state.camera_left, character.y- main_state.camera_bottom, character.w, character.h )


class RunState:

    def enter(character, event):
        if event == RIGHT_DOWN:
            character.dir += 1
        elif event == LEFT_DOWN:
            character.dir -= 1
        elif event == LEFT_UP:
            character.dir += 1
        elif event == RIGHT_UP:
            character.dir -= 1

    def exit(character, event):
        pass

    def do(character):
        if (-MAX_SPEED_MPS < character.lat_speed) and (character.lat_speed <MAX_SPEED_MPS):
            if character.dir > 0:
                character.lat_accel = RUN_SPEED_MPSS
            elif character.dir < 0:
                character.lat_accel = -RUN_SPEED_MPSS
            elif character.lat_speed == 0:
                character.lat_accel = 0
            else:
                if character.lat_speed > 0:
                    if character.lat_speed < 0.01:
                        character.lat_speed = 0
                        character.lat_accel = 0
                    else: character.lat_accel = -RUN_SPEED_MPSS
                else:
                    if character.lat_speed > -0.01:
                        character.lat_speed = 0
                        character.lat_accel = 0
                    else: character.lat_accel = RUN_SPEED_MPSS
        else:
            clamp(-MAX_SPEED_MPS,character.lat_speed,MAX_SPEED_MPS)
            if character.dir == 0:
                if character.lat_speed > 0:
                    character.lat_accel = -RUN_SPEED_MPSS
                else:
                    character.lat_accel = RUN_SPEED_MPSS
            elif character.dir/abs(character.dir) == character.lat_speed/abs(character.lat_speed):
                character.lat_accel = 0
            else:
                if character.dir / abs(character.dir) > 0:
                    character.lat_accel = RUN_SPEED_MPSS
                else:
                    character.lat_accel = -RUN_SPEED_MPSS
        if character.lat_speed > 0 : character.right = True
        elif character.lat_speed < 0 : character.right = False

        character.lat_speed = character.lat_speed + character.lat_accel * game_framework.frame_time
        character.x = character.x + PIXEL_PER_METER * character.lat_speed * game_framework.frame_time

        character.frame = (character.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time)%3 + 1

    def draw(character):
        if character.power_up:
            h = 2
        else:
            h = 1

        if character.jump:
            if character.right:
                    character.image.clip_draw(5 * 16, 144-character.power_up*32, 16, h*16, character.x - main_state.camera_left, character.y- main_state.camera_bottom, character.w,character.h)
            else:
                    character.image.clip_draw(320 - 5 * 16, 64-character.power_up*32, 16, h*16, character.x - main_state.camera_left, character.y- main_state.camera_bottom,character.w, character.h)
            return


        if character.dir != 0:
            if character.lat_speed / character.dir > 0:
                if character.right:
                    character.image.clip_draw(int(character.frame) * 16, 144-character.power_up*32, 16, h*16, character.x - main_state.camera_left, character.y- main_state.camera_bottom, character.w, character.h)
                else:
                    character.image.clip_draw(320 - int(character.frame) * 16, 64-character.power_up*32, 16, h*16, character.x - main_state.camera_left, character.y- main_state.camera_bottom,character.w, character.h)
            else:
                if character.right:
                    character.image.clip_draw(4 * 16, 144-character.power_up*32, 16, h*16, character.x - main_state.camera_left, character.y- main_state.camera_bottom, character.w, character.h)
                else:
                    character.image.clip_draw(320 - 4 * 16, 64-character.power_up*32, 16, h*16, character.x - main_state.camera_left,  character.y- main_state.camera_bottom, character.w,
                                              character.h)
        else:
            if character.right:
                character.image.clip_draw(4 * 16, 144-character.power_up*32, 16, h*16, character.x - main_state.camera_left, character.y- main_state.camera_bottom, character.w, character.h)
            else:
                character.image.clip_draw(320 - 4 * 16, 64-character.power_up*32, 16, h*16, character.x - main_state.camera_left, character.y- main_state.camera_bottom, character.w, character.h)


class DashState:
    def enter(character, event):
        if character.lat_speed == 0 and event == X_UP:
            character.cur_state = IdleState
            IdleState.enter(character,event)
        if character.lat_speed * character.dir >= 0 and character.power_up == 2:
            character.attack()

    def exit(character, event):
        pass

    def do(character):
        if (-MAX_SPEED_MPS*2 < character.lat_speed) and (character.lat_speed < MAX_SPEED_MPS*2):
            if character.dir > 0:
                character.lat_accel = RUN_SPEED_MPSS*2
            elif character.dir < 0:
                character.lat_accel = -RUN_SPEED_MPSS*2
            elif character.lat_speed == 0:
                character.lat_accel = 0
            else:
                if character.lat_speed > 0:
                    if character.lat_speed < 0.05:
                        character.lat_speed = 0
                        character.lat_accel = 0
                    else:
                        character.lat_accel = -RUN_SPEED_MPSS*2
                else:
                    if character.lat_speed > -0.05:
                        character.lat_speed = 0
                        character.lat_accel = 0
                    else:
                        character.lat_accel = RUN_SPEED_MPSS*2
        else:
            clamp(-MAX_SPEED_MPS*2, character.lat_speed, MAX_SPEED_MPS*2)
            if character.dir == 0:
                if character.lat_speed > 0:
                    character.lat_accel = -RUN_SPEED_MPSS*2
                else:
                    character.lat_accel = RUN_SPEED_MPSS*2
            elif character.dir * abs(character.dir) * character.lat_speed * abs(character.lat_speed) > 0:
                character.lat_accel = 0
            else:
                if character.dir * abs(character.dir) > 0:
                    character.lat_accel = RUN_SPEED_MPSS*2
                else:
                    character.lat_accel = -RUN_SPEED_MPSS*2
        if character.lat_speed > 0:
            character.right = True
        elif character.lat_speed < 0:
            character.right = False

        character.lat_speed = character.lat_speed + character.lat_accel * game_framework.frame_time
        character.x = character.x + PIXEL_PER_METER * character.lat_speed * game_framework.frame_time

        character.frame = (character.frame + FRAMES_PER_ACTION * ACTION_PER_TIME*2 * game_framework.frame_time) % 3 + 1

    def draw(character):
        if character.power_up:
            h = 2
        else:
            h = 1
        if character.jump:
            if character.right:
                    character.image.clip_draw(5 * 16, 144-character.power_up*32, 16, 16*h, character.x - main_state.camera_left, character.y- main_state.camera_bottom, character.w,character.h)
            else:
                    character.image.clip_draw(320 - 5 * 16, 64-character.power_up*32, 16, h*16, character.x - main_state.camera_left, character.y- main_state.camera_bottom,character.w, character.h)
            return


        if character.lat_speed == 0:
            IdleState.draw(character)
            return
        if character.lat_speed * character.dir >= 0:
            if character.right:
                character.image.clip_draw(int(character.frame) * 16, 144-character.power_up*32, 16, h*16, character.x - main_state.camera_left, character.y-main_state.camera_bottom, character.w,character.h)
            else:
                character.image.clip_draw(320 - int(character.frame) * 16, 64-character.power_up*32, 16, h*16, character.x - main_state.camera_left, character.y-main_state.camera_bottom,character.w, character.h)
        else:
            if character.right:
                character.image.clip_draw(4 * 16, 144-character.power_up*32, 16, h*16, character.x - main_state.camera_left, character.y-main_state.camera_bottom, character.w, character.h)
            else:
                character.image.clip_draw(320 - 4 * 16, 64-character.power_up*32, 16, h*16, character.x - main_state.camera_left, character.y-main_state.camera_bottom, character.w, character.h)

next_state_table = {
    IdleState: {RIGHT_UP: RunState, LEFT_UP: RunState,
                RIGHT_DOWN: RunState, LEFT_DOWN: RunState,
                X_DOWN: DashState},
    RunState: {RIGHT_UP: IdleState, LEFT_UP: IdleState,
               LEFT_DOWN: IdleState, RIGHT_DOWN: IdleState,
               X_DOWN: DashState},
    DashState: {RIGHT_UP: IdleState, LEFT_UP: IdleState,
                LEFT_DOWN: IdleState, RIGHT_DOWN: IdleState,
                X_UP: DashState}
    }

class Character:
    image = None
    def __init__(self):
        self.x, self.y = 1600 // 2, 90
        if Character.image == None:
           Character.image = load_image('resource\\Character_sprite.png')
        self.x = 200
        self.y = 550  # 위치
        self.w = 1.0 * PIXEL_PER_METER
        self.h = 0.9 * PIXEL_PER_METER # 크기
        self.dir = 0  # 이동하려는 방향. 1 = right/-1 = left
        self.lat_speed = 0  # 횡방향 속도 / right 방향이 +
        self.lat_accel = 0  # 횡방향 가속도
        self.lon_speed = 0  # 종방향 속도 / up 방향이 +
        self.lon_accel = -0.1475  # 종방향 가속도
        self.power_up = 0  # 파워업 상태
        self.right = True  # 우측방향을 바라보고 있는지
        self.jump = True # 공중에 떠있는지
        self.jump_timer = 0
        self.no_damege_timer = 0
        self.frame = 0
        self.event_que = []
        self.cur_state = IdleState
        self.cur_state.enter(self, None)

    def get_bb(self):
        return self.x - self.w / 2 + self.w / 10 , self.y - self.h / 2, self.x + self.w/2 - self.w / 10, self.y + self.h / 2

    def add_event(self, event):
        self.event_que.insert(0, event)

    def attack(self):
        fire = object.CharFire(self.x, self.y, self.right)
        server.char_fires.append(fire)
        game_world.add_object(fire, 4)

    def update(self):

        self.cur_state.do(self)

        if self.lon_accel!=0:
            self.lon_speed = self.lon_speed + self.lon_accel * game_framework.frame_time
            if self.lon_speed < -98: self.lon_speed = -98
        self.y = self.y + PIXEL_PER_METER * self.lon_speed * game_framework.frame_time
        if self.jump_timer != 0:
            self.jump_timer -= 1
        if self.no_damege_timer != 0:
            self.no_damege_timer -= 1
        self.x = clamp(main_state.camera_left,self.x,server.max_width)
        if server.max_width - main_state.camera_left <= main_state.window_width:
            pass
        elif self.x - main_state.camera_left > 6 * PIXEL_PER_METER:
            main_state.camera_left = self.x - 6 * PIXEL_PER_METER
        main_state.camera_bottom = self.y - 6 * PIXEL_PER_METER
        if main_state.camera_bottom <= 2 * PIXEL_PER_METER:
            main_state.camera_bottom = 2 * PIXEL_PER_METER


        if self.y <= 0:
            self.power_up = -1

        if main_state.camera_bottom < 0: main_state.camera_bottom = 0
        if server.max_height - main_state.camera_bottom <= main_state.window_width:
            main_state.camera_bottom = server.max_height - main_state.window_width



        if len(self.event_que) > 0:
            event = self.event_que.pop()
            if self.cur_state in next_state_table:
                if event in next_state_table[self.cur_state]:
                    self.cur_state.exit(self, event)
                    self.cur_state = next_state_table[self.cur_state][event]
                    self.cur_state.enter(self, event)

    def draw(self):
        self.cur_state.draw(self)

    def handle_event(self, event):

        if (event.type, event.key) in key_event_table:

            key_event = key_event_table[(event.type, event.key)]

            if self.cur_state in next_state_table and key_event in next_state_table[self.cur_state]:
                self.add_event(key_event)

        elif (event.type, event.key) == (SDL_KEYDOWN, SDLK_z) and not self.jump:
            self.y += 1
            self.lon_speed = 9.8
            self.jump_timer = 60
            self.jump = True
        elif (event.type, event.key) == (SDL_KEYUP, SDLK_z) and self.jump_timer != 0:

            self.lon_accel -= 9.8 * self.jump_timer
            self.jump_timer = 0
    def damaged(self):
        if self.no_damege_timer==0:
            self.no_damege_timer = 1000
            self.power_up -= 1
            if not self.power_up:
                self.h /= 2
