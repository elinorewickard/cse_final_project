import arcade
import constants as c
from startup import Startup

class InstructionView(arcade.View):
    def __init__(self):
      """"class constructor. Sets up the window."""
      super().__init__()
    
    def on_show(self):
      """This runs when we switch to this view."""
      arcade.set_background_color([100, 100, 100, 0])
      #resets the viewport for scrolling game
      arcade.set_viewport(0, c.SCREEN_WIDTH - 1, 0, c.SCREEN_HEIGHT - 1)

    def on_draw(self):
        """ Draw this view """
        arcade.start_render()
        arcade.draw_text("Starting Screen", c.SCREEN_WIDTH / 2, c.SCREEN_HEIGHT / 2,
                         arcade.color.WHITE, font_size=50, anchor_x="center")
        arcade.draw_text("Click to continue...", c.SCREEN_WIDTH / 2, c.SCREEN_HEIGHT / 2-75,
                         arcade.color.WHITE, font_size=20, anchor_x="center")

    def on_mouse_press(self, _x, _y, _button, _modifiers):
        """ If the user presses the mouse button, start the game. """
        game_view = Startup()
        game_view.setup()
        self.window.show_view(game_view)