import game_framework
from pico2d import *
import main_state
import game_world
import server

PIXEL_PER_METER = (50.0 / 1.0)  # 50 pixel 1meter


# Action Speed
TIME_PER_ACTION = 0.8
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION = 3

class Block():
    image = None
    def __init__(self,x,y):
        if Block.image == None:
           Block.image = load_image('resource\\Block_sprite.png')
        self.x = x
        self.y = y


class Platform(Block):
    def __init__(self,x,y,type):
        super(Platform, self).__init__(x, y)
        self.w = 1 * PIXEL_PER_METER
        self.h = 1 * PIXEL_PER_METER
        self.type = type
    def get_bb(self):
        return self.x-self.w/2, self.y-self.h/2, self.x+self.w/2, self.y+self.h/2
    def update(self):
        if self.x < main_state.camera_left-self.w/2 and main_state.camera_left+800+self.w/2 < self.x: return
        if self.x < main_state.camera_left - self.w/2:
            self.del_self()
            return
    def do(self):
        pass
    def draw(self):
        if self.x < main_state.camera_left-self.w/2 and main_state.camera_left+800+self.w/2 < self.x: return

        if self.type == 0:
            self.image.clip_draw(0,128-server.level*16,16,16,self.x - main_state.camera_left,self.y- main_state.camera_bottom,self.w,self.h)
        if self.type == 1:
            self.image.clip_draw(48,128-server.level*16,16,16,self.x - main_state.camera_left,self.y- main_state.camera_bottom,self.w,self.h)
    def del_self(self):
        server.blocks[self.x].remove(self)
        game_world.remove_object(self)

class Brick(Block):
    def __init__(self,x,y, type):
        super(Brick, self).__init__(x, y)
        self.w = 1 * PIXEL_PER_METER
        self.h = 1 * PIXEL_PER_METER
        self.type = type # 1번 : 윗벽돌 / 2번 : 중간 벽돌
    def get_bb(self):
        return self.x-self.w/2, self.y-self.h/2, self.x+self.w/2, self.y+self.h/2
    def update(self):
        if self.x < main_state.camera_left-self.w/2 and main_state.camera_left+800+self.w/2 < self.x: return
        if self.x < main_state.camera_left - self.w/2:
            self.del_self()
            return
    def do(self):
        if(server.character.power_up):
            self.del_self()
            main_state.score += 10
    def draw(self):
        if self.x < main_state.camera_left-self.w/2 and main_state.camera_left+800+self.w/2 < self.x: return
        self.image.clip_draw(16+self.type*16,128-server.level*16,16,16,self.x - main_state.camera_left,self.y- main_state.camera_bottom,self.w,self.h)
    def del_self(self):
        server.blocks[self.x].remove(self)
        game_world.remove_object(self)

