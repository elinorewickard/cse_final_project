import constants as c
import arcade
from startup import Startup
from startScreen import StartScreen
# program entry point

def main():
   """ Main method, runs the game when called. """
   window = arcade.Window(c.SCREEN_WIDTH, c.SCREEN_HEIGHT, c.SCREEN_TITLE)
   start_view = StartScreen()
   game_view = Startup()
   window.show_view(start_view)
   game_view.setup()
   arcade.run()

if __name__ == "__main__":
   main()
