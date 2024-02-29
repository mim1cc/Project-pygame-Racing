# Main libs imports
import pygame

# Other libs imports
import sys

# System constants
VERSION = "1.0"

# Other game parts
import gameplay.start_menu.welcome_window
import gameplay.start_menu.start_menu
from gameplay.settings_menu.settings import settings
import gameplay.car_menu.car_menu
import gameplay.highway_menu.highway_menu
import gameplay.race.race

# Game constants
reinitialization_required = False
selected_highway = None
# Default size: 900x700, do not change these variables in code
size = width, height = 900, 700

if __name__ == "__main__":
    # Initializing the game
    pygame.init()

    # Setting system settings and variables
    pygame.display.set_caption(f"Racing (version {VERSION})")
    clock = pygame.time.Clock()
    screen = pygame.display.set_mode(
        size, pygame.RESIZABLE, vsync=settings.VSYNC
    )
    running = True

    current_frame = 0  # to change speed of different elements

    # Start a game with the welcome window
    gameplay.start_menu.welcome_window.generate_welcome()

    # Initialize the 1st menu
    current_position = gameplay.start_menu.start_menu.StartMenu()

    # Pause for race()
    paused = False

    while running:
        screen.fill(settings.get_dimmed_color())
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                # Make race stop if in game
                if type(current_position) == gameplay.race.race.Race:
                    current_position = current_position.exit_to_menu(screen)
                # Quitting
                pygame.quit()
                running = False
                sys.exit()  # Just to make sure there are no errors
            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == pygame.BUTTON_LEFT:
                    r = current_position.click_handler(
                        pos=event.pos, screen=screen
                    )
                    if r is not None:
                        current_position = r
                if event.button == pygame.BUTTON_RIGHT:
                    r = current_position.right_click_handler(
                        pos=event.pos, screen=screen
                    )
                    if r is not None:
                        current_position = r
            # Check if window is resized
            if event.type == pygame.VIDEORESIZE:
                w = screen.get_width()
                h = screen.get_height()
                # Check if size is too small
                if w < width / 3:
                    w = width // 3
                if h < height / 3:
                    h = height // 3
                if (w, h) != (screen.get_width(), screen.get_height()):
                    screen = pygame.display.set_mode(
                        (w, h), pygame.RESIZABLE, vsync=settings.VSYNC
                    )

                # Some magical calculations to make the screen
                # look as beautiful as possible
                size_deviations = sorted([w / width - 1, h / height - 1])
                settings.RSF = abs(size_deviations[0] + 1)
                settings.MSF = abs(size_deviations[1] + 1)
                # Applying scaling
                settings.update_scaling()
                del w, h

                # This menus require saving selection
                menus = [
                    gameplay.car_menu.car_menu.CarMenu,
                    gameplay.highway_menu.highway_menu.HighwayMenu,
                ]
                if type(current_position) in menus:
                    sel = current_position.selected
                    current_position.__init__(selected=sel)
                else:
                    current_position.__init__()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    paused = not paused

        # To handle holded keys in race
        if isinstance(current_position, gameplay.race.race.Race):
            current_position.key_handler(screen, keys=pygame.key.get_pressed())

        # Render current menu
        if isinstance(current_position, gameplay.race.race.Race):
            render_code = current_position.render(screen, paused)
        else:
            render_code = current_position.render(screen)

        # Check if it's race and the game is finished
        if render_code == "exit_to_menu" and isinstance(
            current_position, gameplay.race.race.Race
        ):
            current_position = current_position.exit_to_menu(screen)
            paused = False

        current_frame = (current_frame + 1) % settings.FPS
        pygame.display.flip()
        if settings.PRECISE_FPS:
            clock.tick_busy_loop(settings.FPS)
        else:
            clock.tick(settings.FPS)

    pygame.quit()
