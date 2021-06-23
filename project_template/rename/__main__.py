import arcade

# Constants for window
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 650
SCREEN_TITLE = "Vengeance"

# player constants
GRAVITY = 1
PLAYER_MOVEMENT_SPEED = 5
PLAYER_JUMP_SPEED = 20

# margin minimum between character and screen edge
LEFT_VIEWPORT_MARGIN = 250
RIGHT_VIEWPORT_MARGIN = 250
BOTTOM_VIEWPORT_MARGIN = 50
TOP_VIEWPORT_MARGIN = 100

# program entry point

def main():
   """ Main method """
   window = MyGame()
   window.setup()
   arcade.run()

if __name__ == "__main__":
   main()
