import sys

import pygame.event
from PyQt5 import uic, QtCore, QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow

from gameplay.settings_menu.settings import settings


class LevelMenu(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('gameplay/highway_menu/select_level_menu.ui', self)
        self.pushButton.clicked.connect(self.apply)

        # Remove the frame to prevent closing the dialog
        self.setWindowFlags(self.windowFlags() and QtCore.Qt.CustomizeWindowHint)
        # self.setWindowFlags(self.windowFlags() and QtCore.Qt.FramelessWindowHint)

    def apply(self):
        level_sel = self.buttonGroup.checkedButton().text()
        # print(level_sel)
        if level_sel == 'EASY':
            settings.level = 1
        elif level_sel == 'NORMAL':
            settings.level = 2
        else:
            settings.level = 3
        self.close()


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


def main():
    # Fix HiDPI
    if hasattr(QtCore.Qt, 'AA_EnableHighDpiScaling'):
        QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True)
    if hasattr(QtCore.Qt, 'AA_UseHighDpiPixmaps'):
        QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps, True)
    app = QApplication(sys.argv)
    ex = LevelMenu()
    ex.show()
    sys.excepthook = except_hook
    app.exec_()
    del app
    del ex
    pygame.event.clear()


if __name__ == '__main__':
    main()
