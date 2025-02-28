from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
import pickle
import os

CLIENT_SECRET_FILE = 'C:\\Users\\vmarc\\OneDrive\\Área de Trabalho\\new-finder\\client_secret.json'
SCOPES = ['https://mybusiness.googleapis.com']

def get_authenticated_service():
    creds = None
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRET_FILE, SCOPES)
            creds = flow.run_local_server(port=8080)
        
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)
    
    return build('API Google My Business', 'v4.9', credentials=creds)

def test_google_authentication():
    try:
        # Obtém o serviço autenticado
        service = get_authenticated_service()

        # Listando as contas
        accounts = service.accounts().list().execute()
        
        if 'accounts' in accounts:
            print(f'Contas encontradas: {len(accounts["accounts"])}')
            for account in accounts['accounts']:
                print(f"Account ID: {account['name']}")
        else:
            print('Nenhuma conta encontrada.')
    except Exception as e:
        print(f"Erro ao acessar a API: {e}")

# Testando a autenticação e a listagem
if __name__ == '__main__':
    test_google_authentication()
