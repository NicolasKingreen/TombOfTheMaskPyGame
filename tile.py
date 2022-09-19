import pygame
from pygame.math import Vector2

from enum import Enum

from colors import *

TILESIZE = 16


class TileType(Enum):
    EMPTY = 0,
    WALL = 1,
    EXIT = 2,
    COIN = 3,
    SPIKE = 4


class Tile:
    def __init__(self, position, tile_type=0):
        self.pos = position if position is Vector2 else Vector2(position)
        self.type = tile_type  # color by type
        if self.type == TileType.WALL:
            self.rect = pygame.Rect(self.pos, (TILESIZE, TILESIZE))
        elif self.type == TileType.EXIT:
            self.rect = pygame.Rect(self.pos, (TILESIZE, TILESIZE))
        elif self.type == TileType.COIN:
            self.rect = pygame.Rect((self.pos.x + TILESIZE // 2, self.pos.y + TILESIZE // 2), (TILESIZE // 8, TILESIZE // 8))

    def __repr__(self):
        x, y = self.pos
        return f"Tile<({x}, {y}), {self.type}>"

    # def draw(self, surface):
    #     # TODO: move this stuff into constructor
    #     if self.type == TileType.WALL:
    #         pygame.draw.rect(surface, GRAY198, (self.pos, (TILESIZE, TILESIZE)))
    #     elif self.type == TileType.EXIT:
    #         pygame.draw.rect(surface, DARKSLATEBLUE, (self.pos, (TILESIZE, TILESIZE)))
    #     elif self.type == TileType.COIN:
    #         pygame.draw.circle(surface, YELLOW, (self.pos.x + TILESIZE // 2, self.pos.y + TILESIZE // 2), TILESIZE // 8)

