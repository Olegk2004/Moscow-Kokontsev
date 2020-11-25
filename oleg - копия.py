import sys

from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QTableWidget
from PyQt5.QtWidgets import QLabel, QLCDNumber, QLineEdit, QLayout, QInputDialog
import random
from PyQt5.QtCore import QTimer
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

        self.null_count = 0

        self.table = QTableWidget(self)
        self.table.move(325, 0)
        self.table.resize(600, 500)
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(["имя", "время(сек)", "результат", "очки", "сложность"])

        self.watch_player_games = QPushButton('Показать все игры игрока', self)
        self.watch_player_games.resize(150, 20)
        self.watch_player_games.move(0, 375)
        self.watch_player_games.clicked.connect(self.player_games)
        self.name_input = QLineEdit(self)
        self.name_input.move(150, 375)
        self.name_input.resize(150, 20)

        self.watch_all_games = QPushButton('Показать все игры', self)
        self.watch_all_games.resize(150, 20)
        self.watch_all_games.move(0, 400)
        self.watch_all_games.clicked.connect(self.all_games)

        self.watch_win_games = QPushButton('Показать победные игры', self)
        self.watch_win_games.resize(150, 20)
        self.watch_win_games.move(0, 430)
        self.watch_win_games.clicked.connect(self.win_games)

        self.watch_lose_games = QPushButton('Показать проигранные игры', self)
        self.watch_lose_games.resize(150, 20)
        self.watch_lose_games.move(0, 475)
        self.watch_lose_games.clicked.connect(self.lose_games)

        self.watch_hard_games = QPushButton('Показать сложные игры', self)
        self.watch_hard_games.resize(150, 20)
        self.watch_hard_games.move(0, 500)
        self.watch_hard_games.clicked.connect(self.hard_games)

        self.watch_med_games = QPushButton('Показать средние игры', self)
        self.watch_med_games.resize(150, 20)
        self.watch_med_games.move(0, 525)
        self.watch_med_games.clicked.connect(self.med_games)

        self.watch_easy_games = QPushButton('Показать легкие игры', self)
        self.watch_easy_games.resize(150, 20)
        self.watch_easy_games.move(0, 550)
        self.watch_easy_games.clicked.connect(self.easy_games)

        self.end_game = False
        QTimer.singleShot(1000, self.update)
        self.time = -99999
        self.time_label = QLabel(self)
        self.time_label.resize(50, 20)
        self.time_label.move(0, 320)
        self.time_label.setText(f'0 секунд')

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

        self.label = QLabel(self)
        self.label.resize(300, 20)
        self.label.move(0, 300)
        self.labelf = QLabel(self)
        self.labelf.resize(300, 20)
        self.labelf.move(150, 300)
        self.labelf.setText('вы открываете таблички')
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

    def player_games(self):
        try:
            pname = self.name_input.text()
            cur = self.con.cursor()
            res = cur.execute(f"""SELECT * FROM games
                                WHERE name = ?""", (pname,)).fetchall()
            self.table.setRowCount(len(res))
            for i, elem in enumerate(res):
                for j, val in enumerate(elem):
                    self.table.setItem(i, j, QTableWidgetItem(str(val)))
        except BaseException as e:
            print(e)

    def all_games(self):
        try:
            pname = self.name_input.text()
            cur = self.con.cursor()
            res = cur.execute(f"""SELECT * FROM games""").fetchall()
            self.table.setRowCount(len(res))
            for i, elem in enumerate(res):
                for j, val in enumerate(elem):
                    self.table.setItem(i, j, QTableWidgetItem(str(val)))
        except BaseException as e:
            print(e)

    def win_games(self):
        try:
            resul = 'победа'
            cur = self.con.cursor()
            res = cur.execute(f"""SELECT * FROM games
                                            WHERE result = ?""", (resul,)).fetchall()
            self.table.setRowCount(len(res))
            for i, elem in enumerate(res):
                for j, val in enumerate(elem):
                    self.table.setItem(i, j, QTableWidgetItem(str(val)))
        except BaseException as e:
            print(e)

    def lose_games(self):
        try:
            resul = 'проигрыш'
            cur = self.con.cursor()
            res = cur.execute(f"""SELECT * FROM games
                                WHERE result = ?""", (resul,)).fetchall()
            self.table.setRowCount(len(res))
            for i, elem in enumerate(res):
                for j, val in enumerate(elem):
                    self.table.setItem(i, j, QTableWidgetItem(str(val)))
        except BaseException as e:
            print(e)

    def hard_games(self):
        try:
            level = "Hard"
            cur = self.con.cursor()
            res = cur.execute(f"""SELECT * FROM games
                                WHERE lev = ?""", (level,)).fetchall()
            self.table.setRowCount(len(res))
            for i, elem in enumerate(res):
                for j, val in enumerate(elem):
                    self.table.setItem(i, j, QTableWidgetItem(str(val)))
        except BaseException as e:
            print(e)

    def med_games(self):
        try:
            level = "Medium"
            cur = self.con.cursor()
            res = cur.execute(f"""SELECT * FROM games
                                WHERE lev = ?""", (level,)).fetchall()
            self.table.setRowCount(len(res))
            for i, elem in enumerate(res):
                for j, val in enumerate(elem):
                    self.table.setItem(i, j, QTableWidgetItem(str(val)))
        except BaseException as e:
            print(e)

    def easy_games(self):
        try:
            level = "Easy"
            cur = self.con.cursor()
            res = cur.execute(f"""SELECT * FROM games
                                WHERE lev = ?""", (level,)).fetchall()
            self.table.setRowCount(len(res))
            for i, elem in enumerate(res):
                for j, val in enumerate(elem):
                    self.table.setItem(i, j, QTableWidgetItem(str(val)))
        except BaseException as e:
            print(e)

    def change(self):
        if self.flagi:
            self.flagi = False
            self.labelf.setText('вы открываете таблички')
        else:
            self.flagi = True
            self.labelf.setText('вы ставите флаги')

    def update(self):
        if not self.end_game:
            self.time += 1
            if self.time >= 0:
                self.time_label.setText(f'{self.time} секунд')
            QTimer.singleShot(1000, self.update)

    def hod(self):
        if self.hod_count == self.pole_size ** 2:
            self.time = 0
        btn = self.sender()
        if not self.end_game:
            for i in range(self.pole_size):
                for j in range(self.pole_size):
                    if self.button_list[i][j] == btn:
                        if self.flagi:
                            if self.flag_list[i][j] == '|>':
                                self.flag_list[i][j] = ''
                                self.button_list[i][j].setText('')
                            else:
                                self.flag_list[i][j] = '|>'
                                self.button_list[i][j].setText('|>')
                        else:
                            if self.mean_list[i][j] == '(^)':
                                self.button_list[i][j].setText(str(self.mean_list[i][j]))
                                for i1 in range(self.pole_size):
                                    for j1 in range(self.pole_size):
                                        if self.mean_list[i1][j1] == '(^)':
                                            self.button_list[i1][j1].setText('(^)')
                                            if self.flag_list[i1][j1] == '|>':
                                                self.score += 1
                                self.result = 'проигрыш'
                                self.end_game = True
                                self.label.setText(f"игра окончена {self.result}")
                                try:
                                    cur = self.con.cursor()
                                    cur.execute(
                                        "INSERT INTO games(name, result, score, lev, time) VALUES(?, ?, ?, ?, ?)",
                                        (self.name, self.result, self.score, self.level, self.time))
                                    self.con.commit()
                                except BaseException as e:
                                    print(e)
                            #elif self.mean_list[i][j] == '0':
                                #self.button_list[i][j].setText('0')
                                #self.null_count = 1
                                #iq = i
                                #jq = j
                                #while self.null_count != 0:
                                  #  self.find_null(iq, jq)
                                    #self.button_list[i][j].setText('0')

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
                                                if self.flag_list[i2][j2] == '|>':
                                                    self.score += 1
                                    try:
                                        cur = self.con.cursor()
                                        cur.execute(
                                            "INSERT INTO games(name, result, score, lev, time) VALUES(?, ?, ?, ?, ?)",
                                            (self.name, self.result, self.bomb_count2, self.level, self.time))
                                        self.con.commit()
                                    except BaseException as e:
                                        print(e)

        else:
            try:
                self.label.setText(f"игра окончена {self.result}")
            except Exception as e:
                print(e)

    def find_null(self, i, j):
        self.null_count = 0
        if i > 0 and j > 0:
            if self.mean_list[i - 1][j - 1] == '0':
                self.null_count += 1
                iq = i - 1
                jq = j - 1
        if i > 0:
            if self.mean_list[i - 1][j] == '0':
                self.null_count += 1
                iq = i - 1
                jq = j
        if i > 0 and self.pole_size - j > 1:
            if self.mean_list[i - 1][j + 1] == '0':
                self.null_count += 1
                iq = i - 1
                jq = j + 1
        if j > 0:
            if self.mean_list[i][j - 1] == '0':
                self.null_count += 1
                iq = i
                jq = j - 1
        if self.pole_size - j > 1:
            if self.mean_list[i][j + 1] == '0':
                self.null_count += 1
                iq = i
                jq = j + 1
        if j > 0 and self.pole_size - i > 1:
            if self.mean_list[i + 1][j - 1] == '0':
                self.null_count += 1
                iq = i + 1
                jq = j - 1
        if self.pole_size - i > 1:
            if self.mean_list[i + 1][j] == '0':
                self.null_count += 1
                iq = i + 1
                jq = j
        if self.pole_size - i > 1 and self.pole_size - j > 1:
            if self.mean_list[i + 1][j + 1] == '0':
                self.null_count += 1
                iq = i + 1
                jq = j + 1



if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Trick()
    ex.show()
    sys.exit(app.exec())
