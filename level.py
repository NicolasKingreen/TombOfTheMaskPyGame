import pygame

from colors import *
from tile import Tile, TileType, TILESIZE


class Level:
    def __init__(self, level_map):
        self.map = level_map

        self.player_spawn = self.map["player_spawn"]
        self.exit = self.map["exit"]
        self.tiles = self._load_tiles(self.map["tiles"])

    def _load_tiles(self, tile_list):
        tiles = []
        for tile_string in tile_list:
            x, y, tile_type = tile_string
            tile = Tile((x, y), tile_type)
            tiles.append(tile)
        return tiles

    @classmethod
    def from_file(cls, filepath):
        pass

    @classmethod
    def from_img(cls, img_path):
        map_img = pygame.image.load(img_path)
        # colors = map_img.get_palette()
        level_map = {
            "player_spawn": None,
            "exit": None,
            "tiles": []
        }
        for i in range(map_img.get_width()):
            for j in range(map_img.get_height()):
                pixel = map_img.get_at((i, j))
                if pixel[3] != 0:
                    x, y = i * TILESIZE, j * TILESIZE
                    color = pixel[:3]
                    if color == BLACK:
                        level_map["tiles"].append([x, y, TileType.WALL])
                    elif color == YELLOW:
                        level_map["tiles"].append([x, y, TileType.COIN])
                    elif color == ORANGE:
                        level_map["tiles"].append([x, y, TileType.EXIT])
                        level_map["exit"] = (x, y)
                    elif color == MAGENTA:
                        level_map["player_spawn"] = (x, y)
        return cls(level_map)

    def draw(self, surface):
        for tile in self.tiles:
            tile.draw(surface)

    def get_lr_tiles(self, pos):
        x, y = pos
        hard_tiles = self.get_tiles_by_type(TileType.WALL)
        same_row = list(filter(lambda tile: tile.pos.y == y, hard_tiles))
        left_side = list(filter(lambda tile: tile.pos.x < x, same_row))
        right_side = list(filter(lambda tile: tile.pos.x > x, same_row))
        tiles = [left_side[-1], right_side[0]]
        return tiles

    def get_ud_tiles(self, pos):
        x, y = pos
        hard_tiles = self.get_tiles_by_type(TileType.WALL)
        same_col = list(filter(lambda tile: tile.pos.x == x, hard_tiles))
        above = list(filter(lambda tile: tile.pos.y < y, same_col))
        below = list(filter(lambda tile: tile.pos.y > y, same_col))
        tiles = [above[-1], below[0]]
        return tiles

    def get_tiles_by_type(self, tile_type):
        return list(filter(lambda tile: tile.type == tile_type, self.tiles))

    def remove_tile(self, tile):
        if tile in self.tiles:
            self.tiles.remove(tile)


if __name__ == '__main__':
    level = Level.from_img("img/maps/test_level.bmp")
