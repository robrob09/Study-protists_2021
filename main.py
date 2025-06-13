# -*- coding: utf-8 -*-


import sys
import csv
import sqlite3
from copy import deepcopy
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication, QDialog, QMainWindow
from PyQt5.QtWidgets import QApplication, QInputDialog, QFileDialog, QMainWindow
from PIL import Image
from PyQt5.QtGui import QPixmap


class Ui_ObjectInfo(object):
    def setupUi(self, ObjectInfo):
        ObjectInfo.setObjectName("ObjectInfo")
        ObjectInfo.resize(814, 438)
        self.centralwidget = QtWidgets.QWidget(ObjectInfo)
        self.centralwidget.setObjectName("centralwidget")
        self.name = QtWidgets.QLabel(self.centralwidget)
        self.name.setGeometry(QtCore.QRect(30, 10, 191, 31))
        self.name.setStyleSheet("font: 14pt \"MS Shell Dlg 2\";")
        self.name.setText("")
        self.name.setObjectName("name")
        self.objectInfo = QtWidgets.QPlainTextEdit(self.centralwidget)
        self.objectInfo.setGeometry(QtCore.QRect(30, 60, 421, 331))
        self.objectInfo.setStyleSheet("font: 12pt \"MS Shell Dlg 2\";")
        self.objectInfo.setObjectName("objectInfo")
        self.pictureLabel = QtWidgets.QLabel(self.centralwidget)
        self.pictureLabel.setGeometry(QtCore.QRect(480, 60, 321, 331))
        self.pictureLabel.setText("")
        self.pictureLabel.setObjectName("pictureLabel")
        self.picture = QtWidgets.QLabel(self.centralwidget)
        self.picture.setGeometry(QtCore.QRect(470, 12, 101, 31))
        self.picture.setStyleSheet("font: 14pt \"MS Shell Dlg 2\";")
        self.picture.setObjectName("picture")
        ObjectInfo.setCentralWidget(self.centralwidget)

        self.retranslateUi(ObjectInfo)
        QtCore.QMetaObject.connectSlotsByName(ObjectInfo)

    def retranslateUi(self, ObjectInfo):
        _translate = QtCore.QCoreApplication.translate
        ObjectInfo.setWindowTitle(_translate("ObjectInfo", "MainWindow"))
        self.objectInfo.setPlainText(_translate("ObjectInfo", "Свойства:\n"
                                                ""))
        self.picture.setText(_translate("ObjectInfo", "Картинка:"))


class ObjectInfo(QMainWindow, Ui_ObjectInfo):
    def __init__(self, name='', info='', pictureName='', delete=False, isPicture=False):
        super().__init__()
        super().setupUi(self)

        if delete:
            self.setWindowTitle('Описание термина')
        else:
            self.setWindowTitle('Свойства простейшего')
        self.name.setText(name.split()[0])
        self.name.resize(self.name.sizeHint())
        self.objectInfo.setReadOnly(True)
        pixmapName = 'DateBaseImage\\' + pictureName
        if info == 'Свойства данного организма не указаны в базе данных\n':
            self.objectInfo.setPlainText(info)
            self.objectInfo.resize(421, 68)
        elif delete:
            self.objectInfo.setPlainText(info)
        else:
            self.objectInfo.setPlainText(
                'Описание:\n' + info)
        if isPicture:
            image = Image.open(pixmapName)
            image = image.resize((321, 331))
            image.save(pixmapName)
            self.pixmap = QPixmap(pixmapName)
            self.pictureLabel.setPixmap(self.pixmap)
        else:
            self.pictureLabel.setText("Отсутствует")
            self.pictureLabel.setStyleSheet("font-size: 56px")


