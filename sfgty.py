from PyQt5.QtWidgets import QApplication, QWidget, QCheckBox, QPushButton, QTextBrowser
import sys
from PyQt5.QtWidgets import QRadioButton, QLabel


class FocusWindow(QWidget):

    def __init__(self):
        super().__init__()
        self.__init__ui()

    def __init__ui(self):
        self.setGeometry(300, 300, 300, 300)
        self.setWindowTitle('Крестики-нолики')

        self.btn1 = QPushButton('', self)
        self.btn1.move(0, 0)
        self.btn1.resize(20, 20)
        self.btn1.clicked.connect(self.click(self.btn1))

        self.btn2 = QPushButton('', self)
        self.btn2.move(20, 0)
        self.btn2.resize(20, 20)
        self.btn2.clicked.connect(self.click(self.btn2))

        self.btn3 = QPushButton('', self)
        self.btn3.move(40, 0)
        self.btn3.resize(20, 20)
        self.btn3.clicked.connect(self.click(self.btn3))

        self.btn4 = QPushButton('', self)
        self.btn4.move(0, 20)
        self.btn4.resize(20, 20)
        self.btn4.clicked.connect(self.click(self.btn4))

        self.btn5 = QPushButton('', self)
        self.btn5.move(20, 20)
        self.btn5.resize(20, 20)
        self.btn5.clicked.connect(self.click(self.btn5))

        self.btn6 = QPushButton('', self)
        self.btn6.move(40, 20)
        self.btn6.resize(20, 20)
        self.btn6.clicked.connect(self.click(self.btn6))

        self.btn7 = QPushButton('', self)
        self.btn7.move(0, 40)
        self.btn7.resize(20, 20)
        self.btn7.clicked.connect(self.click(self.btn7))

        self.btn8 = QPushButton('', self)
        self.btn8.move(20, 40)
        self.btn8.resize(20, 20)
        self.btn8.clicked.connect(self.click(self.btn8))

        self.btn9 = QPushButton('', self)
        self.btn9.move(0, 40)
        self.btn9.resize(20, 20)
        self.btn9.clicked.connect(self.click(self.btn9))

        self.x = QRadioButton('x', self)
        self.o = QRadioButton('o', self)
        self.player = ''
        self.st = QPushButton('New game', self)
        self.st.resize(75, 20)
        self.st.move(30, 60)
        self.st.clicked.connect(self.start)
        self.line = QLabel(self)
        self.line.resize(150, 20)
        self.line.move(0, 100)
        self.btngroup = []
        self.btngroup.append(self.btn1)
        self.btngroup.append(self.btn2)
        self.btngroup.append(self.btn3)
        self.btngroup.append(self.btn4)
        self.btngroup.append(self.btn5)
        self.btngroup.append(self.btn6)
        self.btngroup.append(self.btn7)
        self.btngroup.append(self.btn8)
        self.btngroup.append(self.btn9)
        self.winner = ''

    def start(self):
        self.btn1.setText('')
        self.btn2.setText('')
        self.btn3.setText('')
        self.btn4.setText('')
        self.btn5.setText('')
        self.btn6.setText('')
        self.btn7.setText('')
        self.btn8.setText('')
        self.btn9.setText('')
        if self.x.isChecked():
            self.player = 'x'
        elif self.o.isChecked():
            self.player - 'o'
        self.winner = ''

    def click(self, btn):
        if btn.text() == '' and self.winner == '':
            btn.setText(self.player)
        if self.btn1 == self.btn2 == self.btn3 and self.btn1 != '' and self.btn1 != ' ':
            self.winner = self.player
        elif self.btn4 == self.btn5 == self.btn6 and self.btn6 != '' and self.btn6 != ' ':
            self.winner = self.player
        elif self.btn7 == self.btn8 == self.btn9 and self.btn9 != '' and self.btn9 != ' ':
            self.winner = self.player
        elif self.btn1 == self.btn4 == self.btn7 and self.btn7 != '' and self.btn7 != ' ':
            self.winner = self.player
        elif self.btn2 == self.btn5 == self.btn8 and self.btn8 != '' and self.btn8 != ' ':
            self.winner = self.player
        elif self.btn3 == self.btn6 == self.btn9 and self.btn9 != '' and self.btn9 != ' ':
            self.winner = self.player
        elif self.btn1 == self.btn5 == self.btn9 and self.btn1 != '' and self.btn1 != ' ':
            self.winner = self.player
        elif self.btn7 == self.btn5 == self.btn3 and self.btn3 != '' and self.btn3 != ' ':
            self.winner = self.player
        elif self.btn1 != '' and self.btn2 != '' and self.btn3 != '' and self.btn4 != ''\
                and self.btn5 != '' and self.btn6 != '' and self.btn7 != '' and self.btn8 != ''\
                and self.btn9 != '' and self.btn1 != ' ' and self.btn2 != ' ' and \
                self.btn3 != ' ' and self.btn4 != ' ' and self.btn5 != ' ' and\
                self.btn6 != ' ' and self.btn7 != ' ' and self.btn8 != ' ' and self.btn9 != ' '\
                and self.winner != '':
            self.line.setText('Ничья')
            self.btn1.setText(' ')
            self.btn2.setText(' ')
            self.btn3.setText(' ')
            self.btn4.setText(' ')
            self.btn5.setText(' ')
            self.btn6.setText(' ')
            self.btn7.setText(' ')
            self.btn8.setText(' ')
            self.btn9.setText(' ')
        if self.winner != '':
            self.line.setText(self.winner + ' win')
            self.btn1.setText(' ')
            self.btn2.setText(' ')
            self.btn3.setText(' ')
            self.btn4.setText(' ')
            self.btn5.setText(' ')
            self.btn6.setText(' ')
            self.btn7.setText(' ')
            self.btn8.setText(' ')
            self.btn9.setText(' ')
        if self.btn1 != ' ':
            if self.player == 'x':
                self.player = '0'
            elif self.player == 'o':
                self.player = 'x'


if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = FocusWindow()
    window.show()

    app.exec()
