import pygame 

class Tilekind:
    def __init__(self, name, image, is_solid):
        self.name = name 
        self.image = pygame.image.load(image)
        self.is_solid = is_solid

class Map:
    def __init__(self, map_file, tile_kinds, tile_size):
        self.tile_kinds = tile_kinds
        
    #load map file 
    file = open(map_fiel, 'r')
    data = file.read()
    file.close()

    #set the tiles from load data 
    self.tiles = []

        

    #set tile loaded data 


