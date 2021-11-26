character = None
bg = []
enemys = []
char_fires = []
objects = []
blocks = dict()

max_width = None
max_height = None

stage = 1
level = 1

def clear():
    global character, enemys, char_fires, objects, blocks
    character = None
    bg.clear()
    enemys.clear()
    char_fires.clear()
    objects.clear()
    blocks.clear()