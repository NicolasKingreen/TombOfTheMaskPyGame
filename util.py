import pygame

from colors import *

pygame.init()
font_size = 30
padding = 10
font = pygame.font.Font(None, font_size)


def draw(text, x=0, y=0, color=RED):
    surface = pygame.display.get_surface()
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect(topleft=(padding + x, padding + y * (font_size + padding)))
    surface.blit(text_surface, text_rect)
