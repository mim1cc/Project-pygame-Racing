# Main libs imports
import threading
import time

import pygame

# Other game parts
import gameplay.start_menu.start_menu
import gameplay.highway_menu.highway_menu
from gameplay.settings_menu.settings import settings
import gameplay.race.renderer
import resources.currency_operations
from gameplay.race.reset_on_exit import reset
import resources.Highways.Highway
from gameplay.race import final_window
import resources.Explosion

# System constants
# EMPTY

# Game constants
from resources.fonts.FONTS import (
    ORBITRON_REGULAR,
    ORBITRON_MEDIUM,
    ORBITRON_EXTRA_BOLD,
)


class Race:
    def __init__(self, heading_y=20):
        settings.update_scaling()
        scaling = settings.get_scaling()
        # 1. Menu
        font = pygame.font.Font(ORBITRON_REGULAR, int(20 * scaling))
        self.menu = font.render("Menu", True, pygame.Color("green"))
        self.menu_x = self.menu.get_width()
        self.menu_y = self.menu.get_height()
        self.heading_y = heading_y  # For compatibility
        # General
        self.margin = int(30 * scaling)
        # Prevent resizing
        self.screen_locked = False
        # Create renderer instance
        self.r = None
        self.ar = None
        # Count distance
        self.distance = 0
        # Darken animation
        self.d = 0
        # Store pause state
        self.paused = False

    def render(self, screen, paused=False):
        # Initialize renderer and async renderer
        if self.r is None or self.ar is None:
            self.r = gameplay.race.renderer.Renderer(screen)
            self.ar = gameplay.race.renderer.AsyncRenderer(screen)
            self.ar.create_daemons()

        # Prevent resizing
        if not self.screen_locked:
            screen = pygame.display.set_mode(
                (screen.get_width(), screen.get_height()), vsync=settings.VSYNC
            )
            self.screen_locked = True

        self.paused = paused  # Store paused state

        # Call all threads to make them start performing background tasks before rendering
        self.ar.generate()

        # Game engine:
        # Rendering
        self.r.render_background()
        self.r.render_cars()

        # Move sprite
        if not paused:
            self.r.move_highways()
            self.r.move_traffic()

        # Render GUI parts (must always be at the top):
        # Menu button
        screen.blit(
            self.menu,
            (
                self.margin,
                self.margin + self.heading_y // 2 - self.menu_y // 2,
            ),
        )
        pygame.draw.rect(
            screen,
            pygame.Color("green"),
            (
                self.margin - 5,
                self.margin + self.heading_y // 2 - self.menu_y // 2 - 5,
                self.menu_x + 10,
                self.menu_y + 10,
            ),
            1,
        )

        # Start explosion animation one time only
        if (
            pygame.sprite.spritecollide(
                settings.selected_car, settings.vehicles, False
            )
            != [settings.selected_car]
            and self.d == 0
        ):
            pos = settings.selected_car.rect.x, settings.selected_car.rect.y
            threading.Thread(
                target=self.ar.explosion_animation, daemon=True, args=(pos,)
            ).start()

        # Do the fade-out animation and get explosion animation
        if (
            pygame.sprite.spritecollide(
                settings.selected_car, settings.vehicles, False
            )
            != [settings.selected_car]
            or self.d != 0
        ):
            for s in pygame.sprite.spritecollide(
                settings.selected_car, settings.vehicles, False
            ):
                s.crashed = True
            surface = pygame.Surface(
                (screen.get_width(), screen.get_height())
            ).convert_alpha()
            self.d += 5 * (60 / settings.FPS)
            surface.fill((0, 0, 0, self.d))
            screen.blit(surface, (0, 0))
            car_pos = (
                settings.selected_car.rect.x,
                settings.selected_car.rect.y,
            )
            if self.ar.explosion.cur_frame < len(self.ar.explosion.frames):
                screen.blit(
                    self.ar.explosion.action, [i - 100 for i in car_pos]
                )
            if self.d > 254:
                return "exit_to_menu"

        if not settings.selected_car.crashed:
            self.distance += settings.selected_car.v

    def key_handler(self, screen, keys):
        if self.paused:
            return None
        car = settings.selected_car
        if car.crashed:
            return None
        arrows_on = settings.CONTROLS == "Arrows"
        if (
            arrows_on
            and keys[pygame.K_RIGHT]
            or not arrows_on
            and keys[pygame.K_d]
        ):
            car.rect.x += 6 / (settings.FPS / 60)
            if (
                car.rect.x
                > settings.selected_highway.rect.x
                + settings.selected_highway.rect.w
                - car.rect.w
            ):
                car.rect.x = (
                    settings.selected_highway.rect.x
                    + settings.selected_highway.rect.w
                    - car.rect.w
                )
        if (
            arrows_on
            and keys[pygame.K_LEFT]
            or not arrows_on
            and keys[pygame.K_a]
        ):
            car.rect.x -= 6 / (settings.FPS / 60)
            if car.rect.x < settings.selected_highway.rect.x:
                car.rect.x = settings.selected_highway.rect.x
        if (
            arrows_on
            and keys[pygame.K_UP]
            or not arrows_on
            and keys[pygame.K_w]
        ):
            car.v += car.get_acceleration() / (settings.FPS / 60)
            if settings.selected_car.v > settings.selected_car.get_speed():
                settings.selected_car.v = settings.selected_car.get_speed()
        if (
            arrows_on
            and keys[pygame.K_DOWN]
            or not arrows_on
            and keys[pygame.K_s]
        ):
            car.v -= car.get_brakes() / (settings.FPS / 60)
            if car.v < settings.NPC_v + 2:
                car.v = settings.NPC_v + 2

    def click_handler(self, pos, screen):
        # Menu button
        rect = [
            range(self.margin - 5, self.margin - 5 + self.menu_x + 10),
            range(
                self.margin + self.heading_y // 2 - self.menu_y // 2 - 5,
                self.margin
                + self.heading_y // 2
                - self.menu_y // 2
                - 5
                + self.menu_y
                + 10,
            ),
        ]
        if pos[0] in rect[0] and pos[1] in rect[1]:
            # Make screen resizable again
            screen = pygame.display.set_mode(
                (screen.get_width(), screen.get_height()),
                pygame.RESIZABLE,
                vsync=settings.VSYNC,
            )

            # Give the player money for the ride
            # Level multipliers: 100, 125, 150%
            m = self.distance / 2500 * (1 + (settings.level - 1) * 0.25)
            # Call final window
            is_crash = (
                pygame.sprite.spritecollide(
                    settings.selected_car, settings.vehicles, False
                )
                != [settings.selected_car]
                or self.d != 0
            )
            final_window.main(self.distance, settings.level, m, crash=is_crash)
            co = resources.currency_operations.CurrencyOperations()
            co.add(int(m))

            # Stop and remove renderers and threads
            self.ar.stop()
            del self.r
            time.sleep(0.001)
            del self.ar

            reset()  # Call to reinitialize all objects
            pygame.event.clear()
            return gameplay.highway_menu.highway_menu.HighwayMenu()

        return self

    def right_click_handler(self, pos, screen):
        return self

    # Should only be called by main.py and race.py
    def exit_to_menu(self, screen):
        # Menu button
        rect = [
            range(self.margin - 5, self.margin - 5 + self.menu_x + 10),
            range(
                self.margin + self.heading_y // 2 - self.menu_y // 2 - 5,
                self.margin
                + self.heading_y // 2
                - self.menu_y // 2
                - 5
                + self.menu_y
                + 10,
            ),
        ]
        return self.click_handler([rect[0][1], rect[1][1]], screen)
