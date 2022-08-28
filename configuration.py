# Kivy Configuration
# from kivy.metrics import dp

# [WINDOW SIZE]
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600

# [CALCULATE GRID SIZE]
WORLD_WIDTH = 800
WORLD_HEIGHT = 800
COLS = 50
ROWS = 50
X_MARGIN = WORLD_WIDTH / COLS
Y_MARGIN = WORLD_HEIGHT / ROWS
BLOCK_WIDTH = (WORLD_WIDTH/(WORLD_WIDTH/X_MARGIN))
BLOCK_HEIGHT = (WORLD_HEIGHT/(WORLD_HEIGHT/Y_MARGIN))

# [BOX SIZE]
BOX_SIZE = 75