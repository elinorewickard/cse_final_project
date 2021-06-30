import arcade
import constants as c

class Startup(arcade.View):
   """Setting up game. """
   def __init__(self):
      """"class constructor. Sets up the window."""
      super().__init__()
      
      self.player_list = arcade.SpriteList()
      self.block_list = arcade.SpriteList()#use_spatial_hash=True)
      self.layer_list = arcade.SpriteList()

      #separate variable for player sprite
      self.player = arcade.Sprite()

      arcade.set_background_color(arcade.csscolor.GREEN)

   def setup(self):
      """set up game here, if called it will restart the game."""
      
      self.player = arcade.Sprite(c.CHAR_IMG, c.SCALING)
      self.player.center_y = c.SCREEN_HEIGHT/2
      self.player.center_x = c.SCREEN_WIDTH/2
      self.player_list.append(self.player)

      self.background = arcade.Sprite(c.BACKGR_IMG)
      self.background.center_y = c.SCREEN_HEIGHT/2
      self.background.center_x = c.SCREEN_WIDTH/2
      self.layer_list.append(self.background)

      for i in range(int(c.SCREEN_WIDTH/(32*c.SCALING) + 1)):
         self.add_block(i)

   def add_block(self,i):
      """Adds blocks to screen, currently it is grass."""
      self.grass = arcade.Sprite(c.GRASS_IMG, c.SCALING)
      self.grass.left = 32 * i * c.SCALING
      self.grass.bottom = 0
      self.block_list.append(self.grass)

   def on_draw(self):
      """Render the c.SCREEN."""
      arcade.start_render()
      self.layer_list.draw()
      self.block_list.draw()
      self.player_list.draw()

   def on_key_press(self, key, modifiers):
      """Called whenever a key is pressed."""
      if key == arcade.key.UP or key == arcade.key.W or key == arcade.key.SPACE:
         self.player.change_y = c.PLAYER_MOVEMENT_SPEED
      if key == arcade.key.DOWN or key == arcade.key.S:
         self.player.change_y = -c.PLAYER_MOVEMENT_SPEED
      if key == arcade.key.LEFT or key == arcade.key.A:
         self.player.change_x = -c.PLAYER_MOVEMENT_SPEED
      if key == arcade.key.RIGHT or key == arcade.key.D:
         self.player.change_x = c.PLAYER_MOVEMENT_SPEED

   def on_key_release(self, key, modifiers):
      """Called when the user releases a key."""
      if key == arcade.key.UP or key == arcade.key.W or key == arcade.key.DOWN or key == arcade.key.S:
         self.player.change_y = 0
      if key == arcade.key.LEFT or key == arcade.key.A or key == arcade.key.RIGHT or key == arcade.key.D:
         self.player.change_x = 0

   def on_update(self, delta_time: float):
      """updates where player is and tracks collisons."""
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