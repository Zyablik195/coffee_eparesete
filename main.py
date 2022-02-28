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
        self.update_result_1()

    def row_column_clicked_1(self):
        row = self.tableWidget_1.currentRow()
        col = self.tableWidget_1.currentColumn()
        value = self.tableWidget_1.item(row, col)
        self.value_to_edit_1 = (row, col)
        # print(row)

    def add_1(self):
        print(222)
        d = Dialog_add(self)
        print(333)
        d.exec()
        print(555)

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
    def __init__(self, parent=None):
        super().__init__()
        self.parent = parent
        uic.loadUi("addEditCoffeeForm.ui", self)
        self.pushButton.clicked.connect(self.add)
        self.pushButton_2.clicked.connect(self.change)

    def add(self):
        a, b, c, d, e, f, g = self.lineEdit.text(), self.lineEdit_2.text(), self.lineEdit_3.text(), self.lineEdit_4.text(), self.lineEdit_5.text(), self.lineEdit_6.text(), self.lineEdit_7.text()
        try:
            self.parent.cur.execute(
                f"""INSERT INTO coffees(id, name, stage, type, description, cost, volume) VALUES({int(a)}, {"'" + b + "'"}, {"'" + c + "'"}, {"'" + d + "'"}, {"'" + e + "'"}, {"'" + f + "'"}, {"'" + g + "'"})""")
            self.parent.con.commit()
            self.parent.update_result_1()
            self.close()
        except:
            pass


    def change(self):
        a, b, c, d, e, f, g = self.lineEdit.text(), self.lineEdit_2.text(), self.lineEdit_3.text(), self.lineEdit_4.text(), self.lineEdit_5.text(), self.lineEdit_6.text(), self.lineEdit_7.text()
        try:
            print(4444)

            self.parent.cur.execute(
                f"""UPDATE coffees SET name = {"'" + b + "'"}, stage = {"'" + c + "'"}, type = {"'" + d + "'"}, description = {"'" + e + "'"}, cost = {"'" + f + "'"}, volume = {"'" + g + "'"} WHERE id = {int(a)}""")

            self.parent.con.commit()
            print(7777)
            self.parent.update_result_1()
            self.close()
        except:
            pass

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyWidget()
    ex.show()
    sys.exit(app.exec())