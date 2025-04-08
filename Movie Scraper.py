from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC

def scrape_movies():
    options = webdriver.ChromeOptions()
    options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36')
    options.add_argument('--headless')
    options.add_argument('--disable-images')
    options.add_argument('--disable-extensions')
    driver = webdriver.Chrome(options=options)
    
    search_text = str(input())
    driver.get(f'https://flickystream.com/search?q={search_text}')
    driver.maximize_window()
    
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, 'h3.text-white.font-medium.line-clamp-1.text-balance'))
    )
    
    movies = driver.find_elements(By.CSS_SELECTOR, 'h3.text-white.font-medium.line-clamp-1.text-balance')
    movies_titles = [movie.text for movie in movies]
    
    input("Press enter to close the browser")
    
    driver.quit()
    return movies_titles

titles = scrape_movies()
print(titles)