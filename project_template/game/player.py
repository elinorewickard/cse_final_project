import arcade
 
class player(object):

 
 
    def on_key_press(self, key, modifiers):
        """Called whenever a key is pressed. """

        if key == arcade.key.UP or key == arcade.key.W or key == arcade.key.SPACE:
            self.player_sprite.change_y = PLAYER_MOVEMENT_SPEED
        if key == arcade.key.DOWN or key == arcade.key.S:
            self.player_sprite.change_y = -PLAYER_MOVEMENT_SPEED
        if key == arcade.key.LEFT or key == arcade.key.A:
            self.player_sprite.change_x = -PLAYER_MOVEMENT_SPEED
        if key == arcade.key.RIGHT or key == arcade.key.D:
            self.player_sprite.change_x = PLAYER_MOVEMENT_SPEED

    def on_key_release(self, key, modifiers):
        """Called when the user releases a key. """

        if key == arcade.key.UP or key == arcade.key.W:
            self.player_sprite.change_y = 0
        if key == arcade.key.DOWN or key == arcade.key.S:
            self.player_sprite.change_y = 0
        if key == arcade.key.LEFT or key == arcade.key.A:
            self.player_sprite.change_x = 0
        if key == arcade.key.RIGHT or key == arcade.key.D:
            self.player_sprite.change_x = 0
