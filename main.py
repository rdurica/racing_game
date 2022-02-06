import pygame

from asset import Asset
from config import Config
from items.car import PlayerCar


class App:

    def __init__(self):
        self.is_running = True
        self.lap_started = False
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
                player_car.bounce()

            finish_poi_collide = player_car.collide(Asset.FINISH_MASK, *Config.FINISH_POSITION)
            if player_car.collide(Asset.FINISH_MASK, *Config.FINISH_POSITION):
                player_car.check_lap_timer()
                if finish_poi_collide[1] == 0:
                    if player_car.locked_start is True:
                        player_car.bounce()
                    else:
                        player_car.lap_started = True

                if finish_poi_collide[1] == 19 and player_car.locked_start is True:
                    print("--- Finished ---")

        pygame.quit()


if __name__ == "__main__":
    app = App()
    app.run()
