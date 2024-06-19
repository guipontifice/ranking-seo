from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

def abrir_pagina_anonima(url):
    chrome_options = Options()
    chrome_options.add_argument("--incognito")
    driver = webdriver.Crhome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    driver.get(url)
    return driver