class Ui_FoundObjects(object):
    def setupUi(self, FoundObjects):
        FoundObjects.setObjectName("FoundObjects")
        FoundObjects.resize(580, 418)
        self.centralwidget = QtWidgets.QWidget(FoundObjects)
        self.centralwidget.setObjectName("centralwidget")
        self.foundNameObjects = QtWidgets.QListWidget(self.centralwidget)
        self.foundNameObjects.setGeometry(QtCore.QRect(50, 60, 481, 301))
        self.foundNameObjects.setObjectName("foundNameObjects")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(60, 10, 211, 31))
        self.label.setObjectName("label")
        self.objectsNotFound = QtWidgets.QLabel(self.centralwidget)
        self.objectsNotFound.setGeometry(QtCore.QRect(10, 10, 551, 51))
        self.objectsNotFound.setStyleSheet(
            "font: 75 30pt \"Times New Roman\";")
        self.objectsNotFound.setObjectName("objectsNotFound")
        FoundObjects.setCentralWidget(self.centralwidget)

        self.retranslateUi(FoundObjects)
        QtCore.QMetaObject.connectSlotsByName(FoundObjects)

    def retranslateUi(self, FoundObjects):
        _translate = QtCore.QCoreApplication.translate
        FoundObjects.setWindowTitle(_translate("FoundObjects", "MainWindow"))
        self.label.setText(_translate(
            "FoundObjects", "<html><head/><body><p><span style=\" font-size:16pt;\">Найденные объекты:</span></p></body></html>"))
        self.objectsNotFound.setText(_translate(
            "FoundObjects", "<html><head/><body><p><span style=\" font-size:28pt;\">Запрошенный объект не найден</span></p></body></html>"))


class FoundObjects(QMainWindow, Ui_FoundObjects):
    def __init__(self, array=[]):
        super().__init__()
        super().setupUi(self)
        self.setWindowTitle("Найденные объекты")
        self.result = deepcopy(array)
        if self.result:
            self.objectsNotFound.setVisible(False)
            for name in self.result:
                self.foundNameObjects.addItem(name)
            self.foundNameObjects.itemClicked.connect(self.itemChecked)
        else:
            self.label.setVisible(False)
            self.foundNameObjects.setVisible(False)
            self.resize(520, 80)

    def itemChecked(self):
        name = self.foundNameObjects.currentItem().text()
        information = self.getResult(name)
        info = ''
        for string in sorted(information, reverse=True):
            if information[string] and string != 'название файла с картинкой':
                info += string + ': ' + information[string] + '\n'
        if not info:
            info = 'Свойства данного организма не указаны в базе данных\n'
        if information['название файла с картинкой'] is None:
            self.objectInformation = ObjectInfo(name=name, info=info)
        else:
            self.objectInformation = ObjectInfo(
                name=name, info=info, pictureName=information['название файла с картинкой'], isPicture=True)
        self.objectInformation.show()
        self.close()

    def getResult(self, name):
        connection = sqlite3.connect("DataBase.db")
        c = connection.cursor()
        answer = {"жгутики": '', "кристы": '', "пластиды": '', "тип питания": '',
                  "другие свойства": '', 'название файла с картинкой': ''}
        answer["жгутики"] = c.execute("""
        SELECT retranslation FROM Flagellums
            WHERE letter = (
        SELECT Flagellum FROM MainTable
            WHERE Name = \'""" + name + "\'" + ')').fetchone()
        answer["кристы"] = c.execute("""
        SELECT retranslation FROM Cristas
            WHERE letter = (
        SELECT Crista FROM MainTable
            WHERE Name = \'""" + name + "\'" + ')').fetchone()
        answer["пластиды"] = c.execute("""
        SELECT retranslation FROM Plastid
            WHERE letter = (
        SELECT Plastid FROM MainTable
            WHERE Name = \'""" + name + "\'" + ')').fetchone()
        answer["тип питания"] = c.execute("""
        SELECT retranslation FROM Food
            WHERE letter = (
        SELECT Food FROM MainTable
            WHERE Name = \'""" + name + "\'" + ')').fetchone()
        answer["другие свойства"] = c.execute("""
        SELECT Property FROM MainTable
            WHERE Name = \'""" + name + "\'").fetchone()
        answer["название файла с картинкой"] = c.execute("""
        SELECT Image FROM MainTable
            WHERE Name = \'""" + name + "\'").fetchone()
        rank_name = str(c.execute(
            """SELECT Rank FROM MainTable WHERE Name = \'""" + name + "\'").fetchone()[0])
        if len(rank_name) > 1:
            answer['предок'] = c.execute("""
            SELECT Name FROM MainTable WHERE Rank = \'""" + rank_name[:rank_name.rfind('.')] + "\'").fetchone()[0]
        else:
            answer['предок'] = None
        for prop in answer:
            if isinstance(answer[prop], tuple):
                answer[prop] = answer[prop][0]
        connection.close()
        return answer


