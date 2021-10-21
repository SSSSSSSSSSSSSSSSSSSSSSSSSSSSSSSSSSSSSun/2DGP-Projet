from object import *

class Character:
    def __init__(self):
        self.x = 200; self.y = 200  # 위치
        self.w = 64; self.h = 64    # 크기
        self.dir = 0   # 이동하려는 방향. 1 = right/-1 = left
        self.lat_speed = 0  # 횡방향 속도 / right 방향이 +
        self.lat_accel = 0   # 횡방향 가속도
        self.lon_speed = 0  # 종방향 속도 / up 방향이 +
        self.lon_accel = 0 # 종방향 가속도
        self.lat_jerk = 0   # 종방향 가가속도
        self.jump = False  # 점프 여부
        self.power_up = 0    # 파워업 상태
        self.clip_l = 0; self.clip_b = 64;
        self.clip_w = 16; self.clip_h = 16;
        self.right = True   # 우측방향을 바라보고 있는지
        self.frame = 0
        self.frame_wait = 0

    def move(self):
        if (-2 <= self.lat_speed) and (self.lat_speed <= 2):
            if self.dir > 0:
                self.lat_accel = 0.01

            elif self.dir < 0:

                self.lat_accel = -0.01
            elif self.lat_speed == 0:
                self.lat_accel = 0
            else:
                if self.lat_speed > 0:
                    if self.lat_speed < 0.01:
                        self.lat_speed = 0
                        self.lat_accel = 0
                    else: self.lat_accel = -0.01

                else:
                    if self.lat_speed > -0.01:
                        self.lat_speed = 0
                        self.lat_accel = 0
                    else: self.lat_accel = 0.01


        else:
            if self.dir == 0:
                if self.lat_speed > 0:
                    self.lat_accel = -0.01
                else:
                    self.lat_accel = 0.01
            elif self.dir/abs(self.dir) == self.lat_speed/abs(self.lat_speed):
                self.lat_accel = 0
            else:
                if self.dir / abs(self.dir) > 0:
                    self.lat_accel = 0.01

                else:
                    self.lat_accel = -0.01

        if self.lat_speed>0: self.right = True
        elif self.lat_speed<0: self.right=False
        self.lat_speed = self.lat_speed + self.lat_accel
        self.x = self.x + self.lat_speed

    def sprite(self):
        if self.lon_speed != 0:
            self.clip_l = 80
        else:
            if self.dir == 0 and self.lat_speed == 0:
                self.clip_l = 0
            elif self.dir != 0 and self.lat_speed != 0:
                if self.dir/abs(self.dir) != self.lat_speed/abs(self.lat_speed):
                    self.clip_l = 64
                else:
                    self.frame_wait = (self.frame_wait + 1) % 30
                    if self.frame_wait == 0:
                        self.frame = (self.frame+1)%3
                        self.clip_l = 16*self.frame
            else:
                self.frame_wait = (self.frame_wait + 1) % 30
                if self.frame_wait == 0:
                    self.frame = (self.frame + 1) % 3
                    self.clip_l = 16 * self.frame

        if self.power_up:
            self.clip_h = 32
            self.h = 128
        else:
            self.clip_h = 16
            self.h = 64

    def attack(self):
        if self.power_up == 2 and self.dir * self.lat_speed >= 0:
            if self.right :
                objects.append(CharFire(self.x,self.y+self.h/2,1))
            else:
                objects.append(CharFire(self.x, self.y + self.h / 2, -1))

char = Character()
