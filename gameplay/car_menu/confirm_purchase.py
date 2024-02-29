# Main libs imports
import pygame
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication, QMessageBox

# Other libs imports
import sys

# Other game parts
# EMPTY

# System constants
# EMPTY

# Game constants
# EMPTY


def confirm_car_purchase(cost=0):
    app = QApplication(sys.argv)
    w = QMessageBox()
    w.setIcon(QMessageBox.Question)
    w.setWindowTitle("Do you want to buy this car?")
    w.setText(f"This car costs ${str(cost)}.")
    w.setStandardButtons(QMessageBox.Cancel | QMessageBox.Yes)
    w.setDefaultButton(QMessageBox.Yes)
    if w.exec() == QMessageBox.Yes:
        pygame.event.clear()
        return True
    pygame.event.clear()
    return False
