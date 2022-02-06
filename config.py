import pygame
from asset import Asset


class Config:
    WIDTH, HEIGHT = Asset.TRACK.get_width(), Asset.TRACK.get_height()
    WIN = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Racing game")
    FPS = 60

    @staticmethod
    def draw():
        Config.WIN.blit(Asset.GRASS, (0, 0))
        Config.WIN.blit(Asset.TRACK, (0, 0))
        Config.WIN.blit(Asset.FINISH, (138, 200))
