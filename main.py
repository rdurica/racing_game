import pygame

from config import Config
from items.car import ComputerCar, PlayerCar
from utils.collider import Collider
from utils.drawer import Drawer


class App:

    def __init__(self):
        self.is_running = True
        self.lap_started = False
        self.clock = pygame.time.Clock()

    def run(self):
        player_car = PlayerCar(name="Player", max_vel=3.2, rotation_vel=2.5)
        computer_car = ComputerCar(name="Computer", max_vel=3.2, rotation_vel=2.6, path=Config.COMPUTER_CAR_PATH)

        while self.is_running:
            self.clock.tick(Config.FPS)

            Drawer.draw_layout()
            player_car.draw(Config.WIN)
            computer_car.draw(Config.WIN)
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.is_running = False
                    break

                Drawer.draw_path(event, computer_car)

            player_car.move()
            computer_car.move()
            Collider.handle_collisions([player_car, computer_car])

        if Config.DRAWER_ENABLED:
            print(f"Computer car path: {computer_car.path}")
        pygame.quit()


if __name__ == "__main__":
    app = App()
    app.run()
