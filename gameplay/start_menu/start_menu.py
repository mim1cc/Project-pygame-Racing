# Main libs imports
import pygame

# Other libs imports
# EMPTY

# Other game parts
import gameplay.car_menu.car_menu
import gameplay.settings_menu.settings_menu
from gameplay.settings_menu.settings import settings

# System constants
from main import VERSION

# Game constants
from resources.fonts.FONTS import (
    ORBITRON_MEDIUM,
    ORBITRON_REGULAR,
    ORBITRON_EXTRA_BOLD,
)


class StartMenu:
    def __init__(self):
        scaling = settings.get_scaling()
        # Defining the print
        # 1. Heading
        font = pygame.font.Font(ORBITRON_EXTRA_BOLD, int(70 * scaling))
        self.heading = font.render("Racing", True, pygame.Color("red"))
        self.heading_x = self.heading.get_width()
        self.heading_y = self.heading.get_height()
        # 2. Info
        font = pygame.font.Font(ORBITRON_REGULAR, int(30 * scaling))
        self.info = font.render(
            f"Version: {VERSION}", True, pygame.Color("red")
        )
        self.info_x = self.info.get_width()
        self.info_y = self.info.get_height()
        # 3. Play button
        font = pygame.font.Font(ORBITRON_MEDIUM, int(65 * scaling))
        self.play = font.render("Play", True, pygame.Color("green"))
        self.play_x = self.play.get_width()
        self.play_y = self.play.get_height()
        self.play_margin = 50
        # 4. Settings button
        self.settings = pygame.image.load("resources/Icons/settings_icon.png")
        self.settings_scaling = 1 / (1 * scaling)
        self.settings_margin = int(20 * scaling)
        self.settings = pygame.transform.scale(
            self.settings,
            (self.settings.get_width() // self.settings_scaling,) * 2,
        )
        self.settings_size = self.settings.get_width()

    def render(self, screen):
        # Rendering fonts
        screen.blit(
            self.heading,
            (
                screen.get_width() // 2 - self.heading_x // 2,
                screen.get_height() // 2 - self.heading_y // 2 - self.play_y,
            ),
        )
        screen.blit(self.info, (10, screen.get_height() - self.info_y))
        screen.blit(
            self.play,
            (
                screen.get_width() // 2 - self.play_x // 2,
                screen.get_height() // 2 - self.play_y // 2 + self.play_margin,
            ),
        )
        # Creating a rectangle around the "Play" button
        margin = self.play_margin // 2
        pygame.draw.rect(
            screen,
            pygame.Color("green"),
            (
                screen.get_width() // 2 - self.play_x // 2 - margin,
                screen.get_height() // 2 - self.play_y // 2 + 2 * margin - 10,
                self.play_x + 2 * margin,
                self.play_y + margin,
            ),
            3,
        )

        # Settings icon
        screen.blit(
            self.settings,
            (
                screen.get_width() - self.settings_size - self.settings_margin,
                self.settings_margin,
            ),
        )

    def click_handler(self, pos, screen):
        # Play button
        margin = self.play_margin // 2
        rect = [
            range(
                screen.get_width() // 2 - self.play_x // 2 - margin,
                screen.get_width() // 2
                - self.play_x // 2
                - margin
                + self.play_x
                + 2 * margin,
            ),
            range(
                screen.get_height() // 2 - self.play_y // 2 + 2 * margin - 10,
                screen.get_height() // 2
                - self.play_y // 2
                + 2 * margin
                - 10
                + self.play_y
                + margin,
            ),
        ]
        if pos[0] in rect[0] and pos[1] in rect[1]:
            return gameplay.car_menu.car_menu.CarMenu()
        # Settings button
        rect = [
            range(
                screen.get_width() - self.settings_size - self.settings_margin,
                screen.get_width(),
            ),
            range(0, self.settings_margin + self.settings_size),
        ]
        # print(rect)
        if pos[0] in rect[0] and pos[1] in rect[1]:
            gameplay.settings_menu.settings_menu.main()
            pygame.display.set_mode(
                (screen.get_width(), screen.get_height()),
                pygame.RESIZABLE,
                vsync=settings.VSYNC,
            )
            settings.update_scaling()
            # print(settings.FPS, settings.VSYNC)
            self.__init__()
            pygame.event.clear()

            return self

    def right_click_handler(self, pos, screen):
        return self.click_handler(pos, screen)