class Ui_FoundTerms(object):
    def setupUi(self, FoundTerms):
        FoundTerms.setObjectName("FoundTerms")
        FoundTerms.resize(580, 418)
        self.centralwidget = QtWidgets.QWidget(FoundTerms)
        self.centralwidget.setObjectName("centralwidget")
        self.foundTermObjects = QtWidgets.QListWidget(self.centralwidget)
        self.foundTermObjects.setGeometry(QtCore.QRect(50, 60, 481, 301))
        self.foundTermObjects.setObjectName("foundTermObjects")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(60, 10, 211, 31))
        self.label.setObjectName("label")
        self.objectsNotFound = QtWidgets.QLabel(self.centralwidget)
        self.objectsNotFound.setGeometry(QtCore.QRect(10, 10, 551, 51))
        self.objectsNotFound.setStyleSheet(
            "font: 75 30pt \"Times New Roman\";")
        self.objectsNotFound.setObjectName("objectsNotFound")
        FoundTerms.setCentralWidget(self.centralwidget)

        self.retranslateUi(FoundTerms)
        QtCore.QMetaObject.connectSlotsByName(FoundTerms)

    def retranslateUi(self, FoundTerms):
        _translate = QtCore.QCoreApplication.translate
        FoundTerms.setWindowTitle(_translate("FoundTerms", "MainWindow"))
        self.label.setText(_translate(
            "FoundTerms", "<html><head/><body><p><span style=\" font-size:16pt;\">Найденные объекты:</span></p></body></html>"))
        self.objectsNotFound.setText(_translate(
            "FoundTerms", "<html><head/><body><p><span style=\" font-size:28pt;\">Запрошенный термин не найден</span></p></body></html>"))


class FoundTermObjects(QMainWindow, Ui_FoundTerms):
    def __init__(self, array=[]):
        super().__init__()
        super().setupUi(self)
        self.setWindowTitle("Найденные объекты")
        self.result = deepcopy(array)
        if self.result:
            self.objectsNotFound.setVisible(False)
            for term in self.result:
                self.foundTermObjects.addItem(term)
            self.foundTermObjects.itemClicked.connect(self.itemChecked)
        else:
            self.label.setVisible(False)
            self.foundTermObjects.setVisible(False)
            self.resize(520, 80)

    def itemChecked(self):
        term = self.foundTermObjects.currentItem().text()
        info, pictureTerm = self.getResult(term)
        if pictureTerm is None:
            self.termInformation = ObjectInfo(
                name=term, delete=True, info=info)
        else:
            self.termInformation = ObjectInfo(
                name=term, info=info, pictureName=pictureTerm, delete=True, isPicture=True)
        self.termInformation.show()
        self.close()

    def getResult(self, term):
        connection = sqlite3.connect("DataBase.db")
        c = connection.cursor()
        result = c.execute("""
        SELECT retranslation, Image FROM Termins
            WHERE Termin = \'""" + term + "\'").fetchone()
        connection.close()
        return result


