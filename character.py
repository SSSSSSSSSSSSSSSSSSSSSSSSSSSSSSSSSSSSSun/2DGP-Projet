import game_framework
import main_state
from pico2d import *
from object import *

import game_world

# Run Speed
PIXEL_PER_METER = (50.0 / 1.0)  # 50 pixel 1meter
RUN_SPEED_MPSS = 20    # m/s^2
MAX_SPEED_MPS = 5


# Action Speed
TIME_PER_ACTION = 0.05
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
        print('enterIdle')
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
        if character.right:
            character.image.clip_draw(0,144,16, 16,character.x, character.y, character.w, character.h)
        else:
            character.image.clip_draw(320, 64, 16,16, character.x, character.y, character.w, character.h )


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
        if character.dir != 0:
            if character.lat_speed / character.dir > 0:
                if character.right:
                    character.image.clip_draw(int(character.frame) * 16, 144, 16, 16, character.x, character.y,
                                              character.w,
                                              character.h)
                else:
                    character.image.clip_draw(320 - int(character.frame) * 16, 64, 16, 16, character.x, character.y,
                                              character.w, character.h)
            else:
                if character.right:
                    character.image.clip_draw(4 * 16, 144, 16, 16, character.x, character.y, character.w, character.h)
                else:
                    character.image.clip_draw(320 - 4 * 16, 64, 16, 16, character.x, character.y, character.w,
                                              character.h)
        else:
            if character.right:
                character.image.clip_draw(4 * 16, 144, 16, 16, character.x, character.y, character.w, character.h)
            else:
                character.image.clip_draw(320 - 4 * 16, 64, 16, 16, character.x, character.y, character.w, character.h)


class DashState:
    def enter(character, event):
        if character.lat_speed == 0 and event == X_UP:
            character.cur_state = IdleState
            IdleState.enter(character,event)
        if character.lat_speed * character.dir >= 0:
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
        if character.lat_speed == 0:
            IdleState.draw(character)
            return
        if character.lat_speed * character.dir >= 0:
            if character.right:
                character.image.clip_draw(int(character.frame) * 16, 144, 16, 16, character.x, character.y, character.w,character.h)
            else:
                character.image.clip_draw(320 - int(character.frame) * 16, 64, 16, 16, character.x, character.y,character.w, character.h)
        else:
            if character.right:
                character.image.clip_draw(4 * 16, 144, 16, 16, character.x, character.y, character.w, character.h)
            else:
                character.image.clip_draw(320 - 4 * 16, 64, 16, 16, character.x, character.y, character.w, character.h)

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

    def __init__(self):
        self.x, self.y = 1600 // 2, 90
        self.image = load_image('resource\\Character_sprite.png')
        self.x = 200
        self.y = 200  # 위치
        self.w = 1 * PIXEL_PER_METER
        self.h = 1 * PIXEL_PER_METER # 크기
        self.dir = 0  # 이동하려는 방향. 1 = right/-1 = left
        self.lat_speed = 0  # 횡방향 속도 / right 방향이 +
        self.lat_accel = 0  # 횡방향 가속도
        self.lon_speed = 0  # 종방향 속도 / up 방향이 +
        self.lon_accel = 0  # 종방향 가속도
        self.power_up = 0  # 파워업 상태
        self.right = True  # 우측방향을 바라보고 있는지
        self.frame = 0
        self.frame_wait = 0
        self.event_que = []
        self.cur_state = IdleState
        self.cur_state.enter(self, None)



    def add_event(self, event):
        self.event_que.insert(0, event)

    def attack(self):
        fire = CharFire(self.x, self.y, self.right)
        main_state.move_object.append(fire)
        game_world.add_object(fire, 1)

    def update(self):
        self.cur_state.do(self)
        if len(self.event_que) > 0:
            event = self.event_que.pop()
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
