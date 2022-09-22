import pygame
from pygame.locals import *

import os
import sys

from colors import *
from level import Level
from camera import Camera
from player import Player
from tile import TILESIZE
from util import *


# TODO: camera, spikes, game menu and little tutorial

MAPSIZE = 32

WINSIZETILES = (MAPSIZE * TILESIZE, MAPSIZE * TILESIZE)
WINSIZE240 = 426, 240
WINSIZE480 = 854, 480
WINSIZE720 = 1280, 720
WINSIZE480320 = 480, 320
WINDOW_SIZE = WINDOW_WIDTH, WINDOW_HEIGHT = WINSIZETILES

GUI_PADDING = 40


class Game:
    def __init__(self):
        pygame.display.set_caption("Tomb of the Mask [PyGame]")
        self.main_surface = pygame.display.set_mode((WINSIZETILES[0], WINSIZETILES[1] + GUI_PADDING))
        #self.main_surface = pygame.display.set_mode((WINSIZE720[0], WINSIZE720[1] + GUI_PADDING))
        self.game_surface = pygame.Surface(WINSIZETILES)
        #self.game_surface = pygame.display.set_mode((WINSIZE720[0], WINSIZE720[1] + GUI_PADDING))
        self.clock = pygame.time.Clock()
        self.debug = True
        self.is_running = False

        self.max_fps_records = 60
        self.last_fps_records = []

        filenames = list(*zip(os.walk("img/maps/")))[0][2]
        self.levels = [Level.from_img("img/maps/" + image) for image in filenames]

        # self.current_level = Level.from_img("img/maps/test_level.bmp")
        self.level_n = 0
        self.current_level = self.levels[self.level_n]
        self.player = Player(self.current_level)
        self.camera = Camera(self.current_level, self.player, self.game_surface)
        self.camera.zoom_scale = 0.5

    def run(self):
        self.is_running = True
        while self.is_running:

            frame_time_ms = self.clock.tick()
            frame_time_s = frame_time_ms / 1000.

            self.last_fps_records.append(int(self.clock.get_fps()))
            if len(self.last_fps_records) > self.max_fps_records:
                self.last_fps_records.pop(0)

            keydowns = []
            keyups = []
            for event in pygame.event.get():
                if event.type == QUIT:
                    self.terminate()
                elif event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        self.terminate()
                    elif event.key == K_i:
                        print(self.current_level.get_lr_tiles(self.player.pos))
                        print(self.current_level.get_ud_tiles(self.player.pos))
                    elif event.key == K_u:
                        self.debug = not self.debug
                    else:
                        keydowns.append(event.key)
                elif event.type == KEYUP:
                    keyups.append(event.key)
            self.player.get_input(keydowns, keyups)

            self._update_states(frame_time_s)
            self._draw_frame()

        pygame.quit()
        sys.exit()

    def terminate(self):
        self.is_running = False

    def _update_states(self, frame_time_s):
        self.player.update(frame_time_s)
        self.camera.update(frame_time_s)
        if self.player.level_finished:
            self.level_n = (self.level_n + 1) % len(self.levels)
            self.current_level = self.levels[self.level_n]
            self.player = Player(self.current_level)  # encapsulate player creation by level
            self.camera = Camera(self.current_level, self.player, self.game_surface)


    def _draw_frame(self):

        self.main_surface.fill(GRAY32)

        self.game_surface.fill(GRAY32)
        #self.current_level.draw(self.game_surface)
        #self.player.draw(self.game_surface)
        self.camera.custom_draw()
        self.main_surface.blit(self.game_surface, (0, GUI_PADDING))

        draw(f"Score: {self.player.score}", color=INDIANRED)
        draw(f"Level {self.level_n+1}", x=200, color=INDIANRED)

        if self.debug:
            avg_fps = sum(self.last_fps_records) / len(self.last_fps_records)
            draw(f"{avg_fps:.1f} avg fps", y=4)
        pygame.display.update()


if __name__ == "__main__":
    Game().run()
