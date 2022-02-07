import pygame

from asset import Asset


class Config:
    DRAWER_ENABLED = False
    WIDTH, HEIGHT = Asset.TRACK.get_width(), Asset.TRACK.get_height()
    WIN = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Racing game")
    FPS = 60
    FINISH_POSITION = (138, 200)
    COMPUTER_CAR_PATH = [(178, 110), (48, 103), (50, 491), (280, 710), (420, 516), (591, 577), (644, 710), (756, 491),
                         (683, 369), (483, 380), (676, 240), (738, 167), (590, 59), (355, 69), (270, 152), (305, 302),
                         (155, 330), (182, 174)]

    @staticmethod
    def draw():
        Config.WIN.blit(Asset.GRASS, (0, 0))
        Config.WIN.blit(Asset.TRACK, (0, 0))
        Config.WIN.blit(Asset.FINISH, Config.FINISH_POSITION)
        Config.WIN.blit(Asset.TRACK_BORDER, (0, 0))
