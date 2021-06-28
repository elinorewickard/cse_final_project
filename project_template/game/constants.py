import os
# Constants for window
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 650
SCREEN_TITLE = "Vengeance"

# player constants
GRAVITY = 1
PLAYER_MOVEMENT_SPEED = 500
PLAYER_JUMP_SPEED = 20
SCALING = 3.0

# margin minimum between character and screen edge
LEFT_VIEWPORT_MARGIN = 250
RIGHT_VIEWPORT_MARGIN = 250
BOTTOM_VIEWPORT_MARGIN = 50
TOP_VIEWPORT_MARGIN = 100

# character reference for file-finding
PATH = os.path.dirname(os.path.abspath(__file__))
CHAR_IMG = os.path.join(PATH, 'assets/boxman.png')
BACKGR_IMG = os.path.join(PATH, 'assets/background.png')
GRASS_IMG = os.path.join(PATH, 'assets/grass.png')