import os
import io
from datetime import datetime
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload, MediaFileUpload
from google.oauth2.service_account import Credentials

def download_latest_csvs_from_drive(folder_id, download_dir):
    """
    Downloads the 2 most recent valid CSV files from a Google Drive folder.
    Valid CSVs are those named 'YYYY-MM.csv' with a date <= current date.
    
    Returns:
        str: The path to the directory containing the downloaded files, or None if failed.
    """
    print(f"Buscando as bases gerais no Google Drive...")
    
    path_script = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    cred_path = os.path.join(path_script, "chaveGoogle.json")
    
    if not os.path.exists(cred_path):
        print(f"Erro: Arquivo de credenciais não encontrado em {cred_path}")
        return None

    # Autenticação
    scopes = ['https://www.googleapis.com/auth/drive.readonly']
    try:
        creds = Credentials.from_service_account_file(cred_path, scopes=scopes)
        service = build('drive', 'v3', credentials=creds)
    except Exception as e:
        print(f"Erro ao autenticar no Google Drive: {e}")
        return None

    # Listar arquivos na pasta (suporte a Drives Compartilhados)
    try:
        results = service.files().list(
            q=f"'{folder_id}' in parents and trashed=false and mimeType='text/csv'",
            fields="nextPageToken, files(id, name, mimeType)",
            pageSize=100,
            supportsAllDrives=True,
            includeItemsFromAllDrives=True
        ).execute()
        items = results.get('files', [])
    except Exception as e:
        print(f"Erro ao listar arquivos do drive: {e}")
        return None

    if not items:
        print("Nenhum arquivo CSV encontrado na pasta especificada do Drive.")
        return None

    # Filtrar e ordenar arquivos
    current_date = datetime.now()
    valid_files = []

    for item in items:
        filename = item['name']
        try:
            # Extrai a data do nome do arquivo (formato YYYY-MM)
            date = datetime.strptime(filename.split('.')[0], '%Y-%m')
            
            # Formata a data atual para comparar apenas mês e ano
            if date <= current_date:
                valid_files.append((date, item))
        except ValueError:
            # Ignora arquivos com nomes que não seguem o formato esperado
            continue

    # Ordena os arquivos por data em ordem decrescente
    valid_files.sort(reverse=True, key=lambda x: x[0])
    
    # Pegar apenas os 2 mais recentes
    top_2 = valid_files[:2]
    
    if not top_2:
        print("Nenhum arquivo CSV válido com base na data foi encontrado.")
        return None

    os.makedirs(download_dir, exist_ok=True)

    print(f"Arquivos selecionados para download: {[item['name'] for _, item in top_2]}")

    # Fazer o download
    try:
        for _, item in top_2:
            request = service.files().get_media(fileId=item['id'])
            file_path = os.path.join(download_dir, item['name'])
            
            with open(file_path, 'wb') as fh:
                downloader = MediaIoBaseDownload(fh, request)
                done = False
                while done is False:
                    status, done = downloader.next_chunk()
        
        print(f"Download das bases gerais concluído com sucesso para {download_dir}")
        return download_dir

    except Exception as e:
        print(f"Erro ao fazer download do arquivo: {e}")
        return None

def download_all_csvs_from_drive(folder_id, download_dir):
    """
    Downloads ALL valid CSV files from a Google Drive folder.
    
    Returns:
        str: The path to the directory containing the downloaded files, or None if failed.
    """
    print(f"Buscando TODOS os arquivos na pasta do Google Drive (ID: {folder_id})...")
    
    path_script = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    cred_path = os.path.join(path_script, "chaveGoogle.json")
    
    if not os.path.exists(cred_path):
        print(f"Erro: Arquivo de credenciais não encontrado em {cred_path}")
        return None

    scopes = ['https://www.googleapis.com/auth/drive.readonly']
    try:
        creds = Credentials.from_service_account_file(cred_path, scopes=scopes)
        service = build('drive', 'v3', credentials=creds)
    except Exception as e:
        print(f"Erro ao autenticar no Google Drive: {e}")
        return None

    try:
        results = service.files().list(
            q=f"'{folder_id}' in parents and trashed=false and mimeType='text/csv'",
            fields="nextPageToken, files(id, name, mimeType)",
            pageSize=1000,
            supportsAllDrives=True,
            includeItemsFromAllDrives=True
        ).execute()
        items = results.get('files', [])
    except Exception as e:
        print(f"Erro ao listar arquivos do drive: {e}")
        return None

    if not items:
        print("Nenhum arquivo CSV encontrado na pasta especificada do Drive.")
        return None

    os.makedirs(download_dir, exist_ok=True)
    print(f"Total de {len(items)} arquivos encontrados. Baixando...")

    try:
        for item in items:
            request = service.files().get_media(fileId=item['id'])
            file_path = os.path.join(download_dir, item['name'])
            
            with open(file_path, 'wb') as fh:
                downloader = MediaIoBaseDownload(fh, request)
                done = False
                while done is False:
                    status, done = downloader.next_chunk()
        
        print(f"Download das bases concluído com sucesso para {download_dir}")
        return download_dir

    except Exception as e:
        print(f"Erro ao fazer download dos arquivos: {e}")
        return None

