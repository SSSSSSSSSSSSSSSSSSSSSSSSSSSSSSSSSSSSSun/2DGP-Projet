import game_framework
import pico2d

import load_state
import main_state

pico2d.open_canvas(main_state.window_width, main_state.window_height) # 800, 600
game_framework.run(load_state)
pico2d.close_canvas()