# Main libs imports
import pygame
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication, QMessageBox

# Other libs imports
import sys


def generate_not_enough_money_error(cost=0):
    app = QApplication(sys.argv)
    w = QMessageBox()
    w.setIcon(QMessageBox.Critical)
    w.setWindowTitle("Error")
    w.setText(
        f"You do not have enough money. \nThis item/upgrade costs ${str(cost)}."
    )
    w.exec()
    pygame.event.clear()
