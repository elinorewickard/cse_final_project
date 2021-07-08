from layersprite import LayerSprite
from arcade import SpriteList
import arcade
class LayerWork():
    def __init__(self):

        self.layer_list = [SpriteList(), SpriteList(), SpriteList(), SpriteList(), SpriteList(), SpriteList()] #moblist, then blocklist

    def add_layer(self,count = 1):
        for i in range(count):
            self.layer_list.insert(0,SpriteList()) #add a layer to the beginning

    def add_sprite(self, sprite: LayerSprite, stype = "block"):
        if sprite.layer < self.length():
            if stype == "block":
                self.layer_list[sprite.layer].insert(0, sprite) #order of sprites in spritelist does not matter
            else: #player and other objects \/
                self.layer_list[sprite.layer].append(sprite)
        else: 
            self.add_layer()
            self.add_sprite(sprite,stype)

    #DOES NOT WORK
    def move_layer(self,sprite,goal_layer): #this assumes that the sprite is the LAST sprite in its layer list
        current_layer = self.layer_list[sprite.layer]
        for item in current_layer:
            if item._get_texture() == sprite._get_texture():
                print(item)
                '''self.layer_list[goal_layer].pop(-1) #remove from current layer, and then place on goal_layer
                sprite.set_layer(goal_layer)
                self.layer_list[goal_layer].insert(-1,sprite)'''

    def add_block(self,sprite: LayerSprite):
        self.add_sprite(sprite,"block")

    def add_mob(self,sprite: LayerSprite):
        self.add_sprite(sprite,"mob")

    def get_list(self):
        return self.layer_list

    def get_block_list(self,layer: int):
        return self.layer_list[layer]

    def get_all(self):
        master_list = SpriteList()
        for layer in self.layer_list:
            for sprite in layer:
                master_list.insert(0,sprite)
        return master_list

    def get_mob_list(self,layer: int):
        return self.layer_list[layer]

    def length(self):
        return len(self.layer_list)
    
