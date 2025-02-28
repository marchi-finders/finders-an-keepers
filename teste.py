import requests

# Substitua pela sua chave de API
API_KEY = "AIzaSyBpO9XxM1ct0B3w9XITyvPKenSrp8tOq74"

# Endpoint da API do Google Meu Negócio
URL = f"https://mybusiness.googleapis.com/v4/accounts?key={API_KEY}"

response = requests.get(URL)

if response.status_code == 200:
    print("✅ Conexão bem-sucedida!")
    print(response.json())  # Mostra os dados retornados
else:
    print("❌ Erro na requisição:", response.status_code, response.text)
