import subprocess
from flask import Flask, request, render_template, redirect, url_for
import os
import sys
import codecs

# Configuração do Flask para procurar templates no diretório específico
app = Flask(__name__, template_folder=r'C:/Users/vmarc/OneDrive/Área de Trabalho/new-finder/static/templates')

# Caminho para o arquivo de nomes
CAMINHO_ARQUIVO = r'C:/Users/vmarc/OneDrive/Área de Trabalho/new-finder/nomes.txt'
CAMINHO_SCRIPT = r'C:/Users/vmarc/OneDrive/Área de Trabalho/new-finder/buscar_psicologos.py'
CAMINHO_SCRIPT_FISIO = r'C:/Users/vmarc/OneDrive/Área de Trabalho/new-finder/buscar_fisio.py'
CAMINHO_SCRIPT_NUTRI = r'C:/Users/vmarc/OneDrive/Área de Trabalho/new-finder/buscar_nutricionistas.py'

# Função para adicionar os nomes ao arquivo
def adicionar_nomes_ao_arquivo(nomes):
    with open(CAMINHO_ARQUIVO, 'a', encoding='utf-8') as arquivo:
        for nome in nomes:
            arquivo.write(nome.strip() + ',\n')

@app.route('/')
def index():
    # Exibe a primeira tela com o botão
    return render_template('primeira_tela.html')

@app.route('/segunda')
def segunda():
    # Exibe a segunda tela para adicionar os nomes
    return render_template('segunda_tela.html')

@app.route('/adicionar_nomes', methods=['POST'])
def adicionar_nomes():
    # Recebe os nomes do formulário
    nomes_input = request.form['nomes']
    
    # Divide os nomes digitados pelo usuário (presumindo que estejam separados por linha)
    nomes = nomes_input.splitlines()
    
    # Adiciona os nomes ao arquivo
    adicionar_nomes_ao_arquivo(nomes)
    
    return '''<script>
                alert("Nomes adicionados com sucesso!");
                window.location.href = "/segunda";
              </script>'''

@app.route('/rodar_script', methods=['POST'])
def rodar_script():
    print(f"Usando Python: {sys.executable}")  # Mostra qual Python está rodando
    try:
        # Executa o script externo
        subprocess.run([sys.executable, CAMINHO_SCRIPT], capture_output=True, text=True, check=True)
        
        # Após rodar o script, redireciona automaticamente para "/resultado"
        return redirect(url_for('resultado'))
    
    except subprocess.CalledProcessError as e:
        return f"Erro ao executar o script:\n{e.stderr or e.output}"
    
if __name__ == '__main__':
    # Cria o arquivo de nomes se ele não existir
    if not os.path.exists(CAMINHO_ARQUIVO):
        with open(CAMINHO_ARQUIVO, 'w', encoding='utf-8'):
            pass  

@app.route('/pesquisar_fisioterapeutas', methods=['POST'])
def pesquisar_fisioterapeutas():
    print(f"Usando Python: {sys.executable}")
    try:
        subprocess.run([sys.executable, CAMINHO_SCRIPT_FISIO], capture_output=True, text=True, check=True)
        return redirect(url_for('resultado'))
    except subprocess.CalledProcessError as e:
        return f"Erro ao executar o script de fisioterapeutas:\n{e.stderr or e.output}"

@app.route('/pesquisar_nutricionistas', methods=['POST'])
def pesquisar_nutricionistas():
    print(f"Usando Python: {sys.executable}")
    try:
        subprocess.run([sys.executable, CAMINHO_SCRIPT_NUTRI], capture_output=True, text=True, check=True)
        return redirect(url_for('resultado'))
    except subprocess.CalledProcessError as e:
        return f"Erro ao executar o script de nutricionistas:\n{e.stderr or e.output}"

@app.route('/resultado')
def resultado():
    try:
        with open('profissionais_sem_ficha.txt', 'r', encoding='utf-8-sig') as file:
            profissionais_sem_ficha = file.readlines()
    except Exception as e:
        profissionais_sem_ficha = [f"Erro ao ler o arquivo: {str(e)}"]
    
    return render_template('terceira_tela.html', profissionais_sem_ficha=profissionais_sem_ficha)

class CustomCodec(codecs.Codec):
    def decode(self, input, errors='strict'):
        decoding_table = {i: chr(i) for i in range(256)}  # Exemplo de tabela de decodificação
        return codecs.charmap_decode(input, errors, decoding_table)

@app.route('/limpar_arquivos', methods=['POST'])
def limpar_arquivos():
    # Caminhos dos arquivos
    arquivos = ['profissionais_sem_ficha.txt', 'nomes.txt']
    
    # Limpa o conteúdo dos arquivos
    for arquivo in arquivos:
        with open(arquivo, 'w') as f:
            f.truncate(0)  # Limpa o conteúdo do arquivo
    
    # Redireciona para a página anterior (ou qualquer outra página de sua escolha)
    return redirect(url_for('segunda'))

# Roda o servidor Flask
app.run(debug=True)



