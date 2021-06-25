import arcade, os

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

# program entry point
class Setup(arcade.Window):
   """setting up game """
   def __init__(self):
      """"class constructor. Sets up the window."""
      super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
      
      self.player_list = arcade.SpriteList()
      self.block_list = arcade.SpriteList()#use_spatial_hash=True)
      self.layer_list = arcade.SpriteList()

      #separate variable for player sprite
      self.player = arcade.Sprite()

      arcade.set_background_color(arcade.csscolor.GREEN)

   def startup(self):
      """set up game here, if called it will restart the game"""
      
      self.player = arcade.Sprite(CHAR_IMG, SCALING)
      self.player.center_y = SCREEN_HEIGHT/2
      self.player.center_x = SCREEN_WIDTH/2
      self.player_list.append(self.player)

      self.background = arcade.Sprite(BACKGR_IMG)
      self.background.center_y = SCREEN_HEIGHT/2
      self.background.center_x = SCREEN_WIDTH/2
      self.layer_list.append(self.background)

      for i in range(int(SCREEN_WIDTH/(32*SCALING) + 1)):
         self.add_block(i)

   def add_block(self,i):
      self.grass = arcade.Sprite(GRASS_IMG, SCALING)
      self.grass.left = 32 * i * SCALING
      self.grass.bottom = 0
      self.block_list.append(self.grass)

   def on_draw(self):
      """Render the screen."""
      arcade.start_render()
      self.layer_list.draw()
      self.block_list.draw()
      self.player_list.draw()

   def on_key_press(self, key, modifiers):
      """Called whenever a key is pressed. """

      if key == arcade.key.UP or key == arcade.key.W or key == arcade.key.SPACE:
         self.player.change_y = PLAYER_MOVEMENT_SPEED
      if key == arcade.key.DOWN or key == arcade.key.S:
         self.player.change_y = -PLAYER_MOVEMENT_SPEED
      if key == arcade.key.LEFT or key == arcade.key.A:
         self.player.change_x = -PLAYER_MOVEMENT_SPEED
      if key == arcade.key.RIGHT or key == arcade.key.D:
         self.player.change_x = PLAYER_MOVEMENT_SPEED

   def on_key_release(self, key, modifiers):
      """Called when the user releases a key. """

      if key == arcade.key.UP or key == arcade.key.W or key == arcade.key.DOWN or key == arcade.key.S:
         self.player.change_y = 0
      if key == arcade.key.LEFT or key == arcade.key.A or key == arcade.key.RIGHT or key == arcade.key.D:
         self.player.change_x = 0

   def on_update(self, delta_time: float):

      for sprite in self.player_list:
         if not sprite.collides_with_list(self.block_list):
            sprite.center_x = float(sprite.center_x + sprite.change_x * delta_time)
            sprite.center_y = float(sprite.center_y + sprite.change_y * delta_time)
         else:
            for block in self.block_list:
               if sprite.bottom < block.top and sprite.bottom >= block.bottom:
                  sprite.bottom = block.top + 1

      if self.player.top > self.height:
         self.player.top = self.height
      if self.player.right > self.width:
         self.player.right = self.width
      if self.player.bottom < 0:
         self.player.bottom = 0
      if self.player.left < 0:
         self.player.left = 0

def main():
   """ Main method, runs the game when called. """
   window = Setup()
   window.startup()
   arcade.run()

if __name__ == "__main__":
   main()
