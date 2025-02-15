import random
import time
import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
import pandas as pd

ua = UserAgent()

def verificar_ranqueamento(prompt, site_alvo, num_resultados=50):
    try:
        query = '+'.join(prompt.split())
        url = f"https://www.google.com/search?q={query}&num={num_resultados}"
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        
        # Verifique se reCAPTCHA está presente
        if "To continue, please verify that you are not a robot" in response.text:
            print("ReCAPTCHA detectado. Pausando solicitações.")
            time.sleep(60 * 15)
            return None

        soup = BeautifulSoup(response.text, 'html.parser')
        resultados = soup.find_all('div', class_='yuRUbf')
        
        for posicao, resultado in enumerate(resultados, start=1):
            link = resultado.find('a', href=True)
            if link and site_alvo in link['href']:
                return posicao
            
        return None
    
    except Exception as e:
        print(f"Ocorreu um erro: {e}")    
        return None

df = pd.read_csv('prompts.csv')

site_alvo = " www.tripadvisor.com.br"

resultados = []

for index, row in df.iterrows():
    prompt = row['Palavras-chave']  # Substitua 'Palavras-chave' pelo nome da coluna que contém as strings de busca
    posicao = verificar_ranqueamento(prompt, site_alvo)
    if posicao is not None:
        print(f"O site {site_alvo} está na posição {posicao} do Google para a busca '{prompt}'")
    else: 
        print(f"O site {site_alvo} não foi encontrado nos primeiros resultados para a busca '{prompt}'")
        
    resultados.append({'Nome da Pesquisa': prompt, 'Rankeamento': posicao if posicao is not None else 'Não encontrado'})
    
    if (index + 1) % 10 == 0:
        resultados_df = pd.DataFrame(resultados)
        resultados_df.to_csv('resultados_parciais.csv', index=False)
        print(f"Resultados parciais salvos no arquivo 'resultados_parciais.csv' até a linha {index + 1}.")
    
    time.sleep(random.uniform(5, 15))

resultados_df = pd.DataFrame(resultados)

resultados_df.to_csv('resultados.csv', index=False)
print("Os resultados finais foram salvos no arquivo 'resultados.csv'.")

print("\nResultados finais:")
print(resultados_df)