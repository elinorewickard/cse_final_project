import arcade
import constants as c
from layersprite import LayerSprite
from layerwork import LayerWork

class Startup(arcade.View):
   """Setting up game. """
   def __init__(self):
      """"class constructor. Sets up the window."""
      super().__init__()
      self.layers = LayerWork()

      #separate variable for player sprite
      self.player = arcade.Sprite()
      arcade.set_background_color(arcade.csscolor.BLACK)
      arcade.set_background_color((200,100,50,100))
      self.score = 0
      self.physics_engine = None
   def setup(self):
      """set up game here, if called it will restart the game."""
      
      self.collect_coin_sound = arcade.load_sound(":resources:sounds/coin1.wav") 
      self.jump_sound = arcade.load_sound(":resources:sounds/jump1.wav")

      self.player = LayerSprite(c.CHAR_IMG, self.layer_scale(0))
      self.player.center_y = c.SCREEN_HEIGHT/2
      self.player.center_x = c.SCREEN_WIDTH/2
      self.layers.add_player(self.player)

      '''self.background = LayerSprite(c.BACKGR_IMG,c.SCALING) #will always be printed first
      self.background.bottom = 0
      self.background.center_x = c.SCREEN_WIDTH/2'''

      for layer in range(0,6):
         for i in range(100):
            self.add_grass(i,layer)
            self.add_coin(i,layer)
         self.add_fire(layer)
      tree = LayerSprite(c.TREE_IMG, self.layer_scale(3))
      tree.bottom = (3) * c.LAYER_WIDTH * self.layer_scale(3) - 13
      tree.left = 500
      tree.layer = 3
      self.layers.add_mob(tree)
      
      self.view_bottom = 0
      self.view_left = 0

      block_list_on_layer = self.layers.get_list(self.player.layer, 'block')
      self.physics_engine = arcade.PhysicsEnginePlatformer(self.player, block_list_on_layer, c.GRAVITY)

   def layer_scale(self, layer: int): #increasingly small with higher layer number
      return float((-c.SCALING * layer)/(c.SCALING * c.SCALING) + c.SCALING)

   def add_fire(self,layer):
      self.fire = LayerSprite(c.FIRE_IMG, self.layer_scale(layer) * 4)
      self.fire.left = -500
      self.fire.bottom = (layer) * c.LAYER_WIDTH * self.layer_scale(layer)
      self.fire.velocity = (c.FIRE_MOVEMENT_SPEED,0)
      self.fire.layer = layer
      self.layers.add_mob(self.fire)
      

   def add_coin(self,i,layer):
      self.coin = LayerSprite(c.COIN_IMG, self.layer_scale(layer))
      self.coin.bottom = (layer) * c.LAYER_WIDTH * self.layer_scale(layer)+50
      self.coin.right = 256 * i * self.layer_scale(layer)
      self.coin.layer = layer
      self.layers.add_coin(self.coin)

   def add_grass(self,i,layer):
      """Adds blocks to screen, currently it is grass."""
      self.grass = LayerSprite(c.GRASS_IMG, self.layer_scale(layer))
      self.grass.set_hit_box(((-128,-32),(128,-32),(128,0),(128,0),(-128,0),(-128,0)))
      self.grass.center_x = 256 * i * self.layer_scale(layer)
      self.grass.bottom = (layer-1) * c.LAYER_WIDTH * self.layer_scale(layer)
      self.grass.layer = layer
      self.layers.add_block(self.grass)

   def on_draw(self):
      """Render SCREEN."""
      arcade.start_render()
      master_list = self.layers.get_all_in_range(self.player.center_x)
      master_list.draw()

      score = (f'Score: {self.score}')
      arcade.draw_text((score), 10 + self.view_left, 10 + self.view_bottom,
                         arcade.csscolor.WHITE, 18)


   def on_key_press(self, key, modifiers):
      """Called whenever a key is pressed."""
      if key == arcade.key.UP or key == arcade.key.W:
         if self.player.layer < 5:
            self.player.push_layer() #move the sprite up one layer
            self.layers.push_player(self.player.layer)
            if self.player.bottom < c.LAYER_WIDTH * self.player.layer:
               self.player.bottom = c.LAYER_WIDTH * self.player.layer #set the y of the player to the proper layer's minimum height
            self.player._set_scale(self.layer_scale(self.player.layer)) #change the player's scale to seem farther away
            block_list_on_layer = self.layers.get_list(self.player.layer, 'block')
               #get the list of blocks on the layer of the player, and prepare them for collision \/
            self.physics_engine = arcade.PhysicsEnginePlatformer(self.player, block_list_on_layer, c.GRAVITY)

      elif key == arcade.key.DOWN or key == arcade.key.S:
         if self.player.layer > 0:
            self.player.pull_layer()
            self.layers.pull_player(self.player.layer)
            self.player._set_scale(self.layer_scale(self.player.layer))
            block_list_on_layer = self.layers.get_list(self.player.layer, 'block')
            self.physics_engine = arcade.PhysicsEnginePlatformer(self.player, block_list_on_layer, c.GRAVITY)

      elif key == arcade.key.LEFT or key == arcade.key.A:
         self.player.change_x = -c.PLAYER_MOVEMENT_SPEED

      elif key == arcade.key.RIGHT or key == arcade.key.D:
         self.player.change_x = c.PLAYER_MOVEMENT_SPEED

      elif arcade.key.SPACE:
         if self.player.bottom < c.LAYER_WIDTH * self.player.layer + 100:
            self.player.change_y = c.PLAYER_MOVEMENT_SPEED

   def on_key_release(self, key, modifiers):
      """Called when the user releases a key."""
      if key == arcade.key.UP or key == arcade.key.W or key == arcade.key.DOWN or key == arcade.key.S:
         self.player.change_y = 0
      if key == arcade.key.LEFT or key == arcade.key.A or key == arcade.key.RIGHT or key == arcade.key.D:
         self.player.change_x = 0

   def on_update(self, delta_time: float):

      current_coin_layer = self.layers.get_list(self.player.layer,'coin') #gets SpriteLIST
      for coin in current_coin_layer:
         if self.player.collides_with_sprite(coin):
            current_coin_layer.remove(coin)
            self.layers.set_list(self.player.layer,current_coin_layer, 'coinlist')
            self.score += 1
            arcade.play_sound(self.collect_coin_sound)

      for i in range(0,6):
         mob_list = self.layers.get_list(i,'mob')
         for sprite in mob_list:
            sprite.center_x = int(sprite.center_x + sprite.change_x)

      self.current_enemy_layer = self.layers.get_list(self.player.layer,'mob')
      if self.player.collides_with_list(self.current_enemy_layer):
         #self.__init__()
         print('end game')

      if self.player.bottom < self.player.layer * c.LAYER_WIDTH * self.layer_scale(self.player.layer):
         self.player.bottom = self.player.layer * c.LAYER_WIDTH * self.layer_scale(self.player.layer)
      if self.player.top > self.window.height:
         self.player.top = self.window.height
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

