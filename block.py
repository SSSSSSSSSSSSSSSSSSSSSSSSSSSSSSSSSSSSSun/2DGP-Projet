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
            self.image.clip_draw(0,128-server.stage*16,16,16,self.x - main_state.camera_left,self.y- main_state.camera_bottom,self.w,self.h)
        if self.type == 1:
            self.image.clip_draw(48,128-server.stage*16,16,16,self.x - main_state.camera_left,self.y- main_state.camera_bottom,self.w,self.h)
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
        pass
    def draw(self):
        if self.x < main_state.camera_left-self.w/2 and main_state.camera_left+800+self.w/2 < self.x: return
        self.image.clip_draw(16+self.type*16,128-server.stage*16,16,16,self.x - main_state.camera_left,self.y- main_state.camera_bottom,self.w,self.h)
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
        super(Box, self).__init__(x, y)
        self.w = 1 * PIXEL_PER_METER
        self.h = 1 * PIXEL_PER_METER
        self.frame = 0
    def get_bb(self):
        return self.x-self.w/2- main_state.camera_left, self.y-self.h/2, self.x+self.w/2- main_state.camera_left, self.y+self.h/2
    def update(self):
        if self.x < main_state.camera_left-self.w/2 and main_state.camera_left+800+self.w/2 < self.x: return
        if self.x < main_state.camera_left - self.w/2:
            self.del_self()
            return

        self.frame = (self.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 4
    def do(self):
        pass
    def draw(self):
        if self.x < main_state.camera_left-self.w/2 and main_state.camera_left+800+self.w/2 < self.x: return
        self.image.clip_draw(int(self.frame)*16,32,16,16,self.x - main_state.camera_left,self.y- main_state.camera_bottom,self.w,self.h)
    def del_self(self):
        server.blocks[self.x].remove(self)
        game_world.remove_object(self)