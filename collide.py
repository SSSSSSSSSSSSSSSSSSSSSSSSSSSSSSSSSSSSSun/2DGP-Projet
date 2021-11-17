import main_state
import game_world

def collide(a, b):
    left_a, bottom_a, right_a, top_a = a.get_bb()
    left_b, bottom_b, right_b, top_b = b.get_bb()
    if left_a > right_b: return False
    if right_a < left_b: return False
    if top_a < bottom_b: return False
    if bottom_a > top_b: return False
    return True

def collide_block(a, block):
    left_a, bottom_a, right_a, top_a = a.get_bb()
    left_b, bottom_b, right_b, top_b = block.get_bb()

    if top_a > top_b:  # 윗 충돌로 간주
        a.lon_speed = 0
        a.lon_accel = 0
        a.y = top_b + a.h/2
        return
    elif bottom_a < bottom_b: # 아랫 충돌로 간주
        a.lon_speed = -0.1
        a.y = bottom_b - a.h/2
        block.do()
        return
    elif left_a < left_b: # 왼 충돌로 간주

        a.x = left_b - a.w/2

        return
    elif right_a > right_b: # 오른 충돌로 간주
        print(2)
        a.x = right_b + a.w/2
        return
    a.lon_speed = 0
    a.lon_accel = 0
    a.y = top_b + a.h/2

def collide_enemy(a, enemy):
    left_a, bottom_a, right_a, top_a = a.get_bb()
    left_b, bottom_b, right_b, top_b = enemy.get_bb()
    if top_a > top_b:  # 윗 충돌로 간주
        a.lon_speed = 10
        enemy.hp -=1
    else:
        #사망
        print("사망")

def collide_fire_block(fire, block):
    left_a, bottom_a, right_a, top_a = fire.get_bb()
    left_b, bottom_b, right_b, top_b = block.get_bb()
    if top_a > top_b:  # 윗 충돌로 간주
        fire.lon_speed = 7.375
        return
    if bottom_a < bottom_b: # 아랫 충돌로 간주
        fire.lon_speed = -7.375
        return
    else:
        main_state.char_fires.remove(fire)
        game_world.remove_object(fire)
        del fire


def collide_enemy_block(enemy, block):

    left_a, bottom_a, right_a, top_a = enemy.get_bb()
    left_b, bottom_b, right_b, top_b = block.get_bb()
    if top_a > top_b:  # 윗 충돌로 간주
        enemy.lon_speed = 0
        enemy.lon_accel = 0
        enemy.y = top_b + enemy.h/2
        return
    if bottom_a < bottom_b: # 아랫 충돌로 간주

        enemy.lon_speed = 0
        enemy.y = bottom_b - enemy.h/2
        return
    if left_a < left_b: # 왼 충돌로 간주

        enemy.x = left_b - enemy.w/2
        enemy.lat_speed = -enemy.lat_speed
        return
    if right_a > right_b: # 오른 충돌로 간주

        enemy.x = right_b + enemy.w/2
        enemy.lat_speed = -enemy.lat_speed
        return
    enemy.lon_speed = 0
    enemy.lon_accel = 0
    enemy.y = top_b + enemy.h/2

def collide_object_block(object, block):
    left_a, bottom_a, right_a, top_a = object.get_bb()
    left_b, bottom_b, right_b, top_b = block.get_bb()
    if top_a > top_b:  # 윗 충돌로 간주
        object.lon_speed = 0
        object.lon_accel = 0
        object.y = top_b + object.h/2
        return
    if bottom_a < bottom_b: # 아랫 충돌로 간주
        object.lon_speed = 0
        object.y = bottom_b - object.h/2
        return
    object.lat_speed = -object.lat_speed

