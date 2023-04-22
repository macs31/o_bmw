import sys

from PyQt5 import uic

from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, \
    QTableWidgetItem, QMessageBox, QWidget, QInputDialog
import sqlite3
import datetime as dt


# Изменение имени
def save(name):
    with open("Info.txt", mode='w', encoding='utf-8') as g:
        g.write(name)


class MyWidget(QMainWindow):
    '''
    Главное окно с переходом в остальные классы
    '''

    def __init__(self):
        super().__init__()
        uic.loadUi('data/project_liceum.ui', self)
        self.about_the_library.clicked.connect(self.about_the_library_f)
        self.take_a_book.clicked.connect(self.take_a_book_f)
        self.turn_in_a_book.clicked.connect(self.turn_in_a_book_f)
        self.help.clicked.connect(self.help_f)
        self.change_name.clicked.connect(self.change)
        self.fine_history.clicked.connect(self.his)

        with open("Info.txt", mode='r', encoding='utf-8') as f:
            str_1 = f.readline()
            self.name = str_1.rstrip('\n')
            self.hello.setText(f'Приветствую, {self.name}!')

        with open("style.txt", mode='r', encoding='utf-8') as f:
            style = f.readlines()
            style = ''.join(style)

        self.about_the_library.setStyleSheet(style)

        self.take_a_book.setStyleSheet(style)

        self.turn_in_a_book.setStyleSheet(style)

        self.help.setStyleSheet(style)

        self.change_name.setStyleSheet(style)

        self.fine_history.setStyleSheet(style)

        self.setStyleSheet('background-color: "#9999CC"')

    def change(self):
        name, ok_pressed = QInputDialog.getText(self, " ",
                                                "Введите имя, длинной не более 16 символов")
        if ok_pressed:
            if self.name == name:
                self.statusbar().showMessage(f'Новое имя совпадает с текущим')
            elif len(name) <= 16:
                self.name = name
                self.hello.setText(f'Приветствую, {self.name}!')
                save(self.name)
            else:
                self.tip = QMessageBox(self)
                self.tip.setGeometry(300, 300, 200, 100)
                self.tip.setIcon(QMessageBox.Warning)
                self.tip.setWindowTitle('Ошибка')
                self.tip.setText('Имя слишком длинное')
                self.tip.show()

    def about_the_library_f(self):
        self.second_form = SecondForm()
        self.second_form.show()
        self.hide()

    def take_a_book_f(self):
        self.third_form = ThirdForm()
        self.third_form.show()
        self.hide()

    def his(self):
        self.hisor = HistoryFine()
        self.hisor.show()

    def turn_in_a_book_f(self):
        self.fourth_form = FourthForm()
        self.fourth_form.show()
        self.hide()

    def help_f(self):
        self.sixth_form = SixthForm()
        self.sixth_form.show()
        self.hide()


# О библиотеке
class SecondForm(QWidget):
    '''
     Окно с описанием приложения
    '''

    def __init__(self):
        super().__init__()
        uic.loadUi('data/SecondForm.ui', self)
        self.back_secondform.clicked.connect(self.Back_second)

        with open("style.txt", mode='r', encoding='utf-8') as f:
            style = f.readlines()
            style = ''.join(style)

        self.back_secondform.setStyleSheet(style)

        self.setStyleSheet('background-color: "#9999CC"')

    def Back_second(self):
        self.back = MyWidget()
        self.back.show()
        self.hide()

    def closeEvent(self, event):
        ex.show()


