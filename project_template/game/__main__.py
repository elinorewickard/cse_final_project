import arcade
from setup import Setup

# program entry point

def main():
   """ Main method, runs the game when called. """
   window = Setup()
   window.startup()
   arcade.run()

if __name__ == "__main__":
   main()
