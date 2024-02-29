# Main libs imports
import pygame
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication, QMessageBox

# Other libs imports
import sys

# Other game parts
# EMPTY

# System constants
from main import VERSION

# Game constants
# EMPTY


def generate_welcome():
    app = QApplication(sys.argv)
    w = QMessageBox()
    w.setWindowTitle("Welcome!")
    w.setText(
        f"This is the first stable version of this game.\n"
        f"To find get more info, visit our GitHub.\n\n"
        f"\n\nVersion: {VERSION}\t\t\t"
    )
    w.exec()
