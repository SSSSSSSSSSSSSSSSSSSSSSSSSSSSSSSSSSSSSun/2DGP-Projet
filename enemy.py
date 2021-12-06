from random import randint


import game_framework
from pico2d import *
import main_state
import game_world
from object import *
import server

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
        self.w = 0.9 * PIXEL_PER_METER
        self.h = 0.9 * PIXEL_PER_METER
        self.hp = 1
        self.timer = -1

    def get_bb(self):
        return self.x-self.w/2, self.y-self.h/2, self.x+self.w/2, self.y+self.h/2

    def update(self):
        if self.timer==0:
            self.del_self()
            return
        elif self.timer > 0:
            self.timer -= 1

        if self.x < main_state.camera_left - self.w/2:
            self.del_self()
            return

        if self.x < main_state.camera_left-self.w/2 and main_state.camera_left+main_state.window_width+self.w/2 < self.x: return
        if self.lon_accel!=0:
            self.lon_speed = self.lon_speed + self.lon_accel + game_framework.frame_time
            if self.lon_speed < -98: self.lon_speed = -98
            self.y = self.y + PIXEL_PER_METER * self.lon_speed * game_framework.frame_time
        self.x = self.x + self.lat_speed * RUN_SPEED_PPS * game_framework.frame_time

        if self.y < -10:    # 추락시
            self.del_self()
            return
        if self.hp == 0:
            self.frame = 5
            if self.timer < 0:
                self.timer = 100
        elif self.hp <0 and self.timer < 0: self.timer = 100
        else:
            self.frame = (self.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 2
    def draw(self):
        if self.x < main_state.camera_left-self.w/2 and main_state.camera_left+800+self.w/2 < self.x: return

        if self.hp < 0:
            self.image.clip_composite_draw(0,240,16,16,-(100-self.timer) * 3.141592 / 270, '', self.x - main_state.camera_left, self.y- main_state.camera_bottom, self.w, self.h)
            return

        if(self.right):
            self.image.clip_draw((7-int(self.frame)) * 16, 112, 16, 16, self.x - main_state.camera_left, self.y- main_state.camera_bottom, self.w, self.h)
        else:
            self.image.clip_draw(int(self.frame) * 16, 240, 16, 16, self.x - main_state.camera_left, self.y- main_state.camera_bottom,self.w,self.h)

    def del_self(self):
            main_state.score += 50
            server.enemys.remove(self)
            game_world.remove_object(self)

class Black_Goomba(Enemy):
    def __init__(self, x, y):
        super(Black_Goomba, self).__init__(x, y)
        self.lat_speed = -0.1
        self.w = 0.9 * PIXEL_PER_METER
        self.h = 0.9 * PIXEL_PER_METER
        self.hp = 1
        self.timer = -1

    def get_bb(self):
        return self.x-self.w/2, self.y-self.h/2, self.x+self.w/2, self.y+self.h/2

    def update(self):
        if self.timer==0:
            self.del_self()
            return
        elif self.timer > 0:
            self.timer -= 1

        if self.x < main_state.camera_left - self.w/2:
            self.del_self()
            return

        if self.x < main_state.camera_left-self.w/2 and main_state.camera_left+main_state.window_width+self.w/2 < self.x: return
        if self.lon_accel!=0:
            self.lon_speed = self.lon_speed + self.lon_accel + game_framework.frame_time
            if self.lon_speed < -98: self.lon_speed = -98
            self.y = self.y + PIXEL_PER_METER * self.lon_speed * game_framework.frame_time
        self.x = self.x + self.lat_speed * RUN_SPEED_PPS * game_framework.frame_time

        if self.y < -10:    # 추락시
            self.del_self()
            return
        if self.hp == 0:
            shell = Shell(self.x, self.y, 1)
            server.objects.append(shell)

            game_world.add_object(shell, 4)
            self.del_self()
            return
        elif self.hp < 0 and self.timer <0:
            self.timer = 100
        else:
            self.frame = (self.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 2
    def draw(self):
        if self.x < main_state.camera_left-self.w/2 and main_state.camera_left+800+self.w/2 < self.x: return

        if self.hp < 0:
            self.image.clip_composite_draw(0,192,16,16,-(100-self.timer) * 3.141592 / 270, '', self.x - main_state.camera_left, self.y- main_state.camera_bottom, self.w, self.h)
            return

        if(self.right):
            self.image.clip_draw((7-int(self.frame)) * 16, 64, 16, 16, self.x - main_state.camera_left, self.y- main_state.camera_bottom, self.w, self.h)
        else:
            self.image.clip_draw(int(self.frame) * 16, 192, 16, 16, self.x - main_state.camera_left, self.y- main_state.camera_bottom,self.w,self.h)

    def del_self(self):
        main_state.score += 50
        server.enemys.remove(self)
        game_world.remove_object(self)

class Turtle(Enemy):
    def __init__(self, x, y, wing):
        super(Turtle, self).__init__(x, y)
        self.lat_speed = -0.1
        self.wing = wing   # 날개가 달려 있는지
        self.w = 0.9  * PIXEL_PER_METER
        self.h = 2 * 0.9 * PIXEL_PER_METER
        self.hp = 1
        self.timer = -1
    def get_bb(self):
        return self.x-self.w/2, self.y-self.h/2, self.x+self.w/2, self.y+self.h/4

    def update(self):
        if self.timer==0:
            self.del_self()
            return
        elif self.timer > 0:
            self.timer -= 1
            self.x += 1

        if self.x < main_state.camera_left - self.w/2:
            self.del_self()
            return
        if self.x < main_state.camera_left-self.w/2 and main_state.camera_left+main_state.window_width+self.w/2 < self.x: return

        if self.lon_accel!=0:
            self.lon_speed = self.lon_speed + self.lon_accel + game_framework.frame_time
            if self.lon_speed < -98: self.lon_speed = -98
            self.y = self.y + PIXEL_PER_METER * self.lon_speed * game_framework.frame_time
        self.x = self.x + self.lat_speed * RUN_SPEED_PPS  * game_framework.frame_time
        if 0:   # 추후 날개가 있을 시 점프하는 코드 추가해야함
            pass# 추후 날개가 있을 시 점프하는 코드 추가해야함
        if self.y < -10:  # 추락시
            self.del_self()
            return
        if self.hp == 0:


            shell = Shell(self.x, self.y-self.h/2, 0)
            server.objects.append(shell)

            game_world.add_object(shell, 4)
            self.del_self()
            return
        elif self.hp < 0 and self.timer <0:
            self.timer = 100
        else:
            self.frame = (self.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 2
            if self.wing:
                self.frame+=3
    def draw(self):
        if self.x < main_state.camera_left-self.w/2 and main_state.camera_left+main_state.window_width+self.w/2 < self.x: return

        if self.hp < 0:
            self.image.clip_composite_draw(0,208,16,32,-(100-self.timer) * 3.141592 / 270, '', self.x - main_state.camera_left, self.y- main_state.camera_bottom, self.w, self.h)
            return

        if (self.right):
            self.image.clip_draw((7 - int(self.frame)) * 16, 80, 16, 32, self.x - main_state.camera_left, self.y- main_state.camera_bottom, self.w, self.h)
        else:
            self.image.clip_draw(int(self.frame) * 16, 208, 16, 32, self.x - main_state.camera_left, self.y- main_state.camera_bottom, self.w, self.h)
    def del_self(self):
        main_state.score += 50
        server.enemys.remove(self)
        game_world.remove_object(self)

class Hammer(Enemy):
    def __init__(self,x,y):
        super(Hammer, self).__init__(x, y)
        self.skill_cooltime = 0
        self.w = 0.9 * PIXEL_PER_METER
        self.h = 2 * 0.9 * PIXEL_PER_METER
        self.hp = 1
        self.timer = -1
    def get_bb(self):
        return self.x - self.w / 2, self.y - self.h / 2, self.x + self.w / 2, self.y + self.h / 4

    def update(self):

        if self.timer==0:
            self.del_self()
            return
        elif self.timer > 0:
            self.timer -= 1
            self.x += 1


        if self.x < main_state.camera_left - self.w/2:
            self.del_self()
            return
        if self.x < main_state.camera_left-self.w/2 and main_state.camera_left+main_state.window_width+self.w/2 < self.x: return

        if self.lon_accel!=0:
            self.lon_speed = self.lon_speed + self.lon_accel + game_framework.frame_time
            if self.lon_speed < -98: self.lon_speed = -98
            self.y = self.y + PIXEL_PER_METER * self.lon_speed * game_framework.frame_time

        if (self.right == 0) and (server.character.x > self.x):
            self.right = True
        elif (self.right == 1) and (server.character.x < self.x):
            self.right = False
        self.skill_cooltime = (self.skill_cooltime + 1) % 1000
        if self.skill_cooltime % 200 == 0:

            hammer = Obj_Hammer(self.x, self.y, 98*1.5, self.right)
            server.objects.append(hammer)
            game_world.add_object(hammer, 3)

        if (self.skill_cooltime)%500== 0:
            self.y += 1
            self.lon_speed = 10
        if self.y < -10:  # 추락시
            self.del_self()
            return
        if self.hp == 0:
            shell = Shell(self.x, self.y-self.h/2, 0)
            server.objects.append(shell)

            game_world.add_object(shell, 4)
            self.del_self()
            return
        elif self.timer < 0 and self.hp < 0:
            self.timer = 100
        else:
            self.frame = (self.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 2
    def draw(self):
        if self.x < main_state.camera_left-self.w/2 and main_state.camera_left+main_state.window_width+self.w/2 < self.x: return

        if self.hp < 0:
            self.image.clip_composite_draw(0,160,16,32,-(100-self.timer) * 3.141592 / 270, '', self.x - main_state.camera_left, self.y- main_state.camera_bottom, self.w, self.h)
            return

        if self.right:
            self.image.clip_draw((7 - int(self.frame)) * 16, 32, 16, 32, self.x -  main_state.camera_left, self.y- main_state.camera_bottom, self.w, self.h)
        else:
            self.image.clip_draw(int(self.frame) * 16, 160, 16, 32, self.x - main_state.camera_left, self.y- main_state.camera_bottom, self.w, self.h)
    def del_self(self):
        server.enemys.remove(self)
        game_world.remove_object(self)
        main_state.score += 100

class Boss(Enemy):
    def __init__(self, x, y):
        super(Boss, self).__init__(x, y)
        self.hp = 20
        self.skill_cooltime = 0
        self.w = 2 * 0.9 * PIXEL_PER_METER
        self.h = 2 * 0.9 * PIXEL_PER_METER

    def get_bb(self):
        return self.x-self.w/2, self.y-self.h/2, self.x+self.w/2, self.y+self.h/2

    def update(self):
        if self.x < main_state.camera_left - self.w/2:
            self.del_self()
            return
        if self.x < main_state.camera_left-self.w/2 and main_state.camera_left+main_state.window_width+self.w/2 < self.x: return

        if self.lon_accel!=0:
            self.lon_speed = self.lon_speed + self.lon_accel + game_framework.frame_time
            if self.lon_speed < -98: self.lon_speed = -98
            self.y = self.y + PIXEL_PER_METER * self.lon_speed * game_framework.frame_time

        self.x = self.x + self.lat_speed
        if self.right == 0  and server.character.x > self.x:
            self.right = True
        elif self.right == 1 and server.character.x < self.x:
            self.right = False

        self.skill_cooltime = (self.skill_cooltime + 1) % 500
        if self.skill_cooltime==0 :
            i = randint(0,2)

            if i==0:
                for i in range(-1,1+1):
                    fire = BossFire(self.x, self.y, PIXEL_PER_METER/500 * i, self.right)
                    server.objects.append(fire)
                    game_world.add_object(fire, 3)
            elif i==1:
                self.y += 1
                self.lon_speed = 10
            else:
                self.y += 1
                self.lon_speed = 15
            
        if self.y < -10:  # 추락시
            self.del_self()
            return
        if self.hp == 0:
            self.frame = 1
        else:
            self.frame = (self.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 4
    def draw(self):
        if self.x < main_state.camera_left-self.w/2 and main_state.camera_left+main_state.window_width+self.w/2 < self.x: return
        if (self.right):
            self.image.clip_draw((6 - int(self.frame)*2) * 16, 0, 32, 32, self.x - main_state.camera_left, self.y- main_state.camera_bottom, self.w, self.h)
        else:
            self.image.clip_draw(int(self.frame) * 32, 128, 32, 32, self.x -main_state.camera_left, self.y- main_state.camera_bottom, self.w, self.h)
    def del_self(self):
        server.enemys.remove(self)
        game_world.remove_object(self)
        main_state.score += 1000
