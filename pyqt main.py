import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout, QLineEdit, QPushButton
from PyQt5.QtCore import QTimer, Qt, QTime
from PyQt5.QtGui import QFont  # Add QFont import
import random

class TimerApp(QWidget):
    def __init__(self):  # Correct the init method name
        super().__init__()  # Correct the super() call
        layout = QVBoxLayout()

        self.random_line = self.get_random_line()  # Store the random line
        self.random_line_label = QLabel(self.random_line, self)
        self.random_line_label.setFont(QFont("Arial", 14))  # Set a larger font for the random_line_label
        layout.addWidget(self.random_line_label)

        self.timer_label = QLabel("Enter time in seconds:", self)
        self.timer_label.setFont(QFont("Arial", 14))  # Set a larger font for the timer_label
        layout.addWidget(self.timer_label)

        self.input_timer = QLineEdit(self)
        self.input_timer.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.input_timer)

        self.start_button = QPushButton("Start Timer", self)
        self.start_button.clicked.connect(self.start_timer)
        layout.addWidget(self.start_button)

        self.error_label = QLabel("", self)
        layout.addWidget(self.error_label)

        self.typing_speed_label = QLabel("", self)
        layout.addWidget(self.typing_speed_label)

        self.setLayout(layout)

        self.timer_counter = QTimer()
        self.timer_counter.timeout.connect(self.update_timer)
        self.current_timer_value = 0  # Store the current timer value for reference

    def start_timer(self):
        self.start_button.setEnabled(False)  # Disable the start button
        self.current_timer_value = int(self.input_timer.text())
        self.timer_label.setText("Timer: " + str(self.format_time(self.current_timer_value)))  # Format the time using format_time method
        self.input_timer.clear()
        self.input_timer.textChanged.connect(self.check_input)  # Connect the text changed signal to check_input method
        self.timer_counter.start(1000)

    def check_input(self, text):
        if text != self.random_line:  # Check if the input text matches the random line
            self.start_button.setEnabled(False)  # Disable the start button if the input is incorrect
        else:
            self.start_button.setEnabled(True)  # Enable the start button if the input is correct

    def update_timer(self):
        self.current_timer_value -= 1
        if self.current_timer_value < 0:  # Check if the timer has expired
            self.timer_counter.stop()
            self.timer_label.setText("Time's up!")
            self.input_timer.hide()  # Hide the input field when the timer expires
            error_count = self.calculate_errors(self.input_timer.text())
            typing_speed = self.calculate_typing_speed(self.input_timer.text())
            self.error_label.setText(f"Errors: {error_count}")  # Update the error count label
            self.typing_speed_label.setText(f"Typing speed: {typing_speed} characters per minute")  # Update the typing speed label
        else:
            self.timer_label.setText("Timer: " + str(self.format_time(self.current_timer_value)))  # Format the time using format_time method

    def format_time(self, seconds):  # Method to format time from seconds to MM:SS format
        return QTime(0, seconds // 60, seconds % 60).toString("mm:ss")

    def calculate_errors(self, input_text):  # Method to calculate the number of errors in the input text
        error_count = 0
        for i in range(len(self.random_line)):
            if i >= len(input_text) or input_text[i] != self.random_line[i]:
                error_count += 1
        return error_count

    def calculate_typing_speed(self, input_text):  # Method to calculate the typing speed
        time_taken = int(self.timer_label.text().split(":")[1])  #
        typing_speed = int(len(input_text) / (time_taken / 60))  # Calculate characters per minute
        return typing_speed

    def get_random_line(self):
        with open('input.txt', encoding='utf8') as f:
            lines = f.readlines()
        return random.choice(lines).strip()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    timer_app = TimerApp()
    timer_app.show()
    timer_app.setGeometry(100, 100, 400, 200)
    app.processEvents()
    sys.exit(app.exec_())

