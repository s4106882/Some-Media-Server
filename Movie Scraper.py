from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def scrape_movies():
    options = webdriver.ChromeOptions()
    options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36')
    options.add_argument('--headless')
    driver = webdriver.Chrome(options=options)
    
    driver.get('https://www.imdb.com/chart/top/?ref_=nv_mv_250')
    
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, 'h3.ipc-title__text'))
    )
    
    movies = driver.find_elements(By.CSS_SELECTOR, 'h3.ipc-title__text')
    movies_titles = [movie.text for movie in movies]
    
    driver.quit()
    return movies_titles

titles = scrape_movies()
print(titles)