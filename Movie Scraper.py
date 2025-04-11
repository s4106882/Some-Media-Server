from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLabel, QLineEdit
from PyQt5.QtCore import Qt
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
import sys

class MediaServerApp(QWidget):
    def __init__(self):
        super().__init__()
        
        # Set up window
        self.setWindowTitle("Rudy's Awesome Media")
        self.setGeometry(100, 100, 400, 400)
        
        self.layout = QVBoxLayout()
        
        self.label = QLabel("Woah this is some really cool text.")
        self.layout.addWidget(self.label)
        
        self.input_box = QLineEdit(self)
        self.input_box.setPlaceholderText("Type something here...")
        self.layout.addWidget(self.input_box)
        
        self.download_button = QPushButton("Search")
        self.download_button.clicked.connect(self.on_download_clicked)
        self.layout.addWidget(self.download_button)
        
        self.setLayout(self.layout)
        
    def on_download_clicked(self):
        search_text = self.input_box.text()
        if search_text:
            self.label.setText("Searching...")
            titles = scrape_movies(search_text)
            if titles:
                temp = titles[:]
                titles.clear()
                for each in temp:
                    if each != '':
                        titles.append(each)
                    else:
                        break
                movie_count = str(len(titles))
                self.layout.addWidget(QLabel("Movies Found: " + movie_count))
                for each in titles:
                        self.layout.addWidget(QPushButton(each))
                #self.label.setText("\n".join(titles))
            else:
                self.label.setText("No results found.")
        else:
            self.label.setText("Please enter a search term.")
        
def scrape_movies(search_text):
    options = webdriver.ChromeOptions()
    options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36')
    options.add_argument('--headless')
    options.add_argument('--disable-images')
    options.add_argument('--disable-extensions')
    driver = webdriver.Chrome(options=options)
    
    driver.get(f'https://flickystream.com/search?q={search_text}')
    driver.maximize_window()
    
    WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'h3.text-white.font-medium.line-clamp-1.text-balance'))
    )
    
    movies = driver.find_elements(By.CSS_SELECTOR, 'h3.text-white.font-medium.line-clamp-1.text-balance')
    movies_titles = [movie.text for movie in movies]
    
    driver.quit()
    return movies_titles

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MediaServerApp()
    window.show()
    sys.exit(app.exec_())
