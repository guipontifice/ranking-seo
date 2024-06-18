from googlesearch import search

def verificar_ranqueamento(prompt, num=10, stop=10, pause=2.0):
    try:

        resultados = search(prompt, num=10, stop=10, pause=2.0)

        for posicao, resultado in enumerate(resultados, start=1):
            if site_alvo in resultado:
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
    print(f"O site {site_alvo} não foi encontrado no Google")
    