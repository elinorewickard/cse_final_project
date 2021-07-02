import arcade
import constants as c

class Startup(arcade.View):
   """Setting up game. """
   def __init__(self):
      """"class constructor. Sets up the window."""
      super().__init__()

      self.player_list = arcade.SpriteList()
      self.block_list = arcade.SpriteList()#use_spatial_hash=True)
      self.hitbox_list = arcade.SpriteList()
      self.layer_list = arcade.SpriteList()

      #separate variable for player sprite
      self.player = arcade.Sprite()

      arcade.set_background_color(arcade.csscolor.GREEN)
      arcade.set_background_color((100,100,100,50))

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
      
      self.view_bottom = 0
      self.view_left = 0

   def add_block(self,i):
      """Adds blocks to screen, currently it is grass."""
      self.grass = arcade.Sprite(c.GRASS_IMG, c.SCALING)
      self.grass.left = 32 * i * c.SCALING
      self.grass.bottom = 0
      self.block_list.append(self.grass)

      for i in range(0,2):   
         self.add_block(i,c.GRASS_IMG,self.block_list)
         self.add_block(i,c.GRASS_HB_IMG,self.hitbox_list)

   def add_block(self,i,IMG,typelist):
      
      self.block = arcade.Sprite(IMG, c.SCALING)
      self.block.left = 256 * i * c.SCALING
      self.block.bottom = 0
      typelist.append(self.block)


   def on_draw(self):
      """Render the c.SCREEN."""
      arcade.start_render()
      self.layer_list.draw()
      #hitbox_list does not get printed
      self.player_list.draw()
      self.block_list.draw()

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
         if not sprite.collides_with_list(self.hitbox_list):
            sprite.center_x = float(sprite.center_x + sprite.change_x * delta_time)
            sprite.center_y = float(sprite.center_y + sprite.change_y * delta_time)
         else:
            for block in self.hitbox_list:
               if sprite.bottom < block.top and sprite.bottom >= block.bottom:
                  sprite.bottom = block.top + 1

      if self.player.top > self.window.height:
         self.player.top = self.window.height
      if self.player.right > self.window.width:
         self.player.right = self.window.width
      if self.player.bottom < 0:
         self.player.bottom = 0
      if self.player.left < 0:
         self.player.left = 0

      changed = False


      left_boundary = self.view_left + c.LEFT_VIEWPORT_MARGIN
      if self.player.left < left_boundary:
         self.view_left -= left_boundary - self.player.left
         changed = True


        # Scroll right
      right_boundary = self.view_left + c.SCREEN_WIDTH - c.RIGHT_VIEWPORT_MARGIN
      if self.player.right > right_boundary:
         self.view_left += self.player.right - right_boundary
         changed = True

        # Scroll up
      top_boundary = self.view_bottom + c.SCREEN_HEIGHT - c.TOP_VIEWPORT_MARGIN
      if self.player.top > top_boundary:
         self.view_bottom += self.player.top - top_boundary
         changed = True

        # Scroll down
      bottom_boundary = self.view_bottom + c.BOTTOM_VIEWPORT_MARGIN
      if self.player.bottom < bottom_boundary:
         self.view_bottom -= bottom_boundary - self.player.bottom
         changed = True

      if changed:
            # Only scroll to integers. Otherwise we end up with pixels that
            # don't line up on the screen
         self.view_bottom = int(self.view_bottom)
         self.view_left = int(self.view_left)

            # Do the scrolling
         arcade.set_viewport(self.view_left,
                              c.SCREEN_WIDTH + self.view_left,
                              self.view_bottom,
                              c.SCREEN_HEIGHT + self.view_bottom)
