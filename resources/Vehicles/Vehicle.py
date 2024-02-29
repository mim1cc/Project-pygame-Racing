# Important note:
# All non-playable vehicles must have size ≥ player vehicle's size
import pygame.image
import resources.Vehicles.Textures.TEXTURES
import sqlite3
import pygame.sprite
from gameplay.settings_menu.settings import settings
from PIL import Image


def create_all_vehicles(initialize=True):
    vehicles = []
    # Connect to the DB
    con = sqlite3.connect("resources/Vehicles/vehicles_table.db")
    cur = con.cursor()
    data = cur.execute("SELECT * from vehicle_table").fetchall()
    cur.close()
    # Create vehicles
    for car in data:
        # print(*car[0:5], (car[5], car[6], car[7]))
        vehicles.append(
            resources.Vehicles.Vehicle.Vehicle(
                *car[0:5],
                (car[5], car[6], car[7]),
                initialize=initialize,
                cost=car[8],
            )
        )
        vehicles[-1].set_texture(
            vehicles[-1].get_texture(width=30)
        )  # Make all cars have same width

    return vehicles


# CREATE TABLE "vehicle_table" (
# 	"name"	TEXT NOT NULL UNIQUE,
# 	"img"	TEXT NOT NULL,
# 	"speed"	INTEGER NOT NULL,
# 	"brakes"	INTEGER NOT NULL,
# 	"acceleration"	INTEGER NOT NULL,
# 	"speed_multiplier"	INTEGER NOT NULL,
# 	"brakes_multiplier"	INTEGER NOT NULL,
# 	"acceleration_multiplier"	INTEGER NOT NULL,
# 	"cost"	INTEGER
# );


class Vehicle(pygame.sprite.Sprite):
    def __init__(
        self,
        name,
        img,
        speed,
        brakes,
        acceleration,
        multipliers=(1, 1, 1),
        x=0,
        y=0,
        initialize=True,
        reverse=False,
        cost=None,
    ):
        # To prevent non-initialized object from rendering
        self.render = initialize

        if self.render:
            super().__init__(settings.vehicles)
        else:
            pass
        self.image = pygame.image.load(img)
        self.im = Image.open(img)
        self.name = name

        self.cost = cost

        self.speed = speed  # Max speed
        self.brakes = brakes / 3
        self.acceleration = acceleration / 3

        self.reversed = False
        if reverse:
            self.revese()

        # print('hi', self.speed, self.acceleration, self.brakes)

        self.speed_multiplier = multipliers[0]
        self.brakes_multiplier = multipliers[1]
        self.acceleration_multiplier = multipliers[2]

        self.v = settings.NPC_v + 2  # Current speed

        self.crashed = False

        self.x, self.y = x, y
        self.rect = self.image.get_rect()

    def load_image(self, name, colorkey=-1):
        if colorkey is not None:
            if colorkey == -1:
                colorkey = name.get_at((0, 0))
            name.set_colorkey(colorkey)
        else:
            name = name.convert_alpha()
        return name

    def pil_to_surf(self, pilImage):
        return self.load_image(
            pygame.image.fromstring(
                pilImage.tobytes(), pilImage.size, pilImage.mode
            ).convert()
        )

    def get_texture(self, scale=1, width=None, height=None):
        py_img = self.pil_to_surf(self.im)
        if width is not None:
            scale = width / self.image.get_rect()[2]
        if height is not None:
            scale = height / self.image.get_rect()[3]
        if width is not None and height is not None:
            return pygame.transform.scale(py_img, (width, height))
        return pygame.transform.scale(
            py_img, (self.rect[2] * scale, self.rect[3] * scale)
        )

    def get_width(self, scale=1):
        return self.rect[2] * scale // 1

    def get_height(self, scale=1):
        return self.rect[3] * scale // 1

    def get_multipliers(self):
        return (
            self.speed_multiplier,
            self.brakes_multiplier,
            self.acceleration_multiplier,
        )

    def set_speed_multiplier(self, new_speed_multiplier):
        con = sqlite3.connect("resources/Vehicles/vehicles_table.db")
        cur = con.cursor()
        cur.execute(
            f"UPDATE vehicle_table SET speed_multiplier = {new_speed_multiplier} WHERE name = '{self.name}'"
        )
        con.commit()
        con.close()

    def set_brakes_multiplier(self, new_brakes_multiplier):
        con = sqlite3.connect("resources/Vehicles/vehicles_table.db")
        cur = con.cursor()
        cur.execute(
            f"UPDATE vehicle_table SET brakes_multiplier = {new_brakes_multiplier} WHERE name = '{self.name}'"
        )
        con.commit()
        con.close()

    def set_acceleration_multiplier(self, new_acceleration_multiplier):
        con = sqlite3.connect("resources/Vehicles/vehicles_table.db")
        cur = con.cursor()
        cur.execute(
            f"UPDATE vehicle_table SET acceleration_multiplier = {new_acceleration_multiplier} WHERE name = '{self.name}'"
        )
        con.commit()
        con.close()

    def set_lane(self, lane, width):
        lane_w = width / settings.selected_highway.get_total_lanes()
        self.rect.x = lane_w * lane + 0.5 * (lane_w - self.get_width())

    def do_render(self):
        self.render = True
        super().__init__(settings.vehicles)

    def set_texture(self, img):
        self.image = img
        self.rect = img.get_rect()

    def get_speed(self):
        return self.speed * self.speed_multiplier

    def get_acceleration(self):
        return self.acceleration * self.acceleration_multiplier

    def get_brakes(self):
        return self.brakes * self.brakes_multiplier

    def reverse(self):
        self.image = pygame.transform.rotate(self.image, 180)
        self.reversed = not self.reversed

    def set_purchased(self):
        con = sqlite3.connect("resources/Vehicles/vehicles_table.db")
        cur = con.cursor()
        cur.execute(
            f"UPDATE vehicle_table SET cost = NULL WHERE name = '{self.name}'"
        )
        con.commit()
        con.close()
