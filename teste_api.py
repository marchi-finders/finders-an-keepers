import requests

# Substitua pela sua chave de API
API_KEY = "AIzaSyAykkPWmJr8sewgpjPaCnVcG6PodCNK1YE"

# Endpoint da API do Google Meu Negócio
URL = f"https://mybusiness.googleapis.com/v4/accounts?key={API_KEY}"

response = requests.get(URL)

if response.status_code == 200:
    print("✅ Conexão bem-sucedida!")
    print(response.json())  # Mostra os dados retornados
else:
    print("❌ Erro na requisição:", response.status_code, response.text)