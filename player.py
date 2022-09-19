import pygame
from pygame.locals import *
from pygame.math import Vector2

from colors import *
from tile import TileType, TILESIZE


class Player:
    def __init__(self, level):
        self.level = level
        self.level_finished = False
        self.pos = Vector2(level.player_spawn)

        self.move_dir = Vector2()
        self.x_target = None
        self.y_target = None

        self.start_speed = 400
        self.max_speed = 1500
        self.acceleration = 5000
        self.speed = self.start_speed

        self.score = 0

    @property
    def rect(self):
        return pygame.Rect(self.pos, (TILESIZE, TILESIZE))

    def get_input(self, keydowns, keyups):
        if not self.move_dir:
            for key in keydowns:
                if key == K_d:
                    self.move_dir.x += 1
                    break
                elif key == K_a:
                    self.move_dir.x -= 1
                    break
                elif key == K_s:
                    self.move_dir.y += 1
                    break
                elif key == K_w:
                    self.move_dir.y -= 1
                    break

    def update(self, frame_time_s):
        self.speed = min(self.speed + self.acceleration * frame_time_s, self.max_speed)  # acceleration
        if Vector2(self.level.exit) == self.pos:
            self.level_finished = True

        for coin_tile in self.level.get_tiles_by_type(TileType.COIN):
            if pygame.Rect(coin_tile.pos, (TILESIZE, TILESIZE)).colliderect(self.rect):
                self.level.remove_tile(coin_tile)
                self.score += 1

        # TODO: combine x and y somehow
        if self.x_target is None and self.move_dir.x != 0:
            left_tile, right_tile = self.level.get_lr_tiles(self.pos)
            if self.move_dir.x > 0:
                self.x_target = right_tile
            elif self.move_dir.x < 0:
                self.x_target = left_tile
        elif self.y_target is None and self.move_dir.y != 0:
            tile_above, tile_below = self.level.get_ud_tiles(self.pos)
            if self.move_dir.y > 0:
                self.y_target = tile_below
            elif self.move_dir.y < 0:
                self.y_target = tile_above

        if self.x_target:
            delta_x = self.move_dir.x * self.speed * frame_time_s
            if delta_x > 0:
                if (self.pos.x + TILESIZE) + delta_x < self.x_target.pos.x:
                    self.pos.x += delta_x
                else:
                    self.pos.x = self.x_target.pos.x - TILESIZE
                    self.move_dir.x = 0
                    self.speed = self.start_speed
                    self.x_target = None
            elif delta_x < 0:
                if self.pos.x + delta_x > self.x_target.pos.x + TILESIZE:
                    self.pos.x += delta_x
                else:
                    self.pos.x = self.x_target.pos.x + TILESIZE
                    self.move_dir.x = 0
                    self.speed = self.start_speed
                    self.x_target = None
        elif self.y_target:
            delta_y = self.move_dir.y * self.speed * frame_time_s
            if delta_y > 0:
                if (self.pos.y + TILESIZE) + delta_y < self.y_target.pos.y:
                    self.pos.y += delta_y
                else:
                    self.pos.y = self.y_target.pos.y - TILESIZE
                    self.move_dir.y = 0
                    self.speed = self.start_speed
                    self.y_target = None
            elif delta_y < 0:
                if self.pos.y + delta_y > self.y_target.pos.y + TILESIZE:
                    self.pos.y += delta_y
                else:
                    self.pos.y = self.y_target.pos.y + TILESIZE
                    self.move_dir.y = 0
                    self.speed = self.start_speed
                    self.y_target = None

    # def _x_movement(self, frame_time_s):  # old
    #     direction = self.move_dir.x
    #     left_tile, right_tile = self.level.get_lr_tiles(self.pos)  # empty list
    #     if direction > 0:
    #         delta_x = min(right_tile.pos.x - (self.pos.x * TILESIZE), direction * self.speed * frame_time_s)
    #     else:
    #         delta_x = max(left_tile.pos.x - (self.pos.x * TILESIZE), direction * self.speed * frame_time_s)
    #     self.pos += Vector2(delta_x)

    def draw(self, surface):
        pygame.draw.rect(surface, INDIANRED, (self.pos, (TILESIZE, TILESIZE)))

    def __repr__(self):
        x, y = self.pos
        return f"Player<({x}, {y})>"
