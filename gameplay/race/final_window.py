# Main libs imports
import pygame
from PyQt5 import uic, QtCore, QtWidgets
from PyQt5.QtGui import QCloseEvent
from PyQt5.QtWidgets import QApplication, QMainWindow

# Other libs imports
import sys

# Other game parts
# EMPTY

# System constants
# EMPTY

# Game constants
# EMPTY


class FinalWindow(QMainWindow):
    def __init__(self, distance, level, earned, crash=True):
        super().__init__()
        uic.loadUi("gameplay/race/final_window.ui", self)
        self.setWindowTitle("Game Over")

        if not crash:
            self.crash.setText("You decided to give up and go home.")
            self.crash.setStyleSheet("")

        # Setting every label
        self.distance.setText(str(round(distance / 2500)) + " km")
        if level == 1:
            self.level.setText("Easy")
        elif level == 2:
            self.level.setText("Normal")
        elif level == 3:
            self.level.setText("Hard")
        self.earned.setText("$" + str(round(earned, 2)))

        # Connecting
        self.close_btn.pressed.connect(self.exit)

    def exit(self):
        self.close()


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


def main(distance, level, earned, crash=True):
    # Fix HiDPI
    if hasattr(QtCore.Qt, "AA_EnableHighDpiScaling"):
        QtWidgets.QApplication.setAttribute(
            QtCore.Qt.AA_EnableHighDpiScaling, True
        )
    if hasattr(QtCore.Qt, "AA_UseHighDpiPixmaps"):
        QtWidgets.QApplication.setAttribute(
            QtCore.Qt.AA_UseHighDpiPixmaps, True
        )
    app = QApplication(sys.argv)
    ex = FinalWindow(distance, level, earned, crash)
    ex.show()
    sys.excepthook = except_hook
    app.exec_()
    del app
    del ex


if __name__ == "__main__":
    main()
