import arcade, os

# Constants for window
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 650
SCREEN_TITLE = "Vengeance"

# player constants
GRAVITY = 1
PLAYER_MOVEMENT_SPEED = 5
PLAYER_JUMP_SPEED = 20
SCALING = 2.0

# margin minimum between character and screen edge
LEFT_VIEWPORT_MARGIN = 250
RIGHT_VIEWPORT_MARGIN = 250
BOTTOM_VIEWPORT_MARGIN = 50
TOP_VIEWPORT_MARGIN = 100

# character reference for file-finding
PATH = os.path.dirname(os.path.abspath(__file__))
CHAR_IMG = os.path.join(PATH, 'assets/boxman.png')
#PADDLE_IMAGE = os.path.join(PATH, '..', 'images', 'paddle-0.png')
#BRICK_IMAGE = os.path.join(PATH, '..', 'images', 'brick-0.png')

# program entry point
class Setup(arcade.Window):
   """setting up game """
   def __init__(self):
      """"class constructor. Sets up the window."""
      super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
      
      self.player_list = arcade.SpriteList()
      self.block_list = arcade.SpriteList(use_spatial_hash=True)
      self.layer_list = arcade.SpriteList()

      #separate variable for player sprite
      self.player_sprite = arcade.Sprite()

      arcade.set_background_color(arcade.csscolor.GREEN)

   def startup(self):
      """set up game here, if called it will restart the game"""
      
      self.player_sprite = arcade.Sprite(CHAR_IMG, SCALING)
      self.player_sprite.center_y = SCREEN_HEIGHT/2
      self.player_sprite.center_x = SCREEN_WIDTH/2
      self.player_list.append(self.player_sprite)

   def on_draw(self):
      """Render the screen."""
      arcade.start_render()
      self.player_list.draw()


def main():
   """ Main method, runs the game when called. """
   window = Setup()
   window.startup()
   arcade.run()

if __name__ == "__main__":
   main()
