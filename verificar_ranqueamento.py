import random
import time
import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
import pandas as pd
from abrir_pagina import abrir_pagina_anonima
from pathlib import Path
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

ua = UserAgent()

proxies = [
    'http://proxy1.com:port',
    'http://proxy2.com:port',
    'http://proxy3.com:port'
    # Adicione mais proxies conforme necessário
]

def configurar_navegador():
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--incognito")
    chrome_options.add_argument("--disabled-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")
    
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    return driver

def verificar_ranqueamento(prompt, site_alvo, num_resultados=50):
    driver = configurar_navegador()
    query = '+'.join(prompt.split())
    url = f"https://www.google.com/search?q={query}&num={num_resultados}"
    
    driver.get(url)
    # Tempo aleatório pro Recaptcha não pegar (é bom aumentar um pouco a entropia pra dps evitar de cair no recaptcha)
    time.sleep(random.uniform(2, 5))  

    resultados = driver.find_elements(By.CSS_SELECTOR, 'div.yuRUbf')
    
    posicao_real = 0
    for resultado in resultados:
        # Verificar se é um anúncio patrocinado
        try:
            anuncio = resultado.find_element(By.XPATH, './/span[text()="Anúncio" or text()="Ad"]')
            if anuncio:
                continue
        except:
            pass
        
        posicao_real += 1
        link = resultado.find_element(By.TAG_NAME, 'a').get_attribute('href')
        if site_alvo in link:
            driver.quit()
            return posicao_real

    driver.quit()
    return None
    

df = pd.read_csv('prompts.csv')

site_alvo = "www.mrferreiralocacoes.com.br"

resultados = []

for index, row in df.iterrows():
    prompt = row['Palavras-chave']  
    posicao = verificar_ranqueamento(prompt, site_alvo)
    if posicao is not None:
        print(f"O site {site_alvo} está na posição {posicao} do Google para a busca '{prompt}'")
    else: 
        print(f"O site {site_alvo} não foi encontrado nos primeiros resultados para a busca '{prompt}'")
        
    resultados.append({'Nome da Pesquisa': prompt, 'Rankeamento': posicao if posicao is not None else 'Não encontrado'})
    
    if (index + 1) % 10 == 0:
        resultados_df = pd.DataFrame(resultados)
        resultados_df.to_csv('resultados_parciais.csv', index=False)
    