from arcade.sprite import Sprite
import constants as c
class LayerSprite(Sprite):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.layer = 0

    def set_layer(self, layer):
        self.change_y -= c.LAYER_WIDTH * (layer - self.layer)
        self.layer = layer

    def push_layer(self):
        self.change_y += c.LAYER_WIDTH
        self.layer -= 1

    def pull_layer(self):
        if self.layer > 0:
            self.change_y -= c.LAYER_WIDTH
            self.layer += 1
