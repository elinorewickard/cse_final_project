import arcade
import constants as c
from layersprite import LayerSprite
from layerwork import LayerWork
from endScreen import EndScreen
from winScreen import WinScreen

class Startup(arcade.View):
   """Setting up game. """

   def __init__(self):
      """"class constructor. Sets up the window."""
      super().__init__()
      self.layers = LayerWork()

      #separate variable for player sprite
      self.player = arcade.Sprite()

      #arcade window setup
      arcade.set_background_color(arcade.csscolor.BLACK)
      arcade.set_background_color((200,100,50,100))

      
      self.score = 0
      self.physics_engine = None


   def setup(self):
      """set up game here, if called it will restart the game."""
      #important for scrolling viewpoint 
      self.view_bottom = 0
      self.view_left = 0

      #sound paths for objects collected and jumps
      self.collect_coin_sound = arcade.load_sound(c.CRUNCH) 
      self.jump_sound = arcade.load_sound(c.JUMP)
      self.fire_sound = arcade.load_sound(c.FIRE)

      #centering the player on the screen
      self.player = LayerSprite(c.CHAR_IMG, self.layer_scale(0))
      self.player.center_y = c.SCREEN_HEIGHT/2
      self.player.center_x = c.SCREEN_WIDTH/2
      self.layers.add_player(self.player)

      #setting up the different layers and adding the sprites to each
      for layer in range(0,6):
         for i in range(100):
            self.add_grass(i,layer)
            self.add_coin(i,layer)
            self.add_tree(i, layer)
         self.add_fire(layer)

      block_list_on_layer = self.layers.get_list(self.player.layer, 'block')
      self.physics_engine = arcade.PhysicsEnginePlatformer(self.player, block_list_on_layer, c.GRAVITY)

   def layer_scale(self, layer: int): #increasingly small with higher layer number
      """Returns a layer sprite"""
      return float((-c.SCALING * layer)/(c.SCALING * c.SCALING) + c.SCALING)
      

   def add_fire(self,layer):
      """Adds fire sprite off of the screen with a rightward velocity."""
      self.fire = LayerSprite(c.FIRE_IMG, self.layer_scale(layer) * 4)
      self.fire.left = -500
      self.fire.bottom = (layer) * c.LAYER_WIDTH * self.layer_scale(layer)
      self.fire.velocity = (c.FIRE_MOVEMENT_SPEED,0)
      self.fire.layer = layer
      self.layers.add_mob(self.fire)
      
      
   def add_tree(self, i, layer):
      """Adds tree sprite to the screen as blocks"""
      self.tree = LayerSprite(c.TREE_IMG, self.layer_scale(3))
      self.tree.bottom = (layer) * c.LAYER_WIDTH * self.layer_scale(layer) + 10
      self.tree.left = 350 * i * self.layer_scale(layer)
      self.tree.layer = layer
      self.layers.add_block(self.tree)


   def add_coin(self,i,layer):
      """Adding coin sprites to the window"""
      self.coin = LayerSprite(c.COIN_IMG, self.layer_scale(layer)*.15)
      self.coin.bottom = (layer) * c.LAYER_WIDTH * self.layer_scale(layer) + 50
      self.coin.right = 400 * i * self.layer_scale(layer)
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

      #tracks score for items collected
      score = (f'Score: {self.score}')
      arcade.draw_text((score), 10 + self.view_left, 10 + self.view_bottom,
                         arcade.csscolor.WHITE, 18)


   def on_key_press(self, key, modifiers):
      """Called whenever a key is pressed. This is how movement is tracked"""
      if key == arcade.key.UP or key == arcade.key.W:
         if self.player.layer < 5:
            self.player.push_layer() #move the sprite up one layer
            if self.player.bottom < c.LAYER_WIDTH * self.player.layer:
               self.player.bottom = c.LAYER_WIDTH * self.player.layer #set the y of the player to the proper layer's minimum height
            self.player._set_scale(self.layer_scale(self.player.layer)) #change the player's scale to seem farther away
            block_list_on_layer = self.layers.get_list(self.player.layer, 'block')
               #get the list of blocks on the layer of the player, and prepare them for collision \/
            self.physics_engine = arcade.PhysicsEnginePlatformer(self.player, block_list_on_layer, c.GRAVITY)

      elif key == arcade.key.DOWN or key == arcade.key.S:
         if self.player.layer > 0:
            self.player.pull_layer()
            self.player._set_scale(self.layer_scale(self.player.layer))
            block_list_on_layer = self.layers.get_list(self.player.layer, 'block')
            self.physics_engine = arcade.PhysicsEnginePlatformer(self.player, block_list_on_layer, c.GRAVITY)

      elif key == arcade.key.LEFT or key == arcade.key.A:
         self.player.change_x = -(c.PLAYER_MOVEMENT_SPEED-((self.player.center_x-200)/50)+(self.score*7))

      elif key == arcade.key.RIGHT or key == arcade.key.D:
         self.player.change_x = (c.PLAYER_MOVEMENT_SPEED-((self.player.center_x-200)/50)+(self.score*7))

      elif arcade.key.SPACE:
         if self.player.bottom < c.LAYER_WIDTH * self.player.layer + 100:
            self.player.change_y = c.PLAYER_MOVEMENT_SPEED
            arcade.play_sound(self.jump_sound)


   def on_key_release(self, key, modifiers):
      """Called when the user releases a key."""
      if key == arcade.key.UP or key == arcade.key.W or key == arcade.key.DOWN or key == arcade.key.S:
         self.player.change_y = 0
      if key == arcade.key.LEFT or key == arcade.key.A or key == arcade.key.RIGHT or key == arcade.key.D:
         self.player.change_x = 0


   def on_update(self, delta_time: float):
      """Needed updates for game play. Change in player positions, fire collisions, etc."""

      #tracking coin collisions
      current_coin_layer = self.layers.get_list(self.player.layer,'coin') #gets SpriteLIST
      for coin in current_coin_layer:
         if self.player.collides_with_sprite(coin):
            current_coin_layer.remove(coin)
            self.layers.set_list(self.player.layer,current_coin_layer, 'coinlist')
            self.score += 1
            arcade.play_sound(self.collect_coin_sound)

      #tracking mmob list - fire wall
      for i in range(0,6):
         mob_list = self.layers.get_list(i,'mob')
         for sprite in mob_list:
            sprite.center_x = int(sprite.center_x + sprite.change_x)

      #when fire collision happens, end screen is pulled up
      self.current_enemy_layer = self.layers.get_list(self.player.layer,'mob')
      if self.player.collides_with_list(self.current_enemy_layer):
         lose_view = EndScreen()
         self.window.show_view(lose_view)
         arcade.play_sound(self.fire_sound)

      #tracking where the player is on the screen
      if self.player.bottom < self.player.layer * c.LAYER_WIDTH * self.layer_scale(self.player.layer):
         self.player.bottom = self.player.layer * c.LAYER_WIDTH * self.layer_scale(self.player.layer)
      if self.player.top > self.window.height:
         self.player.top = self.window.height
      if self.player.bottom < 0:
         self.player.bottom = 0
      if self.player.left < 0:
         self.player.left = 0

      #scrolling screen view
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

      #setting win screen if player gets enough berries and distance
      if self.score == 25 and self.player.center_x >= 500:
         win_view = WinScreen()
         self.window.show_view(win_view)
   
      
      self.physics_engine.update()
