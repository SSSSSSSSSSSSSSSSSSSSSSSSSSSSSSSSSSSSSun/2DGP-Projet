import game_framework
from pico2d import *

import game_world

PIXEL_PER_METER = (50.0 / 1.0)  # 50 pixel 1meter

CHARFIRE_SPEED_MPS = 15    # m/s
CHARFIRE_SPEED_PPS = PIXEL_PER_METER * CHARFIRE_SPEED_MPS

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

class CharFire(Object):
    def __init__(self, x, y, right):
        super(CharFire, self).__init__(x, y)
        self.w = 0.5 * PIXEL_PER_METER
        self.h = 0.5 * PIXEL_PER_METER
        if right == True: self.dir = 1
        else: self.dir = -1

    def get_bb(self):
        return self.x - self.w / 2, self.y - self.h / 2, self.x + self.w / 2, self.y + self.h / 2

    def update(self):
        self.x = self.x + self.dir * CHARFIRE_SPEED_PPS * game_framework.frame_time
        if 0: # 바닥에 닿을 시
            pass
        if 0: # 벽에 닿을 시
            del(self)
        self.frame = (self.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 4
    def draw(self):
        self.image.clip_draw((4 + int(self.frame))*16,0,8,8,self.x,self.y,self.w,self.h)
