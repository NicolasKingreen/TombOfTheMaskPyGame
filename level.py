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
            pygame.draw.rect(surface, (255, 255, 255), tile.rect, 1)

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


class Camera:

    def __init__(self, level, player, game_surface):
        self.game_surface = game_surface
        self.level = level
        self.player = player

        self.all_objects = [self.player]
        self.all_objects.append(self.level.tiles)

        self.offset = pygame.math.Vector2()

        self.zoom_scale = 1

        self.internal_surf_size = (1000, 1000)
        self.internal_surf = pygame.Surface(self.internal_surf_size, pygame.SRCALPHA)
        self.internal_rect = self.internal_surf.get_rect(center=(self.game_surface.get_width() // 2, self.game_surface.get_width() // 2))
        self.internal_surf_vector = pygame.math.Vector2(self.internal_surf_size)
        self.internal_offset = pygame.math.Vector2()

        self.speed = 800
        self.acceleration = pygame.math.Vector2()
        self.move_dir = pygame.math.Vector2()

        self.center_target_camera(self.player)

        self.target_center = pygame.math.Vector2()

    def center_target_camera(self, target):

        self.offset.x = target.rect.centerx - self.internal_surf.get_width() // 2
        self.offset.y = target.rect.centery - self.internal_surf.get_height() // 2

    def motion(self, frame_time_s):
        self.target_center = pygame.math.Vector2(self.player.rect.centerx - self.internal_surf.get_width() // 2,
                                            self.player.rect.centery - self.internal_surf.get_height() // 2)




        vector = pygame.math.Vector2(self.target_center.x, self.target_center.y) - pygame.math.Vector2(self.offset.x, self.offset.y)
        self.acceleration = self.target_center.distance_to(self.offset)
        print(self.acceleration)

        if vector.length() != 0:
            vector = vector.normalize()
        else:
            vector = pygame.math.Vector2()

        if not abs(self.target_center.x - self.offset.x) < 4 or not abs(self.target_center.y - self.offset.y) < 4:

            self.offset.x += vector.x * self.speed * frame_time_s * self.acceleration * 0.009
            self.offset.y += vector.y * self.speed * frame_time_s * self.acceleration * 0.009

        #print(vector)

    def custom_draw(self):
        self.internal_surf.fill(GRAY32)

        for obj in self.level.tiles + [self.player]:
            offset_pos = (obj.rect.topleft - self.offset + self.internal_offset)

            # blit
            if obj != self.player:
                if obj.type == TileType.COIN:
                    pygame.draw.circle(self.internal_surf, YELLOW, (offset_pos.x, offset_pos.y), obj.rect.width)
                if obj.type == TileType.WALL:
                    pygame.draw.rect(self.internal_surf, GRAY198, [int(offset_pos.x), int(offset_pos.y), TILESIZE, TILESIZE])
                if obj.type == TileType.EXIT:
                    pygame.draw.rect(self.internal_surf, DARKSLATEBLUE, [int(offset_pos.x), int(offset_pos.y), TILESIZE, TILESIZE])
            else:
                pygame.draw.rect(self.internal_surf, INDIANRED, [int(offset_pos.x), int(offset_pos.y), TILESIZE, TILESIZE])

        pygame.draw.rect(self.internal_surf, (255, 0, 0),
                         [self.internal_surf.get_width() // 2, self.internal_surf.get_height() // 2, 1, 1])

        scaled_surf = pygame.transform.scale(self.internal_surf, self.internal_surf_vector * self.zoom_scale)
        scaled_rect = scaled_surf.get_rect(center=(self.game_surface.get_width() // 2, self.game_surface.get_height() // 2))

        self.game_surface.blit(scaled_surf, scaled_rect)

    def update(self, frame_time_s):
        self.motion(frame_time_s)


if __name__ == '__main__':
    level = Level.from_img("img/maps/test_level.bmp")
