from carregar_nomes import carregar_nomes
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import time
import random
import requests
from datetime import datetime
import sys
sys.stdout.reconfigure(encoding='utf-8')  # Força saída UTF-8 no Windows


# Função para carregar o arquivo de resultados do dia anterior
def carregar_resultados_anteriores():
    try:
        with open("profissionais_sem_ficha.txt", "r", encoding="utf-8") as f:
            return f.readlines()
    except FileNotFoundError:
        return []

# Configuração do Selenium (sem headless para debug)
chrome_options = Options()
# chrome_options.add_argument("--headless")  # Ative apenas após testar
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--no-sandbox")

# Inicializa o WebDriver
service = Service("chromedriver.exe")  # Ajuste o caminho do chromedriver se necessário
driver = webdriver.Chrome(service=service, options=chrome_options)

# Carregar nomes e estados do arquivo nomes.txt
nomes_estados = carregar_nomes()

# Verificar se há nomes
if not nomes_estados:
    print("Nenhum nome encontrado. Verifique o arquivo nomes.txt.")
    driver.quit()
    exit()

# Carregar resultados do dia anterior
resultados_anteriores = carregar_resultados_anteriores()

# Lista para armazenar os profissionais sem ficha
sem_ficha = []

# Função para verificar se a ficha existe na página
def tem_ficha_google():
    """Verifica se há uma ficha do Google Meu Negócio na página."""
    try:
        time.sleep(3)  # Espera mais rápido para cada página de resultados
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")  # Rola a página
        time.sleep(3)

        # Busca por possíveis classes do painel de ficha do Google
        elementos_ficha = driver.find_elements(By.CLASS_NAME, "kp-wholepage")  # Painel inteiro
        if not elementos_ficha:
            elementos_ficha = driver.find_elements(By.CLASS_NAME, "kp-header")  # Cabeçalho do painel
        if elementos_ficha:
            return True
    except Exception as e:
        print(f"Erro ao verificar ficha: {e}")
    return False

# Registrar data de início
data_inicio = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
print(f" Início do processo: {data_inicio}")

# Loop para pesquisar cada nome + estado, testando "psicólogo" e "psicanalista"
for i, (nome, estado) in enumerate(nomes_estados):
    # Verificar se o nome já foi pesquisado no dia anterior
    if f"{nome}, {estado}\n" in resultados_anteriores:
        print(f" {nome} já foi pesquisado no dia anterior. Pulando pesquisa...")
        continue

    ficha_encontrada = False  # Variável para marcar se algum termo foi encontrado

    # Se o estado não foi fornecido, pesquisa apenas pelo nome e profissão
    for profissao in ["psicólogo", "psicanalista"]:
        if estado.strip():  # Se o estado não for vazio, adiciona na consulta
            consulta = f"{nome} {profissao} {estado}"
        else:  # Se o estado for vazio, pesquisa apenas pelo nome e profissão
            consulta = f"{nome} {profissao}"

        url = f"https://www.google.com/search?q={consulta}"
        print(f" Pesquisando: {consulta}")

        driver.get(url)

        # Aumenta o tempo de espera para a primeira pesquisa (para resolver o CAPTCHA)
        if i == 0:  # A primeira pesquisa terá mais tempo
            time.sleep(30)  # Espera 30 segundos na primeira pesquisa
        else:  # As pesquisas subsequentes terão tempo de espera mais rápido
            time.sleep(0.5)  # Espera 500ms (0.5 segundos) entre as pesquisas

        if tem_ficha_google():
            print(f" {nome} ({profissao}) possui ficha no Google Meu Negócio.")
            ficha_encontrada = True
            break  # Se encontrar ficha para alguma das profissões, interrompe o loop

    if not ficha_encontrada:
        print(f" {nome} NÃO possui ficha no Google Meu Negócio.")
        sem_ficha.append(f"{nome}, {estado}")

# Fecha o navegador
driver.quit()

# Salva os profissionais sem ficha no arquivo
if sem_ficha:
    with open("profissionais_sem_ficha.txt", "a", encoding="utf-8") as f:
        for item in sem_ficha:
            f.write(item + "\n")
    print(" Lista de profissionais sem ficha salva em 'profissionais_sem_ficha.txt'.")

# Adiciona a data de início e a quantidade de profissionais sem ficha ao arquivo de log
with open("log.txt", "a", encoding="utf-8") as log:
    log.write(f"\nInício do processo: {data_inicio}\n")
    log.write(f"Total de profissionais sem ficha: {len(sem_ficha)}\n")
    log.write("-" * 30 + "\n")

# Exibe a quantidade de resultados
if sem_ficha:
    print(f" {len(sem_ficha)} profissionais sem ficha no Google Meu Negócio.")
else:
    print(" Todos os profissionais possuem ficha no Google Meu Negócio.")
