import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton
from PyQt5.QtCore import QTimer, Qt, QEvent

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
        self.setGeometry(100, 100, 400, 200)
        self.setWindowTitle('Speed Typing Test')

        self.label = QLabel('Type the following sentence:', self)
        self.label.move(20, 20)

        self.sentence = QLabel('The quick brown fox jumps over the lazy dog', self)
        self.sentence.setGeometry(20, 40, 360, 20)

        self.input = QLineEdit(self)
        self.input.setGeometry(20, 70, 360, 20)
        self.input.installEventFilter(self)

        self.startButton = QPushButton('Start', self)
        self.startButton.setGeometry(20, 100, 80, 30)
        self.startButton.clicked.connect(self.startTest)  # Привязываем нажатие кнопки "Start" к методу startTest

        self.timerLabel = QLabel('Time: 0 seconds', self)
        self.timerLabel.setGeometry(300, 100, 100, 30)

        self.speedLabel = QLabel('Speed: 0 characters/minute', self)
        self.speedLabel.setGeometry(20, 120, 150, 30)

        self.timer = QTimer()  # Создаем таймер для отслеживания времени
        self.timeElapsed = 0  # Переменная для отслеживания прошедшего времени
        self.stopped = False  # Флаг остановки для отслеживания завершения теста

    def startTest(self):
        # Метод начала теста
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


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = SpeedTypingTest()
    ex.show()
    sys.exit(app.exec_())

# TODO добавить датабазу