def download_docx_from_drive(folder_id, download_dir):
    """
    Downloads ALL valid .docx files from a Google Drive folder.
    
    Returns:
        str: The path to the directory containing the downloaded files, or None if failed.
    """
    print(f"Buscando arquivos DOCX na pasta do Google Drive (ID: {folder_id})...")
    
    path_script = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    cred_path = os.path.join(path_script, "chaveGoogle.json")
    
    if not os.path.exists(cred_path):
        print(f"Erro: Arquivo de credenciais não encontrado em {cred_path}")
        return None

    scopes = ['https://www.googleapis.com/auth/drive.readonly']
    try:
        creds = Credentials.from_service_account_file(cred_path, scopes=scopes)
        service = build('drive', 'v3', credentials=creds)
    except Exception as e:
        print(f"Erro ao autenticar no Google Drive: {e}")
        return None

    try:
        # Busca files com nome .docx ou mimetype especifico de word docs
        results = service.files().list(
            q=f"'{folder_id}' in parents and trashed=false and name contains '.docx'",
            fields="nextPageToken, files(id, name, mimeType)",
            pageSize=1000,
            supportsAllDrives=True,
            includeItemsFromAllDrives=True
        ).execute()
        items = results.get('files', [])
    except Exception as e:
        print(f"Erro ao listar arquivos do drive: {e}")
        return None

    if not items:
        print("Nenhum arquivo DOCX encontrado na pasta especificada do Drive.")
        return None

    os.makedirs(download_dir, exist_ok=True)
    print(f"Total de {len(items)} arquivos encontrados. Baixando...")

    try:
        for item in items:
            request = service.files().get_media(fileId=item['id'])
            file_path = os.path.join(download_dir, item['name'])
            
            # Se o arquivo já existe, pular o download para otimizar (somente templates docs)
            # Como vamos rodar repetidas vezes, é útil
            if not os.path.exists(file_path):
                with open(file_path, 'wb') as fh:
                    downloader = MediaIoBaseDownload(fh, request)
                    done = False
                    while done is False:
                        status, done = downloader.next_chunk()
        
        print(f"Download dos DOCX concluído com sucesso para {download_dir}")
        return download_dir

    except Exception as e:
        print(f"Erro ao fazer download dos arquivos DOCX: {e}")
        return None

def upload_file_to_drive(local_file_path, folder_id, drive_filename=None):
    """
    Faz o upload de um arquivo local para uma pasta específica do Google Drive.
    Se um arquivo com o mesmo nome já existir, ele será substituído (atualizado).
    """
    print(f"Iniciando upload do arquivo '{local_file_path}' para o Google Drive...")
    
    path_script = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    cred_path = os.path.join(path_script, "chaveGoogle.json")
    
    if not os.path.exists(cred_path):
        print(f"Erro: Arquivo de credenciais não encontrado em {cred_path}")
        return False

    if drive_filename is None:
        drive_filename = os.path.basename(local_file_path)

    # Autenticação com permissão de escrita
    scopes = ['https://www.googleapis.com/auth/drive']
    try:
        creds = Credentials.from_service_account_file(cred_path, scopes=scopes)
        service = build('drive', 'v3', credentials=creds)
    except Exception as e:
        print(f"Erro ao autenticar no Google Drive: {e}")
        return False

    # Procurar arquivo existente para atualizar
    try:
        results = service.files().list(
            q=f"'{folder_id}' in parents and name='{drive_filename}' and trashed=false",
            fields="files(id, name)",
            supportsAllDrives=True,
            includeItemsFromAllDrives=True
        ).execute()
        items = results.get('files', [])
        
        media = MediaFileUpload(local_file_path, resumable=True)
        
        if items:
            # Arquivo já existe, vamos atualizar o primeiro encontrado
            file_id = items[0]['id']
            print(f"Arquivo '{drive_filename}' já existe no Drive. Atualizando arquivo atual... (ID: {file_id})")
            updated_file = service.files().update(
                fileId=file_id,
                media_body=media,
                supportsAllDrives=True
            ).execute()
            print(f"Upload concluído. Arquivo atualizado (ID: {updated_file.get('id')})")
        else:
            # Arquivo não existe, vamos criar um novo
            print(f"Criando novo arquivo '{drive_filename}' no Drive...")
            file_metadata = {
                'name': drive_filename,
                'parents': [folder_id]
            }
            new_file = service.files().create(
                body=file_metadata,
                media_body=media,
                fields='id',
                supportsAllDrives=True
            ).execute()
            print(f"Upload concluído. Novo arquivo criado (ID: {new_file.get('id')})")
            
        return True
    except Exception as e:
        print(f"Erro ao fazer upload do arquivo para o Drive: {e}")
        return False
