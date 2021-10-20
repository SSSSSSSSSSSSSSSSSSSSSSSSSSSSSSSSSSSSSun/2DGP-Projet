class Object():
    def __init__(self, x,y):
        self.x=x; self.y=y
        self.w = 16; self.h = 16
        self.frame = 0
        self.frame_wait = 0

class CharFire(Object):
    def __init__(self,x,y,dir):
        super(CharFire,self).__init__(x,y)
        self.dir = dir

    def move(self):
        self.x = self.x + self.dir*2.5
        if 0: # 바닥에 닿을 시
            pass
        if 0: # 벽에 닿을 시
            del(self)
    def sprite(self):
        self.frame_wait = (self.frame_wait+1)%25
        if(self.frame_wait == 0):
            self.frame = (self.frame+1)%4


objects = []