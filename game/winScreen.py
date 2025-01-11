import arcade
import constants as c

class WinScreen(arcade.View):
    def __init__(self):
      """"class constructor. Sets up the window."""
      super().__init__()
    
    def on_show(self):
      """This runs when we switch to this view."""
      arcade.set_background_color((0, 0, 0, 0))
      #resets the viewport for scrolling game
      arcade.set_viewport(0, c.SCREEN_WIDTH - 1, 0, c.SCREEN_HEIGHT - 1)

    def on_draw(self):
        """ Draw this view """
        arcade.start_render()
        arcade.draw_text("You got out!", c.SCREEN_WIDTH / 2, c.SCREEN_HEIGHT / 2,
                         arcade.color.WHITE, font_size=40, anchor_x="center")