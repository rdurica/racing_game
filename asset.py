import pygame
from pygame.surface import Surface


class Asset:

    @staticmethod
    def scale_image(img: Surface, factor: float) -> Surface:
        size = round(img.get_width() * factor), round(img.get_height() * factor)

        return pygame.transform.scale(img, size)

    GRASS = pygame.image.load("assets/img/grass.jpg")
    TRACK = scale_image(pygame.image.load("assets/img/track.png"), 0.9)
    TRACK_BORDER = scale_image(pygame.image.load("assets/img/track-border.png"), 0.9)
    TRACK_BORDER_MASK = pygame.mask.from_surface(TRACK_BORDER)
    FINISH = scale_image(pygame.image.load("assets/img/finish.png"), 1)
    FINISH_MASK = pygame.mask.from_surface(FINISH)
    RED_CAR = scale_image(pygame.image.load("assets/img/red-car.png"), 0.5)
    GREEN_CAR = scale_image(pygame.image.load("assets/img/green-car.png"), 0.5)

    @staticmethod
    def blit_rotate_center(win, image, top_left, angle):
        rotated_image = pygame.transform.rotate(image, angle)
        new_rect = rotated_image.get_rect(center=image.get_rect(topleft=top_left).center)
        win.blit(rotated_image, new_rect.topleft)