# Взять книгу
class ThirdForm(QWidget):
    '''
    Окно в котором обрабатываются, выдача книг пользователям
    '''

    def __init__(self):
        super().__init__()
        uic.loadUi('data/ThirdForm.ui', self)
        self.abs.clicked.connect(self.finded)

        self.back_thirdform.clicked.connect(self.Back_third)
        with open("style.txt", mode='r', encoding='utf-8') as f:
            style = f.readlines()
            style = ''.join(style)

        self.abs.setStyleSheet(style)

        self.back_thirdform.setStyleSheet(style)

        self.setStyleSheet('background-color: "#9999CC"')

        self.fio.setStyleSheet('background-color: white')

    def finded(self):
        con = sqlite3.connect("project_liceum_1")
        cur = con.cursor()
        x = self.fio.text()
        if x == '':
            self.fin = QMessageBox(self)
            self.fin.setGeometry(700, 400, 200, 100)
            self.fin.setIcon(QMessageBox.Warning)
            self.fin.setWindowTitle('Ошибка')
            self.fin.setText('Вы ввели пустой запрос')
            self.fin.show()
            return
        result = cur.execute(f"""SELECT id FROM readers_list WHERE reader = '{x}'""").fetchall()
        if result:
            self.turn_book = Turn_book(self.fio.text())
            self.turn_book.show()
            self.hide()
        else:
            self.resultat.setText('Поисковой запрос неверен или у вас нет читательского дневника')
            refactor = QPushButton('Создать', self)
            refactor.resize(481, 71)
            refactor.move(360, 470)
            refactor.show()
            refactor.clicked.connect(self.RD)

        con.close()

    def RD(self):
        self.fine_2 = Create()
        self.fine_2.show()
        self.hide()

    def Back_third(self):
        self.back = MyWidget()
        self.back.show()
        self.hide()

    def closeEvent(self, event):
        ex.show()


class Turn_book(QWidget):
    '''
    Окно, в котором пользователь вводит книгу, и она добовляется в историю выдачи
    '''

    def __init__(self, t):
        super().__init__()
        self.t = t
        uic.loadUi('data/turn_book.ui', self)
        self.ready_2.clicked.connect(self.Book_title)
        self.back_to_start_2.clicked.connect(self.Back_to_start_2)

        with open("style.txt", mode='r', encoding='utf-8') as f:
            style = f.readlines()
            style = ''.join(style)

        self.ready_2.setStyleSheet(style)

        self.back_to_start_2.setStyleSheet(style)

        self.setStyleSheet('background-color: "#9999CC"')

        self.book_title.setStyleSheet('background-color: white')

    def Book_title(self):
        con = sqlite3.connect("project_liceum_1")
        cur = con.cursor()
        title = self.book_title.text()
        if title == '':
            self.mis = QMessageBox(self)
            self.mis.setGeometry(700, 400, 200, 100)
            self.mis.setIcon(QMessageBox.Warning)
            self.mis.setWindowTitle('Ошибка')
            self.mis.setText('Вы ввели пустой запрос')
            self.mis.show()
            return
        result = cur.execute(f"""SELECT id FROM readers_list WHERE reader = '{self.t}'""").fetchall()
        con.close()

        con = sqlite3.connect("project_liceum_1")
        cur = con.cursor()
        id_book = cur.execute(f"""SELECT id FROM list_books WHERE book = '{title}'""").fetchall()
        con.close()

        con = sqlite3.connect("project_liceum_1")
        cur = con.cursor()
        month = dt.datetime.now().strftime("%m")
        day = dt.datetime.now().strftime("%d")
        year = dt.datetime.now().strftime("%y")
        tr = f'{str(day)}.{str(month)}.{str(year)}'

        result = cur.execute(f"""INSERT INTO books_movement(id_reader, id_book, date) 
        VALUES({result[0][0]}, {id_book[0][0]}, '{tr}')""").fetchall()
        con.commit()
        con.close()

        self.status.setText('Вы успешно взяли книгу. Приятного чтения!')

    def Back_to_start_2(self):
        self.back = MyWidget()
        self.back.show()
        self.hide()

    def closeEvent(self, event):
        ex.show()


