from random import randint
from character import char
class Enemy:
    w = None; h = None # 크기
    hp = None   # 체력. 0되면 사망
    def __init__(self,x,y):
        self.x = x; self.y = y  # 위치

        self.lat_speed = 0  # 횡방향 속도 / right 방향이 +
        self.lon_speed = 0  # 종방향 속도 / up 방향이 +
        self.lon_accel = 0 # 종방향 가속도
        self.jump = False  # 점프 여부
        self.right = False   # 우측방향을 바라보고 있는지
        self.frame = 0
        self.frame_wait = 0

class Goomba(Enemy):
    def __init__(self,x,y):
        super(Goomba, self).__init__(x,y)
        self.lat_speed = -0.1
        self.w =64; self.h = 64
        self.hp = 1
    def attack(self):
        if 1:       #추후 플레이어 시야 안에 들어올 시 움직이는 조건 추가
            if 0:    # 추후 벽에 부딪힐시 반대로 움직이는 조건 추가
                self.lat_speed = - self.lat_speed
                self.right = True
            self.x = self.x + self.lat_speed

        if self.y < -10:    # 추락시
            del self

    def sprite(self):
        if self.hp == 0 :
            self.frame = 5
        else:
            self.frame_wait = (self.frame_wait+1)%100
            if(self.frame_wait == 0):
                self.frame = (self.frame+1)%2

class Turtle(Enemy):
    def __init__(self,x,y, wing):
        super(Turtle, self).__init__(x,y)
        self.lat_speed = -0.1
        self.wing = wing;   # 날개가 달려 있는지
        self.w = 64;   self.h = 128
        self.hp = 1
    def attack(self):
        if 1:  # 추후 플레이어 시야 안에 들어올 시 움직이는 조건 추가
            if 0:    # 추후 벽에 부딪힐시 반대로 움직이는 조건 추가
                self.lat_speed = - self.lat_speed
                self.right = True
            self.x = self.x + self.lat_speed
            if 0:   # 추후 날개가 있을 시 점프하는 코드 추가해야함
                pass# 추후 날개가 있을 시 점프하는 코드 추가해야함
        if self.y < -10:  # 추락시
            del self

    def sprite(self):
        if self.hp == 0:
            self.frame = 5
        else:
            self.frame_wait = (self.frame_wait + 1) % 100
            if (self.frame_wait == 0):
                if(self.wing):
                    self.frame = (self.frame+1)%2 + 3
                else:
                    self.frame = (self.frame+1)%2

class Hammer(Enemy):
    def __init__(self,x,y):
        super(Hammer, self).__init__(x,y)
        self.skill_cooltime = 0
        self.w = 64;   self.h = 128
        self.hp = 1
    def attack(self):
        if 1:  # 추후 플레이어 시야 안에 들어올 시 움직이는 조건 추가
            if (self.right == 0) and (char.x > self.x):
                self.right = True
            elif (self.right == 1) and (char.x < self.x):
                self.right = False
            self.skill_cooltime = (self.skill_cooltime + 1) % 100
            if self.skill_cooltime == 0:
                pass #물건 투척
            if (self.skill_cooltime+randint(1,100+1))%10 == 0:
                pass #점프하는 코드 추가
        if self.y < -10:  # 추락시
            del self
    def sprite(self):
        if self.hp == 0:
            self.frame = 5
        else:
            self.frame_wait = (self.frame_wait + 1) % 100
            if (self.frame_wait == 0):
                self.frame = (self.frame+1)%4

class Boss(Enemy):
    def __init__(self,x,y):
        super(Boss, self).__init__(x,y)
        self.hp = 20
        self.skill_cooltime=0
        self.w = 128;   self.h = 128
    def attack(self):
        if 1:  # 추후 플레이어 시야 안에 들어올 시 움직이는 조건 추가
            self.x = self.x + self.lat_speed
            if (self.right == 0 ) and (char.x > self.x):
                self.right = True
            elif(self.right == 1) and (char.x < self.x):
                self.right = False

            self.skill_cooltime = (self.skill_cooltime + 1)%1000
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
    def sprite(self):
        if self.hp == 0:
            self.frame = 1
        else:
            self.frame_wait = (self.frame_wait + 1) % 1000
            if (self.frame_wait == 0):
                self.frame = (self.frame+1)%4

enemys = [Goomba(400,200),Turtle(500,200,False),Hammer(600,200),Boss(700,200)]