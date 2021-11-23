character = None
enemys = []
char_fires = []
objects = []
blocks = dict()

max_width = None
max_height = None

def clear():
    global character, enemys, char_fires, objects, blocks
    character = None
    enemys.clear()
    char_fires.clear()
    objects.clear()
    blocks.clear()