class Ui_SearchFeature(object):
    def setupUi(self, SearchFeature):
        SearchFeature.setObjectName("SearchFeature")
        SearchFeature.resize(733, 378)
        self.centralwidget = QtWidgets.QWidget(SearchFeature)
        self.centralwidget.setObjectName("centralwidget")
        self.flagellumsCheck = QtWidgets.QCheckBox(self.centralwidget)
        self.flagellumsCheck.setGeometry(QtCore.QRect(10, 10, 101, 31))
        self.flagellumsCheck.setStyleSheet("font: 14pt \"MS Shell Dlg 2\";")
        self.flagellumsCheck.setObjectName("flagellumsCheck")
        self.cristasCheck = QtWidgets.QCheckBox(self.centralwidget)
        self.cristasCheck.setGeometry(QtCore.QRect(10, 70, 101, 31))
        self.cristasCheck.setStyleSheet("font: 14pt \"MS Shell Dlg 2\";")
        self.cristasCheck.setObjectName("cristasCheck")
        self.plastidCheck = QtWidgets.QCheckBox(self.centralwidget)
        self.plastidCheck.setGeometry(QtCore.QRect(10, 210, 111, 31))
        self.plastidCheck.setStyleSheet("font: 14pt \"MS Shell Dlg 2\";")
        self.plastidCheck.setObjectName("plastidCheck")
        self.foodCheck = QtWidgets.QCheckBox(self.centralwidget)
        self.foodCheck.setGeometry(QtCore.QRect(10, 270, 131, 31))
        self.foodCheck.setStyleSheet("font: 14pt \"MS Shell Dlg 2\";")
        self.foodCheck.setObjectName("foodCheck")
        self.Flagellums = QtWidgets.QComboBox(self.centralwidget)
        self.Flagellums.setGeometry(QtCore.QRect(170, 11, 531, 31))
        self.Flagellums.setStyleSheet("font: 12pt \"MS Shell Dlg 2\";")
        self.Flagellums.setObjectName("Flagellums")
        self.Plastid = QtWidgets.QComboBox(self.centralwidget)
        self.Plastid.setGeometry(QtCore.QRect(170, 210, 531, 31))
        self.Plastid.setStyleSheet("font: 12pt \"MS Shell Dlg 2\";")
        self.Plastid.setObjectName("Plastid")
        self.Food = QtWidgets.QComboBox(self.centralwidget)
        self.Food.setGeometry(QtCore.QRect(170, 270, 531, 31))
        self.Food.setStyleSheet("font: 12pt \"MS Shell Dlg 2\";")
        self.Food.setObjectName("Food")
        self.no = QtWidgets.QRadioButton(self.centralwidget)
        self.no.setGeometry(QtCore.QRect(170, 70, 271, 31))
        self.no.setStyleSheet("font: 14pt \"MS Shell Dlg 2\";")
        self.no.setObjectName("no")
        self.group = QtWidgets.QButtonGroup(SearchFeature)
        self.group.setObjectName("group")
        self.group.addButton(self.no)
        self.lamellar = QtWidgets.QRadioButton(self.centralwidget)
        self.lamellar.setGeometry(QtCore.QRect(450, 70, 251, 31))
        self.lamellar.setStyleSheet("font: 14pt \"MS Shell Dlg 2\";")
        self.lamellar.setObjectName("lamellar")
        self.group.addButton(self.lamellar)
        self.discoid = QtWidgets.QRadioButton(self.centralwidget)
        self.discoid.setGeometry(QtCore.QRect(450, 110, 251, 31))
        self.discoid.setStyleSheet("font: 14pt \"MS Shell Dlg 2\";")
        self.discoid.setObjectName("discoid")
        self.group.addButton(self.discoid)
        self.tubular = QtWidgets.QRadioButton(self.centralwidget)
        self.tubular.setGeometry(QtCore.QRect(170, 110, 271, 31))
        self.tubular.setStyleSheet("font: 14pt \"MS Shell Dlg 2\";")
        self.tubular.setObjectName("tubular")
        self.group.addButton(self.tubular)
        self.reduced = QtWidgets.QRadioButton(self.centralwidget)
        self.reduced.setGeometry(QtCore.QRect(170, 150, 531, 31))
        self.reduced.setStyleSheet("font: 14pt \"MS Shell Dlg 2\";")
        self.reduced.setObjectName("reduced")
        self.group.addButton(self.reduced)
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(10, 320, 691, 41))
        self.pushButton.setStyleSheet("font: 14pt \"MS Shell Dlg 2\";")
        self.pushButton.setObjectName("pushButton")
        SearchFeature.setCentralWidget(self.centralwidget)

        self.retranslateUi(SearchFeature)
        QtCore.QMetaObject.connectSlotsByName(SearchFeature)

    def retranslateUi(self, SearchFeature):
        _translate = QtCore.QCoreApplication.translate
        SearchFeature.setWindowTitle(
            _translate("SearchFeature", "MainWindow"))
        self.flagellumsCheck.setText(_translate("SearchFeature", "Жгутики"))
        self.cristasCheck.setText(_translate("SearchFeature", "Кристы"))
        self.plastidCheck.setText(_translate("SearchFeature", "Пластиды"))
        self.foodCheck.setText(_translate("SearchFeature", "Тип питания"))
        self.no.setText(_translate("SearchFeature",
                                   "Отсутствуют митохондрии"))
        self.lamellar.setText(_translate("SearchFeature", "Пластинчатые"))
        self.discoid.setText(_translate("SearchFeature", "Дисковидные"))
        self.tubular.setText(_translate("SearchFeature", "Трубчатые"))
        self.reduced.setText(_translate(
            "SearchFeature", "Гидрогеносомы (редукция митохондрий)"))
        self.pushButton.setText(_translate("SearchFeature", "Далее"))


