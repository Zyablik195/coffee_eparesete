import sqlite3
import sys

from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QInputDialog, QDialog
from PyQt5.QtWidgets import QMainWindow, QTableWidgetItem, QTextEdit, QPushButton, QGridLayout, QVBoxLayout, QLineEdit, \
    QLabel, QHBoxLayout, QComboBox


class MyWidget(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("main.ui", self)
        self.con = sqlite3.connect("coffee.sqlite")
        self.pushButton_1.clicked.connect(self.add_1)
        self.pushButton_2.clicked.connect(self.change_1)
        self.pushButton_3.clicked.connect(self.delete_1)
        self.lll_1 = -1
        self.lll_2 = -1
        self.value_to_edit = None
        self.dic = {'комедия': '1', 'драма': '2', 'мелодрама': '3', 'детектив': '4',
                    'документальный': '5', 'ужасы': '6', 'музыка': '7',
                    'фантастика': '8', 'анимация': '9', 'биография': '10',
                    'боевик': '11', 'приключения': '13', 'война': '15',
                    'семейный': '16', 'триллер': '17', 'фэнтези': '18',
                    'вестерн': '19', 'мистика': '20', 'короткометражный': '21',
                    'мюзикл': '22', 'исторический': '23', 'нуар': '24'}
        self.cur = self.con.cursor()
        self.tableWidget_1.cellClicked.connect(self.row_column_clicked_1)
        self.update_result_1()

    def row_column_clicked_1(self):
        row = self.tableWidget_1.currentRow()
        col = self.tableWidget_1.currentColumn()
        value = self.tableWidget_1.item(row, col)
        self.value_to_edit_1 = (row, col)
        # print(row)

    def add_1(self):
        d = Dialog_add(self)
        d.exec()
        namee, year, genre, duration = d.name_Param.text(), int(d.year_Param.text()), d.comb_Param.currentText(), int(
            d.dur_Param.text())
        self.lll_1 = self.lll_1 + 1
        self.cur.execute(
            f"""INSERT INTO films(id,title, year, genre, duration) VALUES({self.lll_1},{"'" + namee + "'"}, {year}, {self.dic[genre]}, {duration})""")
        self.con.commit()
        self.update_result_1()

    def change_1(self):
        if self.value_to_edit_1:
            d = Dialog_change(self)
            a, b, c = self.tableWidget_1.item(self.value_to_edit_1[0], 1).text(), self.tableWidget_1.item(
                self.value_to_edit_1[0], 2).text(), self.tableWidget_1.item(self.value_to_edit_1[0], 4).text()
            d.name_Param.setText(a)
            d.year_Param.setText(b)
            d.dur_Param.setText(c)
            ind = int(self.dic[self.tableWidget_1.item(self.value_to_edit_1[0], 3).text()]) - 1
            d.comb_Param.setCurrentIndex(ind)
            d.exec()

            # if d.name_Param.text() != '' and d.year_Param.text() != '' and d.dur_Param.text() != '' and d.dur_Param.text()[0] != '-' and d.dur_Param.text().isdigit() and d.year_Param.text().isdigit() and 0 < int(sd.year_Param.text()) < 2022:
            namee, year, genre, duration = d.name_Param.text(), int(
                d.year_Param.text()), d.comb_Param.currentText(), int(d.dur_Param.text())
            # self.lll = self.lll + 1
            self.cur.execute(
                f"""UPDATE films SET title = {"'" + namee + "'"}, duration = {duration}, year = {year}, genre = {self.dic[genre]} WHERE id = {self.tableWidget_1.item(self.value_to_edit_1[0], 0).text()}""")
            self.con.commit()
            self.update_result_1()
            self.value_to_edit_1 = None

    def delete_1(self):
        if self.value_to_edit_1:
            self.lll_1 = self.lll_1 - 1
            result = self.cur.execute((f"""DELETE from films
            where id = {self.tableWidget_1.item(self.value_to_edit_1[0], 0).text()}""")).fetchall()
            self.con.commit()
            self.update_result_1()
            self.value_to_edit_1 = None

    def update_result_1(self):
        # Получили результат запроса, который ввели в текстовое поле
        # cur.execute("SELECT * FROM films")
        result = self.cur.execute("""SELECT *
FROM
  coffees""").fetchall()

        # Заполнили размеры таблицы
        self.tableWidget_1.setRowCount(len(result))
        if self.lll_1 == -1:
            self.lll_1 = result[-1][0]
        # Если запись не нашлась, то не будем ничего делать
        self.tableWidget_1.setColumnCount(len(result[0]))
        self.tableWidget_1.setHorizontalHeaderLabels(
            ["ID", "название сорта", "степень обжарки", "молотый/в зернах", "описание вкуса", "цена", "объем упаковки"])
        # Заполнили таблицу полученными элементами
        for i, elem in enumerate(result):
            print(elem)
            elem1 = (elem[0], elem[1], elem[2], elem[3], elem[4], elem[5], elem[6])
            for j, val in enumerate(elem1):
                self.tableWidget_1.setItem(i, j, QTableWidgetItem(str(val)))


class Dialog_add(QDialog):
    def __init__(self, parent=None, volume=0):
        super(Dialog_add, self).__init__(parent)
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Введите")
        nameParam = QLabel("Название")
        self.name_Param = QLineEdit()
        yearParam = QLabel("Год")
        self.year_Param = QLineEdit()
        combParam = QLabel("Жанр")
        self.comb_Param = QComboBox()
        self.comb_Param.addItems(tuple(
            'комедия драма мелодрама детектив документальный ужасы музыка фантастика анимация биография боевик приключения война семейный триллер фэнтези вестерн мистика короткометражный мюзикл исторический нуар'.split()))
        durParam = QLabel("Длительность")
        self.dur_Param = QLineEdit()
        self.check_Param = QLabel("")
        saveButton = QPushButton("ДОБАВИТЬ")
        hbox1 = QHBoxLayout()
        hbox1.addWidget(nameParam)
        hbox1.addWidget(self.name_Param)

        hbox2 = QHBoxLayout()
        hbox2.addWidget(yearParam)
        hbox2.addWidget(self.year_Param)

        hbox3 = QHBoxLayout()
        hbox3.addWidget(combParam)
        hbox3.addWidget(self.comb_Param)

        hbox4 = QHBoxLayout()
        hbox4.addWidget(durParam)
        hbox4.addWidget(self.dur_Param)

        hbox5 = QHBoxLayout()
        hbox5.addWidget(self.check_Param)

        hbox6 = QHBoxLayout()
        hbox6.addWidget(saveButton)
        mainLayout = QVBoxLayout()
        mainLayout.setSpacing(6)
        mainLayout.addLayout(hbox1)
        mainLayout.addStretch(1)
        mainLayout.addLayout(hbox2)
        mainLayout.addStretch(1)
        mainLayout.addLayout(hbox3)
        mainLayout.addStretch(1)
        mainLayout.addLayout(hbox4)
        mainLayout.addStretch(1)
        mainLayout.addLayout(hbox5)
        mainLayout.addStretch(1)
        mainLayout.addLayout(hbox6)
        self.setLayout(mainLayout)

        saveButton.clicked.connect(self.to_save)

    def to_save(self):
        if self.name_Param.text() != '' and self.year_Param.text() != '' and self.dur_Param.text() != '' and \
                self.dur_Param.text()[
                    0] != '-' and self.dur_Param.text().isdigit() and self.year_Param.text().isdigit() and 0 < int(
                self.year_Param.text()) < 2022:
            self.close()
        else:
            self.check_Param.setText('Неверные данные')


class Dialog_change(QDialog):
    def __init__(self, parent=None, volume=0):
        super(Dialog_change, self).__init__(parent)
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Введите")
        nameParam = QLabel("Название")
        self.name_Param = QLineEdit()
        yearParam = QLabel("Год")
        self.year_Param = QLineEdit()
        combParam = QLabel("Жанр")
        self.comb_Param = QComboBox()
        self.comb_Param.addItems(tuple(
            'комедия драма мелодрама детектив документальный ужасы музыка фантастика анимация биография боевик приключения война семейный триллер фэнтези вестерн мистика короткометражный мюзикл исторический нуар'.split()))
        durParam = QLabel("Длительность")
        self.dur_Param = QLineEdit()
        self.check_Param = QLabel("")
        saveButton = QPushButton("ДОБАВИТЬ")
        hbox1 = QHBoxLayout()
        hbox1.addWidget(nameParam)
        hbox1.addWidget(self.name_Param)

        hbox2 = QHBoxLayout()
        hbox2.addWidget(yearParam)
        hbox2.addWidget(self.year_Param)

        hbox3 = QHBoxLayout()
        hbox3.addWidget(combParam)
        hbox3.addWidget(self.comb_Param)

        hbox4 = QHBoxLayout()
        hbox4.addWidget(durParam)
        hbox4.addWidget(self.dur_Param)

        hbox5 = QHBoxLayout()
        hbox5.addWidget(self.check_Param)

        hbox6 = QHBoxLayout()
        hbox6.addWidget(saveButton)
        mainLayout = QVBoxLayout()
        mainLayout.setSpacing(6)
        mainLayout.addLayout(hbox1)
        mainLayout.addStretch(1)
        mainLayout.addLayout(hbox2)
        mainLayout.addStretch(1)
        mainLayout.addLayout(hbox3)
        mainLayout.addStretch(1)
        mainLayout.addLayout(hbox4)
        mainLayout.addStretch(1)
        mainLayout.addLayout(hbox5)
        mainLayout.addStretch(1)
        mainLayout.addLayout(hbox6)
        self.setLayout(mainLayout)

        saveButton.clicked.connect(self.to_save)

    def to_save(self):
        if self.name_Param.text() != '' and self.year_Param.text() != '' and self.dur_Param.text() != '' and \
                self.dur_Param.text()[
                    0] != '-' and self.dur_Param.text().isdigit() and self.year_Param.text().isdigit() and 0 < int(
                self.year_Param.text()) < 2022:
            self.close()
        else:
            self.check_Param.setText('Неверные данные')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyWidget()
    ex.show()
    sys.exit(app.exec())