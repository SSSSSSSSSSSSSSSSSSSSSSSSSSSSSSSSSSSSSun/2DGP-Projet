from random import randint

import game_framework
from pico2d import *

import game_world

PIXEL_PER_METER = (50.0 / 1.0)  # 50 pixel 1meter
RUN_SPEED_MPS = 10
RUN_SPEED_PPS = PIXEL_PER_METER * RUN_SPEED_MPS

# Action Speed
TIME_PER_ACTION = 0.5
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION = 3

class Enemy:
    image = None
    w = None
    h = None # 크기
    hp = None   # 체력. 0되면 사망
    def __init__(self, x, y):
        if Enemy.image == None:
            Enemy.image = load_image('resource\\Enemies_sprite.png')
        self.x = x
        self.y = y  # 위치
        self.lat_speed = 0  # 횡방향 속도 / right 방향이 +
        self.lon_speed = 0  # 종방향 속도 / up 방향이 +
        self.lon_accel = 0 # 종방향 가속도
        self.right = False   # 우측방향을 바라보고 있는지
        self.frame = 0

class Goomba(Enemy):
    def __init__(self, x, y):
        super(Goomba, self).__init__(x, y)
        self.lat_speed = -0.1
        self.w = 1 * PIXEL_PER_METER
        self.h = 1 * PIXEL_PER_METER
        self.hp = 1

    def update(self):
        if 1:       #추후 플레이어 시야 안에 들어올 시 움직이는 조건 추가
            if 0:    # 추후 벽에 부딪힐시 반대로 움직이는 조건 추가
                self.lat_speed = - self.lat_speed
                self.right = True
            self.x = self.x + self.lat_speed * RUN_SPEED_PPS * game_framework.frame_time

        if self.y < -10:    # 추락시
            del self

        if self.hp == 0:
            self.frame = 5
        else:
            self.frame = (self.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 2
    def draw(self):
        if(self.right):
            self.image.clip_draw((7-int(self.frame)) * 16, 112, 16, 16, self.x, self.y, self.w, self.h)
        else:
            self.image.clip_draw(int(self.frame) * 16, 240, 16, 16, self.x, self.y,self.w,self.h)

class Turtle(Enemy):
    def __init__(self, x, y, wing):
        super(Turtle, self).__init__(x, y)
        self.lat_speed = -0.1
        self.wing = wing   # 날개가 달려 있는지
        self.w = 1  * PIXEL_PER_METER
        self.h = 2 * PIXEL_PER_METER
        self.hp = 1
    def update(self):
        if 1:  # 추후 플레이어 시야 안에 들어올 시 움직이는 조건 추가
            if 0:    # 추후 벽에 부딪힐시 반대로 움직이는 조건 추가
                self.lat_speed = - self.lat_speed
                self.right = True
            self.x = self.x + self.lat_speed * RUN_SPEED_PPS  * game_framework.frame_time
            if 0:   # 추후 날개가 있을 시 점프하는 코드 추가해야함
                pass# 추후 날개가 있을 시 점프하는 코드 추가해야함
        if self.y < -10:  # 추락시
            del self
        if self.hp == 0:
            self.frame = 5
        else:
            self.frame = (self.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 2
            if self.wing:
                self.frame+=3
    def draw(self):
        if (self.right):
            self.image.clip_draw((7 - int(self.frame)) * 16, 80, 16, 32, self.x, self.y, self.w, self.h)
        else:
            self.image.clip_draw(int(self.frame) * 16, 208, 16, 32, self.x, self.y, self.w, self.h)

class Hammer(Enemy):
    def __init__(self,x,y):
        super(Hammer, self).__init__(x, y)
        self.skill_cooltime = 0
        self.w = 1 * PIXEL_PER_METER
        self.h = 2 * PIXEL_PER_METER
        self.hp = 1
    def update(self):
        if 1:  # 추후 플레이어 시야 안에 들어올 시 움직이는 조건 추가
            if (self.right == 0) and (game_world.objects[4][0].x > self.x):
                self.right = True
            elif (self.right == 1) and (game_world.objects[4][0].x < self.x):
                self.right = False
            self.skill_cooltime = (self.skill_cooltime + 1) % 100
            if self.skill_cooltime == 0:
                pass #물건 투척
            if (self.skill_cooltime+randint(1,100+1))%10 == 0:
                pass #점프하는 코드 추가
        if self.y < -10:  # 추락시
            del self

        if self.hp == 0:
            self.frame = 5
        else:
            self.frame = (self.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 2
    def draw(self):

        if (self.right):
            self.image.clip_draw((7 - int(self.frame)) * 16, 32, 16, 32, self.x, self.y, self.w, self.h)
        else:
            self.image.clip_draw(int(self.frame) * 16, 160, 16, 32, self.x, self.y, self.w, self.h)

class Boss(Enemy):
    def __init__(self, x, y):
        super(Boss, self).__init__(x, y)
        self.hp = 20
        self.skill_cooltime = 0
        self.w = 2 * PIXEL_PER_METER
        self.h = 2 * PIXEL_PER_METER
    def update(self):
        if 1:  # 추후 플레이어 시야 안에 들어올 시 움직이는 조건 추가
            self.x = self.x + self.lat_speed
            if self.right == 0  and game_world.objects[4][0].x > self.x:
                self.right = True
            elif self.right == 1 and game_world.objects[4][0].x < self.x:
                self.right = False

            self.skill_cooltime = (self.skill_cooltime + 1) % 1000
            if self.skill_cooltime==0 :
                i = randint(0, 3)
                if i==0:
                    pass #불쏘는 코드
                elif i==1:
                    pass  # 점프하는 코드
                else:
                    pass  # 큰점프하는 코드
            
        if self.y < -10:  # 추락시
           del self

        if self.hp == 0:
            self.frame = 1
        else:
            self.frame = (self.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 4
    def draw(self):

        if (self.right):
            self.image.clip_draw((6 - int(self.frame)*2) * 16, 0, 32, 32, self.x, self.y, self.w, self.h)
        else:
            self.image.clip_draw(int(self.frame) * 32, 128, 32, 32, self.x, self.y, self.w, self.h)