class SearchFeature(QMainWindow, Ui_SearchFeature):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.setWindowTitle("Поиск по признакам")
        self.reset()
        self.Flagellums.setVisible(False)
        self.no.setVisible(False)
        self.lamellar.setVisible(False)
        self.tubular.setVisible(False)
        self.discoid.setVisible(False)
        self.reduced.setVisible(False)
        self.Plastid.setVisible(False)
        self.Food.setVisible(False)
        self.flagellumsCheck.stateChanged.connect(self.changeFlagellums)
        self.cristasCheck.stateChanged.connect(self.changeCristas)
        self.plastidCheck.stateChanged.connect(self.changePlastid)
        self.foodCheck.stateChanged.connect(self.changeFood)
        self.pushButton.setText("OK")
        self.pushButton.clicked.connect(self.findFeature)

    def findFeature(self):
        connection = sqlite3.connect("DataBase.db")
        c = connection.cursor()
        ask = []
        if self.flagellumsCheck.isChecked() and self.Flagellums.currentText() != "не выбрано":
            letter = c.execute("SELECT letter FROM Flagellums WHERE retranslation = \'" +
                               self.Flagellums.currentText() + "\'").fetchone()[0]
            ask.append(" Flagellum = \'" + letter + "\' ")
        if self.group.checkedButton() is not None:
            letter = c.execute("SELECT letter FROM Cristas WHERE retranslation LIKE \'%" +
                               self.group.checkedButton().text() + "%\' OR retranslation LIKE \'%" +
                               self.group.checkedButton().text().lower() + "%\' OR retranslation LIKE \'%" +
                               self.group.checkedButton().text().upper() + "%\' OR retranslation LIKE \'%" +
                               self.group.checkedButton().text().capitalize() + "%\'").fetchone()[0]
            ask.append(" Crista = \'" + letter + "\' ")
        if self.plastidCheck.isChecked() and self.Plastid.currentText() != "не выбрано":
            letter = c.execute("SELECT letter FROM Plastid WHERE retranslation = \'" +
                               self.Plastid.currentText() + "\'").fetchone()[0]
            ask.append(" Plastid = \'" + letter + "\' ")
        if self.foodCheck.isChecked() and self.Food.currentText() != "не выбрано":
            letter = c.execute("SELECT letter FROM Food WHERE retranslation = \'" +
                               self.Food.currentText() + "\'").fetchone()[0]
            ask.append(" Food = \'" + letter + "\' ")
        if ask:
            request = "SELECT Name FROM MainTable\nWHERE" + 'AND'.join(ask)
        else:
            request = "SELECT Name FROM MainTable"
        result = c.execute(request).fetchall()
        for i in range(len(result)):
            result[i] = result[i][0]
        self.foundObjects = FoundObjects(result)
        self.foundObjects.show()
        self.close()
        connection.close()

    def changeFlagellums(self):
        self.Flagellums.setVisible(self.flagellumsCheck.isChecked())
        connection = sqlite3.connect("DataBase.db")
        c = connection.cursor()
        result = c.execute(
            """SELECT retranslation FROM Flagellums""").fetchall()
        for i in range(len(result)):
            result[i] = result[i][0]
        result.insert(0, "не выбрано")
        self.Flagellums.clear()
        self.Flagellums.addItems(deepcopy(result))
        self.Flagellums.setCurrentIndex(0)
        connection.close()

    def changeCristas(self):
        self.no.setVisible(self.cristasCheck.isChecked())
        self.lamellar.setVisible(self.cristasCheck.isChecked())
        self.tubular.setVisible(self.cristasCheck.isChecked())
        self.discoid.setVisible(self.cristasCheck.isChecked())
        self.reduced.setVisible(self.cristasCheck.isChecked())
        self.group.setExclusive(False)
        self.no.setChecked(False)
        self.lamellar.setChecked(False)
        self.tubular.setChecked(False)
        self.discoid.setChecked(False)
        self.reduced.setChecked(False)
        self.group.setExclusive(True)

    def changePlastid(self):
        self.Plastid.setVisible(self.plastidCheck.isChecked())
        connection = sqlite3.connect("DataBase.db")
        c = connection.cursor()
        result = c.execute(
            """SELECT retranslation FROM Plastid""").fetchall()
        for i in range(len(result)):
            result[i] = result[i][0]
        result.insert(0, "не выбрано")
        self.Plastid.clear()
        self.Plastid.addItems(deepcopy(result))
        self.Plastid.setCurrentIndex(0)
        connection.close()

    def changeFood(self):
        self.Food.setVisible(self.foodCheck.isChecked())
        connection = sqlite3.connect("DataBase.db")
        c = connection.cursor()
        result = c.execute(
            """SELECT retranslation FROM Food""").fetchall()
        for i in range(len(result)):
            result[i] = result[i][0]
        result.insert(0, "не выбрано")
        self.Food.clear()
        self.Food.addItems(deepcopy(result))
        self.Food.setCurrentIndex(0)
        connection.close()

    def reset(self):
        connection = sqlite3.connect("DataBase.db")
        c = connection.cursor()

        result = c.execute(
            """SELECT retranslation FROM Flagellums""").fetchall()
        for i in range(len(result)):
            result[i] = result[i][0]
        result.insert(0, "не выбрано")
        self.Flagellums.clear()
        self.Flagellums.addItems(deepcopy(result))
        self.Flagellums.setCurrentIndex(0)

        self.group.setExclusive(False)
        self.no.setChecked(False)
        self.lamellar.setChecked(False)
        self.tubular.setChecked(False)
        self.discoid.setChecked(False)
        self.reduced.setChecked(False)
        self.group.setExclusive(True)

        result = c.execute(
            """SELECT retranslation FROM Plastid""").fetchall()
        for i in range(len(result)):
            result[i] = result[i][0]
        result.insert(0, "не выбрано")
        self.Plastid.clear()
        self.Plastid.addItems(deepcopy(result))
        self.Plastid.setCurrentIndex(0)

        result = c.execute(
            """SELECT retranslation FROM Food""").fetchall()
        for i in range(len(result)):
            result[i] = result[i][0]
        result.insert(0, "не выбрано")
        self.Food.clear()
        self.Food.addItems(deepcopy(result))
        self.Food.setCurrentIndex(0)

        connection.close()


