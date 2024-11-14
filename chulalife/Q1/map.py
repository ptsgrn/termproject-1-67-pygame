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
    for line in data.split("\n"):
        row = []
        for tile_number in line :
            row.append(int(tile_number))
        self.tiles.append(row)
    
    #set the size 
    self.tile_size = tile_size

    def draw(self, screen):
        for y, row in enumerate(self.tiles):
            for x, tile_number in enumerate(row):
                location = (x * self.tile_size, y * self.tile_size)
                image = self.tile_kinds[tile_number].image
                screen.blit(image, location)
        

    #set tile loaded data 


