import arcade
import constants as c
from startup import Startup

class StartScreen(arcade.View):
    def __init__(self):
      """"class constructor. Sets up the window."""
      super().__init__()
    
    def on_show(self):
      """This runs when we switch to this view."""
      arcade.set_background_color((200,100,50,100))
      #resets the viewport for scrolling game
      arcade.set_viewport(0, c.SCREEN_WIDTH - 1, 0, c.SCREEN_HEIGHT - 1)

    def on_draw(self):
        """ Draw this view """
        arcade.start_render()
        arcade.draw_text("Welcome to Wall of Flames", c.SCREEN_WIDTH / 2, c.SCREEN_HEIGHT - 100,
                arcade.color.WHITE, font_size=40, anchor_x="center")
        arcade.draw_text("A fire has broken out in the forest while you\nwere gathering berries. Now you have to travel\nfar enough through the woods and collect\nenough berries to sucessfully get out!", c.SCREEN_WIDTH / 2, c.SCREEN_HEIGHT / 2,
                         arcade.color.WHITE, font_size=35, anchor_x="center", align="center")
        arcade.draw_text("• Use AD or side arrow keys to move \n• WS or up and down arrow keys to move to different levels on the screen \n• and space to jump over obstacles.", c.SCREEN_WIDTH / 2, c.SCREEN_HEIGHT / 2-180,
                  arcade.color.WHITE, font_size=20, anchor_x="center", align="left")
        arcade.draw_text("Click to start...", c.SCREEN_WIDTH / 2, c.SCREEN_HEIGHT / 2-220,
                         arcade.color.WHITE, font_size=20, anchor_x="center")

    def on_mouse_press(self, _x, _y, _button, _modifiers):
        """ When the user presses the mouse button, start the game. """
        game_view = Startup()
        game_view.setup()
        self.window.show_view(game_view)