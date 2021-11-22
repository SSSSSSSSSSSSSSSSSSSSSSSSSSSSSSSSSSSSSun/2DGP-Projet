import game_framework
from pico2d import *
from character import *
import main_state
import game_world
import server


PIXEL_PER_METER = (50.0 / 1.0)  # 50 pixel 1meter

CHARFIRE_SPEED_MPS = 15    # m/s
CHARFIRE_SPEED_PPS = PIXEL_PER_METER * CHARFIRE_SPEED_MPS
MUSHROOM_SPEED_MPS = 1
MUSHROOM_SPEED_PPS = PIXEL_PER_METER * MUSHROOM_SPEED_MPS

# Action Speed
TIME_PER_ACTION = 0.3
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION = 3

class Object():
    image = None
    def __init__(self, x, y):
        if self.image == None:
            Object.image = load_image('resource\\Object_sprite.png')
        self.x = x
        self.y = y
        self.frame = 0
        self.lat_speed = 0  # 횡방향 속도 / right 방향이 +
        self.lon_speed = 0  # 종방향 속도 / up 방향이 +
        self.lon_accel = 0  # 종방향 가속도
        self.timer = 0

class CharFire(Object):
    def __init__(self, x, y, right):
        super(CharFire, self).__init__(x, y)
        self.w = 0.5 * PIXEL_PER_METER
        self.h = 0.5 * PIXEL_PER_METER
        self.lon_accel = -0.1475
        if right == True: self.dir = 1
        else: self.dir = -1

    def get_bb(self):
        return self.x - self.w / 2, self.y - self.h / 2, self.x + self.w / 2, self.y + self.h / 2

    def update(self):
        self.x = self.x + self.dir * CHARFIRE_SPEED_PPS * game_framework.frame_time

        if self.x < main_state.camera_left - self.w/2 or main_state.camera_left + 800+self.w/2 < self.x or self.y < -10:  # 추락 혹은 맵 이탈시
            self.del_self()
            return

        if self.lon_accel!=0:
            self.lon_speed = self.lon_speed + self.lon_accel + game_framework.frame_time
            if self.lon_speed < -98: self.lon_speed = -98
            self.y = self.y + PIXEL_PER_METER * self.lon_speed * game_framework.frame_time

        self.frame = (self.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 4
    def draw(self):
        self.image.clip_draw((4 + int(self.frame))*16,0,8,8,self.x - main_state.camera_left,self.y- main_state.camera_bottom,self.w,self.h)
    def del_self(self):
        server.char_fires.remove(self)
        game_world.remove_object(self)
        del self

class Mushroom(Object):
    def __init__(self, x, y):
        super(Mushroom, self).__init__(x, y)
        self.w = 1 * PIXEL_PER_METER
        self.h = 1 * PIXEL_PER_METER
        self.lat_speed = MUSHROOM_SPEED_PPS
        self.timer = 50
        self.lon_accel = -0.1475

    def get_bb(self):
        return self.x - self.w / 2, self.y - self.h / 2, self.x + self.w / 2, self.y + self.h / 2

    def update(self):
        if self.timer >0:
            self.timer -= 1
            self.y += 1
            return

        self.x = self.x + self.lat_speed * game_framework.frame_time

        if self.x < main_state.camera_left - self.w/2 or main_state.camera_left + 800+self.w/2 < self.x or self.y < -10:  # 추락 혹은 맵 이탈시
            self.del_self()
            return

        if self.lon_accel!=0:
            self.lon_speed = self.lon_speed + self.lon_accel + game_framework.frame_time
            if self.lon_speed < -98: self.lon_speed = -98
            self.y = self.y + PIXEL_PER_METER * self.lon_speed * game_framework.frame_time

    def do(self, character):
        if(character.power_up == 0):
            character.power_up = 1
            character.h *= 2
        self.del_self()
        return
    def draw(self):
        self.image.clip_draw(0, 64,16,16,self.x - main_state.camera_left,self.y- main_state.camera_bottom,self.w,self.h)
    def del_self(self):
        server.objects.remove(self)
        game_world.remove_object(self)
        del self


class Flower(Object):
    def __init__(self, x, y):
        super(Flower, self).__init__(x, y)
        self.w = 1 * PIXEL_PER_METER
        self.h = 1 * PIXEL_PER_METER
        self.timer = 50
        self.frame = 0
    def get_bb(self):
        return self.x - self.w / 2, self.y - self.h / 2, self.x + self.w / 2, self.y + self.h / 2

    def update(self):
        if self.timer >0:
            self.timer -= 1
            self.y += 1
            return

        self.frame = (self.frame + game_framework.frame_time* FRAMES_PER_ACTION * ACTION_PER_TIME)%4
    def do(self, character):
        if(character.power_up == 0):
            character.h *= 2
        character.power_up = 2

        self.del_self()
        return
    def draw(self):
        self.image.clip_draw(int(self.frame)*16, (4-main_state.stage)*16,16,16,self.x - main_state.camera_left,self.y- main_state.camera_bottom,self.w,self.h)
    def del_self(self):
        server.objects.remove(self)
        game_world.remove_object(self)
        del self