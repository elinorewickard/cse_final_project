from layersprite import LayerSprite
from arcade import SpriteList
class LayerWork():
    def __init__(self):
        self.layer_list = [[SpriteList(),SpriteList()]] #moblist, then blocklist

    def add_layer(self,count = 1):
        for i in range(count):
            self.layer_list.insert(0,[SpriteList(),SpriteList()]) 

    def add_sprite(self, sprite, stype = "block"):
        if sprite.layer < self.length():
            if stype == "block":
                self.layer_list[sprite.layer][0].insert(0,sprite)
            else: #player and other objects
                self.layer_list[sprite.layer][1].insert(0,sprite)
        else: 
            self.add_layer()
            self.add_sprite(sprite,stype)

    def add_block(self,sprite):
        self.add_sprite(sprite,"block")

    def add_mob(self,sprite):
        self.add_sprite(sprite,"mob")

    def get_list(self):
        return self.layer_list

    def get_block_list(self,layer):
        return self.layer_list[layer][0]

    def get_mob_list(self,layer):
        return self.layer_list[layer][1]

    def length(self):
        return len(self.layer_list)
    