# Сдать книгу
class FourthForm(QWidget):
    '''
    Окно, в котором обратываются  книги, которые пользователь сдал
    '''

    def __init__(self):
        super().__init__()
        uic.loadUi('data/FourthForm.ui', self)
        self.back_fourthform.clicked.connect(self.Back_fourth)
        self.ready_3.clicked.connect(self.table)
        self.ready_4.clicked.connect(self.Library_book)

        with open("style.txt", mode='r', encoding='utf-8') as f:
            style = f.readlines()
            style = ''.join(style)

        self.back_fourthform.setStyleSheet(style)

        self.ready_3.setStyleSheet(style)

        self.ready_4.setStyleSheet(style)

        self.setStyleSheet('background-color: "#9999CC"')

        self.fio_2.setStyleSheet('background-color: white')

        self.tableWidget.setStyleSheet('background-color: white')

        self.library_book.setStyleSheet('background-color: white')

    def Back_fourth(self):
        self.back = MyWidget()
        self.back.show()
        self.hide()

    def table(self):
        con = sqlite3.connect("project_liceum_1")
        cur = con.cursor()
        books = cur.execute(f"""SELECT book from list_books""").fetchall()
        con.close()

        con = sqlite3.connect("project_liceum_1")
        cur = con.cursor()
        result = cur.execute(f"""SELECT id_book, date From books_movement WHERE id_reader = 
        (SELECT id From readers_list WHERE reader = '{self.fio_2.text()}')""").fetchall()
        if not result:
            self.tip = QMessageBox(self)
            self.tip.setGeometry(300, 300, 200, 100)
            self.tip.setIcon(QMessageBox.Warning)
            self.tip.setWindowTitle('Ошибка')
            self.tip.setText('Читателя не нашлось')
            self.tip.show()
            return
        self.tableWidget.setRowCount(len(result))
        self.tableWidget.setColumnCount(len(result[0]))
        self.tableWidget.setHorizontalHeaderLabels(['Название книги', 'Дата выдачи'])
        self.titles = [description[0] for description in cur.description]
        for i in range(len(result)):
            result[i] = (*books[result[i][0] - 1], result[i][1])
        for i, elem in enumerate(result):
            for j, val in enumerate(elem):
                self.tableWidget.setItem(i, j, QTableWidgetItem(str(val)))
        self.modified = {}
        con.close()

    def Library_book(self):
        b = self.library_book.text()
        con = sqlite3.connect("project_liceum_1")
        cur = con.cursor()
        result = cur.execute(f"""SELECT date from books_movement Where id_book = 
        (SELECT id from list_books Where book = '{b}') and 
        id_reader = (SELECT id from readers_list Where reader = '{self.fio_2.text()}')""").fetchall()
        if not result:
            self.war = QMessageBox(self)
            self.war.setGeometry(500, 500, 200, 100)
            self.war.setIcon(QMessageBox.Warning)
            self.war.setWindowTitle('Ошибка')
            self.war.setText(f'Вы не брали эту книгу')
            self.war.show()
            return
        date = result[0][0]

        days = int(date[0:2]) + int(date[3:5]) * 30 + int(date[6:]) * 365
        date1 = str(dt.date.today()).split('-')
        days1 = int(date1[2]) + int(date1[1]) * 30 + int(date1[0]) * 365 - 2000 * 365
        cost = (days1 - days) * 0.5
        cost -= 5
        if cost < 0:
            cost = 0
        con.close()

        con = sqlite3.connect("project_liceum_1")
        cur = con.cursor()
        result = cur.execute(f"""DELETE from books_movement Where id_book = 
        (SELECT id from list_books Where book = '{b}')""").fetchall()
        con.commit()

        con.close()
        self.tip = QMessageBox(self)
        self.tip.setGeometry(700, 300, 400, 800)
        self.tip.setIcon(QMessageBox.Warning)
        self.tip.setWindowTitle('Успех')
        self.tip.setText(f'{str(cost)} руб.')
        self.tip.show()

        date_normal = f'{date1[2]}-{date1[1]}-{date1[0]}'
        self.fine_1 = Fine_1(cost, date_normal)
        self.fine_1.show()
        self.hide()

    def closeEvent(self, event):
        ex.show()


