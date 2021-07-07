import arcade
import constants as c
from layersprite import LayerSprite
from layerwork import LayerWork

class Startup(arcade.View):
   """Setting up game. """
   def __init__(self):
      """"class constructor. Sets up the window."""
      super().__init__()

      self.mob_list = arcade.SpriteList()
      self.block_list = arcade.SpriteList()
      self.layers = LayerWork()

      #separate variable for player sprite
      self.player = arcade.Sprite()
      arcade.set_background_color(arcade.csscolor.GREEN)
      arcade.set_background_color((100,100,100,50))

      self.physics_engine = None

   def setup(self):
      """set up game here, if called it will restart the game."""
      
      self.player = LayerSprite(c.CHAR_IMG, c.SCALING)
      self.player.center_y = c.SCREEN_HEIGHT/2
      self.player.center_x = c.SCREEN_WIDTH/2
      self.mob_list.append(self.player)
      self.layers.add_sprite(self.player, "player")

      self.background = LayerSprite(c.BACKGR_IMG) #will always be printed first
      self.background.center_y = c.SCREEN_HEIGHT/2
      self.background.center_x = c.SCREEN_WIDTH/2

      for layer in range(0,6):
         for i in range(int(c.SCREEN_WIDTH/(256*c.SCALING) + 10)):
            self.add_block(i,layer)
      
      self.view_bottom = 0
      self.view_left = 0

      block_list_on_layer = self.layers.get_block_list(self.player.layer)
      self.physics_engine = arcade.PhysicsEnginePlatformer(self.player, block_list_on_layer, c.GRAVITY)

   def add_block(self,i,layer):blocks to screen, currently it is grass."""
      LAYER_SCALING = c.SCALING/((layer+1)/3 + 2/3)
      self.grass = LayerSprite(c.GRASS_IMG, LAYER_SCALING)
      self.grass.set_hit_box(((-128,-16),(128,-16),(128,-4),(-128,-4)))
      self.grass.left = 256 * i * LAYER_SCALING
      self.grass.bottom = layer * c.LAYER_WIDTH
      self.grass.layer = layer
      self.block_list.append(self.grass)
      self.layers.add_block(self.grass)
   def on_draw(self):
      """Render c.SCREEN."""
      arcade.start_render()
      self.background.draw()
      for layer in range(self.layers.length()):
         self.layers.get_block_list(layer).draw()
         self.layers.get_mob_list(layer).draw()

   def on_key_press(self, key, modifiers):
      """Called whenever a key is pressed."""
      if key == arcade.key.UP or key == arcade.key.W:
         self.player.push_layer()
         self.player.bottom = c.LAYER_WIDTH * self.player.layer
         self.player._set_scale(c.SCALING/((self.player.layer+1)/3 + 2/3))
         block_list_on_layer = self.layers.get_block_list(self.player.layer)
         self.physics_engine = arcade.PhysicsEnginePlatformer(self.player, block_list_on_layer, c.GRAVITY)
      elif key == arcade.key.DOWN or key == arcade.key.S:
         if self.player.layer > 0:
            self.player.pull_layer()
            self.player._set_scale(c.SCALING/((self.player.layer+1)/3 + 2/3))
            self.player.bottom = -c.LAYER_WIDTH * self.player.layer
            block_list_on_layer = self.layers.get_block_list(self.player.layer)
            self.physics_engine = arcade.PhysicsEnginePlatformer(self.player, block_list_on_layer, c.GRAVITY)
      if key == arcade.key.LEFT or key == arcade.key.A:
         self.player.change_x = -c.PLAYER_MOVEMENT_SPEED
      elif key == arcade.key.RIGHT or key == arcade.key.D:
         self.player.change_x = c.PLAYER_MOVEMENT_SPEED
      '''if arcade.key.SPACE:
         if self.physics_engine.can_jump():
                self.player.change_y = c.PLAYER_JUMP_SPEED'''

   def on_key_release(self, key, modifiers):
      """Called when the user releases a key."""
      if key == arcade.key.UP or key == arcade.key.W or key == arcade.key.DOWN or key == arcade.key.S:
         self.player.change_y = 0
      if key == arcade.key.LEFT or key == arcade.key.A or key == arcade.key.RIGHT or key == arcade.key.D:
         self.player.change_x = 0

   def on_update(self, delta_time: float):
      if self.player.bottom < self.player.layer * c.LAYER_WIDTH:
         self.player.bottom = self.player.layer * c.LAYER_WIDTH
      self.physics_engine.update()
      if self.player.top > self.window.height:
         self.player.top = self.window.height
      if self.player.right > 2000:
         self.player.right = 2000
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
      
      
      self.physics_engine.update()

