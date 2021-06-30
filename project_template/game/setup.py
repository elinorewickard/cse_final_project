import arcade
import constants as c

class Setup(arcade.Window):
   """setting up game """
   def __init__(self):
      """"class constructor. Sets up the window."""
      super().__init__(c.SCREEN_WIDTH, c.SCREEN_HEIGHT, c.SCREEN_TITLE)
      
      self.player_list = arcade.SpriteList()
      self.block_list = arcade.SpriteList()#use_spatial_hash=True)
      self.hitbox_list = arcade.SpriteList()
      self.layer_list = arcade.SpriteList()

      #separate variable for player sprite
      self.player = arcade.Sprite()

      arcade.set_background_color(arcade.csscolor.GREEN)
      arcade.set_background_color((100,100,100,50))

   def startup(self):
      """set up game here, if called it will restart the game"""
      
      self.player = arcade.Sprite(c.CHAR_IMG, c.SCALING)
      self.player.center_y = c.SCREEN_HEIGHT/2
      self.player.center_x = c.SCREEN_WIDTH/2
      self.player_list.append(self.player)

      self.background = arcade.Sprite(c.BACKGR_IMG)
      self.background.center_y = c.SCREEN_HEIGHT/2
      self.background.center_x = c.SCREEN_WIDTH/2
      self.layer_list.append(self.background)

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
      """Called whenever a key is pressed. """

      if key == arcade.key.UP or key == arcade.key.W or key == arcade.key.SPACE:
         self.player.change_y = c.PLAYER_MOVEMENT_SPEED
      if key == arcade.key.DOWN or key == arcade.key.S:
         self.player.change_y = -c.PLAYER_MOVEMENT_SPEED
      if key == arcade.key.LEFT or key == arcade.key.A:
         self.player.change_x = -c.PLAYER_MOVEMENT_SPEED
      if key == arcade.key.RIGHT or key == arcade.key.D:
         self.player.change_x = c.PLAYER_MOVEMENT_SPEED

   def on_key_release(self, key, modifiers):
      """Called when the user releases a key. """

      if key == arcade.key.UP or key == arcade.key.W or key == arcade.key.DOWN or key == arcade.key.S:
         self.player.change_y = 0
      if key == arcade.key.LEFT or key == arcade.key.A or key == arcade.key.RIGHT or key == arcade.key.D:
         self.player.change_x = 0

   def on_update(self, delta_time: float):

      for sprite in self.player_list:
         if not sprite.collides_with_list(self.hitbox_list):
            sprite.center_x = float(sprite.center_x + sprite.change_x * delta_time)
            sprite.center_y = float(sprite.center_y + sprite.change_y * delta_time)
         else:
            for block in self.hitbox_list:
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