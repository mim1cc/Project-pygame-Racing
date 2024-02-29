# Main libs imports
from time import sleep

import pygame

# Other libs imports
import sys
import random
import threading
import random

# Other game parts
import resources.Highways.Highway
import resources.Vehicles.Vehicle
import resources.currency_operations
from gameplay.settings_menu.settings import settings
from resources.Explosion.explosion_animation import Explosion, load_image

# System constants
# EMPTY

# Game constants
# EMPTY


class Renderer:
    def __init__(self, screen):
        # Initializing, setting general variables
        self.screen = screen
        self.width = self.screen.get_width()
        self.height = self.screen.get_height()

        # Setting up highways, and drawing the first one
        self.max_lane_width = 70

        settings.scroll = pygame.sprite.Group(settings.selected_highway)
        hw = settings.selected_highway
        self.padding = 0
        width = hw.get_total_lanes() * self.max_lane_width * settings.MSF
        if width < self.width:
            self.padding = (self.width - width) // 2
        hw.set_texture(hw.get_texture(width=self.width - 2 * self.padding))
        hw.rect.x = self.padding
        hw.rect.y = self.height - hw.get_height(
            width=self.width - 2 * self.padding
        )

        # Setting up the player's car
        self.prepare_car(settings.selected_car)
        settings.selected_car.rect.y = int(
            self.height * 0.8 - settings.selected_car.rect.h
        )
        settings.selected_car.rect.x = (
            self.width // 2 - settings.selected_car.rect.w // 2
        )
        settings.vehicles = pygame.sprite.Group(settings.selected_car)

        # Render highways further
        h = settings.selected_highway.get_height(
            width=self.width - self.padding * 2
        )
        self.preload_scroll = (self.height // h + 1) * 3
        # print(self.preload_scroll)
        self.render_background()

    def render_background(self):
        while len(settings.scroll) <= self.preload_scroll:
            if len(settings.scroll) == 0:
                print("Reset occurred. Consider slowing down.")
                prev_y = self.height - settings.selected_highway.get_height(
                    width=self.width - 2 * self.padding
                )
            else:
                prev_y = min([s.rect.y for s in settings.scroll.sprites()])
            vh = self.create_highway_texture()
            vh.set_texture(vh.get_texture(width=self.width - self.padding * 2))
            vh.rect.x = self.padding
            vh.rect.y = prev_y - settings.selected_highway.get_height(
                width=self.width - self.padding * 2
            )
        settings.scroll.draw(self.screen)

    def render_cars(self):
        settings.vehicles.draw(self.screen)

    def prepare_car(self, car: resources.Vehicles.Vehicle.Vehicle):
        w = (
            (self.width - self.padding * 2)
            / settings.selected_highway.get_total_lanes()
            * 0.6
        )
        car.set_texture(car.get_texture(width=w))

    def prepare_highway(self, highway: resources.Highways.Highway.Highway):
        highway.set_texture(highway.get_texture(width=self.width))

    def create_highway_texture(self):
        hw = settings.selected_highway
        return resources.Highways.Highway.Highway(
            hw.name, hw.image, hw.lanes_per_direction, hw.two_directions
        )

    def move_highways(self):
        v = round(settings.selected_car.v)
        # Do not perform any movement of highways if too few
        if len(settings.scroll.sprites()) <= 2:
            print("critically few HW")
            return 0
        for s in settings.scroll.sprites():
            s.rect.y += v

    def move_traffic(self):
        v = round(settings.selected_car.v)
        for sprite in settings.vehicles.sprites():
            # Moving normal cars
            if (
                sprite.render
                and sprite != settings.selected_car
                and not sprite.crashed
            ):
                if not sprite.reversed:
                    sprite.rect.y += v - settings.NPC_v
                else:
                    sprite.rect.y += v + settings.NPC_v
            # Moving crashed cars
            elif sprite.render and sprite.crashed:
                sprite.rect.y += v


class AsyncRenderer:
    def __init__(self, screen):
        self.screen = screen
        self.daemons = []
        self.run_daemons = True
        self.normal_daemons_count = 0
        self.last_car = None
        self.r = Renderer(screen)
        self.distance = 0
        self.explosion = Explosion(
            load_image("resources/Explosion/explosion.png"), 8, 4, 50, 50
        )

    def generate(self):
        threading.Thread(target=self.check_daemons, daemon=True).start()
        threading.Thread(
            target=self.remove_background_scroll, daemon=True
        ).start()

    def create_daemons(self):
        self.daemons.append(
            threading.Thread(target=self.generate_new_cars, daemon=True)
        )
        self.daemons.append(
            threading.Thread(target=self.remove_background_cars, daemon=True)
        )
        self.normal_daemons_count = len(self.daemons)
        for d in self.daemons:
            d.start()

    def generate_new_cars(self):
        while self.run_daemons:
            if (
                self.last_car is None
                or self.last_car.rect.y
                > self.screen.get_height() / settings.level
            ):
                vhs = []
                for c in resources.Vehicles.Vehicle.create_all_vehicles(False):
                    if c.name != settings.selected_car.name:
                        vhs.append(c)
                vh = random.choice(vhs)
                self.r.prepare_car(vh)
                vh.rect.y = (
                    -300 * settings.level * 0.5
                )  # Make sure the player has enough time to prepare for his level

                # Set lane and position
                num = random.randint(
                    0, settings.selected_highway.get_total_lanes() - 1
                )
                vh.set_lane(num, width=settings.selected_highway.get_width())
                if (
                    settings.selected_highway.two_directions
                    and num < settings.selected_highway.lanes_per_direction
                ):
                    vh.reverse()
                vh.rect.x += settings.selected_highway.rect.x
                vh.do_render()
                self.last_car = vh
            sleep(
                settings.NPC_v / settings.selected_car.v
            )  # Sleep for enough time to preserve battery

    def remove_background_cars(self):
        # Removes cars when they are no longer on the screen
        res = 0
        while self.run_daemons:
            c = 0
            for car in settings.vehicles:
                try:
                    if car.rect.y > self.screen.get_height():
                        res += sys.getsizeof(car)
                        c += 1
                        car.kill()
                        del car
                except AttributeError:
                    pass
            sleep(0.1)

    def remove_background_scroll(self):
        # Removes highway texture when they are no longer on the screen
        for hw in settings.scroll:
            if hw.rect.y > self.screen.get_height():
                hw.kill()
                del hw

    def stop(self):
        self.run_daemons = False
        for d in self.daemons:
            del d

    def check_daemons(self):
        r = False
        for d in self.daemons:
            if not d.is_alive():
                r = True
        if len(self.daemons) < self.normal_daemons_count or r:
            print("Error in daemon(s) occurred. Restarting...")
            self.stop
            sleep(0.001)
            self.create_daemons()

    def explosion_animation(self, pos):
        while self.explosion.cur_frame <= len(self.explosion.frames) - 1:
            self.explosion.update()
            sleep(0.05)
