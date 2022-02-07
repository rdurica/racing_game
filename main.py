import pygame

from asset import Asset
from config import Config
from items.car import ComputerCar, PlayerCar


class App:

    def __init__(self):
        self.is_running = True
        self.lap_started = False
        self.clock = pygame.time.Clock()

    def run(self):
        player_car = PlayerCar(max_vel=3.2, rotation_vel=2.5)
        computer_car = ComputerCar(max_vel=3.2, rotation_vel=2.6, path=Config.COMPUTER_CAR_PATH)

        while self.is_running:
            self.clock.tick(Config.FPS)

            Config.draw()
            player_car.draw(Config.WIN)
            computer_car.draw(Config.WIN)
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.is_running = False
                    break

                def path_drawer():
                    """
                    Draw path for computer car
                    Left click to draw a point
                    Left shift + click to remove last point
                    Left alt + click to reset car position and start again

                    """
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        if pygame.key.get_mods() & pygame.KMOD_LSHIFT:
                            computer_car.path.pop(len(computer_car.path) - 1)
                        elif pygame.key.get_mods() & pygame.KMOD_LALT:
                            computer_car.resset_position()
                        else:
                            pos = pygame.mouse.get_pos()
                            computer_car.path.append(pos)

                if Config.DRAWER_ENABLED:
                    path_drawer()

            player_car.navigation()
            computer_car.move()

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

                if finish_poi_collide[1] == 15 and player_car.locked_start is True:
                    print("--- Finished ---")
        print(f"Computer car path: {computer_car.path}")
        pygame.quit()


if __name__ == "__main__":
    app = App()
    app.run()
