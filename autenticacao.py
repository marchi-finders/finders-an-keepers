import os
import google.auth
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

# Caminho para o arquivo de credenciais que você obteve do Google Cloud Console
CLIENT_SECRET_FILE = 'client_secret.json'
SCOPES = ['https://www.googleapis.com/auth/business.manage']

def get_authenticated_service():
    # Tenta carregar as credenciais salvas anteriormente (se houver)
    creds = None
    if os.path.exists('token.json'):
        creds, project = google.auth.load_credentials_from_file('token.json')
    
    # Se as credenciais não existirem ou forem inválidas, faça a autenticação
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            # Inicia o fluxo OAuth e redireciona para localhost (sem domínio)
            flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRET_FILE, SCOPES)
            creds = flow.run_local_server(port=8080)  # Redirecionamento para localhost:8080
        # Salva as credenciais em um arquivo para uso futuro
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
    
    return creds
