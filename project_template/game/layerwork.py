from layersprite import LayerSprite
from arcade import SpriteList
import arcade
class LayerWork():
    def __init__(self):
                            #coin_list    block_list    mob_list
        self.layer_list = [[SpriteList(), SpriteList(), SpriteList()], [SpriteList(), SpriteList(), SpriteList()],
                           [SpriteList(), SpriteList(), SpriteList()], [SpriteList(), SpriteList(), SpriteList()],
                           [SpriteList(), SpriteList(), SpriteList()], [SpriteList(), SpriteList(), SpriteList()]]

    def add_layer(self,count = 1):
        for i in range(count):
            self.layer_list.insert(0,SpriteList()) #add a layer to the beginning

    def add_sprite(self, sprite: LayerSprite, stype = "block"):
        if sprite.layer < self.length():
            if stype == "block":
                self.layer_list[sprite.layer][1].append(sprite) #order of sprites in spritelist does not matter
            elif stype == "mob": #player and enemies \/
                self.layer_list[sprite.layer][2].append(sprite)
            elif stype == "coin":
                self.layer_list[sprite.layer][0].append(sprite)
        else: 
            self.add_layer()
            self.add_sprite(sprite,stype)

    def add_block(self,sprite: LayerSprite):
        self.add_sprite(sprite,"block")

    def add_mob(self,sprite: LayerSprite):
        self.add_sprite(sprite,"mob")

    def add_coin(self,sprite):
        self.add_sprite(sprite,"coin")

    #def remove_item(self,sprite)

    def get_full_list(self):
        return self.layer_list
    
    def get_list(self,layer: int,stype = 'coin'): #returns a spritelist
        if stype == 'block':
            return self.layer_list[layer][1]
        elif stype == 'mob':
            return self.layer_list[layer][2]
        elif stype == 'coin':
            return self.layer_list[layer][0]

    def set_list(self,layer,slist = SpriteList, stype = 'coinlist'):
        if stype == 'blocklist':
            self.layer_list[layer][1] = slist
        elif stype == 'moblist':
            self.layer_list[layer][2] = slist
        elif stype == 'coinlist':
            self.layer_list[layer][0] = slist

    def get_all(self):
        master_list = SpriteList()
        for a_layer in self.layer_list:
            for a_sprite_list in a_layer:
                for a_sprite in a_sprite_list:
                    master_list.insert(0,a_sprite)
        return master_list

    def get_mob_list(self,layer: int):
        return self.layer_list[layer]

    def length(self):
        return len(self.layer_list)
    
