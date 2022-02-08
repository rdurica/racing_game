import pygame

from assets.asset import Asset
from config import Config
from items.car import ComputerCar


class Drawer:

    @staticmethod
    def draw_path(event, computer_car: ComputerCar):
        """
        Draw path for computer car
        Left click to draw a point
        Left shift + click to remove last point
        Left alt + click to reset car position and start again

        """
        if not Config.DRAWER_ENABLED:
            return

        if event.type == pygame.MOUSEBUTTONDOWN:
            if pygame.key.get_mods() & pygame.KMOD_LSHIFT:
                computer_car.path.pop(len(computer_car.path) - 1)
            elif pygame.key.get_mods() & pygame.KMOD_LALT:
                computer_car.resset_position()
            else:
                pos = pygame.mouse.get_pos()
                computer_car.path.append(pos)

    @staticmethod
    def draw_layout():
        Config.WIN.blit(Asset.GRASS, (0, 0))
        Config.WIN.blit(Asset.TRACK, (0, 0))
        Config.WIN.blit(Asset.FINISH, Config.FINISH_POSITION)
        Config.WIN.blit(Asset.TRACK_BORDER, (0, 0))
