import game_framework
import main_state
from pico2d import *

PIXEL_PER_METER = (50.0 / 1.0)  # 50 pixel 1meter

class BGround():
    image = None
    def __init__(self,x,y):
        if BGround.image == None:
           BGround.image = load_image('resource\\bg.png')
        self.x = x
        self.y = y

class Big_grass(BGround):
    def __init__(self,x,y):
        super(Big_grass, self).__init__(x,y)
        self.w = 5 * PIXEL_PER_METER
        self.h = 1 * PIXEL_PER_METER
    def update(self):
        if self.x < main_state.camera_left - self.w/2:
            self.del_self()
    def draw(self):
        x = self.x - main_state.camera_left
        y = self.y- main_state.camera_bottom
        image_w = int(self.w / PIXEL_PER_METER * 16)
        image_h = int(self.h / PIXEL_PER_METER * 16)
        self.image.clip_draw(0,160,image_w, image_h,x,y,self.w,self.h)
    def del_self(self):
        server.bg.remove(self)
        game_world.remove_object(self)
class grass(BGround):
    def __init__(self,x,y):
        super(grass, self).__init__(x,y)
        self.w = 3 * PIXEL_PER_METER
        self.h = 1 * PIXEL_PER_METER
    def update(self):
        if self.x < main_state.camera_left - self.w/2:
            self.del_self()
    def draw(self):
        x = self.x - main_state.camera_left
        y = self.y- main_state.camera_bottom
        image_w = int(self.w / PIXEL_PER_METER * 16)
        image_h = int(self.h / PIXEL_PER_METER * 16)
        self.image.clip_draw(0,144,image_w, image_h,x,y,self.w,self.h)
    def del_self(self):
        server.bg.remove(self)
        game_world.remove_object(self)
class Big_cloud(BGround):
    def __init__(self,x,y):
        super(Big_cloud, self).__init__(x,y)
        self.w = 4 * PIXEL_PER_METER
        self.h = 2 * PIXEL_PER_METER
    def update(self):
        if self.x < main_state.camera_left - self.w/2:
            self.del_self()
    def draw(self):
        x = self.x - main_state.camera_left
        y = self.y- main_state.camera_bottom
        image_w = int(self.w / PIXEL_PER_METER * 16)
        image_h = int(self.h / PIXEL_PER_METER * 16)
        self.image.clip_draw(0,80,image_w, image_h,x,y,self.w,self.h)
    def del_self(self):
        server.bg.remove(self)
        game_world.remove_object(self)
class cloud(BGround):
    def __init__(self,x,y):
        super(cloud, self).__init__(x,y)
        self.w = 3 * PIXEL_PER_METER
        self.h = 2 * PIXEL_PER_METER
    def update(self):
        if self.x < main_state.camera_left - self.w/2:
            self.del_self()
    def draw(self):
        x = self.x - main_state.camera_left
        y = self.y- main_state.camera_bottom
        image_w = int(self.w / PIXEL_PER_METER * 16)
        image_h = int(self.h / PIXEL_PER_METER * 16)
        self.image.clip_draw(0,112,image_w, image_h,x,y,self.w,self.h)
    def del_self(self):
        server.bg.remove(self)
        game_world.remove_object(self)
class Big_tree(BGround):
    def __init__(self,x,y):
        super(Big_tree, self).__init__(x,y)
        self.w = 1 * PIXEL_PER_METER
        self.h = 3 * PIXEL_PER_METER
    def update(self):
        if self.x < main_state.camera_left - self.w/2:
            self.del_self()
    def draw(self):
        x = self.x - main_state.camera_left
        y = self.y- main_state.camera_bottom
        image_w = int(self.w / PIXEL_PER_METER * 16)
        image_h = int(self.h / PIXEL_PER_METER * 16)
        self.image.clip_draw(96,128,image_w, image_h,x,y,self.w,self.h)
    def del_self(self):
        server.bg.remove(self)
        game_world.remove_object(self)

class tree(BGround):
    def __init__(self,x,y):
        super(tree, self).__init__(x,y)
        self.w = 1 * PIXEL_PER_METER
        self.h = 2 * PIXEL_PER_METER
        self.y += self.h/4
    def update(self):
        if self.x < main_state.camera_left - self.w/2:
            self.del_self()
    def draw(self):
        x = self.x - main_state.camera_left
        y = self.y- main_state.camera_bottom
        image_w = int(self.w / PIXEL_PER_METER * 16)
        image_h = int(self.h / PIXEL_PER_METER * 16)
        self.image.clip_draw(80,144,image_w, image_h,x,y,self.w,self.h)
    def del_self(self):
        server.bg.remove(self)
        game_world.remove_object(self)
class lava(BGround):
    def __init__(self,x,y):
        super(lava, self).__init__(x,y)
        self.w = 4 * PIXEL_PER_METER
        self.h = 2 * PIXEL_PER_METER
        self.y += self.h / 4
    def update(self):
        if self.x < main_state.camera_left - self.w/2:
            self.del_self()
    def draw(self):
        x = self.x - main_state.camera_left
        y = self.y- main_state.camera_bottom
        image_w = int(self.w / PIXEL_PER_METER * 16)
        image_h = int(self.h / PIXEL_PER_METER * 16)
        self.image.clip_draw(80,0,image_w, image_h,x,y,self.w,self.h)
    def del_self(self):
        server.bg.remove(self)
        game_world.remove_object(self)
class BG_pipe(BGround):
    def __init__(self,x,y):
        super(BG_pipe, self).__init__(x,y)
        self.w = 4 * PIXEL_PER_METER
        self.h = 4 * PIXEL_PER_METER
        self.y += self.h / 8
    def update(self):
        if self.x < main_state.camera_left - self.w/2:
            self.del_self()
    def draw(self):
        x = self.x - main_state.camera_left
        y = self.y- main_state.camera_bottom
        image_w = int(self.w / PIXEL_PER_METER * 16)
        image_h = int(self.h / PIXEL_PER_METER * 16)
        self.image.clip_draw(80,48,image_w, image_h,x,y,self.w,self.h)
    def del_self(self):
        server.bg.remove(self)
        game_world.remove_object(self)
class castle(BGround):
    def __init__(self,x,y):
        super(castle, self).__init__(x,y)
        self.w = 5 * PIXEL_PER_METER
        self.h = 5 * PIXEL_PER_METER
    def update(self):
        if self.x < main_state.camera_left - self.w/2:
            self.del_self()
    def draw(self):
        x = self.x - main_state.camera_left
        y = self.y- main_state.camera_bottom
        image_w = int(self.w / PIXEL_PER_METER * 16)
        image_h = int(self.h / PIXEL_PER_METER * 16)
        self.image.clip_draw(0,0,image_w, image_h,x,y,self.w,self.h)
    def del_self(self):
        server.bg.remove(self)
        game_world.remove_object(self)
class Big_castle(BGround):
    def __init__(self,x,y):
        super(Big_castle, self).__init__(x,y)
        self.w = 9 * PIXEL_PER_METER
        self.h = 11 * PIXEL_PER_METER
    def update(self):
        pass
    def draw(self):
        x = self.x - main_state.camera_left
        y = self.y- main_state.camera_bottom
        image_w = int(self.w / PIXEL_PER_METER * 16)
        image_h = int(self.h / PIXEL_PER_METER * 16)
        self.image.clip_draw(144,0,image_w, image_h,x,y,self.w,self.h)
    def del_self(self):
        server.bg.remove(self)
        game_world.remove_object(self)