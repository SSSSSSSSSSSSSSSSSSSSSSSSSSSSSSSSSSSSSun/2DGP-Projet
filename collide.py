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
    if bottom_a < bottom_b: # 아랫 충돌로 간주
        a.lon_speed = 0
        a.y = bottom_b - a.h/2
        return
    if left_a < left_b: # 왼 충돌로 간주
        a.x = left_b - a.w/2
        return
    if right_a > right_b: # 오른 충돌로 간주
        a.x = left_b + a.w/2
        return
    a.lon_speed = 0
    a.lon_accel = 0
    a.y = top_b + a.h/2