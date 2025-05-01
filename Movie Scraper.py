from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLabel, QLineEdit
from PyQt5.QtCore import Qt, QUrl
from PyQt5.QtWebEngineWidgets import QWebEngineView
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
import sys
from functools import partial
import platform
import subprocess

class MediaServerApp(QWidget):
    def __init__(self):
        super().__init__()
        self.movie_dict = {}
        self.result_label = QLabel("")
        self.movie_exists = False
        self.param = '-n' if platform.system().lower() == 'windows' else '-c'
        
        # Set up window
        self.setWindowTitle("Rudy's Awesome Media")
        self.setGeometry(400, 200, 1024, 768)
        
        self.layout = QVBoxLayout()
        
        self.layout.addWidget(self.result_label)
        
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
            titles = self.scrape_movies(search_text)
            if titles:
                if self.movie_dict:
                    for movie_num in range(len(self.movie_dict)):
                        self.layout.removeWidget(self.movie_dict[movie_num])
                    self.movie_dict.clear()
                temp = titles[:]
                titles.clear()
                for each in temp:
                    if each != '':
                        titles.append(each)
                    else:
                        break
                movie_count = str(len(titles))
                self.result_label.setText("Movies Found: " + movie_count)
                for movie_num, title in enumerate(titles):
                    movie_button = QPushButton(title)
                    self.movie_dict[movie_num] = movie_button
                    movie_button.clicked.connect(partial(self.on_movie_selected, title))
                    self.layout.addWidget(movie_button)
            else:
                self.label.setText("No results found.")
        else:
            self.label.setText("Please enter a search term.")
            
    def on_movie_selected(self, title):
        if self.movie_exists:
            self.layout.removeWidget(self.browser)
        self.browser = QWebEngineView()
        self.layout.addWidget(self.browser)
        self.movie_exists = True
        
        #TODO: Add list of actual hosts
        host_list = {'imdb.com': True, 'youtube.com': False}
        
        for host in host_list.keys():
            command = ['ping', self.param, '1', host]
            if subprocess.call(command) == 0:
                host_list[host] = True
            else:
                host_list[host] = False
        
        for host, status in host_list.values():
            if status == True:
                # Check if host has movie in database
                pass
        
        #TODO: Add proxy
        self.browser.setUrl(QUrl(f'imdb.com/movies/{self.title_to_url[title]}'))
            
    def scrape_movies(self, search_text):
        options = webdriver.ChromeOptions()
        options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36')
        options.add_argument('--headless')
        options.add_argument('--disable-images')
        options.add_argument('--disable-extensions')
        driver = webdriver.Chrome(options=options)
    
        driver.get(f'https://www.imdb.com/find/?q={search_text}&ref_=nv_sr_sm')
        driver.maximize_window()
    
        WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, "a.ipc-metadata-list-summary-item__t"))
        )
    
        movies = driver.find_elements(By.CSS_SELECTOR, "a.ipc-metadata-list-summary-item__t")
    
        movie_url_list = []
        self.title_to_url = {}
    
        for link in movies:
            movie_url = link.get_attribute('href')
            movie_url_list.append(movie_url)
        for index, each in enumerate(movie_url_list):
            split_url = each.split('/')
            movie_url_list[index] = split_url[4]
        for each in movie_url_list[:]:
            if 'nm' in each:
                movie_url_list.remove(each)

        movies_titles = [movie.text for movie in movies]
        for i in range(len(movie_url_list)):
            self.title_to_url[movies_titles[i]] = movie_url_list[i]
    
        driver.quit()
        return movies_titles

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MediaServerApp()
    window.show()
    sys.exit(app.exec_())