import sys

from PyQt5.QtWidgets import QApplication, QWidget, QPushButton
from PyQt5.QtWidgets import QLabel, QLCDNumber, QGridLayout, QLayout, QInputDialog
import random
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPainter, QColor
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from sys import argv, executable
import os
from PyQt5 import QtGui
import sqlite3


class Trick(QWidget):
    def __init__(self):
        super().__init__()

        self.setGeometry(300, 100, 700, 700)
        self.setWindowTitle('NIM')

        self.con = sqlite3.connect("sapperBD.db")

        EXIT_CODE_REBOOT = -123

        self.button_string = []

        self.name, self.ok_pressed = QInputDialog.getText(self, "Введите имя", "Как тебя зовут?")
        self.end_game = False
        self.count = 0
        self.hod_count = 0

        self.score = 0

        self.change_flag = QPushButton('флаги', self)
        self.change_flag.move(0, 350)
        self.flagi = False
        self.change_flag.clicked.connect(self.change)

        self.pole_size = 0
        self.bomb_count = 0

        self.restart_button = QPushButton('новая игра', self)
        self.restart_button.move(100, 350)
        self.restart_button.clicked.connect(self.restart)

        self.label = QLabel(self)
        self.label.resize(500, 20)
        self.label.move(0, 300)
        self.result = ''

        self.level, self.ok_pressed = QInputDialog.getItem(
            self, "Выберите уровень", "сложность",
            ("Hard", "Medium", "Easy"))
        print(self.level)
        if self.level == 'Hard':
            self.pole_size = 15
            self.bomb_count = 45
            self.button_list = []
            self.button_size = 20
            for i in range(15):
                for j in range(15):
                    btn = QPushButton('', self)
                    btn.resize(20, 20)
                    btn.move(j * 20, i * 20)
                    self.button_string.append(btn)
                    btn.clicked.connect(self.hod)
                self.button_list.append(self.button_string)
                self.button_string = []
        elif self.level == 'Medium':
            self.pole_size = 10
            self.bomb_count = 20
            self.button_list = []
            self.button_size = 30
            for i in range(10):
                for j in range(10):
                    btn = QPushButton('', self)
                    btn.resize(30, 30)
                    btn.move(j * 30, i * 30)
                    self.button_string.append(btn)
                    btn.clicked.connect(self.hod)
                self.button_list.append(self.button_string)
                self.button_string = []
        elif self.level == 'Easy':
            self.pole_size = 5
            self.bomb_count = 5
            self.button_list = []
            self.button_size = 60
            for i in range(5):
                for j in range(5):
                    btn = QPushButton('', self)
                    btn.resize(60, 60)
                    btn.move(j * 60, i * 60)
                    self.button_string.append(btn)
                    btn.clicked.connect(self.hod)
                self.button_list.append(self.button_string)
                self.button_string = []
        self.mean_list = []
        self.mean_string = []
        self.flag_list = []
        self.flag_string = []
        self.hod_count = self.pole_size ** 2
        self.bomb_count2 = self.bomb_count
        for i in range(self.pole_size):
            for j in range(self.pole_size):
                self.mean_string.append(0)
                self.flag_string.append(0)
            self.mean_list.append(self.mean_string)
            self.mean_string = []
            self.flag_list.append(self.flag_string)
            self.flag_string = []
        print(self.pole_size, " ", self.bomb_count)
        for i in range(self.bomb_count):
            row = random.randint(0, self.pole_size - 1)
            strin = random.randint(0, self.pole_size - 1)
            if self.mean_list[row][strin] != '(^)':
                self.mean_list[row][strin] = '(^)'
                # for q in range(self.pole_size):
                #    print(self.mean_list[q])
                # print('----------')
            else:
                row = random.randint(0, self.pole_size - 1)
                strin = random.randint(0, self.pole_size - 1)
                self.mean_list[row][strin] = '(^)'
        for i in range(self.pole_size):
            for j in range(self.pole_size):
                self.count = 0
                if self.mean_list[i][j] != '(^)':
                    if i > 0 and j > 0:
                        if self.mean_list[i - 1][j - 1] == '(^)':
                            self.count += 1
                    if i > 0:
                        if self.mean_list[i - 1][j] == '(^)':
                            self.count += 1
                    if i > 0 and self.pole_size - j > 1:
                        if self.mean_list[i - 1][j + 1] == '(^)':
                            self.count += 1
                    if j > 0:
                        if self.mean_list[i][j - 1] == '(^)':
                            self.count += 1
                    if self.pole_size - j > 1:
                        if self.mean_list[i][j + 1] == '(^)':
                            self.count += 1
                    if j > 0 and self.pole_size - i > 1:
                        if self.mean_list[i + 1][j - 1] == '(^)':
                            self.count += 1
                    if self.pole_size - i > 1:
                        if self.mean_list[i + 1][j] == '(^)':
                            self.count += 1
                    if self.pole_size - i > 1 and self.pole_size - j > 1:
                        if self.mean_list[i + 1][j + 1] == '(^)':
                            self.count += 1
                    self.mean_list[i][j] = str(self.count)

    def change(self):
        if self.flagi:
            self.flagi = False
        else:
            self.flagi = True

    def hod(self):
        btn = self.sender()
        if not self.end_game:
            for i in range(self.pole_size):
                for j in range(self.pole_size):
                    if self.button_list[i][j] == btn:
                        if self.flagi:
                            self.flag_list[i][j] = '|>'
                            self.button_list[i][j].setText('|>')
                        else:
                            if self.flag_list[i][j] == '|>':
                                self.flag_list[i][j] = ''
                                self.button_list[i][j].setText('')
                            elif self.mean_list[i][j] == '(^)':
                                self.button_list[i][j].setText(str(self.mean_list[i][j]))
                                for i1 in range(self.pole_size):
                                    for j1 in range(self.pole_size):
                                        if self.mean_list[i1][j1] == '(^)':
                                            self.button_list[i1][j1].setText('(^)')
                                            if self.flag_list[i1][j1] == '(^)':
                                                self.score += 1
                                self.result = 'проигрыш'
                                self.end_game = True
                                self.label.setText(f"игра окончена {self.result}")
                                try:
                                    cur = self.con.cursor()
                                    cur.execute(
                                        "INSERT INTO games(name, result, score) VALUES(?, ?, ?)", (self.name, self.result, self.score))
                                    self.con.commit()
                                except BaseException as e:
                                    print(e)
                            else:
                                self.button_list[i][j].setText(str(self.mean_list[i][j]))
                                self.hod_count -= 1
                                if self.hod_count == self.bomb_count2:
                                    self.result = 'победа'
                                    self.end_game = True
                                    for i2 in range(self.pole_size):
                                        for j2 in range(self.pole_size):
                                            if self.mean_list[i2][j2] == '(^)':
                                                self.button_list[i2][j2].setText('(^)')
                                                if self.flag_list[i2][j2] == '(^)':
                                                    self.score += 1
                                    cur = self.con.cursor()
                                    cur.execute(
                                        "INSERT INTO games(name, result, score) VALUES(?, ?, ?)", (self.name, self.result, self.score))
                                    self.con.commit()

        else:
            try:
                self.label.setText(f"игра окончена {self.result}")
            except Exception as e:
                print(e)

    def restart(self):
        pass


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Trick()
    ex.show()
    sys.exit(app.exec())
