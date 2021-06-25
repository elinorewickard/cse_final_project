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
class Setup(arcade.Window):
   """setting up game """
   def __init__(self):
      """"class constructor. Sets up the window."""
      super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
      
      self.block_list = None
      self.layer_list = None
      self.player_list = None

      #separate variable for player sprite
      self.player_sprite = None

      arcade.set_background_color(arcade.csscolor.GREEN)

   def startup(self):
      """set up game here, if called it will restart the game"""
      self.player_list = arcade.SpriteList()
      self.block_list = arcade.SpriteList(use_spatial_hash=True)
      self.layer_list = arcade.SpriteList()
      self.player_list = arcade.SpriteList()
   
   def on_draw(self):
      """Render the screen."""

      arcade.start_render()


def main():
   """ Main method, runs the game when called. """
   window = Setup()
   window.startup()
   arcade.run()

if __name__ == "__main__":
   main()
