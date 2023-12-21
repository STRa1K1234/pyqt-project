import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton, QDesktopWidget
from PyQt5.QtCore import QTimer, Qt, QEvent
import random
import sqlite3

class SpeedTypingTest(QWidget):
    def startTest(self):
        # Устанавливаем фокус на поле ввода и очищаем его
        self.input.setFocus()
        self.input.clear()
        # Сбрасываем время
        self.timeElapsed = 0
        # Устанавливаем соединение с методом updateTime при срабатывании таймера и запускаем его
        self.timer.timeout.connect(self.updateTime)
        self.timer.start(1000)  # Таймер срабатывает каждую секунду
        self.stopped = False  # Устанавливаем флаг остановки в False

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # Настройка интерфейса
        self.setGeometry(100, 100, 750, 200)
        self.setStyleSheet("background-color: #C3E1C9;")
        self.setWindowTitle('Speed Typing Test')

        self.label = QLabel('Type the following sentence:', self)
        self.label.move(20, 20) # установка условий

        self.sentence = QLabel('', self)
        self.sentence.setGeometry(20, 40, 360, 20)  # установка строки

        self.input = QLineEdit(self)
        self.input.setGeometry(20, 70, 360, 20)
        self.input.installEventFilter(self)  # создание окна

        self.startButton = QPushButton('Start', self)
        self.startButton.setGeometry(20, 100, 80, 30)
        self.startButton.clicked.connect(self.startTest)  # Привязываем нажатие кнопки "Start" к методу startTest

        self.timerLabel = QLabel('Time: 0 seconds', self)
        self.timerLabel.setGeometry(300, 100, 200, 30)  # установка таймера

        self.speedLabel = QLabel('Speed: 0 characters/minute', self)
        self.speedLabel.setGeometry(20, 120, 200, 30)   # установка скорости
        self.speedLabel.setGeometry(20, 120, 250, 30)   # установка скорости

        self.timer = QTimer()  # Создаем таймер для отслеживания времени
        self.timeElapsed = 0  # Переменная для отслеживания прошедшего времени
        self.stopped = False  # Флаг остановки для отслеживания завершения теста
        self.center()  # вызов нового метода для центрирования окна
        self.loadRandomSentence()  # загружаем случайную строку из базы данных
        self.sentence.setWordWrap(True)  # позволяет переносить текст внутри Label
        self.sentence.setFixedSize(400, 30)  # установка фиксированного размера для Label

    def loadRandomSentence(self):
        # Подключение к базе данных
        conn = sqlite3.connect('new_database.db')
        cursor = conn.cursor()

        # Выбор случайной строки из базы данных
        cursor.execute("SELECT line FROM lines ORDER BY RANDOM() LIMIT 1")
        result = cursor.fetchone()
        if result:
            self.sentence.setText(result[0])

        conn.close()

    def center(self):
        # Метод для центрирования окна
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def startTest(self):
        # Начало теста
        self.input.setFocus()
        self.input.clear()
        self.timeElapsed = 0
        self.timer.timeout.connect(self.updateTime)
        self.timer.start(1000)
        self.stopped = False

    def eventFilter(self, obj, event):
        # Фильтр событий для поля ввода
        if obj is self.input and event.type() == QEvent.KeyPress and event.key() in (Qt.Key_Return, Qt.Key_Enter) and not self.stopped:
            self.timer.stop()
            self.stopped = True
            accuracy = self.calculateAccuracy()
            self.showResult(accuracy)
        return super().eventFilter(obj, event)

    def updateTime(self):
        self.timeElapsed += 1
        self.timerLabel.setText(f'Time: {self.timeElapsed} seconds')

    def calculateAccuracy(self):
        # Метод расчета точности ввода
        sentence = self.sentence.text()
        userInput = self.input.text()
        correctCharacters = sum(1 for i, j in zip(sentence, userInput) if i == j)
        accuracy = (correctCharacters / len(sentence)) * 100
        speed = len(userInput) / self.timeElapsed * 60
        self.speedLabel.setText(f'Speed: {speed:.2f} characters/minute')
        return accuracy

    def showResult(self, accuracy):
        # Метод отображения результата теста
        resultLabel = QLabel(f'Accuracy: {accuracy:.2f}% \nTime: {self.timeElapsed} seconds', self)
        resultLabel.move(20, 143)
        resultLabel.show()


# запуск программы
if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = SpeedTypingTest()
    ex.show()
    sys.exit(app.exec_())


