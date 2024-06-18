import requests
from bs4 import BeautifulSoup

def verificar_ranqueamento(prompt, site_alvo, num_resultados=50):
    try:
        query = '+'.join(prompt.split())
        url = f"https://www.google.com/search?q={query}&num={num_resultados}"
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, 'html.parser')
        resultados = soup.find_all('div', class_='g')
        
        for posicao, resultado in enumerate(resultados, start=1):
            link = resultado.find('a', href=True)
            if link and site_alvo in link['href']:
                return posicao
            
        return None
    
    except Exception as e:
        print(f"Ocorreu um erro: {e}")	
        return None
    
prompt = "melhores restaurantes guarulhos"
site_alvo = "https://www.tripadvisor.com.br"

posicao = verificar_ranqueamento(prompt, site_alvo)
if posicao is not None:
    print(f"O site {site_alvo} está na posição {posicao} do Google")
else: 
    print(f"O site {site_alvo} não foi encontrado nos primeiros resultados")
