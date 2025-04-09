'''
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLabel, QLineEdit
from PyQt5.QtCore import Qt

class MediaServerApp(QWidget):
    def __init__(self):
        super().__init__()
        
        # Set up window
        self.setWindowTitle("Rudy's Awesome Media")
        self.setGeometry(100, 100, 400, 400)
        
        layout = QVBoxLayout()
        
        self.label = QLabel("Welcome to my server!")
        layout.addWidget(self.label)
        
        self.input_box = QLineEdit(self)
        self.input_box.setPlaceholderText("Type something here...")
        layout.addWidget(self.input_box)
        
        self.download_button = QPushButton("Search")
        self.download_button.clicked.connect(self.on_download_clicked)
        layout.addWidget(self.download_button)
        
        self.setLayout(layout)
        
    def on_download_clicked(self):
        self.download_button.setText("Searching...")
        output = self.input_box.text()
        return output

        
        
if __name__ == '__main__':
    app = QApplication([])
    window = MediaServerApp()
    window.show()
    app.exec_()
'''