class Fine_1(QWidget):
    '''
    Окно, отвечающее за штрафы
    '''

    def __init__(self, cost, date):
        super().__init__()
        uic.loadUi('data/Fine_1.ui', self)
        self.cost = cost
        self.today = date
        self.setGeometry(400, 100, 1134, 869)
        self.price.setText(f'{self.cost} руб')
        self.back_to_start_3.clicked.connect(self.Back_to_start_3)
        self.buy.clicked.connect(self.money)
        self.history.clicked.connect(self.hist)

        with open("style.txt", mode='r', encoding='utf-8') as f:
            style = f.readlines()
            style = ''.join(style)

        self.back_to_start_3.setStyleSheet(style)

        self.buy.setStyleSheet(style)

        self.history.setStyleSheet(style)

        self.setStyleSheet('background-color: "#9999CC"')

    def money(self):
        self.d.setText('Штраф погашен!')

        if self.cost != 0.0:
            with open("history.txt", mode='w', encoding='utf-8') as g:
                g.write(f'Штраф от {self.today} в размере {self.cost}')

    def Back_to_start_3(self):
        self.back = MyWidget()
        self.back.show()
        self.hide()

    def hist(self):
        self.histoty_fine = HistoryFine()
        self.histoty_fine.show()

    def closeEvent(self, event):
        ex.show()


class HistoryFine(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi('data/history.ui', self)
        self.setWindowTitle('История штрафов')
        with open('history.txt', mode='r', encoding='utf-8') as f:
            args = f.readlines()
            args = [i.rstrip('\n') for i in args]

        if len(args) > 0:
            for i in range(len(args)):
                if args[i] != '':
                    self.listWidget.addItem(args[i])


class Create(QWidget):
    '''
    Окно, отвечающее за создание читательского дневника
    '''

    def __init__(self):
        super().__init__()
        uic.loadUi('data/abs.ui', self)
        self.flag = True
        self.create_1.clicked.connect(self.create_text_f)
        self.back_to_start.clicked.connect(self.Back_to_start)

        with open("style.txt", mode='r', encoding='utf-8') as f:
            style = f.readlines()
            style = ''.join(style)

        self.create_1.setStyleSheet(style)

        self.back_to_start.setStyleSheet(style)

        self.setStyleSheet('background-color: "#9999CC"')

        self.create_text.setStyleSheet('background-color: white')

    def create_text_f(self):
        with open("style.txt", mode='r', encoding='utf-8') as f:
            style = f.readlines()
            style = ''.join(style)

        if self.flag:
            con = sqlite3.connect("project_liceum_1")
            cur = con.cursor()
            t = self.create_text.text()
            result = cur.execute(f"""INSERT INTO readers_list(reader) VALUES('{t}')""").fetchall()
            con.commit()
            con.close()
            self.flag = False
            self.create_ready.setText('Читательский дневник успешно создан')

    def Back_to_start(self):
        self.back = MyWidget()
        self.back.show()
        self.hide()

    def closeEvent(self, event):
        ex.show()


# Помощь
class SixthForm(QMainWindow):
    '''
    Окно, отвечающее за помощь пользователю
    '''

    def __init__(self):
        super().__init__()
        uic.loadUi('data/SixthForm.ui', self)
        self.back_sixthform.clicked.connect(self.Back_sixth)

        with open("style.txt", mode='r', encoding='utf-8') as f:
            style = f.readlines()
            style = ''.join(style)

        self.back_sixthform.setStyleSheet(style)

        self.setStyleSheet('background-color: "#9999CC"')

    def Back_sixth(self):
        self.back = MyWidget()
        self.back.show()
        self.hide()

    def closeEvent(self, event):
        ex.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyWidget()
    ex.show()
    sys.exit(app.exec_())
