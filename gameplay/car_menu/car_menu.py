# Main libs imports
import pygame

# Other libs imports
import sys
import random

# Other game parts
import gameplay.start_menu.start_menu
import gameplay.highway_menu.highway_menu
import resources.Vehicles.Vehicle
import resources.currency_operations
from gameplay.settings_menu.settings import settings
from resources.Error_Dialogs.errors_dialogs import generate_not_enough_money_error
from gameplay.car_menu.confirm_purchase import confirm_car_purchase 

# System constants
# EMPTY

# Game constants
from resources.fonts.FONTS import ORBITRON_REGULAR, ORBITRON_MEDIUM, ORBITRON_EXTRA_BOLD
from resources.currency_operations import NotEnoughMoneyException


class CarMenu:
    def __init__(self, selected=1):
        scaling = settings.get_scaling()
        # 1. Heading
        font = pygame.font.Font(ORBITRON_MEDIUM, int(50 * scaling))
        self.heading = font.render('Select Your Car', True, pygame.Color("yellow"))
        self.heading_x = self.heading.get_width()
        self.heading_y = self.heading.get_height()
        # 2. Back
        font = pygame.font.Font(ORBITRON_REGULAR, int(20 * scaling))
        self.back = font.render('Back', True, pygame.Color("green"))
        self.back_x = self.back.get_width()
        self.back_y = self.back.get_height()
        # 3. Next
        font = pygame.font.Font(ORBITRON_REGULAR, int(30 * scaling))
        self.next = font.render('Next', True, pygame.Color("green"))
        self.next_x = self.next.get_width()
        self.next_y = self.next.get_height()
        self.arrow_margin_down = int(10 * scaling)
        self.arrow_height = int(20 * scaling)
        self.arrow_margin = int(20 * scaling)
        # 4. Currency counter
        c = resources.currency_operations.CurrencyOperations()
        font = pygame.font.Font(ORBITRON_REGULAR, int(20 * scaling))
        self.curr = font.render('$' + str(c.get()), True, pygame.Color("green"))
        self.curr_x = self.curr.get_width()
        self.curr_y = self.curr.get_height()
        # Creating Vehicles
        self.vehicles = resources.Vehicles.Vehicle.create_all_vehicles()
        self.selected = selected
        # General
        self.margin = int(30 * scaling)
        # Vehicle scroll
        self.vertical_padding = int(200 * scaling)
        self.scroll_height = int(100 * scaling)
        self.edge_scale = 1.6 * scaling
        self.selected_scale = 2 * scaling
        # print(self.v)
        # Car Specifications:
        # 1. Speed
        font = pygame.font.Font(ORBITRON_REGULAR, int(20 * scaling))
        self.speed = font.render('Speed:', True, pygame.Color("white"))
        self.speed_x = self.speed.get_width()
        self.speed_y = self.speed.get_height()
        # 2. Brakes
        font = pygame.font.Font(ORBITRON_REGULAR, int(20 * scaling))
        self.brakes = font.render('Brakes:', True, pygame.Color("white"))
        self.brakes_x = self.brakes.get_width()
        self.brakes_y = self.brakes.get_height()
        # 3. Acceleration
        font = pygame.font.Font(ORBITRON_REGULAR, int(20 * scaling))
        self.acceleration = font.render('Acceleration:', True, pygame.Color("white"))
        self.acceleration_x = self.acceleration.get_width()
        self.acceleration_y = self.acceleration.get_height()
        # 4. Drawing properties
        self.separator = int(10 * scaling)
        self.rect_width = int(250 * scaling)
        # 5. Upgrade buttons:
        self.upgrade = pygame.image.load('resources/Icons/upgrade_icon_normalized2.png')
        self.upgrade_scaling = 1 / (1 * scaling)
        self.upgrade_margin = int(4 * scaling)
        self.upgrade = pygame.transform.scale(self.upgrade, (self.speed_y + 5 - 2 * self.upgrade_margin,) * 2)
        self.upgrade_size = self.upgrade.get_width()

    def render(self, screen):
            # Heading
            screen.blit(self.heading, (screen.get_width() // 2 - self.heading_x // 2,
                                       self.margin))
            # Back button
            screen.blit(self.back, (self.margin, self.margin + self.heading_y // 2 - self.back_y // 2))
            pygame.draw.rect(screen, pygame.Color('green'),
                             (self.margin - 5, self.margin + self.heading_y // 2 - self.back_y // 2 - 5,
                              self.back_x + 10, self.back_y + 10), 1)
            # Currency counter
            screen.blit(self.curr, (
                screen.get_width() - self.margin - self.curr_x, self.margin + self.heading_y // 2 - self.curr_y // 2))
            pygame.draw.rect(screen, pygame.Color('green'),
                             (screen.get_width() - self.margin - 5 - self.curr_x,
                              self.margin + self.heading_y // 2 - self.curr_y // 2 - 5,
                              self.curr_x + 10, self.curr_y + 10), 1)
            # Arrows to select the vehicle
            pygame.draw.line(screen, pygame.Color('white'),
                             (self.margin // 3 * 2, self.vertical_padding + self.margin),
                             (self.margin // 3, self.vertical_padding + self.scroll_height // 2), 3)
            pygame.draw.line(screen, pygame.Color('white'),
                             (self.margin // 3, self.vertical_padding + self.scroll_height // 2),
                             (self.margin // 3 * 2, self.vertical_padding + self.scroll_height - self.margin), 3)

            pygame.draw.line(screen, pygame.Color('white'),
                             (screen.get_width() - self.margin // 3 * 2, self.vertical_padding + self.margin),
                             (screen.get_width() - self.margin // 3, self.vertical_padding + self.scroll_height // 2), 3)
            pygame.draw.line(screen, pygame.Color('white'),
                             (screen.get_width() - self.margin // 3, self.vertical_padding + self.scroll_height // 2),
                             (screen.get_width() - self.margin // 3 * 2, self.vertical_padding + self.scroll_height -
                              self.margin), 3)
            # Vehicles
            width = (screen.get_width() - self.margin * 4 - 2 * self.margin) // 3
            img_1 = self.vehicles[(self.selected - 1) % len(self.vehicles)]
            img_2 = self.vehicles[self.selected % len(self.vehicles)]
            img_3 = self.vehicles[(self.selected + 1) % len(self.vehicles)]

            screen.blit(img_1.get_texture(self.edge_scale),
                        (self.center_img_horizontally(self.margin, width, img_1.get_width(self.edge_scale), self.margin),
                         self.center_img_vertically(self.vertical_padding, self.scroll_height // 2,
                                                    img_1.get_height(self.edge_scale))))
            screen.blit(img_2.get_texture(self.selected_scale),
                        (self.center_img_horizontally(2 * self.margin + width, width, img_2.get_width(self.selected_scale),
                                                      self.margin),
                         self.center_img_vertically(self.vertical_padding, self.scroll_height // 2,
                                                    img_2.get_height(self.selected_scale))))
            screen.blit(img_3.get_texture(self.edge_scale),
                        (self.center_img_horizontally(3 * self.margin + 2 * width, width, img_3.get_width(self.edge_scale),
                                                      self.margin),
                         self.center_img_vertically(self.vertical_padding, self.scroll_height // 2,
                                                    img_3.get_height(self.edge_scale))))
            # Specifications and upgrades:
            offset_left = .5 * self.rect_width
            # Specification names:
            base_h = int(self.center_img_vertically(self.vertical_padding, self.scroll_height // 2, img_2.get_height(self.edge_scale)) + img_2.get_height(self.edge_scale)) + self.margin * 3
            screen.blit(self.speed, ((screen.get_width() - self.separator) // 2 - self.acceleration_x - offset_left, base_h))
            screen.blit(self.brakes, ((screen.get_width() - self.separator) // 2 - self.acceleration_x - offset_left, base_h + self.margin + self.speed_y))
            screen.blit(self.acceleration, ((screen.get_width() - self.separator) // 2 - self.acceleration_x - offset_left, base_h + self.margin * 2 + self.brakes_y + self.speed_y))
            # Specification values:
            s, b, a = (i - 1.0 for i in img_2.get_multipliers())
            pygame.draw.rect(screen, pygame.Color('green'),
                             ((screen.get_width() + self.separator) // 2 - offset_left, base_h, self.rect_width * s, self.speed_y + 5))
            pygame.draw.rect(screen, pygame.Color('green'),
                             ((screen.get_width() + self.separator) // 2 - offset_left, base_h + self.margin + self.speed_y,
                              self.rect_width * b, self.brakes_y + 5))
            pygame.draw.rect(screen, pygame.Color('green'),
                             ((screen.get_width() + self.separator) // 2 - offset_left,
                              base_h + self.margin * 2 + self.brakes_y + self.speed_y, self.rect_width * a,
                              self.acceleration_y + 5))
            # Borders:
            pygame.draw.rect(screen, pygame.Color('white'),
                             ((screen.get_width() + self.separator) // 2 - offset_left, base_h, self.rect_width, self.speed_y + 5),
                             width=2)
            pygame.draw.rect(screen, pygame.Color('white'),
                             ((screen.get_width() + self.separator) // 2 - offset_left, base_h + self.margin + self.speed_y,
                              self.rect_width, self.brakes_y + 5),
                             width=2)
            pygame.draw.rect(screen, pygame.Color('white'),
                             ((screen.get_width() + self.separator) // 2 - offset_left,
                              base_h + self.margin * 2 + self.brakes_y + self.speed_y, self.rect_width,
                              self.acceleration_y + 5),
                             width=2)

            # Upgrade buttons
            c, w = ('green', 2)
            if img_2.get_multipliers()[0] < 2 and not(img_2.cost):
                screen.blit(self.upgrade, ((screen.get_width() + self.separator) // 2 - offset_left + self.rect_width + self.separator, base_h + self.upgrade_margin))
                pygame.draw.rect(screen, pygame.Color(c), ((screen.get_width() + self.separator) // 2 - offset_left + self.rect_width + self.separator - self.upgrade_margin, base_h, self.upgrade_size + 2 * self.upgrade_margin, self.upgrade_size + 2 * self.upgrade_margin), w)

            if img_2.get_multipliers()[1] < 2 and not(img_2.cost):
                screen.blit(self.upgrade, ((screen.get_width() + self.separator) // 2 - offset_left + self.rect_width + self.separator, base_h + self.margin + self.speed_y + self.upgrade_margin))
                pygame.draw.rect(screen, pygame.Color(c), ((screen.get_width() + self.separator) // 2 - offset_left + self.rect_width + self.separator - self.upgrade_margin, base_h + self.margin + self.speed_y, self.upgrade_size + 2 * self.upgrade_margin, self.upgrade_size + 2 * self.upgrade_margin), w)

            if img_2.get_multipliers()[2] < 2 and not(img_2.cost):
                screen.blit(self.upgrade, ((screen.get_width() + self.separator) // 2 - offset_left + self.rect_width + self.separator,  base_h + self.margin * 2 + self.brakes_y + self.speed_y + self.upgrade_margin))
                pygame.draw.rect(screen, pygame.Color(c), ((screen.get_width() + self.separator) // 2 - offset_left + self.rect_width + self.separator - self.upgrade_margin,  base_h + self.margin * 2 + self.brakes_y + self.speed_y, self.upgrade_size + 2 * self.upgrade_margin, self.upgrade_size + 2 * self.upgrade_margin), w)

            # Next button
            screen.blit(self.next, (screen.get_width() - self.next_x - self.margin,
                                    screen.get_height() - self.next_y - self.margin))
            pygame.draw.line(screen, pygame.Color("green"),
                             (screen.get_width() - self.next_x - self.margin + self.arrow_margin,
                              screen.get_height() - self.next_y - self.arrow_margin_down - self.margin),
                             (screen.get_width() - self.margin - self.arrow_margin,
                              screen.get_height() - self.next_y - self.arrow_margin_down - self.arrow_height - self.margin),
                             8)
            pygame.draw.line(screen, pygame.Color("green"),
                             (screen.get_width() - self.margin - self.arrow_margin,
                              screen.get_height() - self.next_y - self.arrow_margin_down - self.arrow_height - self.margin),
                             (screen.get_width() - self.next_x - self.margin + self.arrow_margin,
                              screen.get_height() - self.next_y - self.arrow_margin_down - 2 * self.arrow_height - self.margin),
                             8)

    def click_handler(self, pos, screen):
        scaling = settings.get_scaling()
        # Back button
        rect = [range(self.margin - 5, self.margin - 5 + self.back_x + 10),
                range(self.margin + self.heading_y // 2 - self.back_y // 2 - 5,
                      self.margin + self.heading_y // 2 - self.back_y // 2 - 5 + self.back_y + 10)]
        if pos[0] in rect[0] and pos[1] in rect[1]:
            new_menu = gameplay.start_menu.start_menu.StartMenu()
            return new_menu

        # Next button
        if pos[0] > screen.get_width() - 150 * scaling and pos[1] > screen.get_height() - 150 * scaling:
            if self.vehicles[self.selected].cost is not None:
                if confirm_car_purchase(self.vehicles[self.selected].cost):
                    try:
                        co = resources.currency_operations.CurrencyOperations()
                        co.buy(self.vehicles[self.selected].cost)
                        self.vehicles[self.selected].set_purchased()
                    except NotEnoughMoneyException:
                        generate_not_enough_money_error(self.vehicles[self.selected].cost)
                        return self
                else:
                    return self
            new_menu = gameplay.highway_menu.highway_menu.HighwayMenu()
            settings.selected_car = self.vehicles[self.selected % len(self.vehicles)]
            # settings.selected_highway = self.highways[self.selected % len(self.highways)]
            # print(settings.selected_car)
            return new_menu

        # Scroll buttons
        img_1 = self.vehicles[(self.selected - 1) % len(self.vehicles)]
        img_2 = self.vehicles[self.selected % len(self.vehicles)]
        img_3 = self.vehicles[(self.selected + 1) % len(self.vehicles)]
        if pos[0] < (screen.get_width() - 350 * scaling) // 2 and pos[1] in range(
                int(self.center_img_vertically(self.vertical_padding, self.scroll_height // 2,
                                               img_1.get_height(self.edge_scale))),
                int(self.center_img_vertically(self.vertical_padding, self.scroll_height // 2,
                                               img_1.get_height(self.edge_scale)) + img_1.get_height(self.edge_scale))):
            if self.selected - 1 < 0:
                self.selected = len(self.vehicles) - 1
            else:
                self.selected -= 1
        if pos[0] > (screen.get_width() + 350 * scaling) // 2 and pos[1] in range(
                int(self.center_img_vertically(self.vertical_padding, self.scroll_height // 2,
                                               img_3.get_height(self.edge_scale))),
                int(self.center_img_vertically(self.vertical_padding, self.scroll_height // 2,
                                               img_3.get_height(self.edge_scale)) + img_3.get_height(self.edge_scale))):
            self.selected = (self.selected + 1) % len(self.vehicles)
        if self.vehicles[self.selected].cost is not None:
            font = pygame.font.Font(ORBITRON_REGULAR, int(30 * scaling))
            self.next = font.render('Buy', True, pygame.Color("green"))
        else:
            font = pygame.font.Font(ORBITRON_REGULAR, int(30 * scaling))
            self.next = font.render('Next', True, pygame.Color("green"))
        self.next_x = self.next.get_width()
        self.next_y = self.next.get_height()

        # Upgrade buttons
        offset_left = .5 * (self.rect_width + self.speed_y)
        base_h = int(self.center_img_vertically(self.vertical_padding, self.scroll_height // 2, img_1.get_height(self.edge_scale)) + img_1.get_height(self.edge_scale)) + self.margin * 3
        rect_speed = ((screen.get_width() + self.separator) // 2 - offset_left + self.rect_width + self.separator - self.upgrade_margin, base_h, self.upgrade_size + 2 * self.upgrade_margin, self.upgrade_size + 2 * self.upgrade_margin)
        rect_brakes = ((screen.get_width() + self.separator) // 2 - offset_left + self.rect_width + self.separator - self.upgrade_margin, base_h + self.margin + self.speed_y, self.upgrade_size + 2 * self.upgrade_margin, self.upgrade_size + 2 * self.upgrade_margin)
        rect_acceleration = ((screen.get_width() + self.separator) // 2 - offset_left + self.rect_width + self.separator - self.upgrade_margin,  base_h + self.margin * 2 + self.brakes_y + self.speed_y, self.upgrade_size + 2 * self.upgrade_margin, self.upgrade_size + 2 * self.upgrade_margin)

        co = resources.currency_operations.CurrencyOperations()
        vh = self.vehicles[self.selected % len(self.vehicles)]
        if pos[0] in range(int(rect_speed[0]), int(rect_speed[0]) + 2 * int(rect_speed[2])) and pos[1] in range(int(
                rect_speed[1]), int(rect_speed[1]) + int(rect_speed[3])):
            if vh.get_multipliers()[0] < 2 and vh.cost is None:
                try:
                    co.buy(10)
                    vh.set_speed_multiplier(vh.get_multipliers()[0] + .05)
                    self.__init__(selected=self.selected)
                except NotEnoughMoneyException:
                    generate_not_enough_money_error(10)
        if pos[0] in range(int(rect_brakes[0]), int(rect_brakes[0]) + 2 * int(rect_brakes[2])) and pos[1] in range(int(
                rect_brakes[1]), int(rect_brakes[1]) + int(rect_brakes[3])):
            if vh.get_multipliers()[1] < 2 and vh.cost is None:
                try:
                    co.buy(10)
                    vh.set_brakes_multiplier(vh.get_multipliers()[1] + .05)
                    self.__init__(selected=self.selected)
                except NotEnoughMoneyException:
                    generate_not_enough_money_error(10)
        if pos[0] in range(int(rect_acceleration[0]), int(rect_acceleration[0]) + 2 * int(rect_acceleration[2])) and pos[1] in range(int(rect_acceleration[1]), int(rect_acceleration[1]) + int(rect_acceleration[3])):
            if vh.get_multipliers()[2] < 2 and vh.cost is None:
                try:
                    co.buy(10)
                    vh.set_acceleration_multiplier(vh.get_multipliers()[2] + .05)
                    self.__init__(selected=self.selected)
                except NotEnoughMoneyException:
                    generate_not_enough_money_error(10)
        return self

    def right_click_handler(self, pos, screen):
        return self

    def center_img_horizontally(self, start, width, img_width, arrow_compensation=0):
        t = (width - img_width) // 2
        # print(t + start)
        return t + start + arrow_compensation

    def center_img_vertically(self, start, center, img_height):
        return start + center - img_height // 2
