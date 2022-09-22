import pygame
from pygame.math import Vector2

from colors import *
from tile import TileType, TILESIZE


class Camera:

    def __init__(self, level, player, game_surface):
        self.game_surface = game_surface
        self.level = level
        self.player = player

        self.offset = Vector2()

        self.zoom_scale = 1

        self.internal_surf_size = (1000, 1000)
        self.internal_surf = pygame.Surface(self.internal_surf_size, pygame.SRCALPHA)
        self.internal_rect = self.internal_surf.get_rect(center=self.game_surface.get_rect().center)
        self.internal_surf_vector = Vector2(self.internal_surf_size)
        self.internal_offset = Vector2()

        self.speed = 800
        self.acceleration = Vector2()
        self.move_dir = Vector2()

        self.center_target_camera(self.player)

        self.target_center = Vector2()

    def center_target_camera(self, target):
        self.offset = Vector2(target.rect.center) - Vector2(self.internal_surf.get_rect().center)

    def motion(self, frame_time_s):
        self.target_center = Vector2(self.player.rect.center) - Vector2(self.internal_surf.get_rect().center)

        camera_to_target = self.target_center - self.offset
        camera_to_target and camera_to_target.normalize_ip()

        self.acceleration = self.target_center.distance_to(self.offset) * 0.009
        if camera_to_target.magnitude() < 4:
            self.offset += camera_to_target * self.speed * frame_time_s * self.acceleration

    def custom_draw(self):
        self.internal_surf.fill(GRAY32)

        for obj in self.level.tiles + [self.player]:
            offset_pos = (obj.rect.topleft - self.offset + self.internal_offset)

            if obj is self.player:
                pygame.draw.rect(self.internal_surf, INDIANRED,
                                 [int(offset_pos.x), int(offset_pos.y), TILESIZE, TILESIZE])
            else:
                if obj.type == TileType.COIN:
                    pygame.draw.circle(self.internal_surf, YELLOW,
                                       (offset_pos.x, offset_pos.y), obj.rect.width)
                elif obj.type == TileType.WALL:
                    pygame.draw.rect(self.internal_surf, GRAY198,
                                     [int(offset_pos.x), int(offset_pos.y), TILESIZE, TILESIZE])
                elif obj.type == TileType.EXIT:
                    pygame.draw.rect(self.internal_surf, DARKSLATEBLUE,
                                     [int(offset_pos.x), int(offset_pos.y), TILESIZE, TILESIZE])

        # dot in the center of the screen
        # pygame.draw.rect(self.internal_surf, (255, 0, 0),
        #                  [self.internal_surf.get_width() // 2, self.internal_surf.get_height() // 2, 1, 1])

        scaled_surf = pygame.transform.scale(self.internal_surf, self.internal_surf_vector * self.zoom_scale)
        scaled_rect = scaled_surf.get_rect(center=self.game_surface.get_rect().center)

        self.game_surface.blit(scaled_surf, scaled_rect)

    def update(self, frame_time_s):
        self.motion(frame_time_s)
        if self.zoom_scale < 1.2:
            self.zoom_scale += 3.4 * frame_time_s
