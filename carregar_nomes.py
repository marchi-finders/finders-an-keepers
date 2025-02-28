def carregar_nomes(arquivo="nomes.txt"):
    try:
        with open(arquivo, "r", encoding="utf-8") as f:
            dados = []
            for linha in f.readlines():
                linha = linha.strip()
                if linha:
                    partes = linha.split(",")  # Separar nome e estado
                    if len(partes) == 2:
                        nome = partes[0].strip()
                        estado = partes[1].strip()
                        dados.append((nome, estado))  # Salvar como tupla (nome, estado)
            return dados
    except FileNotFoundError:
        print(f"Erro: O arquivo {arquivo} não foi encontrado.")
        return []