class Ui_HelpWindow(object):
    def setupUi(self, HelpWindow):
        HelpWindow.setObjectName("HelpWindow")
        HelpWindow.resize(666, 491)
        self.helpInfo = QtWidgets.QPlainTextEdit(HelpWindow)
        self.helpInfo.setGeometry(QtCore.QRect(20, 50, 621, 371))
        self.helpInfo.setStyleSheet("font: 12pt \"MS Shell Dlg 2\";")
        self.helpInfo.setObjectName("helpInfo")
        self.helpLabel = QtWidgets.QLabel(HelpWindow)
        self.helpLabel.setGeometry(QtCore.QRect(230, 10, 131, 31))
        self.helpLabel.setObjectName("helpLabel")
        self.pushButton = QtWidgets.QPushButton(HelpWindow)
        self.pushButton.setGeometry(QtCore.QRect(200, 440, 231, 41))
        self.pushButton.setStyleSheet("font: 12pt \"MS Shell Dlg 2\";")
        self.pushButton.setObjectName("pushButton")

        self.retranslateUi(HelpWindow)
        QtCore.QMetaObject.connectSlotsByName(HelpWindow)

    def retranslateUi(self, HelpWindow):
        _translate = QtCore.QCoreApplication.translate
        HelpWindow.setWindowTitle(_translate("HelpWindow", "Dialog"))
        self.helpLabel.setText(_translate(
            "HelpWindow", "<html><head/><body><p><span style=\" font-size:16pt;\">Окно помощи</span></p></body></html>"))
        self.pushButton.setText(_translate("HelpWindow", "Закрыть"))


