# Необходимо реинициализировать все объекты, а также
# заново загрузить все машины и трассы.
# Функция reset() вызывается из Race.click_handler() последней при выходе,
# после чего Race.click_handler() совршает переход в меню трасс.

import resources.Vehicles.Vehicle
from gameplay.settings_menu.settings import settings


def reset() -> None:
    cars = resources.Vehicles.Vehicle.create_all_vehicles()
    for car_obj in cars:
        if settings.selected_car.name == car_obj.name:
            settings.selected_car = car_obj