class Box(Block):
    def __init__(self,x,y,l):
        super(Box, self).__init__(x, y)
        self.w = 1 * PIXEL_PER_METER
        self.h = 1 * PIXEL_PER_METER
        self.contents = [] + l
        self.frame = 0
    def get_bb(self):
        return self.x-self.w/2, self.y-self.h/2, self.x+self.w/2, self.y+self.h/2
    def update(self):
        if self.x < main_state.camera_left-self.w/2 and main_state.camera_left+800+self.w/2 < self.x: return
        if self.x < main_state.camera_left - self.w/2:
            self.del_self()
            return

        self.frame = (self.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 4
    def do(self):
        if len(self.contents) > 0:
            item = self.contents.pop()
            server.objects.append(item)
            game_world.add_object(item,1)

    def draw(self):
        if self.x < main_state.camera_left-self.w/2 and main_state.camera_left+800+self.w/2 < self.x: return
        if len(self.contents) > 0:
            self.image.clip_draw(int(self.frame)*16,48,16,16,self.x - main_state.camera_left,self.y- main_state.camera_bottom,self.w,self.h)
        else:
            self.image.clip_draw(48,0,16,16,self.x - main_state.camera_left,self.y- main_state.camera_bottom,self.w,self.h)
    def del_self(self):
        server.blocks[self.x].remove(self)
        game_world.remove_object(self)

class Coin(Block):
    def __init__(self,x,y):
        super(Coin, self).__init__(x, y)
        self.w = 1 * PIXEL_PER_METER
        self.h = 1 * PIXEL_PER_METER
        self.frame = 0
    def get_bb(self):
        return self.x-self.w/2, self.y-self.h/2, self.x+self.w/2, self.y+self.h/2
    def update(self):
        if self.x < main_state.camera_left-self.w/2 and main_state.camera_left+800+self.w/2 < self.x: return
        if self.x < main_state.camera_left - self.w/2:
            self.del_self()
            return

        self.frame = (self.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 4
    def do(self):
        main_state.score += 100
    def draw(self):
        if self.x < main_state.camera_left-self.w/2 and main_state.camera_left+800+self.w/2 < self.x: return
        self.image.clip_draw(int(self.frame)*16,16,16,16,self.x - main_state.camera_left,self.y- main_state.camera_bottom,self.w,self.h)
    def del_self(self):
        server.blocks[self.x].remove(self)
        game_world.remove_object(self)

class Flag(Block):
    def __init__(self, x, y, kind):
        super(Flag, self).__init__(x, y)
        self.w = 1 * PIXEL_PER_METER
        self.h = 1 * PIXEL_PER_METER
        self.kind = kind


    def get_bb(self):

        return self.x - self.w / 2, self.y - self.h / 2, self.x + self.w / 2, self.y + self.h / 2

    def update(self):
        pass

    def do(self):
        pass

    def draw(self):
        if self.kind != 2:
            self.image.clip_draw(16*self.kind, 0, 16,16,self.x - main_state.camera_left,self.y- main_state.camera_bottom,self.w,self.h)
        else:
            self.image.clip_draw(16*self.kind, 0, 16,16,self.x - main_state.camera_left+self.w/2,self.y- main_state.camera_bottom,self.w,self.h)

    def del_self(self):
        server.objects.remove(self)
        game_world.remove_object(self)

class Axe(Block):
    def __init__(self, x, y):
        super(Axe, self).__init__(x, y)
        self.w = 1 * PIXEL_PER_METER
        self.h = 1 * PIXEL_PER_METER

    def get_bb(self):

        return self.x - self.w / 2, self.y - self.h / 2, self.x + self.w / 2, self.y + self.h / 2

    def update(self):
        self.frame = (self.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 4

    def do(self):
        pass

    def draw(self):
        self.image.clip_draw(int(self.frame)*16*server.level, 32, 16,16,self.x - main_state.camera_left,self.y- main_state.camera_bottom,self.w,self.h)
    def del_self(self):
        server.objects.remove(self)
        game_world.remove_object(self)

class Pipe(Block):
    def __init__(self,x,y,dir,num):
        super(Pipe, self).__init__(x, y)
        self.w = 1 * PIXEL_PER_METER
        self.h = 1 * PIXEL_PER_METER
        self.dir = dir
        self.num = num
    def get_bb(self):

        return self.x-self.w/2, self.y-self.h/2, self.x+self.w/2, self.y+self.h/2
    def update(self):
        if self.x < main_state.camera_left-self.w/2 and main_state.camera_left+800+self.w/2 < self.x: return
        if self.x < main_state.camera_left - self.w/2:
            self.del_self()
            return
    def do(self):
        pass
    def draw(self):
        if self.x < main_state.camera_left-self.w/2 and main_state.camera_left+800+self.w/2 < self.x: return
        x = None
        if self.dir == 0: x = 1
        elif self.dir == 1: x = 3
        elif self.dir == 2: x= 0
        else: x =2
        nx, ny = None, None
        if self.num == 0:
            nx=0
            ny=0
        elif self.num == 1:
            nx=1
            ny=0
        elif self.num == 2:
            nx=0
            ny=1
        else:
            nx=1
            ny=1
        self.image.clip_draw(64+16*nx+32*x,128-server.level*32-16*ny,16,16,self.x - main_state.camera_left,self.y- main_state.camera_bottom,self.w,self.h)

    def del_self(self):
        server.blocks[self.x].remove(self)
        game_world.remove_object(self)