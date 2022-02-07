from abc import ABC
import datetime
from datetime import datetime, timedelta
import math

import pygame

from asset import Asset
from config import Config


class Car(ABC):

    def __init__(self, name, max_vel, rotation_vel, *args, **kwargs):
        self.name = name
        self.max_vel = max_vel
        self.rotation_vel = rotation_vel
        self.vel, self.angle = 0, 0
        self.img = None
        self.x, self.y = 0, 0
        self.acceleration = 0.1
        self._lap_started = False
        self._lap_start_time = None
        self.locked_start = False
        self._start_position = (145, 220)
        self.current_point = 0
        self.lap_finished = False

    def __str__(self):
        return self.name

    def check_lap_timer(self):
        if not self._lap_start_time or self._lap_started is False:
            return
        present = datetime.now()
        max_time = self._lap_start_time + timedelta(seconds=3)
        if present >= max_time:
            self.locked_start = True

    @property
    def lap_started(self):
        return self._lap_started

    @lap_started.setter
    def lap_started(self, value: bool):
        if value is True:
            if self._lap_started is not True:
                self._lap_start_time = datetime.now()
                self._lap_started = value
        else:
            self._lap_started = value

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

    def resset_position(self):
        self.x, self.y = self._start_position
        self.angle = 0
        self.vel = 0
        self.current_point = 0

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

    def bounce(self):
        ...


class PlayerCar(Car):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.set_start_position(*self._start_position)
        self.set_asset(Asset.RED_CAR)

    def bounce(self):
        self.vel = -self.vel
        self._move()


class ComputerCar(Car):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.path = []
        if "path" in kwargs:
            self.path = kwargs.get("path")
        self.current_point = 0
        self.set_start_position(185, 220)
        self.set_asset(Asset.GREEN_CAR)

    def draw_points(self, win):
        if not Config.DRAWER_ENABLED:
            return
        for point in self.path:
            pygame.draw.circle(win, (255, 0, 0), point, 5)

    def draw(self, win):
        super().draw(win)
        self.draw_points(win)

    def move(self):
        if self.current_point >= len(self.path):
            return

        self._calculate_angle()
        self._update_path_point()
        super().move_forward()

    def _calculate_angle(self):
        target_x, target_y = self.path[self.current_point]
        x_diff = target_x - self.x
        y_diff = target_y - self.y
        if y_diff == 0:
            desired_radian_angle = math.pi / 2
        else:
            desired_radian_angle = math.atan(x_diff / y_diff)

        if target_y > self.y:
            desired_radian_angle += math.pi

        difference_in_angle = self.angle - math.degrees(desired_radian_angle)

        if difference_in_angle >= 180:
            difference_in_angle -= 360

        if difference_in_angle > 0:
            self.angle -= min(self.rotation_vel, abs(difference_in_angle))
        else:
            self.angle += min(self.rotation_vel, abs(difference_in_angle))

    def _update_path_point(self):
        target = self.path[self.current_point]
        rect = pygame.Rect(self.x, self.y, self.img.get_width(), self.img.get_height())
        if rect.collidepoint(*target):
            self.current_point += 1
