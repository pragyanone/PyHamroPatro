import sys
import os
import requests
import ctypes
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QPushButton
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtCore import QUrl, QByteArray, QBuffer, QTimer
from PyQt5.QtGui import QIcon, QImage

# Define constants for Windows API
GWL_STYLE = -16
WS_SYSMENU = 0x80000
WM_SYSCOMMAND = 0x0112
SC_CLOSE = 0xF060
SC_MINIMIZE = 0xF020
SC_MAXIMIZE = 0xF030

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PyHamroPatro")
        self.setGeometry(40, 80, 850, 900)

        # Load and set the application icon
        self.setWindowIcon(QIcon("hamropatro.ico"))  # Replace "your_icon.ico" with the actual path to your ICO file

        self.web_view = QWebEngineView()
        self.load_button = QPushButton("Load Calendar")
        self.load_button.clicked.connect(self.load_calendar)
        
        layout = QVBoxLayout()
        layout.addWidget(self.web_view)
        layout.addWidget(self.load_button)
        
        container = QWidget()
        container.setLayout(layout)
        
        self.setCentralWidget(container)

        # Disable the window buttons
        self.disable_window_buttons()

        # Check internet connection at startup
        self.check_and_load()

    def disable_window_buttons(self):
        hwnd = self.winId()
        style = ctypes.windll.user32.GetWindowLongW(int(hwnd), GWL_STYLE)
        style &= ~WS_SYSMENU  # Remove system menu (close button)
        style &= ~SC_MINIMIZE  # Remove minimize button
        style &= ~SC_MAXIMIZE  # Remove maximize button
        ctypes.windll.user32.SetWindowLongW(int(hwnd), GWL_STYLE, style)

    def check_internet_connection(self):
        try:
            requests.get("https://www.google.com", timeout=5)
            return True
        except requests.ConnectionError:
            return False

    def check_and_load(self):
        if self.check_internet_connection():
            # If internet is available, load the web page
            self.web_view.setUrl(QUrl("https://www.hamropatro.com/widgets/calender-full.php"))
            # Take a screenshot after 5 seconds
            QTimer.singleShot(5000, self.take_screenshot)
        else:
            # If offline, load the screenshot
            self.load_screenshot()

    def take_screenshot(self):
        # Take a screenshot of the web page
        pixmap = self.web_view.grab()
        pixmap = pixmap.scaledToWidth(int(pixmap.width() * 0.98))
        pixmap.save("screenshot.png", "png")

    def load_screenshot(self):
        # Load the screenshot if offline
        if os.path.exists("screenshot.png"):
            image = QImage("screenshot.png")
            bytes_array = QByteArray()
            buffer = QBuffer(bytes_array)
            buffer.open(QBuffer.WriteOnly)
            image.save(buffer, "PNG")
            self.web_view.setHtml(f"<img src='data:image/png;base64,{bytes_array.toBase64().data().decode()}'>")
        else:
            self.web_view.setHtml("<h1>No Internet Connection</h1><p>And no cached version available.</p>")

    def load_calendar(self):
        if self.check_internet_connection():
            # If online, load the web page
            self.web_view.setUrl(QUrl("https://www.hamropatro.com/widgets/calender-full.php"))
        else:
            # If offline, load the screenshot
            self.load_screenshot()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
