import subprocess
import sys
import time
import webbrowser
import requests

# Caminho do Python que está executando o script
python_exec = sys.executable

# Inicia diretamente o script Flask (sem usar 'flask run')
flask_process = subprocess.Popen([python_exec, 'adicionar_nomes.py'])

# URL onde o Flask será acessado
flask_url = "http://127.0.0.1:5000"
timeout = 15  # Tempo máximo para aguardar o Flask iniciar
start_time = time.time()

# Aguarda o Flask iniciar antes de abrir o navegador
while True:
    try:
        response = requests.get(flask_url)
        if response.status_code == 200:
            break  # Flask iniciou com sucesso
    except requests.exceptions.ConnectionError:
        pass  # Continua tentando até o timeout

    if time.time() - start_time > timeout:
        print("Erro: O Flask não iniciou dentro do tempo limite.")
        break  # Sai do loop se não iniciar no tempo limite

    time.sleep(1)  # Espera 1 segundo antes de tentar novamente

# Abre o navegador automaticamente se o Flask estiver rodando
webbrowser.open(flask_url)

# Mantém o terminal aberto para evitar fechamento imediato
input("Pressione Enter para sair...")
