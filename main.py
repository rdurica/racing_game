import pygame

from asset import Asset
from config import Config
from items.car import PlayerCar


class App:

    def __init__(self):
        self.is_running = True
        self.clock = pygame.time.Clock()

    def run(self):
        player_car = PlayerCar(max_vel=4, rotation_vel=4)

        while self.is_running:
            self.clock.tick(Config.FPS)

            Config.draw()
            player_car.draw(Config.WIN)
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.is_running = False
                    break

            player_car.navigation()

            if player_car.collide(Asset.TRACK_BORDER_MASK) is not None:
                ...

        pygame.quit()


if __name__ == "__main__":
    app = App()
    app.run()
