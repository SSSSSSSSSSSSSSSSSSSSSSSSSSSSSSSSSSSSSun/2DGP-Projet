import game_framework
from pico2d import *
import main_state
import game_world

PIXEL_PER_METER = (50.0 / 1.0)  # 50 pixel 1meter


# Action Speed
TIME_PER_ACTION = 0.3
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
    def __init__(self,x,y):
        super(Platform, self).__init__(x, y)
        self.w = 1 * PIXEL_PER_METER
        self.h = 1 * PIXEL_PER_METER

    def get_bb(self):
        return self.x-self.w/2, self.y-self.h/2, self.x+self.w/2, self.y+self.h/2

    def update(self):
        pass

    def draw(self):
        self.image.clip_draw(0,128-main_state.stage*16,16,16,self.x,self.y,self.w,self.h)