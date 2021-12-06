character = None
bg = []
bg_image = None
enemys = []
char_fires = []
objects = []
blocks = dict()

max_width = None
max_height = None

stage = 1
level = 1
life = None
font = None
small_font = None
def clear():
    global character, enemys, char_fires, objects, blocks
    character = None
    bg.clear()
    enemys.clear()
    char_fires.clear()
    objects.clear()
    blocks.clear()