class HelpWindowWork(QMainWindow, Ui_HelpWindow):
    def __init__(self):
        super().__init__()
        super().setupUi(self)

        self.setWindowTitle("Помощь")
        self.helpInfo.setReadOnly(True)
        self.helpInfo.setPlainText("""    1. Поиск одноклеточного организма по названию	
Нажмите кнопу «Найти по названию». В открывшемся окне введите название одноклеточного организма (или группы организмов). Нажмите кнопку «OK». В результате поиска будет выведен список организмов, в названии которых встречается искомое слово. При нажатии на каждый из найденных объектов откроется его описание. В случае, если в Базе данных программы не встречается заданное название, будет выведена надпись: «Не найдено».
    2. Поиск одноклеточного организма по его признакам и свойствам
Нажмите на кнопку «Найти по признакам». В открывшемся окне выберите соответствующие признаки и свойства организма. Если вы затрудняетесь в выборе какого-либо признака (не знаете точно, обладает ли организм данным свойством), то пропустите выбор этого признака. Нажмите кнопку «OK». В результате поиска будет выведен список Простейших, обладающих указанными признаками и свойствами. При нажатии на каждый из найденных объектов откроется его описание. 
    3. Поиск определений научных терминов, используемых при изучении одноклеточных организмов.
Нажмите кнопку «Найти определение термина». В открывшемся окне введите термин, который требуется найти. Нажмите кнопку «OK». В результате поиска будет выведено определение термина (в случае, если оно имеется в Базе данных программы).""")
        self.pushButton.clicked.connect(self.closeHelp)

    def closeHelp(self):
        self.close()


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(618, 357)
        self.buttonHelp = QtWidgets.QPushButton(MainWindow)
        self.buttonHelp.setGeometry(QtCore.QRect(200, 270, 221, 41))
        self.buttonHelp.setStyleSheet("font: 12pt \"MS Shell Dlg 2\";")
        self.buttonHelp.setObjectName("buttonHelp")
        self.buttonName = QtWidgets.QPushButton(MainWindow)
        self.buttonName.setGeometry(QtCore.QRect(100, 20, 411, 51))
        self.buttonName.setMinimumSize(QtCore.QSize(409, 0))
        self.buttonName.setStyleSheet("font: 12pt \"MS Shell Dlg 2\";")
        self.buttonName.setObjectName("buttonName")
        self.buttonFeature = QtWidgets.QPushButton(MainWindow)
        self.buttonFeature.setGeometry(QtCore.QRect(100, 74, 411, 51))
        self.buttonFeature.setStyleSheet("font: 12pt \"MS Shell Dlg 2\";")
        self.buttonFeature.setObjectName("buttonFeature")
        self.buttonTerm = QtWidgets.QPushButton(MainWindow)
        self.buttonTerm.setGeometry(QtCore.QRect(100, 128, 411, 51))
        self.buttonTerm.setStyleSheet("font: 12pt \"MS Shell Dlg 2\";")
        self.buttonTerm.setObjectName("buttonTerm")
        self.buttonChange = QtWidgets.QPushButton(MainWindow)
        self.buttonChange.setGeometry(QtCore.QRect(100, 182, 411, 51))
        self.buttonChange.setStyleSheet("font: 12pt \"MS Shell Dlg 2\";")
        self.buttonChange.setObjectName("buttonChange")

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Dialog"))
        self.buttonHelp.setText(_translate("MainWindow", "Помощь"))
        self.buttonName.setText(_translate(
            "MainWindow", "Найти простейшее по названию"))
        self.buttonFeature.setText(_translate(
            "MainWindow", "Найти простейшее по признакам"))
        self.buttonTerm.setText(_translate(
            "MainWindow", "Найти определение термина"))
        self.buttonChange.setText(_translate(
            "MainWindow", "Изменить базу данных"))


