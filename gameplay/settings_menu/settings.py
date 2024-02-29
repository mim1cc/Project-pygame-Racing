import pygame.sprite


class Settings:
    def __init__(self):
        # Public
        self.VSYNC = True
        self.FPS = 60
        self.PRECISE_FPS = False
        self.CONTROLS = "WASD"
        self.GSF = 1  # Global scaling factor, set by the user settings
        self.RSF = 1  # Resize (Real) scaling factor, calculated when resized
        self.MSF = 1  # Min Scaling, calculated when resized for highways

        # Selected, public
        self.selected_car = None
        self.selected_highway = None
        self.vehicles = pygame.sprite.Group()
        self.NPC_v = 5
        self.scroll = pygame.sprite.Group()
        self.color = "Black"

        self.level = 1

        # Private
        self.__SCALING = 1  # Calculated as GSF * RSF

    def update_scaling(self):
        self.__SCALING = self.GSF * self.RSF

    def get_scaling(self) -> float:
        return self.__SCALING

    def get_dimmed_color(self) -> tuple:
        color = list(pygame.Color(self.color))
        for comp in range(len(color)):
            if color[comp] - 100 < 0:
                color[comp] = 0
            else:
                color[comp] = color[comp] - 100
        return tuple(color)


settings = Settings()
