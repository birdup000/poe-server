import sys
import time
import requests
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QTextEdit, QLineEdit, QPushButton, QLabel, QScrollBar
from PyQt5.QtGui import QIcon, QColor, QPalette, QFont
from PyQt5.QtCore import Qt, QThread, pyqtSignal, QCoreApplication


class TypingThread(QThread):
    typing_done = pyqtSignal()
    typing_output = pyqtSignal(str)

    def __init__(self, response_text):
        super().__init__()
        self.response_text = response_text

    def run(self):
        for char in self.response_text:
            QThread.msleep(50)  # Simulate typing speed
            self.typing_output.emit(char)
        self.typing_done.emit()


class LoadingLabel(QLabel):
    def __init__(self):
        super().__init__()
        self.setText("Loading")
        self.setFont(QFont("Arial", 14, QFont.Bold))
        self.setAlignment(Qt.AlignCenter)
        self.dots = 0

    def update_dots(self, progress):
        self.dots = (progress % 3) + 1
        self.setText("Loading" + "." * self.dots)


class ChatClient(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()
        self.messages = [{'role': 'system', 'content': 'You are a helpful assistant.'}]
        self.typing_thread = None

    def init_ui(self):
        self.setWindowTitle('ChatterBox')
        self.setWindowIcon(QIcon('icon.png'))
        self.resize(400, 500)

        # Create widgets
        self.message_view = QTextEdit()
        self.user_input = QLineEdit()
        self.send_button = QPushButton("Send")
        self.loading_label = LoadingLabel()
        self.loading_label.hide()

        # Set widget styles
        self.message_view.setStyleSheet("QTextEdit { color: white; background-color: #333333; padding: 5px; }")
        self.user_input.setStyleSheet("QLineEdit { color: white; background-color: #333333; padding: 5px; }")
        self.send_button.setStyleSheet("QPushButton { color: white; background-color: #555555; padding: 5px; }")

        self.send_button.clicked.connect(self.send_message)

        # Set up layout
        layout = QVBoxLayout()
        layout.addWidget(self.message_view)
        layout.addWidget(self.user_input)
        layout.addWidget(self.send_button)
        layout.addWidget(self.loading_label)

        self.setLayout(layout)

    def send_message(self):
        user_message = self.user_input.text()
        if user_message.lower() == "exit":
            sys.exit()
        self.loading_screen()
        self.messages.append({'role': 'user', 'content': user_message})
        self.update_message_view()

        self.show_response()

    def loading_screen(self):
        self.loading_label.show()

    def show_response(self):
        self.loading_label.hide()
        response_text = self.generate_response(self.messages)
        self.typing_thread = TypingThread(response_text)
        self.typing_thread.typing_done.connect(self.update_message_view)
        self.typing_thread.typing_output.connect(self.append_char_to_last_message)
        self.typing_thread.start()

    def generate_response(self, messages):
        response = requests.post(
            "http://localhost:8000/v1/chat/completions",  # Your server's address
            json={"messages": messages}
        )
        response.raise_for_status()  # Raise an error if the request failed
        data = response.json()
        return data["choices"][0]["content"]

    def append_char_to_last_message(self, char):
        self.messages[-1]['content'] += char
        self.update_message_view(scroll_to_bottom=True)

    def update_message_view(self, scroll_to_bottom=False):
        self.message_view.clear()

        for message in self.messages:
            role = message['role']
            content = message['content']

            if role == 'user':
                content = f"<b>You:</b> {content}"
                self.message_view.append(content)
            elif role == 'assistant':
                content = f"<b>Assistant:</b> {content}"
                self.message_view.append(content)
            elif role == 'system':
                content = f"<i>{content}</i>"
                self.message_view.append(content)

        self.message_view.append("")  # Add a blank line for spacing

        if scroll_to_bottom:
            scrollbar = self.message_view.verticalScrollBar()
            scrollbar.setValue(scrollbar.maximum())

        self.user_input.clear()
        self.user_input.setFocus()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    chat_client = ChatClient()
    chat_client.show()
    sys.exit(app.exec_())