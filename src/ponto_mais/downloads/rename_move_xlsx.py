import os
import shutil
from datetime import datetime
from time import sleep

# Caminho para a pasta de downloads e pasta de destino
pasta_downloads = os.path.join(os.path.expanduser("~"), "Downloads")


def get_last_xlsx(pasta):
    print("Iniciando busca pelo arquivo xlsx baixado!")
    # Lista todos os arquivos .xlsx na pasta de downloads
    arquivos = [f for f in os.listdir(pasta) if f.endswith('.xlsx')]
    
    if not arquivos:
        print("Nenhum arquivo .xlsx encontrado.")
        return None

    # Caminho completo de cada arquivo
    caminhos_arquivos = [os.path.join(pasta, f) for f in arquivos]

    # Identifica o arquivo mais recente
    arquivo_mais_recente = max(caminhos_arquivos, key=os.path.getctime)
    
    return arquivo_mais_recente

def move_file(arquivo, destino):
    print("Movendo o arquivo xlsx para seu destino: " + destino)
    if not os.path.exists(destino):
        os.makedirs(destino)

    try:
        # Move o arquivo para a pasta de destino
        shutil.move(arquivo, destino)
        print(f"Arquivo {os.path.basename(arquivo)} movido para {destino}")
        return os.path.basename(arquivo)
    except Exception as e:
        print(f"Erro ao mover arquivo: {e}")

    return os.path.basename(arquivo)

def rename_file(caminho_arquivo, novo_nome):
    # Pega o diretório do arquivo e cria o caminho com o novo nome
    novo_caminho = os.path.join(caminho_arquivo, novo_nome)
    
    try:
        os.rename(caminho_arquivo, novo_caminho)
        print(f"Arquivo renomeado para {novo_nome}")
    except Exception as e:
        print(f"Erro ao renomear arquivo: {e}")

def xlsx_move(relatorio,operation):
    # Localiza o último arquivo .xlsx baixado
    last_file = get_last_xlsx(pasta_downloads)
    # Move o arquivo para a pasta de destino, se encontrado
    if last_file:
        pasta_destino = "C:/Users/hp-gustav/Downloads/" + relatorio + "/operations/" + operation # Alterar para diretório de downloads
        file_name = move_file(last_file, pasta_destino)
        sleep(15)
        
        print("Renomeando arquivo!")
        rename_file(pasta_destino + "/" + file_name, pasta_destino + "/ " + operation + " PontoMais " + relatorio + ".xlsx")


        