class MainWindowWork(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle("Поиск простейших")
        self.buttonName.clicked.connect(self.beginNameSearch)
        self.buttonFeature.clicked.connect(self.beginFeatureSearch)
        self.buttonTerm.clicked.connect(self.beginTermSearch)
        self.buttonHelp.clicked.connect(self.openHelp)
        self.buttonChange.clicked.connect(self.beginChange)

    def openHelp(self):
        self.helpWindow = HelpWindowWork()
        self.helpWindow.show()

    def beginNameSearch(self):
        name, ok_pressed = QInputDialog.getText(
            self, "Введите название", "Как называется запрошенное простейшее или группа?")
        if ok_pressed:
            self.foundObjects = FoundObjects(self.findName(name))
            self.foundObjects.show()

    def findName(self, name):
        connection = sqlite3.connect("DataBase.db")
        c = connection.cursor()
        result = c.execute("""
        SELECT Name FROM MainTable
            WHERE Name LIKE \'%""" + name + "%\' OR Name LIKE \'%" +
                           name.lower() + "%\' OR Name LIKE \'%" +
                           name.upper() + "%\' OR Name LIKE \'%" +
                           name.capitalize() + "%\'").fetchall()
        answer = []
        for found_name in result:
            answer.append(found_name[0])
        connection.close()
        return answer

    def beginTermSearch(self):
        term, ok_pressed = QInputDialog.getText(
            self, "Введите название", "Как называется запрошенный термин?")
        if ok_pressed:
            self.foundObjects = FoundTermObjects(self.findTerm(term))
            self.foundObjects.show()

    def findTerm(self, term):
        connection = sqlite3.connect("DataBase.db")
        c = connection.cursor()
        result = c.execute("""
        SELECT Termin FROM Termins
            WHERE Termin LIKE \'%""" + term + "%\' OR Termin LIKE \'%" +
                           term.lower() + "%\' OR Termin LIKE \'%" +
                           term.upper() + "%\' OR Termin LIKE \'%" +
                           term.capitalize() + "%\'").fetchall()
        answer = []
        for found_term in result:
            answer.append(found_term[0])
        connection.close()
        return answer

    def beginFeatureSearch(self):
        self.searchFeature = SearchFeature()
        self.searchFeature.show()

    def beginChange(self):
        fname = QFileDialog.getOpenFileName(
            self, 'Выбрать файл с командами', '', '(*.txt);;(*.csv)')[0]
        if fname == '':
            return
        file = open(fname, encoding='utf-8')
        reader = csv.DictReader(file, delimiter=',', quotechar='\'')
        connection = sqlite3.connect("DataBase.db")
        c = connection.cursor()
        for it in reader:
            _item = deepcopy(it)
            item = {}
            for s in _item:
                item[s.strip()] = _item[s].strip()
            if item['table'] == 'MainTable':
                if 'null' in [item['request'], item['id'], item['Name'], item['Rank']]:
                    continue
                if item['request'] == 'ADD':
                    request = []
                    for s in ["Flagellum", "Crista", "Plastid", "Food", "Property", "Image"]:
                        if item[s] == 'null':
                            request.append('null')
                        else:
                            request.append('\'' + item[s] + '\'')
                    info = f"INSERT INTO MainTable VALUES ({item['id']}, '{item['Name']}', '{item['Rank']}', {', '.join(request)})"
                    c.execute(info)
                elif item['request'] == 'CHANGE':
                    request = []
                    for s in ["Flagellum", "Crista", "Plastid", "Food", "Property", "Image"]:
                        if item[s] == 'null':
                            request.append(f"{s} = null")
                        else:
                            request.append(f"{s} = \'{item[s]}\'")
                    info = f"UPDATE MainTable\nSET {', '.join(request)}\nWHERE id = {item['id']}"
                    c.execute(info)
                elif item['request'] == 'DELETE':
                    info = f"DELETE FROM MainTable\nWHERE id = {item['id']}"
                    c.execute(info)
            elif item['table'] == 'Termins':
                if 'null' in [item['request'], item['id'], item['Termin']]:
                    continue
                if item['request'] == 'ADD':
                    request = []
                    for s in ["retranslation", "Image"]:
                        if item[s] == 'null':
                            request.append('null')
                        else:
                            request.append('\'' + item[s] + '\'')
                    info = f"INSERT INTO Termins VALUES({item['id']}, '{item['Termin']}', {', '.join(request)})"
                    c.execute(info)
                elif item['request'] == 'CHANGE':
                    request = []
                    for s in ["retranslation", "Image"]:
                        if item[s] == 'null':
                            request.append(f"{s} = null")
                        else:
                            request.append(f"{s} = \'{item[s]}\'")
                    info = f"UPDATE Termins\nSET {', '.join(request)}\nWHERE id = {item['id']}"
                    c.execute(info)
                elif item['request'] == 'DELETE':
                    info = f"DELETE FROM Termins\nWHERE id = {item['id']}"
                    c.execute(info)
            elif item['table'] in ['Flagellums', 'Food', 'Plastid']:
                if 'null' in [item['request'], item['id'], item['letter'], item['retranslation']]:
                    continue
                if item['request'] == 'ADD':
                    info = f"INSERT INTO {item['table']} VALUES({item['id']}, '{item['letter']}', '{item['retranslation']}')"
                    c.execute(info)
                elif item['request'] == 'CHANGE':
                    info = f"UPDATE {item['table']}\nSET letter = '{item['letter']}', retranslation = '{item['retranslation']}'\nWHERE id = {item['id']}"
                    c.execute(info)
                elif item['request'] == 'DELETE':
                    info = f"DELETE FROM {item['table']}\nWHERE id = {item['id']}"
                    c.execute(info)

        file.close()
        connection.commit()
        connection.close()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    execute = MainWindowWork()
    execute.show()
    sys.exit(app.exec_())
