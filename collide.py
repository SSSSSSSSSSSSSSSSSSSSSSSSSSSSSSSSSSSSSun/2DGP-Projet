import main_state
import game_world
import server

PIXEL_PER_METER = (50.0 / 1.0)
UP, DOWN, LEFT, RIGHT = 1,2,3,4
def collide(a, b):
    left_a, bottom_a, right_a, top_a = a.get_bb()
    left_b, bottom_b, right_b, top_b = b.get_bb()

    if left_a > right_b: return False
    if right_a < left_b: return False
    if top_a < bottom_b: return False
    if bottom_a >= top_b: return False
    return True

def drop_a_collide(a, b):
    left_a, bottom_a, right_a, top_a = a.get_bb()
    left_b, bottom_b, right_b, top_b = b.get_bb()
    bottom_a -= 1
    if left_a > right_b: return False
    if right_a < left_b: return False
    if top_a < bottom_b: return False
    if bottom_a >= top_b: return False
    return True

def upper_than_ld_to_ru(a,b):
    if a.y >= a.x - b.x + b.y:
        return True
    else:
        return False

def upper_than_lu_to_rd(a,b):
    if a.y >= - a.x + b.x + b.y:
        return True
    else:
        return False

def a_position_than_b(a,b):
    left_a, bottom_a, right_a, top_a = a.get_bb()
    left_b, bottom_b, right_b, top_b = b.get_bb()
    if upper_than_ld_to_ru(a,b):
        if upper_than_lu_to_rd(a,b):
            return UP
        else:
            return LEFT
    else:
        if upper_than_lu_to_rd(a,b):
            return RIGHT
        else:
            return DOWN


def tall_a_position_than_b(a,b):
    left_a, bottom_a, right_a, top_a = a.get_bb()
    left_b, bottom_b, right_b, top_b = b.get_bb()
    a.y -=a.h/4
    if upper_than_ld_to_ru(a,b) and upper_than_lu_to_rd(a,b):
        return UP
    a.y +=a.h/2
    if not upper_than_ld_to_ru(a,b) and not upper_than_lu_to_rd(a,b):
        return DOWN
    a.y -=a.h/4
    if a.x < b.x:
        return LEFT
    else:
        return DOWN

def tall_b_position_than_b(a,b):
    left_a, bottom_a, right_a, top_a = a.get_bb()
    left_b, bottom_b, right_b, top_b = b.get_bb()
    b.y +=b.h/4
    if upper_than_ld_to_ru(a,b) and upper_than_lu_to_rd(a,b):
        return UP
    b.y -=b.h/2
    if not upper_than_ld_to_ru(a,b) and not upper_than_lu_to_rd(a,b):
        return DOWN
    b.y +=b.h/4
    if a.x < b.x:
        return LEFT
    else:
        return DOWN

def tall_a_b_position_than_b(a,b):
    left_a, bottom_a, right_a, top_a = a.get_bb()
    left_b, bottom_b, right_b, top_b = b.get_bb()
    a.y -=a.h/4
    b.y +=b.h/4
    if upper_than_ld_to_ru(a,b) and upper_than_lu_to_rd(a,b):
        return UP
    a.y +=a.h/2
    b.y -=b.h/2
    if not upper_than_ld_to_ru(a,b) and not upper_than_lu_to_rd(a,b):
        return DOWN
    a.y -=a.h/4
    b.y +=b.h/4
    if a.x < b.x:
        return LEFT
    else:
        return DOWN

def collide_block(a, block):
    left_a, bottom_a, right_a, top_a = a.get_bb()
    left_b, bottom_b, right_b, top_b = block.get_bb()
    if a.h >= a.w*2:
        pos = tall_a_position_than_b(a,block)
    else:
        pos = a_position_than_b(a,block)
    if pos == UP:  # 윗 충돌로 간주

        a.lon_speed = 0
        a.lon_accel = 0

        a.y = top_b + a.h/2
        a.jump = False
        return
    elif pos == DOWN: # 아랫 충돌로 간주

        a.lon_speed = 0
        a.lon_accel = 9.8+4.95
        a.y = bottom_b - a.h/2
        block.do()
        return
    elif pos == LEFT: # 왼 충돌로 간주

        a.x = left_b - a.w/2 + a.w / 10 -1

        return
    elif pos == RIGHT: # 오른 충돌로 간주

        a.x = right_b + a.w/2 - a.w / 10 +1
        return
    a.lon_speed = 0
    a.lon_accel = 0
    a.y = top_b + a.h/2

def collide_enemy(a, enemy):
    left_a, bottom_a, right_a, top_a = a.get_bb()
    left_b, bottom_b, right_b, top_b = enemy.get_bb()
    if a.h >= a.w*2:
        if enemy.h >= enemy.w*2:
            pos = tall_a_b_position_than_b(a,enemy)
        else:
            pos = tall_a_position_than_b(a,enemy)
    else:
        if enemy.h >= enemy.w*2:
            pos = tall_b_position_than_b(a,enemy)
        else:
            pos = a_position_than_b(a,enemy)
    if pos == UP:  # 윗 충돌로 간주
        a.lon_speed = 10
        enemy.hp -=1
    else:
        if a.no_damege_timer==0:
            if a.power_up>0:
                a.no_damege_timer = 1000
                a.power_up -= 1
                if not a.power_up:
                    a.h /= 2
            else:
                pass #사망


def collide_fire_block(fire, block):
    left_a, bottom_a, right_a, top_a = fire.get_bb()
    left_b, bottom_b, right_b, top_b = block.get_bb()
    pos = a_position_than_b(fire, block)
    if pos == UP:  # 윗 충돌로 간주
        fire.lon_speed = 7.375
        return
    if pos == DOWN: # 아랫 충돌로 간주
        fire.lon_speed = -7.375
        return
    else:
        fire.del_self()


def collide_enemy_block(enemy, block):
    left_a, bottom_a, right_a, top_a = enemy.get_bb()
    left_b, bottom_b, right_b, top_b = block.get_bb()
    if enemy.h >= enemy.w*2 and top_a == enemy.h/2 + enemy.y:
        pos = tall_a_position_than_b(enemy,block)
    else:
        pos = a_position_than_b(enemy,block)

    if pos == UP:  # 윗 충돌로 간주
        enemy.lon_speed = 0
        enemy.lon_accel = 0
        enemy.y = top_b + enemy.h/2
        return
    if pos == DOWN: # 아랫 충돌로 간주
        enemy.lon_speed = 0
        enemy.y = bottom_b - enemy.h/2
        return
    if pos == LEFT: # 왼 충돌로 간주
        enemy.right = False
        enemy.x = left_b - enemy.w/2 - 1
        enemy.lat_speed = -enemy.lat_speed
        return
    if pos == RIGHT: # 오른 충돌로 간주
        enemy.right = True
        enemy.x = right_b + enemy.w/2 + 1
        enemy.lat_speed = -enemy.lat_speed
        return
    enemy.lon_speed = 0
    enemy.lon_accel = 0
    enemy.y = top_b + enemy.h/2

def collide_object_block(object, block):
    left_a, bottom_a, right_a, top_a = object.get_bb()
    left_b, bottom_b, right_b, top_b = block.get_bb()
    pos = a_position_than_b(object,block)
    if pos == UP:  # 윗 충돌로 간주
        object.lon_speed = 0
        object.lon_accel = 0
        object.y = top_b + object.h/2
        return
    if pos == DOWN: # 아랫 충돌로 간주
        object.lon_speed = 0
        object.y = bottom_b - object.h/2
        return
    object.lat_speed = -object.lat_speed

