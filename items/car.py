from abc import ABC
import math

import pygame

from asset import Asset


class Car(ABC):

    def __init__(self, max_vel, rotation_vel):
        self.max_vel = max_vel
        self.rotation_vel = rotation_vel
        self.vel, self.angle = 0, 0
        self.img = None
        self.x, self.y = 0, 0
        self.acceleration = 0.1

    def navigation(self):
        keys = pygame.key.get_pressed()
        moved = False

        if keys[pygame.K_LEFT]:
            self._rotate(left=True)
        if keys[pygame.K_RIGHT]:
            self._rotate(right=True)
        if keys[pygame.K_UP]:
            moved = True
            self.move_forward()
        if keys[pygame.K_DOWN]:
            moved = True
            self.move_backward()
        if not moved:
            self._reduce_speed()

    def draw(self, win):
        Asset.blit_rotate_center(win, self.img, (self.x, self.y), self.angle)

    def move_forward(self):
        self.vel = min(self.vel + self.acceleration, self.max_vel)
        self._move()

    def move_backward(self):
        self.vel = max(self.vel - self.acceleration, -self.max_vel / 2)
        self._move()

    def set_start_position(self, x, y):
        self.x = x
        self.y = y

    def set_asset(self, asset):
        self.img = asset

    def collide(self, mask, x=0, y=0):
        car_mask = pygame.mask.from_surface(self.img)
        offset = (int(self.x - x), int(self.y - y))
        poi = mask.overlap(car_mask, offset)

        return poi

    def _rotate(self, left=False, right=False):
        if left:
            self.angle += self.rotation_vel
        elif right:
            self.angle -= self.rotation_vel

    def _move(self):
        radians = math.radians(self.angle)
        vertical = math.cos(radians) * self.vel
        horizontal = math.sin(radians) * self.vel

        self.y -= vertical
        self.x -= horizontal

    def _reduce_speed(self):
        self.vel = max(self.vel - self.acceleration / 2, 0)
        self._move()


class PlayerCar(Car):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.set_start_position(145, 220)
        self.set_asset(Asset.RED_CAR)
