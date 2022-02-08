from assets.asset import Asset
from config import Config
from items.car import Car


class Collider:

    @staticmethod
    def handle_collisions(cars: [Car]):
        for car in cars:
            if car.collide(Asset.TRACK_BORDER_MASK) is not None:
                car.bounce()
            finish_poi_collide_player = car.collide(Asset.FINISH_MASK, *Config.FINISH_POSITION)
            if car.collide(Asset.FINISH_MASK, *Config.FINISH_POSITION):
                car.check_lap_timer()
                if finish_poi_collide_player[1] == 0:
                    if car.locked_start is True:
                        car.bounce()
                    else:
                        car.lap_started = True

                if finish_poi_collide_player[1] == 15 and car.locked_start is True:
                    car.lap_finished = True
                    print(f"{car} finished the lap!")
